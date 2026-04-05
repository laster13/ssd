from datetime import datetime, timezone
from urllib.parse import parse_qs, quote, urlsplit

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    generate_streamfusion_addon_token,
    hash_streamfusion_addon_token,
)
from app.models.streamfusion_addon_token import StreamFusionAddonToken
from app.models.user import User
from app.schemas.streamfusion import (
    StreamFusionTokenCreateRequest,
    StreamFusionTokenCreateResponse,
)

router = APIRouter(tags=["streamfusion"])


def normalize_label(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


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
) -> StreamFusionAddonToken:
    token_hash = hash_streamfusion_addon_token(plain_token)

    stmt = (
        select(StreamFusionAddonToken)
        .where(StreamFusionAddonToken.token_hash == token_hash)
        .limit(1)
    )
    row = db.execute(stmt).scalar_one_or_none()

    if not row:
        raise HTTPException(status_code=404, detail="Not found")

    if row.revoked_at is not None:
        raise HTTPException(status_code=404, detail="Not found")

    if row.expires_at is not None and row.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="Not found")

    return row


def extract_token_from_forwarded_uri(x_forwarded_uri: str | None) -> str | None:
    if not x_forwarded_uri:
        return None

    parsed = urlsplit(x_forwarded_uri)
    query = parse_qs(parsed.query)
    values = query.get("token")

    if not values:
        return None

    token = (values[0] or "").strip()
    return token or None


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

    row = StreamFusionAddonToken(
        user_id=current_user.id,
        token_hash=token_hash,
        label=normalize_label(payload.label),
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return token_to_create_response(row, plain_token)


@router.get("/streamfusion/resolve")
def resolve_streamfusion_token(
    token: str | None = Query(default=None),
    x_forwarded_uri: str | None = Header(default=None, alias="X-Forwarded-Uri"),
    db: Session = Depends(get_db),
):
    plain_token = (token or "").strip() or extract_token_from_forwarded_uri(x_forwarded_uri)

    if not plain_token:
        raise HTTPException(status_code=404, detail="Not found")

    row = get_valid_streamfusion_token_or_404(db, plain_token)

    row.last_used_at = datetime.now(timezone.utc)
    db.commit()

    return Response(status_code=204)