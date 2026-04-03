import re
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.catalog.apps import get_catalog_app
from app.core.audit import audit_event
from app.core.database import get_db
from app.models.job import Job
from app.models.job_log import JobLog
from app.models.machine import Machine
from app.models.machine_settings import MachineSettings
from app.models.user import User
from app.schemas.job import (
    AdminJobListItem,
    AdminJobResponse,
    CreateMachineJobResponse,
    CreateMyInstallationRequest,
)
from app.schemas.job_log import AdminJobLogItem
from app.schemas.machine_settings import (
    MachineSettingsResponse,
    UpdateMachineSettingsRequest,
)

router = APIRouter(prefix="/me", tags=["me"])

ALLOWED_AUTH_TYPES = {
    "aucune",
    "basique",
    "oauth",
    "authelia",
    "oauth2-proxy",
}

SUBDOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])?$")


def get_owned_machine_or_404(db: Session, machine_id: UUID, current_user: User) -> Machine:
    stmt = (
        select(Machine)
        .where(Machine.id == machine_id)
        .where(Machine.owner_id == current_user.id)
        .where(Machine.status == "paired")
        .limit(1)
    )
    machine = db.execute(stmt).scalar_one_or_none()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    return machine


@router.get("/machines/{machine_id}/settings", response_model=MachineSettingsResponse)
def get_machine_settings(
    machine_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, machine_id, current_user)

    stmt = select(MachineSettings).where(MachineSettings.machine_id == machine.id)
    settings = db.execute(stmt).scalar_one_or_none()

    if settings is None:
        settings = MachineSettings(
            machine_id=machine.id,
            oauth_enabled=False,
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return MachineSettingsResponse(
        machine_id=settings.machine_id,
        username=settings.username,
        email=settings.email,
        domain=settings.domain,
        password=settings.password,
        cloudflare_login=settings.cloudflare_login,
        cloudflare_api_key=settings.cloudflare_api_key,
        oauth_enabled=settings.oauth_enabled,
        oauth_client=settings.oauth_client,
        oauth_secret=settings.oauth_secret,
        oauth_mail=settings.oauth_mail,
        created_at=settings.created_at,
        updated_at=settings.updated_at,
    )


@router.patch("/machines/{machine_id}/settings", response_model=MachineSettingsResponse)
def update_machine_settings(
    machine_id: UUID,
    payload: UpdateMachineSettingsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, machine_id, current_user)

    stmt = select(MachineSettings).where(MachineSettings.machine_id == machine.id)
    settings = db.execute(stmt).scalar_one_or_none()

    if settings is None:
        settings = MachineSettings(machine_id=machine.id, oauth_enabled=False)
        db.add(settings)

    settings.username = payload.username
    settings.email = payload.email
    settings.domain = payload.domain
    settings.password = payload.password
    settings.cloudflare_login = payload.cloudflare_login
    settings.cloudflare_api_key = payload.cloudflare_api_key
    settings.oauth_enabled = payload.oauth_enabled
    settings.oauth_client = payload.oauth_client
    settings.oauth_secret = payload.oauth_secret
    settings.oauth_mail = payload.oauth_mail

    db.commit()
    db.refresh(settings)

    return MachineSettingsResponse(
        machine_id=settings.machine_id,
        username=settings.username,
        email=settings.email,
        domain=settings.domain,
        password=settings.password,
        cloudflare_login=settings.cloudflare_login,
        cloudflare_api_key=settings.cloudflare_api_key,
        oauth_enabled=settings.oauth_enabled,
        oauth_client=settings.oauth_client,
        oauth_secret=settings.oauth_secret,
        oauth_mail=settings.oauth_mail,
        created_at=settings.created_at,
        updated_at=settings.updated_at,
    )


def get_owned_installation_or_404(db: Session, job_id: UUID, current_user: User) -> Job:
    stmt = (
        select(Job)
        .join(Machine, Job.machine_id == Machine.id)
        .where(Job.id == job_id)
        .where(Job.type == "install_app")
        .where(Machine.owner_id == current_user.id)
        .limit(1)
    )
    job = db.execute(stmt).scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Installation not found")

    return job


def normalize_and_validate_installation_payload(
    payload: CreateMyInstallationRequest,
) -> tuple[str, str, str, str]:
    requested_slug = payload.app_slug.strip()
    auth_type = payload.auth_type.strip().lower()
    subdomain = payload.subdomain.strip().lower()

    catalog_app = get_catalog_app(requested_slug)
    if not catalog_app:
        raise HTTPException(status_code=400, detail="Unsupported app_slug")

    if not catalog_app.get("enabled", False):
        raise HTTPException(status_code=400, detail="App is currently disabled")

    allowed_auth_types = set(catalog_app["allowed_auth_types"])
    if auth_type not in allowed_auth_types:
        raise HTTPException(status_code=400, detail="Unsupported auth_type for this app")

    if not SUBDOMAIN_RE.fullmatch(subdomain):
        raise HTTPException(
            status_code=400,
            detail="Invalid subdomain. Use lowercase letters, numbers and hyphens only.",
        )

    install_profile = str(catalog_app["install_profile"]).strip()
    if not install_profile:
        raise HTTPException(status_code=500, detail="App install profile is missing")

    return catalog_app["slug"], subdomain, auth_type, install_profile


def ensure_no_active_installation_for_machine(db: Session, machine: Machine) -> None:
    stmt = (
        select(Job.id)
        .where(Job.machine_id == machine.id)
        .where(Job.type == "install_app")
        .where(Job.status.in_(["pending", "claimed", "running"]))
        .limit(1)
    )
    active_job_id = db.execute(stmt).scalar_one_or_none()

    if active_job_id:
        raise HTTPException(
            status_code=409,
            detail="An installation is already in progress for this machine",
        )


@router.get("/machines")
def get_my_machines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Machine)
        .where(Machine.owner_id == current_user.id)
        .where(Machine.status == "paired")
        .order_by(Machine.created_at.desc())
    )
    machines = db.execute(stmt).scalars().all()

    return [
        {
            "id": machine.id,
            "machine_uuid": machine.machine_uuid,
            "status": machine.status,
            "hostname": machine.hostname,
            "agent_version": machine.agent_version,
            "ssdv2_installed": machine.ssdv2_installed,
            "ssdv2_checked_at": machine.ssdv2_checked_at,
            "last_seen_at": machine.last_seen_at,
            "created_at": machine.created_at,
            "updated_at": machine.updated_at,
        }
        for machine in machines
    ]


@router.delete("/machines/{machine_id}")
def delete_my_machine(
    machine_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, machine_id, current_user)

    machine.status = "revoked"
    machine.auth_token_hash = None
    machine.auth_token_created_at = None

    db.commit()
    db.refresh(machine)

    audit_event(
        event_type="machine.revoke.user.success",
        severity="warning",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_machine_id=machine.id,
        request=request,
        description="User revoked machine pairing",
        details={"machine_uuid": str(machine.machine_uuid)},
    )

    return {
        "ok": True,
        "machine_id": str(machine.id),
        "status": machine.status,
    }


@router.post("/installations", response_model=CreateMachineJobResponse)
def create_my_installation(
    payload: CreateMyInstallationRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, payload.machine_id, current_user)
    app_slug, subdomain, auth_type, install_profile = normalize_and_validate_installation_payload(
        payload
    )
    ensure_no_active_installation_for_machine(db, machine)

    job = Job(
        machine_id=machine.id,
        type="install_app",
        status="pending",
        payload={
            "app_slug": app_slug,
            "install_profile": install_profile,
            "subdomain": subdomain,
            "auth_type": auth_type,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    audit_event(
        event_type="job.create.user.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_machine_id=machine.id,
        request=request,
        description="User created install job",
        details={"job_id": str(job.id), "payload": job.payload},
    )

    return CreateMachineJobResponse(
        job_id=job.id,
        machine_id=job.machine_id,
        status=job.status,
        type=job.type,
        payload=job.payload,
    )


@router.get("/installations", response_model=list[AdminJobListItem])
def list_my_installations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Job)
        .join(Machine, Job.machine_id == Machine.id)
        .where(Job.type == "install_app")
        .where(Machine.owner_id == current_user.id)
        .order_by(Job.created_at.desc())
    )
    jobs = db.execute(stmt).scalars().all()

    return [
        AdminJobListItem(
            id=job.id,
            machine_id=job.machine_id,
            type=job.type,
            status=job.status,
            payload=job.payload,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]


@router.get("/installations/{job_id}", response_model=AdminJobResponse)
def get_my_installation(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_owned_installation_or_404(db, job_id, current_user)

    return AdminJobResponse(
        id=job.id,
        machine_id=job.machine_id,
        type=job.type,
        status=job.status,
        payload=job.payload,
        result=job.result,
        error_message=job.error_message,
        claimed_at=job.claimed_at,
        completed_at=job.completed_at,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.get("/installations/{job_id}/logs", response_model=list[AdminJobLogItem])
def get_my_installation_logs(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_owned_installation_or_404(db, job_id, current_user)

    stmt = (
        select(JobLog)
        .where(JobLog.job_id == job.id)
        .order_by(JobLog.seq.asc(), JobLog.created_at.asc())
    )
    logs = db.execute(stmt).scalars().all()

    return [
        AdminJobLogItem(
            id=log.id,
            job_id=log.job_id,
            seq=log.seq,
            level=log.level,
            message=log.message,
            created_at=log.created_at,
        )
        for log in logs
    ]