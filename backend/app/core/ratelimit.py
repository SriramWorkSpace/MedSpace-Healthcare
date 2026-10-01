"""Fixed-window rate limiting.

Uses Redis when `QUEUE_MODE=arq` (multi-process deployments share Redis anyway) and an
in-process store otherwise. Exposed as a FastAPI dependency factory: `Depends(rate_limit(...))`.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request

from app.core.config import get_settings
from app.core.errors import RateLimited

logger = logging.getLogger("medspace.ratelimit")


class _MemoryStore:
    def __init__(self) -> None:
        self._hits: dict[str, tuple[int, float]] = {}
        self._lock = asyncio.Lock()

    async def hit(self, key: str, window: int) -> tuple[int, int]:
        now = time.monotonic()
        async with self._lock:
            count, reset_at = self._hits.get(key, (0, now + window))
            if now >= reset_at:
                count, reset_at = 0, now + window
            count += 1
            self._hits[key] = (count, reset_at)
            if len(self._hits) > 50_000:  # crude bound on memory
                self._hits = {k: v for k, v in self._hits.items() if v[1] > now}
            return count, max(1, int(reset_at - now))

    def reset(self) -> None:
        self._hits.clear()


class _RedisStore:
    def __init__(self, url: str) -> None:
        from redis.asyncio import Redis

        self._redis = Redis.from_url(url)

    async def hit(self, key: str, window: int) -> tuple[int, int]:
        bucket = int(time.time() // window)
        rkey = f"rl:{key}:{bucket}"
        pipe = self._redis.pipeline()
        pipe.incr(rkey)
        pipe.expire(rkey, window + 1)
        count, _ = await pipe.execute()
        return int(count), window - int(time.time() % window)


_store: _MemoryStore | _RedisStore | None = None


def _get_store() -> _MemoryStore | _RedisStore:
    global _store
    if _store is None:
        settings = get_settings()
        _store = _RedisStore(settings.redis_url) if settings.queue_mode == "arq" else _MemoryStore()
    return _store


def reset_rate_limits() -> None:
    if isinstance(_store, _MemoryStore):
        _store.reset()


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit(
    scope: str, limit: int, window_seconds: int
) -> Callable[[Request], Coroutine[Any, Any, None]]:
    async def _dependency(request: Request) -> None:
        if not get_settings().rate_limit_enabled:
            return
        key = f"{scope}:{client_ip(request)}"
        try:
            count, retry_after = await _get_store().hit(key, window_seconds)
        except Exception:  # never let the limiter take the API down
            logger.warning("rate limiter unavailable", exc_info=True)
            return
        if count > limit:
            raise RateLimited(
                "Slow down a little. Even good habits work best in measured doses.",
                extra={"retry_after": retry_after},
            )

    return _dependency
