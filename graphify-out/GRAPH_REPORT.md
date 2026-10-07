# Graph Report - MedSpace  (2026-10-07)

## Corpus Check
- 353 files · ~162,187 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2925 nodes · 7350 edges · 204 communities (161 shown, 43 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 112 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f2500915`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- extract
- ratelimit.py
- reminders/service.py
- dependencies
- devDependencies
- sharing/router.py
- router.jsx
- User
- heuristic.py
- Architecture Decision Records
- doses/service.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- integrations/service.py
- sharing/service.py
- FeatureBento.jsx
- auth.jsx
- HttpGoogleClient
- test_google_live.py
- test_visits.py
- visits/service.py
- documents/router.py
- search/service.py
- ReviewForm.jsx
- test_labs.py
- test_email_recovery.py
- test_caregiver_reminders.py
- EasterEggs.jsx
- demo/service.py
- utcnow
- SearchPalette.jsx
- integrations/api.js
- test_eval.py
- supply/service.py
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- signup
- errors.py
- MedSpace
- db.py
- visits/api.js
- test_auth.py
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- Visits.jsx
- scripts
- drain
- SupplyDialog.jsx
- api service (alembic + uvicorn)
- lib/format.js
- Settings.jsx
- test_google_signin.py
- deps.py
- helpers.js
- Ask.jsx
- record
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
- audit/router.py
- csrf
- install.js
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
- export.py
- corpus.py
- Launch guide: the steps only you can do
- google.py
- circle/router.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- locate
- LocalStorage
- get_settings
- doses/api.js
- normalize_frequency
- extraction/router.py
- RecoveryForms.jsx
- offline.js
- test_ratelimit.py
- useResendVerification
- hooks.js
- VisitPrep.jsx
- test_assistant.py
- main.jsx
- CircleAccept.jsx
- totp.py
- env.py
- sw-template.js
- vercel.json
- labs.py
- react-router
- zod
- globals
- test_sharing.py
- test_security_hardening.py
- @testing-library/user-event
- test_timeline_dashboard.py
- test_doses.py
- extraction/service.py
- .dispatch
- links.js
- assistant/service.py
- identity/service.py
- test_email_change.py
- notify/service.py
- smoothScroll.js

## God Nodes (most connected - your core abstractions)
1. `User` - 126 edges
2. `csrf()` - 113 edges
3. `get_settings()` - 95 edges
4. `utcnow()` - 76 edges
5. `signup()` - 57 edges
6. `Base` - 47 edges
7. `NotFound` - 45 edges
8. `record()` - 45 edges
9. `IdMixin` - 42 edges
10. `Architecture Decision Records` - 40 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `test_production_requires_google_credentials_when_google_is_on()` --calls--> `Settings`  [EXTRACTED]
  backend/tests/test_google_live.py → backend/app/core/config.py
- `invite_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/circle/service.py → backend/app/core/config.py
- `share_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/sharing/service.py → backend/app/core/config.py
- `_clean_tables()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (204 total, 43 thin omitted)

### Community 0 - "extract"
Cohesion: 0.12
Nodes (17): ambiguous_date(), diet_category(), _diet_notes(), extract(), _parse_date(), date, Split an advice line like "Diet: low salt. Avoid sugary drinks." into separate…, 11/05/2026 can be 11 May or Nov 5; 25/05/2026 cannot. (+9 more)

### Community 1 - "ratelimit.py"
Cohesion: 0.11
Nodes (18): RateLimited, caller_key(), client_ip(), Decision, _estimate(), get_store(), Any, Request (+10 more)

### Community 2 - "reminders/service.py"
Cohesion: 0.06
Nodes (77): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+69 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "sharing/router.py"
Cohesion: 0.18
Nodes (22): create_share(), list_shares(), open_share(), CurrentUser, DbSession, delete, get, post (+14 more)

### Community 6 - "router.jsx"
Cohesion: 0.06
Nodes (5): MarketingLayout(), RouteError(), appLayout, authLayout, openAuthLayout()

### Community 7 - "User"
Cohesion: 0.16
Nodes (29): Unprocessable, hash_password(), verify_password(), User, begin_setup(), change_password(), check_second_factor(), clear_second_factor() (+21 more)

### Community 8 - "heuristic.py"
Cohesion: 0.12
Nodes (30): _apply_sig(), _dosing(), _lab_results(), _lab_row(), _medication_from_line(), Offline, rule-based extractor used when no LLM is configured (CI, demo, keyless…, Frequency, duration and instructions from the text after a medicine's…, ConfirmCareAction (+22 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.05
Nodes (40): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+32 more)

### Community 10 - "doses/service.py"
Cohesion: 0.13
Nodes (39): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+31 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.12
Nodes (34): constant_time_equals(), has_sync_scopes(), pkce_pair(), True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect(), _frontend() (+26 more)

### Community 12 - "documents/api.js"
Cohesion: 0.10
Nodes (13): ACTIVE, docKeys, isProcessing(), ADR-0031, previewUrl(), uploadDocument(), useDocument(), useDocuments() (+5 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "integrations/service.py"
Cohesion: 0.20
Nodes (30): encrypt(), GoogleAPIError, OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _client(), _clock() (+22 more)

### Community 15 - "sharing/service.py"
Cohesion: 0.21
Nodes (22): NotFound, new_opaque_token(), A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create(), link_status(), list_links() (+14 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 18 - "HttpGoogleClient"
Cohesion: 0.14
Nodes (6): _events(), GoogleAuthError, HttpGoogleClient, Exception, MedSpace's own calendar (the only one calendar.app.created can reach)., Consent was revoked or the refresh token is no longer valid.

### Community 19 - "test_google_live.py"
Cohesion: 0.10
Nodes (20): connect_live(), FakeGoogleHTTP, live(), AsyncClient, fixture, Request, Response, Real Google OAuth 2.0 (GOOGLE_PROVIDER=google), with Google's HTTP endpoints… (+12 more)

### Community 20 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 21 - "visits/service.py"
Cohesion: 0.07
Nodes (73): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+65 more)

### Community 22 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 23 - "search/service.py"
Cohesion: 0.17
Nodes (16): CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession, BaseModel (+8 more)

### Community 24 - "ReviewForm.jsx"
Cohesion: 0.14
Nodes (22): evidenceKeys(), findSpot(), itemName(), ADR-0031, evidence, values, blank(), CARE_KINDS (+14 more)

### Community 25 - "test_labs.py"
Cohesion: 0.31
Nodes (13): build_lab_pdf(), lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_split_line_lab_tables(), test_labs_are_private_and_deletable() (+5 more)

### Community 26 - "test_email_recovery.py"
Cohesion: 0.19
Nodes (29): FakeMailer, Keeps the last messages in memory (the dev outbox and tests read them)., confirm_email(), link_token(), The token from the first `<path>?token=...` link in an email body., Follow the verification link from the outbox, as the address owner would., forgot(), login() (+21 more)

### Community 27 - "test_caregiver_reminders.py"
Cohesion: 0.23
Nodes (26): alerts(), caregiver(), owner_with_medicine(), AsyncClient, Response, Dose alerts for caregivers (ADR-032): opt-in per person, on time or "not ticked…, Eve, confirmed, in Ada's care circle with `role`, with a subscribed device., test_alert_when_due_with_actions_for_helpers() (+18 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "demo/service.py"
Cohesion: 0.22
Nodes (17): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+9 more)

### Community 30 - "utcnow"
Cohesion: 0.17
Nodes (28): datetime, utcnow(), Gone, sha256_hex(), cancel_email_change(), confirm_email_change(), _consume(), EmailChange (+20 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "test_eval.py"
Cohesion: 0.19
Nodes (18): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+10 more)

### Community 34 - "supply/service.py"
Cohesion: 0.10
Nodes (49): clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get, post, put (+41 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.07
Nodes (28): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+20 more)

### Community 36 - "records/service.py"
Cohesion: 0.09
Nodes (70): build_export(), AsyncSession, Medication, delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription(), list_care_actions() (+62 more)

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

### Community 41 - "errors.py"
Cohesion: 0.07
Nodes (38): AppError, Conflict, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI (+30 more)

### Community 42 - "MedSpace"
Cohesion: 0.12
Nodes (16): Architecture at a glance, Deploy, Enable Google sign-in, Calendar & Tasks, Enable real AI extraction (optional), Engineering highlights, Features, Getting started, License (+8 more)

### Community 43 - "db.py"
Cohesion: 0.08
Nodes (51): Base, IdMixin, UUID, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, DocumentChunk (+43 more)

### Community 45 - "test_auth.py"
Cohesion: 0.21
Nodes (17): AsyncClient, test_audit_trail_lists_own_events(), test_demo_login_creates_isolated_demo_user(), test_health_supports_head(), test_login_is_rate_limited(), test_login_wrong_password_is_generic(), test_logout_revokes_session(), test_me_requires_auth() (+9 more)

### Community 46 - "Deploying MedSpace"
Cohesion: 0.25
Nodes (8): 1. Database: Supabase (or any always-on Postgres 15+ with pgvector), 2. Object storage: Cloudflare R2 (or AWS S3), 3. API: one container, 4. Web: static build with an `/api` rewrite, 5. Google OAuth, Checklist, Current deployment, Deploying MedSpace

### Community 47 - "AuthForms.jsx"
Cohesion: 0.18
Nodes (12): ADR-0037, DemoDivider(), LoginForm(), loginSchema, MfaStep(), SignupForm(), signupSchema, useAuthMutation() (+4 more)

### Community 48 - "records/api.js"
Cohesion: 0.18
Nodes (4): recordKeys, useInvalidateRecords(), useUpdateCareAction(), useUpdateMedication()

### Community 50 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, dev, e2e, format, lint, preview, test (+1 more)

### Community 51 - "drain"
Cohesion: 0.14
Nodes (41): build_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+33 more)

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

### Community 57 - "deps.py"
Cohesion: 0.25
Nodes (14): get_session(), AsyncSession, _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request (+6 more)

### Community 58 - "helpers.js"
Cohesion: 0.14
Nodes (10): RFC-6238, here, SAMPLE, confirmEmail(), emailLink(), expectAccessible(), signUp(), startDemo() (+2 more)

### Community 60 - "record"
Cohesion: 0.14
Nodes (31): Forbidden, list_for_user(), Any, AsyncSession, Request, UUID, Stage an audit row in the caller's transaction (committed with the business…, record() (+23 more)

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "identity/router.py"
Cohesion: 0.08
Nodes (75): check(), Count one hit for `scope` + `key` and decide. Fails open if the store is…, decode_purpose_token(), clear_auth_cookies(), Response, Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), cancel_email_change() (+67 more)

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

### Community 115 - "audit/router.py"
Cohesion: 0.36
Nodes (7): list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage, BaseModel

### Community 117 - "csrf"
Cohesion: 0.54
Nodes (13): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+5 more)

### Community 119 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 127 - "test_integrations.py"
Cohesion: 0.30
Nodes (15): decrypt(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 128 - "conftest.py"
Cohesion: 0.21
Nodes (14): reset_rate_limits(), auth_client(), _clean_tables(), client(), AsyncClient, fixture, Test harness: real Postgres (pgvector), fakes for every external service., _schema() (+6 more)

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

### Community 142 - "export.py"
Cohesion: 0.12
Nodes (9): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, index_demo_documents(), Demo background jobs., Index a new demo account's documents for Ask MedSpace. Embedding is most of the…, Background job: process an uploaded document end to end., Account data export: one JSON document with every record the user owns.…, job(), Register a coroutine as a background job under its function name. (+1 more)

### Community 143 - "corpus.py"
Cohesion: 0.24
Nodes (14): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+6 more)

### Community 144 - "Launch guide: the steps only you can do"
Cohesion: 0.13
Nodes (15): Housekeeping, Keep the data safe, Launch guide: the steps only you can do, Part 10. Keep reminders working on the free plan (5 minutes), Part 11. Final checks (15 minutes), Part 12. Make it shine on your resume, Part 1. Accounts to create (about 30 minutes), Part 2. Generate your secrets (5 minutes, on your computer) (+7 more)

### Community 145 - "google.py"
Cohesion: 0.10
Nodes (14): client_for_mode(), client_for_user(), get_google(), GoogleClient, _live(), live_configured(), Any, Protocol (+6 more)

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

### Community 150 - "locate"
Cohesion: 0.11
Nodes (21): _clean(), _date_variants(), locate(), _Locator, date, Rect, Where on the page each extracted value is printed (ADR-031). Given the original…, First variant found, preferring the hinted page (or the anchor's page and… (+13 more)

### Community 151 - "LocalStorage"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 152 - "get_settings"
Cohesion: 0.07
Nodes (45): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., BodySizeLimitMiddleware, _BodyTooLarge, CSRFMiddleware, BaseHTTPMiddleware (+37 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 156 - "normalize_frequency"
Cohesion: 0.20
Nodes (16): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+8 more)

### Community 157 - "extraction/router.py"
Cohesion: 0.30
Nodes (13): confirm_extraction(), discard_extraction(), get_evidence(), get_latest_extraction(), CurrentUser, DbSession, get, post (+5 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "test_ratelimit.py"
Cohesion: 0.16
Nodes (16): MemoryStore, Single-process store (tests, local development). `clock` is injectable for…, fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings() (+8 more)

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 170 - "test_assistant.py"
Cohesion: 0.42
Nodes (12): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+4 more)

### Community 172 - "main.jsx"
Cohesion: 0.21
Nodes (5): Providers(), router, ApiError, ADR-0025, queryClient

### Community 177 - "totp.py"
Cohesion: 0.18
Nodes (15): code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), provisioning_uri(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).… (+7 more)

### Community 178 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 183 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 191 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 192 - "test_security_hardening.py"
Cohesion: 0.05
Nodes (45): field_validator, Refuse to start in production with settings that would quietly be unsafe., Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, image_size(), inspect(), Inspection, _matrix() (+37 more)

### Community 197 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 200 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 202 - "extraction/service.py"
Cohesion: 0.07
Nodes (50): DocumentKind, DocumentStatus, StrEnum, set_status(), process_document(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, _nullable() (+42 more)

### Community 209 - ".dispatch"
Cohesion: 0.60
Nodes (3): Request, Response, RequestResponseEndpoint

### Community 230 - "assistant/service.py"
Cohesion: 0.06
Nodes (58): ChatMessage, ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut (+50 more)

### Community 231 - "identity/service.py"
Cohesion: 0.11
Nodes (26): Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), _fernet(), needs_rehash() (+18 more)

### Community 232 - "test_email_change.py"
Cohesion: 0.40
Nodes (14): change(), change_token(), confirm(), AsyncClient, Response, Changing the account email (ADR-033): proof, confirmation by the new inbox,…, test_addresses_already_in_use_and_unchanged_ones_are_refused(), test_change_happens_only_when_the_new_inbox_confirms() (+6 more)

### Community 235 - "notify/service.py"
Cohesion: 0.07
Nodes (37): outbox(), get, app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, To the address being replaced: once when a change is asked for, once when it…, _send(), send_circle_invite() (+29 more)

## Knowledge Gaps
- **287 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+282 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `ratelimit.py`, `reminders/service.py`, `doses/service.py`, `integrations/router.py`, `sharing/service.py`, `google.py`, `test_google_live.py`, `documents/router.py`, `demo/service.py`, `test_ratelimit.py`, `errors.py`, `db.py`, `env.py`, `record`, `identity/router.py`, `test_security_hardening.py`, `test_timeline_dashboard.py`, `extraction/service.py`, `.dispatch`, `assistant/service.py`, `identity/service.py`, `notify/service.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `reminders/service.py`, `doses/service.py`, `export.py`, `integrations/service.py`, `sharing/service.py`, `circle/router.py`, `test_google_live.py`, `visits/service.py`, `test_email_recovery.py`, `demo/service.py`, `utcnow`, `supply/service.py`, `records/service.py`, `signup`, `db.py`, `test_google_signin.py`, `deps.py`, `record`, `extraction/service.py`, `assistant/service.py`, `identity/service.py`, `test_email_change.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `conftest.py`, `test_google_live.py`, `test_visits.py`, `test_labs.py`, `test_email_recovery.py`, `test_caregiver_reminders.py`, `test_ratelimit.py`, `supply/service.py`, `signup`, `test_assistant.py`, `test_auth.py`, `drain`, `test_google_signin.py`, `test_sharing.py`, `test_security_hardening.py`, `test_timeline_dashboard.py`, `test_doses.py`, `test_email_change.py`, `test_integrations.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _287 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `extract` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `ratelimit.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11396011396011396 - nodes in this community are weakly interconnected._
- **Should `reminders/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05640203154236835 - nodes in this community are weakly interconnected._