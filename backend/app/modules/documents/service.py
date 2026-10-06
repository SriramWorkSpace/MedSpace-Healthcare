"""Documents: intake, storage, page text, status transitions, previews."""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import logging
import re
import uuid
from pathlib import PurePath

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.db import utcnow
from app.core.errors import Conflict, NotFound, PayloadTooLarge, Unprocessable, UnsupportedMedia
from app.modules.documents import files
from app.modules.documents.models import Document, DocumentKind, DocumentPage, DocumentStatus
from app.shared.storage import get_storage

logger = logging.getLogger("medspace.documents")

_EXT = {files.PDF: "pdf", files.PNG: "png", files.JPEG: "jpg", files.WEBP: "webp"}


def _storage_key(user_id: uuid.UUID, doc_id: uuid.UUID, suffix: str) -> str:
    return f"users/{user_id}/documents/{doc_id}/{suffix}"


def _title_from_filename(name: str) -> str:
    stem = PurePath(name).stem
    stem = re.sub(r"[_\-]+", " ", stem).strip()
    return (stem[:1].upper() + stem[1:])[:200] if stem else "Untitled document"


async def create_document(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    filename: str,
    data: bytes,
    kind: str | None = None,
    title: str | None = None,
) -> Document:
    settings = get_settings()
    if not data:
        raise Unprocessable("The file is empty.")
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise PayloadTooLarge(f"Files can be up to {settings.max_upload_mb} MB.")

    mime = files.sniff_mime(data)
    if mime is None:
        raise UnsupportedMedia("MedSpace accepts PDF, JPG, PNG and WEBP files.")
    if mime != files.PDF:
        size = files.image_size(data, mime)
        if size is None:
            raise UnsupportedMedia(
                "This image couldn't be read. Try saving it again as JPG or PNG."
            )
        w, h = size
        if w * h > files.MAX_IMAGE_PIXELS or max(w, h) > files.MAX_IMAGE_SIDE:
            raise Unprocessable(
                "This image is too large in pixels. Resize it (or photograph the page again) and "
                "try once more."
            )

    sha = hashlib.sha256(data).hexdigest()
    existing = await session.scalar(
        select(Document).where(Document.user_id == user_id, Document.sha256 == sha)
    )
    if existing:
        raise Conflict(
            "You've already uploaded this file.", extra={"document_id": str(existing.id)}
        )

    try:
        info = await asyncio.to_thread(files.inspect, data, mime)
    except files.UnreadableFile as exc:
        raise Unprocessable(str(exc)) from exc
    if info.page_count > settings.max_pages:
        raise Unprocessable(f"Documents can have up to {settings.max_pages} pages.")

    if kind is not None and kind not in {k.value for k in DocumentKind}:
        raise Unprocessable("Unknown document kind.")

    doc = Document(
        user_id=user_id,
        title=(title or _title_from_filename(filename)).strip()[:200],
        original_filename=PurePath(filename).name[:255] or "upload",
        kind=kind or DocumentKind.PRESCRIPTION,
        mime_type=mime,
        size_bytes=len(data),
        sha256=sha,
        storage_key="",
        page_count=info.page_count,
        has_text_layer=info.has_text_layer,
        status=DocumentStatus.QUEUED,
    )
    session.add(doc)
    await session.flush()
    doc.storage_key = _storage_key(user_id, doc.id, f"original.{_EXT[mime]}")
    for i, text in enumerate(info.page_texts, start=1):
        session.add(DocumentPage(document_id=doc.id, user_id=user_id, page_no=i, text=text))
    await get_storage().put(doc.storage_key, data, mime)
    return doc


async def list_documents(
    session: AsyncSession, user_id: uuid.UUID, *, status: str | None = None, kind: str | None = None
) -> tuple[list[Document], dict[str, int]]:
    stmt = select(Document).where(Document.user_id == user_id)
    if status:
        stmt = stmt.where(Document.status == status)
    if kind:
        stmt = stmt.where(Document.kind == kind)
    docs = list((await session.scalars(stmt.order_by(Document.created_at.desc()))).all())
    rows = await session.execute(
        select(Document.status, func.count())
        .where(Document.user_id == user_id)
        .group_by(Document.status)
    )
    counts = {s: 0 for s in DocumentStatus}
    counts.update({status_: n for status_, n in rows.all()})
    counts["all"] = sum(v for k, v in counts.items() if k != "all")
    return docs, counts


async def get_document(
    session: AsyncSession, user_id: uuid.UUID, doc_id: uuid.UUID, *, with_pages: bool = False
) -> Document:
    stmt = select(Document).where(Document.id == doc_id, Document.user_id == user_id)
    if with_pages:
        stmt = stmt.options(selectinload(Document.pages))
    doc = await session.scalar(stmt)
    if doc is None:
        raise NotFound("Document not found.")
    return doc


async def get_document_by_id(session: AsyncSession, doc_id: uuid.UUID) -> Document | None:
    """Unscoped load for background jobs. Never call from request handlers."""
    return await session.scalar(
        select(Document).where(Document.id == doc_id).options(selectinload(Document.pages))
    )


async def read_original(doc: Document) -> bytes:
    return await get_storage().get(doc.storage_key)


async def page_preview_png(doc: Document, page_no: int) -> bytes:
    """Rendered PNG for a page, cached in storage next to the original."""
    if page_no < 1 or page_no > doc.page_count:
        raise NotFound("Page not found.")
    storage = get_storage()
    key = _storage_key(doc.user_id, doc.id, f"preview-{page_no}.png")
    try:
        return await storage.get(key)
    except Exception:
        logger.debug("preview cache miss for %s page %s", doc.id, page_no)
    data = await read_original(doc)
    if doc.mime_type == files.PDF:
        pngs = await asyncio.to_thread(
            files.render_pages_png, data, doc.mime_type, dpi=130, max_pages=page_no
        )
        png = pngs[page_no - 1]
    else:
        png = (await asyncio.to_thread(files.render_pages_png, data, doc.mime_type, dpi=130))[0]
    await storage.put(key, png, files.PNG)
    return png


async def purge_user_files(user_id: uuid.UUID) -> None:
    """Remove every stored object for a user (account deletion, demo expiry)."""
    try:
        await get_storage().delete_prefix(f"users/{user_id}/")
    except Exception:
        logger.exception("could not purge files for user %s", user_id)


def set_status(doc: Document, status: DocumentStatus, error: str | None = None) -> None:
    doc.status = status
    doc.error = error
    if status in (DocumentStatus.NEEDS_REVIEW, DocumentStatus.FAILED):
        doc.processed_at = utcnow()


async def delete_document(session: AsyncSession, doc: Document) -> None:
    storage = get_storage()
    keys = [doc.storage_key] + [
        _storage_key(doc.user_id, doc.id, f"preview-{n}.png") for n in range(1, doc.page_count + 1)
    ]
    await session.delete(doc)
    await session.flush()
    for key in keys:
        with contextlib.suppress(Exception):  # previews may never have been rendered
            await storage.delete(key)
