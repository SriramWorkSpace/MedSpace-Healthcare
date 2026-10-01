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
from app.shared.queue import JOBS


async def startup(ctx: dict) -> None:
    configure_logging()


async def purge_demo_accounts(ctx: dict) -> int:
    async with SessionLocal() as session:
        return await demo.purge_expired_demo_accounts(session)


class WorkerSettings:
    functions = list(JOBS.values())
    cron_jobs = [cron(purge_demo_accounts, minute={7, 37})]
    on_startup = startup
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    max_tries = 3
    job_timeout = 300
