# Graph Report - MedSpace  (2026-10-04)

## Corpus Check
- 332 files · ~142,552 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2674 nodes · 6413 edges · 217 communities (160 shown, 57 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 353 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f0c47951`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_pdf
- circle/router.py
- db.py
- dependencies
- devDependencies
- get_settings
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
- supply/router.py
- visits/service.py
- documents/router.py
- ratelimit.py
- ReviewForm.jsx
- heuristic.py
- test_email_recovery.py
- recovery.py
- EasterEggs.jsx
- timedelta
- reminders/service.py
- SearchPalette.jsx
- integrations/api.js
- test_eval.py
- confirm
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- supply/service.py
- signup
- MedSpace
- sharing/service.py
- visits/api.js
- Message
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
- core/security.py
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
- llm.py
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
- GoogleClient
- deps.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- test_evidence.py
- conftest.py
- main.py
- doses/api.js
- embeddings.py
- documents/service.py
- extraction/schemas.py
- notify/service.py
- test_visits.py
- offline.js
- assistant/router.py
- record
- useResendVerification
- User
- hooks.js
- VisitPrep.jsx
- Extraction evaluation
- main.jsx
- files.py
- CircleAccept.jsx
- install.js
- S3Storage
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
- MonkeyPatch
- demo/service.py
- test_labs.py
- test_assistant.py
- test_doses.py
- samples.py
- extraction/jobs.py
- test_timeline_dashboard.py
- CurrentUser
- DbSession
- get
- post
- ObjectStorage
- field_validator
- Any
- Exception
- links.js
- date
- BaseModel

## God Nodes (most connected - your core abstractions)
1. `User` - 110 edges
2. `csrf()` - 87 edges
3. `get_settings()` - 72 edges
4. `utcnow()` - 59 edges
5. `signup()` - 44 edges
6. `NotFound` - 39 edges
7. `record()` - 39 edges
8. `Medication` - 33 edges
9. `Architecture Decision Records` - 32 edges
10. `Base` - 30 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `get_evidence()` --uses--> `EvidenceOut`  [INFERRED]
  backend/app/modules/extraction/router.py → backend/app/modules/extraction/schemas.py
- `confirm_extraction()` --uses--> `ConfirmIn`  [INFERRED]
  backend/app/modules/extraction/router.py → backend/app/modules/extraction/schemas.py
- `MedicationOut` --uses--> `ScheduleModel`  [INFERRED]
  backend/app/modules/records/schemas.py → backend/app/modules/extraction/schemas.py
- `MedicationUpdate` --uses--> `ScheduleModel`  [INFERRED]
  backend/app/modules/records/schemas.py → backend/app/modules/extraction/schemas.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (217 total, 57 thin omitted)

### Community 0 - "build_pdf"
Cohesion: 0.20
Nodes (29): AsyncClient, build_pdf(), drain(), Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works() (+21 more)

### Community 1 - "circle/router.py"
Cohesion: 0.09
Nodes (48): Forbidden, accept(), get_circle(), invite(), preview(), BackgroundTasks, CurrentUser, DbSession (+40 more)

### Community 2 - "db.py"
Cohesion: 0.13
Nodes (25): Base, IdMixin, datetime, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin, uuid7() (+17 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "get_settings"
Cohesion: 0.11
Nodes (22): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., upload_document(), enqueue(), _get_arq_pool(), Any (+14 more)

### Community 6 - "router.jsx"
Cohesion: 0.20
Nodes (3): AppLayout(), AuthLayout(), router

### Community 7 - "utcnow"
Cohesion: 0.17
Nodes (29): AppError, utcnow(), verify_password(), One-time backup codes for two-step verification; only hashes are stored., RecoveryCode, begin_setup(), change_password(), check_second_factor() (+21 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.18
Nodes (33): Conflict, get_google(), GoogleAPIError, GoogleAuthError, Exception, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, Consent was revoked or the refresh token is no longer valid., OAuthConnection (+25 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.06
Nodes (32): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+24 more)

### Community 10 - "doses/service.py"
Cohesion: 0.12
Nodes (40): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+32 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.12
Nodes (33): has_sync_scopes(), pkce_pair(), True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect(), _frontend(), google_sign_in() (+25 more)

### Community 12 - "documents/api.js"
Cohesion: 0.10
Nodes (13): ACTIVE, docKeys, isProcessing(), ADR-0031, previewUrl(), uploadDocument(), useDocument(), useDocuments() (+5 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/router.py"
Cohesion: 0.07
Nodes (74): demo_login(), DbSession, post, Request, Response, clear_auth_cookies(), Response, Auth cookie helpers shared by the identity and demo routers. (+66 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.13
Nodes (26): Any, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractedCareAction (+18 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 19 - "assistant/service.py"
Cohesion: 0.11
Nodes (35): ChatMessage, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, answer_stream(), _best_snippet(), build_prompt(), chunk_pages() (+27 more)

### Community 20 - "supply/router.py"
Cohesion: 0.20
Nodes (15): clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get, post, put (+7 more)

### Community 21 - "visits/service.py"
Cohesion: 0.06
Nodes (74): Account data export: one JSON document with every record the user owns.…, get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut (+66 more)

### Community 22 - "documents/router.py"
Cohesion: 0.21
Nodes (21): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+13 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.07
Nodes (37): RateLimited, caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore (+29 more)

### Community 24 - "ReviewForm.jsx"
Cohesion: 0.14
Nodes (22): evidenceKeys(), findSpot(), itemName(), ADR-0031, evidence, values, blank(), CARE_KINDS (+14 more)

### Community 25 - "heuristic.py"
Cohesion: 0.13
Nodes (24): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+16 more)

### Community 26 - "test_email_recovery.py"
Cohesion: 0.19
Nodes (28): FakeMailer, Keeps the last messages in memory (the dev outbox and tests read them)., confirm_email(), link_token(), The token from the first `<path>?token=...` link in an email body., Follow the verification link from the outbox, as the address owner would., forgot(), login() (+20 more)

### Community 27 - "recovery.py"
Cohesion: 0.28
Nodes (14): EmailToken, A one-time link sent by email (ADR-030): verify an address, or reset a…, _consume(), _issue(), Outgoing, AsyncSession, Request, Email verification and password reset (ADR-030). Links carry a random token;… (+6 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "timedelta"
Cohesion: 0.33
Nodes (16): _at(), estimate(), date, datetime, Pure: the estimate for one medicine at `now` (an aware datetime in the user's…, _count(), _med(), _now() (+8 more)

### Community 30 - "reminders/service.py"
Cohesion: 0.05
Nodes (83): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+75 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "test_eval.py"
Cohesion: 0.19
Nodes (18): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+10 more)

### Community 34 - "confirm"
Cohesion: 0.20
Nodes (22): confirm_extraction(), discard_extraction(), get_evidence(), get_latest_extraction(), Request, UUID, Where each field of the latest reading (or, with `confirmed`, the confirmed…, confirm() (+14 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.08
Nodes (24): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+16 more)

### Community 36 - "records/service.py"
Cohesion: 0.05
Nodes (104): NotFound, Extraction, ExtractionStatus, One AI reading of a document. Versioned; only a confirmed version becomes…, build_export(), AsyncSession, CareAction, DietNote (+96 more)

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
Cohesion: 0.26
Nodes (19): MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, SupplyOut, clear_supply(), list_supplies(), _out(), AsyncSession, UUID (+11 more)

### Community 41 - "signup"
Cohesion: 0.30
Nodes (23): signup(), code_for(), login(), new_client(), AsyncClient, Account security (ADR-029): two-step verification, active sessions, password…, test_a_code_cannot_be_used_twice(), test_cannot_revoke_someone_elses_session() (+15 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/service.py"
Cohesion: 0.09
Nodes (55): Gone, new_opaque_token(), sha256_hex(), A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create_share(), list_shares() (+47 more)

### Community 45 - "Message"
Cohesion: 0.24
Nodes (5): Message, SmtpMailer, test_smtp_failures_are_reported_not_raised(), test_smtp_mailer_builds_a_multipart_message_and_uses_starttls(), EmailMessage

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
Cohesion: 0.15
Nodes (10): RFC-6238, here, SAMPLE, confirmEmail(), emailLink(), expectAccessible(), signUp(), startDemo() (+2 more)

### Community 60 - "Settings"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "core/security.py"
Cohesion: 0.16
Nodes (17): create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), decode_purpose_token(), encrypt(), _fernet(), hash_password() (+9 more)

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

### Community 115 - "llm.py"
Cohesion: 0.23
Nodes (9): get_llm(), GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol (+1 more)

### Community 117 - "csrf"
Cohesion: 0.39
Nodes (16): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+8 more)

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

### Community 145 - "GoogleClient"
Cohesion: 0.11
Nodes (5): GoogleClient, GoogleIdentity, Any, Protocol, Tokens

### Community 146 - "deps.py"
Cohesion: 0.25
Nodes (14): get_session(), AsyncSession, _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request (+6 more)

### Community 147 - "circle/api.js"
Cohesion: 0.25
Nodes (12): ActingBanner(), circleKeys, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite(), useRemoveLink() (+4 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "test_evidence.py"
Cohesion: 0.11
Nodes (24): _clean(), _date_variants(), locate(), _Locator, Document, Where on the page each extracted value is printed (ADR-031). Given the original…, First variant found, preferring the hinted page (or the anchor's page and…, Evidence for every field we can find: {"fields": {path: spot}, "items": {path:… (+16 more)

### Community 151 - "conftest.py"
Cohesion: 0.14
Nodes (19): reset_rate_limits(), outbox(), get, Dev-only outbox: read simulated emails (local testing and e2e). Never mounted…, get_mailer(), Mailer, Email port (ADR-030): SMTP in production, an in-memory outbox in dev, demo and…, Tests swap in their own mailer (None resets to the configured one). (+11 more)

### Community 152 - "main.py"
Cohesion: 0.18
Nodes (16): CSRFMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware, SecurityHeadersMiddleware, constant_time_equals() (+8 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "embeddings.py"
Cohesion: 0.13
Nodes (10): Embedder, FastEmbedEmbedder, get_embedder(), HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and… (+2 more)

### Community 156 - "documents/service.py"
Cohesion: 0.12
Nodes (34): AppError, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI, Request (+26 more)

### Community 157 - "extraction/schemas.py"
Cohesion: 0.15
Nodes (21): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, EvidenceOut, EvidenceSpot, ExtractedDietNote (+13 more)

### Community 158 - "notify/service.py"
Cohesion: 0.40
Nodes (9): app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, _send(), send_circle_invite(), send_password_reset(), send_security_alert(), send_verification() (+1 more)

### Community 160 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "assistant/router.py"
Cohesion: 0.19
Nodes (19): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+11 more)

### Community 163 - "record"
Cohesion: 0.15
Nodes (17): AuditLog, Append-only trail of security-relevant actions. Never updated or deleted by app…, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+9 more)

### Community 166 - "User"
Cohesion: 0.16
Nodes (14): Import every module's ORM models so `Base.metadata` is complete (Alembic,…, Opaque refresh token, stored hashed. Rotated on every use; reuse revokes the…, RefreshToken, User, delete_user(), get_user(), issue_session(), IssuedSession (+6 more)

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
Cohesion: 0.24
Nodes (4): Providers(), ApiError, ADR-0025, queryClient

### Community 173 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 175 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 177 - "S3Storage"
Cohesion: 0.25
Nodes (3): ServiceUnavailable, Any S3-compatible store (MinIO, Cloudflare R2, AWS S3). boto3 calls run in a…, S3Storage

### Community 183 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 197 - "demo/service.py"
Cohesion: 0.23
Nodes (15): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+7 more)

### Community 198 - "test_labs.py"
Cohesion: 0.26
Nodes (14): lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_single_line_rows_and_printed_flags(), test_heuristic_reads_split_line_lab_tables(), test_labs_are_private_and_deletable() (+6 more)

### Community 199 - "test_assistant.py"
Cohesion: 0.42
Nodes (12): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+4 more)

### Community 200 - "test_doses.py"
Cohesion: 0.37
Nodes (13): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_demo_history_and_ask(), test_dose_logs_are_private() (+5 more)

### Community 201 - "samples.py"
Cohesion: 0.31
Nodes (10): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+2 more)

### Community 202 - "extraction/jobs.py"
Cohesion: 0.25
Nodes (6): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, process_document(), Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

### Community 203 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

## Knowledge Gaps
- **252 isolated node(s):** `Features`, `Architecture at a glance`, `Engineering highlights`, `Tech stack`, `Prerequisites` (+247 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **57 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `circle/router.py`, `utcnow`, `integrations/service.py`, `doses/service.py`, `identity/router.py`, `test_google_signin.py`, `deps.py`, `assistant/service.py`, `visits/service.py`, `test_email_recovery.py`, `recovery.py`, `timedelta`, `reminders/service.py`, `records/service.py`, `supply/service.py`, `signup`, `sharing/service.py`, `core/security.py`, `demo/service.py`, `extraction/jobs.py`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `db.py`, `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `assistant/service.py`, `documents/router.py`, `ratelimit.py`, `main.py`, `conftest.py`, `embeddings.py`, `documents/service.py`, `reminders/service.py`, `notify/service.py`, `User`, `sharing/service.py`, `S3Storage`, `Settings`, `core/security.py`, `demo/service.py`, `test_timeline_dashboard.py`, `llm.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_auth.py`, `build_pdf`, `test_visits.py`, `test_labs.py`, `test_assistant.py`, `test_doses.py`, `signup`, `sharing/service.py`, `test_timeline_dashboard.py`, `test_google_signin.py`, `ratelimit.py`, `conftest.py`, `test_email_recovery.py`, `timedelta`, `reminders/service.py`, `test_integrations.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `User` (e.g. with `accept()` and `set_role()`) actually correct?**
  _`User` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `csrf()` (e.g. with `test_confirmed_records_keep_their_item_reference()` and `test_reprocessing_gets_fresh_evidence()`) actually correct?**
  _`csrf()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `utcnow()` (e.g. with `accept()` and `invite()`) actually correct?**
  _`utcnow()` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 45 INFERRED edges - model-reasoned connections that need verification._