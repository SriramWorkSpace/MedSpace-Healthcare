"""Background job dispatch.

`QUEUE_MODE=arq`: jobs go to Redis and run in the `worker` process (durable, retried).
`QUEUE_MODE=inline`: jobs run as asyncio tasks inside the API process (tests, small demos).

Jobs are plain `async def job(ctx, *args)` functions registered in `JOBS`, so both modes share code.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger("medspace.queue")

JobFn = Callable[..., Awaitable[Any]]
JOBS: dict[str, JobFn] = {}
_inline_tasks: set[asyncio.Task] = set()
_arq_pool = None


def job(fn: JobFn) -> JobFn:
    """Register a coroutine as a background job under its function name."""
    JOBS[fn.__name__] = fn
    return fn


async def _get_arq_pool():
    global _arq_pool
    if _arq_pool is None:
        from arq import create_pool
        from arq.connections import RedisSettings

        _arq_pool = await create_pool(RedisSettings.from_dsn(get_settings().redis_url))
    return _arq_pool


async def enqueue(name: str, *args: Any, job_id: str | None = None) -> None:
    if name not in JOBS:
        raise KeyError(f"Unknown job '{name}'")
    if get_settings().queue_mode == "arq":
        pool = await _get_arq_pool()
        await pool.enqueue_job(name, *args, _job_id=job_id)
        return

    async def _run() -> None:
        try:
            await JOBS[name]({"inline": True}, *args)
        except Exception:
            logger.exception("inline job %s failed", name)

    task = asyncio.create_task(_run(), name=f"job:{name}")
    _inline_tasks.add(task)
    task.add_done_callback(_inline_tasks.discard)


async def drain() -> None:
    """Wait for all inline jobs (used by tests)."""
    while _inline_tasks:
        await asyncio.gather(*list(_inline_tasks), return_exceptions=True)
