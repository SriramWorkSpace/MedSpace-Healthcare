from __future__ import annotations

import uuid

from fastapi import APIRouter, Path, Query

from app.core.deps import CurrentUser, DbSession
from app.modules.records import service
from app.modules.records.schemas import (
    CareActionOut,
    CareActionUpdate,
    DietNotesOut,
    LabTrendDetail,
    LabTrendOut,
    MedicationOut,
    MedicationUpdate,
    PrescriptionOut,
    PrescriptionSummary,
)

router = APIRouter(tags=["records"])


@router.get("/prescriptions", response_model=list[PrescriptionSummary])
async def list_prescriptions(user: CurrentUser, session: DbSession):
    return await service.list_prescriptions(session, user.id)


@router.get("/prescriptions/{prescription_id}", response_model=PrescriptionOut)
async def get_prescription(prescription_id: uuid.UUID, user: CurrentUser, session: DbSession):
    return await service.get_prescription(session, user.id, prescription_id)


@router.get("/medications", response_model=list[MedicationOut])
async def list_medications(
    user: CurrentUser,
    session: DbSession,
    status: str | None = Query(None, pattern="^(active|upcoming|completed|stopped)$"),
):
    return await service.list_medications(session, user.id, status=status)


@router.patch("/medications/{med_id}", response_model=MedicationOut)
async def update_medication(
    med_id: uuid.UUID, data: MedicationUpdate, user: CurrentUser, session: DbSession
):
    med = await service.update_medication(session, user.id, med_id, data)
    await session.commit()
    return service.to_medication_out(med)


@router.get("/diet-notes", response_model=DietNotesOut)
async def list_diet_notes(user: CurrentUser, session: DbSession):
    return await service.list_diet_notes(session, user.id)


@router.delete("/diet-notes/{note_id}", status_code=204)
async def delete_diet_note(note_id: uuid.UUID, user: CurrentUser, session: DbSession):
    await service.delete_diet_note(session, user.id, note_id)
    await session.commit()


@router.get("/labs", response_model=list[LabTrendOut])
async def list_lab_trends(user: CurrentUser, session: DbSession):
    return await service.list_lab_trends(session, user.id)


@router.get("/labs/{key}", response_model=LabTrendDetail)
async def get_lab_trend(
    user: CurrentUser, session: DbSession, key: str = Path(pattern=r"^[a-z0-9-]{1,80}$")
):
    return await service.get_lab_trend(session, user.id, key)


@router.delete("/lab-results/{result_id}", status_code=204)
async def delete_lab_result(result_id: uuid.UUID, user: CurrentUser, session: DbSession):
    await service.delete_lab_result(session, user.id, result_id)
    await session.commit()


@router.get("/care-actions", response_model=list[CareActionOut])
async def list_care_actions(user: CurrentUser, session: DbSession, open_only: bool = False):
    return await service.list_care_actions(session, user.id, open_only=open_only)


@router.patch("/care-actions/{action_id}", response_model=CareActionOut)
async def update_care_action(
    action_id: uuid.UUID, data: CareActionUpdate, user: CurrentUser, session: DbSession
):
    action = await service.update_care_action(session, user.id, action_id, data)
    await session.commit()
    return action
