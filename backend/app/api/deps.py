import jwt
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import decode_access_token, parse_uuid_subject
from app.core.database import get_db
from app.core.security import hash_machine_token
from app.models.machine import Machine
from app.models.revoked_token import RevokedToken
from app.models.user import User


def extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = parts[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty bearer token")

    return token


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

    if payload.get("typ") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    subject = payload.get("sub")
    jti = payload.get("jti")
    token_version = payload.get("tv")

    if not subject or not jti or token_version is None:
        raise HTTPException(status_code=401, detail="Invalid access token payload")

    revoked = db.execute(
        select(RevokedToken).where(RevokedToken.jti == jti).limit(1)
    ).scalar_one_or_none()
    if revoked is not None:
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        user_id = parse_uuid_subject(subject)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid access token payload")

    stmt = select(User).where(User.id == user_id).limit(1)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    if int(user.token_version) != int(token_version):
        raise HTTPException(status_code=401, detail="Token expired by rotation")

    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    if not user.two_factor_enabled:
        raise HTTPException(status_code=403, detail="Admin 2FA required")

    return user