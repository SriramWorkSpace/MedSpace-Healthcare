"""Visit prep: a brief the user builds before an appointment (ADR-022)."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class VisitPrep(IdMixin, TimestampMixin, Base):
    """The user's own part of a visit brief: when, with whom, and what they want to ask.

    Everything else in the brief (medicines, labs, doses, to-dos) is read live from records, so
    the brief is always current until the visit happens.
    """

    __tablename__ = "visit_preps"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(120))
    visit_date: Mapped[date | None] = mapped_column(Date, index=True)
    clinician: Mapped[str | None] = mapped_column(String(120))
    since: Mapped[date | None] = mapped_column(Date)  # "changes since"; derived when empty
    # [{"id": str, "text": str, "done": bool, "prompt_key": str | None}]
    questions: Mapped[list] = mapped_column(JSONB, default=list)
