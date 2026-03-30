from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.machine import Machine
from app.models.user import User

router = APIRouter(prefix="/me", tags=["me"])


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
            "last_seen_at": machine.last_seen_at,
            "created_at": machine.created_at,
            "updated_at": machine.updated_at,
        }
        for machine in machines
    ]