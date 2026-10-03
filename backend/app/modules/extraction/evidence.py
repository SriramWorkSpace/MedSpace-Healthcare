"""Where on the page each extracted value is printed (ADR-031).

Given the original file and an extraction payload, find each field's text in the PDF's text layer
and return boxes as fractions of the page (0..1), so they overlay the rendered page preview at
any size. Values are searched for literally, as they were read. Fields of one item (a medicine
line, a lab row) are anchored on the item's name: when a value like "500 mg" or "6.8" is printed
more than once, the occurrence closest to the anchor wins. Photos and scans have no text layer,
so they get no boxes (the UI says so) rather than guessed ones.
"""

from __future__ import annotations

import contextlib
import re
from dataclasses import dataclass, field
from datetime import date

import pymupdf

from app.modules.extraction.schemas import ExtractionPayload

VERSION = 1
PAD = 2.0  # points around each match, so the outline doesn't sit on the glyphs
_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]  # fmt: skip


@dataclass
class Spot:
    page: int
    boxes: list[list[float]] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"page": self.page, "boxes": self.boxes}


def _clean(text: str | None) -> str:
    return " ".join(str(text or "").split())


def _variants(text: str, *, min_words: int = 2) -> list[str]:
    """The value, then shorter word prefixes (a long note can wrap or end differently)."""
    text = _clean(text)
    out = [text] if text else []
    if ";" in text:  # readers join instructions with ";" where the page used ","
        out.append(text.replace("; ", ", "))
        out += [part.strip() for part in text.split(";") if part.strip()]
    if text.lower().startswith("dr. "):
        out.append(text[4:])
    words = text.split()
    for n in range(len(words) - 1, min_words - 1, -1):
        out.append(" ".join(words[:n]))
    return list(dict.fromkeys(v for v in out if len(v) >= 2))


def _date_variants(d: date | None) -> list[str]:
    if d is None:
        return []
    month = _MONTHS[d.month - 1]
    return [
        f"{month} {d.day}, {d.year}",
        f"{d.day} {month} {d.year}",
        f"{month[:3]} {d.day}, {d.year}",
        f"{d.day} {month[:3]} {d.year}",
        d.isoformat(),
        f"{d.day:02d}/{d.month:02d}/{d.year}",
        f"{d.month:02d}/{d.day:02d}/{d.year}",
        f"{d.day:02d}-{d.month:02d}-{d.year}",
    ]


class _Locator:
    def __init__(self, doc: pymupdf.Document) -> None:
        self.doc = doc

    def _pages(self, hint: int) -> list[int]:
        n = self.doc.page_count
        first = min(max(hint, 1), n)
        return [first, *[p for p in range(1, n + 1) if p != first]]

    def _norm(self, page_no: int, rects: list[pymupdf.Rect]) -> list[list[float]]:
        r = self.doc[page_no - 1].rect
        return [
            [
                round(max(0.0, (x.x0 - PAD) / r.width), 4),
                round(max(0.0, (x.y0 - PAD) / r.height), 4),
                round(min(1.0, (x.x1 + PAD) / r.width), 4),
                round(min(1.0, (x.y1 + PAD) / r.height), 4),
            ]
            for x in rects
        ]

    def find(
        self,
        variants: list[str],
        hint: int,
        near: tuple[int, float] | None = None,
    ) -> tuple[Spot, float] | None:
        """First variant found, preferring the hinted page (or the anchor's page and line).

        Returns the spot and the vertical centre of its first box, in points.
        """
        pages = [near[0]] if near else self._pages(hint)
        for page_no in pages:
            page = self.doc[page_no - 1]
            for text in variants:
                hits = page.search_for(text)
                if not hits:
                    continue
                if near:
                    # The occurrence on (or just below) the anchor's line.
                    i = min(
                        range(len(hits)),
                        key=lambda k: abs((hits[k].y0 + hits[k].y1) / 2 - near[1]),
                    )
                    if abs((hits[i].y0 + hits[i].y1) / 2 - near[1]) > 40:
                        continue
                else:
                    i = 0
                rects = [hits[i]]
                # A match that wraps comes back as consecutive rects, one per line.
                while i + 1 < len(hits) and 0 < hits[i + 1].y0 - rects[-1].y1 < 6:
                    i += 1
                    rects.append(hits[i])
                return Spot(page_no, self._norm(page_no, rects)), (rects[0].y0 + rects[0].y1) / 2
        return None


def locate(data: bytes, mime: str, payload: ExtractionPayload) -> dict:
    """Evidence for every field we can find: {"fields": {path: spot}, "items": {path: spot}}."""
    result: dict = {"version": VERSION, "available": False, "fields": {}, "items": {}}
    try:
        doc = pymupdf.open(stream=data, filetype="pdf" if mime == "application/pdf" else None)
    except Exception:
        return result
    with contextlib.closing(doc):
        if not any(page.get_text().strip() for page in doc):
            result["reason"] = "no_text"  # photos and scans: nothing to search
            return result
        result["available"] = True
        loc = _Locator(doc)
        fields: dict[str, dict] = result["fields"]
        items: dict[str, dict] = result["items"]

        def item(
            prefix: str, hint: int, parts: list[tuple[str, list[str]]], *, anchored: bool = True
        ) -> None:
            """parts: (field name, search variants). With `anchored`, the first field found is
            the anchor and the rest must sit on its line (a medicine line, a lab row)."""
            anchor: tuple[int, float] | None = None
            found: list[Spot] = []
            for name, variants in parts:
                if not variants:
                    continue
                hit = loc.find(variants, hint, anchor)
                if hit is None:
                    continue
                spot, y = hit
                if anchor is None and anchored:
                    anchor = (spot.page, y)
                key = f"{prefix}.{name}" if prefix else name
                fields.setdefault(key, spot.as_dict())
                found.append(spot)
            if found and prefix:
                page = found[0].page
                items[prefix] = {
                    "page": page,
                    "boxes": [b for s in found if s.page == page for b in s.boxes],
                }

        for i, m in enumerate(payload.medications):
            strength = _clean(m.strength)
            item(
                f"medications.{i}",
                m.source_page,
                [
                    ("name", _variants(f"{m.name} {strength}") + _variants(m.name, min_words=1)),
                    ("strength", _variants(strength, min_words=1)),
                    ("form", _variants(m.form, min_words=1)),
                    ("frequency_raw", _variants(m.frequency_raw, min_words=1)),
                    ("duration_days", _variants(m.duration_raw)),
                    ("instructions", _variants(m.instructions)),
                ],
            )

        for i, r in enumerate(payload.lab_results):
            value = _clean(r.value)
            unit = _clean(r.unit)
            item(
                f"lab_results.{i}",
                r.source_page,
                [
                    ("name", _variants(r.name, min_words=1)),
                    ("value", [v for v in (f"{value} {unit}".strip(), value) if v]),
                    ("unit", [unit] if unit else []),
                    ("ref_range", _variants(r.ref_range, min_words=1)),
                ],
            )

        for i, n in enumerate(payload.diet_notes):
            item(f"diet_notes.{i}", n.source_page, [("text", _variants(n.text))])

        for i, a in enumerate(payload.care_actions):
            # Titles are written by the reader ("Get CBC test"); the note is copied from the page.
            tokens = [t for t in re.findall(r"[A-Za-z0-9]+", a.title) if len(t) >= 3]
            tokens = [t for t in tokens if t.lower() not in {"get", "the", "visit", "test", "with"}]
            item(
                f"care_actions.{i}",
                a.source_page,
                [("title", _variants(a.title) + _variants(a.notes) + tokens)],
            )

        if payload.prescriber:
            p = payload.prescriber
            item(
                "prescriber",
                1,
                [
                    ("name", _variants(p.name, min_words=1)),
                    ("specialty", _variants(p.specialty, min_words=1)),
                    ("clinic", _variants(p.clinic)),
                ],
                anchored=False,  # a letterhead spans several lines
            )
        if payload.issued_on:
            item("", 1, [("issued_on", _date_variants(payload.issued_on))])
        if payload.follow_up and (payload.follow_up.notes or payload.follow_up.date):
            item(
                "",
                1,
                [
                    (
                        "follow_up.date",
                        _variants(payload.follow_up.notes) + _date_variants(payload.follow_up.date),
                    )
                ],
            )
    return result
