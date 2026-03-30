from collections import deque
from threading import Lock
from time import time

from fastapi import HTTPException, Request

_lock = Lock()
_buckets: dict[str, deque[float]] = {}


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

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
