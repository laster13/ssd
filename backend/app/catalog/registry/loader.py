from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

import yaml

DEFAULT_AUTH_TYPES = [
    "aucune",
    "basique",
    "oauth",
    "authelia",
    "oauth2-proxy",
]
DEFAULT_INSTALL_PROFILE = "seedbox_standard"
REGISTRY_PATH = Path(__file__).with_name("apps.yaml")
PUBLIC_DOCS_BASE = "https://projetssd.github.io/ssdv2_docs/"


def _slug_key(value: str) -> str:
    return value.strip().lower()


def _read_registry() -> dict:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry file not found: {REGISTRY_PATH}")

    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError("apps.yaml must contain a top-level mapping")

    return data


def build_public_docs_url(docs_repo_path: str, highlight: str | None = None) -> str:
    rel = docs_repo_path.strip()

    if rel.startswith("docs/fr/"):
        rel = rel[len("docs/fr/") :]
    elif rel.startswith("docs/"):
        rel = rel[len("docs/") :]

    if rel.endswith(".md"):
        rel = rel[:-3]

    rel = rel.strip("/")
    url = f"{PUBLIC_DOCS_BASE}{rel}/"

    if highlight:
        url += f"?h={quote(highlight)}"

    return url


def _resolve_docs_path(
    raw_apps_by_slug: dict[str, dict],
    slug_key: str,
    seen: set[str] | None = None,
) -> str | None:
    seen = seen or set()
    if slug_key in seen:
        raise ValueError(f"Circular docs.ref detected for slug: {slug_key}")

    seen.add(slug_key)
    raw_app = raw_apps_by_slug[slug_key]
    docs = raw_app.get("docs") or {}

    if docs.get("missing") is True:
        return None

    path = docs.get("path")
    if isinstance(path, str) and path.strip():
        return path.strip()

    ref = docs.get("ref")
    if isinstance(ref, str) and ref.strip():
        ref_key = _slug_key(ref)
        if ref_key not in raw_apps_by_slug:
            raise ValueError(f"Unknown docs.ref '{ref}' for slug '{raw_app['slug']}'")
        return _resolve_docs_path(raw_apps_by_slug, ref_key, seen)

    return None


@lru_cache
def load_catalog_registry() -> tuple[dict, ...]:
    data = _read_registry()
    defaults = data.get("defaults") or {}
    raw_apps = data.get("apps") or []

    if not isinstance(raw_apps, list):
        raise ValueError("apps.yaml: 'apps' must be a list")

    raw_apps_by_slug: dict[str, dict] = {}
    for index, item in enumerate(raw_apps, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"apps.yaml: item #{index} must be a mapping")

        slug = str(item.get("slug") or "").strip()
        if not slug:
            raise ValueError(f"apps.yaml: item #{index} is missing 'slug'")

        slug_key = _slug_key(slug)
        if slug_key in raw_apps_by_slug:
            raise ValueError(f"apps.yaml: duplicate slug '{slug}'")

        raw_apps_by_slug[slug_key] = item

    resolved: list[dict] = []

    for slug_key, raw_app in raw_apps_by_slug.items():
        slug = str(raw_app["slug"]).strip()
        title = str(raw_app.get("title") or raw_app.get("name") or slug).strip()
        category = str(raw_app.get("category") or "Catalogue").strip()
        tagline = str(raw_app.get("tagline") or raw_app.get("description") or title).strip()
        description = str(raw_app.get("description") or raw_app.get("tagline") or title).strip()
        status = str(raw_app.get("status") or defaults.get("status") or "Disponible").strip()
        enabled = bool(raw_app.get("enabled", True))
        install_profile = str(
            raw_app.get("install_profile")
            or defaults.get("install_profile")
            or DEFAULT_INSTALL_PROFILE
        ).strip()

        allowed_auth_types = raw_app.get("allowed_auth_types")
        if not isinstance(allowed_auth_types, list) or not allowed_auth_types:
            allowed_auth_types = defaults.get("allowed_auth_types") or DEFAULT_AUTH_TYPES
        allowed_auth_types = [str(option).strip() for option in allowed_auth_types if str(option).strip()]

        aliases = raw_app.get("aliases") or []
        if not isinstance(aliases, list):
            raise ValueError(f"apps.yaml: aliases for '{slug}' must be a list")
        aliases = [str(alias).strip() for alias in aliases if str(alias).strip()]

        variant_of = raw_app.get("variant_of")
        variant_of = str(variant_of).strip() if variant_of else None

        docs = raw_app.get("docs") or {}
        if not isinstance(docs, dict):
            raise ValueError(f"apps.yaml: docs for '{slug}' must be a mapping")

        docs_repo_path = _resolve_docs_path(raw_apps_by_slug, slug_key)
        docs_ref = str(docs.get("ref") or "").strip() or None
        docs_status = "available" if docs_repo_path else "missing"
        highlight = docs_ref or slug
        docs_url = build_public_docs_url(docs_repo_path, highlight) if docs_repo_path else None

        form_fields = raw_app.get("form_fields") or []
        if not isinstance(form_fields, list):
            raise ValueError(f"apps.yaml: form_fields for '{slug}' must be a list")

        resolved.append(
            {
                "slug": slug,
                "name": title,
                "category": category,
                "tagline": tagline,
                "description": description,
                "status": status,
                "enabled": enabled,
                "install_profile": install_profile,
                "allowed_auth_types": allowed_auth_types,
                "docs_status": docs_status,
                "docs_repo_path": docs_repo_path,
                "docs_url": docs_url,
                "variant_of": variant_of,
                "aliases": aliases,
                "form_fields": form_fields,
            }
        )

    return tuple(resolved)