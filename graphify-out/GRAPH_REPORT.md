# Graph Report - MedSpace  (2026-10-05)

## Corpus Check
- 338 files · ~147,928 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2806 nodes · 6716 edges · 255 communities (168 shown, 87 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 440 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0979c193`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build_pdf
- circle/service.py
- timeline/service.py
- dependencies
- devDependencies
- get_settings
- identity/security.py
- integrations/service.py
- Architecture Decision Records
- User
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- identity/router.py
- ExtractionPayload
- FeatureBento.jsx
- auth.jsx
- HttpGoogleClient
- assistant/service.py
- reminders/service.py
- visits/service.py
- documents/router.py
- ratelimit.py
- ReviewForm.jsx
- test_eval.py
- test_email_recovery.py
- test_caregiver_reminders.py
- EasterEggs.jsx
- push.py
- utcnow
- SearchPalette.jsx
- integrations/api.js
- score.py
- confirm
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- supply/service.py
- signup
- MedSpace
- db.py
- visits/api.js
- sharing/router.py
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
- sharing/service.py
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
- env.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- test_evidence.py
- conftest.py
- main.py
- doses/api.js
- FastEmbedEmbedder
- documents/service.py
- extraction/service.py
- notify/service.py
- RecoveryForms.jsx
- assistant/router.py
- offline.js
- test_supply.py
- useResendVerification
- BackgroundTasks
- hooks.js
- VisitPrep.jsx
- CurrentUser
- main.jsx
- files.py
- CircleAccept.jsx
- AsyncClient
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
- identity/service.py
- llm.py
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
- errors.py
- deps.py
- record
- clear_dose
- test_sharing.py
- get_mailer
- test_visits.py
- export.py
- HashEmbedder
- Extraction evaluation
- Embedder
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

## God Nodes (most connected - your core abstractions)
1. `csrf()` - 97 edges
2. `User` - 94 edges
3. `get_settings()` - 65 edges
4. `utcnow()` - 61 edges
5. `signup()` - 52 edges
6. `record()` - 44 edges
7. `NotFound` - 38 edges
8. `Architecture Decision Records` - 34 edges
9. `Medication` - 32 edges
10. `build_pdf()` - 28 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `_redirect_to_google()` --calls--> `pkce_pair()`  [INFERRED]
  backend/app/modules/integrations/router.py → backend/app/modules/integrations/google.py
- `_issue()` --calls--> `new_opaque_token()`  [INFERRED]
  backend/app/modules/identity/recovery.py → backend/app/core/security.py
- `_issue()` --calls--> `sha256_hex()`  [INFERRED]
  backend/app/modules/identity/recovery.py → backend/app/core/security.py
- `_issue()` --calls--> `EmailToken`  [INFERRED]
  backend/app/modules/identity/recovery.py → backend/app/modules/identity/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (255 total, 87 thin omitted)

### Community 0 - "build_pdf"
Cohesion: 0.20
Nodes (28): build_pdf(), drain(), Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works(), test_review_then_confirm_creates_notes() (+20 more)

### Community 1 - "circle/service.py"
Cohesion: 0.16
Nodes (30): CareLink, Base, IdMixin, TimestampMixin, Care circle: people a user lets see (or help with) their records (ADR-026)., An invitation and, once accepted, a grant from `owner` to `caregiver`.…, accept(), active_helper_link() (+22 more)

### Community 2 - "timeline/service.py"
Cohesion: 0.18
Nodes (23): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+15 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, @fontsource/zen-dots, dependencies, clsx, date-fns (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+17 more)

### Community 5 - "get_settings"
Cohesion: 0.12
Nodes (22): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., Auth cookie helpers shared by the identity and demo routers., share_url(), Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Load (and on first run, download) the embedding model before the first request… (+14 more)

### Community 7 - "identity/security.py"
Cohesion: 0.15
Nodes (32): AppError, Conflict, verify_password(), provisioning_uri(), Opaque refresh token, stored hashed. Rotated on every use; reuse revokes the…, One-time backup codes for two-step verification; only hashes are stored., RecoveryCode, RefreshToken (+24 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.22
Nodes (28): encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), appointment_event(), _clock(), _delete_remote() (+20 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.06
Nodes (34): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+26 more)

### Community 10 - "User"
Cohesion: 0.14
Nodes (31): AdherenceDay, AdherenceOut, Counts, DoseLogIn, DoseLogOut, DoseSlot, MedicationAdherence, BaseModel (+23 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.13
Nodes (31): constant_time_equals(), callback(), connect(), disconnect(), _frontend(), google_sign_in(), preview(), providers() (+23 more)

### Community 12 - "documents/api.js"
Cohesion: 0.10
Nodes (13): ACTIVE, docKeys, isProcessing(), ADR-0031, previewUrl(), uploadDocument(), useDocument(), useDocuments() (+5 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/router.py"
Cohesion: 0.05
Nodes (105): accept(), get_circle(), invite(), preview(), Request, UUID, Dose alerts about someone you help: off, when due, or if not ticked after 30/60…, revoke() (+97 more)

### Community 15 - "ExtractionPayload"
Cohesion: 0.12
Nodes (24): Any, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload (+16 more)

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
Cohesion: 0.11
Nodes (35): ChatMessage, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, answer_stream(), _best_snippet(), build_prompt(), chunk_pages(), classify() (+27 more)

### Community 20 - "reminders/service.py"
Cohesion: 0.06
Nodes (73): Import every module's ORM models so `Base.metadata` is complete (Alembic,…, CaregiverReminderLog, PushSubscription, Base, IdMixin, TimestampMixin, Dose reminders by push notification (ADR-028)., One browser (or installed app) that agreed to receive notifications. (+65 more)

### Community 21 - "visits/service.py"
Cohesion: 0.11
Nodes (50): The user's own part of a visit brief: when, with whom, and what they want to…, VisitPrep, create_visit(), delete_visit(), get_visit(), list_visits(), CurrentUser, DbSession (+42 more)

### Community 22 - "documents/router.py"
Cohesion: 0.12
Nodes (32): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+24 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.07
Nodes (37): RateLimited, caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore (+29 more)

### Community 24 - "ReviewForm.jsx"
Cohesion: 0.14
Nodes (22): evidenceKeys(), findSpot(), itemName(), ADR-0031, evidence, values, blank(), CARE_KINDS (+14 more)

### Community 25 - "test_eval.py"
Cohesion: 0.12
Nodes (29): ambiguous_date(), _apply_sig(), diet_category(), _diet_notes(), _dosing(), extract(), _lab_results(), _lab_row() (+21 more)

### Community 26 - "test_email_recovery.py"
Cohesion: 0.20
Nodes (26): FakeMailer, Keeps the last messages in memory (the dev outbox and tests read them)., link_token(), The token from the first `<path>?token=...` link in an email body., forgot(), login(), AsyncClient, MonkeyPatch (+18 more)

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
Cohesion: 0.22
Nodes (23): AsyncSession, utcnow(), cancel_email_change(), confirm_email_change(), _consume(), EmailChange, _issue(), Outgoing (+15 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "score.py"
Cohesion: 0.20
Nodes (16): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+8 more)

### Community 34 - "confirm"
Cohesion: 0.42
Nodes (11): confirm(), discard(), evidence_for_document(), get_extraction(), latest_for_document(), AsyncSession, Request, UUID (+3 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.08
Nodes (26): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+18 more)

### Community 36 - "records/service.py"
Cohesion: 0.05
Nodes (103): Extraction, ExtractionStatus, One AI reading of a document. Versioned; only a confirmed version becomes…, build_export(), AsyncSession, CareAction, DietNote, LabResult (+95 more)

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
Cohesion: 0.14
Nodes (32): clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get, post, put (+24 more)

### Community 41 - "signup"
Cohesion: 0.30
Nodes (23): signup(), code_for(), login(), new_client(), AsyncClient, Account security (ADR-029): two-step verification, active sessions, password…, test_a_code_cannot_be_used_twice(), test_cannot_revoke_someone_elses_session() (+15 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "db.py"
Cohesion: 0.16
Nodes (20): Base, IdMixin, datetime, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin, uuid7() (+12 more)

### Community 45 - "sharing/router.py"
Cohesion: 0.18
Nodes (22): create_share(), list_shares(), open_share(), CurrentUser, DbSession, delete, get, post (+14 more)

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
Cohesion: 0.22
Nodes (12): create_access_token(), create_purpose_token(), decode_access_claims(), decode_access_token(), decode_purpose_token(), UUID, Password hashing, JWT access tokens, opaque token helpers and field encryption., `session_id` (the refresh-token family) lets a signed-out device's access token… (+4 more)

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

### Community 115 - "sharing/service.py"
Cohesion: 0.23
Nodes (21): Gone, NotFound, new_opaque_token(), A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, create(), link_status(), list_links() (+13 more)

### Community 117 - "csrf"
Cohesion: 0.54
Nodes (13): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+5 more)

### Community 127 - "test_integrations.py"
Cohesion: 0.27
Nodes (16): decrypt(), _fernet(), dose_event(), _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient (+8 more)

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
Cohesion: 0.16
Nodes (25): ADR-0029, securityKeys, useCancelEmailChange(), useChangePassword(), useDisableMfa(), useEnableMfa(), useEndOtherSessions(), useEndSession() (+17 more)

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
Cohesion: 0.20
Nodes (14): code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), Time-based one-time passwords (RFC 6238, the format authenticator apps use).…, 160 random bits as unpadded base32, what authenticator apps expect. (+6 more)

### Community 145 - "google.py"
Cohesion: 0.10
Nodes (9): GoogleClient, GoogleIdentity, has_sync_scopes(), pkce_pair(), Any, Protocol, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, True when the user left both Calendar and Tasks ticked on Google's consent… (+1 more)

### Community 146 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 147 - "circle/api.js"
Cohesion: 0.18
Nodes (18): ActingBanner(), circleKeys, ADR-0032, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite() (+10 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "test_evidence.py"
Cohesion: 0.11
Nodes (23): _clean(), _date_variants(), locate(), _Locator, Document, Where on the page each extracted value is printed (ADR-031). Given the original…, First variant found, preferring the hinted page (or the anchor's page and…, Evidence for every field we can find: {"fields": {path: spot}, "items": {path:… (+15 more)

### Community 151 - "conftest.py"
Cohesion: 0.23
Nodes (12): reset_rate_limits(), auth_client(), _clean_tables(), client(), confirm_email(), mailbox(), AsyncClient, Test harness: real Postgres (pgvector), fakes for every external service. (+4 more)

### Community 152 - "main.py"
Cohesion: 0.17
Nodes (16): CSRFMiddleware, Request, Response, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware, SecurityHeadersMiddleware, Import every module's jobs so the registry in `app.shared.queue.JOBS` is… (+8 more)

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 156 - "documents/service.py"
Cohesion: 0.14
Nodes (30): PayloadTooLarge, UnsupportedMedia, Document, DocumentKind, DocumentPage, DocumentStatus, StrEnum, create_document() (+22 more)

### Community 157 - "extraction/service.py"
Cohesion: 0.19
Nodes (19): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, EvidenceSpot, ExtractedCareAction, ExtractedDietNote (+11 more)

### Community 158 - "notify/service.py"
Cohesion: 0.15
Nodes (17): app_url(), _html(), Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the…, To the address being replaced: once when a change is asked for, once when it…, _send(), send_circle_invite(), send_email_change_link(), send_email_change_notice() (+9 more)

### Community 160 - "assistant/router.py"
Cohesion: 0.19
Nodes (19): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+11 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "test_supply.py"
Cohesion: 0.24
Nodes (19): _at(), estimate(), date, datetime, Pure: the estimate for one medicine at `now` (an aware datetime in the user's…, _count(), _med(), _now() (+11 more)

### Community 168 - "hooks.js"
Cohesion: 0.50
Nodes (6): DeviceSettings(), useInstallPrompt(), useOnline(), usePendingDoseTicks(), useSavedAt(), OfflineBanner()

### Community 169 - "VisitPrep.jsx"
Cohesion: 0.28
Nodes (3): newId(), Prompts(), Questions()

### Community 172 - "main.jsx"
Cohesion: 0.16
Nodes (7): Providers(), router, emit(), listeners, promptInstall(), ADR-0025, queryClient

### Community 173 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 175 - "AsyncClient"
Cohesion: 0.38
Nodes (16): AsyncClient, change(), change_token(), confirm(), Response, Changing the account email (ADR-033): proof, confirmation by the new inbox,…, test_addresses_already_in_use_and_unchanged_ones_are_refused(), test_change_happens_only_when_the_new_inbox_confirms() (+8 more)

### Community 177 - "S3Storage"
Cohesion: 0.25
Nodes (3): ServiceUnavailable, Any S3-compatible store (MinIO, Cloudflare R2, AWS S3). boto3 calls run in a…, S3Storage

### Community 183 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 197 - "demo/service.py"
Cohesion: 0.22
Nodes (14): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+6 more)

### Community 198 - "test_labs.py"
Cohesion: 0.15
Nodes (24): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+16 more)

### Community 199 - "test_assistant.py"
Cohesion: 0.42
Nodes (12): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+4 more)

### Community 200 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 201 - "identity/service.py"
Cohesion: 0.23
Nodes (15): hash_password(), needs_rehash(), sha256_hex(), authenticate(), delete_user(), get_user(), issue_session(), AsyncSession (+7 more)

### Community 202 - "llm.py"
Cohesion: 0.24
Nodes (8): GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol, LLM port and the Groq adapter (ADR-003). When `LLM_PROVIDER=fake` (the default)…

### Community 203 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 230 - "errors.py"
Cohesion: 0.20
Nodes (12): AppError, Forbidden, install_error_handlers(), _problem(), Any, Exception, FastAPI, Request (+4 more)

### Community 231 - "deps.py"
Cohesion: 0.33
Nodes (11): _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, UUID, Shared FastAPI dependencies. (+3 more)

### Community 232 - "record"
Cohesion: 0.27
Nodes (10): AuditLog, Append-only trail of security-relevant actions. Never updated or deleted by app…, list_for_user(), Any, AsyncSession, Request, UUID, Audit trail: `record()` is the single write path, used by every module. (+2 more)

### Community 233 - "clear_dose"
Cohesion: 0.27
Nodes (11): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+3 more)

### Community 234 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 235 - "get_mailer"
Cohesion: 0.22
Nodes (8): outbox(), get, Dev-only outbox: read simulated emails (local testing and e2e). Never mounted…, get_mailer(), Mailer, Tests swap in their own mailer (None resets to the configured one)., set_mailer(), Protocol

### Community 236 - "test_visits.py"
Cohesion: 0.49
Nodes (9): _create(), _demo(), AsyncClient, date, Visit prep: the user's questions plus a live, factual brief built from…, test_a_brief_can_be_shared_and_stays_private(), test_brief_reports_records_since_a_date(), test_create_edit_and_delete() (+1 more)

### Community 237 - "export.py"
Cohesion: 0.22
Nodes (3): Account data export: one JSON document with every record the user owns.…, EmailToken, A one-time link sent by email (ADR-030): verify an address, or reset a…

### Community 239 - "Extraction evaluation"
Cohesion: 0.33
Nodes (6): Extraction evaluation, Method, Metrics, Results: offline extractor, Running it, What the evaluation found, and what changed

## Knowledge Gaps
- **262 isolated node(s):** `Features`, `Architecture at a glance`, `Engineering highlights`, `Tech stack`, `Prerequisites` (+257 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **87 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `ExtractionPayload`, `google.py`, `env.py`, `assistant/service.py`, `documents/router.py`, `ratelimit.py`, `main.py`, `documents/service.py`, `push.py`, `db.py`, `S3Storage`, `Settings`, `core/security.py`, `demo/service.py`, `identity/service.py`, `llm.py`, `test_timeline_dashboard.py`, `get_mailer`, `sharing/service.py`, `test_integrations.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `User` connect `User` to `test_supply.py`, `timeline/service.py`, `records/service.py`, `demo/service.py`, `deps.py`, `identity/security.py`, `identity/service.py`, `integrations/service.py`, `supply/service.py`, `signup`, `export.py`, `test_google_signin.py`, `assistant/service.py`, `sharing/service.py`, `visits/service.py`, `test_email_recovery.py`, `documents/service.py`, `core/security.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_auth.py`, `build_pdf`, `test_supply.py`, `test_labs.py`, `test_assistant.py`, `test_doses.py`, `signup`, `test_sharing.py`, `test_timeline_dashboard.py`, `test_visits.py`, `test_google_signin.py`, `AsyncClient`, `ratelimit.py`, `conftest.py`, `test_email_recovery.py`, `test_caregiver_reminders.py`, `test_integrations.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `csrf()` (e.g. with `change()` and `test_change_needs_the_password_and_a_code_with_two_step_on()`) actually correct?**
  _`csrf()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `User` (e.g. with `begin_setup()` and `change_password()`) actually correct?**
  _`User` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `utcnow()` (e.g. with `accept()` and `invite()`) actually correct?**
  _`utcnow()` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 47 INFERRED edges - model-reasoned connections that need verification._