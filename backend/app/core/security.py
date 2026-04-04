import hashlib
import secrets

from app.core.config import settings

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_pairing_code(length: int = 8) -> str:
    raw = "".join(secrets.choice(ALPHABET) for _ in range(length))
    return f"{raw[:4]}-{raw[4:]}"


def normalize_pairing_code(code: str) -> str:
    return code.strip().upper().replace(" ", "").replace("-", "")


def hash_pairing_code(code: str) -> str:
    normalized = normalize_pairing_code(code)
    return hashlib.sha256(f"{normalized}{settings.token_pepper}".encode("utf-8")).hexdigest()


def generate_machine_token() -> str:
    return secrets.token_urlsafe(48)


def hash_machine_token(token: str) -> str:
    return hashlib.sha256(f"{token}{settings.token_pepper}".encode("utf-8")).hexdigest()


def generate_streamfusion_addon_token() -> str:
    return secrets.token_urlsafe(48)


def hash_streamfusion_addon_token(token: str) -> str:
    return hashlib.sha256(f"{token}{settings.token_pepper}".encode("utf-8")).hexdigest()