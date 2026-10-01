# CLAUDE.md

Guidance for Claude Code (and humans) working in this repository.

## What this is

**MedSpace**: "Your health, all in one space." A full-stack portfolio app that turns prescription PDFs/images into structured, reviewable records and actions: **Upload → Extract → Review → Organize → Act** (Google Calendar/Tasks, timeline, source-grounded AI Q&A, secure sharing).

Synthetic data only. Never add diagnosis, treatment, or dose-change features.

## Read first (context recovery)

When context is lost or a task touches unfamiliar areas, read in this order:
1. `graphify-out/GRAPH_REPORT.md` or `graphify query "<question>"` (cheapest way to orient; see the graphify section below)
2. `docs/plan.md`: what phase we are in and what is done
3. `docs/architecture.md`: modules, flows, data model, API surface
4. `docs/decisions.md`: why things are the way they are (ADRs)

## Stack

- **Backend:** Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async, asyncpg), Alembic, PostgreSQL 17 + pgvector, Redis + ARQ worker, S3-compatible storage (SeaweedFS in dev), Groq (LLM), fastembed (local embeddings), PyMuPDF.
- **Frontend:** React 19 + Vite, **JavaScript/JSX (not TypeScript, ADR-011)**, React Router, TanStack Query, React Hook Form + Zod, Tailwind v4 + hand-authored CSS tokens (ADR-012), `motion/react`, Phosphor icons, Sonner, Geist font.
- **Infra:** Docker Compose, GitHub Actions.

## Commands

```bash
# Full stack (from repo root)
docker compose up --build            # web :5173, api :8000, S3 :8333

# Backend (from backend/)
python -m venv .venv && .venv/Scripts/activate   # Windows; use bin/activate on *nix
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
arq app.worker.WorkerSettings        # only when QUEUE_MODE=arq
pytest                                # needs Postgres (docker compose up postgres)
ruff check . && ruff format --check .

# Frontend (from frontend/)
npm install
npm run dev
npm run lint
npm test
npm run build
```

## Backend conventions

- Modules live in `backend/app/modules/<name>/` with `models.py`, `schemas.py`, `service.py`, `router.py`, optional `jobs.py`.
- **Cross-module rule:** import another module's `service.py` / `schemas.py` only. Never import another module's router or private helpers.
- Routers stay thin: validate → call service → return schema. Business logic lives in services.
- Every user-owned table has `user_id`; every query filters by it. Load resources with `(id, user_id)` so foreign IDs return 404.
- External services go through ports in `app/shared/` (`llm`, `embeddings`, `storage`, `queue`) and Google's client in `integrations`. Every port has a fake adapter; tests and demo never need real keys.
- Security-relevant actions call `audit.service.record(...)`.
- Errors: raise `AppError` subclasses from `app/core/errors.py`; they render as `application/problem+json`.
- New tables → Alembic migration (`alembic revision --autogenerate -m "..."`), review the generated file.
- Tests: `pytest` with real Postgres; use fakes for LLM/embeddings/storage/Google. Add tests with every service change.

## Frontend conventions

- Feature code in `src/features/<domain>/` (api hooks + components); route components in `src/pages/`; shared primitives in `src/components/ui/`.
- Server state via TanStack Query only (query-key factories in each feature's `api.js`). No server data in global stores.
- Design tokens in `src/styles/tokens.css` (exposed to Tailwind via `@theme`). Do not hardcode colors; use tokens/utilities.
- Every data view ships **loading (skeleton shaped like the final layout), empty, and error states**.
- Animations: `motion/react`, transform/opacity only, respect `useReducedMotion()`. No scroll listeners; use `whileInView`/`useScroll`.
- Icons: Phosphor only. No emoji in UI.
- **UI copy:** no em-dashes (use periods, commas, colons). No "seamless/elevate/unleash/revolutionize" filler.
- Accessibility: labels above inputs, visible focus rings, keyboard-reachable everything, WCAG AA contrast in both themes.
- Easter eggs and puns live in `src/easter-eggs/`; keep them tasteful and never in error messages that block the user.

## Docs discipline

- Finished a plan item → tick it in `docs/plan.md`.
- Changed architecture, a dependency, or a plan decision → add an ADR to `docs/decisions.md` and update `docs/architecture.md`.
- After significant code changes: `graphify update .` (AST-only, free) so the graph stays current.

## Git

- Remote: `https://github.com/SriramWorkSpace/MedSpace-Healthcare.git`, branch `main`.
- Commit as the repository owner's configured git identity. **Do not add `Co-Authored-By` trailers, "Generated with" lines, or any AI attribution to commits or PRs.**
- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`), one logical change per commit.
- Never commit `.env`, credentials, or real health data.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
