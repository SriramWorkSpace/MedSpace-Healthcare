# Graph Report - MedSpace  (2026-10-03)

## Corpus Check
- 310 files · ~127,572 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2472 nodes · 6119 edges · 185 communities (144 shown, 41 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ab70b525`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_labs.py
- User
- db.py
- dependencies
- devDependencies
- search/service.py
- router.jsx
- assistant/router.py
- integrations/service.py
- Architecture Decision Records
- doses/service.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- identity/router.py
- extraction/service.py
- FeatureBento.jsx
- auth.jsx
- test_eval.py
- assistant/service.py
- LLMError
- visits/service.py
- documents/router.py
- ratelimit.py
- mapping.js
- heuristic.py
- audit/router.py
- supply/service.py
- EasterEggs.jsx
- google.py
- reminders/service.py
- SearchPalette.jsx
- integrations/api.js
- score.py
- extraction/router.py
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- supply/router.py
- csrf
- MedSpace
- sharing/service.py
- visits/api.js
- timeline/service.py
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
- main.py
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
- circle/service.py
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
- test_ratelimit.py
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
- SecuritySettings.jsx
- ReminderSettings.jsx
- test_integrations.py
- corpus.py
- GoogleClient
- timedelta
- FakeGoogleClient
- circle/api.js
- push.js
- MedicationHistory.jsx
- confirm
- Medication
- seed_family
- doses/api.js
- HashEmbedder
- demo/service.py
- test_visits.py
- env.py
- extraction/jobs.py
- deps.py
- offline.js
- export.py
- demo_login
- Embedder
- identity/service.py
- hooks.js
- VisitPrep.jsx
- Extraction evaluation
- main.jsx
- files.py
- CircleAccept.jsx
- install.js
- S3Storage
- documents/service.py
- sw-template.js
- FastEmbedEmbedder
- ObjectStorage
- get_settings

## God Nodes (most connected - your core abstractions)
1. `User` - 107 edges
2. `csrf()` - 78 edges
3. `get_settings()` - 74 edges
4. `utcnow()` - 59 edges
5. `Base` - 45 edges
6. `NotFound` - 41 edges
7. `IdMixin` - 40 edges
8. `record()` - 36 edges
9. `Medication` - 32 edges
10. `signup()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `share_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/sharing/service.py → backend/app/core/config.py
- `_clean_tables()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `_schema()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `check_second_factor()` --uses--> `AppError`  [INFERRED]
  backend/app/modules/identity/security.py → backend/app/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (185 total, 41 thin omitted)

### Community 0 - "test_labs.py"
Cohesion: 0.05
Nodes (95): chunk_pages(), Split page text into overlapping chunks on line boundaries; chunks never span…, build_lab_pdf(), build_pdf(), build_scan_png(), _diabetes(), issued(), LabReport (+87 more)

### Community 1 - "User"
Cohesion: 0.16
Nodes (32): utcnow(), Conflict, Unauthorized, decode_purpose_token(), encrypt(), hash_password(), verify_password(), User (+24 more)

### Community 2 - "db.py"
Cohesion: 0.14
Nodes (30): Base, IdMixin, datetime, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, AuditLog (+22 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "search/service.py"
Cohesion: 0.15
Nodes (18): DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery() (+10 more)

### Community 6 - "router.jsx"
Cohesion: 0.08
Nodes (4): AppLayout(), AuthLayout(), MarketingLayout(), RouteError()

### Community 7 - "assistant/router.py"
Cohesion: 0.19
Nodes (20): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+12 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.22
Nodes (27): get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _clock(), _delete_remote(), disconnect() (+19 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.07
Nodes (30): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+22 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (40): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+32 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.11
Nodes (34): constant_time_equals(), has_sync_scopes(), pkce_pair(), True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect(), _frontend() (+26 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/router.py"
Cohesion: 0.10
Nodes (55): clear_auth_cookies(), Response, Auth cookie helpers shared by the identity and demo routers., Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), change_password(), _current_session(), delete_account() (+47 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.12
Nodes (30): ExtractionStatus, StrEnum, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt() (+22 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 18 - "test_eval.py"
Cohesion: 0.17
Nodes (18): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, ExtractedMedication, FollowUp, Prescriber (+10 more)

### Community 19 - "assistant/service.py"
Cohesion: 0.13
Nodes (29): ChatMessage, answer_stream(), _best_snippet(), build_prompt(), classify(), _clock(), compose_offline(), create_thread() (+21 more)

### Community 20 - "LLMError"
Cohesion: 0.31
Nodes (5): GroqProvider, LLMError, _parse_json(), Any, Exception

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (50): The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser, DbSession (+42 more)

### Community 22 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.11
Nodes (24): RateLimited, caller_key(), check(), client_ip(), Decision, Any, Request, Response (+16 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "heuristic.py"
Cohesion: 0.14
Nodes (22): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+14 more)

### Community 26 - "audit/router.py"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 27 - "supply/service.py"
Cohesion: 0.28
Nodes (17): SupplyOut, clear_supply(), list_supplies(), _out(), AsyncSession, UUID, ZoneInfo, Medication supply (ADR-023): estimate what's left from the user's own count.… (+9 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "google.py"
Cohesion: 0.16
Nodes (6): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, Consent was revoked or the refresh token is no longer valid.

### Community 30 - "reminders/service.py"
Cohesion: 0.05
Nodes (83): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+75 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "score.py"
Cohesion: 0.21
Nodes (16): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+8 more)

### Community 34 - "extraction/router.py"
Cohesion: 0.35
Nodes (10): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+2 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.10
Nodes (21): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+13 more)

### Community 36 - "records/service.py"
Cohesion: 0.09
Nodes (70): NotFound, build_export(), AsyncSession, delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription(), list_care_actions() (+62 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.21
Nodes (8): APP_LINKS, AppNav(), OWNER_ONLY, MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "supply/router.py"
Cohesion: 0.20
Nodes (15): clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get, post, put (+7 more)

### Community 41 - "csrf"
Cohesion: 0.05
Nodes (104): reset_rate_limits(), code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), provisioning_uri() (+96 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.11
Nodes (40): A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, create_share(), list_shares(), open_share(), CurrentUser, DbSession, delete (+32 more)

### Community 45 - "timeline/service.py"
Cohesion: 0.16
Nodes (25): DocumentKind, StrEnum, get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get (+17 more)

### Community 46 - "Deploying MedSpace"
Cohesion: 0.29
Nodes (7): 1. Database: Neon (or any Postgres 15+ with pgvector), 2. Object storage: Cloudflare R2 (or AWS S3), 3. API: one container, 4. Web: static build with an `/api` rewrite, 5. Google OAuth (optional), Checklist, Deploying MedSpace

### Community 47 - "AuthForms.jsx"
Cohesion: 0.19
Nodes (11): DemoDivider(), LoginForm(), loginSchema, MfaStep(), SignupForm(), signupSchema, useAuthMutation(), GOOGLE_ERRORS (+3 more)

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
Cohesion: 0.16
Nodes (8): RFC-6238, here, SAMPLE, expectAccessible(), signUp(), startDemo(), here, LAB_SAMPLE

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "main.py"
Cohesion: 0.13
Nodes (21): install_error_handlers(), FastAPI, CSRFMiddleware, BaseHTTPMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests… (+13 more)

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

### Community 80 - "circle/service.py"
Cohesion: 0.09
Nodes (50): AppError, Forbidden, Gone, _problem(), Any, Exception, Request, Domain errors rendered as RFC 9457 `application/problem+json`. (+42 more)

### Community 83 - "Field.jsx"
Cohesion: 0.29
Nodes (3): Input, Select, Textarea

### Community 84 - "theme.jsx"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

### Community 115 - "test_ratelimit.py"
Cohesion: 0.12
Nodes (19): _estimate(), get_store(), MemoryStore, Single-process store (tests, local development). `clock` is injectable for…, RedisStore, fake_clock(), _login(), AsyncClient (+11 more)

### Community 135 - "DoseStrip.jsx"
Cohesion: 0.29
Nodes (7): describe(), DoseStrip(), daySummary(), fillDays(), percent(), STATE_LABELS, TONE_CLASS

### Community 136 - "VisitBrief.jsx"
Cohesion: 0.50
Nodes (3): CHANGE_LABELS, label(), VisitBrief()

### Community 137 - "test_search.py"
Cohesion: 0.49
Nodes (9): AsyncClient, search(), test_document_text_matches_with_snippets(), test_no_matches_and_validation(), test_partial_names_find_medications(), test_prescribers_and_clinics(), test_search_is_private(), test_search_requires_auth() (+1 more)

### Community 140 - "SecuritySettings.jsx"
Cohesion: 0.19
Nodes (20): ADR-0029, securityKeys, useChangePassword(), useDisableMfa(), useEnableMfa(), useEndOtherSessions(), useEndSession(), useNewRecoveryCodes() (+12 more)

### Community 141 - "ReminderSettings.jsx"
Cohesion: 0.44
Nodes (7): pushKeys, usePushConfig(), usePushSettings(), useSavePushSettings(), useSendTest(), LEADS, ReminderSettings()

### Community 142 - "test_integrations.py"
Cohesion: 0.30
Nodes (15): decrypt(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 143 - "corpus.py"
Cohesion: 0.24
Nodes (14): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+6 more)

### Community 144 - "GoogleClient"
Cohesion: 0.12
Nodes (4): GoogleClient, Any, Protocol, Tokens

### Community 145 - "timedelta"
Cohesion: 0.26
Nodes (19): _at(), estimate(), date, datetime, Pure: the estimate for one medicine at `now` (an aware datetime in the user's…, _count(), _med(), _now() (+11 more)

### Community 147 - "circle/api.js"
Cohesion: 0.25
Nodes (12): ActingBanner(), circleKeys, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite(), useRemoveLink() (+4 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "confirm"
Cohesion: 0.35
Nodes (12): set_status(), process_document(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction(), latest_for_document() (+4 more)

### Community 151 - "Medication"
Cohesion: 0.25
Nodes (10): CareAction, DietNote, LabResult, Medication, Prescription, Confirmed health records: the source of truth for schedules, timeline, sync and…, A diet, food or drink instruction copied from a confirmed document. Tied to the…, One test result copied from a confirmed lab report (ADR-020). value_text and… (+2 more)

### Community 152 - "seed_family"
Cohesion: 0.24
Nodes (6): create_demo_account(), A fictional family member who added the demo user to her care circle as a…, seed_family(), field_validator, SignupIn, create_user()

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 156 - "demo/service.py"
Cohesion: 0.24
Nodes (11): CareLink, Care circle: people a user lets see (or help with) their records (ADR-026)., An invitation and, once accepted, a grant from `owner` to `caregiver`.…, _ingest(), _page_texts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-… (+3 more)

### Community 157 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 158 - "env.py"
Cohesion: 0.32
Nodes (7): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 159 - "extraction/jobs.py"
Cohesion: 0.25
Nodes (6): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, DocumentStatus, Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

### Community 160 - "deps.py"
Cohesion: 0.33
Nodes (11): _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, UUID, Shared FastAPI dependencies. (+3 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 163 - "demo_login"
Cohesion: 0.40
Nodes (5): demo_login(), DbSession, post, Request, Response

### Community 166 - "identity/service.py"
Cohesion: 0.12
Nodes (28): create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), _fernet(), needs_rehash(), new_opaque_token(), UUID (+20 more)

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 170 - "Extraction evaluation"
Cohesion: 0.33
Nodes (6): Extraction evaluation, Method, Metrics, Results: offline extractor, Running it, What the evaluation found, and what changed

### Community 172 - "main.jsx"
Cohesion: 0.21
Nodes (5): Providers(), router, ApiError, ADR-0025, queryClient

### Community 173 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 175 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 177 - "S3Storage"
Cohesion: 0.25
Nodes (3): ServiceUnavailable, Any S3-compatible store (MinIO, Cloudflare R2, AWS S3). boto3 calls run in a…, S3Storage

### Community 178 - "documents/service.py"
Cohesion: 0.21
Nodes (21): PayloadTooLarge, UnsupportedMedia, Document, DocumentPage, create_document(), delete_document(), get_document(), get_document_by_id() (+13 more)

### Community 186 - "get_settings"
Cohesion: 0.14
Nodes (19): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., purge_expired_demo_accounts(), Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, LLM port and the Groq adapter (ADR-003). When `LLM_PROVIDER=fake` (the default)…, enqueue() (+11 more)

## Knowledge Gaps
- **239 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+234 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `db.py`, `integrations/service.py`, `doses/service.py`, `extraction/service.py`, `timedelta`, `assistant/service.py`, `visits/service.py`, `confirm`, `seed_family`, `supply/service.py`, `demo/service.py`, `reminders/service.py`, `extraction/jobs.py`, `deps.py`, `export.py`, `records/service.py`, `identity/service.py`, `csrf`, `sharing/service.py`, `timeline/service.py`, `circle/service.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `User`, `db.py`, `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `extraction/service.py`, `assistant/service.py`, `documents/router.py`, `ratelimit.py`, `demo/service.py`, `google.py`, `reminders/service.py`, `env.py`, `demo_login`, `identity/service.py`, `sharing/service.py`, `S3Storage`, `documents/service.py`, `test_timeline_dashboard.py`, `Settings`, `main.py`, `circle/service.py`, `test_ratelimit.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_labs.py`, `test_integrations.py`, `timedelta`, `test_ratelimit.py`, `test_timeline_dashboard.py`, `test_visits.py`, `reminders/service.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 47 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 47 INFERRED edges - model-reasoned connections that need verification._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _239 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_labs.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0512521840419336 - nodes in this community are weakly interconnected._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13588850174216027 - nodes in this community are weakly interconnected._