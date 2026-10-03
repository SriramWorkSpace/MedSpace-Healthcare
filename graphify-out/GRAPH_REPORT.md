# Graph Report - MedSpace  (2026-10-03)

## Corpus Check
- 310 files · ~127,547 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2452 nodes · 6100 edges · 182 communities (146 shown, 36 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `68bcfc5a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_documents_flow.py
- User
- db.py
- dependencies
- devDependencies
- Medication
- router.jsx
- utcnow
- integrations/service.py
- Architecture Decision Records
- doses/router.py
- integrations/router.py
- documents/api.js
- TrendChart.jsx
- identity/router.py
- ExtractionPayload
- FeatureBento.jsx
- auth.jsx
- circle/service.py
- assistant/service.py
- llm.py
- visits/service.py
- documents/router.py
- ratelimit.py
- mapping.js
- heuristic.py
- audit/router.py
- test_labs.py
- EasterEggs.jsx
- labs.py
- reminders/service.py
- SearchPalette.jsx
- integrations/api.js
- test_eval.py
- extraction/router.py
- MedSpace Build Plan
- records/service.py
- CLAUDE.md
- AppNav.jsx
- MedSpace Architecture
- supply/service.py
- csrf
- MedSpace
- sharing/router.py
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
- circle/router.py
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
- test_assistant.py
- corpus.py
- test_diet_notes.py
- timedelta
- test_doses.py
- circle/api.js
- push.js
- MedicationHistory.jsx
- extraction/service.py
- record
- .dispatch
- doses/api.js
- embeddings.py
- seed
- acting.js
- env.py
- queue.py
- deps.py
- offline.js
- demo/service.py
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
- documents/service.py
- sw-template.js
- worker.py

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
- `check_second_factor()` --uses--> `Unauthorized`  [INFERRED]
  backend/app/modules/identity/security.py → backend/app/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (182 total, 36 thin omitted)

### Community 0 - "test_documents_flow.py"
Cohesion: 0.26
Nodes (20): build_pdf(), build_scan_png(), issued(), date, A 'photo' of the prescription: rasterized, so it has no text layer., Scenario, drain(), Wait for all inline jobs (used by tests). (+12 more)

### Community 1 - "User"
Cohesion: 0.17
Nodes (28): AppError, Conflict, Forbidden, Exception, User, begin_setup(), change_password(), check_second_factor() (+20 more)

### Community 2 - "db.py"
Cohesion: 0.11
Nodes (38): Base, IdMixin, Database engine, session factory and declarative base., TimestampMixin, Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatThread, AuditLog, Append-only trail of security-relevant actions. Never updated or deleted by app… (+30 more)

### Community 3 - "dependencies"
Cohesion: 0.07
Nodes (27): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+19 more)

### Community 4 - "devDependencies"
Cohesion: 0.08
Nodes (25): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, devDependencies, @axe-core/playwright, eslint, @eslint/js (+17 more)

### Community 5 - "Medication"
Cohesion: 0.11
Nodes (25): _record_line(), Medication, doses_on(), medication_status(), date, Scheduled HH:MM times for one medicine on one day, by its schedule and course…, Scheduled doses for a calendar day (as-needed and stopped meds excluded),…, times_on() (+17 more)

### Community 6 - "router.jsx"
Cohesion: 0.25
Nodes (4): AppLayout(), AuthLayout(), MarketingLayout(), RouteError()

### Community 7 - "utcnow"
Cohesion: 0.23
Nodes (21): datetime, utcnow(), A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create(), link_status(), list_links() (+13 more)

### Community 8 - "integrations/service.py"
Cohesion: 0.07
Nodes (50): decrypt(), encrypt(), FakeGoogleClient, get_google(), GoogleAPIError, GoogleAuthError, HttpGoogleClient, Exception (+42 more)

### Community 9 - "Architecture Decision Records"
Cohesion: 0.07
Nodes (30): ADR-001: Modular monolith with two processes, ADR-002: pgvector instead of FAISS, ADR-003: Groq as the LLM provider, behind a provider interface, ADR-004: Local embeddings with fastembed, ADR-005: Calendar for recurring reminders, Tasks for one-off actions, ADR-006: Deterministic frequency normalization, ADR-007: Durable job queue with ARQ + inline fallback, ADR-008: Own authentication; Google OAuth only for integrations (+22 more)

### Community 10 - "doses/router.py"
Cohesion: 0.11
Nodes (37): adherence(), clear_dose(), log_dose(), medication_adherence(), CurrentUser, date, DbSession, delete (+29 more)

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
Nodes (56): RateLimited, decode_purpose_token(), clear_auth_cookies(), Response, change_password(), _current_session(), delete_account(), end_other_sessions() (+48 more)

### Community 15 - "ExtractionPayload"
Cohesion: 0.12
Nodes (23): _nullable(), Any, Prompts and the strict JSON schema for document extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload, _coerce() (+15 more)

### Community 16 - "FeatureBento.jsx"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "auth.jsx"
Cohesion: 0.21
Nodes (13): getActing(), setActing(), api(), NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler() (+5 more)

### Community 18 - "circle/service.py"
Cohesion: 0.24
Nodes (19): Gone, Unprocessable, sha256_hex(), CareLink, An invitation and, once accepted, a grant from `owner` to `caregiver`.…, accept(), _by_token(), invite() (+11 more)

### Community 19 - "assistant/service.py"
Cohesion: 0.09
Nodes (49): ChatMessage, DocumentChunk, A page-aware slice of a document, embedded for semantic search and indexed for…, ask(), AskIn, create_thread(), delete_thread(), get_thread() (+41 more)

### Community 20 - "llm.py"
Cohesion: 0.23
Nodes (9): get_llm(), GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol (+1 more)

### Community 21 - "visits/service.py"
Cohesion: 0.07
Nodes (69): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+61 more)

### Community 22 - "documents/router.py"
Cohesion: 0.20
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 23 - "ratelimit.py"
Cohesion: 0.11
Nodes (21): caller_key(), check(), client_ip(), Decision, _estimate(), get_store(), MemoryStore, Any (+13 more)

### Community 24 - "mapping.js"
Cohesion: 0.22
Nodes (16): blank(), CARE_KINDS, DIET_CATEGORIES, emptyCareAction(), emptyDietNote(), emptyLabResult(), emptyMedication(), formToConfirm() (+8 more)

### Community 25 - "heuristic.py"
Cohesion: 0.09
Nodes (39): ambiguous_date(), _apply_sig(), _dosing(), extract(), _lab_results(), _lab_row(), _medication_from_line(), _parse_date() (+31 more)

### Community 26 - "audit/router.py"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 27 - "test_labs.py"
Cohesion: 0.22
Nodes (17): build_lab_pdf(), _diabetes(), LabReport, _lipids(), Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every…, lab_confirm_body(), _lab_pdf_text(), AsyncClient (+9 more)

### Community 28 - "EasterEggs.jsx"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "labs.py"
Cohesion: 0.15
Nodes (18): analyte_key(), flag_against(), parse_range(), parse_value(), printed_flag(), Deterministic handling of lab results (ADR-020). Values and reference ranges…, H' / 'High' / 'L*' printed next to a value on the report., The printed range wins when it parses (it stays correct if the value is edited… (+10 more)

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

### Community 34 - "extraction/router.py"
Cohesion: 0.40
Nodes (9): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+1 more)

### Community 35 - "MedSpace Build Plan"
Cohesion: 0.10
Nodes (21): Change log, MedSpace Build Plan, Phase 0: Foundations, Phase 10: Lab results and trends, Phase 11: Dose tracking and history, Phase 12: Visit prep, Phase 13: Medication supply and refills, Phase 14: Extraction evaluation (+13 more)

### Community 36 - "records/service.py"
Cohesion: 0.12
Nodes (49): NotFound, build_export(), AsyncSession, CareActionOut, CareActionUpdate, DietNoteOut, DietNotesOut, LabPoint (+41 more)

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
Nodes (32): MedicationSupply, One count per medicine (ADR-023). Estimates are derived from this count, the…, clear_supply(), list_supplies(), CurrentUser, DbSession, delete, get (+24 more)

### Community 41 - "csrf"
Cohesion: 0.05
Nodes (104): reset_rate_limits(), code_at(), current_step(), _key(), new_recovery_codes(), new_secret(), normalize_recovery_code(), provisioning_uri() (+96 more)

### Community 42 - "MedSpace"
Cohesion: 0.25
Nodes (8): Architecture at a glance, Engineering highlights, Features, License, MedSpace, Project structure, Roadmap, Tech stack

### Community 43 - "sharing/router.py"
Cohesion: 0.18
Nodes (22): create_share(), list_shares(), open_share(), CurrentUser, DbSession, delete, get, post (+14 more)

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

### Community 63 - "get_settings"
Cohesion: 0.10
Nodes (29): get_settings(), install_error_handlers(), FastAPI, Domain errors rendered as RFC 9457 `application/problem+json`., ServiceUnavailable, configure_logging(), Logging configuration., CSRFMiddleware (+21 more)

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

### Community 80 - "circle/router.py"
Cohesion: 0.16
Nodes (27): accept(), get_circle(), invite(), preview(), CurrentUser, DbSession, delete, get (+19 more)

### Community 83 - "Field.jsx"
Cohesion: 0.29
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

### Community 140 - "SecuritySettings.jsx"
Cohesion: 0.19
Nodes (20): ADR-0029, securityKeys, useChangePassword(), useDisableMfa(), useEnableMfa(), useEndOtherSessions(), useEndSession(), useNewRecoveryCodes() (+12 more)

### Community 141 - "ReminderSettings.jsx"
Cohesion: 0.44
Nodes (7): pushKeys, usePushConfig(), usePushSettings(), useSavePushSettings(), useSendTest(), LEADS, ReminderSettings()

### Community 142 - "test_assistant.py"
Cohesion: 0.33
Nodes (14): chunk_pages(), Split page text into overlapping chunks on line boundaries; chunks never span…, ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_chunking_respects_pages_and_size() (+6 more)

### Community 143 - "corpus.py"
Cohesion: 0.24
Nodes (14): build(), Case, _fmt(), Gold, GoldLab, GoldMed, lab_report(), _med_line() (+6 more)

### Community 144 - "test_diet_notes.py"
Cohesion: 0.21
Nodes (14): diet_category(), _diet_notes(), Split an advice line like "Diet: low salt. Avoid sugary drinks." into separate…, AsyncClient, parametrize, Diet notes from your care team: extracted, reviewed, confirmed, never invented., test_advice_lines_split_into_separate_notes(), test_ask_medspace_answers_diet_questions_from_notes() (+6 more)

### Community 145 - "timedelta"
Cohesion: 0.08
Nodes (33): GoogleClient, Any, Protocol, Tokens, _at(), estimate(), date, datetime (+25 more)

### Community 146 - "test_doses.py"
Cohesion: 0.41
Nodes (12): log(), _medicine(), AsyncClient, Response, Dose tracking: taken/skipped logs per scheduled dose, history that never…, Confirm a prescription with one twice-daily medicine that started `days_ago`…, test_dose_logs_are_private(), test_history_counts_without_assuming_misses() (+4 more)

### Community 147 - "circle/api.js"
Cohesion: 0.25
Nodes (12): ActingBanner(), circleKeys, useAccept(), useActing(), useCircle(), useCircleMutation(), useInvite(), useRemoveLink() (+4 more)

### Community 148 - "push.js"
Cohesion: 0.39
Nodes (6): currentSubscription(), ADR-0028, keyToBytes(), subscribePush(), swRegistration(), unsubscribePush()

### Community 149 - "MedicationHistory.jsx"
Cohesion: 0.20
Nodes (3): DOT, RANGES, WEEKDAYS

### Community 150 - "extraction/service.py"
Cohesion: 0.16
Nodes (20): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, set_status(), process_document(), Background job: process an uploaded document end to end., Extraction, ExtractionStatus, StrEnum, One AI reading of a document. Versioned; only a confirmed version becomes… (+12 more)

### Community 151 - "record"
Cohesion: 0.33
Nodes (7): list_for_user(), Any, AsyncSession, Request, UUID, Stage an audit row in the caller's transaction (committed with the business…, record()

### Community 152 - ".dispatch"
Cohesion: 0.60
Nodes (3): Request, Response, RequestResponseEndpoint

### Community 153 - "doses/api.js"
Cohesion: 0.38
Nodes (4): doseKeys, patchDashboard(), patchHistory(), useSetDose()

### Community 155 - "embeddings.py"
Cohesion: 0.15
Nodes (8): Embedder, FastEmbedEmbedder, get_embedder(), HashEmbedder, Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher…, Feature-hashing embedder (words + character trigrams). Deterministic,…, BAAI/bge-small-en-v1.5 via ONNX on CPU. The model downloads once (~130 MB) and…

### Community 156 - "seed"
Cohesion: 0.24
Nodes (14): create_demo_account(), _ingest(), _page_texts(), AsyncSession, date, A fictional family member who added the demo user to her care circle as a…, Seed demo records for a new simulated account; never let seeding block a sign-…, seed() (+6 more)

### Community 157 - "acting.js"
Cohesion: 0.33
Nodes (3): ADR-0026, acting, listeners

### Community 158 - "env.py"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 159 - "queue.py"
Cohesion: 0.50
Nodes (4): enqueue(), _get_arq_pool(), Any, Background job dispatch. `QUEUE_MODE=arq`: jobs go to Redis and run in the…

### Community 160 - "deps.py"
Cohesion: 0.33
Nodes (11): _authenticated(), _extract_token(), get_current_user(), get_optional_user(), AsyncSession, Request, UUID, Shared FastAPI dependencies. (+3 more)

### Community 161 - "offline.js"
Cohesion: 0.24
Nodes (13): clearOfflineCopy(), currentUserId(), emit(), isOfflineEnabled(), ADR-0025, listeners, MAX_AGE_MS, PERSISTED (+5 more)

### Community 162 - "demo/service.py"
Cohesion: 0.19
Nodes (8): purge_expired_demo_accounts(), Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-…, Document, DocumentKind, DocumentStatus, StrEnum, Account data export: one JSON document with every record the user owns.…, Read models over confirmed records: the health timeline and the dashboard. The…

### Community 163 - "demo/router.py"
Cohesion: 0.22
Nodes (5): demo_login(), DbSession, post, Request, Response

### Community 164 - "_problem"
Cohesion: 0.50
Nodes (3): _problem(), Any, Request

### Community 166 - "identity/service.py"
Cohesion: 0.09
Nodes (37): Application settings, loaded from environment variables (and `.env` in…, UUID, Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., uuid7(), Unauthorized, create_access_token(), create_purpose_token(), decode_access_claims() (+29 more)

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
Cohesion: 0.14
Nodes (21): PayloadTooLarge, UnsupportedMedia, create_document(), delete_document(), get_document(), get_document_by_id(), list_documents(), page_preview_png() (+13 more)

### Community 186 - "worker.py"
Cohesion: 0.24
Nodes (6): purge_demo_accounts(), purge_share_links(), ARQ worker entrypoint: `arq app.worker.WorkerSettings`., send_reminders(), WorkerSettings, session()

## Knowledge Gaps
- **239 isolated node(s):** `OWNER_ONLY`, `APP_LINKS`, `Faq`, `EASE`, `DAYS` (+234 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `deps.py`, `db.py`, `demo/service.py`, `records/service.py`, `identity/service.py`, `utcnow`, `integrations/service.py`, `supply/service.py`, `doses/router.py`, `csrf`, `circle/router.py`, `timedelta`, `circle/service.py`, `assistant/service.py`, `visits/service.py`, `extraction/service.py`, `seed`, `reminders/service.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `db.py`, `utcnow`, `integrations/service.py`, `integrations/router.py`, `identity/router.py`, `ExtractionPayload`, `circle/service.py`, `assistant/service.py`, `llm.py`, `documents/router.py`, `ratelimit.py`, `.dispatch`, `extraction/service.py`, `embeddings.py`, `reminders/service.py`, `queue.py`, `env.py`, `demo/service.py`, `demo/router.py`, `identity/service.py`, `documents/service.py`, `test_timeline_dashboard.py`, `worker.py`, `Settings`, `circle/router.py`, `test_ratelimit.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `csrf()` connect `csrf` to `test_documents_flow.py`, `integrations/service.py`, `test_assistant.py`, `test_diet_notes.py`, `timedelta`, `test_doses.py`, `test_ratelimit.py`, `test_timeline_dashboard.py`, `test_labs.py`, `reminders/service.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 47 inferred relationships involving `timedelta` (e.g. with `create_access_token()` and `create_purpose_token()`) actually correct?**
  _`timedelta` has 47 INFERRED edges - model-reasoned connections that need verification._
- **What connects `OWNER_ONLY`, `APP_LINKS`, `Faq` to the rest of the system?**
  _239 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11248185776487664 - nodes in this community are weakly interconnected._
- **Should `dependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._