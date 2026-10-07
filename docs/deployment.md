# Deploying MedSpace

A free-tier friendly setup. Every piece is swappable; the only hard requirement is that the
browser reaches the API on the **same origin** as the web app (ADR-014), because auth uses
first-party `SameSite=Lax` cookies.

```mermaid
flowchart LR
  B[Browser] --> W["Static web host<br/>(Vercel / Netlify / nginx image)"]
  W -- "/api/* rewrite" --> A["API container<br/>(Render / Fly / Railway)"]
  A --> P[("Supabase Postgres<br/>+ pgvector")]
  A --> S[("Cloudflare R2<br/>S3 API")]
  A -. optional .-> R[("Redis + worker<br/>QUEUE_MODE=arq")]
```

## 1. Database: Supabase (or any always-on Postgres 15+ with pgvector)

The API queries the database every minute for due reminders (inline mode), so the database
must not bill by active hours: Neon's free plan (100 CU-hours, about 400 hours a month at the
smallest size) would run out mid-month (ADR-038). Supabase's free plan has no compute-hour
limit and pauses only after 7 days without activity, which the reminder check prevents.

1. Create a project; under connections choose **Only Connection String** (the Data API is
   not used, and turning it off keeps the tables unreachable over Supabase's REST API).
2. Copy the **Session pooler** connection string (IPv4; the direct connection is IPv6-only
   on the free plan, and the transaction pooler breaks asyncpg's prepared statements).
3. Convert it for asyncpg: `postgresql+asyncpg://postgres.REF:PASSWORD@aws-...pooler.supabase.com:5432/postgres?ssl=require`.
4. Set `DB_POOL_SIZE=5` and `DB_MAX_OVERFLOW=5`: the free session pooler allows about 15 clients.
5. Migrations create the `vector` extension automatically (`alembic upgrade head`).

## 2. Object storage: Cloudflare R2 (or AWS S3)

1. Create a bucket, e.g. `medspace-documents`. Keep it **private**; files are always streamed
   through the API (ADR-010).
2. Create an API token with object read/write on that bucket.
3. Set `STORAGE_PROVIDER=s3`, `S3_ENDPOINT_URL=https://<account>.r2.cloudflarestorage.com`,
   `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_REGION=auto`.

## 3. API: one container

Build from `backend/Dockerfile`. Start command:

```bash
sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT --no-proxy-headers --no-access-log"
```

Health check path: `/api/health`, which doesn't touch the database. (`/api/ready` does, and a platform health check polling it every few seconds keeps the database busy for nothing.)

`--no-access-log` matters: uvicorn's access log would write full URLs, including share-link and invitation tokens. MedSpace logs every request itself, with those tokens redacted.

Environment (see `.env.example` for every option):

| Variable | Value |
|---|---|
| `ENV` | `prod` (enables HSTS and turns off the dev email outbox) |
| `DATABASE_URL` | Supabase session pooler URL from step 1 |
| `DB_POOL_SIZE` / `DB_MAX_OVERFLOW` | `5` / `5` (stay under the pooler's client limit) |
| `JWT_SECRET` | `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `TOKEN_ENCRYPTION_KEY` | `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |
| `COOKIE_SECURE` | `true` |
| `FRONTEND_URL` / `PUBLIC_API_URL` | your public web origin, e.g. `https://medspace.example.com` |
| `CORS_ORIGINS` | the same origin |
| `QUEUE_MODE` | `inline` for a single free instance, `arq` with Redis + a worker |
| `EMBEDDING_PROVIDER` | `fastembed` (model downloads once; give the disk ~300 MB) |
| `LLM_PROVIDER` / `GROQ_API_KEY` | optional, for real extraction and answers |
| `GOOGLE_PROVIDER` | `google` for real OAuth 2.0 with `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (production refuses to start without them); `fake` simulates Google. Demo accounts always use the simulation (ADR-036). |
| `GOOGLE_OAUTH_TESTING` | `true` while the consent screen is in Google's Testing status: only listed test users can connect, and the UI says so |
| `TRUSTED_PROXY_HOPS` | number of proxies **you control** that append to `X-Forwarded-For` before the API: `1` behind the bundled nginx or one load balancer, `2` for a CDN rewrite plus a platform load balancer. Wrong values either share one budget across all users (too low) or let clients spoof their IP (too high). |
| `RATE_LIMIT_BACKEND` | `redis` whenever more than one API process runs (limits must be shared); `memory` only for a single process |
| `RATE_LIMIT_SCALE` | leave at `1` in production |
| `VAPID_PUBLIC_KEY` / `VAPID_PRIVATE_KEY` | for dose reminders by notification: generate once with `python -m app.shared.push` and keep them stable (changing them invalidates every device's subscription). Without them reminders are simulated. |
| `VAPID_SUBJECT` | `mailto:` address push services can contact about your traffic |
| `MAIL_PROVIDER` / `BREVO_API_KEY` | `brevo` sends through Brevo's HTTPS API (ADR-039): use it where outbound SMTP ports are blocked, as on Render's free plan. `auto` picks Brevo when a key is set, then SMTP, then the in-memory outbox. |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USERNAME` / `SMTP_PASSWORD` | outgoing mail for confirmation, password reset and security alerts (any provider: Postmark, SES, Resend, Mailgun). `SMTP_SECURITY` is `starttls` (587) or `ssl` (465). Without a host, mail is simulated and nobody can reset a forgotten password. |
| `MAIL_FROM` | sender, e.g. `MedSpace <no-reply@yourdomain>`; set up SPF and DKIM for that domain with your provider |

With `QUEUE_MODE=arq`, run a second process from the same image:
`arq app.worker.WorkerSettings` (it sends dose reminders every minute and purges expired demo accounts and stale share links). In inline mode the API process runs those scheduled jobs itself (reminders every minute, demo purge at :07 and :37, share link purge daily), so a single free container needs no worker.

## 4. Web: static build with an `/api` rewrite

**Vercel:** build `frontend/` with `npm run build` (output `dist`). `frontend/vercel.json` is
committed with the security headers and the rewrites; replace `YOUR-API.onrender.com` in its
`/api` rewrite with your API host. Keep its headers equal to `deploy/security-headers.js` (a unit
test checks).

**Netlify:** add the rewrites below and the same headers in `public/_headers`.

```text
# netlify: public/_redirects
/api/*  https://YOUR-API-HOST/api/:splat  200
/*      /index.html                       200
```

**Single host:** build `frontend/Dockerfile` with `--target prod`. It serves the SPA with nginx and
proxies `/api` to `API_UPSTREAM` (streaming-friendly for Ask MedSpace's SSE).

## 5. Google OAuth

Step by step: [launch-guide.md, Part 9](launch-guide.md#part-9-google-calendar-and-tasks-30-minutes).

Add `https://YOUR-WEB-ORIGIN/api/integrations/google/callback` as an authorized redirect URI and
set `PUBLIC_API_URL` to the web origin so the redirect stays same-origin. Calendar and Tasks
scopes are sensitive: without Google verification, only listed test users can connect.

## Checklist

- [ ] `GET /api/ready` returns `{"status": "ready"}`
- [ ] "Try the demo" lands on a seeded dashboard
- [ ] Uploading a sample PDF reaches "Needs review"
- [ ] Response headers include HSTS and `X-Frame-Options: DENY`
- [ ] The web page's response carries the `Content-Security-Policy` header, and the browser console shows no CSP violations
- [ ] With `ENV=prod`, the API refuses to start if `JWT_SECRET` or `TOKEN_ENCRYPTION_KEY` is missing (the log lists what to fix)
- [ ] API responses carry `RateLimit-Limit` / `RateLimit-Remaining`; eleven quick wrong-password sign-ins to one account return `429` with `Retry-After`
- [ ] Sending a fake `X-Forwarded-For` does not reset a rate limit
- [ ] Signing up delivers a confirmation email; "Forgot password?" delivers a reset link
- [ ] `GET /api/dev/outbox?to=x` returns 404 (dev outbox is off in production)
- [ ] A listed Google test user connects Google, and a confirmed prescription syncs to Calendar and Tasks
