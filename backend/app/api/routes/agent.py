from datetime import datetime, timezone
import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.catalog.apps import get_catalog_app
from app.models.application_state import ApplicationState

from app.api.deps import get_current_machine
from app.core.database import get_db
from app.core.security import generate_machine_token, hash_machine_token
from app.core.ws import job_ws_manager, machine_presence_manager
from app.models.job import Job
from app.models.job_log import JobLog
from app.models.machine import Machine
from app.schemas.agent import AgentAuthResponse
from app.schemas.heartbeat import AgentHeartbeatRequest, AgentHeartbeatResponse
from app.schemas.job import (
    AdminJobResponse,
    AgentCompleteJobRequest,
    AgentCompleteJobResponse,
    AgentFetchJobResponse,
)
from app.schemas.job_log import (
    AgentCreateJobLogRequest,
    AgentCreateJobLogResponse,
)
from app.schemas.me import AgentMeResponse
from app.schemas.token import RotateMachineTokenResponse

router = APIRouter(prefix="/agent", tags=["agent"])

MAX_RESULT_BYTES = 64 * 1024

APPLICATION_JOB_TYPES = {"install_app", "uninstall_app"}
ACTIVE_JOB_STATUSES = {"pending", "claimed", "running"}


def normalize_discovered_app_slug(value: str | None) -> str | None:
    normalized = str(value or "").strip().lower()
    return normalized or None


def sync_local_application_inventory(db: Session, machine_id: UUID, installed_apps) -> None:
    if installed_apps is None:
        return

    seen_slugs: set[str] = set()

    for installed_app in installed_apps:
        app_slug = normalize_discovered_app_slug(getattr(installed_app, "app_slug", None))
        if not app_slug:
            continue

        seen_slugs.add(app_slug)

        raw_name = str(getattr(installed_app, "app_name", "") or "").strip()
        app_name = raw_name or app_slug
        public_url = str(getattr(installed_app, "public_url", "") or "").strip() or None

        state = get_or_create_application_state(
            db=db,
            machine_id=machine_id,
            app_slug=app_slug,
            app_name=app_name,
        )

        if state.transition != "idle":
            continue

        state.app_name = app_name
        state.present = True
        state.public_url = public_url

        # Toute app remontée par l'inventaire local est considérée locale.
        state.source = "local"

        # On nettoie les métadonnées de job si elle n'est pas réellement pilotée par SSD.
        if state.last_job_id is None:
            state.last_operation = None
            state.last_job_status = None
            state.last_error = None
            state.installed_at = None

    stmt = (
        select(ApplicationState)
        .where(ApplicationState.machine_id == machine_id)
        .where(ApplicationState.source == "local")
    )
    local_states = db.execute(stmt).scalars().all()

    for state in local_states:
        if state.app_slug in seen_slugs:
            continue

        if state.transition != "idle":
            continue

        state.present = False
        state.public_url = None
        state.installed_at = None


def get_job_application_identity(job: Job) -> tuple[str | None, str | None]:
    if job.type not in APPLICATION_JOB_TYPES:
        return None, None

    payload = job.payload if isinstance(job.payload, dict) else {}

    app_slug = str((payload.get("app_slug") or "")).strip()
    if not app_slug:
        return None, None

    app_name = str((payload.get("app_name") or "")).strip()
    if not app_name:
        catalog_app = get_catalog_app(app_slug)
        app_name = str(catalog_app.get("name") or app_slug) if catalog_app else app_slug

    return app_slug, app_name


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


def sync_application_state_from_job(db: Session, job: Job) -> None:
    app_slug, app_name = get_job_application_identity(job)
    if not app_slug:
        return

    state = get_or_create_application_state(
        db=db,
        machine_id=job.machine_id,
        app_slug=app_slug,
        app_name=app_name,
    )

    state.app_name = app_name
    state.source = "ssd"
    state.last_job_id = job.id
    state.last_job_status = job.status
    state.last_error = job.error_message
    state.last_operation = "install" if job.type == "install_app" else "uninstall"

    if job.status in ACTIVE_JOB_STATUSES:
        state.transition = "installing" if job.type == "install_app" else "uninstalling"
        return

    state.transition = "idle"

    if job.type == "install_app" and job.status == "completed":
        state.present = True
        state.installed_at = job.completed_at

    if job.type == "uninstall_app" and job.status == "completed":
        state.present = False
        state.installed_at = None


def build_machine_presence_event(machine: Machine) -> dict:
    connection_status = "online" if machine_presence_manager.is_machine_online(machine.id) else "offline"
    return {
        "type": "machine_presence",
        "machine": {
            "id": str(machine.id),
            "machine_uuid": str(machine.machine_uuid),
            "status": machine.status,
            "connection_status": connection_status,
            "hostname": machine.hostname,
            "agent_version": machine.agent_version,
            "ssdv2_installed": machine.ssdv2_installed,
            "ssdv2_checked_at": machine.ssdv2_checked_at.isoformat() if machine.ssdv2_checked_at else None,
            "last_seen_at": machine.last_seen_at.isoformat() if machine.last_seen_at else None,
            "created_at": machine.created_at.isoformat() if machine.created_at else None,
            "updated_at": machine.updated_at.isoformat() if machine.updated_at else None,
        },
    }


@router.post("/auth", response_model=AgentAuthResponse)
async def authenticate_agent(
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    machine.last_seen_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(machine)

    if machine.owner_id:
        await machine_presence_manager.broadcast_to_user(
            machine.owner_id,
            build_machine_presence_event(machine),
        )

    return AgentAuthResponse(
        authenticated=True,
        machine_id=machine.id,
        machine_uuid=machine.machine_uuid,
        status=machine.status,
    )


@router.get("/me", response_model=AgentMeResponse)
async def get_agent_me(machine: Machine = Depends(get_current_machine)):
    return AgentMeResponse(
        machine_id=machine.id,
        machine_uuid=machine.machine_uuid,
        status=machine.status,
        hostname=machine.hostname,
        agent_version=machine.agent_version,
        auth_token_created_at=machine.auth_token_created_at,
        last_seen_at=machine.last_seen_at,
        created_at=machine.created_at,
        updated_at=machine.updated_at,
    )


@router.post("/heartbeat", response_model=AgentHeartbeatResponse)
async def heartbeat(
    payload: AgentHeartbeatRequest,
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    if payload.hostname is not None:
        machine.hostname = payload.hostname

    if payload.agent_version is not None:
        machine.agent_version = payload.agent_version

    if payload.ssdv2_installed is not None:
        machine.ssdv2_installed = payload.ssdv2_installed
        machine.ssdv2_checked_at = now

    if payload.installed_apps is not None:
        sync_local_application_inventory(db, machine.id, payload.installed_apps)

    machine.last_seen_at = now

    db.commit()
    db.refresh(machine)

    if machine.owner_id:
        await machine_presence_manager.broadcast_to_user(
            machine.owner_id,
            build_machine_presence_event(machine),
        )

    return AgentHeartbeatResponse(
        ok=True,
        machine_id=machine.id,
        machine_uuid=machine.machine_uuid,
        status=machine.status,
        last_seen_at=machine.last_seen_at,
    )

@router.post("/rotate-token", response_model=RotateMachineTokenResponse)
async def rotate_machine_token(
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    new_token = generate_machine_token()
    machine.auth_token_hash = hash_machine_token(new_token)
    machine.auth_token_created_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(machine)

    return RotateMachineTokenResponse(
        ok=True,
        machine_token=new_token,
    )


@router.post("/jobs/fetch", response_model=AgentFetchJobResponse)
async def fetch_next_job(
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    stmt = (
        select(Job)
        .where(Job.machine_id == machine.id)
        .where(Job.status == "pending")
        .order_by(Job.created_at.asc())
        .with_for_update(skip_locked=True)
        .limit(1)
    )

    job = db.execute(stmt).scalar_one_or_none()

    if not job:
        return AgentFetchJobResponse(has_job=False)

    job.status = "claimed"
    job.claimed_at = now

    db.commit()
    db.refresh(job)

    sync_application_state_from_job(db, job)

    await job_ws_manager.broadcast(
        job.id,
        {
            "type": "job_status",
            "job_id": str(job.id),
            "status": job.status,
            "claimed_at": job.claimed_at.isoformat() if job.claimed_at else None,
        },
    )

    return AgentFetchJobResponse(
        has_job=True,
        job_id=job.id,
        type=job.type,
        payload=job.payload,
        status=job.status,
        claimed_at=job.claimed_at,
    )


@router.get("/jobs/{job_id}", response_model=AdminJobResponse)
async def get_agent_job(
    job_id: UUID,
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Job)
        .where(Job.id == job_id)
        .where(Job.machine_id == machine.id)
        .limit(1)
    )
    job = db.execute(stmt).scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

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


@router.post("/jobs/{job_id}/logs", response_model=AgentCreateJobLogResponse)
async def create_job_log(
    job_id: UUID,
    payload: AgentCreateJobLogRequest,
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Job)
        .where(Job.id == job_id)
        .where(Job.machine_id == machine.id)
        .limit(1)
    )

    job = db.execute(stmt).scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status in {"completed", "failed"}:
        raise HTTPException(status_code=409, detail="Cannot add logs to a finished job")

    status_changed = False
    if job.status == "claimed":
        job.status = "running"
        status_changed = True
        sync_application_state_from_job(db, job)

    log = JobLog(
        job_id=job.id,
        seq=payload.seq,
        level=payload.level,
        message=payload.message,
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    db.refresh(job)

    if status_changed:
        await job_ws_manager.broadcast(
            job.id,
            {
                "type": "job_status",
                "job_id": str(job.id),
                "status": job.status,
            },
        )

    await job_ws_manager.broadcast(
        job.id,
        {
            "type": "job_log",
            "job_id": str(job.id),
            "log": {
                "id": str(log.id),
                "seq": log.seq,
                "level": log.level,
                "message": log.message,
                "created_at": log.created_at.isoformat(),
            },
        },
    )

    return AgentCreateJobLogResponse(
        ok=True,
        log_id=log.id,
        job_id=log.job_id,
        seq=log.seq,
    )


@router.post("/jobs/{job_id}/complete", response_model=AgentCompleteJobResponse)
async def complete_job(
    job_id: UUID,
    payload: AgentCompleteJobRequest,
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Job)
        .where(Job.id == job_id)
        .where(Job.machine_id == machine.id)
        .limit(1)
    )

    job = db.execute(stmt).scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status in {"completed", "failed"}:
        raise HTTPException(status_code=409, detail="Job already finished")

    if payload.result is not None:
        encoded = json.dumps(payload.result, ensure_ascii=False).encode("utf-8")
        if len(encoded) > MAX_RESULT_BYTES:
            raise HTTPException(status_code=413, detail="Result payload too large")

    now = datetime.now(timezone.utc)

    if payload.error_message:
        job.status = "failed"
        job.error_message = payload.error_message
        job.result = None
    else:
        job.status = "completed"
        job.result = payload.result
        job.error_message = None

    job.completed_at = now

    sync_application_state_from_job(db, job)

    db.commit()
    db.refresh(job)

    await job_ws_manager.broadcast(
        job.id,
        {
            "type": "job_status",
            "job_id": str(job.id),
            "status": job.status,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "result": job.result,
            "error_message": job.error_message,
        },
    )

    return AgentCompleteJobResponse(
        ok=True,
        job_id=job.id,
        status=job.status,
        completed_at=job.completed_at,
    )