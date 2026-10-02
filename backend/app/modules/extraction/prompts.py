"""Prompts and the strict JSON schema for prescription extraction."""

from __future__ import annotations

from typing import Any

SYSTEM_PROMPT = """You are a careful medical-document transcription engine for MedSpace.
You convert prescriptions and medical documents into structured JSON.

Rules:
- Transcribe ONLY what is written. Never infer diagnoses, never suggest treatments, never \
invent doses, never "correct" a prescriber.
- Copy frequency and duration text VERBATIM into frequency_raw and duration_raw (e.g. "1-0-1", \
"BD", "TDS x 5/7", "SOS"). Do not convert them to clock times.
- Set as_needed true only when the document says SOS, PRN, as needed or equivalent.
- source_page is the 1-based page where the item appears.
- confidence is 0-1 for how legible and unambiguous the item is. List the names of any \
fields you are unsure about in uncertain_fields.
- Dates use ISO format YYYY-MM-DD. If a follow-up is relative ("review in 2 weeks") and the \
issue date is known, compute the date; otherwise put the text in follow_up.notes.
- care_actions are one-off things the patient must do that are written on the document: lab \
tests, follow-up visits, reports to bring. Do not invent any.
- diet_notes are diet, food or drink instructions written on the document (e.g. "low-salt \
diet", "avoid alcohol while on antibiotics"). Copy the wording. category is one of avoid, \
limit, include, timing or general. Never add nutrition advice of your own. Instructions that \
belong to a single medicine ("after food") stay in that medicine's instructions.
- summary: one or two neutral sentences describing what the document contains. No advice.
- Use null for anything not present. Output JSON only."""


def _nullable(t: str) -> dict[str, Any]:
    return {"type": [t, "null"]}


_MED = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "strength": _nullable("string"),
        "form": _nullable("string"),
        "dose": _nullable("string"),
        "route": _nullable("string"),
        "frequency_raw": _nullable("string"),
        "duration_raw": _nullable("string"),
        "duration_days": _nullable("integer"),
        "instructions": _nullable("string"),
        "as_needed": {"type": "boolean"},
        "source_page": {"type": "integer"},
        "confidence": {"type": "number"},
        "uncertain_fields": {"type": "array", "items": {"type": "string"}},
    },
}
_MED["required"] = list(_MED["properties"])

_ACTION = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "kind": {
            "type": "string",
            "enum": [
                "lab_test",
                "follow_up",
                "course_completion",
                "upload_report",
                "prepare_documents",
                "other",
            ],
        },
        "title": {"type": "string"},
        "due_on": _nullable("string"),
        "notes": _nullable("string"),
        "source_page": {"type": "integer"},
        "confidence": {"type": "number"},
    },
}
_ACTION["required"] = list(_ACTION["properties"])

_DIET = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "text": {"type": "string"},
        "category": {"type": "string", "enum": ["avoid", "limit", "include", "timing", "general"]},
        "source_page": {"type": "integer"},
        "confidence": {"type": "number"},
    },
}
_DIET["required"] = list(_DIET["properties"])

_PRESCRIBER = {
    "type": ["object", "null"],
    "additionalProperties": False,
    "properties": {
        "name": _nullable("string"),
        "specialty": _nullable("string"),
        "clinic": _nullable("string"),
        "contact": _nullable("string"),
    },
    "required": ["name", "specialty", "clinic", "contact"],
}

_FOLLOW_UP = {
    "type": ["object", "null"],
    "additionalProperties": False,
    "properties": {"date": _nullable("string"), "notes": _nullable("string")},
    "required": ["date", "notes"],
}

EXTRACTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "document_type": {"type": "string", "enum": ["prescription", "lab_report", "other"]},
        "prescriber": _PRESCRIBER,
        "patient_name": _nullable("string"),
        "issued_on": _nullable("string"),
        "follow_up": _FOLLOW_UP,
        "medications": {"type": "array", "items": _MED},
        "care_actions": {"type": "array", "items": _ACTION},
        "diet_notes": {"type": "array", "items": _DIET},
        "summary": _nullable("string"),
        "overall_confidence": {"type": "number"},
    },
}
EXTRACTION_SCHEMA["required"] = list(EXTRACTION_SCHEMA["properties"])

JSON_SHAPE_HINT = (
    "Return a JSON object with keys: document_type, prescriber{name,specialty,clinic,contact}, "
    "patient_name, issued_on, follow_up{date,notes}, medications[{name,strength,form,dose,route,"
    "frequency_raw,duration_raw,duration_days,instructions,as_needed,source_page,confidence,"
    "uncertain_fields[]}], care_actions[{kind,title,due_on,notes,source_page,confidence}], "
    "diet_notes[{text,category,source_page,confidence}], "
    "summary, overall_confidence."
)


def text_user_prompt(pages: list[str]) -> str:
    body = "\n\n".join(f"=== PAGE {i} ===\n{text}" for i, text in enumerate(pages, start=1))
    return f"Extract the structured data from this document.\n\n{body}"


def vision_user_prompt(first_page: int, count: int) -> str:
    last = first_page + count - 1
    pages = f"page {first_page}" if count == 1 else f"pages {first_page}-{last}"
    return (
        f"These images are {pages} of a medical document (in order). Extract the structured "
        f"data. Use the real page numbers for source_page. {JSON_SHAPE_HINT}"
    )


def repair_prompt(errors: str) -> str:
    return (
        "Your previous JSON did not validate. Fix ONLY these problems and return the full "
        f"corrected JSON object:\n{errors}"
    )
