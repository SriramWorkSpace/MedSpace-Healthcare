# MedSpace Build Plan

Phase-by-phase record of the build. Each phase ends in a **working, demoable, committed state**. Tick boxes as work lands; add a dated note under the phase when scope changes (and an ADR in [decisions.md](decisions.md) if it is architectural).

Legend: `[ ]` todo · `[x]` done · `[~]` partial / deferred (with note)

---

## Phase 0: Foundations

Goal: repo, docs, tooling and local infrastructure that every later phase builds on.

- [x] Plan review, critical changes identified (see ADR-002 to ADR-010)
- [x] `CLAUDE.md`, `README.md`, `docs/architecture.md`, `docs/decisions.md`, `docs/plan.md`
- [x] Monorepo layout: `backend/`, `frontend/`, `docs/`
- [x] `docker-compose.yml`: postgres (pgvector), redis, minio (+ bucket init), api, worker, web
- [x] `.env.example` with every setting documented
- [x] Backend tooling: `pyproject.toml`, ruff, pytest config
- [x] Frontend tooling: Vite, ESLint, Prettier, Vitest
- [x] GitHub Actions CI: backend lint+test, frontend lint+test+build
- [ ] graphify knowledge graph of the repo (`graphify-out/`)

## Phase 1: Core platform + design system

Goal: a user can sign up, log in (or "Try the demo"), and land in a polished, empty app shell. The marketing site is complete.

Backend
- [x] App factory, settings (pydantic-settings), structured logging, problem+json errors
- [x] Async SQLAlchemy 2.0 + Alembic, base model mixins (UUID PK, timestamps)
- [x] `identity`: signup/login/logout/me, Argon2id, JWT access cookie, rotating refresh with reuse detection, CSRF
- [x] `audit`: `record()` helper + `GET /api/audit`
- [x] Rate limiting on auth routes
- [x] Security headers middleware, CORS for the SPA origin
- [x] Health/readiness endpoints
- [x] Tests: auth flows, refresh rotation + reuse detection, CSRF enforcement

Frontend
- [x] Design tokens (light/dark), typography, Tailwind v4 `@theme` bridge
- [~] UI primitives: Button, Field/Input, Chip, Skeleton, Dialog, MobileDrawer, EmptyState, Toaster done; Tabs/Tooltip added when first needed
- [x] Top navigation (desktop bar + mobile drawer), theme toggle, user menu
- [x] Marketing landing: hero with live document-to-schedule morph, workflow, feature bento, AI section, trust/privacy, CTA, footer
- [x] Auth pages with validation, error states, demo login
- [x] API client (cookies + CSRF + refresh-on-401 queue), TanStack Query setup, route guards
- [~] Skeleton screens: app shell + generic page skeleton done; shaped skeletons ship with each feature page
- [x] Easter eggs v1: rotating health puns in loaders, 404 pun page, Konami-code apple rain, logo-click apple
- [~] Reduced-motion and keyboard/focus: global reduced-motion, MotionConfig, focus rings, dialog focus trap, skip links; full audit in Phase 8

## Phase 2: Documents + processing pipeline

Goal: drag-and-drop a prescription and watch it process to "needs review".

- [ ] `shared/storage`: S3 (MinIO) + local adapters
- [ ] `shared/queue`: ARQ + inline modes; `worker.py`
- [ ] `documents`: upload validation (MIME, magic bytes, size, pages), dedupe by sha256, list/detail/delete, authenticated file streaming
- [ ] Page text extraction (PyMuPDF) and scanned detection
- [ ] Frontend: dropzone with progress, library grid/list, status chips with live polling, processing skeletons with puns
- [ ] Tests: upload validation, ownership isolation, status transitions

## Phase 3: Prescription intelligence (extract → review → confirm)

Goal: the core loop. A user reviews AI-extracted fields against the source and confirms them.

- [ ] `shared/llm`: `LLMProvider`, `GroqProvider` (text strict-schema, vision JSON), `FakeLLM`
- [ ] Extraction schema + prompts, repair retry, confidence + source page per field
- [ ] Frequency normalizer (`1-0-1`, BD/BID, TDS/TID, QID, OD/QD, HS, qNh, weekly, PRN) with table-driven tests
- [ ] `extractions` versioning, reprocess
- [ ] `records`: confirm → prescriptions, medications, care actions; edit medication; discard draft
- [ ] Prescription report endpoint + printable report page
- [ ] Frontend review workspace: source preview (PDF/image) ↔ editable fields, low-confidence highlighting, schedule editor, confirm flow with celebration micro-interaction
- [ ] Synthetic sample prescriptions (PDF text + scanned image) in `backend/app/modules/demo/samples/`

## Phase 4: Dashboard, medications, timeline

- [ ] `GET /api/dashboard`: today's doses, next follow-up, needs-review queue, counts
- [ ] Medications page: active/completed, schedule visualization, course progress
- [ ] `timeline`: cursor-paginated union read model with type filters
- [ ] Frontend timeline with sticky month headers, filter chips, scroll-reveal
- [ ] Demo seed: realistic synthetic history (3 to 4 prescriptions over months, a lab report, follow-ups)

## Phase 5: Ask MedSpace (RAG)

- [ ] `shared/embeddings`: fastembed + hash adapters
- [ ] Chunking (page-aware, overlap) + embedding job after extraction
- [ ] Hybrid retrieval: pgvector HNSW + tsvector GIN, RRF fusion, `user_id` scoping
- [ ] Grounded prompt with numbered sources + guardrails; SSE streaming; citations persisted
- [ ] Frontend chat: streaming tokens, citation chips that open the source page, suggested questions, thread history
- [ ] Tests: retrieval isolation between users, refusal of diagnosis/dose-change requests, "not in your records" path

## Phase 6: Google Calendar + Tasks

- [ ] OAuth connect/callback/disconnect with state + PKCE, encrypted token storage, refresh handling
- [ ] Calendar: recurring dose events, appointments, follow-ups; idempotent upsert via `sync_links`
- [ ] Tasks: "MedSpace" task list, care actions as tasks, completion sync back
- [ ] Unsync/edit propagation; graceful handling of revoked consent
- [ ] Frontend: integrations settings card, per-prescription "Sync" sheet with preview of events/tasks
- [ ] `FakeGoogleClient` + tests

## Phase 7: Secure sharing + audit UI

- [ ] `sharing`: create (scoped items, expiry, max views), list, revoke; hashed tokens
- [ ] Public share endpoints + public share page `/s/:token` (read-only report + documents)
- [ ] Audit log viewer in settings (filterable)
- [ ] Expiry sweep job
- [ ] Tests: expired/revoked/over-limit links, scope enforcement, audit rows written

## Phase 8: Hardening + launch

- [ ] Playwright e2e: demo login → upload → review → confirm → ask → share
- [ ] Accessibility pass (axe), Lighthouse ≥ 90 across categories on landing + dashboard
- [ ] Error boundaries, offline/slow-network states, toasts for transient failures
- [ ] Account data export + delete account
- [ ] Production Dockerfiles (multi-stage), deployment guide, screenshots/GIF in README
- [ ] Final graphify update and docs sync

---

## Change log

- **2026-10-01**: Phase 1 shipped. Added `GET /api/auth/session` (quiet anonymous boot) and a same-origin API proxy (ADR-014).

- **2026-10-01**: Plan created from the original brief. Changes vs brief: pgvector replaces FAISS (ADR-002); Groq with dual text/vision extraction (ADR-003); local embeddings (ADR-004); Calendar vs Tasks split (ADR-005); deterministic schedule normalization (ADR-006); ARQ queue (ADR-007); own auth + optional Google (ADR-008); draft→confirmed lifecycle (ADR-009); proxied share links (ADR-010).
