from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import format_datetime
from typing import Any

import psycopg
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, Response
from psycopg.rows import dict_row

from app.core.config import settings

router = APIRouter(prefix="/torznab", tags=["torznab"])

TORZNAB_NS = "http://torznab.com/schemas/2015/feed"
ET.register_namespace("torznab", TORZNAB_NS)


@dataclass
class UnifiedTorrent:
    hash: str
    title: str
    size: int = 0
    type: str | None = None
    added: int | None = None
    imdb_id: str | None = None
    tmdb_id: int | None = None
    seasons: list[int] = field(default_factory=list)
    episodes: list[int] = field(default_factory=list)
    magnet: str | None = None
    link: str | None = None
    seeders: int | None = None
    indexer: str | None = None
    privacy: str | None = None
    source: str | None = None


def _pg_dsn() -> str:
    dsn = settings.streamfusion_database_url.strip()
    return dsn.replace("postgresql+psycopg://", "postgresql://", 1)


def _check_api_key(apikey: str | None) -> None:
    expected = getattr(settings, "torznab_api_key", None)
    if expected and apikey != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")


def _meili_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {settings.streamfusion_meili_master_key}",
        "Content-Type": "application/json",
    }


def _http_json(
    method: str,
    url: str,
    *,
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    data = None
    final_headers = headers or {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=final_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=502, detail=f"Upstream error from Meilisearch: {detail}")
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"Cannot reach Meilisearch: {exc}")


def _build_meili_search_payload(
    *,
    q: str | None,
    imdbid: str | None,
    tmdbid: int | None,
    kind: str,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "q": (q or "").strip(),
        "offset": max(offset, 0),
        "limit": max(1, min(limit, 100)),
    }

    filters: list[str] = []

    if kind == "movie":
        filters.append('type = "movie"')
    elif kind == "tvsearch":
        filters.append('type = "show"')

    if imdbid:
        imdbid = imdbid if imdbid.startswith("tt") else f"tt{imdbid}"
        filters.append(f'imdb_id = "{imdbid}"')

    if tmdbid is not None:
        filters.append(f"tmdb_id = {int(tmdbid)}")

    if filters:
        payload["filter"] = " AND ".join(filters)

    return payload


def _as_int_list(value: Any) -> list[int]:
    if not isinstance(value, list):
        return []

    out: list[int] = []
    for item in value:
        try:
            out.append(int(item))
        except Exception:
            continue
    return out


def _meili_doc_to_item(doc: dict[str, Any]) -> UnifiedTorrent:
    return UnifiedTorrent(
        hash=str(doc.get("hash") or "").lower(),
        title=str(doc.get("raw_title") or doc.get("parsed_title") or "").strip(),
        size=int(doc.get("size") or 0),
        type=doc.get("type"),
        added=int(doc["added"]) if doc.get("added") is not None else None,
        imdb_id=doc.get("imdb_id"),
        tmdb_id=int(doc["tmdb_id"]) if doc.get("tmdb_id") is not None else None,
        seasons=_as_int_list(doc.get("seasons")),
        episodes=_as_int_list(doc.get("episodes")),
        indexer=doc.get("indexer") or doc.get("hash_source"),
        source="meili",
    )


def _pg_row_to_item(row: dict[str, Any]) -> UnifiedTorrent:
    parsed_data = row.get("parsed_data") or {}
    if isinstance(parsed_data, str):
        try:
            parsed_data = json.loads(parsed_data)
        except Exception:
            parsed_data = {}

    seasons = _as_int_list(parsed_data.get("seasons"))
    episodes = _as_int_list(parsed_data.get("episodes"))

    return UnifiedTorrent(
        hash=str(row.get("info_hash") or "").lower(),
        title=str(row.get("raw_title") or "").strip(),
        size=int(row.get("size") or 0),
        type=row.get("type"),
        added=int(row["created_at"]) if row.get("created_at") is not None else None,
        imdb_id=row.get("imdb_id"),
        tmdb_id=int(row["tmdb_id"]) if row.get("tmdb_id") is not None else None,
        seasons=seasons,
        episodes=episodes,
        magnet=row.get("magnet"),
        link=row.get("link") or row.get("torrent_download"),
        seeders=int(row["seeders"]) if row.get("seeders") is not None else None,
        indexer=row.get("indexer"),
        privacy=row.get("privacy"),
        source="postgres",
    )


def _apply_episode_filters(
    items: list[UnifiedTorrent],
    *,
    season: int | None,
    ep: int | None,
) -> list[UnifiedTorrent]:
    out: list[UnifiedTorrent] = []
    for item in items:
        if season is not None and season not in item.seasons:
            continue
        if ep is not None and ep not in item.episodes:
            continue
        out.append(item)
    return out


def _query_meili(
    *,
    q: str | None,
    imdbid: str | None,
    tmdbid: int | None,
    kind: str,
    season: int | None,
    ep: int | None,
    offset: int,
    limit: int,
) -> list[UnifiedTorrent]:
    payload = _build_meili_search_payload(
        q=q,
        imdbid=imdbid,
        tmdbid=tmdbid,
        kind=kind,
        offset=offset,
        limit=max(limit * 3, 50),
    )
    url = f"{settings.streamfusion_meili_url.rstrip('/')}/indexes/torrents/search"
    data = _http_json("POST", url, body=payload, headers=_meili_headers())
    hits = data.get("hits", [])
    items = [_meili_doc_to_item(doc) for doc in hits if doc.get("hash") and doc.get("raw_title")]
    return _apply_episode_filters(items, season=season, ep=ep)


def _query_postgres(
    *,
    q: str | None,
    imdbid: str | None,
    tmdbid: int | None,
    kind: str,
    season: int | None,
    ep: int | None,
    limit: int,
) -> list[UnifiedTorrent]:
    where_parts = ["1=1"]
    params: list[Any] = []

    if q and q.strip():
        where_parts.append("raw_title ILIKE %s")
        params.append(f"%{q.strip()}%")

    if imdbid:
        imdbid = imdbid if imdbid.startswith("tt") else f"tt{imdbid}"
        where_parts.append("imdb_id = %s")
        params.append(imdbid)

    if tmdbid is not None:
        where_parts.append("tmdb_id = %s")
        params.append(int(tmdbid))

    if kind == "movie":
        where_parts.append("type = 'movie'")
    elif kind == "tvsearch":
        where_parts.append("type IN ('show', 'series')")

    if season is not None:
        where_parts.append(
            """
            EXISTS (
                SELECT 1
                FROM jsonb_array_elements_text(COALESCE((parsed_data::jsonb)->'seasons', '[]'::jsonb)) s(value)
                WHERE s.value = %s
            )
            """
        )
        params.append(str(season))

    if ep is not None:
        where_parts.append(
            """
            EXISTS (
                SELECT 1
                FROM jsonb_array_elements_text(COALESCE((parsed_data::jsonb)->'episodes', '[]'::jsonb)) e(value)
                WHERE e.value = %s
            )
            """
        )
        params.append(str(ep))

    sql = f"""
        SELECT
            id,
            raw_title,
            size,
            magnet,
            info_hash,
            link,
            seeders,
            indexer,
            privacy,
            type,
            torrent_download,
            parsed_data,
            created_at,
            tmdb_id,
            imdb_id
        FROM torrent_items
        WHERE {" AND ".join(where_parts)}
        ORDER BY seeders DESC NULLS LAST, updated_at DESC NULLS LAST, created_at DESC NULLS LAST
        LIMIT %s
    """
    params.append(max(limit * 3, 50))

    with psycopg.connect(_pg_dsn(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    return [_pg_row_to_item(row) for row in rows if row.get("info_hash") and row.get("raw_title")]


def _merge_items(meili_items: list[UnifiedTorrent], pg_items: list[UnifiedTorrent]) -> list[UnifiedTorrent]:
    merged: dict[str, UnifiedTorrent] = {}

    for item in meili_items:
        merged[item.hash] = item

    for item in pg_items:
        existing = merged.get(item.hash)
        if not existing:
            merged[item.hash] = item
            continue

        existing.magnet = item.magnet or existing.magnet
        existing.link = item.link or existing.link
        existing.seeders = item.seeders if item.seeders is not None else existing.seeders
        existing.indexer = item.indexer or existing.indexer
        existing.privacy = item.privacy or existing.privacy
        existing.type = item.type or existing.type
        existing.imdb_id = item.imdb_id or existing.imdb_id
        existing.tmdb_id = item.tmdb_id or existing.tmdb_id
        existing.seasons = item.seasons or existing.seasons
        existing.episodes = item.episodes or existing.episodes
        existing.source = "meili+postgres"

    items = list(merged.values())
    items.sort(
        key=lambda x: (
            x.seeders if x.seeders is not None else -1,
            x.added if x.added is not None else 0,
            x.size,
        ),
        reverse=True,
    )
    return items


def _infer_kind_from_cat(kind: str, cat: str | None) -> str:
    if kind in {"movie", "tvsearch"}:
        return kind
    if not cat:
        return "search"

    cats = {c.strip() for c in cat.split(",") if c.strip()}
    if any(c.startswith("2000") or c == "2000" for c in cats):
        return "movie"
    if any(c.startswith("5000") or c == "5000" for c in cats):
        return "tvsearch"
    return "search"


def _clean_imdbid(imdbid: str | None) -> str | None:
    if not imdbid:
        return None
    imdbid = imdbid.strip()
    if not imdbid:
        return None
    return imdbid if imdbid.startswith("tt") else f"tt{imdbid}"


def _build_magnet(info_hash: str, title: str) -> str:
    dn = urllib.parse.quote(title or info_hash)
    return f"magnet:?xt=urn:btih:{info_hash}&dn={dn}"


def _category_for_item(item: UnifiedTorrent) -> str:
    return "5000" if item.type in {"show", "series"} else "2000"


def _pub_date_from_ts(ts: int | None) -> str:
    dt = datetime.fromtimestamp(ts or 0, tz=timezone.utc)
    return format_datetime(dt, usegmt=True)


def _external_base_url(request: Request) -> str:
    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or request.url.netloc
    return f"{proto}://{host}"


def _download_url(request: Request, info_hash: str, apikey: str | None = None) -> str:
    base = _external_base_url(request)
    url = f"{base}/torznab/download/{info_hash}"
    if apikey:
        url = f"{url}?apikey={urllib.parse.quote(apikey)}"
    return url


def _item_link(request: Request, item: UnifiedTorrent, apikey: str | None = None) -> str:
    return _download_url(request, item.hash, apikey=apikey)


def _torznab_attr(parent: ET.Element, name: str, value: Any) -> None:
    if value is None:
        return
    ET.SubElement(parent, f"{{{TORZNAB_NS}}}attr", {"name": name, "value": str(value)})


def _display_title(item: UnifiedTorrent) -> str:
    label = {
        "meili": "MEILI",
        "postgres": "PG",
        "meili+postgres": "FUSION",
    }.get(item.source, "?")
    return f"[{label}] {item.title}"


def _build_caps_xml(request: Request) -> bytes:
    caps = ET.Element("caps")

    server = ET.SubElement(caps, "server")
    server.set("version", "1.0")
    server.set("title", "SSD StreamFusion Fusion Torznab")
    server.set("strapline", "Meilisearch + Postgres fusion")
    server.set("email", "noreply@example.invalid")
    server.set("url", _external_base_url(request))

    limits = ET.SubElement(caps, "limits")
    limits.set("max", "100")
    limits.set("default", "50")

    searching = ET.SubElement(caps, "searching")
    ET.SubElement(searching, "search", {"available": "yes", "supportedParams": "q,imdbid,tmdbid,cat,offset,limit"})
    ET.SubElement(searching, "tv-search", {"available": "yes", "supportedParams": "q,imdbid,tvdbid,tmdbid,season,ep,cat,offset,limit"})
    ET.SubElement(searching, "movie-search", {"available": "yes", "supportedParams": "q,imdbid,tmdbid,cat,offset,limit"})

    categories = ET.SubElement(caps, "categories")
    ET.SubElement(categories, "category", {"id": "2000", "name": "Movies"})
    ET.SubElement(categories, "category", {"id": "5000", "name": "TV"})
    ET.SubElement(categories, "category", {"id": "8000", "name": "Other"})

    return ET.tostring(caps, encoding="utf-8", xml_declaration=True)


def _build_search_xml(request: Request, items: list[UnifiedTorrent], apikey: str | None = None) -> bytes:
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "SSD StreamFusion Fusion Torznab"
    ET.SubElement(channel, "description").text = "Meilisearch + Postgres fusion"
    ET.SubElement(channel, "link").text = _external_base_url(request)

    for item in items:
        entry = ET.SubElement(channel, "item")
        ET.SubElement(entry, "title").text = _display_title(item)
        ET.SubElement(entry, "guid", {"isPermaLink": "false"}).text = item.hash

        item_link = _item_link(request, item, apikey=apikey)
        ET.SubElement(entry, "link").text = item_link
        ET.SubElement(entry, "comments").text = item_link
        ET.SubElement(entry, "pubDate").text = _pub_date_from_ts(item.added)
        ET.SubElement(entry, "size").text = str(item.size or 0)
        ET.SubElement(entry, "category").text = _category_for_item(item)

        ET.SubElement(
            entry,
            "enclosure",
            {
                "url": item_link,
                "length": str(item.size or 0),
                "type": "application/x-bittorrent",
            },
        )

        magnet = item.magnet or _build_magnet(item.hash, item.title)
        _torznab_attr(entry, "magneturl", magnet)
        _torznab_attr(entry, "infohash", item.hash)
        _torznab_attr(entry, "size", item.size or 0)
        _torznab_attr(entry, "seeders", item.seeders if item.seeders is not None else 0)
        _torznab_attr(entry, "peers", item.seeders if item.seeders is not None else 0)
        _torznab_attr(entry, "indexer", item.indexer)
        _torznab_attr(entry, "privacy", item.privacy)
        _torznab_attr(entry, "source", item.source)

        if item.imdb_id:
            _torznab_attr(entry, "imdbid", item.imdb_id.removeprefix("tt"))
        if item.tmdb_id is not None:
            _torznab_attr(entry, "tmdbid", item.tmdb_id)
        if item.seasons:
            _torznab_attr(entry, "season", item.seasons[0])
        if item.episodes:
            _torznab_attr(entry, "episode", item.episodes[0])

    return ET.tostring(rss, encoding="utf-8", xml_declaration=True)


def _search_fusion(
    *,
    q: str | None,
    imdbid: str | None,
    tmdbid: int | None,
    kind: str,
    season: int | None,
    ep: int | None,
    offset: int,
    limit: int,
) -> list[UnifiedTorrent]:
    meili_items = _query_meili(
        q=q,
        imdbid=imdbid,
        tmdbid=tmdbid,
        kind=kind,
        season=season,
        ep=ep,
        offset=offset,
        limit=limit,
    )
    pg_items = _query_postgres(
        q=q,
        imdbid=imdbid,
        tmdbid=tmdbid,
        kind=kind,
        season=season,
        ep=ep,
        limit=limit,
    )
    merged = _merge_items(meili_items, pg_items)
    return merged[offset : offset + limit]


@router.get("/api")
def torznab_api(
    request: Request,
    t: str = Query(..., description="caps/search/tvsearch/movie"),
    q: str | None = Query(default=None),
    cat: str | None = Query(default=None),
    imdbid: str | None = Query(default=None),
    tmdbid: int | None = Query(default=None),
    season: int | None = Query(default=None),
    ep: int | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    apikey: str | None = Query(default=None),
):
    _check_api_key(apikey)

    mode = t.strip().lower()

    if mode == "caps":
        return Response(content=_build_caps_xml(request), media_type="application/xml")

    if mode not in {"search", "tvsearch", "movie"}:
        raise HTTPException(status_code=400, detail="Unsupported torznab mode")

    kind = _infer_kind_from_cat(mode, cat)
    imdbid = _clean_imdbid(imdbid)

    items = _search_fusion(
        q=q,
        imdbid=imdbid,
        tmdbid=tmdbid,
        kind=kind,
        season=season,
        ep=ep,
        offset=offset,
        limit=limit,
    )
    return Response(
        content=_build_search_xml(request, items, apikey=apikey),
        media_type="application/xml",
    )


@router.api_route("/download/{info_hash}", methods=["GET", "HEAD"], name="torznab_download")
def torznab_download(
    info_hash: str,
    apikey: str | None = Query(default=None),
):
    _check_api_key(apikey)

    info_hash = (info_hash or "").strip().lower()
    if len(info_hash) != 40:
        raise HTTPException(status_code=400, detail="Invalid info hash")

    with psycopg.connect(_pg_dsn(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT magnet, link, torrent_download, raw_title
                FROM torrent_items
                WHERE info_hash = %s
                ORDER BY updated_at DESC NULLS LAST, created_at DESC NULLS LAST
                LIMIT 1
                """,
                (info_hash,),
            )
            row = cur.fetchone()

    if row:
        target = row.get("magnet") or row.get("link") or row.get("torrent_download")
        if target:
            return RedirectResponse(url=target, status_code=302)

        title = row.get("raw_title") or info_hash
        return RedirectResponse(url=_build_magnet(info_hash, title), status_code=302)

    url = f"{settings.streamfusion_meili_url.rstrip('/')}/indexes/torrents/documents/{info_hash}"
    doc = _http_json("GET", url, headers={"Authorization": f"Bearer {settings.streamfusion_meili_master_key}"})
    title = str(doc.get("raw_title") or info_hash)
    return RedirectResponse(url=_build_magnet(info_hash, title), status_code=302)