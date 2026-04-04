from datetime import datetime, timezone
from uuid import UUID
from urllib.parse import quote, parse_qs, urlsplit

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
    StreamFusionTokenActionResponse,
    StreamFusionTokenCreateRequest,
    StreamFusionTokenCreateResponse,
    StreamFusionTokenListResponse,
    StreamFusionTokenResponse,
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


def token_to_response(row: StreamFusionAddonToken) -> StreamFusionTokenResponse:
    return StreamFusionTokenResponse(
        id=row.id,
        label=row.label,
        created_at=row.created_at,
        last_used_at=row.last_used_at,
        revoked_at=row.revoked_at,
        expires_at=row.expires_at,
    )


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


def get_owned_token_or_404(
    db: Session,
    token_id: UUID,
    current_user: User,
) -> StreamFusionAddonToken:
    stmt = (
        select(StreamFusionAddonToken)
        .where(StreamFusionAddonToken.id == token_id)
        .where(StreamFusionAddonToken.user_id == current_user.id)
        .limit(1)
    )
    row = db.execute(stmt).scalar_one_or_none()

    if not row:
        raise HTTPException(status_code=404, detail="StreamFusion token not found")

    return row


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


@router.get("/me/streamfusion/tokens", response_model=StreamFusionTokenListResponse)
def list_streamfusion_tokens(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(StreamFusionAddonToken)
        .where(StreamFusionAddonToken.user_id == current_user.id)
        .order_by(StreamFusionAddonToken.created_at.desc())
    )
    rows = db.execute(stmt).scalars().all()

    return StreamFusionTokenListResponse(
        items=[token_to_response(row) for row in rows]
    )


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


@router.delete("/me/streamfusion/tokens/{token_id}", response_model=StreamFusionTokenActionResponse)
def revoke_streamfusion_token(
    token_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = get_owned_token_or_404(db, token_id, current_user)

    if row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(row)

    return StreamFusionTokenActionResponse(ok=True, id=row.id)


@router.post(
    "/me/streamfusion/tokens/{token_id}/rotate",
    response_model=StreamFusionTokenCreateResponse,
)
def rotate_streamfusion_token(
    token_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_row = get_owned_token_or_404(db, token_id, current_user)

    if old_row.revoked_at is not None:
        raise HTTPException(status_code=400, detail="StreamFusion token already revoked")

    old_row.revoked_at = datetime.now(timezone.utc)

    plain_token = generate_streamfusion_addon_token()
    token_hash = hash_streamfusion_addon_token(plain_token)

    new_row = StreamFusionAddonToken(
        user_id=current_user.id,
        token_hash=token_hash,
        label=old_row.label,
        expires_at=old_row.expires_at,
    )

    db.add(new_row)
    db.commit()
    db.refresh(new_row)

    return token_to_create_response(new_row, plain_token)


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