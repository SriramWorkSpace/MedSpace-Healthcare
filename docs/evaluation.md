# Extraction evaluation

How MedSpace measures document extraction, and what the numbers mean (ADR-024).

## Method

`backend/app/eval/` generates a labelled corpus of fictional documents from structured specs, so every answer is exact by construction. Each spec is rendered to a real PDF and read back with PyMuPDF, the same path as an upload, then sent through `extract_text_pages` (extraction plus deterministic normalization). A scorer compares the result with the gold answer field by field.

| Set | Documents | Purpose |
|---|---:|---|
| Regression set | 48 prescriptions, 18 lab reports | The extractor is tuned against it. CI fails if it drops below `app/eval/thresholds.json`. |
| Stress set | 48 prescriptions, own seed | Adds phrasings held out from tuning: brand names in brackets, ALL-CAPS names, `500mg`, frequencies and durations in words, ordinal dates, "come back after 1 month". |

Variation in both: six line layouts (numbered, `Tab.`, dashes, `Rx:`, pipes, and dosing on a separate `Sig:` line), shorthand (`1-0-1`, `BD`, `TDS`, `QID`, `q8h`, `HS`, `SOS`), duration styles (`x 5 days`, `5/7`, `for 2 weeks`), four date formats, relative and absolute follow-ups, investigations, diet advice, and lab reports as tables, one-line rows, and rows with printed `H`/`L` flags.

### Metrics

Medicines and lab results are matched to gold by name (similarity of at least 0.85), then compared field by field.

| Metric | Passes when |
|---|---|
| Medicines found / correct | Recall and precision of matched medicines |
| Strength | Same strength, ignoring spaces and case |
| Schedule | Same clock times, period and as-needed flag after normalization |
| Duration | Same number of days |
| Issue date, follow-up date | Exact date |
| Prescriber, document type | Exact (normalized) |
| Investigations, diet notes | Every gold item appears among extracted to-dos or notes |
| Lab value, unit, range, flag | Exactly as printed; the flag compares the value only with the printed range |

## Results: offline extractor

The first run of each set happened before any fixes, so the stress-set baseline is a genuine held-out result.

| Metric | Regression, before | Stress (held out), before | Both sets, after |
|---|---:|---:|---:|
| **Overall (mean of metrics)** | **96.2%** | **92.5%** | **100%** |
| Medicines found | 100% | 88.6% | 100% |
| Schedule | 77.8% | 82.6% | 100% |
| Duration | 78.6% | 77.1% | 100% |
| Issue date | 92.4% | 100% | 100% |
| Follow-up date | 95.8% | 70.8% | 100% |
| Investigations | 90.6% | 100% | 100% |
| Lab fields (all) | 100% | n/a | 100% |

### What the evaluation found, and what changed

1. **Dosing on its own line** (`Sig: BD x 5 days`) was ignored. It now attaches to the medicine above.
2. **Numeric dates** like `11/05/2026` were read month-first. They are now read day-first, the convention of the shorthand this extractor targets, with a review warning whenever both readings are valid. ISO dates are parsed explicitly.
3. **"chest X-ray"** was not recognised as an investigation.
4. *(Stress set)* **Brand names in brackets** hid the medicine entirely, ALL-CAPS names are now title-cased, and frequencies and durations written in words ("every morning", "2 times a day", "for one week") are recognised.
5. *(Stress set)* **"Come back after 1 month"**, "return in 2 weeks" and "see me after 10 days" are follow-ups; "return if fever persists" is not.

**Caveat:** after these fixes both sets have been seen during tuning, so 100% means "no known regressions", not "100% accurate". Real documents are messier than any generator. The honest generalization estimate is the held-out baseline above; the next held-out set should introduce new phrasings rather than a new seed.

## Running it

```bash
cd backend
python -m app.eval                     # regression set, offline extractor
python -m app.eval --stress            # held-out phrasings
python -m app.eval --check             # exit 1 below thresholds (what CI runs)
GROQ_API_KEY=... python -m app.eval --provider groq   # the LLM text path
```

Reports go to `eval-report/report.md` and `report.json`, with per-tag scores and the first 60 failures. CI uploads both sets as the `extraction-eval` artifact.

The Groq path has thresholds in `thresholds.json` but has not been measured here, because the repository runs without an API key. Run it with a key before relying on those numbers.
