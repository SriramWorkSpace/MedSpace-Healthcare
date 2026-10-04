"""Test harness: real Postgres (pgvector), fakes for every external service."""

from __future__ import annotations

import os
import tempfile

# Configure before any app import: settings and the engine read env at import time.
os.environ.update(
    {
        "ENV": "test",
        "DATABASE_URL": os.environ.get(
            "TEST_DATABASE_URL",
            "postgresql+asyncpg://medspace:medspace@localhost:5432/medspace_test",
        ),
        "QUEUE_MODE": "inline",
        "REMINDER_LOOP_ENABLED": "false",
        "STORAGE_PROVIDER": "local",
        "STORAGE_LOCAL_DIR": tempfile.mkdtemp(prefix="medspace-test-"),
        "LLM_PROVIDER": "fake",
        "EMBEDDING_PROVIDER": "hash",
        "GOOGLE_PROVIDER": "fake",
        "COOKIE_SECURE": "false",
    }
)

from collections.abc import AsyncIterator

import httpx
import pytest
from sqlalchemy import text

from app.core.db import Base, SessionLocal, engine
from app.core.ratelimit import reset_rate_limits
from app.main import app
from app.shared.mail import FakeMailer, set_mailer

BASE_URL = "http://medspace.test"


@pytest.fixture(scope="session", autouse=True)
async def _schema() -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture
def sender():
    """A recording push sender (ADR-028) for tests that check notifications."""
    from app.shared.push import FakePushSender, set_push_sender

    fake = FakePushSender()
    set_push_sender(fake)
    yield fake
    set_push_sender(None)


@pytest.fixture(autouse=True)
def mailbox() -> FakeMailer:
    """Every test gets an empty simulated outbox (ADR-030)."""
    box = FakeMailer()
    set_mailer(box)
    return box


@pytest.fixture(autouse=True)
async def _clean_tables() -> AsyncIterator[None]:
    yield
    tables = ", ".join(f'"{t.name}"' for t in reversed(Base.metadata.sorted_tables))
    async with engine.begin() as conn:
        await conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    reset_rate_limits()


@pytest.fixture
async def session():
    async with SessionLocal() as s:
        yield s


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as c:
        yield c


def csrf(client: httpx.AsyncClient) -> dict[str, str]:
    return {"X-CSRF-Token": client.cookies.get("ms_csrf", "")}


async def signup(
    client: httpx.AsyncClient,
    email: str = "ada@example.com",
    password: str = "correct-horse-battery",
    name: str = "Ada Okonkwo",
) -> dict:
    resp = await client.post(
        "/api/auth/signup", json={"email": email, "password": password, "display_name": name}
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


@pytest.fixture
async def auth_client(client: httpx.AsyncClient) -> httpx.AsyncClient:
    await signup(client)
    return client


def link_token(text: str, path: str) -> str:
    """The token from the first `<path>?token=...` link in an email body."""
    import re

    match = re.search(rf"{re.escape(path)}\?token=([A-Za-z0-9_-]+)", text)
    assert match, f"no {path} link in: {text}"
    return match.group(1)


async def confirm_email(client: httpx.AsyncClient, email: str) -> None:
    """Follow the verification link from the outbox, as the address owner would."""
    from app.shared.mail import get_mailer

    message = next(m for m in get_mailer().latest(email) if "Confirm your email" in m.subject)
    resp = await client.post(
        "/api/auth/email/verify", json={"token": link_token(message.text, "/verify-email")}
    )
    assert resp.status_code == 200, resp.text
