"""Lab results: copied from reports, flagged only against the printed range, charted over time."""

from __future__ import annotations

import httpx
import pymupdf
import pytest

from app.modules.demo.samples import LAB_REPORT, build_lab_pdf
from app.modules.extraction import heuristic, labs
from app.shared.queue import drain
from tests.conftest import BASE_URL, csrf
from tests.test_assistant import ask, new_thread
from tests.test_documents_flow import confirm_body, upload


@pytest.mark.parametrize(
    ("value", "ref", "flag"),
    [
        ("212", "< 200", "high"),
        ("200", "< 200", "high"),  # "< 200" excludes 200 itself
        ("199", "< 200", "normal"),
        ("40", "> 40", "low"),
        ("40", ">= 40", "normal"),
        ("5.6", "4.0 - 5.6", "normal"),
        ("3.9", "4.0 – 5.6", "low"),  # noqa: RUF001 (en dash as printed)
        ("4,500", "4,000-11,000", "normal"),
        ("Negative", None, None),
        ("<0.5", "< 1.0", None),  # bounded values are kept as text, not compared
        ("12", "see note", None),
    ],
)
def test_flags_compare_only_with_the_printed_range(value, ref, flag):
    assert labs.resolve_flag(value, ref, None) == flag


def test_printed_flag_is_kept_when_there_is_no_usable_range():
    assert labs.resolve_flag("Positive", None, "high") == "high"
    # A printed range wins, so editing the value in review cannot leave a stale flag.
    assert labs.resolve_flag("150", "< 200", "high") == "normal"


@pytest.mark.parametrize(
    ("name", "key"),
    [
        ("LDL-C", "ldl-cholesterol"),
        ("LDL Cholesterol (calculated)", "ldl-cholesterol"),
        ("Cholesterol, Total", "total-cholesterol"),
        ("Hemoglobin A1c", "hba1c"),
        ("Fasting Blood Sugar", "fasting-glucose"),
        ("Serum Creatinine", "creatinine"),
        ("Vitamin B12", "vitamin-b12"),
    ],
)
def test_test_names_line_up_across_labs(name, key):
    assert labs.analyte_key(name) == key


def _lab_pdf_text() -> str:
    doc = pymupdf.open(stream=build_lab_pdf(LAB_REPORT), filetype="pdf")
    return doc[0].get_text()


def test_heuristic_reads_split_line_lab_tables():
    payload = heuristic.extract([_lab_pdf_text()])
    assert payload.document_type == "lab_report"
    assert payload.issued_on is not None
    assert [(r.name, r.value, r.unit, r.ref_range) for r in payload.lab_results] == [
        ("Total cholesterol", "212", "mg/dL", "< 200"),
        ("LDL cholesterol", "138", "mg/dL", "< 130"),
        ("HDL cholesterol", "48", "mg/dL", "> 40"),
        ("Triglycerides", "131", "mg/dL", "< 150"),
    ]
    # Results are not tests to go and get, and a lab is not a prescriber.
    assert payload.care_actions == []
    assert payload.summary.startswith("Lab report from Cedar Valley Diagnostics")


def test_heuristic_reads_single_line_rows_and_printed_flags():
    page = "\n".join(
        [
            "Northside Lab",
            "Reference range",
            "HbA1c: 6.1 % H (4.0 - 5.6)",
            "Fasting glucose 104 mg/dL 70-99",
            "Urine sugar: Negative",
            "Patient: Sam Doe 41",
        ]
    )
    rows = {r.name: r for r in heuristic.extract([page]).lab_results}
    assert set(rows) == {"HbA1c", "Fasting glucose", "Urine sugar"}
    assert rows["HbA1c"].flag == "high"
    assert (rows["HbA1c"].unit, rows["HbA1c"].ref_range) == ("%", "4.0 - 5.6")
    assert rows["Urine sugar"].value == "Negative"


def test_prescriptions_are_not_read_as_lab_reports():
    page = "Dr. Ana Ruiz\nAmoxicillin 500 mg 1-0-1 x 5 days\nInvestigations: CBC"
    payload = heuristic.extract([page])
    assert payload.lab_results == []
    assert [a.kind for a in payload.care_actions] == ["lab_test"]


def lab_confirm_body(payload: dict) -> dict:
    body = confirm_body(payload)
    body["lab_results"] = [
        {k: r[k] for k in ("name", "value", "unit", "ref_range", "flag", "source_page")}
        for r in payload["lab_results"]
    ]
    return body


async def _upload_lab(client: httpx.AsyncClient) -> tuple[dict, dict]:
    doc = (await upload(client, build_lab_pdf(LAB_REPORT), name="lipids.pdf")).json()
    await drain()
    ex = (await client.get(f"/api/documents/{doc['id']}/extraction")).json()
    return doc, ex


async def test_review_edits_are_kept_and_flags_recomputed(auth_client: httpx.AsyncClient):
    _, ex = await _upload_lab(auth_client)
    assert len(ex["payload"]["lab_results"]) == 4
    body = lab_confirm_body(ex["payload"])
    body["lab_results"][1]["value"] = "128"  # the reviewer fixes a misread LDL
    resp = await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm", json=body, headers=csrf(auth_client)
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["prescription_id"] is None  # a lab report is not a prescription

    trends = {t["key"]: t for t in (await auth_client.get("/api/labs")).json()}
    assert list(trends) == [
        "total-cholesterol",
        "ldl-cholesterol",
        "hdl-cholesterol",
        "triglycerides",
    ]
    ldl = trends["ldl-cholesterol"]["latest"]
    assert (ldl["value"], ldl["value_text"], ldl["flag"]) == (128.0, "128", "normal")
    assert trends["total-cholesterol"]["latest"]["flag"] == "high"
    assert trends["hdl-cholesterol"]["latest"]["ref_low"] == 40.0


async def test_reconfirming_replaces_results(auth_client: httpx.AsyncClient):
    doc, ex = await _upload_lab(auth_client)
    await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm",
        json=lab_confirm_body(ex["payload"]),
        headers=csrf(auth_client),
    )
    await auth_client.post(f"/api/documents/{doc['id']}/reprocess", headers=csrf(auth_client))
    await drain()
    ex2 = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    assert ex2["version"] == 2
    await auth_client.post(
        f"/api/extractions/{ex2['id']}/confirm",
        json=lab_confirm_body(ex2["payload"]),
        headers=csrf(auth_client),
    )
    detail = (await auth_client.get("/api/labs/ldl-cholesterol")).json()
    assert detail["count"] == 1


async def test_demo_trends_chart_history(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    trends = (await client.get("/api/labs")).json()
    keys = [t["key"] for t in trends]
    # The newest report's tests come first, in report order.
    assert keys[:3] == ["hba1c", "fasting-glucose", "creatinine"]

    ldl = (await client.get("/api/labs/ldl-cholesterol")).json()
    assert ldl["count"] == 3 and ldl["uncharted"] == 0
    assert [p["value"] for p in ldl["points"]] == [158.0, 149.0, 138.0]  # oldest first
    assert ldl["latest"]["value"] == 138.0 and ldl["previous"]["value"] == 149.0
    assert ldl["latest"]["document_title"] == "Lipid profile results"
    assert [r["collected_on"] for r in ldl["results"]] == sorted(
        (r["collected_on"] for r in ldl["results"]), reverse=True
    )
    hdl = (await client.get("/api/labs/hdl-cholesterol")).json()
    assert {r["flag"] for r in hdl["results"]} == {"normal"}


async def test_other_units_are_listed_but_not_charted(auth_client: httpx.AsyncClient):
    _, ex = await _upload_lab(auth_client)
    body = lab_confirm_body(ex["payload"])
    body["lab_results"].append(
        {
            "name": "LDL-C",
            "value": "3.6",
            "unit": "mmol/L",
            "ref_range": "< 3.4",
            "flag": None,
            "source_page": 1,
        }
    )
    await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm", json=body, headers=csrf(auth_client)
    )
    ldl = (await auth_client.get("/api/labs/ldl-cholesterol")).json()
    assert ldl["count"] == 2
    assert len(ldl["points"]) + ldl["uncharted"] == 2
    assert ldl["uncharted"] == 1


async def test_labs_are_private_and_deletable(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    ldl = (await client.get("/api/labs/ldl-cholesterol")).json()
    result_id = ldl["latest"]["id"]
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={"email": "eve@example.com", "password": "long-enough-pass", "display_name": "E"},
        )
        assert (await other.get("/api/labs")).json() == []
        assert (await other.get("/api/labs/ldl-cholesterol")).status_code == 404
        resp = await other.delete(f"/api/lab-results/{result_id}", headers=csrf(other))
        assert resp.status_code == 404

    assert (
        await client.delete(f"/api/lab-results/{result_id}", headers=csrf(client))
    ).status_code == 204
    assert (await client.get("/api/labs/ldl-cholesterol")).json()["count"] == 2
    assert (await client.get("/api/labs/NOT a key")).status_code == 422


async def test_search_and_ask_use_lab_results(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    hits = (await client.get("/api/search", params={"q": "ldl"})).json()["groups"]["lab_results"]
    assert hits[0]["href"] == "/app/labs/ldl-cholesterol"
    assert hits[0]["subtitle"].startswith("138 mg/dL")

    thread = await new_thread(client)
    res = await ask(client, thread, "What was my LDL on the last report?")
    titles = [s["title"] for s in res["sources"]]
    assert "LDL cholesterol (lab result)" in titles
    assert not any("HbA1c" in t for t in titles)
    assert "138 mg/dL" in res["answer"]
    assert "range printed on the report: < 130, above that range" in res["answer"]

    res = await ask(client, thread, "Is my cholesterol high?")
    assert res["answer"].startswith("I can't give medical advice")
    assert "Total cholesterol (lab result)" in [s["title"] for s in res["sources"]]
