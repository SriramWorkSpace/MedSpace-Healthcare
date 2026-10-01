from __future__ import annotations

import json

import httpx

from app.modules.assistant.service import chunk_pages, classify, keywords
from tests.conftest import BASE_URL, csrf


async def ask(client: httpx.AsyncClient, thread_id: str, question: str) -> dict:
    """Consume the SSE stream and return {sources, answer, done, events}."""
    out = {"sources": [], "answer": "", "done": None, "events": []}
    async with client.stream(
        "POST",
        f"/api/assistant/threads/{thread_id}/messages",
        json={"content": question},
        headers=csrf(client),
    ) as resp:
        assert resp.status_code == 200, await resp.aread()
        assert resp.headers["content-type"].startswith("text/event-stream")
        event = None
        async for line in resp.aiter_lines():
            if line.startswith("event: "):
                event = line[7:]
            elif line.startswith("data: "):
                data = json.loads(line[6:])
                out["events"].append(event)
                if event == "sources":
                    out["sources"] = data["sources"]
                    out["intent"] = data["intent"]
                elif event == "token":
                    out["answer"] += data["t"]
                elif event == "done":
                    out["done"] = data
    return out


async def new_thread(client: httpx.AsyncClient) -> str:
    resp = await client.post("/api/assistant/threads", json={}, headers=csrf(client))
    assert resp.status_code == 201
    return resp.json()["id"]


def test_chunking_respects_pages_and_size():
    long = "\n".join(f"line {i} " + "x" * 60 for i in range(30))
    chunks = chunk_pages([(1, long), (2, "short page")])
    assert all(len(c) <= 760 for _, c in chunks)
    assert chunks[-1] == (2, "short page")
    assert {p for p, _ in chunks} == {1, 2}


def test_intent_classification():
    assert classify("Should I stop taking metformin?") == "advice"
    assert classify("Can I double my dose of ibuprofen?") == "advice"
    assert classify("What medications am I on?") == "meds"
    assert classify("When is my follow-up with Dr. Oduya?") == "lookup"
    assert keywords("How often should I take the Amoxicillin?") == ["often", "amoxicillin"]


async def test_answers_are_grounded_and_cited(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    tid = await new_thread(client)
    result = await ask(client, tid, "How often do I take Amoxicillin?")
    assert result["events"][0] == "sources"
    assert result["events"][-1] == "done"
    assert any(s["kind"] == "record" and "Amoxicillin" in s["title"] for s in result["sources"])
    assert "twice daily at 8:00 AM and 8:00 PM" in result["answer"]
    assert "[1]" in result["answer"]
    assert result["done"]["citations"], "cited sources are persisted with the message"

    detail = (await client.get(f"/api/assistant/threads/{tid}")).json()
    assert [m["role"] for m in detail["messages"]] == ["user", "assistant"]
    assert detail["title"].startswith("How often do I take Amoxicillin")


async def test_document_text_is_searchable(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    tid = await new_thread(client)
    result = await ask(client, tid, "What did the lipid panel say about LDL cholesterol?")
    doc_sources = [s for s in result["sources"] if s["kind"] == "document"]
    assert doc_sources, "full-text retrieval should find the lab report"
    assert any("LDL" in s["snippet"] for s in doc_sources)
    assert "LDL" in result["answer"]


async def test_lists_current_medications(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    tid = await new_thread(client)
    result = await ask(client, tid, "What medications am I currently taking?")
    assert result["intent"] == "meds"
    for name in ("Amoxicillin", "Metformin", "Atorvastatin"):
        assert name in result["answer"]
    assert "Doxycycline" not in result["answer"]  # completed course


async def test_refuses_medical_advice(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    tid = await new_thread(client)
    result = await ask(client, tid, "Should I stop taking Metformin?")
    assert result["intent"] == "advice"
    assert "can't give medical advice" in result["answer"]
    assert "Metformin" in result["answer"]


async def test_unknown_topics_say_not_found(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    tid = await new_thread(client)
    result = await ask(client, tid, "What was my last eye exam prescription?")
    assert "couldn't find that in your records" in result["answer"]


async def test_retrieval_never_crosses_users(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")  # user A has rich records
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={
                "email": "eve@example.com",
                "password": "long-enough-pass",
                "display_name": "Eve",
            },
        )
        tid = await new_thread(other)
        result = await ask(other, tid, "What did the lipid panel say about LDL cholesterol?")
        assert result["sources"] == []
        assert "couldn't find" in result["answer"]
        # And A's thread is invisible to B.
        threads = (await other.get("/api/assistant/threads")).json()
        assert [t["id"] for t in threads] == [tid]
