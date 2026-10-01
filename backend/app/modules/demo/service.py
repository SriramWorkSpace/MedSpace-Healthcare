"""Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-lived account."""

from __future__ import annotations

import secrets
from datetime import timedelta

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow
from app.modules.identity import service as identity
from app.modules.identity.models import User
from app.modules.identity.schemas import SignupIn

DEMO_NAMES = ("Avery Lindqvist", "Noor Haddad", "Mateo Okafor", "Priya Raman", "Jun Takeda")


async def create_demo_account(session: AsyncSession) -> User:
    handle = secrets.token_hex(5)
    user = await identity.create_user(
        session,
        SignupIn(
            email=f"demo-{handle}@demo.medspace.dev",
            password=secrets.token_urlsafe(24),
            display_name=secrets.choice(DEMO_NAMES),
            timezone="America/New_York",
        ),
        is_demo=True,
    )
    return user


async def purge_expired_demo_accounts(session: AsyncSession) -> int:
    cutoff = utcnow() - timedelta(hours=get_settings().demo_ttl_hours)
    result = await session.execute(
        delete(User).where(User.is_demo.is_(True), User.created_at < cutoff)
    )
    await session.commit()
    return result.rowcount or 0
