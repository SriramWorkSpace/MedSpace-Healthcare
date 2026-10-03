from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Request

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.circle import service
from app.modules.circle.schemas import (
    AcceptIn,
    CareLinkOut,
    CircleOut,
    InviteCreated,
    InviteIn,
    InvitePreview,
    RoleIn,
)
from app.modules.identity.models import User

router = APIRouter(prefix="/circle", tags=["circle"])


@router.get("", response_model=CircleOut)
async def get_circle(user: CurrentUser, session: DbSession):
    return await service.circle(session, user)


@router.post(
    "/invites",
    response_model=InviteCreated,
    status_code=201,
    dependencies=[Depends(rate_limit("circle-invite", 20, 3600))],
)
async def invite(data: InviteIn, request: Request, user: CurrentUser, session: DbSession):
    link, token = await service.invite(session, user, data, request)
    await session.commit()
    await session.refresh(link)
    out = service.to_out(link, None)
    return InviteCreated(link=out, url=service.invite_url(token), token=token)


@router.get("/invites/{token}", response_model=InvitePreview)
async def preview(token: str, user: CurrentUser, session: DbSession):
    return await service.preview(session, user, token)


@router.post("/accept", response_model=CareLinkOut)
async def accept(data: AcceptIn, request: Request, user: CurrentUser, session: DbSession):
    link = await service.accept(session, user, data.token, request)
    await session.commit()
    owner = await session.get(User, link.owner_id)
    return service.to_out(link, owner)


@router.patch("/{link_id}", response_model=CareLinkOut)
async def set_role(link_id: uuid.UUID, data: RoleIn, user: CurrentUser, session: DbSession):
    link = await service.set_role(session, user, link_id, data.role)
    await session.commit()
    other = await session.get(User, link.caregiver_id) if link.caregiver_id else None
    return service.to_out(link, other)


@router.delete("/{link_id}", status_code=204)
async def revoke(link_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession):
    await service.revoke(session, user, link_id, request)
    await session.commit()
