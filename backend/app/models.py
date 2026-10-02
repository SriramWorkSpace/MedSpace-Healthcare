"""Import every module's ORM models so `Base.metadata` is complete (Alembic, tests)."""

from app.modules.assistant.models import ChatMessage, ChatThread, DocumentChunk
from app.modules.audit.models import AuditLog
from app.modules.documents.models import Document, DocumentPage
from app.modules.doses.models import DoseLog
from app.modules.extraction.models import Extraction
from app.modules.identity.models import RefreshToken, User
from app.modules.integrations.models import OAuthConnection, SyncLink
from app.modules.records.models import (
    CareAction,
    DietNote,
    LabResult,
    Medication,
    Prescription,
)
from app.modules.sharing.models import ShareLink, ShareLinkItem
from app.modules.visits.models import VisitPrep

__all__ = [
    "AuditLog",
    "CareAction",
    "ChatMessage",
    "ChatThread",
    "DietNote",
    "Document",
    "DocumentChunk",
    "DocumentPage",
    "DoseLog",
    "Extraction",
    "LabResult",
    "Medication",
    "OAuthConnection",
    "Prescription",
    "RefreshToken",
    "ShareLink",
    "ShareLinkItem",
    "SyncLink",
    "User",
    "VisitPrep",
]
