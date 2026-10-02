# Graph Report - MedSpace  (2026-10-02)

## Corpus Check
- 92 files · ~65,489 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1425 nodes · 2900 edges · 126 communities (104 shown, 22 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.9)
- Token cost: 104,142 input · 0 output

## Community Hubs (Navigation)
- Backend Test Harness & Samples
- ORM Models & Base
- Secure Sharing
- Frontend Runtime Deps
- Frontend Dev & Test Tooling
- Timeline & Dashboard API
- SPA Router & Layouts
- RAG Assistant Service
- Google Sync Service
- App Factory & Embeddings
- Documents API Router
- Google OAuth Router
- Documents Client API
- Assistant API Router
- Identity & Password Security
- Extraction Pipeline Service
- Landing Sections
- API Client & Auth State
- Schemas & Rate-Limited Routes
- Document Intake Service
- Frequency Normalizer
- Google HTTP Client
- Domain Errors
- Auth Cookies & Sessions
- Review Form Mapping
- Google Client Port
- Confirmation Schemas
- Calendar Event Builders
- Easter Eggs
- Settings & Config
- Current-User Dependency
- Extraction Pipeline (docs)
- Integrations Client API
- Extraction Lifecycle
- Job Registry
- Assistant Tests
- Groq LLM Adapter
- Backend Conventions (docs)
- App Navigation
- CI Workflow
- HTTP Middleware
- Google Simulation
- Modular Monolith Rules (docs)
- RAG Design (docs)
- Audit Router
- Audit Service
- Storage & Deployment (docs)
- Auth Forms
- Records Client API
- Rate Limiter
- Model Registry
- Demo Seeding
- File Inspection
- Docs & Graph Workflow
- Format Helpers
- Settings Page
- Profile Router
- Local Storage Adapter
- E2E Core Flows
- Ask Page
- Config
- Heuristic
- Models
- Storage
- Storage
- Architecture
- Widgets
- Api
- Prompts
- Dialog
- Puns
- Api
- Heromorph
- Embeddings
- Todayschedule
- Workflow
- Audit
- Medications
- Sharing
- Timeline
- Router
- Env
- Pageskeleton
- Field
- Theme
- Sharedview
- Decisions
- Reportbody
- Landing
- Queue
- Marketingnav
- Processingstate
- Documents
- Misc
- Pyproject

## God Nodes (most connected - your core abstractions)
1. `get_settings()` - 38 edges
2. `Base` - 20 edges
3. `User` - 18 edges
4. `Document` - 18 edges
5. `record()` - 17 edges
6. `FakeGoogleClient` - 17 edges
7. `utcnow()` - 16 edges
8. `issue_session()` - 16 edges
9. `csrf()` - 16 edges
10. `HttpGoogleClient` - 16 edges

## Surprising Connections (you probably didn't know these)
- `CI Backend job (ruff + pytest on pgvector Postgres)` --semantically_similar_to--> `postgres service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `Two-path document extraction (text vs vision)` --semantically_similar_to--> `Extraction pipeline (classify, extract, validate, normalize, draft)`  [INFERRED] [semantically similar]
  README.md → docs/architecture.md
- `Phase 0: Foundations` --references--> `s3 service (SeaweedFS)`  [AMBIGUOUS]
  docs/plan.md → docker-compose.yml
- `Upload -> Extract -> Review -> Organize -> Act` --semantically_similar_to--> `Upload/process document sequence flow`  [INFERRED] [semantically similar]
  README.md → docs/architecture.md
- `CI E2E job (Playwright + axe, fake providers)` --references--> `FakeGoogleClient (in-memory)`  [INFERRED]
  .github/workflows/ci.yml → docs/architecture.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ports with production and offline fake adapters** — docs_architecture_ports_and_adapters, docs_architecture_llmprovider, docs_architecture_embedder, docs_architecture_objectstorage, docs_architecture_googleclient, docs_architecture_fakellm, docs_architecture_hashembedder, docs_architecture_localstorage, docs_architecture_fakegoogleclient [EXTRACTED 1.00]
- **Upload -> extract -> review -> confirm pipeline** — docs_architecture_module_documents, docs_architecture_module_extraction, docs_architecture_module_records, docs_architecture_extraction_pipeline, docs_architecture_data_lifecycle, docs_architecture_schedule, docs_architecture_queue_mode [EXTRACTED 1.00]
- **Local Docker Compose stack** — docker_compose_postgres, docker_compose_redis, docker_compose_s3, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (126 total, 22 thin omitted)

### Community 0 - "Backend Test Harness & Samples"
Cohesion: 0.07
Nodes (69): reset_rate_limits(), build_lab_pdf(), build_pdf(), build_scan_png(), issued(), LabReport, date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+61 more)

### Community 1 - "ORM Models & Base"
Cohesion: 0.09
Nodes (61): Base, IdMixin, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin, utcnow(), uuid7() (+53 more)

### Community 2 - "Secure Sharing"
Cohesion: 0.10
Nodes (48): Base, IdMixin, TimestampMixin, A scoped, expiring, revocable read-only link (ADR-010). Only the token's hash…, ShareLink, ShareLinkItem, create_share(), list_shares() (+40 more)

### Community 3 - "Frontend Runtime Deps"
Cohesion: 0.04
Nodes (44): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+36 more)

### Community 4 - "Frontend Dev & Test Tooling"
Cohesion: 0.06
Nodes (35): @axe-core/playwright, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, @axe-core/playwright, eslint (+27 more)

### Community 5 - "Timeline & Dashboard API"
Cohesion: 0.11
Nodes (28): get_dashboard(), get_timeline(), CurrentUser, date, DbSession, get, AsNeededOut, DashboardOut (+20 more)

### Community 6 - "SPA Router & Layouts"
Cohesion: 0.08
Nodes (6): AppLayout(), AuthLayout(), MarketingLayout(), Providers(), RouteError(), router

### Community 7 - "RAG Assistant Service"
Cohesion: 0.13
Nodes (26): answer_stream(), _best_snippet(), build_prompt(), chunk_pages(), _clock(), compose_offline(), create_thread(), _day() (+18 more)

### Community 8 - "Google Sync Service"
Cohesion: 0.22
Nodes (28): get_google(), access_token(), appointment_event(), _clock(), _delete_remote(), disconnect(), get_connection(), _links() (+20 more)

### Community 9 - "App Factory & Embeddings"
Cohesion: 0.11
Nodes (16): create_app(), lifespan(), FastAPI application factory., Embedder, FastEmbedEmbedder, get_embedder(), Protocol, Embedding port (ADR-004): local fastembed in production, a deterministic hasher… (+8 more)

### Community 10 - "Documents API Router"
Cohesion: 0.19
Nodes (23): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+15 more)

### Community 11 - "Google OAuth Router"
Cohesion: 0.17
Nodes (23): GoogleAPIError, pkce_pair(), Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory…, callback(), connect(), disconnect(), preview(), pull() (+15 more)

### Community 12 - "Documents Client API"
Cohesion: 0.10
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 13 - "Assistant API Router"
Cohesion: 0.17
Nodes (21): ask(), AskIn, create_thread(), delete_thread(), get_thread(), list_threads(), MessageOut, BaseModel (+13 more)

### Community 14 - "Identity & Password Security"
Cohesion: 0.22
Nodes (19): hash_password(), needs_rehash(), sha256_hex(), verify_password(), User, authenticate(), create_user(), delete_user() (+11 more)

### Community 15 - "Extraction Pipeline Service"
Cohesion: 0.17
Nodes (19): ExtractionStatus, StrEnum, ExtractionPayload, _coerce(), extract_document(), _extract_text(), _extract_vision(), ExtractionFailed (+11 more)

### Community 16 - "Landing Sections"
Cohesion: 0.11
Nodes (6): FAQ, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 17 - "API Client & Auth State"
Cohesion: 0.17
Nodes (13): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+5 more)

### Community 18 - "Schemas & Rate-Limited Routes"
Cohesion: 0.19
Nodes (8): Any, rate_limit(), LoginIn, ProfileUpdate, BaseModel, field_validator, SignupIn, UserOut

### Community 19 - "Document Intake Service"
Cohesion: 0.26
Nodes (18): Document, create_document(), delete_document(), get_document(), get_document_by_id(), list_documents(), page_preview_png(), purge_user_files() (+10 more)

### Community 20 - "Frequency Normalizer"
Cohesion: 0.20
Nodes (16): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+8 more)

### Community 21 - "Google HTTP Client"
Cohesion: 0.16
Nodes (4): GoogleAuthError, HttpGoogleClient, Consent was revoked or the refresh token is no longer valid., Exception

### Community 22 - "Domain Errors"
Cohesion: 0.18
Nodes (16): AppError, Forbidden, Gone, install_error_handlers(), PayloadTooLarge, _problem(), Any, Exception (+8 more)

### Community 23 - "Auth Cookies & Sessions"
Cohesion: 0.24
Nodes (17): new_opaque_token(), clear_auth_cookies(), Response, Auth cookie helpers shared by the identity and demo routers., Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in…, set_auth_cookies(), delete_account(), login() (+9 more)

### Community 24 - "Review Form Mapping"
Cohesion: 0.25
Nodes (13): blank(), CARE_KINDS, emptyCareAction(), emptyMedication(), formToConfirm(), num(), payloadToForm(), reviewSchema (+5 more)

### Community 25 - "Google Client Port"
Cohesion: 0.13
Nodes (4): Any, GoogleClient, Protocol, Tokens

### Community 26 - "Confirmation Schemas"
Cohesion: 0.22
Nodes (14): ConfirmCareAction, ConfirmIn, ConfirmMedication, ExtractedCareAction, ExtractedMedication, ExtractionOut, FollowUp, Prescriber (+6 more)

### Community 27 - "Calendar Event Builders"
Cohesion: 0.28
Nodes (15): dose_event(), Medication, _rrule(), bucket_for(), connect(), first_prescription(), AsyncClient, Google Calendar/Tasks sync against the in-memory simulation… (+7 more)

### Community 28 - "Easter Eggs"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 29 - "Settings & Config"
Cohesion: 0.24
Nodes (10): get_settings(), Application settings, loaded from environment variables (and `.env` in…, configure_logging(), Logging configuration., HTTP middleware: security headers, CSRF double-submit check, request logging., LLM port and the Groq adapter (ADR-003). When `LLM_PROVIDER=fake` (the default)…, enqueue(), _get_arq_pool() (+2 more)

### Community 30 - "Current-User Dependency"
Cohesion: 0.23
Nodes (12): _extract_token(), get_current_user(), AsyncSession, Request, Shared FastAPI dependencies., create_access_token(), decode_access_token(), decrypt() (+4 more)

### Community 31 - "Extraction Pipeline (docs)"
Cohesion: 0.24
Nodes (14): Document/extraction data lifecycle (draft -> confirmed), Extraction pipeline (classify, extract, validate, normalize, draft), FakeLLM (deterministic, regex-based), GroqProvider (gpt-oss-120b text, qwen3.8-27b vision), LLMProvider port, extraction module, records module, PrescriptionExtraction schema (per-field confidence + source_page) (+6 more)

### Community 32 - "Integrations Client API"
Cohesion: 0.29
Nodes (10): connectGoogle(), googleKeys, useDisconnectGoogle(), useGoogleMutation(), useGooglePreview(), useGoogleStatus(), usePullTasks(), useSyncPrescription() (+2 more)

### Community 33 - "Extraction Lifecycle"
Cohesion: 0.32
Nodes (13): Conflict, set_status(), process_document(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction() (+5 more)

### Community 34 - "Job Registry"
Cohesion: 0.27
Nodes (10): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post (+2 more)

### Community 35 - "Assistant Tests"
Cohesion: 0.41
Nodes (12): classify(), ask(), new_thread(), AsyncClient, Consume the SSE stream and return {sources, answer, done, events}., test_answers_are_grounded_and_cited(), test_document_text_is_searchable(), test_intent_classification() (+4 more)

### Community 36 - "Groq LLM Adapter"
Cohesion: 0.26
Nodes (7): GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol

### Community 37 - "Backend Conventions (docs)"
Cohesion: 0.21
Nodes (13): AppError subclasses rendered as problem+json, user_id scoping on every query ((id, user_id) loads, 404 for foreign IDs), CSRF double-submit (ms_csrf cookie + X-CSRF-Token), audit module (append-only, record()), identity module, sharing module, Rotating refresh tokens with family reuse detection, Secure sharing flow (hashed tokens, expiry, view limits) (+5 more)

### Community 38 - "App Navigation"
Cohesion: 0.22
Nodes (6): APP_LINKS, MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 39 - "CI Workflow"
Cohesion: 0.26
Nodes (12): CI Backend job (ruff + pytest on pgvector Postgres), CI Docker images build job, CI E2E job (Playwright + axe, fake providers), CI Frontend job (lint + Vitest + build), LocalStorage (filesystem), documents module, ObjectStorage port, Ports and adapters (offline fakes) (+4 more)

### Community 40 - "HTTP Middleware"
Cohesion: 0.26
Nodes (9): CSRFMiddleware, Request, Response, Double-submit cookie check for cookie-authenticated unsafe requests. Requests…, RequestLogMiddleware, SecurityHeadersMiddleware, constant_time_equals(), BaseHTTPMiddleware (+1 more)

### Community 42 - "Modular Monolith Rules (docs)"
Cohesion: 0.21
Nodes (12): Cross-module import rule (service.py/schemas.py only), Thin routers convention, Modular monolith (API + worker processes), demo module (synthetic seeding), timeline module (read model), Upload/process document sequence flow, ADR-001: Modular monolith with two processes, ADR-013: Synthetic data only, explicit non-goals (+4 more)

### Community 43 - "RAG Design (docs)"
Cohesion: 0.27
Nodes (12): Ask MedSpace hybrid RAG (pgvector + full-text), document_chunks (vector(384) HNSW + tsvector GIN), Embedder port, FastEmbedEmbedder (bge-small-en-v1.5, 384-d), HashEmbedder (hashing trick), assistant module, RAG guardrails (cite sources, no diagnosis/dose changes, SQL user scoping), Reciprocal Rank Fusion (top 6 chunks) (+4 more)

### Community 44 - "Audit Router"
Cohesion: 0.27
Nodes (9): get_session(), AsyncSession, list_audit(), AsyncSession, CurrentUser, get, AuditLogOut, AuditPage (+1 more)

### Community 45 - "Audit Service"
Cohesion: 0.25
Nodes (10): client_ip(), Request, list_for_user(), Any, AsyncSession, Request, UUID, Audit trail: `record()` is the single write path, used by every module. (+2 more)

### Community 46 - "Storage & Deployment (docs)"
Cohesion: 0.24
Nodes (11): s3 service (SeaweedFS), web service (Vite dev), S3Storage (SeaweedFS dev, R2/S3 prod), ADR-014: Same-origin API for first-party auth cookies, ADR-016: SeaweedFS for local S3; storage failures surface as 503, /api rewrite (Vercel rewrites / Netlify _redirects), Deployment checklist (/api/ready, demo, HSTS, X-Frame-Options), Cloudflare R2 private bucket (+3 more)

### Community 47 - "Auth Forms"
Cohesion: 0.24
Nodes (6): LoginForm(), loginSchema, SignupForm(), signupSchema, useAuthMutation(), useDemoLogin()

### Community 48 - "Records Client API"
Cohesion: 0.22
Nodes (4): recordKeys, useInvalidateRecords(), useUpdateCareAction(), useUpdateMedication()

### Community 49 - "Rate Limiter"
Cohesion: 0.24
Nodes (4): _get_store(), _MemoryStore, Fixed-window rate limiting. Uses Redis when `QUEUE_MODE=arq` (multi-process…, _RedisStore

### Community 50 - "Model Registry"
Cohesion: 0.36
Nodes (8): Import every module's ORM models so `Base.metadata` is complete (Alembic,…, ChatMessage, ChatThread, DocumentChunk, Base, IdMixin, TimestampMixin, A page-aware slice of a document, embedded for semantic search and indexed for…

### Community 51 - "Demo Seeding"
Cohesion: 0.40
Nodes (9): create_demo_account(), _ingest(), _page_texts(), purge_expired_demo_accounts(), AsyncSession, date, User, Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-… (+1 more)

### Community 52 - "File Inspection"
Cohesion: 0.24
Nodes (9): inspect(), Inspection, Exception, File inspection: type sniffing by magic bytes, PDF text extraction and page…, Identify the real file type from its leading bytes; never trust the client's…, PNG bytes per page for the vision model. Images are passed through (re-encoded…, render_pages_png(), sniff_mime() (+1 more)

### Community 53 - "Docs & Graph Workflow"
Cohesion: 0.33
Nodes (10): Docs discipline (tick plan, add ADR, graphify update), graphify knowledge graph workflow, api service (alembic + uvicorn), x-backend-env shared env anchor, postgres service (pgvector/pgvector:pg17), redis service, worker service (arq WorkerSettings), QUEUE_MODE (inline | arq) (+2 more)

### Community 54 - "Format Helpers"
Cohesion: 0.36
Nodes (8): firstName(), formatBytes(), formatClock(), formatDate(), formatRelativeDay(), greeting(), timeAgo(), toDate()

### Community 56 - "Profile Router"
Cohesion: 0.22
Nodes (9): me(), BaseModel, CurrentUser, get, patch, Who am I, without a 401 for anonymous visitors (the SPA calls this on boot)., session_state(), SessionState (+1 more)

### Community 57 - "Local Storage Adapter"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 58 - "E2E Core Flows"
Cohesion: 0.36
Nodes (5): here, SAMPLE, expectAccessible(), signUp(), startDemo()

### Community 60 - "Config"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 61 - "Heuristic"
Cohesion: 0.32
Nodes (7): extract(), _medication_from_line(), _parse_date(), date, Offline, rule-based extractor used when no LLM is configured (CI, demo, keyless…, ExtractedMedication, ExtractionPayload

### Community 62 - "Models"
Cohesion: 0.36
Nodes (7): OAuthConnection, Base, IdMixin, TimestampMixin, A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)., Maps a MedSpace entity (one dose slot, an appointment, a to-do) to its remote…, SyncLink

### Community 63 - "Storage"
Cohesion: 0.25
Nodes (3): ObjectStorage, Protocol, Object storage port with filesystem and S3-compatible adapters.

### Community 65 - "Architecture"
Cohesion: 0.39
Nodes (8): FakeGoogleClient (in-memory), Google integration (Calendar RRULE events, Tasks list, Fernet tokens), GoogleClient port, HttpGoogleClient (Calendar v3 / Tasks v1), integrations module, sync_links table (idempotent sync mapping), ADR-005: Calendar for recurring reminders, Tasks for one-off actions, Phase 6: Google Calendar + Tasks

### Community 68 - "Prompts"
Cohesion: 0.29
Nodes (6): _nullable(), Any, Prompts and the strict JSON schema for prescription extraction., repair_prompt(), text_user_prompt(), vision_user_prompt()

### Community 70 - "Puns"
Cohesion: 0.29
Nodes (5): EMPTY_QUIPS, LOADING_PUNS, MARQUEE_PUNS, NOT_FOUND_LINES, PROCESSING_PUNS

### Community 72 - "Heromorph"
Cohesion: 0.33
Nodes (6): DURATIONS, EASE, HeroMorph(), PHASES, RX, usePhase()

### Community 74 - "Todayschedule"
Cohesion: 0.53
Nodes (5): nowHHMM(), slotFor(), SLOTS, TodaySchedule(), useTaken()

### Community 79 - "Timeline"
Cohesion: 0.40
Nodes (3): EventRow(), linkFor(), TYPES

### Community 80 - "Router"
Cohesion: 0.40
Nodes (5): demo_login(), DbSession, post, Request, Response

### Community 81 - "Env"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 83 - "Field"
Cohesion: 0.40
Nodes (3): Input, Select, Textarea

### Community 84 - "Theme"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

### Community 87 - "Decisions"
Cohesion: 0.83
Nodes (4): UI copy and frontend conventions (tokens, skeleton/empty/error states, Phosphor, no em-dashes), Frontend architecture (React 19, TanStack Query, Zod, Tailwind v4), ADR-011: JavaScript frontend (TypeScript declined), ADR-012: Tailwind v4 utilities plus hand-authored CSS design system

### Community 91 - "Queue"
Cohesion: 0.67
Nodes (3): job(), Register a coroutine as a background job under its function name., JobFn

## Ambiguous Edges - Review These
- `s3 service (SeaweedFS)` → `Phase 0: Foundations`  [AMBIGUOUS]
  docs/plan.md · relation: references

## Knowledge Gaps
- **104 isolated node(s):** `FILTERS`, `EASE`, `NO_REFRESH`, `UNSAFE`, `AuthContext` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `s3 service (SeaweedFS)` and `Phase 0: Foundations`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `get_settings()` connect `Settings & Config` to `Backend Test Harness & Samples`, `ORM Models & Base`, `HTTP Middleware`, `Documents API Router`, `Identity & Password Security`, `Extraction Pipeline Service`, `Router`, `Rate Limiter`, `Schemas & Rate-Limited Routes`, `Document Intake Service`, `Env`, `Auth Cookies & Sessions`, `Config`, `Current-User Dependency`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `S3Storage` connect `Storage` to `Document Intake Service`, `Storage`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `HttpGoogleClient` connect `Google HTTP Client` to `Google Sync Service`, `Google OAuth Router`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Base` (e.g. with `_clean_tables()` and `_schema()`) actually correct?**
  _`Base` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `FILTERS`, `EASE`, `NO_REFRESH` to the rest of the system?**
  _104 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Backend Test Harness & Samples` be split into smaller, more focused modules?**
  _Cohesion score 0.07063063063063063 - nodes in this community are weakly interconnected._