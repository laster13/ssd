from __future__ import annotations

import logging
from functools import lru_cache

from fastapi import HTTPException, Request
from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_redis() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)


def get_client_ip(request: Request) -> str:
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip:
        return cf_ip.strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def _build_key(key: str) -> str:
    return f"{settings.rate_limit_redis_prefix}:{key}"


def enforce_rate_limit(key: str, limit: int, window_seconds: int) -> None:
    redis_key = _build_key(key)

    lua_script = """
    local current = redis.call("INCR", KEYS[1])
    if current == 1 then
        redis.call("EXPIRE", KEYS[1], ARGV[1])
    end
    return current
    """

    try:
        current = int(get_redis().eval(lua_script, 1, redis_key, window_seconds))
    except RedisError as exc:
        logger.warning("Redis unavailable for rate limiting: %s", exc)
        return

    if current > limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )