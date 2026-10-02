from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.doses import service
from app.modules.doses.schemas import AdherenceOut, DoseLogIn, DoseLogOut

router = APIRouter(tags=["doses"])

TIME = r"^([01]\d|2[0-3]):[0-5]\d$"


@router.put(
    "/doses",
    response_model=DoseLogOut,
    dependencies=[Depends(rate_limit("doses", 240, 60))],
)
async def log_dose(data: DoseLogIn, user: CurrentUser, session: DbSession):
    out = await service.log_dose(session, user, data)
    await session.commit()
    return out


@router.delete("/doses", status_code=204)
async def clear_dose(
    user: CurrentUser,
    session: DbSession,
    medication_id: uuid.UUID,
    date: date,
    time: str = Query(pattern=TIME),
):
    await service.clear_dose(session, user, medication_id, date, time)
    await session.commit()


@router.get("/adherence", response_model=AdherenceOut)
async def adherence(user: CurrentUser, session: DbSession, days: int = Query(30, ge=7, le=120)):
    return await service.adherence(session, user, days)


@router.get("/adherence/{medication_id}", response_model=AdherenceOut)
async def medication_adherence(
    medication_id: uuid.UUID,
    user: CurrentUser,
    session: DbSession,
    days: int = Query(56, ge=7, le=120),
):
    return await service.adherence(session, user, days, medication_id)
