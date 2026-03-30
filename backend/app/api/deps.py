import jwt
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import decode_access_token
from app.core.database import get_db
from app.core.security import hash_machine_token
from app.models.machine import Machine
from app.models.user import User


def extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    return parts[1].strip()


def get_current_machine(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> Machine:
    machine_token = extract_bearer_token(authorization)
    token_hash = hash_machine_token(machine_token)

    stmt = select(Machine).where(Machine.auth_token_hash == token_hash).limit(1)
    machine = db.execute(stmt).scalar_one_or_none()

    if not machine:
        raise HTTPException(status_code=401, detail="Invalid machine token")

    if machine.status == "revoked":
        raise HTTPException(status_code=403, detail="Machine is revoked")

    return machine


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    token = extract_bearer_token(authorization)

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=401, detail="Invalid access token payload")

    stmt = select(User).where(User.id == subject).limit(1)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user