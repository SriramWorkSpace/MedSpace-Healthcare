# Graph Report - MedSpace  (2026-10-07)

## Corpus Check
- 352 files · ~161,530 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2918 nodes · 7315 edges · 207 communities (162 shown, 45 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 110 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8c9bc46a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_eval.py
- record
- reminders/router.py
- dependencies
- devDependencies
- S3Storage
- router.jsx
- User
- reminders/service.py
- Architecture Decision Records
- doses/service.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- integrations/service.py
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
- AsyncClient
- test_caregiver_reminders.py
- EasterEggs.jsx
- test_evidence.py
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
- demo/service.py
- MedSpace
- db.py
- visits/api.js
- test_auth.py
- Deploying MedSpace
- AuthForms.jsx
- records/api.js
- Visits.jsx
- scripts
- build_pdf
- SupplyDialog.jsx
- api service (alembic + uvicorn)
- lib/format.js
- Settings.jsx
- test_google_signin.py
- deps.py
- helpers.js
- Ask.jsx
- sharing/service.py
- 4. Core flows
- Diet.jsx
- identity/router.py
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
- worker.py
- csrf
- files.py
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
- test_authorization_sweep.py
- corpus.py
- Launch guide: the steps only you can do
- google.py
- circle/router.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- evidence.py
- test_timeline_dashboard.py
- main.py
- doses/api.js
- test_sharing.py
- normalize_frequency
- Extraction evaluation
- notify/service.py
- RecoveryForms.jsx
- llm.py
- offline.js
- test_ratelimit.py
- useResendVerification
- LocalStorage
- hooks.js
- VisitPrep.jsx
- install.js
- main.jsx
- ObjectStorage
- CircleAccept.jsx
- @axe-core/playwright
- totp.py
- sw-template.js
- vercel.json
- labs.py
- react-router
- zod
- globals
- test_security_hardening.py
- test_assistant.py
- test_doses.py
- extraction/service.py
- safe_path
- links.js
- assistant/service.py
- get_settings
- FakeMailer
- test_email_recovery.py
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
- `_clean_tables()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `_schema()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `demo_login()` --uses--> `NotFound`  [INFERRED]
  backend/app/modules/demo/router.py → backend/app/core/errors.py
- `outbox()` --uses--> `NotFound`  [INFERRED]
  backend/app/modules/notify/router.py → backend/app/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (207 total, 45 thin omitted)

### Community 0 - "test_eval.py"
Cohesion: 0.10
Nodes (34): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+26 more)

### Community 1 - "record"
Cohesion: 0.13
Nodes (35): AuditLog, Append-only trail of security-relevant actions. Never updated or deleted by app…, list_for_user(), Any, AsyncSession, Request, UUID, Audit trail: `record()` is the single write path, used by every module. (+27 more)

### Community 2 - "reminders/router.py"
Cohesion: 0.07
Nodes (47): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+39 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks (+17 more)

### Community 6 - "router.jsx"
Cohesion: 0.06
Nodes (5): MarketingLayout(), RouteError(), appLayout, authLayout, openAuthLayout()

### Community 7 - "User"
Cohesion: 0.10
Nodes (42): AppError, Forbidden, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI (+34 more)

### Community 8 - "reminders/service.py"
Cohesion: 0.15
Nodes (31): SubscriptionOut, action_token(), apply_action(), _clock(), _deliver(), _due(), get_settings_for(), _labels() (+23 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.05
Nodes (40): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+32 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (40): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+32 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.10
Nodes (38): constant_time_equals(), mfa_challenge(), The token a first-factor success hands back instead of a session., client_for_user(), has_sync_scopes(), pkce_pair(), True when the user left both Calendar and Tasks ticked on Google's consent…, Demo accounts always use the simulation: their data is synthetic and deleted… (+30 more)

### Community 12 - "documents/api.js"
Cohesion: 0.10
Nodes (13): ACTIVE, docKeys, isProcessing(), ADR-0031, previewUrl(), uploadDocument(), useDocument(), useDocuments() (+5 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "integrations/service.py"
Cohesion: 0.20
Nodes (30): Conflict, encrypt(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _client(), _clock() (+22 more)

### Community 15 - "extraction/schemas.py"
Cohesion: 0.13
Nodes (27): confirm_extraction(), discard_extraction(), get_evidence(), get_latest_extraction(), CurrentUser, DbSession, get, post (+19 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 18 - "HttpGoogleClient"
Cohesion: 0.13
Nodes (9): _events(), GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, MedSpace's own calendar (the only one calendar.app.created can reach)., Consent was revoked or the refresh token is no longer valid., test_connect_asks_for_least_privilege_scopes_with_pkce() (+1 more)

### Community 19 - "test_google_live.py"
Cohesion: 0.12
Nodes (17): connect_live(), FakeGoogleHTTP, live(), AsyncClient, fixture, Request, Response, Real Google OAuth 2.0 (GOOGLE_PROVIDER=google), with Google's HTTP endpoints… (+9 more)

### Community 20 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 21 - "visits/service.py"
Cohesion: 0.07
Nodes (73): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+65 more)

### Community 22 - "documents/router.py"
Cohesion: 0.16
Nodes (26): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+18 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.09
Nodes (22): caller_key(), client_ip(), Decision, _estimate(), get_store(), MemoryStore, Any, Request (+14 more)

### Community 24 - "ReviewForm.jsx"
Cohesion: 0.14
Nodes (22): evidenceKeys(), findSpot(), itemName(), ADR-0031, evidence, values, blank(), CARE_KINDS (+14 more)

### Community 25 - "test_labs.py"
Cohesion: 0.26
Nodes (14): lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_single_line_rows_and_printed_flags(), test_heuristic_reads_split_line_lab_tables(), test_labs_are_private_and_deletable() (+6 more)

### Community 26 - "AsyncClient"
Cohesion: 0.21
Nodes (18): forgot(), login(), AsyncClient, MonkeyPatch, Response, Pre-hijack: an attacker signs up with the victim's address and sets a password., reset_token(), subjects() (+10 more)

### Community 27 - "test_caregiver_reminders.py"
Cohesion: 0.25
Nodes (26): alerts(), caregiver(), owner_with_medicine(), AsyncClient, Response, Dose alerts for caregivers (ADR-032): opt-in per person, on time or "not ticked…, Eve, confirmed, in Ada's care circle with `role`, with a subscribed device., test_alert_when_due_with_actions_for_helpers() (+18 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "test_evidence.py"
Cohesion: 0.15
Nodes (24): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+16 more)

### Community 30 - "utcnow"
Cohesion: 0.09
Nodes (47): datetime, UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., utcnow(), uuid7(), Gone, Unauthorized, hash_password() (+39 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "score.py"
Cohesion: 0.21
Nodes (16): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+8 more)

### Community 34 - "supply/service.py"
Cohesion: 0.09
Nodes (53): MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get (+45 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.07
Nodes (28): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+20 more)

### Community 36 - "records/service.py"
Cohesion: 0.09
Nodes (70): build_export(), AsyncSession, Account data export: one JSON document with every record the user owns.…, delete_diet_note(), delete_lab_result(), get_lab_trend(), get_prescription(), list_care_actions() (+62 more)

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

### Community 41 - "demo/service.py"
Cohesion: 0.10
Nodes (49): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+41 more)

### Community 42 - "MedSpace"
Cohesion: 0.12
Nodes (16): Architecture at a glance, Deploy, Enable Google sign-in, Calendar & Tasks, Enable real AI extraction (optional), Engineering highlights, Features, Getting started, License (+8 more)

### Community 43 - "db.py"
Cohesion: 0.08
Nodes (55): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for… (+47 more)

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

### Community 51 - "build_pdf"
Cohesion: 0.19
Nodes (30): build_pdf(), drain(), Background job dispatch. `QUEUE_MODE=arq`: jobs go to Redis and run in the…, Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works() (+22 more)

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
Cohesion: 0.08
Nodes (42): get_session(), AsyncSession, _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request (+34 more)

### Community 58 - "helpers.js"
Cohesion: 0.14
Nodes (10): RFC-6238, here, SAMPLE, confirmEmail(), emailLink(), expectAccessible(), signUp(), startDemo() (+2 more)

### Community 60 - "sharing/service.py"
Cohesion: 0.24
Nodes (20): NotFound, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create(), link_status(), list_links(), open_public() (+12 more)

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "identity/router.py"
Cohesion: 0.07
Nodes (80): RateLimited, check(), Count one hit for `scope` + `key` and decide. Fails open if the store is…, demo_login(), DbSession, post, Request, Response (+72 more)

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

### Community 115 - "worker.py"
Cohesion: 0.09
Nodes (16): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, Embedder, FastEmbedEmbedder, get_embedder(), Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and…, Load (and on first run, download) the embedding model before the first request… (+8 more)

### Community 117 - "csrf"
Cohesion: 0.54
Nodes (13): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+5 more)

### Community 119 - "files.py"
Cohesion: 0.15
Nodes (15): image_size(), inspect(), Inspection, _matrix(), Exception, Rect, File inspection: type sniffing by magic bytes, PDF text extraction and page…, PNG bytes per page for the vision model. Images are passed through (re-encoded… (+7 more)

### Community 127 - "test_integrations.py"
Cohesion: 0.30
Nodes (15): decrypt(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 128 - "conftest.py"
Cohesion: 0.29
Nodes (10): reset_rate_limits(), auth_client(), _clean_tables(), client(), mailbox(), AsyncClient, fixture, Test harness: real Postgres (pgvector), fakes for every external service. (+2 more)

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

### Community 142 - "test_authorization_sweep.py"
Cohesion: 0.52
Nodes (6): fill(), owner_ids(), AsyncClient, Every route that takes an ID refuses another account's IDs, and leaves that…, snapshot(), test_no_route_accepts_another_accounts_ids()

### Community 143 - "corpus.py"
Cohesion: 0.24
Nodes (14): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+6 more)

### Community 144 - "Launch guide: the steps only you can do"
Cohesion: 0.13
Nodes (15): Housekeeping, Keep the data safe, Launch guide: the steps only you can do, Part 10. Keep reminders working on the free plan (5 minutes), Part 11. Final checks (15 minutes), Part 12. Make it shine on your resume, Part 1. Accounts to create (about 30 minutes), Part 2. Generate your secrets (5 minutes, on your computer) (+7 more)

### Community 145 - "google.py"
Cohesion: 0.10
Nodes (12): client_for_mode(), get_google(), GoogleClient, _live(), live_configured(), Any, Protocol, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory… (+4 more)

### Community 146 - "circle/router.py"
Cohesion: 0.15
Nodes (28): accept(), get_circle(), invite(), preview(), BackgroundTasks, CurrentUser, DbSession, delete (+20 more)

### Community 147 - "circle/api.js"
Cohesion: 0.18
Nodes (18): ActingBanner(), circleKeys, ADR-0032, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite() (+10 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "evidence.py"
Cohesion: 0.16
Nodes (10): _clean(), _date_variants(), _Locator, date, Rect, Where on the page each extracted value is printed (ADR-031). Given the original…, First variant found, preferring the hinted page (or the anchor's page and…, The value, then shorter word prefixes (a long note can wrap or end differently). (+2 more)

### Community 151 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 152 - "main.py"
Cohesion: 0.09
Nodes (29): Application settings, loaded from environment variables (and `.env` in…, ServiceUnavailable, configure_logging(), Logging configuration., BodySizeLimitMiddleware, _BodyTooLarge, CSRFMiddleware, BaseHTTPMiddleware (+21 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 156 - "normalize_frequency"
Cohesion: 0.22
Nodes (14): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, Schedule, _times_for(), parametrize (+6 more)

### Community 157 - "Extraction evaluation"
Cohesion: 0.33
Nodes (6): Extraction evaluation, Method, Metrics, Results: offline extractor, Running it, What the evaluation found, and what changed

### Community 158 - "notify/service.py"
Cohesion: 0.32
Nodes (12): app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, To the address being replaced: once when a change is asked for, once when it…, _send(), send_circle_invite(), send_email_change_link(), send_email_change_notice() (+4 more)

### Community 160 - "llm.py"
Cohesion: 0.27
Nodes (6): GroqProvider, LLMError, _parse_json(), Any, Exception, LLM port and the Groq adapter (ADR-003). When `LLM_PROVIDER=fake` (the default)…

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "test_ratelimit.py"
Cohesion: 0.22
Nodes (14): fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings(), test_baseline_budget_covers_every_route(), test_headers_scale_and_disable() (+6 more)

### Community 166 - "LocalStorage"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 170 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 172 - "main.jsx"
Cohesion: 0.21
Nodes (5): Providers(), router, ApiError, ADR-0025, queryClient

### Community 177 - "totp.py"
Cohesion: 0.20
Nodes (14): code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).…, 160 random bits as unpadded base32, what authenticator apps expect. (+6 more)

### Community 183 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 192 - "test_security_hardening.py"
Cohesion: 0.08
Nodes (27): field_validator, Refuse to start in production with settings that would quietly be unsafe., Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, test_production_requires_google_credentials_when_google_is_on(), png_header(), AsyncClient, parametrize (+19 more)

### Community 199 - "test_assistant.py"
Cohesion: 0.42
Nodes (12): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+4 more)

### Community 200 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 202 - "extraction/service.py"
Cohesion: 0.12
Nodes (30): ExtractionStatus, StrEnum, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt() (+22 more)

### Community 209 - "safe_path"
Cohesion: 0.33
Nodes (6): Request, Response, The request path with secret tokens replaced, for logs., safe_path(), test_token_paths_are_redacted(), RequestResponseEndpoint

### Community 230 - "assistant/service.py"
Cohesion: 0.07
Nodes (53): ChatMessage, ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut (+45 more)

### Community 231 - "get_settings"
Cohesion: 0.16
Nodes (19): get_settings(), create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), _fernet(), needs_rehash(), UUID (+11 more)

### Community 232 - "FakeMailer"
Cohesion: 0.23
Nodes (24): FakeMailer, Keeps the last messages in memory (the dev outbox and tests read them)., confirm_email(), link_token(), The token from the first `<path>?token=...` link in an email body., Follow the verification link from the outbox, as the address owner would., change(), change_token() (+16 more)

### Community 235 - "test_email_recovery.py"
Cohesion: 0.09
Nodes (25): outbox(), get, Dev-only outbox: read simulated emails (local testing and e2e). Never mounted…, BrevoMailer, get_mailer(), Mailer, Message, AsyncClient (+17 more)

## Knowledge Gaps
- **286 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+281 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `record`, `reminders/router.py`, `S3Storage`, `User`, `reminders/service.py`, `integrations/router.py`, `google.py`, `test_google_live.py`, `documents/router.py`, `ratelimit.py`, `main.py`, `test_timeline_dashboard.py`, `notify/service.py`, `utcnow`, `llm.py`, `test_ratelimit.py`, `demo/service.py`, `db.py`, `build_pdf`, `sharing/service.py`, `identity/router.py`, `test_security_hardening.py`, `extraction/service.py`, `safe_path`, `assistant/service.py`, `test_email_recovery.py`, `worker.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `record`, `reminders/service.py`, `doses/service.py`, `integrations/router.py`, `integrations/service.py`, `circle/router.py`, `test_google_live.py`, `visits/service.py`, `utcnow`, `supply/service.py`, `records/service.py`, `signup`, `demo/service.py`, `db.py`, `test_google_signin.py`, `deps.py`, `sharing/service.py`, `extraction/service.py`, `assistant/service.py`, `FakeMailer`, `test_email_recovery.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `conftest.py`, `test_authorization_sweep.py`, `test_google_live.py`, `test_visits.py`, `test_timeline_dashboard.py`, `test_labs.py`, `AsyncClient`, `test_sharing.py`, `test_caregiver_reminders.py`, `test_evidence.py`, `test_ratelimit.py`, `supply/service.py`, `signup`, `test_auth.py`, `build_pdf`, `test_google_signin.py`, `test_security_hardening.py`, `test_assistant.py`, `test_doses.py`, `FakeMailer`, `test_email_recovery.py`, `test_integrations.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _286 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_eval.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1036036036036036 - nodes in this community are weakly interconnected._
- **Should `record` be split into smaller, more focused modules?**
  _Cohesion score 0.12612612612612611 - nodes in this community are weakly interconnected._
- **Should `reminders/router.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07402597402597402 - nodes in this community are weakly interconnected._