from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import (
    generate_machine_token,
    generate_pairing_code,
    hash_machine_token,
    hash_pairing_code,
)
from app.models.machine import Machine
from app.models.pairing_token import PairingToken
from app.models.user import User
from app.schemas.pairing import (
    PairingRegisterResponse,
    PairingVerifyRequest,
    PairingVerifyResponse,
)

router = APIRouter(prefix="/pairing", tags=["pairing"])


@router.post("/register", response_model=PairingRegisterResponse)
def register_pairing(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    machine = Machine(
        owner_id=current_user.id,
        status="pending_pairing",
    )
    db.add(machine)
    db.flush()

    pairing_code = generate_pairing_code()
    token = PairingToken(
        machine_id=machine.id,
        token_hash=hash_pairing_code(pairing_code),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    db.add(token)
    db.commit()
    db.refresh(machine)

    return PairingRegisterResponse(
        machine_id=machine.id,
        machine_uuid=machine.machine_uuid,
        pairing_code=pairing_code,
        expires_at=token.expires_at,
    )


@router.post("/verify", response_model=PairingVerifyResponse)
def verify_pairing(payload: PairingVerifyRequest, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    code_hash = hash_pairing_code(payload.pairing_code)

    stmt = (
        select(PairingToken, Machine)
        .join(Machine, Machine.id == PairingToken.machine_id)
        .where(PairingToken.token_hash == code_hash)
        .where(PairingToken.used_at.is_(None))
        .where(PairingToken.expires_at > now)
        .limit(1)
    )

    result = db.execute(stmt).first()

    if not result:
        raise HTTPException(status_code=404, detail="Invalid or expired pairing code")

    token, machine = result

    machine_token = generate_machine_token()

    token.used_at = now
    machine.status = "paired"
    machine.auth_token_hash = hash_machine_token(machine_token)
    machine.auth_token_created_at = now
    machine.last_seen_at = now

    db.add(token)
    db.add(machine)
    db.commit()
    db.refresh(machine)

    return PairingVerifyResponse(
        valid=True,
        machine_id=machine.id,
        machine_uuid=machine.machine_uuid,
        status=machine.status,
        machine_token=machine_token,
    )