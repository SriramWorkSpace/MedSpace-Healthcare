"""Evidence highlights: where each extracted value is printed on the page (ADR-031)."""

from __future__ import annotations

import httpx
import pymupdf
import pytest
from sqlalchemy import select

from app.modules.demo.samples import SCENARIOS, _diabetes, build_lab_pdf, build_pdf, build_scan_png
from app.modules.extraction import evidence, heuristic
from app.modules.extraction.models import Extraction
from app.shared.queue import drain
from tests.conftest import BASE_URL, csrf, signup
from tests.test_documents_flow import upload


def text_in(data: bytes, spot: dict) -> str:
    """The text inside a spot's first box (the inverse of what `locate` computed)."""
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        page = doc[spot["page"] - 1]
        x0, y0, x1, y1 = spot["boxes"][0]
        w, h = page.rect.width, page.rect.height
        return " ".join(page.get_textbox(pymupdf.Rect(x0 * w, y0 * h, x1 * w, y1 * h)).split())


def read(data: bytes):
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        return heuristic.extract([p.get_text() for p in doc])


# ---- The locator --------------------------------------------------------------------------------


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda s: s.slug)
def test_every_medication_field_is_found_where_it_is_printed(scenario):
    data = build_pdf(scenario)
    payload = read(data)
    ev = evidence.locate(data, "application/pdf", payload)
    assert ev["available"] is True
    for i, med in enumerate(payload.medications):
        name = ev["fields"][f"medications.{i}.name"]
        assert med.name in text_in(data, name)
        for field, value in (
            ("strength", med.strength),
            ("frequency_raw", med.frequency_raw),
            ("duration_days", med.duration_raw),
        ):
            if value:
                assert value in text_in(data, ev["fields"][f"medications.{i}.{field}"])
        # The whole line: every box on the medicine's page and inside the page.
        line = ev["items"][f"medications.{i}"]
        assert line["page"] == med.source_page
        assert all(0 <= v <= 1 for box in line["boxes"] for v in box)
    for i, note in enumerate(payload.diet_notes):
        assert note.text in text_in(data, ev["fields"][f"diet_notes.{i}.text"])


def test_repeated_values_resolve_to_their_own_row():
    """'mg/dL' and similar numbers appear on several rows; each result gets its own."""
    data = build_lab_pdf(_diabetes("x", 10, "6.8", 118, "0.8"))
    payload = read(data)
    ev = evidence.locate(data, "application/pdf", payload)
    ys = []
    for i, r in enumerate(payload.lab_results):
        value = ev["fields"][f"lab_results.{i}.value"]
        assert r.value in text_in(data, value)
        assert r.ref_range in text_in(data, ev["fields"][f"lab_results.{i}.ref_range"])
        name_box = ev["fields"][f"lab_results.{i}.name"]["boxes"][0]
        unit_box = ev["fields"][f"lab_results.{i}.unit"]["boxes"][0]
        assert abs(name_box[1] - unit_box[1]) < 0.02  # same row as its name
        ys.append(name_box[1])
    assert ys == sorted(ys) and len(set(ys)) == len(ys)


def test_letterhead_and_dates_are_found():
    data = build_pdf(SCENARIOS[1])
    payload = read(data)
    ev = evidence.locate(data, "application/pdf", payload)
    assert "Tomas Varga" in text_in(data, ev["fields"]["prescriber.name"])
    assert payload.prescriber.clinic in text_in(data, ev["fields"]["prescriber.clinic"])
    assert "August 23, 2026" in text_in(data, ev["fields"]["issued_on"])
    assert "Review in 3 months" in text_in(data, ev["fields"]["follow_up.date"])


def test_photos_have_no_text_to_search():
    payload = read(build_pdf(SCENARIOS[0]))
    ev = evidence.locate(build_scan_png(SCENARIOS[0]), "image/png", payload)
    assert ev["available"] is False and ev["reason"] == "no_text"
    assert ev["fields"] == {}


def test_values_not_on_the_page_are_simply_missing():
    data = build_pdf(SCENARIOS[0])
    payload = read(data)
    payload.medications[0].name = "Nonexistentamycin"
    payload.medications[0].strength = "999 mg"
    ev = evidence.locate(data, "application/pdf", payload)
    assert "medications.0.name" not in ev["fields"]
    assert "medications.1.name" in ev["fields"]


# ---- The endpoint -------------------------------------------------------------------------------


async def test_evidence_endpoint_computes_once_and_is_private(
    auth_client: httpx.AsyncClient, session
):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[0]))).json()
    await drain()
    resp = await auth_client.get(f"/api/documents/{doc['id']}/evidence")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["available"] is True
    assert body["fields"]["medications.0.name"]["page"] == 1
    extraction = await session.scalar(select(Extraction))
    assert extraction.evidence["version"] == evidence.VERSION
    assert str(extraction.id) == body["extraction_id"]

    again = await auth_client.get(f"/api/documents/{doc['id']}/evidence")
    assert again.json() == body

    from app.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as bo:
        await signup(bo, email="bo@example.com")
        other = await bo.get(f"/api/documents/{doc['id']}/evidence")
        assert other.status_code == 404


async def test_reprocessing_gets_fresh_evidence(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[1]))).json()
    await drain()
    first = (await auth_client.get(f"/api/documents/{doc['id']}/evidence")).json()
    await auth_client.post(f"/api/documents/{doc['id']}/reprocess", headers=csrf(auth_client))
    await drain()
    second = (await auth_client.get(f"/api/documents/{doc['id']}/evidence")).json()
    assert second["extraction_id"] != first["extraction_id"]
    assert second["fields"] == first["fields"]


async def test_scans_report_no_text(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_scan_png(SCENARIOS[0]), "scan.png")).json()
    await drain()
    resp = await auth_client.get(f"/api/documents/{doc['id']}/evidence")
    assert resp.status_code == 200
    assert resp.json()["available"] is False and resp.json()["reason"] == "no_text"
