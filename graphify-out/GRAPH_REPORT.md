# Graph Report - MedSpace  (2026-10-02)

## Corpus Check
- Corpus is ~42,543 words - fits in a single context window. You may not need a graph.

## Summary
- 1022 nodes · 2205 edges · 86 communities (77 shown, 9 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 83 edges (avg confidence: 0.91)
- Token cost: 79,149 input · 0 output

## Community Hubs (Navigation)
- DB Core & ORM Base
- Test Harness & Demo Samples
- Auth Routers & Cookies
- Domain Errors & File Inspection
- Frontend Runtime Deps
- Records Module
- Frontend Dev Tooling
- Timeline & Status Enums
- SPA Router & Layouts
- Extraction Job & Prompts
- Documents Client API
- Documents API Router
- Heuristic Extractor
- Landing Sections
- API Client & Auth State
- Settings & Config
- Frequency Normalizer
- App Factory & Logging
- Review Form Mapping
- Groq LLM Adapter
- Repo Conventions (CLAUDE.md)
- Easter Eggs
- Core Flow & Modules (docs)
- Docker Compose Stack
- Rate Limiting
- App Navigation
- RAG & Embeddings (docs)
- Auth Forms
- Extraction Lifecycle
- Extraction API Router
- Data Model & Retrieval (docs)
- Extraction Pipeline (docs)
- Format Helpers
- Local Storage Adapter
- Security Model (docs)
- Lifecycle & Build Plan
- Settings Validation & Secrets
- Job Registry
- Google Integration (docs)
- HTTP Middleware
- S3 Storage Adapter
- Buttons & Dialogs
- Pun Pharmacy
- Hero Morph Preview
- CI Workflow
- Workflow Story Section
- Alembic Env
- Page Skeleton & Header
- Form Fields
- Theme Provider
- Landing Page
- Marketing Nav
- Processing State View
- Documents Page
- Backend Package

## God Nodes (most connected - your core abstractions)
1. `get_settings()` - 46 edges
2. `User` - 28 edges
3. `MedSpace Build Plan` - 23 edges
4. `Base` - 20 edges
5. `Document` - 20 edges
6. `Architecture Decision Records` - 19 edges
7. `utcnow()` - 18 edges
8. `record()` - 17 edges
9. `MedSpace Architecture Doc` - 17 edges
10. `normalize_frequency()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `CI Postgres Service (pgvector pg17)` --semantically_similar_to--> `postgres Service (pgvector/pgvector:pg17)`  [INFERRED] [semantically similar]
  .github/workflows/ci.yml → docker-compose.yml
- `Upload -> Extract -> Review -> Organize -> Act Workflow` --semantically_similar_to--> `Upload -> Extract -> Review -> Organize -> Act Flow`  [INFERRED] [semantically similar]
  README.md → docs/architecture.md
- `Ask MedSpace Assistant` --references--> `Ask MedSpace RAG Pipeline`  [INFERRED]
  README.md → docs/architecture.md
- `ADR-002: pgvector instead of FAISS` --rationale_for--> `postgres Service (pgvector/pgvector:pg17)`  [INFERRED]
  docs/decisions.md → docker-compose.yml
- `minio Service` --shares_data_with--> `S3Storage`  [INFERRED]
  docker-compose.yml → docs/architecture.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Upload -> Extract -> Review -> Organize -> Act Flow** — docs_architecture_documents_module, docs_architecture_extraction_module, docs_architecture_records_module, docs_architecture_integrations_module, docs_architecture_worker_process, docs_architecture_core_flow [EXTRACTED 1.00]
- **External Ports with Offline Fake Adapters** — docs_architecture_llmprovider, docs_architecture_embedder, docs_architecture_objectstorage, docs_architecture_googleclient, docs_architecture_ports_and_adapters [EXTRACTED 1.00]
- **Local Docker Compose Stack** — docker_compose_postgres, docker_compose_redis, docker_compose_minio, docker_compose_api, docker_compose_worker, docker_compose_web [EXTRACTED 1.00]

## Communities (86 total, 9 thin omitted)

### Community 0 - "DB Core & ORM Base"
Cohesion: 0.06
Nodes (72): Base, get_session(), IdMixin, AsyncSession, UUID, Database engine, session factory and declarative base., Time-ordered UUID (RFC 9562 v7) so primary keys index and sort well., TimestampMixin (+64 more)

### Community 1 - "Test Harness & Demo Samples"
Cohesion: 0.08
Nodes (59): reset_rate_limits(), build_lab_pdf(), build_pdf(), build_scan_png(), issued(), LabReport, date, Synthetic prescriptions rendered as real PDFs (and one scan-style PNG). Every… (+51 more)

### Community 2 - "Auth Routers & Cookies"
Cohesion: 0.08
Nodes (43): demo_login(), DbSession, post, Request, Response, create_demo_account(), _ingest(), _page_texts() (+35 more)

### Community 3 - "Domain Errors & File Inspection"
Cohesion: 0.08
Nodes (42): AppError, Conflict, Forbidden, Gone, PayloadTooLarge, _problem(), Any, Exception (+34 more)

### Community 4 - "Frontend Runtime Deps"
Cohesion: 0.05
Nodes (43): clsx, date-fns, @fontsource-variable/geist, @fontsource-variable/geist-mono, dependencies, clsx, date-fns, @fontsource-variable/geist (+35 more)

### Community 5 - "Records Module"
Cohesion: 0.14
Nodes (39): NotFound, Medication, get_prescription(), list_care_actions(), list_medications(), list_prescriptions(), CurrentUser, DbSession (+31 more)

### Community 6 - "Frontend Dev Tooling"
Cohesion: 0.06
Nodes (33): eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, devDependencies, eslint, @eslint/js, eslint-plugin-react-hooks (+25 more)

### Community 7 - "Timeline & Status Enums"
Cohesion: 0.15
Nodes (26): DocumentKind, DocumentStatus, StrEnum, get_dashboard(), get_timeline(), CurrentUser, date, DbSession (+18 more)

### Community 8 - "SPA Router & Layouts"
Cohesion: 0.08
Nodes (6): AppLayout(), AuthLayout(), MarketingLayout(), Providers(), RouteError(), router

### Community 9 - "Extraction Job & Prompts"
Cohesion: 0.14
Nodes (24): process_document(), _nullable(), Any, Prompts and the strict JSON schema for prescription extraction., repair_prompt(), text_user_prompt(), vision_user_prompt(), ExtractionPayload (+16 more)

### Community 10 - "Documents Client API"
Cohesion: 0.10
Nodes (12): ACTIVE, docKeys, isProcessing(), previewUrl(), uploadDocument(), useDocument(), useDocuments(), DocumentThumb() (+4 more)

### Community 11 - "Documents API Router"
Cohesion: 0.23
Nodes (20): delete_document(), download_document(), get_document(), list_documents(), page_preview(), CurrentUser, DbSession, delete (+12 more)

### Community 12 - "Heuristic Extractor"
Cohesion: 0.18
Nodes (19): extract(), _medication_from_line(), _parse_date(), date, Offline, rule-based extractor used when no LLM is configured (CI, demo, keyless…, ConfirmCareAction, ConfirmIn, ConfirmMedication (+11 more)

### Community 13 - "Landing Sections"
Cohesion: 0.11
Nodes (6): Faq, DAYS, EASE, EASE, Reveal(), PRINCIPLES

### Community 14 - "API Client & Auth State"
Cohesion: 0.17
Nodes (13): api(), ApiError, NO_REFRESH, onSessionExpired(), readCookie(), refreshSession(), setSessionExpiredHandler(), UNSAFE (+5 more)

### Community 15 - "Settings & Config"
Cohesion: 0.15
Nodes (15): get_settings(), Application settings, loaded from environment variables (and `.env` in…, purge_expired_demo_accounts(), post, upload_document(), enqueue(), _get_arq_pool(), Any (+7 more)

### Community 16 - "Frequency Normalizer"
Cohesion: 0.20
Nodes (16): _clean(), _hm_to_min(), _min_to_hm(), normalize_frequency(), parse_duration_days(), Deterministic normalization of prescription shorthand (ADR-006). The LLM copies…, x 7 days' -> 7, '2/52' -> 14, '3/12' -> 90, '1 month' -> 30. Ongoing or unknown…, Schedule (+8 more)

### Community 17 - "App Factory & Logging"
Cohesion: 0.22
Nodes (15): install_error_handlers(), FastAPI, ServiceUnavailable, configure_logging(), Logging configuration., CSRFMiddleware, HTTP middleware: security headers, CSRF double-submit check, request logging., Double-submit cookie check for cookie-authenticated unsafe requests. Requests… (+7 more)

### Community 18 - "Review Form Mapping"
Cohesion: 0.25
Nodes (13): blank(), CARE_KINDS, emptyCareAction(), emptyMedication(), formToConfirm(), num(), payloadToForm(), reviewSchema (+5 more)

### Community 19 - "Groq LLM Adapter"
Cohesion: 0.23
Nodes (9): get_llm(), GroqProvider, LLMError, LLMProvider, _parse_json(), Any, Exception, Protocol (+1 more)

### Community 20 - "Repo Conventions (CLAUDE.md)"
Cohesion: 0.20
Nodes (16): CLAUDE.md Repository Guidance, AppError (problem+json errors), Context Recovery Reading Order, Conventional Commits Policy (no AI attribution), Docs Discipline, Thin Routers, Logic in Services, Loading/Empty/Error States Rule, MedSpace Architecture Doc (+8 more)

### Community 21 - "Easter Eggs"
Cohesion: 0.18
Nodes (12): AppleRain(), makeApples(), AppleRain, EasterEggProvider(), onKey(), EggContext, EGGS, isTyping() (+4 more)

### Community 22 - "Core Flow & Modules (docs)"
Cohesion: 0.20
Nodes (14): Cross-Module Import Rule, Upload -> Extract -> Review -> Organize -> Act Flow, documents Module, extraction Module, LocalStorage, Modular Monolith (API + Worker), ObjectStorage Port, records Module (+6 more)

### Community 23 - "Docker Compose Stack"
Cohesion: 0.30
Nodes (14): Docker Compose Stack (medspace), api Service (alembic + uvicorn), x-backend-env Shared Environment, minio Service, minio-init Bucket Bootstrap, postgres Service (pgvector/pgvector:pg17), redis Service, web Service (Vite dev server) (+6 more)

### Community 24 - "Rate Limiting"
Cohesion: 0.18
Nodes (7): _get_store(), _MemoryStore, Any, Request, rate_limit(), Fixed-window rate limiting. Uses Redis when `QUEUE_MODE=arq` (multi-process…, _RedisStore

### Community 25 - "App Navigation"
Cohesion: 0.23
Nodes (7): APP_LINKS, AppNav(), MobileDrawer(), ThemeToggle(), initials(), UserMenu(), useScrolled()

### Community 26 - "RAG & Embeddings (docs)"
Cohesion: 0.22
Nodes (11): Ask MedSpace RAG Pipeline, assistant Module, demo Module (synthetic seeding), Embedder Port, FastEmbedEmbedder, HashEmbedder, RAG Guardrails (cite-only, no diagnosis), ADR-004: Local Embeddings with fastembed (+3 more)

### Community 27 - "Auth Forms"
Cohesion: 0.25
Nodes (7): DemoDivider(), LoginForm(), loginSchema, SignupForm(), signupSchema, useAuthMutation(), useDemoLogin()

### Community 28 - "Extraction Lifecycle"
Cohesion: 0.42
Nodes (10): set_status(), Extraction, One AI reading of a document. Versioned; only a confirmed version becomes…, confirm(), discard(), get_extraction(), latest_for_document(), AsyncSession (+2 more)

### Community 29 - "Extraction API Router"
Cohesion: 0.40
Nodes (9): confirm_extraction(), discard_extraction(), get_latest_extraction(), CurrentUser, DbSession, get, post, Request (+1 more)

### Community 30 - "Data Model & Retrieval (docs)"
Cohesion: 0.22
Nodes (10): audit_logs Append-Only Table, Data Model (ER), document_chunks Table (vector(384) + tsvector), Reciprocal Rank Fusion (hybrid retrieval), Secure Sharing Flow (hashed tokens, proxied files), sharing Module, ADR-002: pgvector instead of FAISS, ADR-010: Share Links Proxied through API, Tokens Hashed (+2 more)

### Community 31 - "Extraction Pipeline (docs)"
Cohesion: 0.31
Nodes (10): Extraction Pipeline (classify, extract, validate, normalize, draft), FakeLLM, GroqProvider, LLMProvider Port, PrescriptionExtraction Schema, Schedule Model (times, days_of_week, as_needed), ADR-003: Groq LLM behind Provider Interface, ADR-006: Deterministic Frequency Normalization (+2 more)

### Community 32 - "Format Helpers"
Cohesion: 0.36
Nodes (8): firstName(), formatBytes(), formatClock(), formatDate(), formatRelativeDay(), greeting(), timeAgo(), toDate()

### Community 33 - "Local Storage Adapter"
Cohesion: 0.36
Nodes (3): LocalStorage, Stores objects under a directory. Used for tests and keyless local runs., Path

### Community 34 - "Security Model (docs)"
Cohesion: 0.28
Nodes (9): user_id Scoping on Every Query, audit Module, CSRF Double-Submit Token, identity Module, Rotating Refresh Tokens with Family Reuse Detection, Security Model, ADR-008: Own Authentication; Google OAuth only for Integrations, ADR-014: Same-Origin API for First-Party Auth Cookies (+1 more)

### Community 35 - "Lifecycle & Build Plan"
Cohesion: 0.28
Nodes (9): Document/Extraction Data Lifecycle, ADR-009: Draft -> Confirmed Lifecycle with Provenance, MedSpace Build Plan, Phase 0: Foundations, Phase 8: Hardening + Launch, README (MedSpace), Ask MedSpace Assistant, Human-in-the-Loop Review Workspace (+1 more)

### Community 36 - "Settings Validation & Secrets"
Cohesion: 0.25
Nodes (4): field_validator, Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod., Settings, BaseSettings

### Community 37 - "Job Registry"
Cohesion: 0.29
Nodes (5): Import every module's jobs so the registry in `app.shared.queue.JOBS` is…, Background job: process an uploaded document end to end., job(), Register a coroutine as a background job under its function name., JobFn

### Community 38 - "Google Integration (docs)"
Cohesion: 0.32
Nodes (8): FakeGoogleClient, Google Integration (Calendar + Tasks), GoogleClient Port, HttpGoogleClient, integrations Module, sync_links Idempotency Mapping, ADR-005: Calendar for Recurring Reminders, Tasks for One-off Actions, Phase 6: Google Calendar + Tasks

### Community 39 - "HTTP Middleware"
Cohesion: 0.48
Nodes (4): Request, Response, constant_time_equals(), RequestResponseEndpoint

### Community 42 - "Pun Pharmacy"
Cohesion: 0.29
Nodes (5): EMPTY_QUIPS, LOADING_PUNS, MARQUEE_PUNS, NOT_FOUND_LINES, PROCESSING_PUNS

### Community 43 - "Hero Morph Preview"
Cohesion: 0.33
Nodes (6): DURATIONS, EASE, HeroMorph(), PHASES, RX, usePhase()

### Community 44 - "CI Workflow"
Cohesion: 0.47
Nodes (6): CI Workflow, CI Backend Job (ruff + pytest), CI Docker Images Build Job, CI Frontend Job (lint + test + build), CI Postgres Service (pgvector pg17), Deployment Topology

### Community 46 - "Alembic Env"
Cohesion: 0.70
Nodes (4): _do_run(), run_migrations_offline(), run_migrations_online(), _url()

### Community 48 - "Form Fields"
Cohesion: 0.40
Nodes (3): Input, Select, Textarea

### Community 49 - "Theme Provider"
Cohesion: 0.50
Nodes (3): systemTheme(), ThemeContext, ThemeProvider()

## Knowledge Gaps
- **89 isolated node(s):** `WorkerSettings`, `medspace-api`, `name`, `private`, `version` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `Settings & Config` to `DB Core & ORM Base`, `Test Harness & Demo Samples`, `Auth Routers & Cookies`, `Domain Errors & File Inspection`, `Settings Validation & Secrets`, `HTTP Middleware`, `S3 Storage Adapter`, `Extraction Job & Prompts`, `Documents API Router`, `Alembic Env`, `App Factory & Logging`, `Groq LLM Adapter`, `Rate Limiting`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `User` connect `DB Core & ORM Base` to `Auth Routers & Cookies`, `Job Registry`, `Timeline & Status Enums`, `Extraction Job & Prompts`, `Extraction Lifecycle`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `normalize_frequency()` connect `Frequency Normalizer` to `Extraction Job & Prompts`, `Heuristic Extractor`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Base` (e.g. with `_clean_tables()` and `_schema()`) actually correct?**
  _`Base` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `WorkerSettings`, `medspace-api`, `name` to the rest of the system?**
  _89 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DB Core & ORM Base` be split into smaller, more focused modules?**
  _Cohesion score 0.059917920656634746 - nodes in this community are weakly interconnected._
- **Should `Test Harness & Demo Samples` be split into smaller, more focused modules?**
  _Cohesion score 0.08234126984126984 - nodes in this community are weakly interconnected._