from __future__ import annotations

import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from app.core.db import SessionLocal, utcnow
from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.assistant import service
from app.modules.assistant.models import ChatMessage

logger = logging.getLogger("medspace.assistant")
router = APIRouter(prefix="/assistant", tags=["assistant"])


class ThreadIn(BaseModel):
    title: str | None = Field(None, max_length=120)


class ThreadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: str
    content: str
    citations: list
    created_at: datetime


class ThreadDetail(ThreadOut):
    messages: list[MessageOut]


class AskIn(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


@router.post(
    "/threads",
    response_model=ThreadOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit("assistant:threads", 30, 60))],
)
async def create_thread(data: ThreadIn, user: CurrentUser, session: DbSession):
    thread = await service.create_thread(session, user.id, data.title)
    await session.commit()
    return thread


@router.get("/threads", response_model=list[ThreadOut])
async def list_threads(user: CurrentUser, session: DbSession):
    return await service.list_threads(session, user.id)


@router.get("/threads/{thread_id}", response_model=ThreadDetail)
async def get_thread(thread_id: uuid.UUID, user: CurrentUser, session: DbSession):
    thread = await service.get_thread(session, user.id, thread_id)
    messages = await service.thread_messages(session, thread.id)
    return ThreadDetail(
        **ThreadOut.model_validate(thread).model_dump(),
        messages=[MessageOut.model_validate(m) for m in messages],
    )


@router.delete("/threads/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread(thread_id: uuid.UUID, user: CurrentUser, session: DbSession):
    thread = await service.get_thread(session, user.id, thread_id)
    await session.delete(thread)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/threads/{thread_id}/messages",
    dependencies=[Depends(rate_limit("assistant:ask", 20, 60))],
    responses={200: {"content": {"text/event-stream": {}}}},
)
async def ask(
    thread_id: uuid.UUID, data: AskIn, request: Request, user: CurrentUser, session: DbSession
):
    """Server-sent events: `sources`, then `token`*, then `done` (or `error`)."""
    thread = await service.get_thread(session, user.id, thread_id)
    history = await service.thread_messages(session, thread.id)
    question = data.content.strip()
    intent = service.classify(question)
    sources = await service.gather_sources(
        session, user.id, question, include_all_meds=intent == "meds"
    )
    session.add(ChatMessage(thread_id=thread.id, user_id=user.id, role="user", content=question))
    if thread.title == "New conversation":
        thread.title = question[:60] + ("…" if len(question) > 60 else "")
    thread.updated_at = utcnow()
    await session.commit()

    user_id, tid = user.id, thread.id

    async def events():
        yield service.sse("sources", {"intent": intent, "sources": [s.public() for s in sources]})
        parts: list[str] = []
        failed = False
        try:
            async for delta in service.answer_stream(question, intent, sources, history):
                parts.append(delta)
                yield service.sse("token", {"t": delta})
                if await request.is_disconnected():
                    break
        except Exception:
            logger.exception("assistant answer failed")
            failed = True
            yield service.sse("error", {"detail": "The assistant hit a snag. Please try again."})
        answer = "".join(parts).strip()
        if not answer or failed:
            return
        async with SessionLocal() as s:
            msg = ChatMessage(
                thread_id=tid,
                user_id=user_id,
                role="assistant",
                content=answer,
                citations=service.used_citations(answer, sources),
            )
            s.add(msg)
            await s.commit()
            yield service.sse("done", {"message_id": str(msg.id), "citations": msg.citations})

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
