"""Run the extraction evaluation (ADR-024).

    python -m app.eval                      # offline extractor, default corpus
    python -m app.eval --provider groq      # the LLM path (needs GROQ_API_KEY)
    python -m app.eval --check              # exit 1 if below app/eval/thresholds.json

Writes report.json and report.md to --out (default: eval-report/).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict
from pathlib import Path

from app.eval import corpus
from app.eval.score import Report, aggregate, score_case
from app.modules.extraction import service as extraction
from app.modules.extraction.normalize import DEFAULT_DOSE_TIMES

THRESHOLDS = Path(__file__).with_name("thresholds.json")

LABELS = {
    "document_type": "Document type",
    "issued_on": "Issue / collection date",
    "prescriber": "Prescriber",
    "follow_up": "Follow-up date",
    "medication_recall": "Medicines found (recall)",
    "medication_precision": "Medicines correct (precision)",
    "strength": "Strength",
    "schedule": "Schedule (times, period, as needed)",
    "duration_days": "Duration",
    "investigations": "Investigations to-dos",
    "diet_notes": "Diet notes",
    "lab_recall": "Lab results found (recall)",
    "lab_precision": "Lab results correct (precision)",
    "lab_value": "Lab value",
    "lab_unit": "Lab unit",
    "lab_range": "Printed reference range",
    "lab_flag": "Flag against printed range",
}


async def run(
    provider: str, cases: list[corpus.Case] | None = None, *, stress: bool = False
) -> Report:
    cases = cases if cases is not None else corpus.build(stress=stress)
    results = []
    for case in cases:
        payload, _ = await extraction.extract_text_pages(
            case.pages(), dict(DEFAULT_DOSE_TIMES), offline=provider == "heuristic"
        )
        results.append(score_case(case, payload))
    return aggregate(f"{provider}{' (stress set)' if stress else ''}", results)


def to_markdown(report: Report) -> str:
    lines = [
        f"# Extraction evaluation: `{report.provider}`",
        "",
        f"{report.cases} synthetic documents. Overall (mean of metrics): **{report.overall:.1%}**",
        "",
        "| Metric | Score | Passed |",
        "|---|---:|---:|",
    ]
    for key, m in report.metrics.items():
        score = "n/a" if m["score"] is None else f"{m['score']:.1%}"
        lines.append(f"| {LABELS.get(key, key)} | {score} | {m['passed']}/{m['total']} |")
    lines += ["", "## By tag", "", "| Tag | Score |", "|---|---:|"]
    lines += [f"| `{t}` | {v['score']:.1%} |" for t, v in report.by_tag.items()]
    if report.failures:
        lines += ["", "## Failures (first 60)", ""]
        lines += [f"- `{f['case']}` {f['metric']}: {f['detail']}" for f in report.failures]
    return "\n".join(lines) + "\n"


def check(report: Report, thresholds: dict[str, float]) -> list[str]:
    problems = []
    for key, minimum in thresholds.items():
        got = report.overall if key == "overall" else (report.metrics.get(key) or {}).get("score")
        if got is None or got + 1e-9 < minimum:
            problems.append(f"{key}: {got} < {minimum}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.eval")
    parser.add_argument("--provider", choices=["heuristic", "groq"], default="heuristic")
    parser.add_argument("--out", default="eval-report")
    parser.add_argument("--check", action="store_true", help="fail below thresholds.json")
    parser.add_argument("--stress", action="store_true", help="held-out phrasings instead")
    args = parser.parse_args(argv)

    report = asyncio.run(run(args.provider, stress=args.stress))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    (out / "report.md").write_text(to_markdown(report), encoding="utf-8")
    print(to_markdown(report).split("## By tag")[0])

    if args.check:
        key = f"{args.provider}{'_stress' if args.stress else ''}"
        problems = check(report, json.loads(THRESHOLDS.read_text(encoding="utf-8"))[key])
        if problems:
            print("Below threshold:\n  " + "\n  ".join(problems), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
