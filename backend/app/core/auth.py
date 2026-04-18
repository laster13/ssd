from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def create_access_token(
    subject: str,
    *,
    token_version: int,
    is_admin: bool,
    expires_minutes: int | None = None,
    extra: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes or settings.jwt_access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": subject,
        "jti": uuid4().hex,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "typ": "access",
        "tv": token_version,
        "is_admin": is_admin,
    }

    if extra:
        payload.update(extra)

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
        options={
            "require": ["sub", "jti", "iss", "aud", "iat", "nbf", "exp", "typ", "tv"],
        },
    )


def parse_uuid_subject(subject: str) -> UUID:
    return UUID(subject)