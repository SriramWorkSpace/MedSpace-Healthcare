"""Audit trail: `record()` is the single write path, used by every module."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ratelimit import client_ip
from app.modules.audit.models import AuditLog


async def record(
    session: AsyncSession,
    *,
    action: str,
    user_id: uuid.UUID | None,
    request: Request | None = None,
    actor: str = "user",
    entity_type: str | None = None,
    entity_id: uuid.UUID | None = None,
    meta: dict[str, Any] | None = None,
) -> AuditLog:
    """Stage an audit row in the caller's transaction (committed with the business change)."""
    entry = AuditLog(
        user_id=user_id,
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip=client_ip(request) if request else None,
        user_agent=(request.headers.get("user-agent") or "")[:256] if request else None,
        meta=meta or {},
    )
    session.add(entry)
    return entry


async def list_for_user(
    session: AsyncSession,
    user_id: uuid.UUID,
    *,
    limit: int = 50,
    cursor: str | None = None,
    action_prefix: str | None = None,
) -> tuple[list[AuditLog], str | None]:
    stmt = select(AuditLog).where(AuditLog.user_id == user_id)
    if action_prefix:
        stmt = stmt.where(AuditLog.action.startswith(action_prefix))
    if cursor:
        stmt = stmt.where(AuditLog.created_at < datetime.fromisoformat(cursor))
    stmt = stmt.order_by(AuditLog.created_at.desc()).limit(limit + 1)
    rows = list((await session.scalars(stmt)).all())
    next_cursor = rows[limit - 1].created_at.isoformat() if len(rows) > limit else None
    return rows[:limit], next_cursor
