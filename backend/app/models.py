"""Import every module's ORM models so `Base.metadata` is complete (Alembic, tests)."""

from app.modules.assistant.models import ChatMessage, ChatThread, DocumentChunk
from app.modules.audit.models import AuditLog
from app.modules.documents.models import Document, DocumentPage
from app.modules.extraction.models import Extraction
from app.modules.identity.models import RefreshToken, User
from app.modules.records.models import CareAction, Medication, Prescription

__all__ = [
    "AuditLog",
    "CareAction",
    "ChatMessage",
    "ChatThread",
    "Document",
    "DocumentChunk",
    "DocumentPage",
    "Extraction",
    "Medication",
    "Prescription",
    "RefreshToken",
    "User",
]
