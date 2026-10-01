from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin, TimestampMixin


class ShareLink(IdMixin, TimestampMixin, Base):
    """A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash is stored."""

    __tablename__ = "share_links"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    label: Mapped[str] = mapped_column(String(120))
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    token_hint: Mapped[str] = mapped_column(String(8))  # last chars, to tell links apart
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    max_views: Mapped[int | None] = mapped_column(Integer)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    last_viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    items: Mapped[list[ShareLinkItem]] = relationship(
        back_populates="link", cascade="all, delete-orphan", lazy="selectin"
    )


class ShareLinkItem(IdMixin, Base):
    __tablename__ = "share_link_items"

    share_link_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("share_links.id", ondelete="CASCADE"), index=True
    )
    item_type: Mapped[str] = mapped_column(String(16))  # document | prescription
    item_id: Mapped[uuid.UUID]

    link: Mapped[ShareLink] = relationship(back_populates="items")

    __table_args__ = (
        UniqueConstraint("share_link_id", "item_type", "item_id", name="uq_share_item"),
    )
