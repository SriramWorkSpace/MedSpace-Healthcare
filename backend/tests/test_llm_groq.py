"""Groq (LLM_PROVIDER=groq) with Groq's HTTP API mocked.

The rest of the suite runs offline (LLM_PROVIDER=fake). These tests drive the production
GroqProvider and the real extraction and Ask code paths against a fake Groq endpoint, checking the
requests MedSpace sends (models, structured output, reasoning settings, image batches) and how
failures surface.
"""

from __future__ import annotations

import json
import logging

import httpx
import pytest

from app.core.config import get_settings
from app.modules.assistant import service as assistant
from app.modules.extraction import prompts
from app.modules.extraction import service as extraction
from app.modules.extraction.schemas import ExtractionPayload
from app.shared import llm as llm_module
from app.shared.llm import GroqProvider, LLMError, get_llm

KEY = "gsk_test_key_never_logged"
CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
PAYLOAD = ExtractionPayload(document_type="prescription", overall_confidence=0.9).model_dump(
    mode="json"
)


def completion(content: str) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "chatcmpl-1",
            "object": "chat.completion",
            "created": 0,
            "model": "m",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
        },
    )


class FakeGroq:
    """Answers like Groq's chat completions endpoint and records every request body."""

    def __init__(self, *responses) -> None:
        self.responses = list(responses)
        self.requests: list[httpx.Request] = []

    def __call__(self, req: httpx.Request) -> httpx.Response:
        self.requests.append(req)
        nxt = self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]
        return nxt(req) if callable(nxt) else nxt

    @property
    def bodies(self) -> list[dict]:
        return [json.loads(r.content) for r in self.requests]


def provider(fake: FakeGroq) -> GroqProvider:
    return GroqProvider(KEY, http_client=httpx.AsyncClient(transport=httpx.MockTransport(fake)))


# ---- Requests MedSpace sends -------------------------------------------------------------------


async def test_text_extraction_uses_strict_schema_and_short_reasoning():
    fake = FakeGroq(completion(json.dumps(PAYLOAD)))
    result = await extraction._extract_text(provider(fake), ["Amoxicillin 500 mg ..."])
    assert result.document_type == "prescription"
    [req] = fake.requests
    assert str(req.url) == CHAT_URL
    assert req.headers["authorization"] == f"Bearer {KEY}"
    body = fake.bodies[0]
    assert body["model"] == get_settings().groq_text_model == "openai/gpt-oss-120b"
    assert body["response_format"]["type"] == "json_schema"
    assert body["response_format"]["json_schema"]["strict"] is True
    assert body["response_format"]["json_schema"]["schema"] == prompts.EXTRACTION_SCHEMA
    assert body["reasoning_effort"] == "low"
    assert body["temperature"] == 0


async def test_vision_uses_qwen_in_instruct_mode_with_at_most_three_images():
    import pymupdf

    doc = pymupdf.open()
    for _ in range(4):
        doc.new_page(width=300, height=400)  # no text layer: a "scan"
    fake = FakeGroq(completion(json.dumps(PAYLOAD)))
    result = await extraction._extract_vision(provider(fake), doc.tobytes(), "application/pdf")
    assert result.document_type == "prescription"
    assert len(fake.requests) == 2  # 4 pages -> batches of 3 and 1
    for body in fake.bodies:
        assert body["model"] == get_settings().groq_vision_model == "qwen/qwen3.8-27b"
        assert body["reasoning_effort"] == "none"  # no thinking text before the JSON
        images = [part for part in body["messages"][-1]["content"] if part["type"] == "image_url"]
        assert 1 <= len(images) <= 3
        assert all(i["image_url"]["url"].startswith("data:image/png;base64,") for i in images)


def test_reasoning_settings_per_model_family():
    assert GroqProvider._reasoning_kwargs("openai/gpt-oss-120b") == {"reasoning_effort": "low"}
    assert GroqProvider._reasoning_kwargs("qwen/qwen3.8-27b") == {"reasoning_effort": "none"}
    assert GroqProvider._reasoning_kwargs("llama-3.3-70b-versatile") == {}


async def test_reasoning_preamble_around_json_is_tolerated():
    fake = FakeGroq(completion("Here is the result:\n```json\n" + json.dumps(PAYLOAD) + "\n```"))
    raw = await provider(fake).complete_json(model="openai/gpt-oss-120b", messages=[], schema={})
    assert raw["document_type"] == "prescription"


# ---- Failures ----------------------------------------------------------------------------------


def bad_request() -> httpx.Response:
    return httpx.Response(400, json={"error": {"message": "schema not supported"}})


async def test_rejected_strict_schema_falls_back_to_json_mode(caplog):
    fake = FakeGroq(bad_request(), completion(json.dumps(PAYLOAD)))
    raw = await provider(fake).complete_json(
        model="qwen/qwen3.8-27b", messages=[], schema=prompts.EXTRACTION_SCHEMA
    )
    assert raw["document_type"] == "prescription"
    assert [b["response_format"]["type"] for b in fake.bodies] == ["json_schema", "json_object"]
    assert "falling back to json_object" in caplog.text


async def test_a_failing_fallback_raises_llm_error_not_a_raw_sdk_error():
    fake = FakeGroq(bad_request(), bad_request())
    with pytest.raises(LLMError):
        await provider(fake).complete_json(model="m", messages=[], schema={"type": "object"})


@pytest.mark.parametrize("status", [401, 404, 413])
async def test_api_errors_become_llm_errors_without_the_key(status, caplog):
    caplog.set_level(logging.DEBUG)
    fake = FakeGroq(httpx.Response(status, json={"error": {"message": "nope"}}))
    with pytest.raises(LLMError):
        await provider(fake).complete_json(model="m", messages=[])
    assert KEY not in caplog.text


async def test_non_json_reply_is_an_llm_error():
    fake = FakeGroq(completion("I can't help with that."))
    with pytest.raises(LLMError):
        await provider(fake).complete_json(model="m", messages=[])


# ---- Ask MedSpace streaming --------------------------------------------------------------------


def sse(*deltas: dict) -> httpx.Response:
    chunks = [
        {
            "id": "c",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": "m",
            "choices": [{"index": 0, "delta": d, "finish_reason": None}],
        }
        for d in deltas
    ]
    body = "".join(f"data: {json.dumps(c)}\n\n" for c in chunks) + "data: [DONE]\n\n"
    return httpx.Response(200, text=body, headers={"content-type": "text/event-stream"})


async def test_streaming_yields_only_answer_text():
    fake = FakeGroq(
        sse(
            {"role": "assistant", "reasoning": "thinking..."},
            {"content": "LDL "},
            {"content": "is 162 [1]."},
        )
    )
    out = [d async for d in provider(fake).stream_text(model="openai/gpt-oss-120b", messages=[])]
    assert "".join(out) == "LDL is 162 [1]."
    assert fake.bodies[0]["stream"] is True
    assert fake.bodies[0]["reasoning_effort"] == "low"


async def test_a_failed_stream_falls_back_to_the_offline_answer(monkeypatch):
    fake = FakeGroq(httpx.Response(503, json={"error": {"message": "over capacity"}}))
    groq = provider(fake)
    groq.client = groq.client.with_options(max_retries=0)
    monkeypatch.setattr(assistant, "get_llm", lambda: groq)
    source = assistant.Source(
        n=1,
        kind="document",
        title="Lipid profile",
        page_no=1,
        snippet="LDL 162 mg/dL",
        document_id="d1",
        confirmed=True,
        text="Lipid profile. LDL cholesterol 162 mg/dL (high).",
    )
    text = "".join(
        [d async for d in assistant.answer_stream("What is my LDL?", "general", [source], [])]
    )
    assert text.strip()  # the visitor still gets an answer, built offline from the sources


# ---- Provider selection ------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("provider_name", "key", "expected"),
    [("groq", KEY, "groq"), ("groq", None, None), ("fake", KEY, None)],
)
def test_get_llm_selects_groq_only_with_a_key(monkeypatch, provider_name, key, expected):
    s = get_settings()
    monkeypatch.setattr(s, "llm_provider", provider_name)
    monkeypatch.setattr(s, "groq_api_key", type(s.jwt_secret)(key) if key else None)
    get_llm.cache_clear()
    try:
        chosen = get_llm()
        assert (chosen.name if chosen else None) == expected
    finally:
        get_llm.cache_clear()


def test_offline_default_is_kept_in_tests():
    assert llm_module.get_settings().llm_provider == "fake"


# ---- Answer formatting -------------------------------------------------------------------------

LB, RB, DAGGER = "【", "】", "†"  # the model's citation brackets and dagger


def test_model_citation_styles_become_square_brackets_across_chunks():
    n = assistant.CitationNormalizer()
    chunks = ["Low-salt diet ", LB, "1", RB + LB + "6" + DAGGER + "L3", "-L5" + RB, " and [2]."]
    assert "".join(n.feed(c) for c in chunks) == "Low-salt diet [1][6] and [2]."


def test_ordinary_brackets_are_left_alone():
    n = assistant.CitationNormalizer()
    text = "Dose [a]: take 1 [2] then see array[0] and [x" + DAGGER + "y]"
    assert n.feed(text) == text


def test_grouped_citations_count():
    def src(i):
        return assistant.Source(
            n=i, kind="record", title=f"S{i}", page_no=1, snippet="", document_id=None,
            confirmed=True, text="",
        )  # fmt: skip

    cited = assistant.used_citations("A [1, 3] and B [2]", [src(1), src(2), src(3), src(4)])
    assert [c["n"] for c in cited] == [1, 2, 3]


def test_the_prompt_asks_for_plain_text_and_square_bracket_citations():
    assert "No Markdown" in assistant.SYSTEM_PROMPT
    assert "[2] or [1][3]" in assistant.SYSTEM_PROMPT


async def test_streamed_answer_reaches_the_visitor_normalized(monkeypatch):
    fake = FakeGroq(
        sse(
            {"content": "Low-salt diet " + LB + "1"},
            {"content": RB + LB + "2" + DAGGER + "L1-L2" + RB + "."},
        )
    )
    monkeypatch.setattr(assistant, "get_llm", lambda: provider(fake))
    source = assistant.Source(
        n=1, kind="record", title="Diet", page_no=1, snippet="Low salt", document_id="d1",
        confirmed=True, text="Low-salt diet.",
    )  # fmt: skip
    text = "".join([d async for d in assistant.answer_stream("Diet?", "general", [source], [])])
    assert text == "Low-salt diet [1][2]."
