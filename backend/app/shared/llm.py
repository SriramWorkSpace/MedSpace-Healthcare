"""LLM port and the Groq adapter (ADR-003).

When `LLM_PROVIDER=fake` (the default) `get_llm()` returns None and callers use their offline
strategy (heuristic extraction, extractive answers). That keeps CI and the demo keyless.
"""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Any, Protocol

from app.core.config import get_settings

logger = logging.getLogger("medspace.llm")


class LLMError(Exception):
    pass


class LLMProvider(Protocol):
    name: str

    async def complete_json(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        schema: dict[str, Any] | None = None,
        schema_name: str = "result",
    ) -> dict[str, Any]: ...

    def stream_text(
        self, *, model: str, messages: list[dict[str, Any]], temperature: float = 0.2
    ) -> AsyncIterator[str]: ...


def _parse_json(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{") :]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise LLMError("Model did not return JSON.")
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise LLMError(f"Model returned invalid JSON: {exc}") from exc


class GroqProvider:
    name = "groq"

    def __init__(self, api_key: str, http_client: Any = None) -> None:
        from groq import AsyncGroq

        # http_client: tests pass an httpx client with a mocked transport.
        self.client = AsyncGroq(api_key=api_key, max_retries=2, timeout=90, http_client=http_client)

    @staticmethod
    def _reasoning_kwargs(model: str) -> dict[str, Any]:
        # gpt-oss models always reason before answering: keep it short. Qwen 3.x models think by
        # default, which slows extraction and can leak reasoning into the JSON; "none" switches them
        # to instruct mode.
        if "gpt-oss" in model:
            return {"reasoning_effort": "low"}
        if "qwen" in model:
            return {"reasoning_effort": "none"}
        return {}

    async def complete_json(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        schema: dict[str, Any] | None = None,
        schema_name: str = "result",
    ) -> dict[str, Any]:
        from groq import BadRequestError

        kwargs: dict[str, Any] = {"model": model, "messages": messages, "temperature": 0}
        kwargs.update(self._reasoning_kwargs(model))
        if schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": schema_name, "strict": True, "schema": schema},
            }
        else:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            resp = await self.client.chat.completions.create(**kwargs)
        except BadRequestError as exc:
            if schema is None:
                raise LLMError(str(exc)) from exc
            # Strict schemas are model-dependent; degrade to JSON mode + Pydantic validation.
            logger.warning("strict schema rejected by %s, falling back to json_object", model)
            kwargs["response_format"] = {"type": "json_object"}
            try:
                resp = await self.client.chat.completions.create(**kwargs)
            except Exception as retry_exc:  # callers handle LLMError, never raw SDK errors
                raise LLMError(f"LLM request failed: {retry_exc}") from retry_exc
        except Exception as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc
        return _parse_json(resp.choices[0].message.content or "")

    async def stream_text(
        self, *, model: str, messages: list[dict[str, Any]], temperature: float = 0.2
    ) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True,
                **self._reasoning_kwargs(model),
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    yield delta
        except Exception as exc:
            raise LLMError(f"LLM stream failed: {exc}") from exc


@lru_cache
def get_llm() -> LLMProvider | None:
    settings = get_settings()
    if settings.llm_provider == "groq":
        key = settings.groq_api_key.get_secret_value() if settings.groq_api_key else ""
        if not key:
            logger.warning("LLM_PROVIDER=groq but GROQ_API_KEY is empty; using offline mode")
            return None
        return GroqProvider(key)
    return None
