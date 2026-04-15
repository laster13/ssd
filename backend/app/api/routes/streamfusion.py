from datetime import datetime, timedelta, timezone
from urllib.parse import quote, urlsplit

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Query, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    generate_streamfusion_addon_token,
    generate_streamfusion_session_token,
    hash_streamfusion_addon_token,
    hash_streamfusion_session_token,
)
from app.models.streamfusion_addon_token import StreamFusionAddonToken
from app.models.streamfusion_session import StreamFusionSession
from app.models.user import User
from app.schemas.streamfusion import (
    StreamFusionTokenCreateRequest,
    StreamFusionTokenCreateResponse,
)

router = APIRouter(tags=["streamfusion"])


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def normalize_label(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def normalize_header_value(value: str | None, max_len: int = 512) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return value[:max_len]


def extract_client_ip(x_forwarded_for: str | None) -> str | None:
    if not x_forwarded_for:
        return None
    first = x_forwarded_for.split(",", 1)[0].strip()
    return first or None


def expected_streamfusion_host() -> str:
    host = urlsplit(settings.streamfusion_public_base_url).hostname
    if not host:
        raise RuntimeError("Invalid STREAMFUSION_PUBLIC_BASE_URL")
    return host.lower()


def build_configure_url(plain_token: str) -> str:
    base = settings.streamfusion_public_base_url.rstrip("/")
    return f"{base}/configure?token={quote(plain_token)}"


def token_to_create_response(
    row: StreamFusionAddonToken,
    plain_token: str,
) -> StreamFusionTokenCreateResponse:
    return StreamFusionTokenCreateResponse(
        id=row.id,
        label=row.label,
        created_at=row.created_at,
        last_used_at=row.last_used_at,
        revoked_at=row.revoked_at,
        expires_at=row.expires_at,
        plain_token=plain_token,
        configure_url=build_configure_url(plain_token),
    )


def get_valid_streamfusion_token_or_404(
    db: Session,
    plain_token: str,
    *,
    for_update: bool = False,
) -> StreamFusionAddonToken:
    token_hash = hash_streamfusion_addon_token(plain_token)

    stmt = (
        select(StreamFusionAddonToken)
        .where(StreamFusionAddonToken.token_hash == token_hash)
        .limit(1)
    )

    if for_update:
        stmt = stmt.with_for_update()

    row = db.execute(stmt).scalar_one_or_none()

    if not row:
        raise HTTPException(status_code=404, detail="Not found")

    now = now_utc()

    if row.revoked_at is not None:
        raise HTTPException(status_code=404, detail="Not found")

    if row.expires_at <= now:
        raise HTTPException(status_code=404, detail="Not found")

    if row.consumed_at is not None:
        raise HTTPException(status_code=404, detail="Not found")

    return row


def get_valid_streamfusion_session_or_403(
    db: Session,
    plain_session_token: str | None,
) -> StreamFusionSession:
    token = (plain_session_token or "").strip()
    if not token:
        raise HTTPException(status_code=403, detail="Forbidden")

    session_hash = hash_streamfusion_session_token(token)

    stmt = (
        select(StreamFusionSession)
        .where(StreamFusionSession.session_hash == session_hash)
        .limit(1)
    )
    row = db.execute(stmt).scalar_one_or_none()

    if not row:
        raise HTTPException(status_code=403, detail="Forbidden")

    now = now_utc()

    if row.revoked_at is not None:
        raise HTTPException(status_code=403, detail="Forbidden")

    if row.expires_at <= now:
        raise HTTPException(status_code=403, detail="Forbidden")

    return row


@router.post(
    "/me/streamfusion/tokens",
    response_model=StreamFusionTokenCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_streamfusion_token(
    payload: StreamFusionTokenCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plain_token = generate_streamfusion_addon_token()
    token_hash = hash_streamfusion_addon_token(plain_token)
    expires_at = now_utc() + timedelta(seconds=settings.streamfusion_token_ttl_seconds)

    row = StreamFusionAddonToken(
        user_id=current_user.id,
        token_hash=token_hash,
        label=normalize_label(payload.label),
        expires_at=expires_at,
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return token_to_create_response(row, plain_token)


@router.get("/streamfusion/configure")
def configure_streamfusion_access(
    token: str = Query(...),
    x_forwarded_host: str | None = Header(default=None, alias="X-Forwarded-Host"),
    x_forwarded_for: str | None = Header(default=None, alias="X-Forwarded-For"),
    user_agent: str | None = Header(default=None, alias="User-Agent"),
    db: Session = Depends(get_db),
):
    forwarded_host = normalize_header_value(x_forwarded_host, max_len=255)
    if forwarded_host is not None:
        forwarded_host = forwarded_host.split(":", 1)[0].lower()
        if forwarded_host != expected_streamfusion_host():
            raise HTTPException(status_code=404, detail="Not found")

    client_ip = extract_client_ip(x_forwarded_for)
    normalized_user_agent = normalize_header_value(user_agent, max_len=512)
    now = now_utc()

    token_row = get_valid_streamfusion_token_or_404(db, token, for_update=True)

    db.execute(
        update(StreamFusionSession)
        .where(
            StreamFusionSession.user_id == token_row.user_id,
            StreamFusionSession.revoked_at.is_(None),
            StreamFusionSession.expires_at > now,
        )
        .values(revoked_at=now)
    )

    plain_session = generate_streamfusion_session_token()
    session_hash = hash_streamfusion_session_token(plain_session)

    session_row = StreamFusionSession(
        user_id=token_row.user_id,
        addon_token_id=token_row.id,
        session_hash=session_hash,
        expires_at=now + timedelta(seconds=settings.streamfusion_session_ttl_seconds),
        client_ip=client_ip,
        user_agent=normalized_user_agent,
    )

    token_row.last_used_at = now
    token_row.consumed_at = now
    token_row.consumed_ip = client_ip
    token_row.consumed_user_agent = normalized_user_agent

    db.add(session_row)
    db.commit()

    response = RedirectResponse(
        url=f"{settings.streamfusion_public_base_url.rstrip('/')}/",
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie(
        key=settings.streamfusion_session_cookie_name,
        value=plain_session,
        max_age=settings.streamfusion_session_ttl_seconds,
        secure=True,
        httponly=True,
        samesite="strict",
        path="/",
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@router.get("/streamfusion/resolve")
def resolve_streamfusion_access(
    response: Response,
    streamfusion_session: str | None = Cookie(
        default=None,
        alias=settings.streamfusion_session_cookie_name,
    ),
    x_forwarded_host: str | None = Header(default=None, alias="X-Forwarded-Host"),
    db: Session = Depends(get_db),
):
    forwarded_host = normalize_header_value(x_forwarded_host, max_len=255)
    if forwarded_host is not None:
        forwarded_host = forwarded_host.split(":", 1)[0].lower()
        if forwarded_host != expected_streamfusion_host():
            raise HTTPException(status_code=404, detail="Not found")

    session_row = get_valid_streamfusion_session_or_403(db, streamfusion_session)
    session_row.last_used_at = now_utc()
    db.commit()

    response.status_code = 204
    response.headers["Cache-Control"] = "no-store"
    return response