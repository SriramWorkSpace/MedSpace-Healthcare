# Graph Report - MedSpace  (2026-10-03)

## Corpus Check
- 302 files · ~120,584 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2337 nodes · 5642 edges · 182 communities (146 shown, 36 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 117 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d35dc42e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_diet_notes.py
- reminders/service.py
- db.py
- dependencies
- devDependencies
- Medication
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
- sharing/service.py
- extraction/jobs.py
- llm.py
- visits/service.py
- documents/router.py
- identity/router.py
- mapping.js
- test_eval.py
- audit/router.py
- test_reminders.py
- EasterEggs.jsx
- google.py
- samples.py
- SearchPalette.jsx
- integrations/api.js
- score.py
- confirm_extraction
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- timedelta
- test_google_signin.py
- MedSpace
- sharing/router.py
- visits/api.js
- extraction/schemas.py
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
- get_settings
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
- User
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
- test_timeline_dashboard.py
- ReminderSettings.jsx
- Conflict
- test_sharing.py
- test_auth.py
- csrf
- labs.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- corpus.py
- test_doses.py
- SignupIn
- doses/api.js
- export.py
- demo/service.py
- ObjectStorage
- test_labs.py
- test_assistant.py
- deps.py
- offline.js
- files.py
- record
- .dispatch
- conftest.py
- ratelimit.py
- hooks.js
- VisitPrep.jsx
- Extraction evaluation
- main.jsx
- search
- CircleAccept.jsx
- install.js
- errors.py
- sw-template.js
- _diet_notes

## God Nodes (most connected - your core abstractions)
1. `User` - 90 edges
2. `get_settings()` - 72 edges
3. `csrf()` - 67 edges
4. `utcnow()` - 49 edges
5. `Base` - 44 edges
6. `IdMixin` - 39 edges
7. `NotFound` - 39 edges
8. `Medication` - 32 edges
9. `TimestampMixin` - 29 edges
10. `record()` - 29 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `_clean_tables()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `_schema()` --uses--> `Base`  [INFERRED]
  backend/tests/conftest.py → backend/app/core/db.py
- `demo_login()` --uses--> `NotFound`  [INFERRED]
  backend/app/modules/demo/router.py → backend/app/core/errors.py
- `apply_action()` --uses--> `NotFound`  [INFERRED]
  backend/app/modules/reminders/service.py → backend/app/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (182 total, 36 thin omitted)

### Community 0 - "test_diet_notes.py"
Cohesion: 0.25
Nodes (22): build_pdf(), drain(), Wait for all inline jobs (used by tests)., AsyncClient, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_demo_has_diet_notes_and_they_are_private(), test_reconfirming_replaces_notes_and_delete_works(), test_review_then_confirm_creates_notes() (+14 more)

### Community 1 - "reminders/service.py"
Cohesion: 0.06
Nodes (72): action(), config(), get_settings(), list_subscriptions(), put_settings(), CurrentUser, DbSession, delete (+64 more)

### Community 2 - "db.py"
Cohesion: 0.14
Nodes (28): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for… (+20 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "Medication"
Cohesion: 0.11
Nodes (29): appointment_event(), _clock(), dose_event(), plan_items(), Planned, _rrule(), task_body(), CareAction (+21 more)

### Community 6 - "router.jsx"
Cohesion: 0.08
Nodes (4): AppLayout(), AuthLayout(), MarketingLayout(), RouteError()

### Community 7 - "assistant/service.py"
Cohesion: 0.06
Nodes (59): ChatMessage, ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut (+51 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.28
Nodes (23): encrypt(), get_google(), OAuthConnection, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., access_token(), _delete_remote(), disconnect(), get_connection() (+15 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.07
Nodes (29): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+21 more)

### Community 10 - "documents/service.py"
Cohesion: 0.26
Nodes (18): Document, create_document(), delete_document(), get_document(), get_document_by_id(), list_documents(), page_preview_png(), purge_user_files() (+10 more)

### Community 11 - "integrations/router.py"
Cohesion: 0.11
Nodes (34): constant_time_equals(), has_sync_scopes(), pkce_pair(), True when the user left both Calendar and Tasks ticked on Google's consent…, callback(), connect(), disconnect(), _frontend() (+26 more)

### Community 12 - "documents/api.js"
Cohesion: 0.11
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "TrendChart.jsx"
Cohesion: 0.21
Nodes (11): describeChange(), FLAG_LABELS, formatNumber(), buildScale(), linePath(), niceTicks(), PAD, Sparkline() (+3 more)

### Community 14 - "identity/service.py"
Cohesion: 0.13
Nodes (27): UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), create_access_token(), hash_password(), needs_rehash(), new_opaque_token(), UUID (+19 more)

### Community 15 - "extraction/service.py"
Cohesion: 0.13
Nodes (27): ExtractionStatus, StrEnum, _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt() (+19 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.15
Nodes (16): ADR-0026, acting, getActing(), listeners, setActing(), api(), NO_REFRESH, onSessionExpired() (+8 more)

### Community 18 - "sharing/service.py"
Cohesion: 0.22
Nodes (22): datetime, utcnow(), Gone, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create(), link_status() (+14 more)

### Community 19 - "extraction/jobs.py"
Cohesion: 0.25
Nodes (8): DocumentKind, DocumentStatus, StrEnum, process_document(), Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

### Community 20 - "llm.py"
Cohesion: 0.24
Nodes (8): GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol, LLM port and the Groq adapter (ADR-003). When `LLM_PROVIDER=fake` (the default)…

### Community 21 - "visits/service.py"
Cohesion: 0.07
Nodes (73): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+65 more)

### Community 22 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 23 - "identity/router.py"
Cohesion: 0.17
Nodes (26): clear_auth_cookies(), Response, Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), delete_account(), export_data(), login(), logout() (+18 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "test_eval.py"
Cohesion: 0.13
Nodes (26): ambiguous_date(), _apply_sig(), _dosing(), extract(), _lab_results(), _lab_row(), _medication_from_line(), _parse_date() (+18 more)

### Community 26 - "audit/router.py"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 27 - "test_reminders.py"
Cohesion: 0.44
Nodes (11): at(), AsyncClient, datetime, Dose reminders by push: who gets reminded, when, once, and acting from the…, _subscribe(), test_a_due_dose_is_reminded_exactly_once(), test_devices_subscribe_privately(), test_marked_doses_lead_time_and_switching_off() (+3 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "google.py"
Cohesion: 0.17
Nodes (6): GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception, Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, Consent was revoked or the refresh token is no longer valid.

### Community 30 - "samples.py"
Cohesion: 0.31
Nodes (10): build_lab_pdf(), build_scan_png(), _diabetes(), issued(), LabReport, _lipids(), date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+2 more)

### Community 31 - "SearchPalette.jsx"
Cohesion: 0.15
Nodes (11): useSearch(), SearchContext, EASE_IN, EASE_OUT, GROUPS, JUMP_TO, SearchPalette(), useDebounced() (+3 more)

### Community 32 - "integrations/api.js"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "score.py"
Cohesion: 0.21
Nodes (16): check(), main(), Run the extraction evaluation (ADR-024). python -m app.eval # offline…, run(), to_markdown(), aggregate(), CaseResult, Check (+8 more)

### Community 34 - "confirm_extraction"
Cohesion: 0.39
Nodes (9): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+1 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.10
Nodes (20): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+12 more)

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

### Community 40 - "timedelta"
Cohesion: 0.06
Nodes (63): GoogleClient, Any, Protocol, Tokens, MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies() (+55 more)

### Community 41 - "test_google_signin.py"
Cohesion: 0.09
Nodes (34): decrypt(), _fernet(), FakeGoogleClient, GoogleIdentity, In-memory Google for demos and tests. State is per access token and per…, google_sign_in(), AsyncClient, Response (+26 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/router.py"
Cohesion: 0.18
Nodes (22): create_share(), list_shares(), open_share(), CurrentUser, DbSession, delete, get, post (+14 more)

### Community 45 - "extraction/schemas.py"
Cohesion: 0.17
Nodes (16): ConfirmCareAction, ConfirmDietNote, ConfirmIn, ConfirmLabResult, ConfirmMedication, ExtractedCareAction, ExtractedDietNote, ExtractionOut (+8 more)

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

### Community 57 - "LocalStorage"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 58 - "helpers.js"
Cohesion: 0.20
Nodes (7): here, SAMPLE, expectAccessible(), signUp(), startDemo(), here, LAB_SAMPLE

### Community 60 - "get_settings"
Cohesion: 0.13
Nodes (15): get_settings(), field_validator, Application settings, loaded from environment variables (and `.env` in…, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, share_url(), enqueue(), _get_arq_pool() (+7 more)

### Community 61 - "4. Core flows"
Cohesion: 0.25
Nodes (8): 4.1 Upload → Extract → Review → Organize → Act, 4.2.1 Evaluation, 4.2 Extraction pipeline details, 4.3 Data lifecycle, 4.4 Ask MedSpace (RAG), 4.5 Secure sharing, 4.6 Google integration, 4. Core flows

### Community 63 - "main.py"
Cohesion: 0.10
Nodes (26): configure_logging(), Logging configuration., CSRFMiddleware, BaseHTTPMiddleware, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware, SecurityHeadersMiddleware (+18 more)

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

### Community 80 - "User"
Cohesion: 0.06
Nodes (86): Forbidden, Unprocessable, CareLink, An invitation and, once accepted, a grant from `owner` to `caregiver`.…, accept(), get_circle(), invite(), preview() (+78 more)

### Community 83 - "Field.jsx"
Cohesion: 0.40
Nodes (3): Input, Select, Textarea

### Community 84 - "theme.jsx"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

### Community 115 - "test_ratelimit.py"
Cohesion: 0.22
Nodes (14): fake_clock(), _login(), AsyncClient, fixture, Rate limiting: sliding windows, honest client IPs, per-user and per-account…, settings(), test_baseline_budget_covers_every_route(), test_headers_scale_and_disable() (+6 more)

### Community 135 - "DoseStrip.jsx"
Cohesion: 0.29
Nodes (7): describe(), DoseStrip(), daySummary(), fillDays(), percent(), STATE_LABELS, TONE_CLASS

### Community 136 - "VisitBrief.jsx"
Cohesion: 0.50
Nodes (3): CHANGE_LABELS, label(), VisitBrief()

### Community 137 - "test_search.py"
Cohesion: 0.49
Nodes (9): AsyncClient, search(), test_document_text_matches_with_snippets(), test_no_matches_and_validation(), test_partial_names_find_medications(), test_prescribers_and_clinics(), test_search_is_private(), test_search_requires_auth() (+1 more)

### Community 140 - "test_timeline_dashboard.py"
Cohesion: 0.56
Nodes (8): demo(), AsyncClient, test_dashboard_shows_today(), test_deleting_account_removes_files(), test_demo_account_is_seeded_with_history(), test_export_contains_records_but_no_secrets(), test_timeline_orders_and_filters(), test_timeline_pagination_never_splits_a_day()

### Community 141 - "ReminderSettings.jsx"
Cohesion: 0.44
Nodes (7): pushKeys, usePushConfig(), usePushSettings(), useSavePushSettings(), useSendTest(), LEADS, ReminderSettings()

### Community 142 - "Conflict"
Cohesion: 0.35
Nodes (12): Conflict, set_status(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction(), latest_for_document() (+4 more)

### Community 143 - "test_sharing.py"
Cohesion: 0.53
Nodes (10): anon(), AsyncClient, setup_share(), test_cannot_share_someone_elses_records(), test_create_returns_token_once_and_stores_only_hash(), test_expired_links_are_gone(), test_public_view_returns_scoped_bundle_and_audits(), test_revoked_links_stop_working_immediately() (+2 more)

### Community 144 - "test_auth.py"
Cohesion: 0.23
Nodes (18): signup(), AsyncClient, test_audit_trail_lists_own_events(), test_demo_login_creates_isolated_demo_user(), test_health_supports_head(), test_login_is_rate_limited(), test_login_wrong_password_is_generic(), test_logout_revokes_session() (+10 more)

### Community 145 - "csrf"
Cohesion: 0.39
Nodes (16): csrf(), acting(), _invite(), _owner(), person(), AsyncClient, Care circle: invitations bound to an email, role-limited access to someone…, test_demo_accounts_help_a_family_member() (+8 more)

### Community 146 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

### Community 147 - "circle/api.js"
Cohesion: 0.25
Nodes (12): ActingBanner(), circleKeys, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite(), useRemoveLink() (+4 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "corpus.py"
Cohesion: 0.26
Nodes (13): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+5 more)

### Community 151 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 152 - "SignupIn"
Cohesion: 0.23
Nodes (7): LoginIn, ProfileUpdate, BaseModel, field_validator, SignupIn, UserOut, update_profile()

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "export.py"
Cohesion: 0.17
Nodes (7): Audit trail: `record()` is the single write path, used by every module., demo_login(), DbSession, post, Request, Response, Account data export: one JSON document with every record the user owns.…

### Community 156 - "demo/service.py"
Cohesion: 0.29
Nodes (12): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, A fictional family member who added the demo user to her care circle as a… (+4 more)

### Community 158 - "test_labs.py"
Cohesion: 0.32
Nodes (12): lab_confirm_body(), _lab_pdf_text(), AsyncClient, Lab results: copied from reports, flagged only against the printed range,…, test_demo_trends_chart_history(), test_heuristic_reads_split_line_lab_tables(), test_labs_are_private_and_deletable(), test_other_units_are_listed_but_not_charted() (+4 more)

### Community 159 - "test_assistant.py"
Cohesion: 0.38
Nodes (13): ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_lists_current_medications(), test_refuses_medical_advice() (+5 more)

### Community 160 - "deps.py"
Cohesion: 0.38
Nodes (9): _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, Shared FastAPI dependencies., The user whose records this request reads or changes. Normally the signed-in…, Unauthorized (+1 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "files.py"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 163 - "record"
Cohesion: 0.33
Nodes (7): list_for_user(), Any, AsyncSession, Request, UUID, Stage an audit row in the caller's transaction (committed with the business…, record()

### Community 164 - ".dispatch"
Cohesion: 0.60
Nodes (3): Request, Response, RequestResponseEndpoint

### Community 166 - "conftest.py"
Cohesion: 0.36
Nodes (8): reset_rate_limits(), auth_client(), _clean_tables(), client(), AsyncClient, fixture, Test harness: real Postgres (pgvector), fakes for every external service., _schema()

### Community 167 - "ratelimit.py"
Cohesion: 0.11
Nodes (20): caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore, Any (+12 more)

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

### Community 173 - "search"
Cohesion: 0.50
Nodes (4): CurrentUser, DbSession, get, search()

### Community 175 - "install.js"
Cohesion: 0.33
Nodes (3): emit(), listeners, promptInstall()

### Community 178 - "errors.py"
Cohesion: 0.12
Nodes (15): AppError, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception, FastAPI, Request (+7 more)

### Community 181 - "_diet_notes"
Cohesion: 0.33
Nodes (6): diet_category(), _diet_notes(), Split an advice line like "Diet: low salt. Avoid sugary drinks." into separate…, parametrize, test_advice_lines_split_into_separate_notes(), test_diet_categories()

## Knowledge Gaps
- **235 isolated node(s):** `WorkerSettings`, `medspace-api`, `here`, `SAMPLE`, `here` (+230 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `deps.py`, `reminders/service.py`, `db.py`, `records/service.py`, `assistant/service.py`, `integrations/service.py`, `timedelta`, `test_google_signin.py`, `Conflict`, `extraction/service.py`, `identity/service.py`, `sharing/service.py`, `extraction/jobs.py`, `visits/service.py`, `SignupIn`, `export.py`, `demo/service.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `reminders/service.py`, `db.py`, `assistant/service.py`, `integrations/service.py`, `documents/service.py`, `integrations/router.py`, `test_timeline_dashboard.py`, `identity/service.py`, `extraction/service.py`, `sharing/service.py`, `llm.py`, `documents/router.py`, `identity/router.py`, `export.py`, `demo/service.py`, `google.py`, `deps.py`, `.dispatch`, `ratelimit.py`, `test_google_signin.py`, `errors.py`, `main.py`, `User`, `test_ratelimit.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_diet_notes.py`, `conftest.py`, `timedelta`, `test_google_signin.py`, `test_timeline_dashboard.py`, `test_sharing.py`, `test_auth.py`, `test_ratelimit.py`, `test_doses.py`, `test_reminders.py`, `test_labs.py`, `test_assistant.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 46 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `lab_report()`) actually correct?**
  _`timedelta` has 46 INFERRED edges - model-reasoned connections that need verification._
- **What connects `WorkerSettings`, `medspace-api`, `here` to the rest of the system?**
  _235 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `reminders/service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.057813911472448055 - nodes in this community are weakly interconnected._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.140534262485482 - nodes in this community are weakly interconnected._