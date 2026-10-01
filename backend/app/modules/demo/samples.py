"""Synthetic prescriptions rendered as real PDFs (and one scan-style PNG).

Every clinic, prescriber and patient here is fictional. Dates are relative to "today" so demo
accounts always look current. Run `python -m app.modules.demo.samples ../samples` to write the
files used for manual upload testing.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

import pymupdf

INK = (0.12, 0.16, 0.15)
MUTED = (0.42, 0.47, 0.45)
ACCENT = (0.12, 0.48, 0.36)


@dataclass(frozen=True)
class Scenario:
    slug: str
    clinic: str
    address: str
    doctor: str
    specialty: str
    days_ago: int
    patient: str
    lines: list[str]
    notes: list[str] = field(default_factory=list)
    title: str = "Prescription"
    kind: str = "prescription"


SCENARIOS: list[Scenario] = [
    Scenario(
        slug="riverside-acute",
        clinic="Riverside Family Clinic",
        address="214 Alder Street, Portland, OR 97205  |  (503) 555-0142",
        doctor="Dr. Imani Oduya, MD",
        specialty="Internal Medicine",
        days_ago=3,
        patient="Avery Lindqvist, 34 F",
        lines=[
            "1. Amoxicillin 500 mg capsule - 1-0-1 x 7 days - after food",
            "2. Ibuprofen 400 mg tablet - SOS, max TDS - after food",
            "3. Cetirizine 10 mg tablet - HS x 5 days",
        ],
        notes=["Follow-up: Review in 2 weeks", "Investigations: CBC before next visit"],
    ),
    Scenario(
        slug="northgate-diabetes",
        clinic="Northgate Diabetes & Endocrine Centre",
        address="88 Kestrel Avenue, Suite 300, Denver, CO 80203  |  (720) 555-0187",
        doctor="Dr. Tomas Varga, MD",
        specialty="Endocrinology",
        days_ago=41,
        patient="Avery Lindqvist, 34 F",
        lines=[
            "1. Metformin 500 mg tablet - BD x 90 days - after meals",
            "2. Atorvastatin 20 mg tablet - HS x 90 days",
            "3. Cholecalciferol 60000 IU capsule - once a week x 8 weeks - with milk",
        ],
        notes=[
            "Follow-up: Review in 3 months",
            "Investigations: HbA1c and lipid panel before next visit",
        ],
    ),
    Scenario(
        slug="harbor-derm",
        clinic="Harbor Dermatology Practice",
        address="5 Wharf Lane, Seattle, WA 98101  |  (206) 555-0119",
        doctor="Dr. Lena Moreau, MD",
        specialty="Dermatology",
        days_ago=118,
        patient="Avery Lindqvist, 34 F",
        lines=[
            "1. Doxycycline 100 mg capsule - OD x 6 weeks - after food, with water",
            "2. Clindamycin 1% gel - at night x 8 weeks",
        ],
        notes=["Follow-up: Review in 6 weeks"],
    ),
]


def issued(s: Scenario, today: date | None = None) -> date:
    return (today or date.today()) - timedelta(days=s.days_ago)


def build_pdf(s: Scenario, today: date | None = None) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    x = 56
    page.draw_rect(pymupdf.Rect(0, 0, 595, 8), color=None, fill=ACCENT)
    page.insert_text((x, 64), s.clinic, fontname="hebo", fontsize=17, color=INK)
    page.insert_text((x, 82), s.address, fontname="helv", fontsize=9, color=MUTED)
    page.insert_text(
        (x, 112), f"{s.doctor} · {s.specialty}", fontname="hebo", fontsize=11, color=INK
    )
    page.draw_line((x, 126), (539, 126), color=(0.85, 0.88, 0.86), width=0.8)

    d = issued(s, today)
    page.insert_text((x, 150), f"Patient: {s.patient}", fontname="helv", fontsize=10, color=INK)
    page.insert_text(
        (360, 150), f"Date: {d:%B} {d.day}, {d.year}", fontname="helv", fontsize=10, color=INK
    )

    page.insert_text((x, 196), "Rx", fontname="tibo", fontsize=26, color=ACCENT)
    y = 232
    for line in s.lines:
        page.insert_text((x + 8, y), line, fontname="cour", fontsize=11, color=INK)
        y += 24

    y += 16
    for note in s.notes:
        page.insert_text((x, y), note, fontname="helv", fontsize=10.5, color=INK)
        y += 20

    page.draw_line((360, 700), (539, 700), color=MUTED, width=0.6)
    page.insert_text((360, 716), s.doctor, fontname="helv", fontsize=9, color=MUTED)
    page.insert_text(
        (x, 800),
        "SYNTHETIC SAMPLE FOR THE MEDSPACE DEMO. NOT A REAL PRESCRIPTION.",
        fontname="helv",
        fontsize=7.5,
        color=MUTED,
    )
    data = doc.tobytes(deflate=True)
    doc.close()
    return data


def build_scan_png(s: Scenario, today: date | None = None) -> bytes:
    """A 'photo' of the prescription: rasterized, so it has no text layer."""
    with pymupdf.open(stream=build_pdf(s, today), filetype="pdf") as doc:
        return doc[0].get_pixmap(dpi=110).tobytes("png")


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "samples")
    out.mkdir(parents=True, exist_ok=True)
    for sc in SCENARIOS:
        (out / f"rx-{sc.slug}.pdf").write_bytes(build_pdf(sc))
    (out / f"rx-{SCENARIOS[0].slug}-photo.png").write_bytes(build_scan_png(SCENARIOS[0]))
    print(f"Wrote {len(SCENARIOS) + 1} samples to {out.resolve()}")
