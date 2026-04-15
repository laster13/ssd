import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def _as_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    try:
        from app.core.config import settings
    except Exception as exc:
        raise RuntimeError(
            "DATABASE_URL is not set. Export DATABASE_URL or define it in backend/.env."
        ) from exc

    return settings.database_url


def _get_debug_flag() -> bool:
    raw_debug = os.getenv("DEBUG")
    if raw_debug is not None:
        return _as_bool(raw_debug)

    try:
        from app.core.config import settings
    except Exception:
        return False

    return bool(settings.debug)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    _get_database_url(),
    future=True,
    echo=_get_debug_flag(),
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()