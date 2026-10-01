FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml ./
RUN mkdir -p app && touch app/__init__.py \
 && pip install ".[embeddings,dev]" \
 && rm -rf app build *.egg-info

COPY . .
RUN pip install --no-deps -e .

RUN useradd --create-home --uid 10001 medspace && mkdir -p /cache && chown -R medspace /app /cache
USER medspace

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
