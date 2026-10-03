"""Care circle (ADR-026): invite, accept, revoke, and resolve "acting for" requests.

A caregiver opens someone else's records by sending `X-Acting-For: <owner id>`. `resolve_acting`
is the single place that decides whether that request is allowed: there must be an active link,
and the route must be on the allow-list for the link's role. Everything not listed (uploads,
confirmations, sharing, the assistant, settings) is refused, so new endpoints are private to
their owner by default.
"""

from __future__ import annotations

import uuid
from datetime import timedelta

from fastapi import Request
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow
from app.core.errors import Conflict, Forbidden, Gone, NotFound, Unprocessable
from app.core.security import new_opaque_token, sha256_hex
from app.modules.audit import service as audit
from app.modules.circle.models import CareLink
from app.modules.circle.schemas import CareLinkOut, CircleOut, InviteIn, InvitePreview, Person
from app.modules.identity.models import User

INVITE_DAYS = 7
MAX_LINKS = 10

# Routes (method, router-relative template) a caregiver may use on someone else's records.
_READ = {
    ("GET", p)
    for p in (
        "/dashboard",
        "/timeline",
        "/search",
        "/prescriptions",
        "/prescriptions/{prescription_id}",
        "/medications",
        "/care-actions",
        "/diet-notes",
        "/labs",
        "/labs/{key}",
        "/adherence",
        "/adherence/{medication_id}",
        "/supply",
        "/visits",
        "/visits/{prep_id}",
        "/visits/{prep_id}/brief",
        "/documents",
        "/documents/{doc_id}",
        "/documents/{doc_id}/file",
        "/documents/{doc_id}/pages/{page_no}/preview",
        "/documents/{doc_id}/extraction",
    )
}
_HELP = {
    ("PUT", "/doses"),
    ("DELETE", "/doses"),
    ("PATCH", "/care-actions/{action_id}"),
    ("PUT", "/supply/{medication_id}"),
    ("POST", "/supply/{medication_id}/refill"),
}
ALLOWED = {"viewer": _READ, "helper": _READ | _HELP}

# Routes about the signed-in person themselves: the acting header is ignored here.
# Compared by first path segment: a prefix test would treat "/medications" as "/me".
_SELF_SECTIONS = {"auth", "circle", "me", "audit", "integrations", "demo", "public", "push"}


def link_status(link: CareLink) -> str:
    if link.status == "pending" and link.expires_at < utcnow():
        return "expired"
    return link.status


async def resolve_acting(
    session: AsyncSession, request: Request, user: User, owner_ref: str
) -> User:
    """Return the user whose records this request acts on (the caller, or an owner)."""
    route = request.scope.get("route")
    path = getattr(route, "path_format", None) or getattr(route, "path", "") or ""
    if path.strip("/").split("/", 1)[0] in _SELF_SECTIONS:
        return user
    try:
        owner_id = uuid.UUID(owner_ref)
    except ValueError as exc:
        raise Forbidden("You don't have access to those records.") from exc
    if owner_id == user.id:
        return user
    link = await session.scalar(
        select(CareLink).where(
            CareLink.owner_id == owner_id,
            CareLink.caregiver_id == user.id,
            CareLink.status == "active",
        )
    )
    if link is None:
        raise Forbidden("You don't have access to those records.")
    method = request.method.upper()
    if (method, path) not in ALLOWED[link.role]:
        raise Forbidden(
            "That isn't available while viewing someone else's records."
            if method == "GET" or link.role == "helper"
            else "As a viewer you can read these records but not change them."
        )
    owner = await session.get(User, owner_id)
    if owner is None:
        raise Forbidden("You don't have access to those records.")
    request.state.caregiver = user
    if method != "GET":
        # Stage an audit row in the same transaction: it commits only if the change does.
        await audit.record(
            session,
            action="caregiver.change",
            user_id=owner.id,
            actor="caregiver",
            request=request,
            meta={
                "caregiver_id": str(user.id),
                "caregiver": user.display_name,
                "method": method,
                "path": path,
            },
        )
    return owner


def _person(user: User | None, email: str) -> Person:
    return Person(
        id=user.id if user else None, name=user.display_name if user else email, email=email
    )


def to_out(link: CareLink, other: User | None) -> CareLinkOut:
    return CareLinkOut(
        id=link.id,
        role=link.role,
        status=link_status(link),
        person=_person(other, other.email if other else link.invite_email),
        created_at=link.created_at,
        accepted_at=link.accepted_at,
        expires_at=link.expires_at,
    )


async def circle(session: AsyncSession, user: User) -> CircleOut:
    links = (
        await session.scalars(
            select(CareLink)
            .where(
                or_(CareLink.owner_id == user.id, CareLink.caregiver_id == user.id),
                CareLink.status != "revoked",
            )
            .order_by(CareLink.created_at)
        )
    ).all()
    ids = {lnk.owner_id for lnk in links} | {lnk.caregiver_id for lnk in links if lnk.caregiver_id}
    people = {u.id: u for u in (await session.scalars(select(User).where(User.id.in_(ids)))).all()}
    return CircleOut(
        caregivers=[
            to_out(lnk, people.get(lnk.caregiver_id)) for lnk in links if lnk.owner_id == user.id
        ],
        caring_for=[
            to_out(lnk, people.get(lnk.owner_id))
            for lnk in links
            if lnk.caregiver_id == user.id and lnk.status == "active"
        ],
    )


def invite_url(token: str) -> str:
    return f"{get_settings().frontend_url}/app/circle/accept/{token}"


async def invite(
    session: AsyncSession, user: User, data: InviteIn, request: Request | None = None
) -> tuple[CareLink, str]:
    email = data.email.lower()
    if email == user.email.lower():
        raise Unprocessable("That's your own email address.")
    existing = (
        await session.scalars(
            select(CareLink).where(CareLink.owner_id == user.id, CareLink.status != "revoked")
        )
    ).all()
    if len(existing) >= MAX_LINKS:
        raise Unprocessable(f"A care circle can have up to {MAX_LINKS} people.")
    for lnk in existing:
        if lnk.invite_email == email and link_status(lnk) in ("pending", "active"):
            raise Conflict("That person already has an invitation or access.")
    token = new_opaque_token(32)
    link = CareLink(
        owner_id=user.id,
        invite_email=email,
        role=data.role,
        status="pending",
        token_hash=sha256_hex(token),
        token_hint=token[-6:],
        expires_at=utcnow() + timedelta(days=INVITE_DAYS),
    )
    session.add(link)
    await session.flush()
    await audit.record(
        session,
        action="circle.invited",
        user_id=user.id,
        request=request,
        entity_type="care_link",
        entity_id=link.id,
        meta={"email": email, "role": data.role},
    )
    return link, token


async def _by_token(session: AsyncSession, token: str) -> CareLink:
    link = await session.scalar(select(CareLink).where(CareLink.token_hash == sha256_hex(token)))
    if link is None:
        raise NotFound("This invitation doesn't exist.")
    return link


async def preview(session: AsyncSession, user: User, token: str) -> InvitePreview:
    link = await _by_token(session, token)
    owner = await session.get(User, link.owner_id)
    return InvitePreview(
        owner_name=owner.display_name if owner else "Someone",
        role=link.role,
        email=link.invite_email,
        status=link_status(link),
        expires_at=link.expires_at,
    )


async def accept(
    session: AsyncSession, user: User, token: str, request: Request | None = None
) -> CareLink:
    link = await _by_token(session, token)
    state = link_status(link)
    if state == "expired":
        raise Gone("This invitation has expired. Ask for a new one.")
    if state != "pending":
        raise Gone("This invitation has already been used or withdrawn.")
    if link.owner_id == user.id:
        raise Unprocessable("You can't accept your own invitation.")
    if user.email.lower() != link.invite_email:
        raise Forbidden(
            f"This invitation is for {link.invite_email}. Sign in with that account to accept it."
        )
    link.caregiver_id = user.id
    link.status = "active"
    link.accepted_at = utcnow()
    link.token_hash = None  # one-time
    await session.flush()
    await audit.record(
        session,
        action="circle.accepted",
        user_id=link.owner_id,
        request=request,
        entity_type="care_link",
        entity_id=link.id,
        meta={"caregiver": user.display_name, "caregiver_id": str(user.id), "role": link.role},
    )
    return link


async def set_role(session: AsyncSession, user: User, link_id: uuid.UUID, role: str) -> CareLink:
    link = await session.scalar(
        select(CareLink).where(CareLink.id == link_id, CareLink.owner_id == user.id)
    )
    if link is None or link.status == "revoked":
        raise NotFound("Care circle member not found.")
    link.role = role
    await session.flush()
    return link


async def revoke(
    session: AsyncSession, user: User, link_id: uuid.UUID, request: Request | None = None
) -> None:
    """The owner removes someone, or a caregiver leaves."""
    link = await session.scalar(
        select(CareLink).where(
            CareLink.id == link_id,
            or_(CareLink.owner_id == user.id, CareLink.caregiver_id == user.id),
        )
    )
    if link is None or link.status == "revoked":
        raise NotFound("Care circle member not found.")
    link.status = "revoked"
    link.revoked_at = utcnow()
    link.token_hash = None
    await session.flush()
    await audit.record(
        session,
        action="circle.revoked",
        user_id=link.owner_id,
        request=request,
        entity_type="care_link",
        entity_id=link.id,
        meta={"by": "owner" if link.owner_id == user.id else "caregiver"},
    )
