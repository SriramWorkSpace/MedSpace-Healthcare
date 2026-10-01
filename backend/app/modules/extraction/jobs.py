"""Background job: process an uploaded document end to end."""

from __future__ import annotations

import logging
import uuid

from app.core.db import SessionLocal
from app.modules.documents import service as documents
from app.modules.documents.models import DocumentStatus
from app.modules.extraction import service as extraction
from app.modules.identity.models import User
from app.shared.queue import job

logger = logging.getLogger("medspace.jobs")


@job
async def process_document(ctx: dict, document_id: str) -> str:
    doc_id = uuid.UUID(document_id)
    async with SessionLocal() as session:
        doc = await documents.get_document_by_id(session, doc_id)
        if doc is None:
            return "missing"
        documents.set_status(doc, DocumentStatus.PROCESSING)
        await session.commit()

        user = await session.get(User, doc.user_id)
        pages = [p.text for p in doc.pages]
        try:
            payload, method, model = await extraction.extract_document(
                doc, pages, user.dose_times if user else {}
            )
            await extraction.save_draft(session, doc, payload, method, model)
            documents.set_status(doc, DocumentStatus.NEEDS_REVIEW)
            await session.commit()
        except extraction.ExtractionFailed as exc:
            await session.rollback()
            documents.set_status(doc, DocumentStatus.FAILED, str(exc))
            await session.commit()
            return "failed"
        except Exception:
            logger.exception("processing document %s failed", document_id)
            await session.rollback()
            documents.set_status(
                doc, DocumentStatus.FAILED, "Something went wrong while reading this file."
            )
            await session.commit()
            return "failed"

    # Indexing for Ask MedSpace is best-effort and never blocks review.
    try:
        from app.modules.assistant import service as assistant

        async with SessionLocal() as session:
            await assistant.index_document(session, doc_id)
            await session.commit()
    except ImportError:
        pass
    except Exception:
        logger.exception("indexing document %s failed", document_id)
    return "ok"
