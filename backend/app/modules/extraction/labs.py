"""Deterministic handling of lab results (ADR-020).

Values and reference ranges are copied from the report. This module only parses them so results
can be charted, and flags a value against the range *printed on that report*. It never supplies
a range of its own and never says what a result means.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

LabFlag = Literal["low", "high", "normal"]

_NUMBER = r"\d{1,6}(?:,\d{3})*(?:\.\d+)?|\.\d+"
_PLAIN_VALUE = re.compile(rf"^\s*({_NUMBER})\s*$")
_BETWEEN = re.compile(rf"^\s*({_NUMBER})\s*(?:-|–|—|to)\s*({_NUMBER})\b")  # noqa: RUF001
_BOUND = re.compile(rf"^\s*(<=|>=|≤|≥|<|>|up to|below|under|above|over)\s*({_NUMBER})\b", re.I)
_PRINTED_FLAG = re.compile(r"^(h|l|high|low|hi|lo)\*?$", re.IGNORECASE)

# Common spellings of the same test, so results from different labs line up on one chart.
_SYNONYMS = {
    "cholesterol total": "total cholesterol",
    "cholesterol": "total cholesterol",
    "total chol": "total cholesterol",
    "ldl": "ldl cholesterol",
    "ldl-c": "ldl cholesterol",
    "ldl c": "ldl cholesterol",
    "ldl cholesterol calculated": "ldl cholesterol",
    "hdl": "hdl cholesterol",
    "hdl-c": "hdl cholesterol",
    "hdl c": "hdl cholesterol",
    "tg": "triglycerides",
    "triglyceride": "triglycerides",
    "a1c": "hba1c",
    "hemoglobin a1c": "hba1c",
    "haemoglobin a1c": "hba1c",
    "glycated hemoglobin": "hba1c",
    "glycated haemoglobin": "hba1c",
    "glycosylated hemoglobin": "hba1c",
    "fbs": "fasting glucose",
    "fasting blood sugar": "fasting glucose",
    "fasting blood glucose": "fasting glucose",
    "fasting plasma glucose": "fasting glucose",
    "glucose fasting": "fasting glucose",
    "hb": "hemoglobin",
    "hgb": "hemoglobin",
    "haemoglobin": "hemoglobin",
    "thyroid stimulating hormone": "tsh",
    "25-oh vitamin d": "vitamin d",
    "25 oh vitamin d": "vitamin d",
    "vitamin d 25-oh": "vitamin d",
    "vitamin d3": "vitamin d",
    "serum creatinine": "creatinine",
}


def parse_value(text: str | None) -> float | None:
    """'212' -> 212.0, '4,500' -> 4500.0. Qualitative or bounded values ('<0.5', 'Negative')
    return None: they are kept as text but not charted."""
    if not text:
        return None
    m = _PLAIN_VALUE.match(text)
    return float(m.group(1).replace(",", "")) if m else None


@dataclass(frozen=True, slots=True)
class RefRange:
    low: float | None = None
    high: float | None = None
    low_inclusive: bool = True  # is the low bound itself inside the range?
    high_inclusive: bool = True


def parse_range(text: str | None) -> RefRange | None:
    """Parse a printed reference range: '70 - 99', '< 200', '>= 40', 'up to 5.6'."""
    if not text:
        return None
    t = text.strip().strip("()").strip()
    if m := _BETWEEN.match(t):
        low, high = (float(g.replace(",", "")) for g in m.groups())
        return RefRange(low=min(low, high), high=max(low, high))
    if m := _BOUND.match(t):
        op, num = m.group(1).lower(), float(m.group(2).replace(",", ""))
        if op in ("<", "below", "under"):
            return RefRange(high=num, high_inclusive=False)
        if op in ("<=", "≤", "up to"):
            return RefRange(high=num)
        if op in (">", "above", "over"):
            return RefRange(low=num, low_inclusive=False)
        return RefRange(low=num)
    return None


def flag_against(value: float | None, ref: RefRange | None) -> LabFlag | None:
    if value is None or ref is None:
        return None
    if ref.low is not None and (value < ref.low or (value == ref.low and not ref.low_inclusive)):
        return "low"
    if ref.high is not None and (
        value > ref.high or (value == ref.high and not ref.high_inclusive)
    ):
        return "high"
    return "normal"


def printed_flag(text: str | None) -> LabFlag | None:
    """'H' / 'High' / 'L*' printed next to a value on the report."""
    if not text or not (m := _PRINTED_FLAG.match(text.strip())):
        return None
    return "high" if m.group(1).lower().startswith("h") else "low"


def resolve_flag(value_text: str, ref_range: str | None, printed: LabFlag | None) -> LabFlag | None:
    """The printed range wins when it parses (it stays correct if the value is edited in review);
    otherwise keep a flag the report printed itself."""
    computed = flag_against(parse_value(value_text), parse_range(ref_range))
    return computed or printed


def analyte_key(name: str) -> str:
    """URL-safe key that groups the same test across reports: 'LDL-C' -> 'ldl-cholesterol'."""
    n = re.sub(r"\(.*?\)", " ", name.lower())
    n = re.sub(r"[,:;*]", " ", n)
    n = " ".join(n.split())
    if n not in _SYNONYMS and len(n.split()) > 1:
        n = " ".join(re.sub(r"\b(serum|plasma|level|levels)\b", " ", n).split())
    n = _SYNONYMS.get(n, n)
    slug = re.sub(r"[^a-z0-9]+", "-", n).strip("-")
    return slug[:80] or "result"
