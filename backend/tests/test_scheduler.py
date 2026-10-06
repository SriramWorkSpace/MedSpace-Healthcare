"""Inline deployments run the worker's scheduled jobs themselves (free single-container hosting)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx
from sqlalchemy import func, select, update

from app.core.db import utcnow
from app.main import run_scheduled_jobs
from app.modules.identity.models import User


async def test_expired_demo_accounts_are_purged_without_a_worker(
    client: httpx.AsyncClient, session
):
    await client.post("/api/auth/demo")
    assert await session.scalar(select(func.count()).select_from(User)) >= 1
    await session.execute(update(User).values(created_at=utcnow() - timedelta(hours=25)))
    await session.commit()

    ran = await run_scheduled_jobs(datetime(2026, 10, 7, 12, 8, tzinfo=UTC))
    assert ran == ["reminders"]  # not the purge minute: nothing deleted yet
    assert await session.scalar(select(func.count()).select_from(User)) >= 1

    ran = await run_scheduled_jobs(datetime(2026, 10, 7, 12, 7, tzinfo=UTC))
    assert ran == ["reminders", "demo purge"]
    session.expire_all()
    assert await session.scalar(select(func.count()).select_from(User)) == 0


async def test_share_links_are_tidied_daily():
    ran = await run_scheduled_jobs(datetime(2026, 10, 7, 3, 15, tzinfo=UTC))
    assert ran == ["reminders", "share link purge"]
