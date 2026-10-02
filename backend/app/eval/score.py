"""Field-level scoring of an ExtractionPayload against a gold answer.

Every check is a (metric, passed) pair, so results aggregate into accuracy per metric, per tag,
and a list of concrete failures to read. Medicines and lab results are matched to gold by name
(tolerant of small differences) before their fields are compared.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher

from app.eval.corpus import Case
from app.modules.extraction import labs
from app.modules.extraction.schemas import ExtractionPayload


@dataclass
class Check:
    metric: str
    passed: bool
    detail: str = ""


@dataclass
class CaseResult:
    case_id: str
    tags: list[str]
    checks: list[Check] = field(default_factory=list)

    def add(self, metric: str, passed: bool, detail: str = "") -> None:
        self.checks.append(Check(metric, bool(passed), detail))


def _norm(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _match(gold: list, pred: list, key_gold, key_pred, threshold: float = 0.85):
    """Greedy best-first matching by name similarity. Returns (pairs, unmatched_gold, extra)."""
    candidates = sorted(
        (
            (_similar(key_gold(g), key_pred(p)), gi, pi)
            for gi, g in enumerate(gold)
            for pi, p in enumerate(pred)
        ),
        reverse=True,
    )
    used_g, used_p, pairs = set(), set(), []
    for score, gi, pi in candidates:
        if score < threshold or gi in used_g or pi in used_p:
            continue
        used_g.add(gi)
        used_p.add(pi)
        pairs.append((gold[gi], pred[pi]))
    missing = [g for i, g in enumerate(gold) if i not in used_g]
    extra = [p for i, p in enumerate(pred) if i not in used_p]
    return pairs, missing, extra


def score_case(case: Case, payload: ExtractionPayload) -> CaseResult:
    g = case.gold
    r = CaseResult(case.id, case.tags)
    r.add("document_type", payload.document_type == g.document_type, payload.document_type)
    r.add(
        "issued_on",
        payload.issued_on == g.issued_on,
        f"got {payload.issued_on}, want {g.issued_on}",
    )

    if g.document_type == "prescription":
        got = payload.prescriber.name if payload.prescriber else None
        r.add(
            "prescriber", _norm(got) == _norm(g.prescriber), f"got {got!r}, want {g.prescriber!r}"
        )
        got_fu = payload.follow_up.date if payload.follow_up else None
        r.add("follow_up", got_fu == g.follow_up, f"got {got_fu}, want {g.follow_up}")

        pairs, missing, extra = _match(
            g.medications, payload.medications, lambda m: m.name, lambda m: m.name
        )
        for m in missing:
            r.add("medication_recall", False, f"missed {m.name} {m.strength}")
        for _ in pairs:
            r.add("medication_recall", True)
        for p in extra:
            r.add("medication_precision", False, f"extra {p.name} {p.strength}")
        for _ in pairs:
            r.add("medication_precision", True)
        for gm, pm in pairs:
            r.add(
                "strength",
                _norm(pm.strength).replace(" ", "") == _norm(gm.strength).replace(" ", ""),
                f"{gm.name}: got {pm.strength!r}, want {gm.strength!r}",
            )
            sched = pm.schedule
            got = (sched.times, sched.period, sched.as_needed) if sched else None
            want = (gm.times, gm.period, gm.as_needed)
            r.add(
                "schedule", got == want, f"{gm.name}: got {got}, want {want} ({pm.frequency_raw!r})"
            )
            r.add(
                "duration_days",
                pm.duration_days == gm.duration_days,
                f"{gm.name}: got {pm.duration_days}, want {gm.duration_days}",
            )

        titles = [_norm(a.title) for a in payload.care_actions if a.kind == "lab_test"]
        for t in g.tests:
            r.add("investigations", any(_norm(t) in x for x in titles), f"missed test {t!r}")
        notes = [n.text for n in payload.diet_notes]
        for d in g.diet:
            r.add("diet_notes", any(_similar(d, n) > 0.8 for n in notes), f"missed advice {d!r}")

    if g.document_type == "lab_report":
        pairs, missing, extra = _match(
            g.labs, payload.lab_results, lambda x: x.name, lambda x: x.name
        )
        for m in missing:
            r.add("lab_recall", False, f"missed {m.name}")
        for _ in pairs:
            r.add("lab_recall", True)
            r.add("lab_precision", True)
        for p in extra:
            r.add("lab_precision", False, f"extra {p.name}")
        for gl, pl in pairs:
            r.add(
                "lab_value", pl.value == gl.value, f"{gl.name}: got {pl.value!r}, want {gl.value!r}"
            )
            r.add("lab_unit", _norm(pl.unit) == _norm(gl.unit), f"{gl.name}: got {pl.unit!r}")
            r.add(
                "lab_range",
                _norm(pl.ref_range) == _norm(gl.ref_range),
                f"{gl.name}: got {pl.ref_range!r}, want {gl.ref_range!r}",
            )
            flag = labs.resolve_flag(pl.value, pl.ref_range, pl.flag)
            r.add("lab_flag", flag == gl.flag, f"{gl.name}: got {flag}, want {gl.flag}")
    return r


@dataclass
class Report:
    provider: str
    cases: int
    metrics: dict[str, dict]  # metric -> {passed, total, score}
    by_tag: dict[str, dict[str, float]]
    failures: list[dict]
    overall: float


def aggregate(provider: str, results: list[CaseResult], max_failures: int = 60) -> Report:
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    tag_totals: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    failures = []
    for r in results:
        for c in r.checks:
            totals[c.metric][0] += c.passed
            totals[c.metric][1] += 1
            for t in r.tags:
                tag_totals[t][c.metric][0] += c.passed
                tag_totals[t][c.metric][1] += 1
            if not c.passed and len(failures) < max_failures:
                failures.append({"case": r.case_id, "metric": c.metric, "detail": c.detail})
    metrics = {
        m: {"passed": p, "total": n, "score": round(p / n, 4) if n else None}
        for m, (p, n) in sorted(totals.items())
    }
    by_tag = {
        t: {
            "score": round(sum(p for p, _ in v.values()) / max(1, sum(n for _, n in v.values())), 4)
        }
        for t, v in sorted(tag_totals.items())
    }
    scored = [v["score"] for v in metrics.values() if v["score"] is not None]
    overall = round(sum(scored) / len(scored), 4) if scored else 0.0
    return Report(provider, len(results), metrics, by_tag, failures, overall)
