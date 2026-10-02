"""The extraction evaluation harness, and the extractor behaviours it drove (ADR-024)."""

from __future__ import annotations

import json
from datetime import date

from app.eval import corpus
from app.eval.__main__ import THRESHOLDS, check, run
from app.eval.score import aggregate, score_case
from app.modules.extraction import heuristic
from app.modules.extraction.normalize import parse_duration_days
from app.modules.extraction.schemas import (
    ExtractedLabResult,
    ExtractedMedication,
    ExtractionPayload,
    FollowUp,
    Prescriber,
    ScheduleModel,
)


def _perfect(case: corpus.Case) -> ExtractionPayload:
    g = case.gold
    return ExtractionPayload(
        document_type=g.document_type,
        prescriber=Prescriber(name=g.prescriber, clinic=g.clinic),
        issued_on=g.issued_on,
        follow_up=FollowUp(date=g.follow_up) if g.follow_up else None,
        medications=[
            ExtractedMedication(
                name=m.name,
                strength=m.strength,
                duration_days=m.duration_days,
                schedule=ScheduleModel(times=m.times, period=m.period, as_needed=m.as_needed),
            )
            for m in g.medications
        ],
        care_actions=[{"kind": "lab_test", "title": f"Get {t} test"} for t in g.tests],
        diet_notes=[{"text": d} for d in g.diet],
        lab_results=[
            ExtractedLabResult(name=x.name, value=x.value, unit=x.unit, ref_range=x.ref_range)
            for x in g.labs
        ],
    )


def test_corpus_is_deterministic_and_varied():
    a, b = corpus.build(), corpus.build()
    assert [c.id for c in a] == [c.id for c in b]
    assert [c.pages() for c in a[:3]] == [c.pages() for c in b[:3]]
    tags = {t for c in a for t in c.tags}
    assert {f"template:{t}" for t in corpus.TEMPLATES} <= tags
    assert {"layout:table", "layout:inline", "layout:inline_flags"} <= tags
    stress = corpus.build(stress=True)
    assert all(c.id.startswith("stress-") for c in stress)


def test_a_perfect_answer_scores_100_and_mistakes_are_counted():
    cases = corpus.build(n_prescriptions=6, n_labs=3)
    results = [score_case(c, _perfect(c)) for c in cases]
    assert aggregate("perfect", results).overall == 1.0

    case = next(c for c in cases if len(c.gold.medications) >= 2)
    wrong = _perfect(case)
    wrong.medications = wrong.medications[1:]  # one medicine missed
    wrong.medications.append(ExtractedMedication(name="Placebozol", strength="1 mg"))
    r = aggregate("wrong", [score_case(case, wrong)])
    assert r.metrics["medication_recall"]["score"] < 1
    assert r.metrics["medication_precision"]["score"] < 1
    assert any("missed" in f["detail"] for f in r.failures)


async def test_offline_extractor_meets_its_thresholds():
    thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))
    report = await run("heuristic")
    assert check(report, thresholds["heuristic"]) == [], report.failures[:10]
    stress = await run("heuristic", stress=True)
    assert check(stress, thresholds["heuristic_stress"]) == [], stress.failures[:10]


# ---- Behaviours added because the evaluation found them missing ---------------------------------


def test_dosing_on_its_own_line_belongs_to_the_medicine_above():
    payload = heuristic.extract(["1. Amoxicillin 500 mg capsule", "Sig: BD x 5 days after food"])
    med = payload.medications[0]
    assert (med.frequency_raw, med.duration_days, med.instructions) == ("BD", 5, "after food")
    assert "frequency_raw" not in med.uncertain_fields


def test_numeric_dates_are_day_first_and_ambiguous_ones_are_flagged():
    p = heuristic.extract(["Dr. Ana Ruiz", "Date: 11/05/2026", "Amoxicillin 500 mg BD"])
    assert p.issued_on == date(2026, 5, 11)
    assert any("can be read two ways" in w for w in p.warnings)
    p = heuristic.extract(["Date: 25/05/2026", "Amoxicillin 500 mg BD"])
    assert p.issued_on == date(2026, 5, 25) and not p.warnings
    p = heuristic.extract(["Date: 2026-04-07", "Amoxicillin 500 mg BD"])
    assert p.issued_on == date(2026, 4, 7) and not p.warnings


def test_brands_caps_and_words():
    p = heuristic.extract(
        [
            "PARACETAMOL (Feverease) 650mg - every morning - for one week",
            "Cetirizine 10 mg - 2 times a day - for a month",
        ]
    )
    names = [(m.name, m.strength, m.frequency_raw, m.duration_days) for m in p.medications]
    assert names == [
        ("Paracetamol", "650mg", "every morning", 7),
        ("Cetirizine", "10 mg", "2 times a day", 30),
    ]
    assert parse_duration_days("for three days") == 3


def test_follow_up_phrasings():
    def follow_up(line):
        p = heuristic.extract(["Date: 2026-05-01", "Amoxicillin 500 mg BD", line])
        return p.follow_up.date if p.follow_up else None

    assert follow_up("Come back after 1 month") == date(2026, 5, 31)
    assert follow_up("Return in 2 weeks") == date(2026, 5, 15)
    assert follow_up("Return if fever persists") is None
