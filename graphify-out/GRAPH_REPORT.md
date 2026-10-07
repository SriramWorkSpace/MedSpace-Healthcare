# Graph Report - MedSpace  (2026-10-07)

## Corpus Check
- 351 files · ~160,084 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2898 nodes · 7274 edges · 211 communities (166 shown, 45 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db4ed76c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_eval.py
- circle/service.py
- reminders/service.py
- dependencies
- devDependencies
- records/models.py
- router.jsx
- User
- integrations/service.py
- Architecture Decision Records
- doses/service.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- DbSession
- extraction/schemas.py
- FeatureBento.jsx
- auth.jsx
- HttpGoogleClient
- test_google_live.py
- test_visits.py
- visits/service.py
- documents/router.py
- ratelimit.py
- ReviewForm.jsx
- test_labs.py
- test_email_recovery.py
- test_caregiver_reminders.py
- EasterEggs.jsx
- worker.py
- utcnow
- SearchPalette.jsx
- integrations/api.js
- score.py
- supply/service.py
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- signup
- documents/service.py
- MedSpace
- db.py
- visits/api.js
- test_auth.py
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- Visits.jsx
- scripts
- test_evidence.py
- SupplyDialog.jsx
- api service (alembic + uvicorn)
- lib/format.js
- Settings.jsx
- test_google_signin.py
- drain
- helpers.js
- Ask.jsx
- assistant/router.py
- 4. Core flows
- Diet.jsx
- identity/router.py
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
- demo/router.py
- csrf
- vite.config.js
- medspace-api
- @phosphor-icons/react
- test_integrations.py
- conftest.py
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
- _Locator
- test_timeline_dashboard.py
- main.py
- doses/api.js
- test_sharing.py
- files.py
- safe_path
- demo/service.py
- RecoveryForms.jsx
- test_authorization_sweep.py
- offline.js
- test_ratelimit.py
- useResendVerification
- ProfileUpdate
- hooks.js
- VisitPrep.jsx
- audit/router.py
- main.jsx
- S3Storage
- CircleAccept.jsx
- install.js
- totp.py
- session_state
- sw-template.js
- vercel.json
- labs.py
- react-router
- zod
- globals
- @testing-library/user-event
- get_settings
- env.py
- test_assistant.py
- test_doses.py
- identity/service.py
- extraction/service.py
- embeddings.py
- links.js
- assistant/service.py
- errors.py
- test_email_change.py
- notify/service.py
- smoothScroll.js

## God Nodes (most connected - your core abstractions)
1. `User` - 126 edges
2. `csrf()` - 113 edges
3. `get_settings()` - 93 edges
4. `utcnow()` - 76 edges
5. `signup()` - 57 edges
6. `Base` - 47 edges
7. `NotFound` - 45 edges
8. `record()` - 44 edges
9. `IdMixin` - 42 edges
10. `Architecture Decision Records` - 39 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `invite_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/circle/service.py → backend/app/core/config.py
- `share_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/sharing/service.py → backend/app/core/config.py
- `_clean_tables()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `_schema()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (211 total, 45 thin omitted)

### Community 0 - "test_eval.py"
Cohesion: 0.09
Nodes (41): ambiguous_date(), _apply_sig(), _dosing(), extract(), _lab_results(), _lab_row(), _medication_from_line(), _parse_date() (+33 more)

### Community 1 - "circle/service.py"
Cohesion: 0.14
Nodes (32): Unprocessable, list_for_user(), Any, AsyncSession, Request, UUID, Audit trail: `record()` is the single write path, used by every module., Stage an audit row in the caller's transaction (committed with the business… (+24 more)

### Community 2 - "reminders/service.py"
Cohesion: 0.06
Nodes (74): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+66 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "records/models.py"
Cohesion: 0.11
Nodes (25): CareAction, DietNote, LabResult, Prescription, Confirmed health records: the source of truth for schedules, timeline, sync and…, One test result copied from a confirmed lab report (ADR-020). value_text and…, A diet, food or drink instruction copied from a confirmed document. Tied to the…, Create records from a confirmed review, replacing earlier confirmations of the… (+17 more)

### Community 6 - "router.jsx"
Cohesion: 0.06
Nodes (5): MarketingLayout(), RouteError(), appLayout, authLayout, openAuthLayout()

### Community 7 - "User"
Cohesion: 0.17
Nodes (27): Forbidden, decode_purpose_token(), User, begin_setup(), change_password(), check_second_factor(), clear_second_factor(), describe_device() (+19 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.18
Nodes (34): Conflict, encrypt(), GoogleAPIError, GoogleAuthError, Exception, Consent was revoked or the refresh token is no longer valid., OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008). (+26 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.05
Nodes (39): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+31 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (40): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+32 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.09
Nodes (44): constant_time_equals(), client_for_mode(), client_for_user(), get_google(), has_sync_scopes(), _live(), live_configured(), pkce_pair() (+36 more)

### Community 12 - "documents/api.js"
Cohesion: 0.10
Nodes (13): ACTIVE, docKeys, isProcessing(), ADR-0031, previewUrl(), uploadDocument(), useDocument(), useDocuments() (+5 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "DbSession"
Cohesion: 0.16
Nodes (34): cancel_email_change(), change_password(), check_reset_link(), confirm_email_change(), _current_session(), delete_account(), end_other_sessions(), end_session() (+26 more)

### Community 15 - "extraction/schemas.py"
Cohesion: 0.12
Nodes (30): confirm_extraction(), discard_extraction(), get_evidence(), get_latest_extraction(), CurrentUser, DbSession, get, post (+22 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 18 - "HttpGoogleClient"
Cohesion: 0.18
Nodes (3): _events(), HttpGoogleClient, MedSpace's own calendar (the only one calendar.app.created can reach).

### Community 19 - "test_google_live.py"
Cohesion: 0.11
Nodes (19): connect_live(), FakeGoogleHTTP, live(), AsyncClient, fixture, Request, Response, Real Google OAuth 2.0 (GOOGLE_PROVIDER=google), with Google's HTTP endpoints… (+11 more)

### Community 20 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (50): The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser, DbSession (+42 more)

### Community 22 - "documents/router.py"
Cohesion: 0.17
Nodes (26): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+18 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.11
Nodes (21): caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore, Any (+13 more)

### Community 24 - "ReviewForm.jsx"
Cohesion: 0.14
Nodes (22): evidenceKeys(), findSpot(), itemName(), ADR-0031, evidence, values, blank(), CARE_KINDS (+14 more)

### Community 25 - "test_labs.py"
Cohesion: 0.25
Nodes (15): build_lab_pdf(), lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_single_line_rows_and_printed_flags(), test_heuristic_reads_split_line_lab_tables() (+7 more)

### Community 26 - "test_email_recovery.py"
Cohesion: 0.22
Nodes (25): FakeMailer, Keeps the last messages in memory (the dev outbox and tests read them)., forgot(), login(), AsyncClient, MonkeyPatch, Response, Email verification, password reset and security alerts (ADR-030). (+17 more)

### Community 27 - "test_caregiver_reminders.py"
Cohesion: 0.25
Nodes (26): alerts(), caregiver(), owner_with_medicine(), AsyncClient, Response, Dose alerts for caregivers (ADR-032): opt-in per person, on time or "not ticked…, Eve, confirmed, in Ada's care circle with `role`, with a subscribed device., test_alert_when_due_with_actions_for_helpers() (+18 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "worker.py"
Cohesion: 0.18
Nodes (9): Load (and on first run, download) the embedding model before the first request…, warm_up(), purge_demo_accounts(), purge_share_links(), ARQ worker entrypoint: `arq app.worker.WorkerSettings`., send_reminders(), startup(), WorkerSettings (+1 more)

### Community 30 - "utcnow"
Cohesion: 0.14
Nodes (32): datetime, utcnow(), Gone, new_opaque_token(), sha256_hex(), cancel_email_change(), confirm_email_change(), _consume() (+24 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "score.py"
Cohesion: 0.17
Nodes (17): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+9 more)

### Community 34 - "supply/service.py"
Cohesion: 0.06
Nodes (72): MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get (+64 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.07
Nodes (28): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+20 more)

### Community 36 - "records/service.py"
Cohesion: 0.05
Nodes (111): NotFound, build_export(), AsyncSession, Account data export: one JSON document with every record the user owns.…, delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription() (+103 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.21
Nodes (8): APP_LINKS, AppNav(), OWNER_ONLY, MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "signup"
Cohesion: 0.30
Nodes (23): signup(), code_for(), login(), new_client(), AsyncClient, Account security (ADR-029): two-step verification, active sessions, password…, test_a_code_cannot_be_used_twice(), test_cannot_revoke_someone_elses_session() (+15 more)

### Community 41 - "documents/service.py"
Cohesion: 0.11
Nodes (30): Document, DocumentKind, DocumentStatus, StrEnum, create_document(), delete_document(), get_document(), get_document_by_id() (+22 more)

### Community 42 - "MedSpace"
Cohesion: 0.12
Nodes (16): Architecture at a glance, Deploy, Enable Google sign-in, Calendar & Tasks, Enable real AI extraction (optional), Engineering highlights, Features, Getting started, License (+8 more)

### Community 43 - "db.py"
Cohesion: 0.11
Nodes (37): Base, IdMixin, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin, uuid7(), Import every module's ORM models so `Base.metadata` is complete (Alembic,… (+29 more)

### Community 45 - "test_auth.py"
Cohesion: 0.21
Nodes (17): AsyncClient, test_audit_trail_lists_own_events(), test_demo_login_creates_isolated_demo_user(), test_health_supports_head(), test_login_is_rate_limited(), test_login_wrong_password_is_generic(), test_logout_revokes_session(), test_me_requires_auth() (+9 more)

### Community 46 - "Deploying MedSpace"
Cohesion: 0.29
Nodes (7): 1. Database: Supabase (or any always-on Postgres 15+ with pgvector), 2. Object storage: Cloudflare R2 (or AWS S3), 3. API: one container, 4. Web: static build with an `/api` rewrite, 5. Google OAuth, Checklist, Deploying MedSpace

### Community 47 - "AuthForms.jsx"
Cohesion: 0.18
Nodes (12): ADR-0037, DemoDivider(), LoginForm(), loginSchema, MfaStep(), SignupForm(), signupSchema, useAuthMutation() (+4 more)

### Community 48 - "records/api.js"
Cohesion: 0.18
Nodes (4): recordKeys, useInvalidateRecords(), useUpdateCareAction(), useUpdateMedication()

### Community 50 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, dev, e2e, format, lint, preview, test (+1 more)

### Community 51 - "test_evidence.py"
Cohesion: 0.13
Nodes (34): build_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+26 more)

### Community 52 - "SupplyDialog.jsx"
Cohesion: 0.25
Nodes (13): supplyKeys, useClearSupply(), useRefill(), useSetSupply(), useSupplyMutation(), leftLabel(), runsOutLabel(), trim() (+5 more)

### Community 53 - "api service (alembic + uvicorn)"
Cohesion: 0.25
Nodes (11): CI Backend job (ruff + pytest on pgvector Postgres), CI Docker images build job, CI E2E job (Playwright + axe, fake providers), CI Frontend job (lint + Vitest + build), api service (alembic + uvicorn), x-backend-env shared env anchor, postgres service (pgvector/pgvector:pg17), redis service (+3 more)

### Community 54 - "lib/format.js"
Cohesion: 0.38
Nodes (8): firstName(), formatBytes(), formatClock(), formatDate(), formatRelativeDay(), greeting(), timeAgo(), toDate()

### Community 56 - "test_google_signin.py"
Cohesion: 0.25
Nodes (18): GoogleIdentity, google_sign_in(), AsyncClient, MonkeyPatch, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017., Run start -> (simulated consent) -> callback. Returns the final redirect. (+10 more)

### Community 57 - "drain"
Cohesion: 0.16
Nodes (28): diet_category(), _diet_notes(), Split an advice line like "Diet: low salt. Avoid sugary drinks." into separate…, drain(), Background job dispatch. `QUEUE_MODE=arq`: jobs go to Redis and run in the…, Wait for all inline jobs (used by tests)., AsyncClient, parametrize (+20 more)

### Community 58 - "helpers.js"
Cohesion: 0.14
Nodes (10): RFC-6238, here, SAMPLE, confirmEmail(), emailLink(), expectAccessible(), signUp(), startDemo() (+2 more)

### Community 60 - "assistant/router.py"
Cohesion: 0.17
Nodes (21): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+13 more)

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "identity/router.py"
Cohesion: 0.25
Nodes (19): mfa_new_codes(), _security_out(), CodeIn, DeviceSessionOut, EmailChangeIn, ForgotPasswordIn, LoginIn, LoginResult (+11 more)

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
Nodes (3): DocumentReview(), ADR-0031, recordLabel()

### Community 115 - "demo/router.py"
Cohesion: 0.15
Nodes (17): RateLimited, demo_login(), DbSession, post, Request, Response, clear_auth_cookies(), Response (+9 more)

### Community 117 - "csrf"
Cohesion: 0.39
Nodes (16): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+8 more)

### Community 127 - "test_integrations.py"
Cohesion: 0.30
Nodes (15): decrypt(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 128 - "conftest.py"
Cohesion: 0.18
Nodes (16): reset_rate_limits(), Tests swap in their own mailer (None resets to the configured one)., set_mailer(), Tests swap in their own sender (None resets to the configured one)., set_push_sender(), auth_client(), _clean_tables(), client() (+8 more)

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
Cohesion: 0.36
Nodes (12): Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), evidence_for_document(), get_extraction(), latest_for_document(), AsyncSession (+4 more)

### Community 143 - "corpus.py"
Cohesion: 0.26
Nodes (13): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+5 more)

### Community 144 - "Launch guide: the steps only you can do"
Cohesion: 0.13
Nodes (15): Housekeeping, Keep the data safe, Launch guide: the steps only you can do, Part 10. Keep reminders working on the free plan (5 minutes), Part 11. Final checks (15 minutes), Part 12. Make it shine on your resume, Part 1. Accounts to create (about 30 minutes), Part 2. Generate your secrets (5 minutes, on your computer) (+7 more)

### Community 145 - "GoogleClient"
Cohesion: 0.11
Nodes (4): GoogleClient, Any, Protocol, Tokens

### Community 146 - "circle/router.py"
Cohesion: 0.13
Nodes (31): accept(), get_circle(), invite(), preview(), BackgroundTasks, CurrentUser, DbSession, delete (+23 more)

### Community 147 - "circle/api.js"
Cohesion: 0.18
Nodes (18): ActingBanner(), circleKeys, ADR-0032, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite() (+10 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "_Locator"
Cohesion: 0.28
Nodes (4): _Locator, Rect, First variant found, preferring the hinted page (or the anchor's page and…, Spot

### Community 151 - "test_timeline_dashboard.py"
Cohesion: 0.22
Nodes (11): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets() (+3 more)

### Community 152 - "main.py"
Cohesion: 0.11
Nodes (25): configure_logging(), BodySizeLimitMiddleware, _BodyTooLarge, CSRFMiddleware, BaseHTTPMiddleware, Exception, HTTP middleware: security headers, CSRF double-submit check, request logging., Reject request bodies over `max_bytes` as they stream in, before anything… (+17 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 156 - "files.py"
Cohesion: 0.15
Nodes (15): image_size(), inspect(), Inspection, _matrix(), Exception, Rect, File inspection: type sniffing by magic bytes, PDF text extraction and page…, PNG bytes per page for the vision model. Images are passed through (re-encoded… (+7 more)

### Community 157 - "safe_path"
Cohesion: 0.33
Nodes (6): Request, Response, The request path with secret tokens replaced, for logs., safe_path(), test_token_paths_are_redacted(), RequestResponseEndpoint

### Community 158 - "demo/service.py"
Cohesion: 0.30
Nodes (14): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+6 more)

### Community 160 - "test_authorization_sweep.py"
Cohesion: 0.52
Nodes (6): fill(), owner_ids(), AsyncClient, Every route that takes an ID refuses another account's IDs, and leaves that…, snapshot(), test_no_route_accepts_another_accounts_ids()

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "test_ratelimit.py"
Cohesion: 0.24
Nodes (13): fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings(), test_baseline_budget_covers_every_route(), test_headers_scale_and_disable() (+5 more)

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 170 - "audit/router.py"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 172 - "main.jsx"
Cohesion: 0.21
Nodes (5): Providers(), router, ApiError, ADR-0025, queryClient

### Community 175 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 177 - "totp.py"
Cohesion: 0.18
Nodes (15): code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), provisioning_uri(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).… (+7 more)

### Community 178 - "session_state"
Cohesion: 0.40
Nodes (5): BaseModel, OptionalUser, Who am I, without a 401 for anonymous visitors (the SPA calls this on boot). A…, session_state(), SessionState

### Community 183 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 192 - "get_settings"
Cohesion: 0.09
Nodes (30): get_settings(), field_validator, Application settings, loaded from environment variables (and `.env` in…, Refuse to start in production with settings that would quietly be unsafe., Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, Logging configuration., Auth cookie helpers shared by the identity and demo routers. (+22 more)

### Community 194 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 199 - "test_assistant.py"
Cohesion: 0.38
Nodes (13): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+5 more)

### Community 200 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 201 - "identity/service.py"
Cohesion: 0.13
Nodes (25): create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), _fernet(), hash_password(), needs_rehash(), UUID (+17 more)

### Community 202 - "extraction/service.py"
Cohesion: 0.09
Nodes (36): _date_variants(), date, Where on the page each extracted value is printed (ADR-031). Given the original…, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt() (+28 more)

### Community 206 - "embeddings.py"
Cohesion: 0.15
Nodes (8): Embedder, FastEmbedEmbedder, get_embedder(), HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and…

### Community 230 - "assistant/service.py"
Cohesion: 0.12
Nodes (34): ChatMessage, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, answer_stream(), _best_snippet(), build_prompt(), chunk_pages() (+26 more)

### Community 231 - "errors.py"
Cohesion: 0.14
Nodes (23): _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, UUID, Shared FastAPI dependencies. (+15 more)

### Community 232 - "test_email_change.py"
Cohesion: 0.29
Nodes (18): confirm_email(), link_token(), The token from the first `<path>?token=...` link in an email body., Follow the verification link from the outbox, as the address owner would., change(), change_token(), confirm(), AsyncClient (+10 more)

### Community 235 - "notify/service.py"
Cohesion: 0.11
Nodes (24): outbox(), get, Dev-only outbox: read simulated emails (local testing and e2e). Never mounted…, app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, To the address being replaced: once when a change is asked for, once when it…, _send() (+16 more)

## Knowledge Gaps
- **285 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+280 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `circle/service.py`, `reminders/service.py`, `User`, `integrations/router.py`, `test_google_live.py`, `documents/router.py`, `ratelimit.py`, `main.py`, `test_timeline_dashboard.py`, `safe_path`, `demo/service.py`, `worker.py`, `test_ratelimit.py`, `records/service.py`, `documents/service.py`, `db.py`, `S3Storage`, `drain`, `env.py`, `identity/service.py`, `extraction/service.py`, `embeddings.py`, `assistant/service.py`, `notify/service.py`, `demo/router.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `circle/service.py`, `reminders/service.py`, `integrations/service.py`, `doses/service.py`, `confirm`, `circle/router.py`, `test_google_live.py`, `visits/service.py`, `main.py`, `test_email_recovery.py`, `utcnow`, `demo/service.py`, `supply/service.py`, `records/service.py`, `signup`, `documents/service.py`, `db.py`, `test_google_signin.py`, `identity/service.py`, `extraction/service.py`, `assistant/service.py`, `errors.py`, `test_email_change.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `conftest.py`, `test_google_live.py`, `test_visits.py`, `test_timeline_dashboard.py`, `test_labs.py`, `test_email_recovery.py`, `test_sharing.py`, `test_caregiver_reminders.py`, `test_authorization_sweep.py`, `test_ratelimit.py`, `supply/service.py`, `signup`, `test_auth.py`, `test_evidence.py`, `test_google_signin.py`, `drain`, `get_settings`, `test_assistant.py`, `test_doses.py`, `test_email_change.py`, `test_integrations.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _285 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_eval.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08973172987974098 - nodes in this community are weakly interconnected._
- **Should `circle/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1354723707664884 - nodes in this community are weakly interconnected._
- **Should `reminders/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05966724039013196 - nodes in this community are weakly interconnected._