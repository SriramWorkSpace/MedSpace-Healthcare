"""Demo background jobs."""

from __future__ import annotations

import uuid

from app.core.db import SessionLocal
from app.modules.assistant import service as assistant
from app.modules.documents import service as documents
from app.shared.queue import job


@job
async def index_demo_documents(ctx: dict, user_id: str) -> int:
    """Index a new demo account's documents for Ask MedSpace.

    Embedding is most of the demo's setup cost (about 90% on a small shared CPU), so it runs after
    the visitor is signed in instead of before. Enqueue it only after the seed has committed.
    """
    async with SessionLocal() as session:
        docs, _ = await documents.list_documents(session, uuid.UUID(user_id))
        chunks = 0
        for d in docs:
            chunks += await assistant.index_document(session, d.id)
        await session.commit()
    return chunks
