"""Rate limiting (ADR-027).

Sliding-window counters (the previous window's count, weighted by how much of it still overlaps,
plus the current window's count). This smooths the double-burst that plain fixed windows allow
at a boundary, with two counters per key.

Two layers:
- `RateLimitMiddleware`: a baseline budget for every /api request (reads and writes separately),
  keyed by user when signed in and by client IP otherwise.
- `rate_limit(...)` dependencies and `check(...)`: tighter limits on sensitive or expensive routes
  (sign-in, AI calls, exports, uploads), and on keys other than the caller (e.g. per account).

Backends: Redis (shared by every API process) or in-process memory (single process, tests).
Client IPs come from X-Forwarded-For only for `TRUSTED_PROXY_HOPS` proxies we run ourselves;
the client controls the rest of that header, so trusting it blindly would let anyone reset limits.
"""

from __future__ import annotations

import asyncio
import logging
import math
import time
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.config import get_settings
from app.core.errors import RateLimited
from app.core.security import ACCESS_COOKIE, decode_access_token

logger = logging.getLogger("medspace.ratelimit")

PROBLEM_JSON = "application/problem+json"
MESSAGE = "Slow down a little. Even good habits work best in measured doses."


@dataclass(frozen=True, slots=True)
class Decision:
    allowed: bool
    limit: int
    remaining: int
    reset: int  # seconds until the window frees up capacity

    def headers(self) -> dict[str, str]:
        h = {
            "RateLimit-Limit": str(self.limit),
            "RateLimit-Remaining": str(self.remaining),
            "RateLimit-Reset": str(self.reset),
        }
        if not self.allowed:
            h["Retry-After"] = str(self.reset)
        return h


def _estimate(prev: int, current: int, window: int, now: float) -> tuple[float, int]:
    elapsed = now % window
    weight = 1 - elapsed / window
    return prev * weight + current, max(1, math.ceil(window - elapsed))


class MemoryStore:
    """Single-process store (tests, local development). `clock` is injectable for tests."""

    def __init__(self, clock: Callable[[], float] = time.time) -> None:
        self._counts: dict[tuple[str, int], int] = {}
        self._lock = asyncio.Lock()
        self.clock = clock

    async def hit(self, key: str, window: int) -> tuple[float, int]:
        now = self.clock()
        bucket = int(now // window)
        async with self._lock:
            current = self._counts.get((key, bucket), 0) + 1
            self._counts[(key, bucket)] = current
            prev = self._counts.get((key, bucket - 1), 0)
            if len(self._counts) > 100_000:  # drop buckets older than the previous one
                self._counts = {
                    k: v for k, v in self._counts.items() if k[1] >= int(now // 3600) - 1
                } or {(key, bucket): current}
        return _estimate(prev, current, window, now)

    def reset(self) -> None:
        self._counts.clear()


class RedisStore:
    def __init__(self, url: str) -> None:
        from redis.asyncio import Redis

        self._redis = Redis.from_url(url)

    async def hit(self, key: str, window: int) -> tuple[float, int]:
        now = time.time()
        bucket = int(now // window)
        cur, prev = f"rl:{key}:{window}:{bucket}", f"rl:{key}:{window}:{bucket - 1}"
        pipe = self._redis.pipeline()
        pipe.incr(cur)
        pipe.expire(cur, window * 2 + 1)
        pipe.get(prev)
        current, _, previous = await pipe.execute()
        return _estimate(int(previous or 0), int(current), window, now)


_store: MemoryStore | RedisStore | None = None


def get_store() -> MemoryStore | RedisStore:
    global _store
    if _store is None:
        s = get_settings()
        backend = s.rate_limit_backend
        if backend == "auto":
            backend = "redis" if s.queue_mode == "arq" else "memory"
        _store = RedisStore(s.redis_url) if backend == "redis" else MemoryStore()
    return _store


def reset_rate_limits() -> None:
    if isinstance(_store, MemoryStore):
        _store.reset()


def client_ip(request: Request) -> str:
    """The connecting client's IP, honouring X-Forwarded-For only for our own proxies.

    Each trusted proxy appends the address it saw, so with N trusted hops the client is the N-th
    entry from the right. Anything further left was supplied by the client and is ignored.
    """
    hops = get_settings().trusted_proxy_hops
    direct = request.client.host if request.client else "unknown"
    if hops <= 0:
        return direct
    forwarded = [
        p.strip() for p in request.headers.get("x-forwarded-for", "").split(",") if p.strip()
    ]
    return forwarded[-hops] if len(forwarded) >= hops else direct


def caller_key(request: Request) -> str:
    """ "u:<user id>" for signed-in requests, otherwise "ip:<client ip>"."""
    auth = request.headers.get("authorization", "")
    token = (
        auth[7:].strip()
        if auth.lower().startswith("bearer ")
        else request.cookies.get(ACCESS_COOKIE)
    )
    user_id = decode_access_token(token) if token else None
    return f"u:{user_id}" if user_id else f"ip:{client_ip(request)}"


async def check(scope: str, key: str, limit: int, window: int) -> Decision:
    """Count one hit for `scope` + `key` and decide. Fails open if the store is unavailable."""
    s = get_settings()
    limit = max(1, int(limit * s.rate_limit_scale))
    if not s.rate_limit_enabled:
        return Decision(True, limit, limit, window)
    try:
        estimate, reset = await get_store().hit(f"{scope}:{key}", window)
    except Exception:  # the limiter must never take the API down
        logger.warning("rate limiter unavailable", exc_info=True)
        return Decision(True, limit, limit, window)
    allowed = estimate <= limit
    return Decision(allowed, limit, max(0, int(limit - estimate)), reset)


def rate_limit(
    scope: str, limit: int, window_seconds: int, *, by: str = "caller"
) -> Callable[[Request], Coroutine[Any, Any, None]]:
    """Dependency for one route. `by="caller"` keys by user (or IP when signed out);
    `by="ip"` always keys by IP (sign-in, sign-up, public links)."""

    async def _dependency(request: Request) -> None:
        key = caller_key(request) if by == "caller" else f"ip:{client_ip(request)}"
        decision = await check(scope, key, limit, window_seconds)
        _remember(request, decision)
        if not decision.allowed:
            raise RateLimited(MESSAGE, extra={"retry_after": decision.reset})

    return _dependency


def _remember(request: Request, decision: Decision) -> None:
    """Keep the tightest decision so response headers describe the limit closest to biting."""
    current = getattr(request.state, "rate_limit", None)
    if current is None or decision.remaining < current.remaining:
        request.state.rate_limit = decision


# Baseline budgets for every API request, per user (or IP when signed out).
BASELINE_READS = (600, 60)
BASELINE_WRITES = (120, 60)
_EXEMPT = ("/api/health", "/api/ready")
_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        if not path.startswith("/api/") or path.startswith(_EXEMPT):
            return await call_next(request)
        is_read = request.method in _SAFE_METHODS
        scope, (limit, window) = (
            ("base:read", BASELINE_READS) if is_read else ("base:write", BASELINE_WRITES)
        )
        decision = await check(scope, caller_key(request), limit, window)
        if not decision.allowed:
            return JSONResponse(
                {
                    "type": "about:blank",
                    "title": "Too many requests",
                    "status": 429,
                    "detail": MESSAGE,
                    "code": "rate_limited",
                    "retry_after": decision.reset,
                    "instance": path,
                },
                status_code=429,
                media_type=PROBLEM_JSON,
                headers=decision.headers(),
            )
        _remember(request, decision)
        response = await call_next(request)
        tightest = getattr(request.state, "rate_limit", decision)
        for k, v in tightest.headers().items():
            response.headers.setdefault(k, v)
        return response
