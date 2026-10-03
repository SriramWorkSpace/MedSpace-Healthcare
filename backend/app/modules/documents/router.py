from __future__ import annotations

import uuid
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, Query, Request, Response, UploadFile, status

from app.core.config import get_settings
from app.core.deps import CurrentUser, DbSession
from app.core.errors import Conflict, PayloadTooLarge
from app.core.ratelimit import rate_limit
from app.modules.audit import service as audit
from app.modules.documents import service
from app.modules.documents.models import DocumentStatus
from app.modules.documents.schemas import DocumentDetail, DocumentList, DocumentOut, DocumentUpdate
from app.shared.queue import enqueue

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(
    "",
    response_model=DocumentOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(rate_limit("documents:upload", 30, 60))],
)
async def upload_document(
    request: Request,
    user: CurrentUser,
    session: DbSession,
    file: UploadFile = File(...),
    kind: str | None = Form(None),
    title: str | None = Form(None),
):
    limit = get_settings().max_upload_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise PayloadTooLarge(f"Files can be up to {get_settings().max_upload_mb} MB.")
    doc = await service.create_document(
        session,
        user_id=user.id,
        filename=file.filename or "upload",
        data=data,
        kind=kind,
        title=title,
    )
    await audit.record(
        session,
        action="document.uploaded",
        user_id=user.id,
        request=request,
        entity_type="document",
        entity_id=doc.id,
        meta={"filename": doc.original_filename, "pages": doc.page_count},
    )
    await session.commit()
    await enqueue("process_document", str(doc.id))
    return doc


@router.get("", response_model=DocumentList)
async def list_documents(
    user: CurrentUser,
    session: DbSession,
    status_: str | None = Query(None, alias="status"),
    kind: str | None = None,
):
    docs, counts = await service.list_documents(session, user.id, status=status_, kind=kind)
    return DocumentList(items=[DocumentOut.model_validate(d) for d in docs], counts=counts)


@router.get("/{doc_id}", response_model=DocumentDetail)
async def get_document(doc_id: uuid.UUID, user: CurrentUser, session: DbSession):
    return await service.get_document(session, user.id, doc_id, with_pages=True)


@router.get("/{doc_id}/file")
async def download_document(doc_id: uuid.UUID, user: CurrentUser, session: DbSession):
    doc = await service.get_document(session, user.id, doc_id)
    data = await service.read_original(doc)
    filename = quote(doc.original_filename)
    return Response(
        content=data,
        media_type=doc.mime_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
            "Cache-Control": "private, no-store",
        },
    )


@router.get("/{doc_id}/pages/{page_no}/preview")
async def page_preview(doc_id: uuid.UUID, page_no: int, user: CurrentUser, session: DbSession):
    doc = await service.get_document(session, user.id, doc_id)
    png = await service.page_preview_png(doc, page_no)
    return Response(
        content=png, media_type="image/png", headers={"Cache-Control": "private, max-age=3600"}
    )


@router.patch("/{doc_id}", response_model=DocumentOut)
async def update_document(
    doc_id: uuid.UUID, data: DocumentUpdate, user: CurrentUser, session: DbSession
):
    doc = await service.get_document(session, user.id, doc_id)
    if data.title is not None:
        doc.title = data.title.strip()
    if data.kind is not None:
        doc.kind = data.kind
    await session.commit()
    return doc


@router.post(
    "/{doc_id}/reprocess",
    response_model=DocumentOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(rate_limit("documents:reprocess", 10, 60))],  # an AI call each
)
async def reprocess_document(
    doc_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession
):
    doc = await service.get_document(session, user.id, doc_id)
    if doc.status in (DocumentStatus.QUEUED, DocumentStatus.PROCESSING):
        raise Conflict("This document is already being processed.")
    service.set_status(doc, DocumentStatus.QUEUED)
    await audit.record(
        session,
        action="document.reprocessed",
        user_id=user.id,
        request=request,
        entity_type="document",
        entity_id=doc.id,
    )
    await session.commit()
    await enqueue("process_document", str(doc.id))
    return doc


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession
):
    doc = await service.get_document(session, user.id, doc_id)
    await audit.record(
        session,
        action="document.deleted",
        user_id=user.id,
        request=request,
        entity_type="document",
        entity_id=doc.id,
        meta={"title": doc.title},
    )
    await service.delete_document(session, doc)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
