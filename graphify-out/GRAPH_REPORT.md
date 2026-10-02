# Graph Report - MedSpace  (2026-10-03)

## Corpus Check
- 276 files · ~107,067 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2071 nodes · 4816 edges · 182 communities (143 shown, 39 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8657683b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_diet_notes.py
- records/service.py
- db.py
- dependencies
- devDependencies
- assistant/router.py
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
- auth.jsx
- doses/service.py
- timeline/service.py
- test_sharing.py
- visits/service.py
- documents/router.py
- set_auth_cookies
- mapping.js
- heuristic.py
- search/service.py
- test_integrations.py
- EasterEggs.jsx
- HttpGoogleClient
- GoogleClient
- SearchPalette.jsx
- integrations/api.js
- test_eval.py
- extraction/schemas.py
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
- .dispatch
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
- test_timeline_dashboard.py
- helpers.js
- Ask.jsx
- Settings
- 4. Core flows
- Diet.jsx
- confirm
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
- vite.config.js
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
- samples.py
- extraction/router.py
- test_labs.py
- test_assistant.py
- test_doses.py
- labs.py
- audit/service.py
- test_supply.py
- MedicationHistory.jsx
- corpus.py
- csrf
- errors.py
- doses/api.js
- ratelimit.py
- demo/service.py
- env.py
- ExtractionStatus
- conftest.py
- doses/router.py
- offline.js
- files.py
- identity/router.py
- deps.py
- DbSession
- supply/router.py
- hooks.js
- VisitPrep.jsx
- Extraction evaluation
- demo_login
- main.jsx
- export.py
- export_data
- install.js
- FastEmbedEmbedder
- Embedder
- login_with_google
- sw-template.js

## God Nodes (most connected - your core abstractions)
1. `User` - 73 edges
2. `get_settings()` - 61 edges
3. `csrf()` - 52 edges
4. `utcnow()` - 38 edges
5. `Base` - 38 edges
6. `IdMixin` - 33 edges
7. `NotFound` - 32 edges
8. `Medication` - 31 edges
9. `Architecture Decision Records` - 26 edges
10. `record()` - 25 edges

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

## Communities (182 total, 39 thin omitted)

### Community 0 - "test_diet_notes.py"
Cohesion: 0.25
Nodes (22): build_pdf(), drain(), Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works(), test_review_then_confirm_creates_notes() (+14 more)

### Community 1 - "records/service.py"
Cohesion: 0.09
Nodes (74): NotFound, _record_line(), build_export(), AsyncSession, Medication, delete_diet_note(), delete_lab_result(), get_lab_trend() (+66 more)

### Community 2 - "db.py"
Cohesion: 0.14
Nodes (30): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatMessage, ChatThread, DocumentChunk (+22 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "assistant/router.py"
Cohesion: 0.20
Nodes (20): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+12 more)

### Community 6 - "router.jsx"
Cohesion: 0.08
Nodes (4): AppLayout(), AuthLayout(), MarketingLayout(), RouteError()

### Community 7 - "assistant/service.py"
Cohesion: 0.12
Nodes (27): answer_stream(), _best_snippet(), build_prompt(), _clock(), compose_offline(), create_thread(), _day(), describe_medication() (+19 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.18
Nodes (32): Conflict, encrypt(), Any, Request, Stage an audit row in the caller's transaction (committed with the business…, record(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008). (+24 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.08
Nodes (26): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+18 more)

### Community 10 - "documents/service.py"
Cohesion: 0.26
Nodes (18): Document, create_document(), delete_document(), get_document(), get_document_by_id(), list_documents(), page_preview_png(), purge_user_files() (+10 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.11
Nodes (35): get_google(), has_sync_scopes(), pkce_pair(), Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect() (+27 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/service.py"
Cohesion: 0.16
Nodes (23): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), create_access_token(), hash_password(), needs_rehash(), UUID, Password hashing, JWT access tokens, opaque token helpers and field encryption. (+15 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.14
Nodes (27): _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload, _coerce() (+19 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.19
Nodes (12): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+4 more)

### Community 18 - "doses/service.py"
Cohesion: 0.17
Nodes (29): AdherenceDay, AdherenceOut, Counts, DoseLogOut, DoseSlot, MedicationAdherence, BaseModel, adherence() (+21 more)

### Community 19 - "timeline/service.py"
Cohesion: 0.18
Nodes (23): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+15 more)

### Community 20 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (51): Unprocessable, The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser (+43 more)

### Community 22 - "documents/router.py"
Cohesion: 0.18
Nodes (25): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+17 more)

### Community 23 - "set_auth_cookies"
Cohesion: 0.18
Nodes (21): new_opaque_token(), clear_auth_cookies(), Response, Auth cookie helpers shared by the identity and demo routers., Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), delete_account(), login() (+13 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "heuristic.py"
Cohesion: 0.12
Nodes (27): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+19 more)

### Community 26 - "search/service.py"
Cohesion: 0.16
Nodes (16): CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession, BaseModel (+8 more)

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

### Community 33 - "test_eval.py"
Cohesion: 0.17
Nodes (20): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+12 more)

### Community 34 - "extraction/schemas.py"
Cohesion: 0.18
Nodes (16): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, ExtractedCareAction, ExtractedDietNote, ExtractionOut (+8 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.11
Nodes (18): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+10 more)

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
Cohesion: 0.19
Nodes (23): User, MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, BaseModel, field_validator, RefillIn, SupplyIn, SupplyOut (+15 more)

### Community 41 - "test_google_signin.py"
Cohesion: 0.13
Nodes (20): FakeGoogleClient, GoogleIdentity, In-memory Google for demos and tests. State is per access token and per…, google_sign_in(), AsyncClient, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017. (+12 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.15
Nodes (32): datetime, utcnow(), Gone, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, create_share(), post, PublicDocument (+24 more)

### Community 45 - ".dispatch"
Cohesion: 0.48
Nodes (4): Request, Response, constant_time_equals(), RequestResponseEndpoint

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
Nodes (17): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+9 more)

### Community 52 - "SupplyDialog.jsx"
Cohesion: 0.25
Nodes (13): supplyKeys, useClearSupply(), useRefill(), useSetSupply(), useSupplyMutation(), leftLabel(), runsOutLabel(), trim() (+5 more)

### Community 53 - "api service (alembic + uvicorn)"
Cohesion: 0.25
Nodes (11): CI Backend job (ruff + pytest on pgvector Postgres), CI Docker images build job, CI E2E job (Playwright + axe, fake providers), CI Frontend job (lint + Vitest + build), api service (alembic + uvicorn), x-backend-env shared env anchor, postgres service (pgvector/pgvector:pg17), redis service (+3 more)

### Community 54 - "lib/format.js"
Cohesion: 0.38
Nodes (8): firstName(), formatBytes(), formatClock(), formatDate(), formatRelativeDay(), greeting(), timeAgo(), toDate()

### Community 56 - "Getting started"
Cohesion: 0.25
Nodes (8): Deploy, Enable Google sign-in, Calendar & Tasks (optional), Enable real AI extraction (optional), Getting started, Prerequisites, Run everything, Run tests, What works without any API keys

### Community 57 - "test_timeline_dashboard.py"
Cohesion: 0.22
Nodes (11): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets() (+3 more)

### Community 58 - "helpers.js"
Cohesion: 0.23
Nodes (7): here, SAMPLE, expectAccessible(), signUp(), startDemo(), here, LAB_SAMPLE

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "confirm"
Cohesion: 0.25
Nodes (15): set_status(), process_document(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction(), latest_for_document() (+7 more)

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
Cohesion: 0.12
Nodes (27): get_settings(), Application settings, loaded from environment variables (and `.env` in…, install_error_handlers(), configure_logging(), Logging configuration., CSRFMiddleware, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests… (+19 more)

### Community 141 - "samples.py"
Cohesion: 0.31
Nodes (9): build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every…, A 'photo' of the prescription: rasterized, so it has no text layer. (+1 more)

### Community 142 - "extraction/router.py"
Cohesion: 0.40
Nodes (9): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+1 more)

### Community 143 - "test_labs.py"
Cohesion: 0.31
Nodes (13): build_lab_pdf(), lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_split_line_lab_tables(), test_labs_are_private_and_deletable() (+5 more)

### Community 144 - "test_assistant.py"
Cohesion: 0.28
Nodes (16): chunk_pages(), classify(), Split page text into overlapping chunks on line boundaries; chunks never span…, ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited() (+8 more)

### Community 145 - "test_doses.py"
Cohesion: 0.37
Nodes (13): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_demo_history_and_ask(), test_dose_logs_are_private() (+5 more)

### Community 146 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 147 - "audit/service.py"
Cohesion: 0.22
Nodes (11): list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage, BaseModel, list_for_user() (+3 more)

### Community 148 - "test_supply.py"
Cohesion: 0.24
Nodes (19): _at(), estimate(), date, datetime, Pure: the estimate for one medicine at `now` (an aware datetime in the user's…, _count(), _med(), _now() (+11 more)

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "corpus.py"
Cohesion: 0.24
Nodes (14): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+6 more)

### Community 151 - "csrf"
Cohesion: 0.49
Nodes (10): csrf(), _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date() (+2 more)

### Community 152 - "errors.py"
Cohesion: 0.09
Nodes (17): AppError, Forbidden, PayloadTooLarge, _problem(), Any, Exception, FastAPI, Request (+9 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "ratelimit.py"
Cohesion: 0.20
Nodes (6): client_ip(), _get_store(), _MemoryStore, Request, Fixed-window rate limiting. Uses Redis when `QUEUE_MODE=arq` (multi-process…, _RedisStore

### Community 156 - "demo/service.py"
Cohesion: 0.18
Nodes (14): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, Seed demo records for a new simulated account; never let seeding block a sign-… (+6 more)

### Community 157 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 159 - "conftest.py"
Cohesion: 0.36
Nodes (8): reset_rate_limits(), auth_client(), _clean_tables(), client(), AsyncClient, Test harness: real Postgres (pgvector), fakes for every external service., _schema(), fixture

### Community 160 - "doses/router.py"
Cohesion: 0.28
Nodes (12): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+4 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 163 - "identity/router.py"
Cohesion: 0.19
Nodes (9): Any, rate_limit(), LoginIn, ProfileUpdate, BaseModel, field_validator, SignupIn, UserOut (+1 more)

### Community 164 - "deps.py"
Cohesion: 0.33
Nodes (10): get_session(), AsyncSession, _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, Shared FastAPI dependencies. (+2 more)

### Community 166 - "DbSession"
Cohesion: 0.27
Nodes (12): list_shares(), open_share(), CurrentUser, DbSession, delete, get, Request, Response (+4 more)

### Community 167 - "supply/router.py"
Cohesion: 0.30
Nodes (11): clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get, post, put (+3 more)

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 170 - "Extraction evaluation"
Cohesion: 0.33
Nodes (6): Extraction evaluation, Method, Metrics, Results: offline extractor, Running it, What the evaluation found, and what changed

### Community 171 - "demo_login"
Cohesion: 0.40
Nodes (5): demo_login(), DbSession, post, Request, Response

### Community 172 - "main.jsx"
Cohesion: 0.32
Nodes (4): Providers(), router, ADR-0025, queryClient

### Community 174 - "export_data"
Cohesion: 0.33
Nodes (7): export_data(), me(), CurrentUser, get, patch, Everything this account holds, as one JSON file (tokens and secrets excluded)., update_profile()

### Community 175 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

## Knowledge Gaps
- **217 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+212 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `db.py`, `assistant/service.py`, `documents/service.py`, `integrations/router.py`, `identity/service.py`, `extraction/service.py`, `documents/router.py`, `set_auth_cookies`, `errors.py`, `test_integrations.py`, `demo/service.py`, `ratelimit.py`, `env.py`, `identity/router.py`, `deps.py`, `llm.py`, `demo_login`, `sharing/service.py`, `.dispatch`, `test_timeline_dashboard.py`, `Settings`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `records/service.py`, `db.py`, `identity/router.py`, `deps.py`, `assistant/service.py`, `integrations/service.py`, `test_google_signin.py`, `sharing/service.py`, `export.py`, `identity/service.py`, `extraction/service.py`, `doses/service.py`, `login_with_google`, `test_supply.py`, `timeline/service.py`, `visits/service.py`, `demo/service.py`, `confirm`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_diet_notes.py`, `test_google_signin.py`, `test_labs.py`, `test_assistant.py`, `test_doses.py`, `test_auth.py`, `test_sharing.py`, `test_supply.py`, `test_timeline_dashboard.py`, `test_integrations.py`, `conftest.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Base` (e.g. with `_clean_tables()` and `_schema()`) actually correct?**
  _`Base` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _217 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `records/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0861244019138756 - nodes in this community are weakly interconnected._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._