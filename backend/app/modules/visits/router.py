from __future__ import annotations

import uuid

from fastapi import APIRouter

from app.core.deps import CurrentUser, DbSession
from app.modules.visits import service
from app.modules.visits.schemas import VisitBrief, VisitCreate, VisitOut, VisitUpdate

router = APIRouter(prefix="/visits", tags=["visits"])


@router.post("", response_model=VisitOut, status_code=201)
async def create_visit(data: VisitCreate, user: CurrentUser, session: DbSession):
    prep = await service.create_prep(session, user, data)
    await session.commit()
    await session.refresh(prep)
    return prep


@router.get("", response_model=list[VisitOut])
async def list_visits(user: CurrentUser, session: DbSession):
    return await service.list_preps(session, user.id)


@router.get("/{prep_id}", response_model=VisitOut)
async def get_visit(prep_id: uuid.UUID, user: CurrentUser, session: DbSession):
    return await service.get_prep(session, user.id, prep_id)


@router.patch("/{prep_id}", response_model=VisitOut)
async def update_visit(
    prep_id: uuid.UUID, data: VisitUpdate, user: CurrentUser, session: DbSession
):
    prep = await service.update_prep(session, user, prep_id, data)
    await session.commit()
    await session.refresh(prep)
    return prep


@router.delete("/{prep_id}", status_code=204)
async def delete_visit(prep_id: uuid.UUID, user: CurrentUser, session: DbSession):
    await service.delete_prep(session, user.id, prep_id)
    await session.commit()


@router.get("/{prep_id}/brief", response_model=VisitBrief)
async def visit_brief(prep_id: uuid.UUID, user: CurrentUser, session: DbSession):
    prep = await service.get_prep(session, user.id, prep_id)
    return await service.brief(session, user, prep)
