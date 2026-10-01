from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.deps import CurrentUser
from app.modules.audit import service
from app.modules.audit.schemas import AuditLogOut, AuditPage

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=AuditPage)
async def list_audit(
    user: CurrentUser,
    session: AsyncSession = Depends(get_session),
    cursor: str | None = None,
    action: str | None = Query(None, description="Filter by action prefix, e.g. 'share.'"),
    limit: int = Query(50, ge=1, le=200),
) -> AuditPage:
    rows, next_cursor = await service.list_for_user(
        session, user.id, limit=limit, cursor=cursor, action_prefix=action
    )
    return AuditPage(items=[AuditLogOut.model_validate(r) for r in rows], next_cursor=next_cursor)
