from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.catalog.apps import get_catalog_app
from app.core.audit import audit_event
from app.core.database import get_db
from app.core.security import generate_machine_token, hash_machine_token
from app.models.job import Job
from app.models.job_log import JobLog
from app.models.machine import Machine
from app.models.security_audit_log import SecurityAuditLog
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.job import (
    AdminJobListItem,
    AdminJobResponse,
    CreateMachineJobRequest,
    CreateMachineJobResponse,
)
from app.schemas.job_log import AdminJobLogItem
from app.schemas.machine import AdminMachineListItem, AdminMachineResponse
from app.schemas.security_audit_log import SecurityAuditLogItem
from app.schemas.token import RevokeMachineTokenResponse, RotateMachineTokenResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stmt = select(User).order_by(User.created_at.desc())
    users = db.execute(stmt).scalars().all()

    return [
        UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]


@router.post("/users/{user_id}/grant-admin", response_model=UserResponse)
def grant_admin(
    user_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    user = db.get(User, user_id)
    if not user:
        audit_event(
            event_type="user.admin.grant.failed",
            severity="warning",
            success=False,
            status_code=404,
            actor_type="admin",
            actor_user_id=admin.id,
            target_user_id=user_id,
            request=request,
            description="Grant admin failed: user not found",
        )
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        audit_event(
            event_type="user.admin.grant.failed",
            severity="warning",
            success=False,
            status_code=409,
            actor_type="admin",
            actor_user_id=admin.id,
            target_user_id=user.id,
            request=request,
            description="Grant admin failed: inactive user",
            details={"email": user.email},
        )
        raise HTTPException(status_code=409, detail="Inactive user")

    if user.is_admin:
        audit_event(
            event_type="user.admin.grant.failed",
            severity="info",
            success=False,
            status_code=409,
            actor_type="admin",
            actor_user_id=admin.id,
            target_user_id=user.id,
            request=request,
            description="Grant admin failed: user already admin",
            details={"email": user.email},
        )
        raise HTTPException(status_code=409, detail="User is already admin")

    user.is_admin = True
    db.commit()
    db.refresh(user)

    audit_event(
        event_type="user.admin.grant.success",
        severity="critical",
        success=True,
        status_code=200,
        actor_type="admin",
        actor_user_id=admin.id,
        target_user_id=user.id,
        request=request,
        description="Admin granted to user",
        details={"email": user.email},
    )

    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


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


@router.post("/machines/{machine_id}/rotate-token", response_model=RotateMachineTokenResponse)
def rotate_machine_token_admin(
    machine_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    machine = db.get(Machine, machine_id)
    if not machine:
        audit_event(
            event_type="machine.token.rotate.failed",
            severity="warning",
            success=False,
            status_code=404,
            actor_type="admin",
            actor_user_id=admin.id,
            target_machine_id=machine_id,
            request=request,
            description="Rotate machine token failed: machine not found",
        )
        raise HTTPException(status_code=404, detail="Machine not found")

    if machine.status == "revoked":
        audit_event(
            event_type="machine.token.rotate.failed",
            severity="warning",
            success=False,
            status_code=409,
            actor_type="admin",
            actor_user_id=admin.id,
            target_machine_id=machine.id,
            request=request,
            description="Rotate machine token failed: machine is revoked",
        )
        raise HTTPException(
            status_code=409,
            detail="Cannot rotate token for a revoked machine. Re-pair it instead.",
        )

    new_token = generate_machine_token()
    machine.auth_token_hash = hash_machine_token(new_token)
    machine.auth_token_created_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(machine)

    audit_event(
        event_type="machine.token.rotate.success",
        severity="warning",
        success=True,
        status_code=200,
        actor_type="admin",
        actor_user_id=admin.id,
        target_machine_id=machine.id,
        request=request,
        description="Machine token rotated",
        details={"machine_uuid": str(machine.machine_uuid)},
    )

    return RotateMachineTokenResponse(
        ok=True,
        machine_token=new_token,
    )


@router.post("/machines/{machine_id}/revoke-token", response_model=RevokeMachineTokenResponse)
def revoke_machine_token_admin(
    machine_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    machine = db.get(Machine, machine_id)
    if not machine:
        audit_event(
            event_type="machine.revoke.failed",
            severity="warning",
            success=False,
            status_code=404,
            actor_type="admin",
            actor_user_id=admin.id,
            target_machine_id=machine_id,
            request=request,
            description="Machine revoke failed: machine not found",
        )
        raise HTTPException(status_code=404, detail="Machine not found")

    machine.status = "revoked"
    machine.auth_token_hash = None
    machine.auth_token_created_at = None

    db.commit()
    db.refresh(machine)

    audit_event(
        event_type="machine.revoke.success",
        severity="critical",
        success=True,
        status_code=200,
        actor_type="admin",
        actor_user_id=admin.id,
        target_machine_id=machine.id,
        request=request,
        description="Machine revoked",
        details={"machine_uuid": str(machine.machine_uuid)},
    )

    return RevokeMachineTokenResponse(
        ok=True,
        machine_id=str(machine.id),
        status=machine.status,
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

    stmt = select(Job).where(Job.machine_id == machine_id).order_by(Job.created_at.desc())
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
            payload=job.payload,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )
        for job in jobs
    ]


@router.post("/machines/{machine_id}/jobs", response_model=CreateMachineJobResponse)
def create_job(
    machine_id: UUID,
    payload: CreateMachineJobRequest,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    catalog_app = get_catalog_app(payload.app_slug)
    if not catalog_app:
        raise HTTPException(status_code=400, detail="Unsupported app_slug")

    if not catalog_app.get("enabled", False):
        raise HTTPException(status_code=400, detail="App is currently disabled")

    auth_type = payload.auth_type.strip().lower()
    if auth_type not in set(catalog_app["allowed_auth_types"]):
        raise HTTPException(status_code=400, detail="Unsupported auth_type for this app")

    machine = db.get(Machine, machine_id)
    if not machine:
        audit_event(
            event_type="job.create.failed",
            severity="warning",
            success=False,
            status_code=404,
            actor_type="admin",
            actor_user_id=admin.id,
            target_machine_id=machine_id,
            request=request,
            description="Admin job create failed: machine not found",
        )
        raise HTTPException(status_code=404, detail="Machine not found")

    job = Job(
        machine_id=machine.id,
        type="install_app",
        status="pending",
        payload={
            "app_slug": catalog_app["slug"],
            "install_profile": catalog_app["install_profile"],
            "subdomain": payload.subdomain.strip().lower(),
            "auth_type": auth_type,
        },
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    audit_event(
        event_type="job.create.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="admin",
        actor_user_id=admin.id,
        target_machine_id=machine.id,
        request=request,
        description="Admin created install job",
        details={"job_id": str(job.id), "payload": job.payload},
    )

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

    stmt = select(JobLog).where(JobLog.job_id == job_id).order_by(JobLog.seq.asc(), JobLog.created_at.asc())
    logs = db.execute(stmt).scalars().all()

    return logs


@router.get("/security-audit", response_model=list[SecurityAuditLogItem])
def list_security_audit(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stmt = select(SecurityAuditLog).order_by(SecurityAuditLog.created_at.desc()).limit(limit)
    logs = db.execute(stmt).scalars().all()

    return [
        SecurityAuditLogItem(
            id=log.id,
            event_type=log.event_type,
            severity=log.severity,
            success=log.success,
            status_code=log.status_code,
            actor_type=log.actor_type,
            actor_user_id=log.actor_user_id,
            actor_machine_id=log.actor_machine_id,
            target_user_id=log.target_user_id,
            target_machine_id=log.target_machine_id,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            description=log.description,
            details=log.details,
            created_at=log.created_at,
        )
        for log in logs
    ]