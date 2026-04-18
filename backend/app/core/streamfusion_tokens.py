from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlsplit

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_streamfusion_addon_token
from app.models.streamfusion_addon_token import StreamFusionAddonToken


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def expected_streamfusion_host() -> str:
    host = urlsplit(settings.streamfusion_public_base_url).hostname
    if not host:
        raise RuntimeError("Invalid STREAMFUSION_PUBLIC_BASE_URL")
    return host.lower()


def normalize_forwarded_host(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return value.split(":", 1)[0].lower()


def assert_expected_streamfusion_host_or_404(forwarded_host: str | None) -> None:
    host = normalize_forwarded_host(forwarded_host)
    if host is not None and host != expected_streamfusion_host():
        raise HTTPException(status_code=404, detail="Not found")


def _split_path_parts(path_or_uri: str | None) -> list[str]:
    if not path_or_uri:
        return []
    path = path_or_uri.split("?", 1)[0].strip()
    if not path:
        return []
    return [part for part in path.split("/") if part]


def extract_streamfusion_token_from_forwarded_uri(forwarded_uri: str | None) -> str | None:
    parts = _split_path_parts(forwarded_uri)
    if len(parts) < 2:
        return None

    token = parts[0].strip()
    return token or None


def extract_streamfusion_token_from_referer(referer: str | None) -> str | None:
    if not referer:
        return None

    parsed = urlsplit(referer)
    host = (parsed.hostname or "").lower()
    if host != expected_streamfusion_host():
        return None

    parts = _split_path_parts(parsed.path)
    if len(parts) < 2:
        return None

    token = parts[0].strip()
    return token or None


def path_can_fallback_to_referer(forwarded_uri: str | None) -> bool:
    parts = _split_path_parts(forwarded_uri)
    if not parts:
        return False

    normalized_path = "/" + "/".join(parts)

    # On autorise uniquement les routes racines que l'app peut atteindre
    # après une navigation depuis une URL tokenisée.
    return normalized_path in {
        "/register",
        "/configure",
    }


def get_valid_streamfusion_path_token_or_403(
    db: Session,
    plain_token: str | None,
) -> StreamFusionAddonToken:
    token = (plain_token or "").strip()
    if not token:
        raise HTTPException(status_code=403, detail="Forbidden")

    token_hash = hash_streamfusion_addon_token(token)
    stmt = (
        select(StreamFusionAddonToken)
        .where(StreamFusionAddonToken.token_hash == token_hash)
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


def assert_valid_streamfusion_path_token(
    db: Session,
    forwarded_uri: str | None,
    *,
    referer: str | None = None,
) -> StreamFusionAddonToken:
    plain_token = extract_streamfusion_token_from_forwarded_uri(forwarded_uri)

    if plain_token is None and path_can_fallback_to_referer(forwarded_uri):
        plain_token = extract_streamfusion_token_from_referer(referer)

    return get_valid_streamfusion_path_token_or_403(db, plain_token)