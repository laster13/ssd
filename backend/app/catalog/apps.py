from __future__ import annotations

from functools import lru_cache

from .registry.loader import load_catalog_registry


DEFAULT_AUTH_TYPES = [
    "aucune",
    "basique",
    "oauth",
    "authelia",
    "oauth2-proxy",
]
DEFAULT_INSTALL_PROFILE = "seedbox_standard"


def _slug_key(value: str) -> str:
    return value.strip().lower()


@lru_cache
def get_catalog_apps() -> tuple[dict, ...]:
    return tuple(dict(app) for app in load_catalog_registry())


def list_catalog_apps() -> list[dict]:
    return [dict(app) for app in get_catalog_apps()]


def get_catalog_app(slug: str) -> dict | None:
    wanted = _slug_key(slug)

    for app in get_catalog_apps():
        if _slug_key(app["slug"]) == wanted:
            return dict(app)

        aliases = app.get("aliases") or []
        if any(_slug_key(alias) == wanted for alias in aliases):
            return dict(app)

    return None


def is_supported_catalog_app(slug: str) -> bool:
    return get_catalog_app(slug) is not None