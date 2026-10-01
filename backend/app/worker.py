"""ARQ worker entrypoint: `arq app.worker.WorkerSettings`."""

from __future__ import annotations

from arq.connections import RedisSettings
from arq.cron import cron

import app.jobs  # noqa: F401  (register jobs)
from app import models as _models  # noqa: F401
from app.core.config import get_settings
from app.core.db import SessionLocal
from app.core.logging import configure_logging
from app.modules.demo import service as demo
from app.modules.sharing import service as sharing
from app.shared.embeddings import warm_up
from app.shared.queue import JOBS


async def startup(ctx: dict) -> None:
    configure_logging()
    if get_settings().embedding_provider != "hash":
        await warm_up()


async def purge_demo_accounts(ctx: dict) -> int:
    async with SessionLocal() as session:
        return await demo.purge_expired_demo_accounts(session)


async def purge_share_links(ctx: dict) -> int:
    async with SessionLocal() as session:
        return await sharing.purge_stale_links(session)


class WorkerSettings:
    functions = list(JOBS.values())
    cron_jobs = [
        cron(purge_demo_accounts, minute={7, 37}),
        cron(purge_share_links, hour={3}, minute={15}),
    ]
    on_startup = startup
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    max_tries = 3
    job_timeout = 300
