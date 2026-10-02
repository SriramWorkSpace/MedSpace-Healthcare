"""A labelled, synthetic evaluation corpus for document extraction (ADR-024).

Each case is generated from a structured spec, so its gold answer is exact by construction. The
spec is rendered to a real PDF and read back with PyMuPDF, exactly like an upload, so layout and
text-extraction quirks (split lines, column order) are part of what gets measured.

Variation covers what real prescriptions do: numbered lists, "Tab." prefixes, pipes and tables,
"Sig:" on its own line, shorthand (1-0-1, BD, TDS, q8h, SOS, HS), duration styles (x 5 days, 5/7,
for 2 weeks), date formats, relative and absolute follow-ups, investigations and diet advice, and
lab reports with one-line and tabular rows. Everything is fictional.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, timedelta

import pymupdf

# ---- Vocabulary ---------------------------------------------------------------------------------

DRUGS = [
    ("Amoxicillin", "500 mg", "capsule"),
    ("Azithromycin", "250 mg", "tablet"),
    ("Paracetamol", "650 mg", "tablet"),
    ("Ibuprofen", "400 mg", "tablet"),
    ("Pantoprazole", "40 mg", "tablet"),
    ("Metformin", "500 mg", "tablet"),
    ("Atorvastatin", "20 mg", "tablet"),
    ("Amlodipine", "5 mg", "tablet"),
    ("Losartan", "50 mg", "tablet"),
    ("Cetirizine", "10 mg", "tablet"),
    ("Montelukast", "10 mg", "tablet"),
    ("Levothyroxine", "50 mcg", "tablet"),
    ("Omeprazole", "20 mg", "capsule"),
    ("Doxycycline", "100 mg", "capsule"),
    ("Prednisolone", "10 mg", "tablet"),
    ("Sertraline", "50 mg", "tablet"),
    ("Clopidogrel", "75 mg", "tablet"),
    ("Furosemide", "40 mg", "tablet"),
    ("Ondansetron", "4 mg", "tablet"),
    ("Cholecalciferol", "60000 IU", "capsule"),
]

# notation -> (times with default dose times, period, as_needed)
FREQUENCIES: dict[str, tuple[list[str], str, bool]] = {
    "1-0-1": (["08:00", "20:00"], "daily", False),
    "BD": (["08:00", "20:00"], "daily", False),
    "twice daily": (["08:00", "20:00"], "daily", False),
    "1-1-1": (["08:00", "14:00", "20:00"], "daily", False),
    "TDS": (["08:00", "14:00", "20:00"], "daily", False),
    "three times a day": (["08:00", "14:00", "20:00"], "daily", False),
    "OD": (["08:00"], "daily", False),
    "once daily": (["08:00"], "daily", False),
    "1-0-0": (["08:00"], "daily", False),
    "0-0-1": (["20:00"], "daily", False),
    "HS": (["22:00"], "daily", False),
    "at bedtime": (["22:00"], "daily", False),
    "QID": (["08:00", "14:00", "20:00", "22:00"], "daily", False),
    "q8h": (["00:00", "08:00", "16:00"], "interval", False),
    "every 6 hours": (["02:00", "08:00", "14:00", "20:00"], "interval", False),
    "once a week": (["08:00"], "weekly", False),
    "SOS": ([], "as_needed", True),
    "as needed": ([], "as_needed", True),
}

DURATIONS: dict[str, int | None] = {
    "x 5 days": 5,
    "x 7 days": 7,
    "5/7": 5,
    "for 10 days": 10,
    "for 2 weeks": 14,
    "x 1 month": 30,
    "x 6 weeks": 42,
    "x 90 days": 90,
    "": None,
}

# Stress set only: phrasings the extractor was not tuned on (held out, ADR-024).
WORD_FREQUENCIES: dict[str, tuple[list[str], str, bool]] = {
    "1 tablet twice a day": (["08:00", "20:00"], "daily", False),
    "one tab at night": (["22:00"], "daily", False),
    "every morning": (["08:00"], "daily", False),
    "2 times a day": (["08:00", "20:00"], "daily", False),
    "once in the morning": (["08:00"], "daily", False),
    "when required": ([], "as_needed", True),
}
WORD_DURATIONS: dict[str, int] = {
    "for one week": 7,
    "for three days": 3,
    "for a month": 30,
    "for 2 wks": 14,
}
BRANDS = {
    "Paracetamol": "Feverease",
    "Pantoprazole": "Acidguard",
    "Cetirizine": "Allerclear",
    "Amlodipine": "Vasocalm",
    "Metformin": "Glucobal",
}

INSTRUCTIONS = ["after food", "before food", "with water", "after meals", ""]

CLINICS = [
    "Maple Grove Family Clinic",
    "Cedar Point Medical Centre",
    "Bayview Internal Medicine Associates",
    "Summit Health Practice",
    "Riverbend Community Hospital",
]
DOCTORS = [
    ("Dr. Hana Okoye", "Family Medicine"),
    ("Dr. Rafael Duarte", "Internal Medicine"),
    ("Dr. Mei Lin Zhou", "Cardiology"),
    ("Dr. Samir Haddad", "Endocrinology"),
    ("Dr. Ingrid Solberg", "Pulmonology"),
]
TESTS = ["CBC", "HbA1c", "lipid panel", "TSH", "vitamin D", "chest X-ray", "ECG"]
DIET = [
    "Avoid alcohol.",
    "Drink plenty of fluids.",
    "Low salt diet.",
    "Avoid fried and fatty food.",
    "Limit caffeine.",
]

LABS = [
    # name, unit, ref text, low, high, value range
    ("Hemoglobin", "g/dL", "12.0 - 15.5", 12.0, 15.5, (10.5, 16.5)),
    ("Total cholesterol", "mg/dL", "< 200", None, 200, (150, 260)),
    ("LDL cholesterol", "mg/dL", "< 130", None, 130, (80, 180)),
    ("HDL cholesterol", "mg/dL", "> 40", 40, None, (30, 70)),
    ("Triglycerides", "mg/dL", "< 150", None, 150, (80, 240)),
    ("Fasting glucose", "mg/dL", "70 - 99", 70, 99, (75, 140)),
    ("HbA1c", "%", "4.0 - 5.6", 4.0, 5.6, (4.8, 8.4)),
    ("TSH", "mIU/L", "0.4 - 4.0", 0.4, 4.0, (0.3, 6.5)),
    ("Creatinine", "mg/dL", "0.6 - 1.1", 0.6, 1.1, (0.5, 1.6)),
]

DATE_STYLES = [
    lambda d: f"Date: {d:%B} {d.day}, {d.year}",
    lambda d: f"Date: {d.day:02d}/{d.month:02d}/{d.year}",
    lambda d: f"Dated {d.day}-{d:%b}-{d.year}",
    lambda d: f"Date: {d.isoformat()}",
]


# ---- Gold ---------------------------------------------------------------------------------------


@dataclass
class GoldMed:
    name: str
    strength: str
    times: list[str]
    period: str
    as_needed: bool
    duration_days: int | None


@dataclass
class GoldLab:
    name: str
    value: str
    unit: str
    ref_range: str
    flag: str  # low | high | normal


@dataclass
class Gold:
    document_type: str
    prescriber: str | None = None
    clinic: str | None = None
    issued_on: date | None = None
    follow_up: date | None = None
    medications: list[GoldMed] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)  # ordered investigations
    diet: list[str] = field(default_factory=list)
    labs: list[GoldLab] = field(default_factory=list)


@dataclass
class Case:
    id: str
    tags: list[str]
    lines: list[tuple[float, str]]  # (x offset, text) per printed line; x lets us draw columns
    gold: Gold

    def pdf(self) -> bytes:
        doc = pymupdf.open()
        page = doc.new_page(width=595, height=842)
        y = 60.0
        for x, text in self.lines:
            if text == "\n":
                y += 22
                continue
            if x < 0:  # same row as the previous line (table column)
                y -= 20
                x = -x
            page.insert_text((x, y), text, fontname="helv", fontsize=10.5)
            y += 20
        data = doc.tobytes()
        doc.close()
        return data

    def pages(self) -> list[str]:
        doc = pymupdf.open(stream=self.pdf(), filetype="pdf")
        texts = [p.get_text() for p in doc]
        doc.close()
        return texts


# ---- Generators ---------------------------------------------------------------------------------


def _med_line(rng: random.Random, i: int, template: str, med, freq, dur, instr) -> list[str]:
    name, strength, form = med
    parts = [p for p in (freq, dur, instr) if p]
    if template == "numbered":
        return [f"{i}. {name} {strength} {form} - " + " - ".join(parts)]
    if template == "tab":
        prefix = "Tab." if form == "tablet" else "Cap."
        return [f"{prefix} {name} {strength} " + " ".join(parts)]
    if template == "dash":
        return [f"- {name} {strength}  " + "  ".join(parts)]
    if template == "rx":
        return [f"Rx: {name} {strength} {form}, " + ", ".join(parts)]
    if template == "pipe":
        return [f"{name} {strength} | " + " | ".join(parts)]
    # "sig": dosing on its own line, as many prescriptions print it
    return [f"{i}. {name} {strength} {form}", f"Sig: {' '.join(parts)}"]


TEMPLATES = ["numbered", "tab", "dash", "rx", "pipe", "sig"]


def prescription(rng: random.Random, n: int, today: date, stress: bool = False) -> Case:
    issued = today - timedelta(days=rng.randint(0, 60))
    clinic = rng.choice(CLINICS)
    doctor, specialty = rng.choice(DOCTORS)
    template = TEMPLATES[n % len(TEMPLATES)]
    meds = rng.sample(DRUGS, rng.randint(1, 4))

    lines: list[tuple[float, str]] = [(56, clinic), (56, f"{doctor}, MD - {specialty}")]
    lines.append((56, f"Patient: Test Patient {n}"))
    if stress and rng.random() < 0.4:
        suffix = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}
        lines.append(
            (56, f"Date - {issued.day}{suffix.get(issued.day, 'th')} {issued:%B} {issued.year}")
        )
    else:
        lines.append((56, rng.choice(DATE_STYLES)(issued)))
    lines.append((56, "\n"))

    gold_meds = []
    freqs = {**FREQUENCIES, **(WORD_FREQUENCIES if stress else {})}
    durs = {**DURATIONS, **(WORD_DURATIONS if stress else {})}
    for i, med in enumerate(meds, start=1):
        freq = rng.choice(list(freqs))
        dur = "" if freqs[freq][2] else rng.choice(list(durs))
        instr = rng.choice(INSTRUCTIONS)
        shown = med
        if stress:
            name, strength, form = med
            if rng.random() < 0.3:
                strength = strength.replace(" ", "")
            if rng.random() < 0.25:
                name = name.upper()
            if name.title() in BRANDS and rng.random() < 0.5:
                name = f"{name} ({BRANDS[name.title()]})"
            shown = (name, strength, form)
        for text in _med_line(rng, i, template, shown, freq, dur, instr):
            lines.append((56, text))
        times, period, prn = freqs[freq]
        gold_meds.append(
            GoldMed(
                name=med[0],
                strength=med[1],
                times=times,
                period=period,
                as_needed=prn,
                duration_days=durs.get(dur),
            )
        )

    lines.append((56, "\n"))
    follow_up = None
    styles = ["relative_weeks", "relative_days", "absolute", "none"]
    style = rng.choice(styles + (["month_words"] if stress else []))
    if style == "relative_weeks":
        weeks = rng.randint(1, 6)
        lines.append((56, f"Follow-up: Review in {weeks} week{'s' if weeks > 1 else ''}"))
        follow_up = issued + timedelta(days=7 * weeks)
    elif style == "relative_days":
        days = rng.choice([5, 10, 14])
        lines.append((56, f"Review after {days} days"))
        follow_up = issued + timedelta(days=days)
    elif style == "month_words":
        lines.append((56, "Come back after 1 month"))
        follow_up = issued + timedelta(days=30)
    elif style == "absolute":
        follow_up = issued + timedelta(days=rng.randint(10, 60))
        lines.append((56, f"Next visit: {follow_up:%B} {follow_up.day}, {follow_up.year}"))

    tests = rng.sample(TESTS, rng.randint(0, 2))
    if tests:
        lines.append((56, f"Investigations: {' and '.join(tests)} before next visit"))
    diet = rng.sample(DIET, rng.randint(0, 2))
    if diet:
        lines.append((56, f"Advice: {' '.join(diet)}"))

    return Case(
        id=f"{'stress-' if stress else ''}rx-{n:03d}",
        tags=["prescription", f"template:{template}", f"follow-up:{style}"],
        lines=lines,
        gold=Gold(
            document_type="prescription",
            prescriber=doctor,
            clinic=clinic,
            issued_on=issued,
            follow_up=follow_up,
            medications=gold_meds,
            tests=tests,
            diet=diet,
        ),
    )


def _fmt(v: float) -> str:
    return f"{v:.1f}" if v < 20 else f"{round(v)}"


def lab_report(rng: random.Random, n: int, today: date) -> Case:
    collected = today - timedelta(days=rng.randint(0, 90))
    layout = ["table", "inline", "inline_flags"][n % 3]
    rows = rng.sample(LABS, rng.randint(3, 6))
    lines: list[tuple[float, str]] = [
        (56, "Northwind Diagnostics Laboratory"),
        (56, "Laboratory Report"),
        (56, f"Patient: Test Patient {n}"),
        (56, f"Collected: {collected:%B} {collected.day}, {collected.year}"),
        (56, "\n"),
    ]
    if layout == "table":
        lines += [(56, "Test"), (-300, "Result"), (-430, "Reference")]
    else:
        lines.append((56, "Reference range"))

    gold_labs = []
    for name, unit, ref, low, high, (vmin, vmax) in rows:
        value = rng.uniform(vmin, vmax)
        text = _fmt(value)
        v = float(text)
        flag = (
            "low"
            if low is not None and v < low
            else "high"
            if high is not None and (v >= high if ref.startswith("<") else v > high)
            else "normal"
        )
        if layout == "table":
            lines += [(56, f"{name}:"), (-300, f"{text} {unit}"), (-430, ref)]
        else:
            mark = {"high": " H", "low": " L"}.get(flag, "") if layout == "inline_flags" else ""
            lines.append((56, f"{name}: {text} {unit}{mark} ({ref})"))
        gold_labs.append(GoldLab(name=name, value=text, unit=unit, ref_range=ref, flag=flag))

    return Case(
        id=f"lab-{n:03d}",
        tags=["lab_report", f"layout:{layout}"],
        lines=lines,
        gold=Gold(document_type="lab_report", issued_on=collected, labs=gold_labs),
    )


def build(
    n_prescriptions: int = 48,
    n_labs: int = 18,
    seed: int = 7,
    today: date | None = None,
    stress: bool = False,
):
    """Deterministic for a given seed and day.

    The default set is the regression gate: the extractor has been tuned against it. The stress
    set (stress=True, its own seed) adds phrasings that were held out from tuning, so its score is
    the honest estimate of how the extractor generalizes.
    """
    rng = random.Random(seed + (1000 if stress else 0))  # noqa: S311 (synthetic test data)
    today = today or date(2026, 6, 1)
    cases = [prescription(rng, i, today, stress) for i in range(n_prescriptions)]
    if not stress:
        cases += [lab_report(rng, i, today) for i in range(n_labs)]
    return cases
