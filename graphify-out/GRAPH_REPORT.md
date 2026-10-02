# Graph Report - MedSpace  (2026-10-02)

## Corpus Check
- 220 files · ~82,172 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1670 nodes · 3756 edges · 135 communities (105 shown, 30 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `01cf2d8c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- csrf
- records/service.py
- sharing/service.py
- dependencies
- devDependencies
- timeline/service.py
- router.jsx
- assistant/service.py
- integrations/service.py
- Architecture Decision Records
- documents/router.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- identity/service.py
- extraction/service.py
- FeatureBento.jsx
- lib/api.js
- SignupIn
- documents/service.py
- heuristic.py
- HttpGoogleClient
- errors.py
- identity/router.py
- mapping.js
- GoogleClient
- labs.py
- test_integrations.py
- EasterEggs.jsx
- search/service.py
- deps.py
- SearchPalette.jsx
- integrations/api.js
- Conflict
- extraction/jobs.py
- MedSpace Build Plan
- llm.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- get_settings
- test_google_signin.py
- MedSpace
- test_search.py
- audit/router.py
- record
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- ratelimit.py
- scripts
- User
- files.py
- api service (alembic + uvicorn)
- lib/format.js
- Settings.jsx
- Getting started
- LocalStorage
- helpers.js
- Ask.jsx
- Settings
- 4. Core flows
- Diet.jsx
- ObjectStorage
- package.json
- Widgets.jsx
- sharing/api.js
- labs/api.js
- ConfirmDialog.jsx
- puns.js
- assistant/api.js
- HeroMorph.jsx
- LabDetail.jsx
- TodaySchedule.jsx
- Workflow.jsx
- audit.js
- Medications.jsx
- Sharing.jsx
- Timeline.jsx
- demo_login
- Labs.jsx
- ComingSoon.jsx
- Field.jsx
- theme.jsx
- SharedView.jsx
- ReportBody.jsx
- Landing.jsx
- MarketingNav.jsx
- ProcessingState.jsx
- Documents.jsx
- eslint-plugin-react-refresh
- medspace-api
- @phosphor-icons/react
- @tanstack/react-query
- @playwright/test
- tailwindcss
- @testing-library/react
- vitest

## God Nodes (most connected - your core abstractions)
1. `get_settings()` - 61 edges
2. `User` - 46 edges
3. `csrf()` - 39 edges
4. `utcnow()` - 32 edges
5. `Base` - 32 edges
6. `IdMixin` - 27 edges
7. `NotFound` - 26 edges
8. `record()` - 25 edges
9. `Document` - 25 edges
10. `Medication` - 22 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `share_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/sharing/service.py → backend/app/core/config.py
- `_clean_tables()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `_schema()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `demo_login()` --uses--> `NotFound`  [INFERRED]
  backend/app/modules/demo/router.py → backend/app/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (135 total, 30 thin omitted)

### Community 0 - "csrf"
Cohesion: 0.06
Nodes (91): reset_rate_limits(), build_lab_pdf(), build_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids() (+83 more)

### Community 1 - "records/service.py"
Cohesion: 0.09
Nodes (73): NotFound, build_export(), AsyncSession, LabResult, Medication, One test result copied from a confirmed lab report (ADR-020). value_text and…, delete_diet_note(), delete_lab_result() (+65 more)

### Community 2 - "sharing/service.py"
Cohesion: 0.06
Nodes (83): Base, IdMixin, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin, utcnow(), uuid7() (+75 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "timeline/service.py"
Cohesion: 0.18
Nodes (23): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+15 more)

### Community 6 - "router.jsx"
Cohesion: 0.07
Nodes (6): AppLayout(), AuthLayout(), MarketingLayout(), Providers(), RouteError(), router

### Community 7 - "assistant/service.py"
Cohesion: 0.05
Nodes (63): ChatMessage, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, ask(), AskIn, create_thread(), delete_thread(), get_thread() (+55 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.22
Nodes (28): encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _clock(), _delete_remote() (+20 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.10
Nodes (21): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+13 more)

### Community 10 - "documents/router.py"
Cohesion: 0.17
Nodes (26): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+18 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.16
Nodes (23): connect(), disconnect(), google_sign_in(), preview(), providers(), pull(), BaseModel, CurrentUser (+15 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/service.py"
Cohesion: 0.18
Nodes (22): constant_time_equals(), create_access_token(), hash_password(), needs_rehash(), new_opaque_token(), UUID, Password hashing, JWT access tokens, opaque token helpers and field encryption., sha256_hex() (+14 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.12
Nodes (32): Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt() (+24 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "lib/api.js"
Cohesion: 0.17
Nodes (13): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+5 more)

### Community 18 - "SignupIn"
Cohesion: 0.27
Nodes (5): LoginIn, ProfileUpdate, BaseModel, field_validator, SignupIn

### Community 19 - "documents/service.py"
Cohesion: 0.18
Nodes (25): PayloadTooLarge, Unprocessable, UnsupportedMedia, Document, DocumentKind, DocumentStatus, StrEnum, create_document() (+17 more)

### Community 20 - "heuristic.py"
Cohesion: 0.06
Nodes (61): diet_category(), _diet_notes(), extract(), _lab_results(), _lab_row(), _medication_from_line(), _parse_date(), date (+53 more)

### Community 21 - "HttpGoogleClient"
Cohesion: 0.17
Nodes (5): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, Consent was revoked or the refresh token is no longer valid.

### Community 22 - "errors.py"
Cohesion: 0.12
Nodes (14): AppError, Forbidden, install_error_handlers(), _problem(), Any, Exception, FastAPI, Request (+6 more)

### Community 23 - "identity/router.py"
Cohesion: 0.16
Nodes (27): clear_auth_cookies(), Response, Auth cookie helpers shared by the identity and demo routers., Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), delete_account(), export_data(), login() (+19 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "GoogleClient"
Cohesion: 0.12
Nodes (4): GoogleClient, Any, Protocol, Tokens

### Community 26 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 27 - "test_integrations.py"
Cohesion: 0.27
Nodes (16): decrypt(), _fernet(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient (+8 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "search/service.py"
Cohesion: 0.16
Nodes (16): CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession, BaseModel (+8 more)

### Community 30 - "deps.py"
Cohesion: 0.44
Nodes (8): _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, Shared FastAPI dependencies., Unauthorized, decode_access_token()

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.16
Nodes (10): useSearch(), SearchContext, GROUPS, JUMP_TO, SearchPalette(), useDebounced(), isTyping(), SearchPalette (+2 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "Conflict"
Cohesion: 0.15
Nodes (14): Conflict, login_with_google(), Find or create the account for a Google identity. Returns (user, outcome) where…, has_sync_scopes(), pkce_pair(), Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent…, callback() (+6 more)

### Community 34 - "extraction/jobs.py"
Cohesion: 0.18
Nodes (9): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, process_document(), Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., purge_demo_accounts(), purge_share_links(), session() (+1 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.15
Nodes (13): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 1: Core platform + design system, Phase 2: Documents + processing pipeline, Phase 3: Prescription intelligence (extract → review → confirm), Phase 4: Dashboard, medications, timeline (+5 more)

### Community 36 - "llm.py"
Cohesion: 0.23
Nodes (9): get_llm(), GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol (+1 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.23
Nodes (7): APP_LINKS, AppNav(), MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "get_settings"
Cohesion: 0.15
Nodes (20): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., CSRFMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging. (+12 more)

### Community 41 - "test_google_signin.py"
Cohesion: 0.13
Nodes (20): FakeGoogleClient, GoogleIdentity, In-memory Google for demos and tests. State is per access token and per…, google_sign_in(), AsyncClient, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017. (+12 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "test_search.py"
Cohesion: 0.49
Nodes (9): AsyncClient, search(), test_document_text_matches_with_snippets(), test_no_matches_and_validation(), test_partial_names_find_medications(), test_prescribers_and_clinics(), test_search_is_private(), test_search_requires_auth() (+1 more)

### Community 44 - "audit/router.py"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 45 - "record"
Cohesion: 0.33
Nodes (7): list_for_user(), Any, AsyncSession, Request, UUID, Stage an audit row in the caller's transaction (committed with the business…, record()

### Community 46 - "Deploying MedSpace"
Cohesion: 0.29
Nodes (7): 1. Database: Neon (or any Postgres 15+ with pgvector), 2. Object storage: Cloudflare R2 (or AWS S3), 3. API: one container, 4. Web: static build with an `/api` rewrite, 5. Google OAuth (optional), Checklist, Deploying MedSpace

### Community 47 - "AuthForms.jsx"
Cohesion: 0.18
Nodes (10): DemoDivider(), LoginForm(), loginSchema, SignupForm(), signupSchema, useAuthMutation(), GOOGLE_ERRORS, useAuthProviders() (+2 more)

### Community 48 - "records/api.js"
Cohesion: 0.18
Nodes (4): recordKeys, useInvalidateRecords(), useUpdateCareAction(), useUpdateMedication()

### Community 49 - "ratelimit.py"
Cohesion: 0.12
Nodes (11): client_ip(), _get_store(), _MemoryStore, Any, Request, rate_limit(), Fixed-window rate limiting. Uses Redis when `QUEUE_MODE=arq` (multi-process…, _RedisStore (+3 more)

### Community 50 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, dev, e2e, format, lint, preview, test (+1 more)

### Community 51 - "User"
Cohesion: 0.24
Nodes (12): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, Seed demo records for a new simulated account; never let seeding block a sign-… (+4 more)

### Community 52 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 53 - "api service (alembic + uvicorn)"
Cohesion: 0.25
Nodes (11): CI Backend job (ruff + pytest on pgvector Postgres), CI Docker images build job, CI E2E job (Playwright + axe, fake providers), CI Frontend job (lint + Vitest + build), api service (alembic + uvicorn), x-backend-env shared env anchor, postgres service (pgvector/pgvector:pg17), redis service (+3 more)

### Community 54 - "lib/format.js"
Cohesion: 0.36
Nodes (8): firstName(), formatBytes(), formatClock(), formatDate(), formatRelativeDay(), greeting(), timeAgo(), toDate()

### Community 56 - "Getting started"
Cohesion: 0.25
Nodes (8): Deploy, Enable Google sign-in, Calendar & Tasks (optional), Enable real AI extraction (optional), Getting started, Prerequisites, Run everything, Run tests, What works without any API keys

### Community 57 - "LocalStorage"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 58 - "helpers.js"
Cohesion: 0.28
Nodes (7): here, SAMPLE, expectAccessible(), signUp(), startDemo(), here, LAB_SAMPLE

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.29
Nodes (7): 4.1 Upload → Extract → Review → Organize → Act, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 65 - "package.json"
Cohesion: 0.40
Nodes (4): name, private, type, version

### Community 70 - "puns.js"
Cohesion: 0.29
Nodes (5): EMPTY_QUIPS, LOADING_PUNS, MARQUEE_PUNS, NOT_FOUND_LINES, PROCESSING_PUNS

### Community 72 - "HeroMorph.jsx"
Cohesion: 0.33
Nodes (6): DURATIONS, EASE, HeroMorph(), PHASES, RX, usePhase()

### Community 74 - "TodaySchedule.jsx"
Cohesion: 0.53
Nodes (5): nowHHMM(), slotFor(), SLOTS, TodaySchedule(), useTaken()

### Community 79 - "Timeline.jsx"
Cohesion: 0.40
Nodes (3): EventRow(), linkFor(), TYPES

### Community 80 - "demo_login"
Cohesion: 0.40
Nodes (5): demo_login(), DbSession, post, Request, Response

### Community 83 - "Field.jsx"
Cohesion: 0.40
Nodes (3): Input, Select, Textarea

### Community 84 - "theme.jsx"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

## Knowledge Gaps
- **186 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+181 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `csrf`, `sharing/service.py`, `assistant/service.py`, `integrations/service.py`, `documents/router.py`, `integrations/router.py`, `identity/service.py`, `extraction/service.py`, `documents/service.py`, `errors.py`, `identity/router.py`, `test_integrations.py`, `deps.py`, `Conflict`, `llm.py`, `ratelimit.py`, `User`, `Settings`, `demo_login`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `records/service.py`, `sharing/service.py`, `extraction/jobs.py`, `Conflict`, `timeline/service.py`, `integrations/service.py`, `test_google_signin.py`, `identity/service.py`, `extraction/service.py`, `ratelimit.py`, `deps.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `GoogleClient` connect `GoogleClient` to `integrations/service.py`, `Conflict`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _186 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `csrf` be split into smaller, more focused modules?**
  _Cohesion score 0.05919191919191919 - nodes in this community are weakly interconnected._
- **Should `records/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08544087491455912 - nodes in this community are weakly interconnected._
- **Should `sharing/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.060382916053019146 - nodes in this community are weakly interconnected._