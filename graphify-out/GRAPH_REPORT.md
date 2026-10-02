# Graph Report - MedSpace  (2026-10-02)

## Corpus Check
- 261 files · ~99,101 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1964 nodes · 4576 edges · 166 communities (132 shown, 34 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 59 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1647abdd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_diet_notes.py
- records/service.py
- db.py
- dependencies
- devDependencies
- embeddings.py
- router.jsx
- assistant/service.py
- integrations/service.py
- Architecture Decision Records
- documents/service.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- identity/service.py
- extraction/service.py
- FeatureBento.jsx
- lib/api.js
- doses/service.py
- timeline/service.py
- labs.py
- visits/service.py
- errors.py
- identity/router.py
- mapping.js
- heuristic.py
- search/service.py
- test_integrations.py
- EasterEggs.jsx
- google.py
- GoogleClient
- SearchPalette.jsx
- integrations/api.js
- SignupIn
- assistant/router.py
- MedSpace Build Plan
- llm.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- User
- test_google_signin.py
- MedSpace
- sharing/service.py
- visits/api.js
- extraction/jobs.py
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- Visits.jsx
- scripts
- normalize_frequency
- SupplyDialog.jsx
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
- test_supply.py
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
- test_auth.py
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
- get_settings
- confirm
- test_labs.py
- test_assistant.py
- test_doses.py
- FakeGoogleClient
- audit/router.py
- doses/router.py
- MedicationHistory.jsx
- test_sharing.py
- csrf
- record
- doses/api.js
- _MemoryStore
- extraction/router.py
- env.py
- deps.py
- conftest.py
- test_timeline_dashboard.py
- demo_login
- supply/router.py
- demo/service.py
- uuid7

## God Nodes (most connected - your core abstractions)
1. `User` - 73 edges
2. `get_settings()` - 61 edges
3. `csrf()` - 52 edges
4. `utcnow()` - 38 edges
5. `Base` - 38 edges
6. `IdMixin` - 33 edges
7. `NotFound` - 32 edges
8. `Medication` - 31 edges
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

## Communities (166 total, 34 thin omitted)

### Community 0 - "test_diet_notes.py"
Cohesion: 0.17
Nodes (30): build_pdf(), build_scan_png(), issued(), date, A 'photo' of the prescription: rasterized, so it has no text layer., Scenario, drain(), Background job dispatch. `QUEUE_MODE=arq`: jobs go to Redis and run in the… (+22 more)

### Community 1 - "records/service.py"
Cohesion: 0.09
Nodes (72): NotFound, _record_line(), build_export(), AsyncSession, Medication, delete_diet_note(), delete_lab_result(), get_lab_trend() (+64 more)

### Community 2 - "db.py"
Cohesion: 0.14
Nodes (32): Base, IdMixin, datetime, Database engine, session factory and declarative base., TimestampMixin, utcnow(), Import every module's ORM models so `Base.metadata` is complete (Alembic,…, AuditLog (+24 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "embeddings.py"
Cohesion: 0.13
Nodes (10): Embedder, FastEmbedEmbedder, get_embedder(), HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and… (+2 more)

### Community 6 - "router.jsx"
Cohesion: 0.06
Nodes (9): AppLayout(), AuthLayout(), MarketingLayout(), Providers(), RouteError(), router, newId(), Prompts() (+1 more)

### Community 7 - "assistant/service.py"
Cohesion: 0.12
Nodes (34): ChatMessage, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, answer_stream(), _best_snippet(), build_prompt(), chunk_pages() (+26 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.19
Nodes (32): Conflict, encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _clock() (+24 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.08
Nodes (24): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+16 more)

### Community 10 - "documents/service.py"
Cohesion: 0.06
Nodes (61): PayloadTooLarge, UnsupportedMedia, inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded… (+53 more)

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
Cohesion: 0.17
Nodes (23): create_access_token(), hash_password(), needs_rehash(), new_opaque_token(), UUID, Password hashing, JWT access tokens, opaque token helpers and field encryption., sha256_hex(), verify_password() (+15 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.13
Nodes (27): ExtractionStatus, StrEnum, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt() (+19 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "lib/api.js"
Cohesion: 0.17
Nodes (13): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+5 more)

### Community 18 - "doses/service.py"
Cohesion: 0.17
Nodes (29): AdherenceDay, AdherenceOut, Counts, DoseLogIn, DoseLogOut, DoseSlot, MedicationAdherence, BaseModel (+21 more)

### Community 19 - "timeline/service.py"
Cohesion: 0.18
Nodes (23): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+15 more)

### Community 20 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (51): Unprocessable, The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser (+43 more)

### Community 22 - "errors.py"
Cohesion: 0.12
Nodes (14): AppError, Forbidden, install_error_handlers(), _problem(), Any, Exception, FastAPI, Request (+6 more)

### Community 23 - "identity/router.py"
Cohesion: 0.10
Nodes (36): client_ip(), Any, Request, rate_limit(), Fixed-window rate limiting. Uses Redis when `QUEUE_MODE=arq` (multi-process…, Audit trail: `record()` is the single write path, used by every module., clear_auth_cookies(), Response (+28 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "heuristic.py"
Cohesion: 0.11
Nodes (33): diet_category(), _diet_notes(), extract(), _lab_results(), _lab_row(), _medication_from_line(), _parse_date(), date (+25 more)

### Community 26 - "search/service.py"
Cohesion: 0.16
Nodes (16): CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession, BaseModel (+8 more)

### Community 27 - "test_integrations.py"
Cohesion: 0.41
Nodes (12): decrypt(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation…, test_callback_rejects_forged_state(), test_completed_tasks_flow_back() (+4 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "google.py"
Cohesion: 0.13
Nodes (8): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Any, Exception, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, Consent was revoked or the refresh token is no longer valid., Tokens

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.16
Nodes (10): useSearch(), SearchContext, GROUPS, JUMP_TO, SearchPalette(), useDebounced(), isTyping(), SearchPalette (+2 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "SignupIn"
Cohesion: 0.27
Nodes (4): ProfileUpdate, field_validator, SignupIn, update_profile()

### Community 34 - "assistant/router.py"
Cohesion: 0.21
Nodes (19): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+11 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.12
Nodes (16): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 1: Core platform + design system (+8 more)

### Community 36 - "llm.py"
Cohesion: 0.27
Nodes (6): GroqProvider, LLMError, _parse_json(), Any, Exception, LLM port and the Groq adapter (ADR-003). When `LLM_PROVIDER=fake` (the default)…

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.23
Nodes (7): APP_LINKS, AppNav(), MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "User"
Cohesion: 0.20
Nodes (21): User, BaseModel, field_validator, RefillIn, SupplyIn, SupplyOut, clear_supply(), list_supplies() (+13 more)

### Community 41 - "test_google_signin.py"
Cohesion: 0.23
Nodes (18): GoogleIdentity, google_sign_in(), AsyncClient, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017., Run start -> (simulated consent) -> callback. Returns the final redirect., test_callback_without_state_cookie_is_rejected() (+10 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.10
Nodes (43): Gone, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, create_share(), list_shares(), open_share(), CurrentUser, DbSession (+35 more)

### Community 45 - "extraction/jobs.py"
Cohesion: 0.29
Nodes (5): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

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
Cohesion: 0.20
Nodes (16): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+8 more)

### Community 52 - "SupplyDialog.jsx"
Cohesion: 0.25
Nodes (13): supplyKeys, useClearSupply(), useRefill(), useSetSupply(), useSupplyMutation(), leftLabel(), runsOutLabel(), trim() (+5 more)

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
Cohesion: 0.27
Nodes (7): here, SAMPLE, expectAccessible(), signUp(), startDemo(), here, LAB_SAMPLE

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.29
Nodes (7): 4.1 Upload → Extract → Review → Organize → Act, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "test_supply.py"
Cohesion: 0.29
Nodes (16): _at(), estimate(), date, datetime, Pure: the estimate for one medicine at `now` (an aware datetime in the user's…, _count(), _med(), _now() (+8 more)

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

### Community 80 - "test_auth.py"
Cohesion: 0.23
Nodes (18): signup(), AsyncClient, test_audit_trail_lists_own_events(), test_demo_login_creates_isolated_demo_user(), test_health_supports_head(), test_login_is_rate_limited(), test_login_wrong_password_is_generic(), test_logout_revokes_session() (+10 more)

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

### Community 140 - "get_settings"
Cohesion: 0.13
Nodes (22): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., CSRFMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging. (+14 more)

### Community 142 - "confirm"
Cohesion: 0.35
Nodes (12): set_status(), process_document(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction(), latest_for_document() (+4 more)

### Community 143 - "test_labs.py"
Cohesion: 0.19
Nodes (19): build_lab_pdf(), _diabetes(), LabReport, _lipids(), Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every…, lab_confirm_body(), _lab_pdf_text(), AsyncClient (+11 more)

### Community 144 - "test_assistant.py"
Cohesion: 0.42
Nodes (12): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+4 more)

### Community 145 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 147 - "audit/router.py"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 148 - "doses/router.py"
Cohesion: 0.27
Nodes (11): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+3 more)

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 151 - "csrf"
Cohesion: 0.34
Nodes (13): csrf(), AsyncClient, test_count_refill_and_clear(), test_supplies_are_private(), _create(), _demo(), AsyncClient, date (+5 more)

### Community 152 - "record"
Cohesion: 0.33
Nodes (7): list_for_user(), Any, AsyncSession, Request, UUID, Stage an audit row in the caller's transaction (committed with the business…, record()

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "_MemoryStore"
Cohesion: 0.25
Nodes (3): _get_store(), _MemoryStore, _RedisStore

### Community 156 - "extraction/router.py"
Cohesion: 0.40
Nodes (9): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+1 more)

### Community 157 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 158 - "deps.py"
Cohesion: 0.44
Nodes (8): _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, Shared FastAPI dependencies., Unauthorized, decode_access_token()

### Community 159 - "conftest.py"
Cohesion: 0.33
Nodes (9): reset_rate_limits(), auth_client(), _clean_tables(), client(), AsyncClient, Test harness: real Postgres (pgvector), fakes for every external service., _schema(), session() (+1 more)

### Community 160 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 161 - "demo_login"
Cohesion: 0.40
Nodes (5): demo_login(), DbSession, post, Request, Response

### Community 162 - "supply/router.py"
Cohesion: 0.27
Nodes (11): clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get, post, put (+3 more)

### Community 163 - "demo/service.py"
Cohesion: 0.35
Nodes (10): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, Seed demo records for a new simulated account; never let seeding block a sign-… (+2 more)

### Community 164 - "uuid7"
Cohesion: 0.67
Nodes (3): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7()

## Knowledge Gaps
- **202 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+197 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `test_diet_notes.py`, `db.py`, `embeddings.py`, `assistant/service.py`, `integrations/service.py`, `documents/service.py`, `integrations/router.py`, `identity/service.py`, `extraction/service.py`, `errors.py`, `identity/router.py`, `_MemoryStore`, `google.py`, `deps.py`, `env.py`, `test_timeline_dashboard.py`, `demo_login`, `demo/service.py`, `llm.py`, `sharing/service.py`, `Settings`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `records/service.py`, `db.py`, `demo/service.py`, `SignupIn`, `assistant/service.py`, `integrations/service.py`, `test_google_signin.py`, `documents/service.py`, `sharing/service.py`, `extraction/jobs.py`, `confirm`, `extraction/service.py`, `identity/service.py`, `doses/service.py`, `timeline/service.py`, `visits/service.py`, `deps.py`, `test_supply.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `utcnow()` connect `db.py` to `records/service.py`, `assistant/router.py`, `demo/service.py`, `integrations/service.py`, `User`, `documents/service.py`, `sharing/service.py`, `confirm`, `extraction/service.py`, `identity/service.py`, `doses/service.py`, `test_sharing.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Base` (e.g. with `_clean_tables()` and `_schema()`) actually correct?**
  _`Base` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _202 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `records/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08701754385964912 - nodes in this community are weakly interconnected._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13535353535353536 - nodes in this community are weakly interconnected._