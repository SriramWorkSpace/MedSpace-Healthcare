from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Query

from app.core.deps import CurrentUser, DbSession
from app.modules.timeline import service
from app.modules.timeline.schemas import DashboardOut, TimelinePage

router = APIRouter(tags=["timeline"])


@router.get("/timeline", response_model=TimelinePage)
async def get_timeline(
    user: CurrentUser,
    session: DbSession,
    before: date | None = None,
    types: str | None = Query(None, description="Comma-separated event types"),
    limit: int = Query(40, ge=5, le=200),
):
    return await service.timeline_page(
        session, user, before=before, types=service.parse_types(types), limit=limit
    )


@router.get("/dashboard", response_model=DashboardOut)
async def get_dashboard(user: CurrentUser, session: DbSession):
    return await service.dashboard(session, user)
