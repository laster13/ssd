from datetime import datetime, timezone
import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_machine
from app.core.database import get_db
from app.core.security import generate_machine_token, hash_machine_token
from app.core.ws import job_ws_manager
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


@router.post("/auth", response_model=AgentAuthResponse)
async def authenticate_agent(
    machine: Machine = Depends(get_current_machine),
    db: Session = Depends(get_db),
):
    machine.last_seen_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(machine)

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

    machine.last_seen_at = now

    db.commit()
    db.refresh(machine)

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