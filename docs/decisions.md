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

## ADR-026: Care circle with central, allow-listed "acting for" access

- **Date:** 2026-10-03
- **Status:** Accepted
- **Context:** Many people manage medicines with help: an adult child for a parent, a partner, a carer. Sharing a password or a public share link is the wrong tool; helpers need ongoing, revocable, limited access to the live records.
- **Decision:** An owner invites someone by email with a role: viewer (read) or helper (read, and tick doses, complete to-dos, update supply). Invitations are one-time tokens stored only as hashes, expire after 7 days, and can only be accepted by a signed-in account with the invited email. A caregiver acts on someone's records by sending `X-Acting-For: <owner id>`. The check lives in one place: `get_current_user` hands the request to `circle.resolve_acting`, which requires an active link and matches the route's method and template against an allow-list for the role. Anything not listed is refused, so new endpoints are private by default; routes about the signed-in person themselves (auth, circle, profile, audit, integrations) ignore the header. Changes made by helpers write a `caregiver.change` audit row to the owner's log in the same transaction. The frontend keeps the acting profile per tab (sessionStorage), clears the query cache on every switch, shows a banner, hides controls the role can't use, switches back automatically if access is revoked, and never writes someone else's records to the offline copy.
- **Consequences:** One small, testable surface decides cross-account access. The allow-list must be extended deliberately when a caregiver-relevant endpoint is added. Section names are compared by path segment, not prefix (a prefix test once let "/medications" match "/me"; a test caught it before release).

## ADR-027: Rate limiting: baseline budgets, targeted limits, honest client IPs

- **Date:** 2026-10-03
- **Status:** Accepted (replaces the original per-route, fixed-window limiter)
- **Context:** Before going public, a review of the limiter found that it keyed every limit on the first `X-Forwarded-For` value, which the client controls (anyone could bypass every limit, including sign-in protection, by sending a random header). Most endpoints had no limit at all, including AI-backed reprocessing and data export. Sign-in was limited per IP only, everyone behind one network shared a budget, fixed windows allowed double bursts at boundaries, and the in-memory store silently became per-process with several workers.
- **Decision:**
  - **Two layers.** Middleware applies a baseline budget to every `/api` request (reads and writes separately). Per-route dependencies add tighter limits where cost or risk is higher: sign-in, sign-up, demo, refresh, Google sign-in (per IP); reprocessing, confirmations, uploads, Ask MedSpace, exports, account deletion, share creation, invitations, visit preps and supply writes (per user); public share views and files (per IP). Sign-in also has a per-account limit (10 attempts per 15 minutes per email), so guessing one password from many addresses still slows down.
  - **Keys.** Signed-in requests are keyed by user id (read from the access token), signed-out requests by client IP.
  - **Client IP.** `X-Forwarded-For` is used only for `TRUSTED_PROXY_HOPS` proxies we run: the client is the N-th entry from the right. Uvicorn's proxy-header rewriting is turned off so there is one source of truth.
  - **Algorithm.** Sliding-window counters (previous window weighted by overlap plus the current window), two keys per limit in Redis or memory. `RATE_LIMIT_BACKEND` chooses explicitly; production with more than one process uses Redis. If the store fails, requests are allowed and a warning is logged.
  - **Responses.** `RateLimit-Limit/Remaining/Reset` on API responses (the tightest applicable limit); `429` problem+json with `Retry-After`. The frontend turns that into "Try again in N seconds".
  - **Environments.** `RATE_LIMIT_SCALE` multiplies limits for local e2e runs (10 in Docker dev, 20 in CI) so tests exercise the limiter instead of turning it off; it stays 1 in production.
- **Consequences:** No endpoint is unlimited, and limits can't be dodged with a forged header. Deployments must set `TRUSTED_PROXY_HOPS` correctly (documented in deployment.md with what goes wrong either way). Limits are counted per process when `memory` is chosen with several workers, which the docs warn against.

## ADR-028: Dose reminders by Web Push, actionable from the notification

- **Date:** 2026-10-03
- **Status:** Accepted
- **Context:** Reminders depended on Google Calendar, which many people don't use. The installable app (ADR-025) already has a service worker, so the browser's own push channel is available without a third-party account.
- **Decision:** A `reminders` module stores push subscriptions (one per browser, upserted by endpoint, never echoed back in full), per-user settings (on/off, lead time of 0 to 30 minutes) and a `reminder_logs` row per reminded dose. A tick runs every minute (ARQ cron with a worker; an in-process loop in inline deployments): for each user with a device it finds doses whose reminder time fell in the last 10 minutes (in the user's timezone), skips doses already marked, claims each dose with `INSERT ... ON CONFLICT DO NOTHING` so concurrent workers can't double-send, groups doses due at the same time into one notification and sends it to every device. Expired endpoints (404/410) and endpoints failing 5 times in a row are removed. Each notification carries a signed, 12-hour token for exactly those doses; the service worker's Taken and Skip buttons post it to `/api/push/actions` without cookies, so no session is exposed to the worker and CSRF does not apply. Push goes through a port: pywebpush with VAPID keys in production, a recording fake in dev, demo and CI.
- **Consequences:** Reminders work for anyone who installs or opens the site in a browser that supports push. Caregivers don't get reminders for the people they help yet (added in ADR-032). A notification's token can mark (or re-mark) its own doses until it expires, which is the intended convenience. E2E tests stub the browser subscription (headless browsers have no push service) and deliver push messages to the real service worker via CDP, using full Chromium because the headless shell denies notifications.

## ADR-029: Two-step verification, session-bound access tokens, device list

- **Date:** 2026-10-03
- **Status:** Accepted
- **Context:** A health record behind a password alone is one leaked password away from exposure. Signing out another device only revoked its refresh token, so a stolen access token kept working for up to 15 minutes, and there was no way to see which devices were signed in.
- **Decision:** TOTP (RFC 6238: HMAC-SHA1, 30-second steps, 6 digits, a window of one step either side) implemented in `app/core/totp.py` (about 60 lines, checked against the RFC vectors) rather than a dependency. The secret is Fernet-encrypted at rest; setup is two-step (a pending secret becomes active only after a correct code), and the last accepted step is stored so a code can't be used twice. Ten one-time recovery codes are stored as SHA-256 hashes, shown once, and replaced as a set. With two-step on, a correct password (or a Google sign-in) returns a signed 5-minute `mfa` token instead of a session; `POST /auth/login/mfa` exchanges it plus a code for the session, limited per IP and to 5 attempts per account per 5 minutes. Access tokens now carry `sid`, their refresh-token family, and every authenticated request checks that the family still has a live token, so signing a device out takes effect on its next request (one indexed lookup per request). Sessions are listed by family with a readable device name from the user agent. Turning two-step on and changing the password sign out every other session. Re-checks of a password or code by a signed-in user fail with 403, not 401, so the client never mistakes a typo for an expired session. QR codes are rendered server-side as SVG with `segno`. CI gains a dependency audit job (pip-audit, `npm audit` for runtime packages at high and above).
- **Consequences:** Turning off two-step, regenerating codes and changing the password require proof (password and code, or a code). A user who loses both their phone and their recovery codes has no self-service way back in; account recovery by email is a later step. Access tokens issued before this change have no `sid` and keep their old behaviour until they expire. The demo account can enable two-step like any other account.

## ADR-030: Email: verification, password reset, security alerts

- **Date:** 2026-10-03
- **Status:** Accepted
- **Context:** MedSpace sent no email, so a forgotten password locked a password-only account out for good, and nothing proved an account owned its address. That left two real holes: care circle invitations are bound to an email address, so anyone could register someone else's address and accept an invitation meant for them; and "Continue with Google" linked a verified Google identity into an existing password account without asking who set that password (account pre-hijacking).
- **Decision:** A mail port (`app/shared/mail.py`) with an SMTP adapter (stdlib `smtplib` in a thread; STARTTLS, implicit TLS or none) and a fake that keeps an in-memory outbox; `MAIL_PROVIDER=auto` picks SMTP when `SMTP_HOST` is set. Outside production a dev-only `GET /api/dev/outbox` shows simulated mail, which local testing and e2e use. A `notify` module owns the wording: plain text plus a small HTML version, never any health information, and nothing is sent to demo addresses (demo accounts are open to anyone, so they must not be a relay). One-time links use an `email_tokens` table: SHA-256 of a random token, purpose (`verify` or `reset`), the address it was sent to (changing the email voids it), expiry (48 hours to confirm, 30 minutes to reset) and `used_at`; issuing a new link retires older ones. Signup sends a confirmation link; until then an app banner offers to resend it. Forgot password always answers 202, is limited per IP and quietly to three links per address per hour, and sends from a background task after the response so timing doesn't reveal which addresses exist. Resetting sets the password, confirms the address, signs out every session and sends an alert, but doesn't bypass two-step verification. Password changes and turning two-step on or off also send alerts. Accepting a care circle invitation now requires a confirmed address. When Google links into an account whose address was never confirmed, that account's password, two-step setup and sessions are removed ("reclaimed", audited) because whoever set them never proved they own the address. Token-carrying routes (verify, forgot, reset) are exempt from the CSRF check like sign-in, since the emailed token is the proof. Existing Google-linked and demo accounts are marked confirmed by the migration.
- **Consequences:** Real deployments need SMTP credentials (any provider: Postmark, SES, Resend, Mailgun); without them everything still works and mail is simulated. Accounts created before this change must confirm their address before accepting invitations. Losing both the authenticator and the recovery codes still has no self-service path; an email reset of two-step verification would make the inbox a single factor, so it stays manual. Changing the account email isn't offered yet (added in ADR-033).

## ADR-031: Evidence highlights from the PDF text layer

- **Date:** 2026-10-03
- **Status:** Accepted
- **Context:** Reviewing a draft meant reading the page and the form side by side and finding each value by eye. Every item already recorded its page; nothing recorded where on the page. ADR-015 left page previews as images partly so boxes could be drawn on them later.
- **Decision:** `extraction/evidence.py` locates each value in the original PDF's text layer with PyMuPDF's `search_for` and returns boxes as fractions of the page, which overlay the rendered preview at any size and zoom. Values are searched literally as they were read, then with fallbacks (shorter word prefixes for wrapped notes, "Dr." dropped, ";" read back as ","), preferring the item's page. Fields of one item (a medicine line, a lab row) are anchored on its name: a value printed more than once ("500 mg", "mg/dL") resolves to the occurrence on the anchor's line; letterhead fields aren't anchored. Reader-written care-action titles fall back to the copied note and distinctive words. Results are keyed by review-form path ("medications.0.strength") plus one box set per item, computed on first request by `GET /documents/{id}/evidence` and cached on the extraction (`extractions.evidence`, versioned so an improved locator recomputes). In the review workspace, focusing a field highlights its spot (falling back to its whole line) with a marker-style box, switches page and scrolls only the viewer; each item carries its original position so removing or adding items while reviewing doesn't misalign highlights. Fields with nothing to show clear the highlight; the "p.N" button explains why when nothing is marked.
- **Consequences:** No model calls, no new dependency, and highlights are exact for PDFs with text. Photos and scans have no text layer and get no highlights (the viewer says so); OCR with word positions would be the way to add them. Values a reader paraphrased rather than copied can't be found and are simply not marked, never guessed. Highlights cover the review workspace. *Update (Phase 21):* confirmed records now keep a `source_ref` to the item they were read from (sent by the review form, which tracks original positions; validated against a strict pattern), and their "Source" links open the document with that line highlighted, resolved in the confirmed reading (`?confirmed=true`) so a later re-read can't misplace it. Records confirmed before this have no reference and open on their page without a highlight.

## ADR-032: Dose alerts for caregivers

- **Date:** 2026-10-04
- **Status:** Accepted
- **Context:** Helpers can tick doses for someone they look after (ADR-026), and owners get reminders on their own devices (ADR-028), but a caregiver had no way to know a dose was due or still open without opening the app.
- **Decision:** The caregiver opts in per person, on the care link (`care_links.alert_minutes`): off (the default), when a dose is due, or if it isn't ticked 30 or 60 minutes after it was due. The setting belongs to the caregiver (only they can change it, `PUT /circle/{id}/alerts`); the owner sees it on their circle list and in their activity log, so nobody is told about someone's doses invisibly. The minute tick reuses the owner's due-dose logic with a shift (owners: minus their lead time; caregivers: plus the delay), in the owner's timezone, skipping doses already ticked, so "not ticked yet" alerts only go out for doses still open. Each link hears about each dose once (`caregiver_reminder_logs`, claimed atomically like the owner's log). Alerts go to the caregiver's own devices and respect their own "reminders off" switch. Viewers get the alert only; helpers also get Taken / Skip, whose token names the link and the caregiver and is re-checked when used, so revoking access (or demoting to viewer) also disables buttons on alerts already delivered; such changes are audited in the owner's log like any helper change. Tapping an alert opens `/app?for=<owner>`, which switches to that person's records only if the signed-in user actively helps them. Wording never says "missed" (ADR-021): an unticked dose may simply not be logged.
- **Consequences:** Families get a gentle nudge without anyone giving the caregiver more access than they already had. Alerts can't be addressed to someone who isn't a caregiver, and there is no escalation chain (several caregivers each choose for themselves). Email or SMS alerts aren't offered; push needs a device with reminders turned on.

## ADR-033: Changing the account email

- **Date:** 2026-10-05
- **Status:** Accepted
- **Context:** The sign-in address couldn't be changed. It is also the reset channel (ADR-030), so a stolen session that could change it silently would turn a temporary compromise into a permanent takeover.
- **Decision:** `POST /me/email/change` needs fresh proof: the current password, plus a code when two-step verification is on. Accounts without a password (Google-only) add one first; demo accounts can't change. The address must be free. Nothing changes yet: a one-time link (an `email_tokens` row of purpose `change`, pinned to the new address, 24 hours) goes to the new inbox, and the current address is told a change was requested so a real owner can react. Opening the link (any browser, CSRF-exempt because the token is the proof) re-checks the address is still free, moves the account, marks it confirmed, voids every outstanding link sent to the old address, audits the change and tells the old address it happened. Settings shows a pending change, which can be cancelled or replaced.
- **Consequences:** A takeover needs the password (and the second factor when on), and the owner's inbox hears about it twice. An attacker who already knows the password and controls the session can still move the account, but not quietly. There is no "undo" link in the notice to the old address; recovery stays a password reset plus signing out other devices, which the notice points to.

## ADR-034: Two editions from one codebase (free hosted, full with OCR)

- **Date:** 2026-10-07
- **Status:** Proposed (to be built in Phase 25)
- **Context:** Highlights and offline extraction don't work for photos and scans: they need OCR with word positions (ADR-031). Tesseract needs about 1 GB of memory and real CPU to be usable, while the free hosting target (one ~512 MB container with a fraction of a CPU, ADR-001's inline mode) can't spare either. The project should stay hostable for free and still show the full feature set.
- **Decision:** One codebase on `main`, no long-lived feature branch. OCR is a port like the others (`app/shared/ocr.py`), chosen by `OCR_PROVIDER`: `none` (the free hosted edition, today's behaviour) or `tesseract` (the full edition, via PyMuPDF's Tesseract integration). The full edition runs OCR in the ARQ worker with Redis, never in the request path, so slow pages can't block the API. OCR word boxes are stored per page and feed the existing evidence locator, global search and the offline extractor. OCR highlights only mark words above a confidence threshold and use a distinct "approximate" style. A synthetic photo corpus (generated sample documents, rotated, blurred and noised) measures OCR accuracy in the evaluation harness and CI.
- **Consequences:** The free deployment is unchanged and stays within free tiers. The full edition needs a worker, Redis and about 1 GB of memory (a small paid server, or `docker compose up` locally), and its image is roughly 30 to 60 MB larger. Both editions are tested in CI. The README describes both and links the live free edition.

## ADR-035: Hardening for a public deployment

- **Date:** 2026-10-07
- **Status:** Accepted
- **Context:** Before the first public deployment, a security and data-integrity review looked for gaps that tests of individual features would not catch. It found: production would start with the development JWT secret and no encryption key if those variables were forgotten; the server POSTs to any push endpoint a user registers (a server-side request forgery path, e.g. to cloud metadata addresses); share and invitation tokens appeared in request logs (ours and uvicorn's access log); image uploads were limited in bytes but not in pixels, so a small file could decode to gigabytes; oversized request bodies were spooled to disk before the size check; the public demo had per-IP limits but no overall cap; and the web app sent no Content-Security-Policy.
- **Decision:**
  - Settings refuse to load in production unless the JWT secret is random and at least 32 characters, `TOKEN_ENCRYPTION_KEY` is set, cookies are secure, the frontend URL and CORS origins are https (no `*`) and storage is S3.
  - Push endpoints must belong to a browser push service (FCM, Mozilla, WNS, Apple), matched by exact host or dot-suffix.
  - Request logs redact share and invitation tokens; uvicorn runs with `--no-access-log` everywhere.
  - Images are checked from their headers before decoding: at most 40 megapixels and 12,000 px per side. Page rendering caps each side at 4,000 px.
  - A pure ASGI middleware rejects bodies over the upload limit plus 1 MB as they stream in (declared or chunked) with a 413.
  - Demo sign-ups are capped at 400 live demo users overall and 20 per IP per hour, answering 503 "busy" past the cap.
  - The web app sends a strict CSP (`script-src 'self'`, no inline script, `frame-ancestors 'none'`), `X-Frame-Options`, `nosniff`, `Referrer-Policy`, `Permissions-Policy` and COOP, defined once in `frontend/deploy/security-headers.js` and copied into `vercel.json` and the nginx template; a unit test fails if a copy drifts, and `vite preview` sends them so e2e runs under the real policy. The theme script moved from inline to `/theme-init.js`, and Zod runs `jitless` so it never probes `Function()`.
  - An authorization sweep test enumerates every ID-taking route from the OpenAPI schema and proves another account's IDs get 403/404 and change nothing.
- **Consequences:** A misconfigured production deploy fails at start-up with a list of what to fix, instead of running insecurely. Inline styles stay allowed (motion sets them); a future inline script or third-party origin needs a CSP change and fails the e2e run until then. Residual risks are documented in the launch guide: a crafted PDF with huge embedded images can still use a lot of memory during rendering (bounded by the page and size caps), and hosting providers' own request logs record share URLs.

## ADR-036: Real Google OAuth for accounts, the simulation for demos

- **Date:** 2026-10-07
- **Status:** Accepted
- **Context:** Google Calendar and Tasks are a core MedSpace flow (upload, extract, confirm, schedule, then reminders in Calendar and to-dos in Tasks), so the hosted deployment must use real Google. Until Google verifies the app, its OAuth consent screen stays in Testing: only listed test users can connect, and their refresh tokens expire after 7 days. The simulation was chosen server-wide (`GOOGLE_PROVIDER`), and silently stood in if credentials were missing. That left three problems once real Google is on: public demo visitors would hit Google's "access blocked" page, a tester connecting a demo account would get fake events in a real calendar that outlive the 24-hour demo, and a misconfigured production server would quietly simulate. Deleting an account also left the grant listed in the user's Google account.
- **Decision:**
  - Production uses `GOOGLE_PROVIDER=google` with real OAuth 2.0 (authorization code, PKCE S256, `access_type=offline`), scopes `openid email profile calendar.events tasks`. Settings refuse to start in production when `GOOGLE_PROVIDER=google` lacks a client ID or secret.
  - The client is chosen per use, not once per server: real accounts use live Google when configured; demo accounts always use the simulation. Each connection records the client that issued its tokens (`oauth_connections.mode`), and every later call (refresh, sync, pull, revoke) goes to that same client, so a simulated grant never reaches Google and a live one never falls back to the simulation. The signed OAuth state carries the client used, so the callback finishes with the client that started.
  - `GOOGLE_OAUTH_TESTING=true` tells the UI the app is in Testing; the Google buttons say access is open to invited testers. Expired testing grants already surface as "Reconnect needed".
  - Deleting an account disconnects Google first, revoking the grant.
  - The simulation stays for development without credentials and for demo accounts.
- **Consequences:** Testers get real Calendar events and Tasks; everyone else still sees the full flow through the demo. Testers reconnect weekly until the app is verified; publishing the app needs no code change (`GOOGLE_OAUTH_TESTING=false`). The production client is now tested at the HTTP level against a mocked Google (request shapes, PKCE, token refresh and revocation, sync calls).
