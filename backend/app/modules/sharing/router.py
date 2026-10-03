from __future__ import annotations

import uuid
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request, Response, status

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.modules.documents import service as documents
from app.modules.sharing import service
from app.modules.sharing.schemas import PublicShare, ShareCreate, ShareCreated, ShareOut

router = APIRouter(prefix="/shares", tags=["sharing"])
public_router = APIRouter(
    prefix="/public/shares",
    tags=["sharing (public)"],
    dependencies=[Depends(rate_limit("public:shares", 60, 60, by="ip"))],
)

PUBLIC_HEADERS = {"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"}


@router.post(
    "",
    response_model=ShareCreated,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit("shares:create", 30, 3600))],
)
async def create_share(data: ShareCreate, request: Request, user: CurrentUser, session: DbSession):
    link, token = await service.create(session, user, data, request)
    await session.commit()
    await session.refresh(link)
    return ShareCreated(
        share=await service.to_out(session, link), url=service.share_url(token), token=token
    )


@router.get("", response_model=list[ShareOut])
async def list_shares(user: CurrentUser, session: DbSession):
    return [
        await service.to_out(session, link) for link in await service.list_links(session, user.id)
    ]


@router.delete("/{link_id}", response_model=ShareOut)
async def revoke_share(link_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession):
    link = await service.revoke(session, user, link_id, request)
    await session.commit()
    return await service.to_out(session, link)


@public_router.get("/{token}", response_model=PublicShare)
async def open_share(token: str, request: Request, response: Response, session: DbSession):
    bundle = await service.open_public(session, token, request)
    await session.commit()
    response.headers.update(PUBLIC_HEADERS)
    return bundle


@public_router.get(
    "/{token}/documents/{doc_id}/pages/{page_no}/preview",
    dependencies=[Depends(rate_limit("public:files", 120, 60, by="ip"))],
)
async def shared_preview(token: str, doc_id: uuid.UUID, page_no: int, session: DbSession):
    doc = await service.shared_document(session, token, doc_id)
    png = await documents.page_preview_png(doc, page_no)
    return Response(content=png, media_type="image/png", headers=PUBLIC_HEADERS)


@public_router.get(
    "/{token}/documents/{doc_id}/file",
    dependencies=[Depends(rate_limit("public:files", 120, 60, by="ip"))],
)
async def shared_file(token: str, doc_id: uuid.UUID, session: DbSession):
    doc = await service.shared_document(session, token, doc_id)
    data = await documents.read_original(doc)
    return Response(
        content=data,
        media_type=doc.mime_type,
        headers={
            **PUBLIC_HEADERS,
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(doc.original_filename)}",
        },
    )
