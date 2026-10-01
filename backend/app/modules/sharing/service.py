"""Secure sharing: scoped, expiring, revocable, view-limited, audited (ADR-010)."""

from __future__ import annotations

import uuid
from datetime import timedelta

from fastapi import Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow
from app.core.errors import Gone, NotFound, Unprocessable
from app.core.security import new_opaque_token, sha256_hex
from app.modules.audit import service as audit
from app.modules.documents.models import Document
from app.modules.identity.models import User
from app.modules.records import service as records
from app.modules.records.models import Prescription
from app.modules.sharing.models import ShareLink, ShareLinkItem
from app.modules.sharing.schemas import (
    PublicDocument,
    PublicShare,
    ShareCreate,
    ShareItemOut,
    ShareOut,
)


def link_status(link: ShareLink) -> str:
    if link.revoked_at is not None:
        return "revoked"
    if link.expires_at <= utcnow():
        return "expired"
    if link.max_views is not None and link.view_count >= link.max_views:
        return "exhausted"
    return "active"


async def _titles(session: AsyncSession, items: list[ShareLinkItem]) -> dict[uuid.UUID, str]:
    doc_ids = [i.item_id for i in items if i.item_type == "document"]
    rx_ids = [i.item_id for i in items if i.item_type == "prescription"]
    titles: dict[uuid.UUID, str] = {}
    if doc_ids:
        rows = await session.execute(
            select(Document.id, Document.title).where(Document.id.in_(doc_ids))
        )
        titles.update(dict(rows.all()))
    if rx_ids:
        rows = await session.execute(
            select(Prescription.id, Prescription.prescriber_name, Prescription.clinic_name).where(
                Prescription.id.in_(rx_ids)
            )
        )
        for pid, who, clinic in rows.all():
            titles[pid] = f"Prescription from {who or clinic or 'your prescriber'}"
    return titles


async def to_out(session: AsyncSession, link: ShareLink) -> ShareOut:
    titles = await _titles(session, link.items)
    return ShareOut(
        id=link.id,
        label=link.label,
        token_hint=link.token_hint,
        status=link_status(link),
        expires_at=link.expires_at,
        revoked_at=link.revoked_at,
        max_views=link.max_views,
        view_count=link.view_count,
        last_viewed_at=link.last_viewed_at,
        created_at=link.created_at,
        items=[
            ShareItemOut(
                type=i.item_type, id=i.item_id, title=titles.get(i.item_id, "Removed item")
            )
            for i in link.items
        ],
    )


async def create(
    session: AsyncSession, user: User, data: ShareCreate, request: Request | None = None
) -> tuple[ShareLink, str]:
    wanted = {(i.type, i.id) for i in data.items}
    doc_ids = {i for t, i in wanted if t == "document"}
    rx_ids = {i for t, i in wanted if t == "prescription"}
    owned_docs = (
        set(
            (
                await session.scalars(
                    select(Document.id).where(Document.user_id == user.id, Document.id.in_(doc_ids))
                )
            ).all()
        )
        if doc_ids
        else set()
    )
    owned_rx = (
        set(
            (
                await session.scalars(
                    select(Prescription.id).where(
                        Prescription.user_id == user.id, Prescription.id.in_(rx_ids)
                    )
                )
            ).all()
        )
        if rx_ids
        else set()
    )
    if owned_docs != doc_ids or owned_rx != rx_ids:
        raise Unprocessable("Some of those items don't exist or aren't yours to share.")

    token = new_opaque_token(32)
    link = ShareLink(
        user_id=user.id,
        label=data.label.strip(),
        token_hash=sha256_hex(token),
        token_hint=token[-6:],
        expires_at=utcnow() + timedelta(days=data.expires_in_days),
        max_views=data.max_views,
        items=[ShareLinkItem(item_type=t, item_id=i) for t, i in sorted(wanted, key=str)],
    )
    session.add(link)
    await session.flush()
    await audit.record(
        session,
        action="share.created",
        user_id=user.id,
        request=request,
        entity_type="share_link",
        entity_id=link.id,
        meta={"label": link.label, "items": len(wanted), "days": data.expires_in_days},
    )
    return link, token


async def purge_stale_links(session: AsyncSession, older_than_days: int = 30) -> int:
    """Delete links that expired or were revoked long ago (their audit rows remain)."""
    from sqlalchemy import delete, or_

    cutoff = utcnow() - timedelta(days=older_than_days)
    result = await session.execute(
        delete(ShareLink).where(or_(ShareLink.expires_at < cutoff, ShareLink.revoked_at < cutoff))
    )
    await session.commit()
    return result.rowcount or 0


def share_url(token: str) -> str:
    return f"{get_settings().frontend_url}/s/{token}"


async def list_links(session: AsyncSession, user_id: uuid.UUID) -> list[ShareLink]:
    return list(
        (
            await session.scalars(
                select(ShareLink)
                .where(ShareLink.user_id == user_id)
                .order_by(ShareLink.created_at.desc())
            )
        ).all()
    )


async def revoke(
    session: AsyncSession, user: User, link_id: uuid.UUID, request: Request | None = None
) -> ShareLink:
    link = await session.scalar(
        select(ShareLink).where(ShareLink.id == link_id, ShareLink.user_id == user.id)
    )
    if link is None:
        raise NotFound("Share link not found.")
    if link.revoked_at is None:
        link.revoked_at = utcnow()
        await audit.record(
            session,
            action="share.revoked",
            user_id=user.id,
            request=request,
            entity_type="share_link",
            entity_id=link.id,
            meta={"label": link.label},
        )
    await session.flush()
    return link


# --------------------------------------------------------------------------- public access

_GONE_REASONS = {
    "expired": "This share link has expired.",
    "revoked": "This share link was turned off by its owner.",
    "exhausted": "This share link has reached its view limit.",
}


async def resolve(session: AsyncSession, token: str) -> ShareLink:
    link = await session.scalar(select(ShareLink).where(ShareLink.token_hash == sha256_hex(token)))
    if link is None:
        raise NotFound("This share link doesn't exist.")
    status = link_status(link)
    if status != "active":
        raise Gone(_GONE_REASONS[status], extra={"reason": status})
    return link


async def open_public(session: AsyncSession, token: str, request: Request) -> PublicShare:
    link = await resolve(session, token)
    # Atomic increment guarded by the limit, so concurrent views can't exceed max_views.
    counted = await session.execute(
        update(ShareLink)
        .where(
            ShareLink.id == link.id,
            (ShareLink.max_views.is_(None)) | (ShareLink.view_count < ShareLink.max_views),
        )
        .values(view_count=ShareLink.view_count + 1, last_viewed_at=utcnow())
        .returning(ShareLink.view_count)
    )
    views = counted.scalar_one_or_none()
    if views is None:
        raise Gone(_GONE_REASONS["exhausted"], extra={"reason": "exhausted"})
    await audit.record(
        session,
        action="share.viewed",
        user_id=link.user_id,
        actor="public",
        request=request,
        entity_type="share_link",
        entity_id=link.id,
        meta={"label": link.label, "view": views},
    )

    owner = await session.get(User, link.user_id)
    prescriptions = []
    documents = []
    for item in link.items:
        if item.item_type == "prescription":
            try:
                prescriptions.append(
                    await records.get_prescription(session, link.user_id, item.item_id)
                )
            except NotFound:
                continue
        else:
            doc = await session.scalar(
                select(Document).where(
                    Document.id == item.item_id, Document.user_id == link.user_id
                )
            )
            if doc:
                documents.append(
                    PublicDocument(
                        id=doc.id,
                        title=doc.title,
                        kind=doc.kind,
                        page_count=doc.page_count,
                        document_date=doc.document_date,
                    )
                )
    await session.flush()
    return PublicShare(
        label=link.label,
        shared_by=(owner.display_name.split()[0] if owner else "Someone"),
        expires_at=link.expires_at,
        views_left=None if link.max_views is None else max(0, link.max_views - views),
        prescriptions=prescriptions,
        documents=documents,
    )


async def shared_document(session: AsyncSession, token: str, doc_id: uuid.UUID) -> Document:
    """A document reachable through the link: shared directly, or the source of a shared Rx."""
    link = await resolve(session, token)
    direct = any(i.item_type == "document" and i.item_id == doc_id for i in link.items)
    via_rx = False
    rx_ids = [i.item_id for i in link.items if i.item_type == "prescription"]
    if not direct and rx_ids:
        via_rx = bool(
            await session.scalar(
                select(Prescription.id).where(
                    Prescription.id.in_(rx_ids), Prescription.document_id == doc_id
                )
            )
        )
    if not (direct or via_rx):
        raise NotFound("Not part of this share.")
    doc = await session.scalar(
        select(Document).where(Document.id == doc_id, Document.user_id == link.user_id)
    )
    if doc is None:
        raise NotFound("Not part of this share.")
    return doc
