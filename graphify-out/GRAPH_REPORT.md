# Graph Report - MedSpace  (2026-10-03)

## Corpus Check
- 324 files · ~137,714 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2603 nodes · 6319 edges · 197 communities (150 shown, 47 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 280 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eeaffed9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_labs.py
- circle/router.py
- db.py
- dependencies
- devDependencies
- search/service.py
- router.jsx
- utcnow
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
- test_email_recovery.py
- record
- EasterEggs.jsx
- circle/service.py
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
- timedelta
- signup
- MedSpace
- sharing/service.py
- visits/api.js
- notify/service.py
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
- test_auth.py
- tailwindcss
- @testing-library/react
- vitest
- DoseStrip.jsx
- VisitBrief.jsx
- test_search.py
- clinician.js
- SecuritySettings.jsx
- ReminderSettings.jsx
- test_google_signin.py
- corpus.py
- totp.py
- google.py
- deps.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- identity/models.py
- conftest.py
- main.py
- doses/api.js
- FastEmbedEmbedder
- demo/service.py
- HashEmbedder
- env.py
- Embedder
- offline.js
- assistant/router.py
- audit/router.py
- useResendVerification
- User
- hooks.js
- VisitPrep.jsx
- Extraction evaluation
- main.jsx
- files.py
- CircleAccept.jsx
- install.js
- storage.py
- documents/service.py
- sw-template.js
- ExtractionStatus
- uuid7
- react-router
- zod
- globals
- @testing-library/user-event
- BaseHTTPMiddleware
- FastAPI
- fixture
- MonkeyPatch

## God Nodes (most connected - your core abstractions)
1. `User` - 123 edges
2. `csrf()` - 84 edges
3. `get_settings()` - 78 edges
4. `utcnow()` - 62 edges
5. `signup()` - 43 edges
6. `NotFound` - 40 edges
7. `record()` - 39 edges
8. `Base` - 38 edges
9. `IdMixin` - 36 edges
10. `Architecture Decision Records` - 31 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `authenticate()` --calls--> `needs_rehash()`  [INFERRED]
  backend/app/modules/identity/service.py → backend/app/core/security.py
- `invite_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/circle/service.py → backend/app/core/config.py
- `share_url()` --calls--> `get_settings()`  [EXTRACTED]
  backend/app/modules/sharing/service.py → backend/app/core/config.py
- `reminder_loop()` --indirect_call--> `session()`  [INFERRED]
  backend/app/main.py → backend/tests/conftest.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (197 total, 47 thin omitted)

### Community 0 - "test_labs.py"
Cohesion: 0.05
Nodes (92): build_lab_pdf(), build_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date (+84 more)

### Community 1 - "circle/router.py"
Cohesion: 0.17
Nodes (24): accept(), get_circle(), invite(), preview(), BackgroundTasks, CurrentUser, DbSession, delete (+16 more)

### Community 2 - "db.py"
Cohesion: 0.11
Nodes (32): Base, IdMixin, datetime, Database engine, session factory and declarative base., TimestampMixin, AuditLog, Append-only trail of security-relevant actions. Never updated or deleted by app…, CareLink (+24 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "search/service.py"
Cohesion: 0.16
Nodes (16): CurrentUser, DbSession, get, search(), _like(), _prefix_tsquery(), AsyncSession, BaseModel (+8 more)

### Community 7 - "utcnow"
Cohesion: 0.18
Nodes (28): AppError, utcnow(), Conflict, verify_password(), begin_setup(), change_password(), check_second_factor(), clear_second_factor() (+20 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.22
Nodes (28): encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _clock(), _delete_remote() (+20 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.06
Nodes (31): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+23 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (40): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+32 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.13
Nodes (31): pkce_pair(), callback(), connect(), disconnect(), _frontend(), google_sign_in(), preview(), providers() (+23 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/router.py"
Cohesion: 0.08
Nodes (71): demo_login(), DbSession, post, Request, Response, clear_auth_cookies(), Response, Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in… (+63 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.14
Nodes (27): _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload, _coerce() (+19 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 18 - "HttpGoogleClient"
Cohesion: 0.17
Nodes (5): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, Consent was revoked or the refresh token is no longer valid.

### Community 19 - "assistant/service.py"
Cohesion: 0.12
Nodes (34): ChatMessage, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, answer_stream(), _best_snippet(), build_prompt(), chunk_pages() (+26 more)

### Community 20 - "LLMError"
Cohesion: 0.31
Nodes (5): GroqProvider, LLMError, _parse_json(), Any, Exception

### Community 21 - "visits/service.py"
Cohesion: 0.07
Nodes (73): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+65 more)

### Community 22 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.10
Nodes (23): RateLimited, caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore (+15 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "test_eval.py"
Cohesion: 0.09
Nodes (42): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+34 more)

### Community 26 - "test_email_recovery.py"
Cohesion: 0.20
Nodes (26): FakeMailer, Keeps the last messages in memory (the dev outbox and tests read them)., link_token(), The token from the first `<path>?token=...` link in an email body., forgot(), login(), AsyncClient, MonkeyPatch (+18 more)

### Community 27 - "record"
Cohesion: 0.17
Nodes (20): list_for_user(), Any, AsyncSession, Request, UUID, Audit trail: `record()` is the single write path, used by every module., Stage an audit row in the caller's transaction (committed with the business…, record() (+12 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "circle/service.py"
Cohesion: 0.22
Nodes (20): Forbidden, accept(), _by_token(), circle(), invite(), invite_url(), link_status(), _person() (+12 more)

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
Cohesion: 0.36
Nodes (10): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+2 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.09
Nodes (22): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+14 more)

### Community 36 - "records/service.py"
Cohesion: 0.08
Nodes (74): NotFound, build_export(), AsyncSession, Account data export: one JSON document with every record the user owns.…, Medication, delete_diet_note(), delete_lab_result(), get_lab_trend() (+66 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Backend conventions, Commands, Docs discipline, Frontend conventions, Git, graphify, Read first (context recovery), Stack (+1 more)

### Community 38 - "AppNav.jsx"
Cohesion: 0.21
Nodes (8): APP_LINKS, AppNav(), OWNER_ONLY, MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "MedSpace Architecture"
Cohesion: 0.18
Nodes (11): 10. Deployment, 1. System overview, 2. Repository layout, 3.1 Ports and adapters, 3. Backend modules (bounded contexts), 5. Data model, 6. API surface (v1), 7. Security model (+3 more)

### Community 40 - "timedelta"
Cohesion: 0.08
Nodes (62): MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get (+54 more)

### Community 41 - "signup"
Cohesion: 0.30
Nodes (23): signup(), code_for(), login(), new_client(), AsyncClient, Account security (ADR-029): two-step verification, active sessions, password…, test_a_code_cannot_be_used_twice(), test_cannot_revoke_someone_elses_session() (+15 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.08
Nodes (55): Gone, new_opaque_token(), A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create_share(), list_shares(), open_share() (+47 more)

### Community 45 - "notify/service.py"
Cohesion: 0.17
Nodes (14): app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, _send(), send_circle_invite(), send_password_reset(), send_security_alert(), send_verification() (+6 more)

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
Cohesion: 0.20
Nodes (16): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+8 more)

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
Cohesion: 0.15
Nodes (10): RFC-6238, here, SAMPLE, confirmEmail(), emailLink(), expectAccessible(), signUp(), startDemo() (+2 more)

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "get_settings"
Cohesion: 0.09
Nodes (31): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token() (+23 more)

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
Cohesion: 0.22
Nodes (14): fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings(), test_baseline_budget_covers_every_route(), test_headers_scale_and_disable() (+6 more)

### Community 117 - "csrf"
Cohesion: 0.54
Nodes (13): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+5 more)

### Community 127 - "test_integrations.py"
Cohesion: 0.30
Nodes (15): decrypt(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 128 - "test_auth.py"
Cohesion: 0.21
Nodes (17): AsyncClient, test_audit_trail_lists_own_events(), test_demo_login_creates_isolated_demo_user(), test_health_supports_head(), test_login_is_rate_limited(), test_login_wrong_password_is_generic(), test_logout_revokes_session(), test_me_requires_auth() (+9 more)

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

### Community 142 - "test_google_signin.py"
Cohesion: 0.26
Nodes (17): google_sign_in(), AsyncClient, MonkeyPatch, Response, query(), Optional "Continue with Google" sign-in (simulation mode), ADR-017., Run start -> (simulated consent) -> callback. Returns the final redirect., test_callback_without_state_cookie_is_rejected() (+9 more)

### Community 143 - "corpus.py"
Cohesion: 0.24
Nodes (14): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+6 more)

### Community 144 - "totp.py"
Cohesion: 0.18
Nodes (15): code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), provisioning_uri(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).… (+7 more)

### Community 145 - "google.py"
Cohesion: 0.10
Nodes (8): GoogleClient, GoogleIdentity, has_sync_scopes(), Any, Protocol, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent…, Tokens

### Community 146 - "deps.py"
Cohesion: 0.31
Nodes (12): _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, UUID, Shared FastAPI dependencies. (+4 more)

### Community 147 - "circle/api.js"
Cohesion: 0.25
Nodes (12): ActingBanner(), circleKeys, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite(), useRemoveLink() (+4 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "identity/models.py"
Cohesion: 0.31
Nodes (9): Import every module's ORM models so `Base.metadata` is complete (Alembic,…, EmailToken, Opaque refresh token, stored hashed. Rotated on every use; reuse revokes the…, One-time backup codes for two-step verification; only hashes are stored., A one-time link sent by email (ADR-030): verify an address, or reset a…, RecoveryCode, RefreshToken, Base (+1 more)

### Community 151 - "conftest.py"
Cohesion: 0.13
Nodes (21): reset_rate_limits(), outbox(), get, Dev-only outbox: read simulated emails (local testing and e2e). Never mounted…, get_mailer(), Mailer, Email port (ADR-030): SMTP in production, an in-memory outbox in dev, demo and…, Tests swap in their own mailer (None resets to the configured one). (+13 more)

### Community 152 - "main.py"
Cohesion: 0.18
Nodes (16): CSRFMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware, SecurityHeadersMiddleware, constant_time_equals() (+8 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 156 - "demo/service.py"
Cohesion: 0.10
Nodes (32): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-… (+24 more)

### Community 158 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "assistant/router.py"
Cohesion: 0.17
Nodes (21): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+13 more)

### Community 163 - "audit/router.py"
Cohesion: 0.24
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 166 - "User"
Cohesion: 0.15
Nodes (20): hash_password(), sha256_hex(), User, mfa_challenge(), The token a first-factor success hands back instead of a session., authenticate(), create_user(), delete_user() (+12 more)

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

### Community 177 - "storage.py"
Cohesion: 0.13
Nodes (6): ServiceUnavailable, ObjectStorage, Protocol, Object storage port with filesystem and S3-compatible adapters., Any S3-compatible store (MinIO, Cloudflare R2, AWS S3). boto3 calls run in a…, S3Storage

### Community 178 - "documents/service.py"
Cohesion: 0.14
Nodes (29): AppError, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI, Request (+21 more)

### Community 183 - "uuid7"
Cohesion: 0.67
Nodes (3): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7()

## Knowledge Gaps
- **242 isolated node(s):** `Features`, `Architecture at a glance`, `Engineering highlights`, `Tech stack`, `Prerequisites` (+237 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `circle/router.py`, `utcnow`, `integrations/service.py`, `doses/service.py`, `test_google_signin.py`, `extraction/service.py`, `deps.py`, `assistant/service.py`, `visits/service.py`, `identity/models.py`, `test_email_recovery.py`, `record`, `demo/service.py`, `circle/service.py`, `reminders/service.py`, `records/service.py`, `timedelta`, `signup`, `sharing/service.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `db.py`, `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `extraction/service.py`, `google.py`, `assistant/service.py`, `documents/router.py`, `ratelimit.py`, `main.py`, `conftest.py`, `demo/service.py`, `circle/service.py`, `reminders/service.py`, `env.py`, `User`, `sharing/service.py`, `notify/service.py`, `storage.py`, `documents/service.py`, `test_timeline_dashboard.py`, `Settings`, `test_ratelimit.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_labs.py`, `test_auth.py`, `timedelta`, `signup`, `sharing/service.py`, `test_google_signin.py`, `test_ratelimit.py`, `conftest.py`, `test_timeline_dashboard.py`, `test_email_recovery.py`, `reminders/service.py`, `test_integrations.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 40 inferred relationships involving `User` (e.g. with `accept()` and `set_role()`) actually correct?**
  _`User` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `utcnow()` (e.g. with `accept()` and `invite()`) actually correct?**
  _`utcnow()` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 48 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Features`, `Architecture at a glance`, `Engineering highlights` to the rest of the system?**
  _242 weakly-connected nodes found - possible documentation gaps or missing edges._