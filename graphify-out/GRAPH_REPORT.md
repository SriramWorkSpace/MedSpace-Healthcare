# Graph Report - MedSpace  (2026-10-02)

## Corpus Check
- 248 files · ~95,132 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1875 nodes · 4278 edges · 149 communities (116 shown, 33 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b12a7b3b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- csrf
- records/service.py
- db.py
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
- User
- extract_document
- FeatureBento.jsx
- lib/api.js
- doses/service.py
- documents/service.py
- labs.py
- visits/service.py
- errors.py
- identity/router.py
- mapping.js
- heuristic.py
- search/service.py
- test_integrations.py
- EasterEggs.jsx
- HttpGoogleClient
- GoogleClient
- SearchPalette.jsx
- integrations/api.js
- SignupIn
- Medication
- MedSpace Build Plan
- LLMError
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- get_settings
- test_google_signin.py
- MedSpace
- sharing/service.py
- visits/api.js
- extraction/schemas.py
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- Visits.jsx
- scripts
- normalize_frequency
- files.py
- api service (alembic + uvicorn)
- lib/format.js
- Settings.jsx
- Getting started
- test_timeline_dashboard.py
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
- demo/service.py
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
- DoseStrip.jsx
- VisitBrief.jsx
- test_search.py
- clinician.js
- .dispatch
- extraction/service.py
- records/router.py
- MedicationHistory.jsx
- record
- doses/api.js
- env.py

## God Nodes (most connected - your core abstractions)
1. `get_settings()` - 61 edges
2. `User` - 61 edges
3. `csrf()` - 49 edges
4. `Base` - 36 edges
5. `utcnow()` - 35 edges
6. `IdMixin` - 31 edges
7. `NotFound` - 30 edges
8. `Medication` - 26 edges
9. `record()` - 25 edges
10. `Document` - 25 edges

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

## Communities (149 total, 33 thin omitted)

### Community 0 - "csrf"
Cohesion: 0.05
Nodes (107): reset_rate_limits(), build_lab_pdf(), build_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids() (+99 more)

### Community 1 - "records/service.py"
Cohesion: 0.13
Nodes (44): build_export(), AsyncSession, CareActionOut, CareActionUpdate, DietNoteOut, DietNotesOut, LabPoint, LabResultOut (+36 more)

### Community 2 - "db.py"
Cohesion: 0.15
Nodes (28): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, AuditLog, Append-only trail of security-relevant actions. Never updated or deleted by app… (+20 more)

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
Cohesion: 0.06
Nodes (9): AppLayout(), AuthLayout(), MarketingLayout(), Providers(), RouteError(), router, newId(), Prompts() (+1 more)

### Community 7 - "assistant/service.py"
Cohesion: 0.05
Nodes (63): ChatMessage, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, ask(), AskIn, create_thread(), delete_thread(), get_thread() (+55 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.22
Nodes (28): encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _clock(), _delete_remote() (+20 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.09
Nodes (23): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+15 more)

### Community 10 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.11
Nodes (35): constant_time_equals(), has_sync_scopes(), pkce_pair(), Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect() (+27 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "User"
Cohesion: 0.07
Nodes (57): get_session(), AsyncSession, UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), _extract_token(), get_current_user(), get_optional_user() (+49 more)

### Community 15 - "extract_document"
Cohesion: 0.14
Nodes (19): _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload, _coerce() (+11 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "lib/api.js"
Cohesion: 0.17
Nodes (13): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+5 more)

### Community 18 - "doses/service.py"
Cohesion: 0.13
Nodes (38): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+30 more)

### Community 19 - "documents/service.py"
Cohesion: 0.13
Nodes (30): Conflict, PayloadTooLarge, UnsupportedMedia, Document, DocumentKind, DocumentStatus, StrEnum, create_document() (+22 more)

### Community 20 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 21 - "visits/service.py"
Cohesion: 0.10
Nodes (50): Unprocessable, The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser (+42 more)

### Community 22 - "errors.py"
Cohesion: 0.09
Nodes (21): AppError, Forbidden, install_error_handlers(), _problem(), Any, Exception, FastAPI, Request (+13 more)

### Community 23 - "identity/router.py"
Cohesion: 0.16
Nodes (27): clear_auth_cookies(), Response, Auth cookie helpers shared by the identity and demo routers., Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), delete_account(), export_data(), login() (+19 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "heuristic.py"
Cohesion: 0.15
Nodes (20): diet_category(), _diet_notes(), extract(), _lab_results(), _lab_row(), _parse_date(), date, Offline, rule-based extractor used when no LLM is configured (CI, demo, keyless… (+12 more)

### Community 26 - "search/service.py"
Cohesion: 0.15
Nodes (17): medication_status(), CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession (+9 more)

### Community 27 - "test_integrations.py"
Cohesion: 0.27
Nodes (16): decrypt(), _fernet(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient (+8 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "HttpGoogleClient"
Cohesion: 0.17
Nodes (5): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, Consent was revoked or the refresh token is no longer valid.

### Community 30 - "GoogleClient"
Cohesion: 0.12
Nodes (4): GoogleClient, Any, Protocol, Tokens

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.16
Nodes (10): useSearch(), SearchContext, GROUPS, JUMP_TO, SearchPalette(), useDebounced(), isTyping(), SearchPalette (+2 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "SignupIn"
Cohesion: 0.26
Nodes (6): LoginIn, ProfileUpdate, BaseModel, field_validator, SignupIn, UserOut

### Community 34 - "Medication"
Cohesion: 0.36
Nodes (8): Medication, doses_on(), get_medication(), date, Scheduled HH:MM times for one medicine on one day, by its schedule and course…, Scheduled doses for a calendar day (as-needed and stopped meds excluded),…, times_on(), update_medication()

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.13
Nodes (15): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 1: Core platform + design system, Phase 2: Documents + processing pipeline (+7 more)

### Community 36 - "LLMError"
Cohesion: 0.24
Nodes (8): get_llm(), GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol

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
Cohesion: 0.11
Nodes (24): get_settings(), Application settings, loaded from environment variables (and `.env` in…, ServiceUnavailable, configure_logging(), Logging configuration., CSRFMiddleware, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests… (+16 more)

### Community 41 - "test_google_signin.py"
Cohesion: 0.13
Nodes (20): FakeGoogleClient, GoogleIdentity, In-memory Google for demos and tests. State is per access token and per…, google_sign_in(), AsyncClient, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017. (+12 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.11
Nodes (45): datetime, utcnow(), Gone, NotFound, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, create_share(), list_shares() (+37 more)

### Community 45 - "extraction/schemas.py"
Cohesion: 0.14
Nodes (23): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+15 more)

### Community 46 - "Deploying MedSpace"
Cohesion: 0.29
Nodes (7): 1. Database: Neon (or any Postgres 15+ with pgvector), 2. Object storage: Cloudflare R2 (or AWS S3), 3. API: one container, 4. Web: static build with an `/api` rewrite, 5. Google OAuth (optional), Checklist, Deploying MedSpace

### Community 47 - "AuthForms.jsx"
Cohesion: 0.18
Nodes (10): DemoDivider(), LoginForm(), loginSchema, SignupForm(), signupSchema, useAuthMutation(), GOOGLE_ERRORS, useAuthProviders() (+2 more)

### Community 48 - "records/api.js"
Cohesion: 0.18
Nodes (4): recordKeys, useInvalidateRecords(), useUpdateCareAction(), useUpdateMedication()

### Community 50 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, dev, e2e, format, lint, preview, test (+1 more)

### Community 51 - "normalize_frequency"
Cohesion: 0.19
Nodes (17): _medication_from_line(), _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown… (+9 more)

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

### Community 57 - "test_timeline_dashboard.py"
Cohesion: 0.22
Nodes (11): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets() (+3 more)

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
Cohesion: 0.25
Nodes (6): EMPTY_QUIPS, LOADING_PUNS, MARQUEE_PUNS, NOT_FOUND_LINES, PROCESSING_PUNS, STREAK_LINE

### Community 72 - "HeroMorph.jsx"
Cohesion: 0.33
Nodes (6): DURATIONS, EASE, HeroMorph(), PHASES, RX, usePhase()

### Community 74 - "TodaySchedule.jsx"
Cohesion: 0.53
Nodes (5): nowHHMM(), slotFor(), SLOTS, TodaySchedule(), useMigrateDeviceTicks()

### Community 79 - "Timeline.jsx"
Cohesion: 0.40
Nodes (3): EventRow(), linkFor(), TYPES

### Community 80 - "demo/service.py"
Cohesion: 0.11
Nodes (17): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-… (+9 more)

### Community 83 - "Field.jsx"
Cohesion: 0.40
Nodes (3): Input, Select, Textarea

### Community 84 - "theme.jsx"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

### Community 135 - "DoseStrip.jsx"
Cohesion: 0.29
Nodes (7): describe(), DoseStrip(), daySummary(), fillDays(), percent(), STATE_LABELS, TONE_CLASS

### Community 136 - "VisitBrief.jsx"
Cohesion: 0.50
Nodes (3): CHANGE_LABELS, label(), VisitBrief()

### Community 137 - "test_search.py"
Cohesion: 0.49
Nodes (9): AsyncClient, search(), test_document_text_matches_with_snippets(), test_no_matches_and_validation(), test_partial_names_find_medications(), test_prescribers_and_clinics(), test_search_is_private(), test_search_requires_auth() (+1 more)

### Community 140 - ".dispatch"
Cohesion: 0.60
Nodes (3): Request, Response, RequestResponseEndpoint

### Community 142 - "extraction/service.py"
Cohesion: 0.32
Nodes (13): Extraction, ExtractionStatus, StrEnum, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction(), latest_for_document() (+5 more)

### Community 143 - "records/router.py"
Cohesion: 0.33
Nodes (17): delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription(), list_care_actions(), list_diet_notes(), list_lab_trends(), list_medications() (+9 more)

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 152 - "record"
Cohesion: 0.31
Nodes (8): list_for_user(), Any, AsyncSession, Request, UUID, Audit trail: `record()` is the single write path, used by every module., Stage an audit row in the caller's transaction (committed with the business…, record()

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 157 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

## Knowledge Gaps
- **198 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+193 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `db.py`, `assistant/service.py`, `integrations/service.py`, `documents/router.py`, `integrations/router.py`, `.dispatch`, `User`, `extraction/service.py`, `extract_document`, `documents/service.py`, `errors.py`, `identity/router.py`, `test_integrations.py`, `env.py`, `LLMError`, `sharing/service.py`, `test_timeline_dashboard.py`, `Settings`, `demo/service.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `records/service.py`, `db.py`, `timeline/service.py`, `assistant/service.py`, `integrations/service.py`, `test_google_signin.py`, `sharing/service.py`, `extraction/service.py`, `demo/service.py`, `doses/service.py`, `documents/service.py`, `visits/service.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_google_signin.py`, `test_integrations.py`, `User`, `test_timeline_dashboard.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Base` (e.g. with `_clean_tables()` and `_schema()`) actually correct?**
  _`Base` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _198 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `csrf` be split into smaller, more focused modules?**
  _Cohesion score 0.05217391304347826 - nodes in this community are weakly interconnected._
- **Should `records/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1294685990338164 - nodes in this community are weakly interconnected._