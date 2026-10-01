# Architecture Decision Records

Every meaningful change to the plan or architecture gets an entry here: **what** changed, **why**, and **what it costs**. Newest at the bottom. Never delete an ADR; supersede it with a new one and update the status.

Format: `Status: Accepted | Superseded by ADR-xxx | Deprecated`

---

## ADR-001: Modular monolith with two processes

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** The feature set (documents, extraction, records, RAG, integrations, sharing) has clear domain seams but a single developer and a portfolio budget. Microservices would add network hops, deployment surface and distributed-transaction problems with no user-facing benefit.
- **Decision:** One FastAPI codebase organized into bounded-context modules (`backend/app/modules/*`) with an explicit import rule (modules talk through `service.py`). Deployed as an `api` process and a `worker` process from the same image.
- **Consequences:** Simple local dev and deploy; module seams keep extraction into services possible later. Discipline is enforced by convention and code review, not by the network.

## ADR-002: pgvector instead of FAISS

- **Date:** 2026-10-01
- **Status:** Accepted (replaces "FAISS/vector search" from the original plan)
- **Context:** A FAISS index lives outside Postgres. That creates (1) dual-write consistency problems when documents are deleted or shares revoked, (2) no per-user isolation at the index level (cross-tenant leakage risk in a health app), (3) loss of the index on ephemeral PaaS disks (Render/Fly/Railway), (4) extra persistence and rebuild code.
- **Decision:** Store embeddings in `document_chunks.embedding vector(384)` with an HNSW cosine index, filtered by `user_id` in SQL, combined with Postgres full-text search via Reciprocal Rank Fusion (hybrid retrieval).
- **Consequences:** Transactional deletes via `ON DELETE CASCADE`, one datastore to back up, tenant isolation in the WHERE clause. Requires the `vector` extension (available on Neon, Supabase, RDS, and the `pgvector/pgvector` Docker image). At portfolio scale (≪1M chunks) performance is a non-issue.

## ADR-003: Groq as the LLM provider, behind a provider interface

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** The user chose Groq. Groq does not accept PDF input; only `qwen/qwen3.8-27b` accepts images (max 3 per request, JSON mode but not strict schemas); strict `json_schema` outputs are supported on `openai/gpt-oss-120b`/`20b` but not combined with images or streaming.
- **Decision:** Two extraction paths: text-layer PDFs → PyMuPDF text → `openai/gpt-oss-120b` with strict JSON schema; scanned PDFs/images → rendered page PNGs (batches of ≤3) → `qwen/qwen3.8-27b` in JSON mode → Pydantic validation with one repair retry. RAG answers stream from `openai/gpt-oss-120b`. Model IDs are env-configurable (`GROQ_TEXT_MODEL`, `GROQ_VISION_MODEL`, `GROQ_CHAT_MODEL`). All calls go through `LLMProvider`, with a deterministic `FakeLLM` when `LLM_PROVIDER=fake` or no key is set.
- **Consequences:** The demo and CI run with zero API keys. Swapping providers is a single adapter. Vision batching adds latency on multi-page scans (acceptable: processing is async with progress UI).

## ADR-004: Local embeddings with fastembed

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** Groq offers no embeddings endpoint. A second paid API key would hurt the "clone and run" experience.
- **Decision:** `fastembed` with `BAAI/bge-small-en-v1.5` (384-d, ONNX, CPU) in the worker/API. Tests use a deterministic `HashEmbedder`.
- **Consequences:** Free and offline; ~130 MB model download on first run (cached in a Docker volume). Quality is good for short medical documents.

## ADR-005: Calendar for recurring reminders, Tasks for one-off actions

- **Date:** 2026-10-01
- **Status:** Accepted (refines original "Google Tasks integration" scope)
- **Context:** Google Tasks API stores only the date part of `due` (time is discarded) and has no recurrence. "Take medication" as a recurring Task cannot represent "8am and 8pm for 7 days".
- **Decision:** Recurring medication reminders, appointments and follow-ups → **Google Calendar** (RRULE events). One-off care actions (get a lab test, complete the course, upload a follow-up report, prepare documents) → **Google Tasks** in a dedicated "MedSpace" list.
- **Consequences:** Each Google surface is used for what it does well; the UI explains the split ("Reminders go to Calendar, to-dos go to Tasks").

## ADR-006: Deterministic frequency normalization

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** Prescriptions encode frequency as `1-0-1`, `BD`, `TDS`, `q8h`, `HS`, `SOS/PRN`, "after food". Letting the LLM invent clock times is non-deterministic and untestable.
- **Decision:** The LLM extracts `frequency_raw` verbatim; a pure-Python parser maps it to `Schedule {times[], as_needed, period}` using the user's preferred dose times (default 08:00 / 14:00 / 20:00 / 22:00). PRN medications are never calendared. Unparseable values are flagged for the reviewer.
- **Consequences:** Table-driven unit tests cover the abbreviations; reviewers always see and can edit the resulting times.

## ADR-007: Durable job queue with ARQ + inline fallback

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** FastAPI `BackgroundTasks` run in the request process and are lost on restart; extraction and embeddings take seconds to minutes and need retries.
- **Decision:** ARQ (async-native, Redis-backed) with a dedicated worker process. `QUEUE_MODE=inline` executes jobs as in-process asyncio tasks for tests and single-instance free-tier demos.
- **Consequences:** Adds Redis to the stack (already useful for rate limiting). Job functions are plain async functions, so both modes share code.

## ADR-008: Own authentication; Google OAuth only for integrations

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** Mixing "Sign in with Google" with Calendar/Tasks consent couples login to sensitive scopes and forces Google verification for every user.
- **Decision:** Email/password auth owned by MedSpace (Argon2id, JWT access cookie, rotating refresh tokens with reuse detection, CSRF double-submit). Google is a separately connected account with incremental consent; tokens are Fernet-encrypted at rest.
- **Consequences:** Without Google app verification the OAuth consent screen stays in *Testing* mode (≤100 named test users). Documented in README. A demo account works without Google entirely.

## ADR-009: Draft → confirmed data lifecycle with provenance

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** AI extraction is fallible; health data must not silently become "truth".
- **Decision:** Extractions are versioned drafts with per-field `confidence` and `source_page`. Only an explicit user confirmation creates `prescriptions`/`medications`/`care_actions`. Only confirmed data syncs to Google, appears in the timeline, or is shareable as a report.
- **Consequences:** An extra review step in the UX, which is the product's trust story and is designed as a first-class screen (side-by-side source preview).

## ADR-010: Share links proxied through the API, tokens hashed

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** Presigned storage URLs cannot be revoked or audited once issued.
- **Decision:** Random 256-bit tokens shown once, stored as SHA-256. Public endpoints validate expiry/revocation/view-limit on every request and stream files through the API, writing an audit row per view.
- **Consequences:** Slightly more API bandwidth; revocation is instant and every access is logged.

## ADR-011: JavaScript frontend (TypeScript declined)

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** TypeScript was proposed; the user chose to stay with JavaScript.
- **Decision:** React + JSX. Mitigations: Zod schemas at the API boundary (forms and response parsing on critical paths), JSDoc types on shared utilities, ESLint with React Hooks rules, Vitest coverage on logic-heavy hooks.
- **Consequences:** Less compile-time safety; keep API contracts mirrored in `frontend/src/lib/schemas.js`.

## ADR-012: Tailwind v4 utilities plus hand-authored CSS design system

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** The user wants a bespoke, senior-looking UI and asked for "a mix of both": Tailwind for speed, hand-written CSS so the result does not look like a Tailwind template.
- **Decision:** Design tokens (color, type scale, radius, shadow, motion curves) live as CSS custom properties in `styles/tokens.css` and are exposed to Tailwind via `@theme`. Layout/spacing uses utilities; signature components (skeleton shimmer, hero document morph, timeline rail, chat bubbles, dropzone) have dedicated CSS. Visual language: Geist type, evergreen accent, off-white/ink neutrals, soft 14px radius system, light + dark themes.
- **Consequences:** One source of truth for tokens; components stay readable.

## ADR-013: Synthetic data only, explicit non-goals

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** A portfolio app processing health records must not imply clinical use.
- **Decision:** Demo seed and sample uploads use synthetic prescriptions (fictional prescribers, clinics and patients). The UI never diagnoses, recommends treatment or alters doses; the assistant refuses such requests. App-wide disclaimer: not a medical device, not HIPAA compliant.
- **Consequences:** Clear scope for reviewers; guardrail tests in the assistant test suite.

## ADR-014: Same-origin API for first-party auth cookies

- **Date:** 2026-10-01
- **Status:** Accepted
- **Context:** Auth uses `SameSite=Lax` httpOnly cookies. If the SPA (e.g. Vercel) and API (e.g. Render) live on different sites, browsers treat the cookies as third-party and increasingly block them.
- **Decision:** The SPA always calls a same-origin `/api` path: the Vite dev proxy locally and a host rewrite/reverse proxy in production (Vercel `rewrites`, Netlify `_redirects`, or nginx). `VITE_API_URL` exists only as an escape hatch.
- **Consequences:** No CORS preflights in normal operation, cookies stay first-party, and CSRF protection stays simple. Deployment docs must include the rewrite rule.

## ADR-015: Server-rendered page previews; records only for prescriptions

- **Date:** 2026-10-02
- **Status:** Accepted
- **Context:** (1) Embedding PDFs in an iframe is inconsistent across browsers and mostly broken on mobile, and framing would require relaxing `X-Frame-Options`. (2) Confirming a lab report created an empty "prescription", which polluted counts and the timeline.
- **Decision:** (1) `GET /documents/{id}/pages/{n}/preview` renders each page to PNG with PyMuPDF and caches it in object storage next to the original; the review workspace shows images. (2) `records.replace_for_document` returns no prescription when the document is not a prescription and has no medications or to-dos; such documents still appear on the timeline as reports.
- **Consequences:** Identical preview behaviour everywhere, strict framing headers stay on, and a natural hook for future bounding-box highlights. Lab results are not yet structured (future work).
