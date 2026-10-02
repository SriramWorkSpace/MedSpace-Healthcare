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
- **Status:** Amended by ADR-017 (Google sign-in added as an option)
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

## ADR-016: SeaweedFS for local S3; storage failures surface as 503

- **Date:** 2026-10-02
- **Status:** Accepted (supersedes the MinIO detail of ADR-001's local topology)
- **Context:** MinIO stopped publishing community images to Docker Hub (and quay.io), so `docker compose up` failed for new clones. Separately, a misconfigured store produced generic 500s on upload and silently empty demo accounts.
- **Decision:** The compose stack uses SeaweedFS (`chrislusf/seaweedfs`, `server -s3`) on port 8333; the app talks plain S3, so production can use Cloudflare R2 or AWS S3 unchanged. `S3Storage` creates its bucket on first use (no init container) and maps provider errors to `503 File storage is temporarily unavailable`. The embedding model is warmed up at API and worker start so the first demo login doesn't pay the download.
- **Consequences:** One fewer container; storage outages are explicit to users and in logs.

## ADR-017: Optional "Continue with Google" that can also connect reminders

- **Date:** 2026-10-02
- **Status:** Accepted (amends ADR-008)
- **Context:** Users who live in Google expect one-click sign-in, and connecting Calendar/Tasks as a separate step afterwards is friction. Making Google the *only* sign-in would force every user (and every recruiter trying the demo) through Google's sensitive-scope consent screen and its 100-test-user cap.
- **Decision:** Email/password stays; "Continue with Google" is an option on both auth pages. It requests `openid email profile` plus `calendar.events` and `tasks` in a single consent. If the user leaves Calendar/Tasks ticked, the OAuth connection is stored and reminders work immediately; if they untick them (Google's granular consent allows it), they are simply signed in and can connect later from Settings or the "Add to Google" dialog. Both flows share one callback (`/api/integrations/google/callback`), so only one redirect URI is registered; a signed, httpOnly state cookie carries the intent (`login` or `connect`), the PKCE verifier and a validated relative `next` path.
- **Account rules:** match on Google's stable `sub` first; link an existing password account only when Google reports the email as verified (otherwise `email_taken`, never silent takeover); otherwise create a password-less account. Password login on a Google-only account fails with the same generic error as a wrong password. In simulation mode each sign-in is a distinct, seeded, 24-hour demo account so visitors never share data.
- **Consequences:** `users.password_hash` is nullable and `users.google_sub` is unique. One consent screen for the common case, still optional for everyone else.

## ADR-018: Diet notes come from documents; MedSpace never generates nutrition advice

- **Date:** 2026-10-02
- **Status:** Accepted
- **Context:** A request to "recommend macros and micros for people with medical conditions" amounts to medical nutrition therapy. Correct targets depend on diagnosis, stage and labs (protein and potassium limits in kidney disease, for example); MedSpace does not know conditions and must not infer them (ADR-013).
- **Decision:** Build "Diet notes from your care team" instead. Diet, food and drink instructions written on a document (e.g. "low-salt diet", "avoid alcohol while on antibiotics") are extracted with a category (avoid, limit, include, timing, general) and source page, reviewed and edited like every other field, and stored as `diet_notes` tied to the document (so letters and reports can carry them too). Food rules attached to current medicines ("after meals", "with milk") are derived at read time from confirmed medications. They appear on a Diet page, a dashboard card, the prescription report and share view, and as citable sources in Ask MedSpace. The extraction prompt forbids adding advice; the UI says notes are copied, not recommended.
- **Consequences:** Useful, low-risk and consistent with the trust model. Personalized targets (logging meals against clinician-set limits) remain a possible future feature.

## ADR-019: Global search on Postgres, no separate search engine

- **Date:** 2026-10-02
- **Status:** Accepted
- **Context:** Users need to find a medicine, doctor, to-do or a line inside a document without knowing which page it lives on. Options: a search service (Meilisearch, OpenSearch), the existing vector index, or Postgres.
- **Decision:** One read-model endpoint, `GET /search`, queries Postgres directly. Names use escaped `ILIKE` substring matching so partial words work as you type ("amox"); document contents reuse the chunk `tsvector` GIN index with prefix `to_tsquery` (`amox:* & 500:*`) and `ts_headline` snippets. Vectors are not used: search should be literal and predictable, and Ask MedSpace already covers questions. Every query filters by `user_id` in SQL. The UI is a command palette that deep-links to the result.
- **Consequences:** No new infrastructure to run or keep in sync, and results are always consistent with confirmed records. No typo tolerance or cross-group ranking; at personal-record scale that is acceptable, and a trigram index can be added if it is not.

## ADR-020: Structured lab results, flagged only against the printed range

- **Date:** 2026-10-02
- **Status:** Accepted (supersedes the "records only for prescriptions" part of ADR-015 for lab reports)
- **Context:** Lab reports were confirmed as plain documents, so values like LDL or HbA1c could not be followed over time. Showing trends is useful, but saying whether a value is good, bad or concerning is interpretation, which MedSpace does not do (ADR-013).
- **Decision:** Extract each result as printed (test name, value, unit, reference range, and any H/L flag printed by the lab), review it like every other field, and store it in `lab_results` tied to its document. On confirm, deterministic code parses the value and the printed range and sets `flag` to `low`, `high` or `normal` relative to that range only; a range that parses wins over a printed flag so an edited value cannot keep a stale flag. MedSpace never supplies a range of its own. Test names map to an `analyte_key` so the same test from different reports charts as one series; results in another unit are listed but not charted. The Labs page groups tests by report, shows direction of change ("Down 11 mg/dL since Feb 13") without judging it, and repeats that each result is compared only with its own report's range. Ask MedSpace states values and printed ranges; questions like "is my cholesterol high?" get the no-advice reply followed by the records.
- **Consequences:** Real trends with no new medical claims. Synonym mapping is a short hand-written list; unusual test names chart separately until it grows. Converting between units is out of scope.

## ADR-021: Dose tracking on the server, with no assumed misses

- **Date:** 2026-10-02
- **Status:** Accepted (replaces device-only dose ticks)
- **Context:** Ticks on the dashboard lived in `localStorage`: they did not follow the user to another device, vanished when site data was cleared, and could not show history. Adherence views are useful, but treating every unmarked dose as "missed" would be a claim MedSpace cannot verify, and scoring people can feel punitive.
- **Decision:** A `dose_logs` table stores one row per scheduled dose the user marks, keyed by medicine, local calendar date and scheduled time (unique), with status `taken` or `skipped`. Marks are upserted and can be cleared. Only doses on the medicine's schedule can be logged, never for a future day; the evening dose can be marked early on the same day. History is computed from the schedule plus the log in the user's timezone; unmarked past doses are "not logged" and doses later today are "upcoming". A stopped medicine keeps its history up to the day it was stopped. The UI reports counts and "days in a row with every due dose taken" in neutral words, lets users fill in or correct past days, and says that the history is not advice. Ask MedSpace can state the counts; "what should I do if I missed a dose?" gets the no-advice reply. Old device ticks for today are moved to the account once.
- **Consequences:** Marks sync everywhere and show up in exports. Changing a medicine's times does not rewrite past marks; marks at times no longer scheduled simply stop appearing in history.

## ADR-022: Visit prep as stored questions plus a live, factual brief

- **Date:** 2026-10-02
- **Status:** Accepted
- **Context:** Appointments are short. People forget questions and struggle to recall what changed since the last visit. MedSpace already holds the pieces (confirmed medicines, dose marks, lab results, to-dos), but in separate pages.
- **Decision:** A `visit_preps` row stores only what the user authored: title, visit date, clinician, an optional "changes since" date and up to 30 questions (JSONB, each with an optional `prompt_key`). The brief is a read model built on request from records, so it stays current until the visit: current medicines, medicine changes, dose marks per medicine (only medicines with marks in the period, so untracked ones never read as missed), lab results collected in the period with their previous value, open to-dos, upcoming appointments, diet notes and new documents. The period defaults to the previous visit's date, else 90 days (capped at 120). "From your records" prompts are observations only (a value outside its printed range, doses marked skipped, a course ending soon, an overdue to-do); adding one creates a question the user can edit. A brief can be printed or shared through the existing share links as a new `visit` item type; the public view renders the same component.
- **Consequences:** No duplicated medical data and nothing to keep in sync. A shared brief reflects records at viewing time rather than a frozen snapshot; that is acceptable for short-lived links and avoids storing copies of health data.

## ADR-023: Supply estimates from the user's own count

- **Date:** 2026-10-02
- **Status:** Accepted
- **Context:** Running out of a long-term medicine is a common, avoidable problem. MedSpace knows each schedule and which doses were marked skipped, but not how many units the user has; prescriptions rarely state a quantity reliably, and pharmacies dispense differently.
- **Decision:** The user enters a count (units on hand, unit, units per dose, a warning window). One `medication_supplies` row per medicine stores it with a timestamp. The estimate is arithmetic: units left = count minus units per dose for every scheduled dose after the count, except doses marked skipped. The run-out date is the first future scheduled dose the estimate can't cover, projected up to 400 days, or "enough for the rest of the course" when the course ends first. As-needed medicines keep the count but get no date. A refill adds to the current estimate and restarts the count. Status (`ok`, `low`, `out`, `course_covered`, `as_needed`) drives a dashboard "Running low" card, visit-prep prompts and Ask MedSpace answers; the UI always says "estimate".
- **Consequences:** Useful with no new medical claims and no guessing about pharmacies. Untaken doses that weren't marked skipped are assumed taken, so estimates drift low rather than high, which errs on the side of refilling early; recounting resets drift.

## ADR-024: Measure extraction with a generated, labelled corpus; gate it in CI

- **Date:** 2026-10-02
- **Status:** Accepted
- **Context:** Extraction is the core AI feature, but its accuracy was only ever checked by example tests. Real prescriptions can't be used (synthetic data only, ADR-013), and hand-labelling documents is slow and error-prone.
- **Decision:** `app/eval` generates fictional documents from structured specs, so gold answers are exact by construction, renders them to real PDFs, and runs them through the production text path (`extract_text_pages`). A field-level scorer reports per-metric accuracy, per-tag breakdowns and concrete failures. Two sets: a regression set the extractor is tuned against (CI fails below `thresholds.json`), and a stress set of held-out phrasings whose first run is the honest generalization estimate. The same runner measures the Groq path when a key is present. Numeric dates are read day-first, matching the shorthand the extractor targets, and ambiguous ones raise a review warning rather than being guessed silently.
- **Consequences:** Accuracy is a number in CI, and every extractor change shows its effect. Generated documents are cleaner than real ones, so scores are an upper bound; the docs say so. Once a held-out set has been tuned against, it becomes a regression set and new phrasings are needed for the next honest estimate.

## ADR-025: Installable app; offline reading is opt-in and never in the service worker

- **Date:** 2026-10-03
- **Status:** Accepted
- **Context:** People check their schedule in places with poor signal (pharmacies, clinics, travel) and want MedSpace on their home screen. Caching health data on a device is a privacy decision, though: shared computers and lost phones exist.
- **Decision:** A web app manifest and icons make the app installable. A build-time Vite plugin emits `sw.js` with a content hash and the list of every built asset, so each deploy installs exactly its own files. The worker serves the app shell and hashed assets from cache and falls back to the shell for navigations while offline. It never handles `/api`. Offline reading is a per-device opt-in in Settings: the app snapshots selected query data (records, dashboard, doses, labs, visits, supply; not chat, search, shares or audit) into IndexedDB with TanStack Query's `dehydrate`, restores it before the first render, expires it after 7 days, ties it to the signed-in user, and deletes it on sign-out, session expiry or when the setting is turned off. Dose ticks made offline are paused mutations with a registered default request, so they persist with the snapshot and resume on reconnect. Startup seeds TanStack's online state from `navigator.onLine`, since it otherwise assumes "online" until an event fires.
- **Consequences:** Reading and ticking doses work without a connection when the user chooses it; nothing health-related is cached by default. Edits other than dose ticks need a connection. Assets match by URL with `ignoreVary` because module scripts are CORS requests and servers send `Vary: Origin`; this is safe because asset URLs are content-hashed.

