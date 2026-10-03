"""Import every module's ORM models so `Base.metadata` is complete (Alembic, tests)."""

from app.modules.assistant.models import ChatMessage, ChatThread, DocumentChunk
from app.modules.audit.models import AuditLog
from app.modules.circle.models import CareLink
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
from app.modules.reminders.models import PushSubscription, ReminderLog, ReminderSettings
from app.modules.sharing.models import ShareLink, ShareLinkItem
from app.modules.supply.models import MedicationSupply
from app.modules.visits.models import VisitPrep

__all__ = [
    "AuditLog",
    "CareAction",
    "CareLink",
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
    "MedicationSupply",
    "OAuthConnection",
    "Prescription",
    "PushSubscription",
    "RefreshToken",
    "ReminderLog",
    "ReminderSettings",
    "ShareLink",
    "ShareLinkItem",
    "SyncLink",
    "User",
    "VisitPrep",
]
