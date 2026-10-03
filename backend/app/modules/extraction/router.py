from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Request

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.extraction import service
from app.modules.extraction.schemas import ConfirmIn, EvidenceOut, ExtractionOut

router = APIRouter(tags=["extraction"])


@router.get("/documents/{doc_id}/extraction", response_model=ExtractionOut)
async def get_latest_extraction(doc_id: uuid.UUID, user: CurrentUser, session: DbSession):
    return await service.latest_for_document(session, user.id, doc_id)


@router.get(
    "/documents/{doc_id}/evidence",
    response_model=EvidenceOut,
    dependencies=[Depends(rate_limit("documents:evidence", 60, 60))],
)
async def get_evidence(doc_id: uuid.UUID, user: CurrentUser, session: DbSession):
    """Where each field of the latest draft or confirmed reading is printed on the page."""
    extraction, found = await service.evidence_for_document(session, user.id, doc_id)
    await session.commit()
    return EvidenceOut(
        extraction_id=extraction.id,
        available=found.get("available", False),
        reason=found.get("reason"),
        fields=found.get("fields", {}),
        items=found.get("items", {}),
    )


@router.post(
    "/extractions/{extraction_id}/confirm",
    response_model=ExtractionOut,
    dependencies=[Depends(rate_limit("extractions:confirm", 30, 60))],
)
async def confirm_extraction(
    extraction_id: uuid.UUID,
    data: ConfirmIn,
    request: Request,
    user: CurrentUser,
    session: DbSession,
):
    extraction = await service.confirm(session, user, extraction_id, data, request)
    await session.commit()
    return extraction


@router.post("/extractions/{extraction_id}/discard", response_model=ExtractionOut)
async def discard_extraction(
    extraction_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession
):
    extraction = await service.discard(session, user, extraction_id, request)
    await session.commit()
    return extraction
