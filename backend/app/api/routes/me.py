import re
from urllib.parse import urlparse
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.catalog.apps import get_catalog_app
from app.core.audit import audit_event
from app.core.database import get_db
from app.models.application_state import ApplicationState
from app.models.job import Job
from app.models.job_log import JobLog
from app.models.machine import Machine
from app.models.user import User
from app.schemas.job import (
    AdminJobListItem,
    AdminJobResponse,
    CreateMachineJobResponse,
    CreateMyInstallationRequest,
)
from app.schemas.job_log import AdminJobLogItem

router = APIRouter(prefix="/me", tags=["me"])

INSTALL_JOB_TYPES = ["install_app", "install_ssdv2", "uninstall_app"]

SUBDOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])?$")
PUBLIC_URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
HOSTNAME_RE = re.compile(
    r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b",
    re.IGNORECASE,
)

IGNORED_HOSTS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
}


class CreateMyUninstallationRequest(BaseModel):
    machine_id: UUID
    app_slug: str


def _clean_public_url(value: str) -> str:
    return value.rstrip(").,;\"'")


def _clean_hostname(value: str) -> str:
    return value.rstrip(").,;\"'").lower()


def _looks_like_public_host(hostname: str) -> bool:
    if not hostname:
        return False
    if hostname in IGNORED_HOSTS:
        return False
    if "." not in hostname:
        return False
    return True


def _extract_public_url_from_messages(
    messages: list[str],
    preferred_subdomain: str | None = None,
) -> str | None:
    fallback_url: str | None = None
    fallback_host: str | None = None
    preferred_prefix = f"{preferred_subdomain.lower()}." if preferred_subdomain else None

    for message in messages:
        if not message:
            continue

        for raw_url in PUBLIC_URL_RE.findall(message):
            url = _clean_public_url(raw_url)
            parsed = urlparse(url)
            hostname = (parsed.hostname or "").lower()
            if not _looks_like_public_host(hostname):
                continue
            if preferred_prefix and hostname.startswith(preferred_prefix):
                return url
            if fallback_url is None:
                fallback_url = url

        for raw_host in HOSTNAME_RE.findall(message):
            hostname = _clean_hostname(raw_host)
            if not _looks_like_public_host(hostname):
                continue
            rebuilt_url = f"https://{hostname}"
            if preferred_prefix and hostname.startswith(preferred_prefix):
                return rebuilt_url
            if fallback_host is None:
                fallback_host = rebuilt_url

    return fallback_url or fallback_host


def _find_latest_install_job_for_app(db: Session, state: ApplicationState) -> Job | None:
    stmt = (
        select(Job)
        .where(Job.machine_id == state.machine_id)
        .where(Job.type == "install_app")
        .order_by(Job.created_at.desc())
    )
    jobs = db.execute(stmt).scalars().all()

    wanted_slug = (state.app_slug or "").strip().lower()
    for job in jobs:
        payload = job.payload or {}
        payload_slug = str(payload.get("app_slug") or "").strip().lower()
        if payload_slug == wanted_slug:
            return job

    return None


def resolve_application_public_url(db: Session, state: ApplicationState) -> str | None:
    if not state.present:
        return None
    if state.transition != "idle":
        return None
    if state.source == "local":
        return state.public_url

    job = _find_latest_install_job_for_app(db, state)
    if job is None:
        return None

    payload = job.payload or {}
    preferred_subdomain = str(payload.get("subdomain") or "").strip().lower() or None

    stmt = (
        select(JobLog.message)
        .where(JobLog.job_id == job.id)
        .order_by(JobLog.seq.desc(), JobLog.created_at.desc())
    )
    messages = db.execute(stmt).scalars().all()
    return _extract_public_url_from_messages(messages, preferred_subdomain)


def build_application_state_response(db: Session, state: ApplicationState) -> dict:
    return {
        "id": state.id,
        "machine_id": state.machine_id,
        "app_slug": state.app_slug,
        "app_name": state.app_name,
        "source": state.source,
        "present": state.present,
        "transition": state.transition,
        "last_operation": state.last_operation,
        "last_job_id": state.last_job_id,
        "last_job_status": state.last_job_status,
        "last_error": state.last_error,
        "installed_at": state.installed_at,
        "created_at": state.created_at,
        "updated_at": state.updated_at,
        "public_url": resolve_application_public_url(db, state),
    }


def get_or_create_application_state(
    db: Session,
    machine_id: UUID,
    app_slug: str,
    app_name: str | None = None,
) -> ApplicationState:
    stmt = (
        select(ApplicationState)
        .where(ApplicationState.machine_id == machine_id)
        .where(ApplicationState.app_slug == app_slug)
        .limit(1)
    )
    state = db.execute(stmt).scalar_one_or_none()

    if state is None:
        state = ApplicationState(
            machine_id=machine_id,
            app_slug=app_slug,
            app_name=app_name,
        )
        db.add(state)
    elif app_name:
        state.app_name = app_name

    return state


def queue_application_state_for_new_job(
    db: Session,
    *,
    machine_id: UUID,
    app_slug: str,
    app_name: str,
    operation: str,
    job: Job,
) -> None:
    state = get_or_create_application_state(
        db=db,
        machine_id=machine_id,
        app_slug=app_slug,
        app_name=app_name,
    )
    state.app_name = app_name
    state.source = "ssd"
    state.last_operation = operation
    state.last_job_id = job.id
    state.last_job_status = job.status
    state.last_error = None
    state.transition = "installing" if operation == "install" else "uninstalling"


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


def get_owned_installation_or_404(db: Session, job_id: UUID, current_user: User) -> Job:
    stmt = (
        select(Job)
        .join(Machine, Job.machine_id == Machine.id)
        .where(Job.id == job_id)
        .where(Job.type.in_(INSTALL_JOB_TYPES))
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


def normalize_uninstall_app_slug(app_slug: str) -> tuple[str, str]:
    normalized_slug = app_slug.strip()
    if not normalized_slug:
        raise HTTPException(status_code=400, detail="app_slug is required")

    catalog_app = get_catalog_app(normalized_slug)
    if catalog_app:
        return catalog_app["slug"], str(catalog_app.get("name") or catalog_app["slug"])

    return normalized_slug, normalized_slug


def ensure_no_active_installation_for_machine(db: Session, machine: Machine) -> None:
    stmt = (
        select(Job.id)
        .where(Job.machine_id == machine.id)
        .where(Job.type.in_(INSTALL_JOB_TYPES))
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


@router.post("/machines/{machine_id}/install-ssdv2", response_model=CreateMachineJobResponse)
def create_ssdv2_installation(
    machine_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, machine_id, current_user)
    ensure_no_active_installation_for_machine(db, machine)

    payload = {
        "machine_id": str(machine.id),
        "hostname": machine.hostname,
    }
    job = Job(
        machine_id=machine.id,
        type="install_ssdv2",
        status="pending",
        payload=payload,
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
        description="User created SSDv2 install job",
        details={"job_id": str(job.id), "type": job.type},
    )

    return CreateMachineJobResponse(
        job_id=job.id,
        machine_id=job.machine_id,
        status=job.status,
        type=job.type,
        payload=job.payload,
    )


@router.post("/installations", response_model=CreateMachineJobResponse)
def create_my_installation(
    payload: CreateMyInstallationRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, payload.machine_id, current_user)
    app_slug, subdomain, auth_type, install_profile = normalize_and_validate_installation_payload(payload)

    catalog_app = get_catalog_app(app_slug)
    app_name = str(catalog_app.get("name") or app_slug) if catalog_app else app_slug

    ensure_no_active_installation_for_machine(db, machine)

    job = Job(
        machine_id=machine.id,
        type="install_app",
        status="pending",
        payload={
            "app_slug": app_slug,
            "app_name": app_name,
            "install_profile": install_profile,
            "subdomain": subdomain,
            "auth_type": auth_type,
        },
    )
    db.add(job)
    db.flush()

    queue_application_state_for_new_job(
        db,
        machine_id=machine.id,
        app_slug=app_slug,
        app_name=app_name,
        operation="install",
        job=job,
    )

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


@router.post("/uninstallations", response_model=CreateMachineJobResponse)
def create_my_uninstallation(
    payload: CreateMyUninstallationRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    machine = get_owned_machine_or_404(db, payload.machine_id, current_user)
    ensure_no_active_installation_for_machine(db, machine)

    app_slug, app_name = normalize_uninstall_app_slug(payload.app_slug)

    job = Job(
        machine_id=machine.id,
        type="uninstall_app",
        status="pending",
        payload={
            "app_slug": app_slug,
            "app_name": app_name,
        },
    )
    db.add(job)
    db.flush()

    queue_application_state_for_new_job(
        db,
        machine_id=machine.id,
        app_slug=app_slug,
        app_name=app_name,
        operation="uninstall",
        job=job,
    )

    db.commit()
    db.refresh(job)

    audit_event(
        event_type="job.uninstall.user.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_machine_id=machine.id,
        request=request,
        description="User created uninstall job",
        details={"job_id": str(job.id), "app_slug": app_slug},
    )

    return CreateMachineJobResponse(
        job_id=job.id,
        machine_id=job.machine_id,
        status=job.status,
        type=job.type,
        payload=job.payload,
    )


@router.get("/applications")
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(ApplicationState)
        .join(Machine, ApplicationState.machine_id == Machine.id)
        .where(Machine.owner_id == current_user.id)
        .order_by(ApplicationState.updated_at.desc(), ApplicationState.created_at.desc())
    )
    states = db.execute(stmt).scalars().all()
    return [build_application_state_response(db, state) for state in states]


@router.get("/installations", response_model=list[AdminJobListItem])
def list_my_installations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Job)
        .join(Machine, Job.machine_id == Machine.id)
        .where(Job.type.in_(INSTALL_JOB_TYPES))
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


@router.delete("/installations/{job_id}")
def delete_my_installation(
    job_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_owned_installation_or_404(db, job_id, current_user)

    if job.status in {"pending", "claimed", "running"}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An installation in progress cannot be deleted",
        )

    deleted_job_id = job.id
    target_machine_id = job.machine_id
    deleted_status = job.status
    deleted_job_type = job.type

    db.delete(job)
    db.commit()

    audit_event(
        event_type="job.delete.user.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_machine_id=target_machine_id,
        request=request,
        description="User deleted install job",
        details={
            "job_id": str(deleted_job_id),
            "job_status": deleted_status,
            "job_type": deleted_job_type,
        },
    )

    return {
        "ok": True,
        "job_id": str(deleted_job_id),
    }


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
