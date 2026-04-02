from collections import deque
from threading import Lock
from time import time

from fastapi import HTTPException, Request

_lock = Lock()
_buckets: dict[str, deque[float]] = {}


def get_client_ip(request: Request) -> str:
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip:
        return cf_ip.strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def enforce_rate_limit(key: str, limit: int, window_seconds: int) -> None:
    now = time()

    with _lock:
        bucket = _buckets.setdefault(key, deque())

        while bucket and bucket[0] <= now - window_seconds:
            bucket.popleft()

        if len(bucket) >= limit:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        bucket.append(now)