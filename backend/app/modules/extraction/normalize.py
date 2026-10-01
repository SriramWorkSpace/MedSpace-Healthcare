"""Deterministic normalization of prescription shorthand (ADR-006).

The LLM copies frequency and duration text verbatim; this module turns it into clock times and
day counts using the user's preferred dose times. Anything ambiguous is flagged, never guessed.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

DEFAULT_DOSE_TIMES = {
    "morning": "08:00",
    "afternoon": "14:00",
    "evening": "20:00",
    "bedtime": "22:00",
}

SLOT_ORDER = ("morning", "afternoon", "evening", "bedtime")


@dataclass(slots=True)
class Schedule:
    times: list[str] = field(default_factory=list)
    period: str = "daily"  # daily | weekly | alternate_days | interval | once | as_needed | unknown
    as_needed: bool = False
    interval_hours: int | None = None
    label: str = ""
    needs_attention: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def _clean(text: str) -> str:
    text = text.lower().replace("½", "0.5").replace("¼", "0.25")
    text = re.sub(r"(?<=[a-z])\.(?=[a-z])", "", text)  # b.i.d. -> bid.
    text = re.sub(r"(?<!\d)\.|\.(?!\d)|[,;]", " ", text)  # keep decimals like 0.5
    return re.sub(r"\s+", " ", text).strip()


def _times_for(slots: list[str], dose_times: dict[str, str]) -> list[str]:
    merged = {**DEFAULT_DOSE_TIMES, **(dose_times or {})}
    return sorted({merged[s] for s in slots})


def _hm_to_min(hm: str) -> int:
    h, m = hm.split(":")
    return int(h) * 60 + int(m)


def _min_to_hm(minutes: int) -> str:
    minutes %= 24 * 60
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


_PRN = re.compile(
    r"\b(prn|sos|as needed|as required|when needed|when required|if needed|if required)\b"
)
_SLOT_PATTERN = re.compile(
    r"(?<![\d/])(\d(?:\.\d+)?)\s*-\s*(\d(?:\.\d+)?)\s*-\s*(\d(?:\.\d+)?)(?:\s*-\s*(\d(?:\.\d+)?))?(?![\d/])"
)
_INTERVAL = re.compile(
    r"\b(?:q\s*(\d{1,2})\s*h(?:rs?|ours?)?|every\s+(\d{1,2})\s*(?:h|hrs?|hours?))\b"
)

_RULES: list[tuple[re.Pattern, list[str], str]] = [
    (
        re.compile(
            r"\b(qid|qds|four times(?: a| per)? day|4 times(?: a| per)? day|4x(?: daily| a day)?)\b"
        ),
        ["morning", "afternoon", "evening", "bedtime"],
        "Four times daily",
    ),
    (
        re.compile(
            r"\b(tds|tid|thrice daily|three times(?: a| per)? day|3 times(?: a| per)? day|3x(?: daily| a day)?)\b"
        ),
        ["morning", "afternoon", "evening"],
        "Three times daily",
    ),
    (
        re.compile(
            r"\b(bd|bid|twice daily|twice a day|two times(?: a| per)? day|2 times(?: a| per)? day|2x(?: daily| a day)?|morning and (?:evening|night))\b"
        ),
        ["morning", "evening"],
        "Twice daily",
    ),
    (
        re.compile(
            r"\b(hs|qhs|nocte|at bedtime|at night|before bed|bedtime|every night|nightly)\b"
        ),
        ["bedtime"],
        "Once daily at bedtime",
    ),
    (
        re.compile(r"\b(every evening|in the evening|once daily in the evening)\b"),
        ["evening"],
        "Once daily in the evening",
    ),
    (
        re.compile(
            r"\b(od|qd|qam|once daily|once a day|daily|every day|every morning|in the morning|1x daily|once)\b"
        ),
        ["morning"],
        "Once daily",
    ),
]


def normalize_frequency(raw: str | None, dose_times: dict[str, str] | None = None) -> Schedule:
    if not raw or not raw.strip():
        return Schedule(period="unknown", label="Frequency missing", needs_attention=True)
    text = _clean(raw)

    if _PRN.search(text):
        return Schedule(period="as_needed", as_needed=True, label="As needed")

    if re.search(r"\bstat\b|\bsingle dose\b|\bone time\b", text):
        return Schedule(
            times=_times_for(["morning"], dose_times), period="once", label="Single dose"
        )

    if re.search(r"\b(alternate days?|every other day|eod|qod)\b", text):
        return Schedule(
            times=_times_for(["morning"], dose_times),
            period="alternate_days",
            label="Every other day",
        )

    if re.search(r"\b(weekly|once a week|every week|once weekly)\b", text):
        return Schedule(
            times=_times_for(["morning"], dose_times), period="weekly", label="Once a week"
        )

    m = _SLOT_PATTERN.search(text)
    if m:
        values = [v for v in m.groups() if v is not None]
        slots = ("morning", "afternoon", "evening") if len(values) == 3 else SLOT_ORDER
        chosen = [slot for slot, v in zip(slots, values, strict=False) if float(v) > 0]
        if not chosen:
            return Schedule(period="unknown", label=raw.strip(), needs_attention=True)
        labels = {1: "Once daily", 2: "Twice daily", 3: "Three times daily", 4: "Four times daily"}
        return Schedule(times=_times_for(chosen, dose_times), label=labels[len(chosen)])

    m = _INTERVAL.search(text)
    if m:
        hours = int(m.group(1) or m.group(2))
        if hours <= 0 or (24 % hours != 0 and hours not in (36, 48, 72)):
            return Schedule(
                period="interval",
                interval_hours=hours,
                label=f"Every {hours} hours",
                needs_attention=True,
            )
        start = _hm_to_min({**DEFAULT_DOSE_TIMES, **(dose_times or {})}["morning"])
        times = sorted({_min_to_hm(start + i * hours * 60) for i in range(max(1, 24 // hours))})
        return Schedule(
            times=times, period="interval", interval_hours=hours, label=f"Every {hours} hours"
        )

    for pattern, slots, label in _RULES:
        if pattern.search(text):
            return Schedule(times=_times_for(slots, dose_times), label=label)

    return Schedule(period="unknown", label=raw.strip(), needs_attention=True)


_DUR_SLASH = re.compile(r"(?<!\d)(\d{1,3})\s*/\s*(7|52|12)(?!\d)")
_DUR_WORDS = re.compile(r"(?:x|for|\*|×)?\s*(\d{1,3})\s*(d|days?|wks?|weeks?|w|mo|months?|m)\b")


def parse_duration_days(raw: str | None) -> int | None:
    """'x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown -> None."""
    if not raw:
        return None
    text = _clean(raw)
    if re.search(
        r"\b(ongoing|continue|long term|indefinitely|until further notice|chronic)\b", text
    ):
        return None
    m = _DUR_SLASH.search(text)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        return n * {"7": 1, "52": 7, "12": 30}[unit]
    m = _DUR_WORDS.search(text)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        if unit.startswith("d"):
            return n
        if unit.startswith("w"):
            return n * 7
        if unit.startswith("m"):
            return n * 30
    return None
