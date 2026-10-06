# Graph Report - MedSpace  (2026-10-07)

## Corpus Check
- 343 files · ~152,162 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2831 nodes · 6701 edges · 257 communities (168 shown, 89 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 438 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c1ccb264`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_pdf
- circle/service.py
- reminders/router.py
- dependencies
- devDependencies
- app/models.py
- router.jsx
- identity/security.py
- integrations/service.py
- Architecture Decision Records
- doses/service.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- identity/router.py
- ExtractionPayload
- FeatureBento.jsx
- auth.jsx
- HttpGoogleClient
- CurrentUser
- reminders/service.py
- visits/service.py
- documents/router.py
- ratelimit.py
- ReviewForm.jsx
- heuristic.py
- signup
- test_caregiver_reminders.py
- EasterEggs.jsx
- push.py
- utcnow
- SearchPalette.jsx
- integrations/api.js
- test_eval.py
- timedelta
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- Medication
- search/service.py
- MedSpace
- db.py
- visits/api.js
- records/router.py
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
- records/schemas.py
- LocalStorage
- helpers.js
- Ask.jsx
- Settings
- 4. Core flows
- Diet.jsx
- get_settings
- README.md
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
- SourceViewer.jsx
- DocumentReview.jsx
- Documents.jsx
- sharing/router.py
- csrf
- vite.config.js
- medspace-api
- @phosphor-icons/react
- test_integrations.py
- middleware.py
- tailwindcss
- @testing-library/react
- vitest
- DoseStrip.jsx
- VisitBrief.jsx
- test_search.py
- clinician.js
- SecuritySettings.jsx
- ReminderSettings.jsx
- confirm
- corpus.py
- Launch guide: the steps only you can do
- GoogleClient
- circle/router.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- locate
- conftest.py
- extraction/jobs.py
- doses/api.js
- worker.py
- documents/service.py
- extraction/service.py
- test_timeline_dashboard.py
- RecoveryForms.jsx
- assistant/router.py
- offline.js
- test_ratelimit.py
- useResendVerification
- BackgroundTasks
- hooks.js
- VisitPrep.jsx
- CurrentUser
- main.jsx
- files.py
- CircleAccept.jsx
- identity/schemas.py
- User
- sw-template.js
- StrEnum
- labs.py
- react-router
- zod
- globals
- @testing-library/user-event
- BaseHTTPMiddleware
- FastAPI
- fixture
- sharing/service.py
- test_labs.py
- test_assistant.py
- test_doses.py
- User
- llm.py
- CurrentUser
- DbSession
- get
- post
- audit/service.py
- field_validator
- Any
- Exception
- links.js
- date
- DbSession
- delete
- get
- patch
- post
- BaseModel
- date
- ZoneInfo
- fixture
- CareLink
- CareLinkOut
- CircleOut
- InviteIn
- InvitePreview
- assistant/service.py
- deps.py
- demo/service.py
- test_sharing.py
- notify/service.py
- field_validator
- install.js
- acting.js
- ObjectStorage
- ApiError
- AsyncSession
- BackgroundTasks
- CurrentUser
- DbSession
- delete
- get
- OptionalUser
- patch
- post
- UUID
- field_validator
- session_state
- smoothScroll.js
- ._https
- BaseModel
- AsyncClient
- MonkeyPatch

## God Nodes (most connected - your core abstractions)
1. `csrf()` - 96 edges
2. `User` - 92 edges
3. `utcnow()` - 63 edges
4. `get_settings()` - 62 edges
5. `signup()` - 52 edges
6. `record()` - 44 edges
7. `NotFound` - 38 edges
8. `Architecture Decision Records` - 35 edges
9. `Medication` - 32 edges
10. `MedSpace Build Plan` - 28 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `authenticate()` --calls--> `needs_rehash()`  [INFERRED]
  backend/app/modules/identity/service.py → backend/app/core/security.py
- `run_scheduled_jobs()` --indirect_call--> `session()`  [INFERRED]
  backend/app/main.py → backend/tests/conftest.py
- `lifespan()` --calls--> `configure_logging()`  [INFERRED]
  backend/app/main.py → backend/app/core/logging.py
- `lifespan()` --calls--> `warm_up()`  [INFERRED]
  backend/app/main.py → backend/app/shared/embeddings.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (257 total, 89 thin omitted)

### Community 0 - "build_pdf"
Cohesion: 0.14
Nodes (38): build_pdf(), drain(), Background job dispatch. `QUEUE_MODE=arq`: jobs go to Redis and run in the…, Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works() (+30 more)

### Community 1 - "circle/service.py"
Cohesion: 0.15
Nodes (31): Forbidden, CareLink, Base, IdMixin, TimestampMixin, Care circle: people a user lets see (or help with) their records (ADR-026)., An invitation and, once accepted, a grant from `owner` to `caregiver`.…, accept() (+23 more)

### Community 2 - "reminders/router.py"
Cohesion: 0.16
Nodes (26): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+18 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "app/models.py"
Cohesion: 0.17
Nodes (18): Import every module's ORM models so `Base.metadata` is complete (Alembic,…, CaregiverReminderLog, PushSubscription, Base, IdMixin, TimestampMixin, Dose reminders by push notification (ADR-028)., One browser (or installed app) that agreed to receive notifications. (+10 more)

### Community 6 - "router.jsx"
Cohesion: 0.18
Nodes (3): appLayout, authLayout, openAuthLayout()

### Community 7 - "identity/security.py"
Cohesion: 0.15
Nodes (29): AppError, verify_password(), provisioning_uri(), One-time backup codes for two-step verification; only hashes are stored., RecoveryCode, begin_setup(), change_password(), check_second_factor() (+21 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.18
Nodes (33): Conflict, encrypt(), Any, Request, Stage an audit row in the caller's transaction (committed with the business…, record(), get_google(), OAuthConnection (+25 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.06
Nodes (35): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+27 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (41): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+33 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.13
Nodes (31): pkce_pair(), callback(), connect(), disconnect(), _frontend(), google_sign_in(), preview(), providers() (+23 more)

### Community 12 - "documents/api.js"
Cohesion: 0.10
Nodes (13): ACTIVE, docKeys, isProcessing(), ADR-0031, previewUrl(), uploadDocument(), useDocument(), useDocuments() (+5 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/router.py"
Cohesion: 0.12
Nodes (48): clear_auth_cookies(), cancel_email_change(), change_password(), check_reset_link(), confirm_email_change(), _current_session(), delete_account(), end_other_sessions() (+40 more)

### Community 15 - "ExtractionPayload"
Cohesion: 0.12
Nodes (24): Any, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload (+16 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.21
Nodes (13): getActing(), setActing(), api(), NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler() (+5 more)

### Community 18 - "HttpGoogleClient"
Cohesion: 0.13
Nodes (9): GoogleAPIError, GoogleAuthError, GoogleIdentity, has_sync_scopes(), HttpGoogleClient, Exception, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent… (+1 more)

### Community 19 - "CurrentUser"
Cohesion: 0.17
Nodes (19): get_circle(), preview(), confirm_extraction(), discard_extraction(), get_evidence(), get_latest_extraction(), Request, UUID (+11 more)

### Community 20 - "reminders/service.py"
Cohesion: 0.17
Nodes (27): action_token(), _clock(), _deliver(), _due(), get_settings_for(), _labels(), AsyncSession, datetime (+19 more)

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (51): Unprocessable, The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser (+43 more)

### Community 22 - "documents/router.py"
Cohesion: 0.17
Nodes (26): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+18 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.10
Nodes (23): RateLimited, caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore (+15 more)

### Community 24 - "ReviewForm.jsx"
Cohesion: 0.14
Nodes (22): evidenceKeys(), findSpot(), itemName(), ADR-0031, evidence, values, blank(), CARE_KINDS (+14 more)

### Community 25 - "heuristic.py"
Cohesion: 0.11
Nodes (26): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+18 more)

### Community 26 - "signup"
Cohesion: 0.05
Nodes (113): AsyncClient, code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).… (+105 more)

### Community 27 - "test_caregiver_reminders.py"
Cohesion: 0.25
Nodes (26): alerts(), caregiver(), owner_with_medicine(), AsyncClient, Dose alerts for caregivers (ADR-032): opt-in per person, on time or "not ticked…, Eve, confirmed, in Ada's care circle with `role`, with a subscribed device., test_alert_when_due_with_actions_for_helpers(), test_alerts_are_off_until_the_caregiver_asks() (+18 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "push.py"
Cohesion: 0.14
Nodes (20): _b64url(), FakePushSender, generate_vapid_keys(), get_push_sender(), PushSender, Protocol, Web Push port (ADR-028): a real sender (pywebpush + VAPID) and a fake for dev,…, Tests swap in their own sender (None resets to the configured one). (+12 more)

### Community 30 - "utcnow"
Cohesion: 0.20
Nodes (25): AsyncSession, utcnow(), sha256_hex(), cancel_email_change(), confirm_email_change(), _consume(), EmailChange, _issue() (+17 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "test_eval.py"
Cohesion: 0.18
Nodes (19): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+11 more)

### Community 34 - "timedelta"
Cohesion: 0.05
Nodes (83): Account data export: one JSON document with every record the user owns.…, MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies(), CurrentUser, DbSession, delete (+75 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.07
Nodes (28): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+20 more)

### Community 36 - "records/service.py"
Cohesion: 0.17
Nodes (34): NotFound, build_export(), AsyncSession, DietNote, Prescription, A diet, food or drink instruction copied from a confirmed document. Tied to the…, LabResultOut, delete_diet_note() (+26 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.21
Nodes (8): APP_LINKS, AppNav(), OWNER_ONLY, MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "Medication"
Cohesion: 0.12
Nodes (25): _record_line(), Extraction, ExtractionStatus, One AI reading of a document. Versioned; only a confirmed version becomes…, EmailToken, A one-time link sent by email (ADR-030): verify an address, or reset a…, CareAction, LabResult (+17 more)

### Community 41 - "search/service.py"
Cohesion: 0.16
Nodes (16): CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession, BaseModel (+8 more)

### Community 42 - "MedSpace"
Cohesion: 0.12
Nodes (16): Architecture at a glance, Deploy, Enable Google sign-in, Calendar & Tasks (optional), Enable real AI extraction (optional), Engineering highlights, Features, Getting started, License (+8 more)

### Community 43 - "db.py"
Cohesion: 0.15
Nodes (22): Base, IdMixin, datetime, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin, uuid7() (+14 more)

### Community 45 - "records/router.py"
Cohesion: 0.33
Nodes (17): delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription(), list_care_actions(), list_diet_notes(), list_lab_trends(), list_medications() (+9 more)

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

### Community 56 - "records/schemas.py"
Cohesion: 0.22
Nodes (15): CareActionOut, CareActionUpdate, DietNoteOut, DietNotesOut, LabPoint, LabTrendDetail, LabTrendOut, MedicationFoodNote (+7 more)

### Community 57 - "LocalStorage"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 58 - "helpers.js"
Cohesion: 0.14
Nodes (10): RFC-6238, here, SAMPLE, confirmEmail(), emailLink(), expectAccessible(), signUp(), startDemo() (+2 more)

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "get_settings"
Cohesion: 0.09
Nodes (30): get_settings(), Application settings, loaded from environment variables (and `.env` in…, Logging configuration., create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), decode_purpose_token() (+22 more)

### Community 64 - "README.md"
Cohesion: 0.22
Nodes (6): Extraction evaluation, Method, Metrics, Results: offline extractor, Running it, What the evaluation found, and what changed

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

### Community 103 - "DocumentReview.jsx"
Cohesion: 0.50
Nodes (3): ADR-0031, DocumentReview(), recordLabel()

### Community 115 - "sharing/router.py"
Cohesion: 0.18
Nodes (22): create_share(), list_shares(), open_share(), CurrentUser, DbSession, delete, get, post (+14 more)

### Community 117 - "csrf"
Cohesion: 0.39
Nodes (16): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+8 more)

### Community 127 - "test_integrations.py"
Cohesion: 0.30
Nodes (15): decrypt(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 128 - "middleware.py"
Cohesion: 0.23
Nodes (10): CSRFMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware, SecurityHeadersMiddleware, constant_time_equals() (+2 more)

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
Cohesion: 0.16
Nodes (25): ADR-0029, securityKeys, useCancelEmailChange(), useChangePassword(), useDisableMfa(), useEnableMfa(), useEndOtherSessions(), useEndSession() (+17 more)

### Community 141 - "ReminderSettings.jsx"
Cohesion: 0.44
Nodes (7): pushKeys, usePushConfig(), usePushSettings(), useSavePushSettings(), useSendTest(), LEADS, ReminderSettings()

### Community 142 - "confirm"
Cohesion: 0.31
Nodes (14): set_status(), process_document(), confirm(), discard(), evidence_for_document(), get_extraction(), latest_for_document(), AsyncSession (+6 more)

### Community 143 - "corpus.py"
Cohesion: 0.26
Nodes (13): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+5 more)

### Community 144 - "Launch guide: the steps only you can do"
Cohesion: 0.14
Nodes (14): Housekeeping, Launch guide: the steps only you can do, Part 10. Keep reminders working on the free plan (5 minutes), Part 11. Final checks (15 minutes), Part 12. Make it shine on your resume, Part 1. Accounts to create (about 30 minutes), Part 2. Generate your secrets (5 minutes, on your computer), Part 3. Database: Neon (10 minutes) (+6 more)

### Community 145 - "GoogleClient"
Cohesion: 0.13
Nodes (4): GoogleClient, Any, Protocol, Tokens

### Community 146 - "circle/router.py"
Cohesion: 0.22
Nodes (19): accept(), invite(), Request, UUID, Dose alerts about someone you help: off, when due, or if not ticked after 30/60…, revoke(), set_alerts(), set_role() (+11 more)

### Community 147 - "circle/api.js"
Cohesion: 0.18
Nodes (18): ActingBanner(), circleKeys, ADR-0032, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite() (+10 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "locate"
Cohesion: 0.16
Nodes (12): _clean(), _date_variants(), locate(), _Locator, Document, Where on the page each extracted value is printed (ADR-031). Given the original…, First variant found, preferring the hinted page (or the anchor's page and…, Evidence for every field we can find: {"fields": {path: spot}, "items": {path:… (+4 more)

### Community 151 - "conftest.py"
Cohesion: 0.27
Nodes (10): reset_rate_limits(), auth_client(), _clean_tables(), client(), mailbox(), AsyncClient, Test harness: real Postgres (pgvector), fakes for every external service., Every test gets an empty simulated outbox (ADR-030). (+2 more)

### Community 152 - "extraction/jobs.py"
Cohesion: 0.13
Nodes (19): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, create_app(), lifespan(), FastAPI application factory., Inline deployments have no worker, so this does the worker's scheduled jobs:…, reminder_loop(), run_scheduled_jobs(), DocumentKind (+11 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "worker.py"
Cohesion: 0.09
Nodes (17): configure_logging(), Embedder, FastEmbedEmbedder, get_embedder(), HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,… (+9 more)

### Community 156 - "documents/service.py"
Cohesion: 0.10
Nodes (32): AppError, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI, Request (+24 more)

### Community 157 - "extraction/service.py"
Cohesion: 0.19
Nodes (20): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, EvidenceSpot, ExtractedCareAction, ExtractedDietNote (+12 more)

### Community 158 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 160 - "assistant/router.py"
Cohesion: 0.21
Nodes (16): AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel, CurrentUser (+8 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "test_ratelimit.py"
Cohesion: 0.22
Nodes (14): fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings(), test_baseline_budget_covers_every_route(), test_headers_scale_and_disable() (+6 more)

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 172 - "main.jsx"
Cohesion: 0.32
Nodes (4): Providers(), router, ADR-0025, queryClient

### Community 173 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 175 - "identity/schemas.py"
Cohesion: 0.20
Nodes (17): CodeIn, DeviceSessionOut, EmailChangeIn, ForgotPasswordIn, LoginIn, LoginResult, MfaDisableIn, MfaLoginIn (+9 more)

### Community 183 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 197 - "sharing/service.py"
Cohesion: 0.20
Nodes (22): Gone, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create(), link_status(), list_links(), open_public() (+14 more)

### Community 198 - "test_labs.py"
Cohesion: 0.15
Nodes (24): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+16 more)

### Community 199 - "test_assistant.py"
Cohesion: 0.29
Nodes (16): chunk_pages(), Split page text into overlapping chunks on line boundaries; chunks never span…, ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_chunking_respects_pages_and_size() (+8 more)

### Community 200 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 201 - "User"
Cohesion: 0.17
Nodes (18): Opaque refresh token, stored hashed. Rotated on every use; reuse revokes the…, RefreshToken, User, authenticate(), delete_user(), get_user(), issue_session(), IssuedSession (+10 more)

### Community 202 - "llm.py"
Cohesion: 0.23
Nodes (9): get_llm(), GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol (+1 more)

### Community 209 - "audit/service.py"
Cohesion: 0.17
Nodes (13): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+5 more)

### Community 230 - "assistant/service.py"
Cohesion: 0.13
Nodes (31): ChatMessage, ask(), Request, Server-sent events: `sources`, then `token`*, then `done` (or `error`)., answer_stream(), _best_snippet(), build_prompt(), classify() (+23 more)

### Community 231 - "deps.py"
Cohesion: 0.31
Nodes (12): _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, UUID, Shared FastAPI dependencies. (+4 more)

### Community 233 - "demo/service.py"
Cohesion: 0.27
Nodes (15): hash_password(), create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-… (+7 more)

### Community 234 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 235 - "notify/service.py"
Cohesion: 0.10
Nodes (27): outbox(), get, Dev-only outbox: read simulated emails (local testing and e2e). Never mounted…, app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, To the address being replaced: once when a change is asked for, once when it…, _send() (+19 more)

### Community 238 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 239 - "acting.js"
Cohesion: 0.33
Nodes (3): ADR-0026, acting, listeners

### Community 255 - "session_state"
Cohesion: 0.50
Nodes (4): Who am I, without a 401 for anonymous visitors (the SPA calls this on boot). A…, session_state(), SessionState, OptionalUser

## Knowledge Gaps
- **278 isolated node(s):** `Features`, `Architecture at a glance`, `Engineering highlights`, `Tech stack`, `Prerequisites` (+273 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **89 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `timedelta`, `records/service.py`, `sharing/service.py`, `assistant/service.py`, `deps.py`, `Medication`, `demo/service.py`, `doses/service.py`, `identity/security.py`, `integrations/service.py`, `visits/service.py`, `extraction/jobs.py`, `signup`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `build_pdf`, `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `HttpGoogleClient`, `documents/router.py`, `ratelimit.py`, `worker.py`, `documents/service.py`, `push.py`, `test_timeline_dashboard.py`, `test_ratelimit.py`, `db.py`, `Settings`, `sharing/service.py`, `User`, `llm.py`, `assistant/service.py`, `demo/service.py`, `notify/service.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `build_pdf`, `test_ratelimit.py`, `timedelta`, `test_labs.py`, `test_assistant.py`, `test_doses.py`, `test_sharing.py`, `conftest.py`, `signup`, `test_caregiver_reminders.py`, `test_timeline_dashboard.py`, `test_integrations.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `csrf()` (e.g. with `change()` and `test_change_needs_the_password_and_a_code_with_two_step_on()`) actually correct?**
  _`csrf()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `User` (e.g. with `begin_setup()` and `change_password()`) actually correct?**
  _`User` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `utcnow()` (e.g. with `accept()` and `invite()`) actually correct?**
  _`utcnow()` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 47 INFERRED edges - model-reasoned connections that need verification._