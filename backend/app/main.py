"""FastAPI application factory."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app import jobs as _jobs  # noqa: F401  (register background jobs)
from app import models as _models  # noqa: F401  (register all ORM models)
from app.core.config import get_settings
from app.core.db import engine
from app.core.errors import ServiceUnavailable, install_error_handlers
from app.core.logging import configure_logging
from app.core.middleware import CSRFMiddleware, RequestLogMiddleware, SecurityHeadersMiddleware
from app.modules.assistant.router import router as assistant_router
from app.modules.audit.router import router as audit_router
from app.modules.demo.router import router as demo_router
from app.modules.documents.router import router as documents_router
from app.modules.extraction.router import router as extraction_router
from app.modules.identity.router import profile_router
from app.modules.identity.router import router as auth_router
from app.modules.integrations.router import router as integrations_router
from app.modules.records.router import router as records_router
from app.modules.sharing.router import public_router as public_share_router
from app.modules.sharing.router import router as sharing_router
from app.modules.timeline.router import router as timeline_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    yield
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["content-type", "x-csrf-token", "x-request-id", "authorization"],
        expose_headers=["x-request-id", "retry-after"],
    )
    app.add_middleware(RequestLogMiddleware)
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
    api.include_router(assistant_router)
    api.include_router(integrations_router)
    api.include_router(sharing_router)
    api.include_router(public_share_router)

    @api.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.get("/ready", tags=["ops"])
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
