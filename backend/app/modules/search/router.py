from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.search import service
from app.modules.search.service import SearchResults

router = APIRouter(tags=["search"])


@router.get(
    "/search",
    response_model=SearchResults,
    dependencies=[Depends(rate_limit("search", 120, 60))],
)
async def search(
    user: CurrentUser, session: DbSession, q: str = Query(min_length=2, max_length=100)
):
    return await service.search(session, user.id, q)
