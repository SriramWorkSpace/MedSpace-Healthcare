from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.supply import service
from app.modules.supply.schemas import RefillIn, SupplyIn, SupplyOut

router = APIRouter(prefix="/supply", tags=["supply"])


@router.get("", response_model=list[SupplyOut])
async def list_supplies(user: CurrentUser, session: DbSession):
    return await service.list_supplies(session, user)


@router.put(
    "/{medication_id}",
    response_model=SupplyOut,
    dependencies=[Depends(rate_limit("supply:write", 60, 60))],
)
async def set_supply(
    medication_id: uuid.UUID, data: SupplyIn, user: CurrentUser, session: DbSession
):
    out = await service.set_supply(session, user, medication_id, data)
    await session.commit()
    return out


@router.post(
    "/{medication_id}/refill",
    response_model=SupplyOut,
    dependencies=[Depends(rate_limit("supply:write", 60, 60))],
)
async def refill(medication_id: uuid.UUID, data: RefillIn, user: CurrentUser, session: DbSession):
    out = await service.refill(session, user, medication_id, data)
    await session.commit()
    return out


@router.delete("/{medication_id}", status_code=204)
async def clear_supply(medication_id: uuid.UUID, user: CurrentUser, session: DbSession):
    await service.clear_supply(session, user, medication_id)
    await session.commit()
