FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/cache/hf \
    FASTEMBED_CACHE_PATH=/cache/fastembed

# Production installs only what runs; docker-compose adds the dev tools (EXTRAS=embeddings,dev).
ARG EXTRAS=embeddings

WORKDIR /app

COPY pyproject.toml ./
RUN mkdir -p app && touch app/__init__.py \
 && pip install ".[${EXTRAS}]" \
 && rm -rf app build *.egg-info

COPY . .
RUN pip install --no-deps -e .

# Bake the embedding model into the image: hosts with ephemeral disks (Render's free plan) would
# otherwise download it on every start, and a start would fail whenever the download does.
RUN python -c "from fastembed import TextEmbedding; TextEmbedding('BAAI/bge-small-en-v1.5')"

RUN useradd --create-home --uid 10001 medspace && mkdir -p /cache && chown -R medspace /app /cache
USER medspace

EXPOSE 8000
# Migrate, then serve on the host's $PORT (Render sets it; 8000 otherwise). Client IPs come from
# TRUSTED_PROXY_HOPS (ADR-027), not uvicorn's proxy headers; the access log stays off because it
# would record share-link tokens (ADR-035).
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --no-proxy-headers --no-access-log"]
