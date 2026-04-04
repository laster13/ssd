import re
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
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

INSTALL_JOB_TYPES = ["install_app", "install_ssdv2", "uninstall_app"]

SUBDOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])?$")

SENSITIVE_JOB_PAYLOAD_KEYS = {
    "password",
    "cloudflare_login",
    "cloudflare_api_key",
    "oauth_client",
    "oauth_secret",
}


class CreateMyUninstallationRequest(BaseModel):
    machine_id: UUID
    app_slug: str


def has_non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalize_optional_string(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value)


def dump_model_updates(model: BaseModel) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_unset=True)
    return model.dict(exclude_unset=True)


def build_machine_settings_response(settings: MachineSettings) -> MachineSettingsResponse:
    return MachineSettingsResponse(
        machine_id=settings.machine_id,
        username=settings.username,
        email=settings.email,
        domain=settings.domain,
        oauth_enabled=settings.oauth_enabled,
        oauth_mail=settings.oauth_mail,
        password_configured=has_non_empty(settings.password),
        cloudflare_login_configured=has_non_empty(settings.cloudflare_login),
        cloudflare_api_key_configured=has_non_empty(settings.cloudflare_api_key),
        oauth_client_configured=has_non_empty(settings.oauth_client),
        oauth_secret_configured=has_non_empty(settings.oauth_secret),
        created_at=settings.created_at,
        updated_at=settings.updated_at,
    )


def redact_job_payload(payload: dict | None) -> dict | None:
    if not isinstance(payload, dict):
        return payload

    redacted = dict(payload)

    for key in SENSITIVE_JOB_PAYLOAD_KEYS:
        if key in redacted:
            redacted.pop(key, None)
            redacted[f"{key}_configured"] = True

    return redacted


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


def get_machine_settings_or_400(db: Session, machine_id: UUID) -> MachineSettings:
    stmt = (
        select(MachineSettings)
        .where(MachineSettings.machine_id == machine_id)
        .limit(1)
    )
    settings = db.execute(stmt).scalar_one_or_none()

    if not settings:
        raise HTTPException(status_code=400, detail="Machine settings not found")

    return settings


def validate_machine_settings_for_install(settings: MachineSettings) -> None:
    required_fields = {
        "username": settings.username,
        "email": settings.email,
        "domain": settings.domain,
        "password": settings.password,
        "cloudflare_login": settings.cloudflare_login,
        "cloudflare_api_key": settings.cloudflare_api_key,
    }

    missing = [key for key, value in required_fields.items() if not str(value or "").strip()]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required machine settings: {', '.join(missing)}",
        )

    if settings.oauth_enabled:
        oauth_required = {
            "oauth_client": settings.oauth_client,
            "oauth_secret": settings.oauth_secret,
            "oauth_mail": settings.oauth_mail,
        }
        oauth_missing = [key for key, value in oauth_required.items() if not str(value or "").strip()]
        if oauth_missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required OAuth settings: {', '.join(oauth_missing)}",
            )


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

    return build_machine_settings_response(settings)


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

    updates = dump_model_updates(payload)

    string_fields = {
        "username",
        "email",
        "domain",
        "password",
        "cloudflare_login",
        "cloudflare_api_key",
        "oauth_client",
        "oauth_secret",
        "oauth_mail",
    }

    for field in string_fields:
        if field in updates:
            setattr(settings, field, normalize_optional_string(updates[field]))

    if "oauth_enabled" in updates:
        settings.oauth_enabled = bool(updates["oauth_enabled"])

    db.commit()
    db.refresh(settings)

    return build_machine_settings_response(settings)


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
    settings = get_machine_settings_or_400(db, machine.id)
    validate_machine_settings_for_install(settings)
    ensure_no_active_installation_for_machine(db, machine)

    payload = {
        "machine_id": str(machine.id),
        "hostname": machine.hostname,
        "username": settings.username,
        "email": settings.email,
        "domain": settings.domain,
        "password": settings.password,
        "cloudflare_login": settings.cloudflare_login,
        "cloudflare_api_key": settings.cloudflare_api_key,
        "oauth_enabled": settings.oauth_enabled,
        "oauth_client": settings.oauth_client,
        "oauth_secret": settings.oauth_secret,
        "oauth_mail": settings.oauth_mail,
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
        payload=redact_job_payload(job.payload),
    )


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
        payload=redact_job_payload(job.payload),
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
        payload=redact_job_payload(job.payload),
    )


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
            payload=redact_job_payload(job.payload),
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
        payload=redact_job_payload(job.payload),
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