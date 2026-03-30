from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.job import Job
from app.models.job_log import JobLog
from app.models.machine import Machine
from app.models.user import User
from app.schemas.job import AdminJobListItem, AdminJobResponse
from app.schemas.job_log import AdminJobLogItem
from app.schemas.machine import AdminMachineListItem, AdminMachineResponse
from app.schemas.job import AdminJobListItem, AdminJobResponse, CreateMachineJobRequest, CreateMachineJobResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/machines", response_model=list[AdminMachineListItem])
def list_machines(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stmt = select(Machine).order_by(Machine.created_at.desc())
    machines = db.execute(stmt).scalars().all()

    return [
        AdminMachineListItem(
            id=machine.id,
            machine_uuid=machine.machine_uuid,
            status=machine.status,
            hostname=machine.hostname,
            agent_version=machine.agent_version,
            last_seen_at=machine.last_seen_at,
            created_at=machine.created_at,
            updated_at=machine.updated_at,
        )
        for machine in machines
    ]


@router.get("/machines/{machine_id}", response_model=AdminMachineResponse)
def get_machine(
    machine_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    machine = db.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    return AdminMachineResponse(
        id=machine.id,
        machine_uuid=machine.machine_uuid,
        status=machine.status,
        hostname=machine.hostname,
        agent_version=machine.agent_version,
        auth_token_created_at=machine.auth_token_created_at,
        last_seen_at=machine.last_seen_at,
        created_at=machine.created_at,
        updated_at=machine.updated_at,
    )


@router.get("/machines/{machine_id}/jobs", response_model=list[AdminJobListItem])
def list_machine_jobs(
    machine_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    machine = db.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    stmt = (
        select(Job)
        .where(Job.machine_id == machine_id)
        .order_by(Job.created_at.desc())
    )
    jobs = db.execute(stmt).scalars().all()

    return [
        AdminJobListItem(
            id=job.id,
            machine_id=job.machine_id,
            type=job.type,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]


@router.get("/jobs", response_model=list[AdminJobListItem])
def list_jobs(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stmt = select(Job).order_by(Job.created_at.desc())
    jobs = db.execute(stmt).scalars().all()

    return [
        AdminJobListItem(
            id=job.id,
            machine_id=job.machine_id,
            type=job.type,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]


@router.post("/machines/{machine_id}/jobs", response_model=CreateMachineJobResponse)
def create_job(
    machine_id: UUID,
    payload: CreateMachineJobRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    machine = db.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    job = Job(
        machine_id=machine.id,
        type="install_app",
        status="pending",
        payload={
            "app_slug": payload.app_slug,
            "subdomain": payload.subdomain,
            "auth_type": payload.auth_type,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return CreateMachineJobResponse(
        job_id=job.id,
        machine_id=job.machine_id,
        status=job.status,
        type=job.type,
        payload=job.payload,
    )

@router.get("/jobs/{job_id}", response_model=AdminJobResponse)
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    job = db.get(Job, job_id)
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


@router.get("/jobs/{job_id}/logs", response_model=list[AdminJobLogItem])
def get_job_logs(
    job_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    stmt = (
        select(JobLog)
        .where(JobLog.job_id == job_id)
        .order_by(JobLog.seq.asc(), JobLog.created_at.asc())
    )

    logs = db.execute(stmt).scalars().all()
    return logs