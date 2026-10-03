# MedSpace Build Plan

Phase-by-phase record of the build. Each phase ends in a **working, demoable, committed state**. Tick boxes as work lands; add a dated note under the phase when scope changes (and an ADR in [decisions.md](decisions.md) if it is architectural).

Legend: `[ ]` todo · `[x]` done · `[~]` partial / deferred (with note)

---

## Phase 0: Foundations

Goal: repo, docs, tooling and local infrastructure that every later phase builds on.

- [x] Plan review, critical changes identified (see ADR-002 to ADR-010)
- [x] `CLAUDE.md`, `README.md`, `docs/architecture.md`, `docs/decisions.md`, `docs/plan.md`
- [x] Monorepo layout: `backend/`, `frontend/`, `docs/`
- [x] `docker-compose.yml`: postgres (pgvector), redis, s3 (SeaweedFS, replaced MinIO per ADR-016), api, worker, web
- [x] `.env.example` with every setting documented
- [x] Backend tooling: `pyproject.toml`, ruff, pytest config
- [x] Frontend tooling: Vite, ESLint, Prettier, Vitest
- [x] GitHub Actions CI: backend lint+test, frontend lint+test+build
- [x] graphify knowledge graph of the repo (`graphify-out/`)

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

- [x] `shared/storage`: S3 (SeaweedFS locally, R2/S3 in prod) + local adapters
- [x] `shared/queue`: ARQ + inline modes; `worker.py`
- [x] `documents`: upload validation (MIME, magic bytes, size, pages), dedupe by sha256, list/detail/delete, authenticated file streaming
- [x] Page text extraction (PyMuPDF) and scanned detection
- [x] Frontend: dropzone with progress, library grid/list, status chips with live polling, processing skeletons with puns
- [x] Tests: upload validation, ownership isolation, status transitions

## Phase 3: Prescription intelligence (extract → review → confirm)

Goal: the core loop. A user reviews AI-extracted fields against the source and confirms them.

- [x] `shared/llm`: `LLMProvider`, `GroqProvider` (text strict-schema, vision JSON), `FakeLLM`
- [x] Extraction schema + prompts, repair retry, confidence + source page per field
- [x] Frequency normalizer (`1-0-1`, BD/BID, TDS/TID, QID, OD/QD, HS, qNh, weekly, PRN) with table-driven tests
- [x] `extractions` versioning, reprocess
- [x] `records`: confirm → prescriptions, medications, care actions; edit medication; discard draft
- [x] Printable prescription report (rendered from `GET /prescriptions/{id}`; print stylesheet)
- [x] Frontend review workspace: source preview (PDF/image) ↔ editable fields, low-confidence highlighting, schedule editor, confirm flow with celebration micro-interaction
- [x] Synthetic sample prescriptions (PDF text + scanned image) in `backend/app/modules/demo/samples/`

## Phase 4: Dashboard, medications, timeline

- [x] `GET /api/dashboard`: today's doses, next follow-up, needs-review queue, counts
- [x] Medications page: active/completed, schedule visualization, course progress
- [x] `timeline`: cursor-paginated union read model with type filters
- [x] Frontend timeline with sticky month headers, filter chips, scroll-reveal
- [x] Demo seed: realistic synthetic history (3 to 4 prescriptions over months, a lab report, follow-ups)

## Phase 5: Ask MedSpace (RAG)

- [x] `shared/embeddings`: fastembed + hash adapters
- [x] Chunking (page-aware, overlap) + embedding job after extraction
- [x] Hybrid retrieval: pgvector HNSW + tsvector GIN, RRF fusion, `user_id` scoping
- [x] Grounded prompt with numbered sources + guardrails; SSE streaming; citations persisted
- [x] Frontend chat: streaming tokens, citation chips that open the source page, suggested questions, thread history
- [x] Tests: retrieval isolation between users, refusal of diagnosis/dose-change requests, "not in your records" path

## Phase 6: Google Calendar + Tasks

- [x] OAuth connect/callback/disconnect with state + PKCE, encrypted token storage, refresh handling
- [x] Calendar: recurring dose events, appointments, follow-ups; idempotent upsert via `sync_links`
- [x] Tasks: "MedSpace" task list, care actions as tasks, completion sync back
- [x] Unsync/edit propagation; graceful handling of revoked consent
- [x] Frontend: integrations settings card, per-prescription "Sync" sheet with preview of events/tasks
- [x] `FakeGoogleClient` + tests

## Phase 7: Secure sharing + audit UI

- [x] `sharing`: create (scoped items, expiry, max views), list, revoke; hashed tokens
- [x] Public share endpoints + public share page `/s/:token` (read-only report + documents)
- [x] Audit log viewer in settings (filterable)
- [x] Expiry sweep job
- [x] Tests: expired/revoked/over-limit links, scope enforcement, audit rows written

## Phase 8: Hardening + launch

- [x] Playwright e2e: demo login → upload → review → confirm → ask → share (12 tests, desktop + mobile, in CI)
- [x] Accessibility pass: axe WCAG 2.1 AA in e2e (landing, login dark, review, dashboard); token contrast fixed. [~] Lighthouse run not yet recorded
- [x] Route error boundary, retry states on every data view, toasts for transient failures, storage outages as 503
- [x] Account data export (`GET /api/me/export`, secrets excluded) and delete account with file purge
- [x] Multi-stage web image (nginx + /api proxy), deployment guide (docs/deployment.md), README screenshots
- [x] Final graphify update and docs sync

## Phase 16: Care circle (caregiver access)

- [x] `care_links` table and `circle` module: email-bound one-time invitations (hashed, 7-day expiry), accept, change role, revoke or leave (ADR-026)
- [x] Central access check: `X-Acting-For` resolved in `get_current_user`; role allow-lists (viewer reads; helper also ticks doses, completes to-dos, updates supply); everything else refused; personal routes ignore the header
- [x] Helper changes audited in the owner's activity log
- [x] Frontend: Care circle settings (invite, copy link, roles, remove, leave), accept page, profile switcher in the account menu, acting banner, role-aware UI, auto switch-back on revocation, no offline copy while acting
- [x] Demo: every demo account helps a fictional family member with her own records
- [x] Tests: 6 backend (flow, roles, audit, out-of-bounds routes, one-time email-bound invites, revocation, demo), 2 e2e (with axe)

## Phase 15: Installable app and offline access

- [x] Web app manifest, icons (any + maskable, generated from the favicon by `scripts/icons.mjs`), shortcuts (ADR-025)
- [x] Build-time service worker: versioned precache of every built asset, network-first navigations with an offline app shell, never touches `/api`
- [x] Opt-in offline copy per device (Settings, This device): IndexedDB snapshot via `dehydrate`, restored before render, 7-day expiry, per user, cleared on sign-out and session expiry
- [x] Dose ticks made offline persist and sync on reconnect; offline banner with saved time and pending ticks; offline screen instead of a login redirect
- [x] Install button from the browser's install prompt; standalone detection
- [x] Fixed on the way: `formatDate` crashed on epoch timestamps; the app started "online" when loaded offline
- [x] Tests: 1 unit, 1 e2e against the production build (offline reload, queued tick across reload, sync, sign-out clears the copy)

## Phase 14: Extraction evaluation

- [x] Labelled corpus generator: six prescription layouts, shorthand, duration and date styles, follow-ups, investigations, diet, three lab layouts; rendered through real PDFs (ADR-024)
- [x] Field-level scorer with per-metric, per-tag and failure reports; CLI `python -m app.eval` (JSON + Markdown)
- [x] Regression set gated in CI (thresholds.json); held-out stress set; Groq provider supported
- [x] Extractor fixes driven by the results: `Sig:` lines, day-first numeric dates with ambiguity warnings, ISO dates, chest X-ray, bracketed brands, ALL-CAPS names, word frequencies and durations, "come back after" follow-ups
- [x] Held-out baseline 92.5% (regression set 96.2%) before fixes; both 100% after (see docs/evaluation.md for the caveat)
- [x] Tests: 7 (corpus determinism, scorer, thresholds, each fix)

## Phase 13: Medication supply and refills

- [x] `medication_supplies` table and `supply` module: count, refill, stop tracking (ADR-023)
- [x] Deterministic estimate: units left from the count, schedule and skipped marks; run-out date or "covers the course"; statuses for low/out
- [x] Medication cards: supply line with Update count / Refill, or Track supply; one dialog for both
- [x] Dashboard "Running low" card with one-tap refill
- [x] Visit prep prompts and Ask MedSpace answers state supply estimates; export includes supplies
- [x] Demo: Metformin running low, Atorvastatin with a date, Amoxicillin covering its course
- [x] Tests: 8 backend (pure estimate cases, API, privacy, integrations), 2 e2e (with axe)

## Phase 12: Visit prep

- [x] `visit_preps` table and `visits` module: create, edit details and questions, delete (ADR-022)
- [x] Live brief: current medicines, changes, dose marks, lab results with previous values, open to-dos, appointments, diet notes, documents; period defaults to the previous visit or 90 days
- [x] Factual prompts from records, one click to turn into a question
- [x] Visits page (upcoming, past, quick start from upcoming appointments) and visit page (questions, prompts, details, printable brief)
- [x] Dashboard "Prepare" on appointments; sharing supports visit briefs; the public view renders them
- [x] Demo: a prep for the next follow-up with two questions
- [x] Nav fits nine links at 1024px (compact link spacing between `lg` and `xl`)
- [x] Tests: 4 backend, 1 unit, 2 e2e (with axe scans), visits in the phone overflow guard

## Phase 11: Dose tracking and history

- [x] `dose_logs` table and `doses` module: mark a scheduled dose taken or skipped, change or clear it; only scheduled doses, never a future day (ADR-021)
- [x] History read model in the user's timezone: taken / skipped / not logged / later today, counts, rate, days-in-a-row; stopped medicines keep their past
- [x] Dashboard ticks saved to the account (optimistic), a Skip action, and a one-time move of old device-only ticks
- [x] Medication cards: 14-day strip and "Taken X of Y"; per-medicine history page with a calendar and a day panel to fill in past doses
- [x] Ask MedSpace states dose-log counts; questions about what to do after a missed dose get the no-advice reply
- [x] Demo: four weeks of seeded history (mostly taken, a few skips and gaps), today left for the visitor
- [x] Tests: 6 backend, 4 unit, 2 e2e (with axe scans and a phone overflow check)

## Phase 10: Lab results and trends

- [x] Extraction: `lab_results` in the LLM schema and prompt (copy as printed, flag only when the report marks it); offline extractor reads lab tables in one-line and split name/value/range layouts and stops turning result rows into "get this test" to-dos (ADR-020)
- [x] Deterministic parsing: values, printed ranges (`< 200`, `>= 40`, `70 - 99`, `up to 5.6`), flags against the printed range, test-name synonyms (`analyte_key`)
- [x] `lab_results` table replaced on every confirmation; `GET /labs`, `GET /labs/{key}`, `DELETE /lab-results/{id}`; export includes results
- [x] Review form: a Lab results section, placed first on lab reports
- [x] Labs page (grouped by report, sparklines, direction of change) and a per-test page (trend chart with the printed range as a band, every result with its source page)
- [x] Search finds tests; Ask MedSpace cites results with their printed ranges and refuses to interpret them
- [x] Demo: five dated lab reports (three lipid panels, two diabetes panels) run through the real offline pipeline
- [x] Fixed: the app bar overflowed sideways between 768px and 1279px; links now collapse into the drawer below `lg`
- [x] Tests: 28 backend, 5 unit, 2 e2e plus tablet-width overflow checks

## Phase 9: Global search

- [x] `GET /api/search?q=`: medications and strengths, prescribers and clinics, document titles, text inside documents (prefix full-text with highlighted snippets), to-dos and diet notes, 5 per group, always scoped by `user_id` (ADR-019)
- [x] Command palette: Ctrl/Cmd+K anywhere, `/` outside inputs, a nav button; grouped results, combobox keyboard control, quick links when empty
- [x] Results deep-link: `/app/medications?focus=` opens the right tab and rings the card; document hits open on the matching page
- [x] "Ask MedSpace about …" hands the query to the assistant (`/app/ask?q=`), asked once in a new conversation
- [x] Tests: 7 backend (partial names, snippets, wildcard escaping, privacy, auth), 2 e2e (keyboard flow with axe scan, hand-over to Ask)

---

## Change log

- **2026-10-03**: Rate limiting hardened (ADR-027): fixed a spoofable client IP (`X-Forwarded-For` trusted blindly), added a baseline budget for every route, limits on AI, export, sharing and invitation endpoints, a per-account sign-in limit, per-user keys, sliding windows, `RateLimit-*` headers, explicit Redis backend, and limiter-on e2e in CI. 8 new backend tests, 1 unit test.

- **2026-10-03**: Phase 16 shipped: care circle with role-limited caregiver access (ADR-026). The access tests caught a prefix-matching bug ("/medications" treated as "/me") before release.

- **2026-10-03**: Phase 15 shipped: installable app with opt-in offline access (ADR-025).

- **2026-10-02**: Phase 14 shipped: extraction evaluation harness, CI gate, and the extractor fixes it surfaced (ADR-024, docs/evaluation.md).

- **2026-10-02**: Phase 13 shipped: supply tracking and refill estimates (ADR-023).

- **2026-10-02**: Phase 12 shipped: visit prep with a live, shareable brief (ADR-022).

- **2026-10-02**: QA pass across 19 pages x 4 viewports x 2 themes (console errors, failed requests, overflow, full axe incl. best practices, focus visibility). Fixed: Skip and delete-conversation controls were hover-only and unreachable on touch screens; dose and medication names truncated on phones; report and shared-view tables were not keyboard-scrollable; demo banner and 404 header outside landmarks; duplicate landmark label on the lab page; dose history heading started before the medicine did; report back link always pointed to the timeline; timeline filters showed on an empty timeline and "no match" read as "empty". Regression tests added for touch controls and the phone report.

- **2026-10-02**: Phase 11 shipped: dose tracking moved from the browser to the account, with history and backfilling (ADR-021). Also registered `LabResult` in `app/models.py`, which Phase 10 had missed.

- **2026-10-02**: Phase 10 shipped: structured lab results with trends (ADR-020). Demo documents grew from 5 to 9. Document search hits now show their date, since several reports can share a title.

- **2026-10-02**: Phase 9 shipped: global search with a Ctrl+K command palette (ADR-019). The palette opens instantly with no animation because it is summoned from the keyboard.

- **2026-10-02**: Added Diet notes (ADR-018) instead of generated nutrition advice: extraction (heuristic + LLM schema), review section, `diet_notes` table, Diet page, dashboard card, report and share sections, Ask MedSpace sources. Thin themed scrollbars replace the OS default.

- **2026-10-02**: Added optional "Continue with Google" (ADR-017): one consent can also connect Calendar/Tasks; skipping keeps the connect-later path. 10 backend tests and an e2e test cover account linking, takeover prevention, scopes, returning users and redirects.

- **2026-10-02**: Phase 8 shipped. Full Docker stack verified end to end (worker queue, SeaweedFS S3, fastembed). Accessibility and phone-overflow regressions are now caught by CI. Data export added. Remaining nice-to-haves: recorded Lighthouse scores, structured lab results, real-Groq evaluation set.

- **2026-10-02**: Phases 6-7 shipped. Google runs in simulation mode by default (`GOOGLE_PROVIDER=fake`) so every demo visitor can exercise sync end to end. Share tokens are shown exactly once; the list shows only a 6-character hint. Added `tzdata` so `zoneinfo` works on Windows hosts.

- **2026-10-02**: Phase 5 shipped. Offline mode answers extractively from confirmed records and keyword hits (hash vectors never count as evidence on their own). Generic domain words are excluded from keyword scoring.

- **2026-10-02**: Phases 2-4 shipped. Page previews render server-side as PNG (works on mobile, no PDF viewer needed). Non-prescription documents confirm without a prescription record (ADR-015). Course-completion to-dos stay tasks but are not duplicated on the timeline. Initial graphify graph: 1,022 nodes, 86 communities.

- **2026-10-01**: Phase 1 shipped. Added `GET /api/auth/session` (quiet anonymous boot) and a same-origin API proxy (ADR-014).

- **2026-10-01**: Plan created from the original brief. Changes vs brief: pgvector replaces FAISS (ADR-002); Groq with dual text/vision extraction (ADR-003); local embeddings (ADR-004); Calendar vs Tasks split (ADR-005); deterministic schedule normalization (ADR-006); ARQ queue (ADR-007); own auth + optional Google (ADR-008); draft→confirmed lifecycle (ADR-009); proxied share links (ADR-010).
