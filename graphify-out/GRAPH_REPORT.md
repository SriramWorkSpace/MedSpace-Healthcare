# Graph Report - MedSpace  (2026-10-03)

## Corpus Check
- 310 files · ~131,162 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2454 nodes · 6102 edges · 189 communities (149 shown, 40 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c02bd32`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_diet_notes.py
- User
- db.py
- dependencies
- devDependencies
- records/models.py
- router.jsx
- push.py
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
- HttpGoogleClient
- assistant/service.py
- LLMError
- visits/service.py
- documents/router.py
- ratelimit.py
- mapping.js
- test_eval.py
- extraction/schemas.py
- test_labs.py
- EasterEggs.jsx
- labs.py
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
- supply/service.py
- test_account_security.py
- MedSpace
- sharing/service.py
- visits/api.js
- timedelta
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
- get_settings
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
- FakeGoogleClient
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
- csrf
- vite.config.js
- medspace-api
- @phosphor-icons/react
- test_integrations.py
- test_sharing.py
- tailwindcss
- @testing-library/react
- vitest
- DoseStrip.jsx
- VisitBrief.jsx
- test_search.py
- clinician.js
- SecuritySettings.jsx
- ReminderSettings.jsx
- test_assistant.py
- corpus.py
- test_visits.py
- GoogleClient
- test_reminders.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- confirm
- conftest.py
- .dispatch
- doses/api.js
- embeddings.py
- demo/service.py
- acting.js
- env.py
- test_timeline_dashboard.py
- plan_items
- offline.js
- assistant/router.py
- demo/router.py
- _problem
- identity/service.py
- ApiError
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
- extraction/jobs.py
- ObjectStorage
- uuid7
- react-router
- zod
- globals
- @testing-library/user-event

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
- `reprocess_document()` --uses--> `Conflict`  [INFERRED]
  backend/app/modules/documents/router.py → backend/app/core/errors.py
- `callback()` --uses--> `Conflict`  [INFERRED]
  backend/app/modules/integrations/router.py → backend/app/core/errors.py
- `disconnect()` --uses--> `Conflict`  [INFERRED]
  backend/app/modules/integrations/service.py → backend/app/core/errors.py
- `score_case()` --uses--> `Case`  [INFERRED]
  backend/app/eval/score.py → backend/app/eval/corpus.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (189 total, 40 thin omitted)

### Community 0 - "test_diet_notes.py"
Cohesion: 0.23
Nodes (23): build_pdf(), drain(), Background job dispatch. `QUEUE_MODE=arq`: jobs go to Redis and run in the…, Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works() (+15 more)

### Community 1 - "User"
Cohesion: 0.05
Nodes (104): get_session(), AsyncSession, datetime, utcnow(), _authenticated(), _extract_token(), get_current_user(), get_optional_user() (+96 more)

### Community 2 - "db.py"
Cohesion: 0.12
Nodes (34): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for… (+26 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "records/models.py"
Cohesion: 0.11
Nodes (25): CareAction, DietNote, LabResult, Prescription, Confirmed health records: the source of truth for schedules, timeline, sync and…, A diet, food or drink instruction copied from a confirmed document. Tied to the…, One test result copied from a confirmed lab report (ADR-020). value_text and…, Create records from a confirmed review, replacing earlier confirmations of the… (+17 more)

### Community 6 - "router.jsx"
Cohesion: 0.25
Nodes (4): AppLayout(), AuthLayout(), MarketingLayout(), RouteError()

### Community 7 - "push.py"
Cohesion: 0.14
Nodes (20): _b64url(), FakePushSender, generate_vapid_keys(), get_push_sender(), PushSender, Protocol, Web Push port (ADR-028): a real sender (pywebpush + VAPID) and a fake for dev,…, Tests swap in their own sender (None resets to the configured one). (+12 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.28
Nodes (23): encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), _delete_remote(), disconnect(), get_connection() (+15 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.07
Nodes (30): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+22 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (40): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+32 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.11
Nodes (35): constant_time_equals(), has_sync_scopes(), pkce_pair(), Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect() (+27 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/router.py"
Cohesion: 0.09
Nodes (55): RateLimited, decode_purpose_token(), clear_auth_cookies(), Response, change_password(), _current_session(), delete_account(), end_other_sessions() (+47 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.12
Nodes (29): ExtractionStatus, StrEnum, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt() (+21 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.21
Nodes (13): getActing(), setActing(), api(), NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler() (+5 more)

### Community 18 - "HttpGoogleClient"
Cohesion: 0.17
Nodes (5): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, Consent was revoked or the refresh token is no longer valid.

### Community 19 - "assistant/service.py"
Cohesion: 0.12
Nodes (34): ChatMessage, answer_stream(), _best_snippet(), build_prompt(), chunk_pages(), classify(), _clock(), compose_offline() (+26 more)

### Community 20 - "LLMError"
Cohesion: 0.31
Nodes (5): GroqProvider, LLMError, _parse_json(), Any, Exception

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (50): The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser, DbSession (+42 more)

### Community 22 - "documents/router.py"
Cohesion: 0.17
Nodes (26): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+18 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.10
Nodes (22): caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore, Any (+14 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "test_eval.py"
Cohesion: 0.10
Nodes (32): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+24 more)

### Community 26 - "extraction/schemas.py"
Cohesion: 0.18
Nodes (16): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, ExtractedCareAction, ExtractedDietNote, ExtractionOut (+8 more)

### Community 27 - "test_labs.py"
Cohesion: 0.17
Nodes (22): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+14 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 30 - "reminders/service.py"
Cohesion: 0.09
Nodes (52): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+44 more)

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
Nodes (9): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+1 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.10
Nodes (21): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+13 more)

### Community 36 - "records/service.py"
Cohesion: 0.09
Nodes (69): NotFound, build_export(), AsyncSession, delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription(), list_care_actions() (+61 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.21
Nodes (8): APP_LINKS, AppNav(), OWNER_ONLY, MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "supply/service.py"
Cohesion: 0.07
Nodes (63): Account data export: one JSON document with every record the user owns.…, MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies(), CurrentUser, DbSession, delete (+55 more)

### Community 41 - "test_account_security.py"
Cohesion: 0.07
Nodes (73): code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), provisioning_uri(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).… (+65 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.11
Nodes (42): Gone, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, create_share(), list_shares(), open_share(), CurrentUser, DbSession (+34 more)

### Community 45 - "timedelta"
Cohesion: 0.34
Nodes (14): _count(), _med(), _now(), AsyncClient, datetime, Medication supply: estimates from the user's own count, the schedule and…, test_count_refill_and_clear(), test_counts_scheduled_doses_since_the_count() (+6 more)

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

### Community 57 - "LocalStorage"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 58 - "helpers.js"
Cohesion: 0.16
Nodes (8): RFC-6238, here, SAMPLE, expectAccessible(), signUp(), startDemo(), here, LAB_SAMPLE

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "get_settings"
Cohesion: 0.10
Nodes (31): get_settings(), Application settings, loaded from environment variables (and `.env` in…, install_error_handlers(), FastAPI, ServiceUnavailable, configure_logging(), Logging configuration., CSRFMiddleware (+23 more)

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

### Community 83 - "Field.jsx"
Cohesion: 0.29
Nodes (3): Input, Select, Textarea

### Community 84 - "theme.jsx"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

### Community 115 - "test_ratelimit.py"
Cohesion: 0.24
Nodes (13): fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings(), test_baseline_budget_covers_every_route(), test_headers_scale_and_disable() (+5 more)

### Community 117 - "csrf"
Cohesion: 0.54
Nodes (13): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+5 more)

### Community 127 - "test_integrations.py"
Cohesion: 0.41
Nodes (12): decrypt(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation…, test_callback_rejects_forged_state(), test_completed_tasks_flow_back() (+4 more)

### Community 128 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

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

### Community 142 - "test_assistant.py"
Cohesion: 0.38
Nodes (13): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+5 more)

### Community 143 - "corpus.py"
Cohesion: 0.26
Nodes (13): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+5 more)

### Community 144 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 145 - "GoogleClient"
Cohesion: 0.12
Nodes (4): GoogleClient, Any, Protocol, Tokens

### Community 146 - "test_reminders.py"
Cohesion: 0.23
Nodes (23): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+15 more)

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

### Community 151 - "conftest.py"
Cohesion: 0.36
Nodes (8): reset_rate_limits(), auth_client(), _clean_tables(), client(), AsyncClient, fixture, Test harness: real Postgres (pgvector), fakes for every external service., _schema()

### Community 152 - ".dispatch"
Cohesion: 0.60
Nodes (3): Request, Response, RequestResponseEndpoint

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "embeddings.py"
Cohesion: 0.14
Nodes (7): Embedder, FastEmbedEmbedder, HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and…

### Community 156 - "demo/service.py"
Cohesion: 0.27
Nodes (14): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+6 more)

### Community 157 - "acting.js"
Cohesion: 0.33
Nodes (3): ADR-0026, acting, listeners

### Community 158 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 159 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 160 - "plan_items"
Cohesion: 0.25
Nodes (8): appointment_event(), _clock(), dose_event(), plan_items(), Planned, _rrule(), task_body(), test_dose_event_shape()

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "assistant/router.py"
Cohesion: 0.19
Nodes (20): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+12 more)

### Community 163 - "demo/router.py"
Cohesion: 0.18
Nodes (9): new_opaque_token(), demo_login(), DbSession, post, Request, Response, Auth cookie helpers shared by the identity and demo routers., Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in… (+1 more)

### Community 164 - "_problem"
Cohesion: 0.50
Nodes (3): _problem(), Any, Request

### Community 166 - "identity/service.py"
Cohesion: 0.12
Nodes (28): create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), _fernet(), hash_password(), needs_rehash(), UUID (+20 more)

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
Cohesion: 0.32
Nodes (4): Providers(), router, ADR-0025, queryClient

### Community 173 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 175 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 178 - "documents/service.py"
Cohesion: 0.19
Nodes (22): PayloadTooLarge, Domain errors rendered as RFC 9457 `application/problem+json`., UnsupportedMedia, Document, create_document(), delete_document(), get_document(), get_document_by_id() (+14 more)

### Community 181 - "extraction/jobs.py"
Cohesion: 0.33
Nodes (4): Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

### Community 183 - "uuid7"
Cohesion: 0.67
Nodes (3): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7()

## Knowledge Gaps
- **240 isolated node(s):** `Phase 0: Foundations`, `Phase 1: Core platform + design system`, `Phase 2: Documents + processing pipeline`, `Phase 3: Prescription intelligence (extract → review → confirm)`, `Phase 4: Dashboard, medications, timeline` (+235 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `db.py`, `records/service.py`, `identity/service.py`, `supply/service.py`, `integrations/service.py`, `doses/service.py`, `sharing/service.py`, `test_account_security.py`, `timedelta`, `extraction/service.py`, `assistant/service.py`, `extraction/jobs.py`, `confirm`, `visits/service.py`, `demo/service.py`, `reminders/service.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `test_diet_notes.py`, `User`, `db.py`, `push.py`, `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `extraction/service.py`, `assistant/service.py`, `documents/router.py`, `ratelimit.py`, `.dispatch`, `embeddings.py`, `demo/service.py`, `reminders/service.py`, `env.py`, `test_timeline_dashboard.py`, `demo/router.py`, `identity/service.py`, `sharing/service.py`, `S3Storage`, `documents/service.py`, `Settings`, `test_ratelimit.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_diet_notes.py`, `test_sharing.py`, `test_timeline_dashboard.py`, `test_account_security.py`, `timedelta`, `test_assistant.py`, `test_visits.py`, `test_reminders.py`, `test_ratelimit.py`, `conftest.py`, `test_labs.py`, `test_integrations.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 47 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 47 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Phase 0: Foundations`, `Phase 1: Core platform + design system`, `Phase 2: Documents + processing pipeline` to the rest of the system?**
  _240 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `User` be split into smaller, more focused modules?**
  _Cohesion score 0.05064836003051106 - nodes in this community are weakly interconnected._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11879432624113476 - nodes in this community are weakly interconnected._