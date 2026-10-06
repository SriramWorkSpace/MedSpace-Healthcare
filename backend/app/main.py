"""FastAPI application factory."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text

from app import jobs as _jobs  # noqa: F401  (register background jobs)
from app import models as _models  # noqa: F401  (register all ORM models)
from app.core.config import get_settings
from app.core.db import engine
from app.core.errors import ServiceUnavailable, install_error_handlers
from app.core.logging import configure_logging
from app.core.middleware import (
    BodySizeLimitMiddleware,
    CSRFMiddleware,
    RequestLogMiddleware,
    SecurityHeadersMiddleware,
)
from app.core.ratelimit import RateLimitMiddleware
from app.modules.assistant.router import router as assistant_router
from app.modules.audit.router import router as audit_router
from app.modules.circle.router import router as circle_router
from app.modules.demo.router import router as demo_router
from app.modules.documents.router import router as documents_router
from app.modules.doses.router import router as doses_router
from app.modules.extraction.router import router as extraction_router
from app.modules.identity.router import profile_router
from app.modules.identity.router import router as auth_router
from app.modules.integrations.router import auth_router as google_auth_router
from app.modules.integrations.router import router as integrations_router
from app.modules.notify.router import dev_router
from app.modules.records.router import router as records_router
from app.modules.reminders.router import router as reminders_router
from app.modules.search.router import router as search_router
from app.modules.sharing.router import public_router as public_share_router
from app.modules.sharing.router import router as sharing_router
from app.modules.supply.router import router as supply_router
from app.modules.timeline.router import router as timeline_router
from app.modules.visits.router import router as visits_router
from app.shared.embeddings import warm_up


async def run_scheduled_jobs(now: datetime) -> list[str]:
    """Inline deployments have no worker, so this does the worker's scheduled jobs: dose reminders
    every minute, expired demo accounts at :07 and :37, stale share links daily at 03:15 UTC.
    Returns the jobs that ran."""
    from app.core.db import SessionLocal
    from app.modules.demo import service as demo
    from app.modules.reminders import service as reminders
    from app.modules.sharing import service as sharing

    jobs = [("reminders", reminders.send_due_reminders, True)]
    if now.minute in (7, 37):
        jobs.append(("demo purge", demo.purge_expired_demo_accounts, False))
    if (now.hour, now.minute) == (3, 15):
        jobs.append(("share link purge", sharing.purge_stale_links, False))
    for name, job, commit in jobs:
        try:  # never let one failing job stop the others
            async with SessionLocal() as session:
                await job(session)
                if commit:
                    await session.commit()
        except Exception:
            logging.getLogger("medspace.scheduler").exception("%s failed", name)
    return [name for name, _, _ in jobs]


async def reminder_loop() -> None:
    while True:
        await asyncio.sleep(60 - time.time() % 60)  # on the minute
        await run_scheduled_jobs(datetime.now(UTC))


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    settings = get_settings()
    warm = asyncio.create_task(warm_up()) if settings.embedding_provider != "hash" else None
    # With a worker (QUEUE_MODE=arq) reminders run as an ARQ cron job; inline, they run here.
    ticker = (
        asyncio.create_task(reminder_loop())
        if settings.queue_mode == "inline" and settings.reminder_loop_enabled
        else None
    )
    yield
    for task in (warm, ticker):
        if task and not task.done():
            task.cancel()
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="MedSpace API",
        version="0.1.0",
        description="Your health, all in one space. Synthetic data only; not a medical device.",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url=None,
    )

    # Middleware executes bottom-up for requests: logging → CORS → CSRF → headers.
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CSRFMiddleware)
    # Inside CORS, so a 429 still carries CORS headers the browser can read.
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "content-type",
            "x-csrf-token",
            "x-request-id",
            "authorization",
            "x-acting-for",
        ],
        expose_headers=[
            "x-request-id",
            "retry-after",
            "ratelimit-limit",
            "ratelimit-remaining",
            "ratelimit-reset",
        ],
    )
    app.add_middleware(RequestLogMiddleware)
    # Uploads are the largest bodies; allow their limit plus multipart overhead, nothing more.
    app.add_middleware(
        BodySizeLimitMiddleware, max_bytes=(settings.max_upload_mb + 1) * 1024 * 1024
    )
    # JSON lists compress well; tiny responses aren't worth it. (nginx compresses static files.)
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    install_error_handlers(app)

    api = APIRouter(prefix="/api")
    api.include_router(auth_router)
    api.include_router(demo_router)
    api.include_router(profile_router)
    api.include_router(audit_router)
    api.include_router(documents_router)
    api.include_router(extraction_router)
    api.include_router(records_router)
    api.include_router(timeline_router)
    api.include_router(search_router)
    api.include_router(doses_router)
    api.include_router(visits_router)
    api.include_router(supply_router)
    api.include_router(circle_router)
    api.include_router(reminders_router)
    api.include_router(assistant_router)
    api.include_router(integrations_router)
    api.include_router(google_auth_router)
    api.include_router(sharing_router)
    api.include_router(public_share_router)
    if not settings.is_prod and settings.dev_outbox_enabled:
        api.include_router(dev_router)  # simulated emails, for local testing and e2e

    @api.api_route("/health", methods=["GET", "HEAD"], tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.api_route("/ready", methods=["GET", "HEAD"], tags=["ops"])
    async def ready() -> dict[str, str]:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as exc:
            raise ServiceUnavailable("Database is not reachable.") from exc
        return {"status": "ready"}

    app.include_router(api)
    return app


app = create_app()
