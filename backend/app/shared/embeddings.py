"""Embedding port (ADR-004): local fastembed in production, a deterministic hasher offline."""

from __future__ import annotations

import asyncio
import hashlib
import math
import re
from functools import lru_cache
from typing import Protocol

from app.core.config import get_settings

_TOKEN = re.compile(r"[a-z0-9]+")


class Embedder(Protocol):
    dim: int

    async def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    async def embed_query(self, text: str) -> list[float]: ...


class HashEmbedder:
    """Feature-hashing embedder (words + character trigrams). Deterministic, dependency-free.

    Not semantic, but lexically meaningful: good enough for tests and keyless demos, and the
    hybrid retriever's full-text leg carries most of the weight in that mode anyway.
    """

    def __init__(self, dim: int) -> None:
        self.dim = dim

    def _vec(self, text: str) -> list[float]:
        v = [0.0] * self.dim
        words = _TOKEN.findall(text.lower())
        feats = words + [w[i : i + 3] for w in words if len(w) > 3 for i in range(len(w) - 2)]
        for f in feats:
            h = int.from_bytes(hashlib.blake2b(f.encode(), digest_size=8).digest(), "big")
            v[h % self.dim] += 1.0 if (h >> 63) & 1 else -1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norm for x in v]

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._vec(t) for t in texts]

    async def embed_query(self, text: str) -> list[float]:
        return self._vec(text)


class FastEmbedEmbedder:
    """BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and is cached."""

    def __init__(self, model: str, dim: int) -> None:
        self.model_name = model
        self.dim = dim
        self._model = None
        self._lock = asyncio.Lock()

    async def _get(self):
        async with self._lock:
            if self._model is None:
                from fastembed import TextEmbedding

                self._model = await asyncio.to_thread(TextEmbedding, self.model_name)
        return self._model

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        model = await self._get()
        vectors = await asyncio.to_thread(lambda: list(model.passage_embed(texts)))
        return [v.tolist() for v in vectors]

    async def embed_query(self, text: str) -> list[float]:
        model = await self._get()
        vectors = await asyncio.to_thread(lambda: list(model.query_embed([text])))
        return vectors[0].tolist()


async def warm_up() -> None:
    """Load (and on first run, download) the embedding model before the first request needs it."""
    import logging

    try:
        await get_embedder().embed_query("warm up")
    except Exception:
        logging.getLogger("medspace.embeddings").warning("embedding warm-up failed", exc_info=True)


@lru_cache
def get_embedder() -> Embedder:
    s = get_settings()
    if s.embedding_provider == "fastembed":
        return FastEmbedEmbedder(s.embedding_model, s.embedding_dim)
    return HashEmbedder(s.embedding_dim)
