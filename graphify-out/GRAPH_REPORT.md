# Graph Report - MedSpace  (2026-10-02)

## Corpus Check
- 220 files · ~82,172 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1692 nodes · 3669 edges · 149 communities (109 shown, 40 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 133 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b2c33a92`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_documents_flow.py
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
- Exception
- FeatureBento.jsx
- lib/api.js
- SignupIn
- documents/service.py
- extraction/service.py
- google.py
- errors.py
- identity/router.py
- mapping.js
- GoogleClient
- labs.py
- test_integrations.py
- EasterEggs.jsx
- embeddings.py
- deps.py
- SearchPalette.jsx
- integrations/api.js
- csrf
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
- audit/service.py
- test_diet_notes.py
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- ratelimit.py
- scripts
- normalize_frequency
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
- demo/router.py
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
- test_labs.py
- conftest.py
- samples.py
- test_sharing.py
- test_timeline_dashboard.py
- .dispatch
- field_validator
- Request
- CurrentUser
- DbSession
- delete
- get
- patch
- parametrize

## God Nodes (most connected - your core abstractions)
1. `get_settings()` - 57 edges
2. `csrf()` - 37 edges
3. `User` - 36 edges
4. `utcnow()` - 29 edges
5. `Medication` - 27 edges
6. `Base` - 26 edges
7. `record()` - 25 edges
8. `Prescription` - 23 edges
9. `NotFound` - 23 edges
10. `Architecture Decision Records` - 21 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `index_document()` --calls--> `DocumentChunk`  [INFERRED]
  backend/app/modules/assistant/service.py → backend/app/modules/assistant/models.py
- `index_document()` --calls--> `get_embedder()`  [INFERRED]
  backend/app/modules/assistant/service.py → backend/app/shared/embeddings.py
- `Source` --uses--> `Medication`  [INFERRED]
  backend/app/modules/assistant/service.py → backend/app/modules/records/models.py
- `_hybrid_chunk_ids()` --calls--> `get_embedder()`  [INFERRED]
  backend/app/modules/assistant/service.py → backend/app/shared/embeddings.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (149 total, 40 thin omitted)

### Community 0 - "test_documents_flow.py"
Cohesion: 0.31
Nodes (19): build_pdf(), drain(), Wait for all inline jobs (used by tests)., test_reconfirming_replaces_notes_and_delete_works(), test_review_then_confirm_creates_notes(), confirm_body(), AsyncClient, Response (+11 more)

### Community 1 - "records/service.py"
Cohesion: 0.06
Nodes (97): NotFound, build_export(), AsyncSession, User, Account data export: one JSON document with every record the user owns.…, CareAction, DietNote, LabResult (+89 more)

### Community 2 - "sharing/service.py"
Cohesion: 0.06
Nodes (77): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, utcnow(), Gone, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatMessage (+69 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "timeline/service.py"
Cohesion: 0.17
Nodes (23): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+15 more)

### Community 6 - "router.jsx"
Cohesion: 0.07
Nodes (3): AppLayout(), Providers(), router

### Community 7 - "assistant/service.py"
Cohesion: 0.09
Nodes (46): ask(), create_thread(), delete_thread(), get_thread(), list_threads(), CurrentUser, DbSession, delete (+38 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.18
Nodes (33): Conflict, encrypt(), Any, Request, Stage an audit row in the caller's transaction (committed with the business…, record(), get_google(), OAuthConnection (+25 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.10
Nodes (21): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+13 more)

### Community 10 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.11
Nodes (34): constant_time_equals(), has_sync_scopes(), pkce_pair(), True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect(), _frontend() (+26 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/service.py"
Cohesion: 0.14
Nodes (26): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), create_access_token(), hash_password(), needs_rehash(), UUID, Password hashing, JWT access tokens, opaque token helpers and field encryption. (+18 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "lib/api.js"
Cohesion: 0.17
Nodes (13): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+5 more)

### Community 18 - "SignupIn"
Cohesion: 0.23
Nodes (7): LoginIn, ProfileUpdate, BaseModel, field_validator, SignupIn, UserOut, update_profile()

### Community 19 - "documents/service.py"
Cohesion: 0.26
Nodes (18): Document, create_document(), delete_document(), get_document(), get_document_by_id(), list_documents(), page_preview_png(), purge_user_files() (+10 more)

### Community 20 - "extraction/service.py"
Cohesion: 0.05
Nodes (87): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, User, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-… (+79 more)

### Community 21 - "google.py"
Cohesion: 0.13
Nodes (8): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Any, Exception, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, Consent was revoked or the refresh token is no longer valid., Tokens

### Community 22 - "errors.py"
Cohesion: 0.11
Nodes (17): AppError, Forbidden, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI (+9 more)

### Community 23 - "identity/router.py"
Cohesion: 0.20
Nodes (23): clear_auth_cookies(), delete_account(), export_data(), login(), logout(), me(), BaseModel, CurrentUser (+15 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 26 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 27 - "test_integrations.py"
Cohesion: 0.27
Nodes (16): decrypt(), _fernet(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient (+8 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "embeddings.py"
Cohesion: 0.13
Nodes (10): Embedder, FastEmbedEmbedder, get_embedder(), HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and… (+2 more)

### Community 30 - "deps.py"
Cohesion: 0.33
Nodes (10): get_session(), AsyncSession, _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, Shared FastAPI dependencies. (+2 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.16
Nodes (10): useSearch(), SearchContext, GROUPS, JUMP_TO, SearchPalette(), useDebounced(), isTyping(), SearchPalette (+2 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "csrf"
Cohesion: 0.24
Nodes (19): csrf(), signup(), AsyncClient, test_audit_trail_lists_own_events(), test_demo_login_creates_isolated_demo_user(), test_health_supports_head(), test_login_is_rate_limited(), test_login_wrong_password_is_generic() (+11 more)

### Community 34 - "extraction/jobs.py"
Cohesion: 0.18
Nodes (8): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, DocumentKind, DocumentStatus, StrEnum, Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

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
Cohesion: 0.16
Nodes (21): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., CSRFMiddleware, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware (+13 more)

### Community 41 - "test_google_signin.py"
Cohesion: 0.13
Nodes (20): FakeGoogleClient, GoogleIdentity, In-memory Google for demos and tests. State is per access token and per…, google_sign_in(), AsyncClient, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017. (+12 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "test_search.py"
Cohesion: 0.49
Nodes (9): AsyncClient, search(), test_document_text_matches_with_snippets(), test_no_matches_and_validation(), test_partial_names_find_medications(), test_prescribers_and_clinics(), test_search_is_private(), test_search_requires_auth() (+1 more)

### Community 44 - "audit/service.py"
Cohesion: 0.20
Nodes (11): list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage, BaseModel, list_for_user() (+3 more)

### Community 45 - "test_diet_notes.py"
Cohesion: 0.23
Nodes (18): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+10 more)

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
Nodes (12): client_ip(), _get_store(), _MemoryStore, Any, Request, rate_limit(), Fixed-window rate limiting. Uses Redis when `QUEUE_MODE=arq` (multi-process…, _RedisStore (+4 more)

### Community 50 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, dev, e2e, format, lint, preview, test (+1 more)

### Community 51 - "normalize_frequency"
Cohesion: 0.20
Nodes (16): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+8 more)

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

### Community 80 - "demo/router.py"
Cohesion: 0.19
Nodes (10): new_opaque_token(), demo_login(), DbSession, post, Request, Response, Response, Auth cookie helpers shared by the identity and demo routers. (+2 more)

### Community 83 - "Field.jsx"
Cohesion: 0.40
Nodes (3): Input, Select, Textarea

### Community 84 - "theme.jsx"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

### Community 135 - "test_labs.py"
Cohesion: 0.27
Nodes (13): lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_single_line_rows_and_printed_flags(), test_heuristic_reads_split_line_lab_tables(), test_labs_are_private_and_deletable() (+5 more)

### Community 136 - "conftest.py"
Cohesion: 0.29
Nodes (10): reset_rate_limits(), purge_demo_accounts(), auth_client(), _clean_tables(), client(), AsyncClient, Test harness: real Postgres (pgvector), fakes for every external service., _schema() (+2 more)

### Community 137 - "samples.py"
Cohesion: 0.31
Nodes (10): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+2 more)

### Community 138 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 139 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 140 - ".dispatch"
Cohesion: 0.60
Nodes (3): Request, Response, RequestResponseEndpoint

## Knowledge Gaps
- **186 isolated node(s):** `Features`, `Architecture at a glance`, `Engineering highlights`, `Tech stack`, `Prerequisites` (+181 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `sharing/service.py`, `assistant/service.py`, `integrations/service.py`, `documents/router.py`, `integrations/router.py`, `.dispatch`, `test_timeline_dashboard.py`, `identity/service.py`, `documents/service.py`, `extraction/service.py`, `google.py`, `errors.py`, `identity/router.py`, `test_integrations.py`, `embeddings.py`, `deps.py`, `llm.py`, `ratelimit.py`, `Settings`, `demo/router.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `post_process()` connect `extraction/service.py` to `normalize_frequency`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `User` connect `identity/service.py` to `sharing/service.py`, `extraction/jobs.py`, `timeline/service.py`, `integrations/service.py`, `test_google_signin.py`, `SignupIn`, `deps.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `get_settings()` (e.g. with `answer_stream()` and `purge_expired_demo_accounts()`) actually correct?**
  _`get_settings()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `csrf()` (e.g. with `test_labs_are_private_and_deletable()` and `test_other_units_are_listed_but_not_charted()`) actually correct?**
  _`csrf()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `utcnow()` (e.g. with `purge_expired_demo_accounts()` and `confirm()`) actually correct?**
  _`utcnow()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Features`, `Architecture at a glance`, `Engineering highlights` to the rest of the system?**
  _186 weakly-connected nodes found - possible documentation gaps or missing edges._