"""Offline, rule-based extractor used when no LLM is configured (CI, demo, keyless clones).

It understands typical typed prescriptions (one medication per line with a strength), which
covers the synthetic samples. Real-world messy documents are what the Groq path is for.
"""

from __future__ import annotations

import re
from datetime import date, timedelta

from dateutil import parser as dateparser

from app.modules.extraction.normalize import normalize_frequency, parse_duration_days
from app.modules.extraction.schemas import (
    ExtractedCareAction,
    ExtractedMedication,
    ExtractionPayload,
    FollowUp,
    Prescriber,
)

_STRENGTH = (
    r"\d+(?:\.\d+)?\s?(?:mg|mcg|µg|g|ml|mL|IU|units?|%)(?:\s?/\s?\d+(?:\.\d+)?\s?(?:mg|ml|mL))?"
)
_FORM_PREFIX = r"(?:(?:tab|tabs|tablet|cap|caps|capsule|syp|syrup|inj|injection|oint|ointment|drops?|susp)\.?\s+)?"
_MED_LINE = re.compile(
    rf"^\s*(?:\d+[.)]\s*|[-•*]\s*|rx[:\s]+)?{_FORM_PREFIX}"
    rf"(?P<name>[A-Za-z][A-Za-z\-]+(?:\s[A-Z][A-Za-z\-]+)?)\s+(?P<strength>{_STRENGTH})(?P<rest>.*)$",
    re.IGNORECASE,
)
_FORM_WORDS = {
    "tab": "tablet",
    "tablet": "tablet",
    "cap": "capsule",
    "capsule": "capsule",
    "syrup": "syrup",
    "syp": "syrup",
    "inj": "injection",
    "drops": "drops",
    "ointment": "ointment",
    "cream": "cream",
    "inhaler": "inhaler",
    "suspension": "suspension",
    "gel": "gel",
    "lotion": "lotion",
    "spray": "spray",
    "patch": "patch",
    "solution": "solution",
}
_INSTRUCTION_RE = re.compile(
    r"(after (?:food|meals?|breakfast|dinner|lunch)|before (?:food|meals?|breakfast|bed|sleep)|"
    r"with (?:food|meals?|water|milk)|on an empty stomach|empty stomach|avoid [a-z ]+|"
    r"do not [a-z ]+|p\.?c\.?|a\.?c\.?)",
    re.IGNORECASE,
)
_FREQ_RE = re.compile(
    r"(\d(?:\.\d+)?\s*-\s*\d(?:\.\d+)?\s*-\s*\d(?:\.\d+)?(?:\s*-\s*\d(?:\.\d+)?)?|"
    r"\b(?:sos|prn|stat|od|qd|bd|bid|tds|tid|qid|qds|hs|qhs|nocte)\b(?:,?\s*max\s+\w+)?|"
    r"q\s*\d{1,2}\s*h|every \d{1,2} hours?|once (?:daily|a day|a week|weekly)|twice (?:daily|a day)|"
    r"(?:three|four|two) times (?:a|per) day|at (?:night|bedtime)|as needed|when required|"
    r"alternate days|every other day|weekly|daily)",
    re.IGNORECASE,
)
_DUR_RE = re.compile(
    r"((?:x|for|×)\s*\d{1,3}\s*(?:days?|d|weeks?|wks?|months?)\b|\d{1,3}\s*/\s*(?:7|52|12)\b|"
    r"\d{1,3}\s*(?:days?|weeks?|months?)\b|ongoing|continue)",
    re.IGNORECASE,
)
_DATE_LINE = re.compile(r"\b(?:date|dated|issued)\s*[:\-]?\s*(?P<d>[^\n]+)", re.IGNORECASE)
_FOLLOW_UP = re.compile(
    r"\b(?:follow[\s-]?up|review|next visit)\b[:\s\-]*(?P<rest>[^\n]*)", re.IGNORECASE
)
_DOCTOR = re.compile(r"\bDr\.?\s+(?P<name>[A-Z][A-Za-z.'\-]+(?:\s+[A-Z][A-Za-z.'\-]+){0,3})")
_CLINIC = re.compile(
    r"(clinic|hospital|medical|health|centre|center|practice|surgery|urgent care|care|"
    r"diagnostics|associates|institute|wellness|pharmacy)",
    re.IGNORECASE,
)
_LAB = re.compile(
    r"\b(cbc|complete blood count|lipid (?:panel|profile)|hba1c|blood (?:test|work|sugar)|"
    r"x-?ray|ultrasound|ecg|ekg|urine (?:test|analysis)|thyroid|tsh|vitamin d|lft|kft|"
    r"liver function|kidney function|mri|ct scan)\b",
    re.IGNORECASE,
)
_RELATIVE = re.compile(r"\b(?:in|after)\s+(\d{1,2})\s*(day|week|month)s?\b", re.IGNORECASE)
_SPECIALTY_HINT = re.compile(
    r"(internal medicine|family medicine|general practi\w+|cardiology|dermatology|pediatrics|"
    r"paediatrics|endocrinology|orthopedics|ent|psychiatry|neurology|gastroenterology|"
    r"pulmonology|gynecology|obstetrics)",
    re.IGNORECASE,
)


def _parse_date(text: str) -> date | None:
    text = text.strip().strip(".")
    if not text:
        return None
    try:
        return dateparser.parse(text, fuzzy=True, dayfirst=False).date()
    except (ValueError, OverflowError):
        return None


def _medication_from_line(line: str, page_no: int) -> ExtractedMedication | None:
    m = _MED_LINE.match(line)
    if not m:
        return None
    name = m.group("name").strip()
    if name.lower() in {"date", "patient", "age", "weight", "dr", "page", "follow", "review"}:
        return None
    rest = m.group("rest")
    freq = _FREQ_RE.search(rest)
    dur = _DUR_RE.search(rest)
    instr = _INSTRUCTION_RE.findall(rest)
    form = next(
        (v for k, v in _FORM_WORDS.items() if re.search(rf"\b{k}\b", line, re.IGNORECASE)), None
    )
    frequency_raw = freq.group(0).strip() if freq else None
    duration_raw = dur.group(0).strip() if dur else None
    uncertain = [f for f, v in (("frequency_raw", frequency_raw),) if not v]
    instructions = "; ".join(dict.fromkeys(i.strip() for i in instr)) or None
    if instructions:
        instructions = instructions.replace("p.c.", "after food").replace("a.c.", "before food")
    as_needed = normalize_frequency(frequency_raw).as_needed if frequency_raw else False
    return ExtractedMedication(
        name=name[:1].upper() + name[1:],
        strength=re.sub(r"\s+", " ", m.group("strength")).strip(),
        form=form,
        frequency_raw=frequency_raw,
        duration_raw=duration_raw,
        duration_days=parse_duration_days(duration_raw),
        instructions=instructions,
        as_needed=as_needed,
        source_page=page_no,
        confidence=0.9 if not uncertain else 0.62,
        uncertain_fields=uncertain,
    )


def extract(pages: list[str]) -> ExtractionPayload:
    meds: list[ExtractedMedication] = []
    actions: list[ExtractedCareAction] = []
    prescriber = Prescriber()
    issued_on: date | None = None
    follow_up: FollowUp | None = None
    patient: str | None = None
    lab_lines_seen: set[str] = set()

    for page_no, text in enumerate(pages, start=1):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for idx, line in enumerate(lines):
            if prescriber.clinic is None and idx < 6 and _CLINIC.search(line) and "Dr" not in line:
                prescriber.clinic = line[:120]
            if prescriber.name is None and (d := _DOCTOR.search(line)):
                prescriber.name = "Dr. " + d.group("name").strip().rstrip(",")
                if s := _SPECIALTY_HINT.search(line):
                    prescriber.specialty = s.group(1).title()
                continue
            if patient is None and line.lower().startswith("patient"):
                patient = line.split(":", 1)[-1].strip() or None
                continue
            if issued_on is None and (dm := _DATE_LINE.search(line)):
                issued_on = _parse_date(dm.group("d"))
                continue
            if fm := _FOLLOW_UP.match(line):
                rest = fm.group("rest").strip()
                fu_date = None
                if rel := _RELATIVE.search(rest):
                    n, unit = int(rel.group(1)), rel.group(2).lower()
                    if issued_on:
                        fu_date = issued_on + timedelta(
                            days=n * {"day": 1, "week": 7, "month": 30}[unit]
                        )
                else:
                    fu_date = _parse_date(rest) if re.search(r"\d", rest) else None
                follow_up = FollowUp(date=fu_date, notes=rest or None)
                actions.append(
                    ExtractedCareAction(
                        kind="follow_up",
                        title=f"Follow-up visit{f' with {prescriber.name}' if prescriber.name else ''}",
                        due_on=fu_date,
                        notes=rest or None,
                        source_page=page_no,
                        confidence=0.85 if fu_date else 0.6,
                    )
                )
                # A follow-up line can also mention tests ("Review in 2 weeks with CBC").
            labs = [] if _MED_LINE.match(line) else list(_LAB.finditer(line))
            for lab in labs:
                label = lab.group(1)
                key = label.lower()
                if key in lab_lines_seen:
                    continue
                lab_lines_seen.add(key)
                pretty = label if any(c.isupper() for c in label) else label[:1].upper() + label[1:]
                actions.append(
                    ExtractedCareAction(
                        kind="lab_test",
                        title=f"Get {pretty} test" if "test" not in key else f"Get {pretty}",
                        due_on=follow_up.date if follow_up else None,
                        notes=line[:200],
                        source_page=page_no,
                        confidence=0.8,
                    )
                )
            if labs:
                continue
            if med := _medication_from_line(line, page_no):
                meds.append(med)

    has_meds = bool(meds)
    summary = None
    if prescriber.name or prescriber.clinic or has_meds:
        who = prescriber.name or prescriber.clinic or "the prescriber"
        when = f" dated {issued_on:%B} {issued_on.day}, {issued_on.year}" if issued_on else ""
        listing = (
            f", listing {len(meds)} medication{'s' if len(meds) != 1 else ''}" if has_meds else ""
        )
        follow = " and a follow-up visit" if follow_up else ""
        summary = f"Prescription from {who}{when}{listing}{follow}."

    confidences = [m.confidence for m in meds] or [0.5]
    doc_type = "prescription" if has_meds else ("lab_report" if lab_lines_seen else "other")
    return ExtractionPayload(
        document_type=doc_type,
        prescriber=prescriber if any(prescriber.model_dump().values()) else None,
        patient_name=patient,
        issued_on=issued_on,
        follow_up=follow_up,
        medications=meds,
        care_actions=actions,
        summary=summary,
        overall_confidence=round(sum(confidences) / len(confidences), 2),
    )
