# Deploying MedSpace

A free-tier friendly setup. Every piece is swappable; the only hard requirement is that the
browser reaches the API on the **same origin** as the web app (ADR-014), because auth uses
first-party `SameSite=Lax` cookies.

```mermaid
flowchart LR
  B[Browser] --> W["Static web host<br/>(Vercel / Netlify / nginx image)"]
  W -- "/api/* rewrite" --> A["API container<br/>(Render / Fly / Railway)"]
  A --> P[("Neon Postgres<br/>+ pgvector")]
  A --> S[("Cloudflare R2<br/>S3 API")]
  A -. optional .-> R[("Redis + worker<br/>QUEUE_MODE=arq")]
```

## 1. Database: Neon (or any Postgres 15+ with pgvector)

1. Create a project and copy the connection string.
2. Convert it for asyncpg: `postgresql+asyncpg://USER:PASSWORD@HOST/DB?ssl=require`.
3. Migrations create the `vector` extension automatically (`alembic upgrade head`).

## 2. Object storage: Cloudflare R2 (or AWS S3)

1. Create a bucket, e.g. `medspace-documents`. Keep it **private**; files are always streamed
   through the API (ADR-010).
2. Create an API token with object read/write on that bucket.
3. Set `STORAGE_PROVIDER=s3`, `S3_ENDPOINT_URL=https://<account>.r2.cloudflarestorage.com`,
   `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_REGION=auto`.

## 3. API: one container

Build from `backend/Dockerfile`. Start command:

```bash
sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*'"
```

Environment (see `.env.example` for every option):

| Variable | Value |
|---|---|
| `ENV` | `prod` (enables HSTS) |
| `DATABASE_URL` | Neon URL from step 1 |
| `JWT_SECRET` | `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `TOKEN_ENCRYPTION_KEY` | `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |
| `COOKIE_SECURE` | `true` |
| `FRONTEND_URL` / `PUBLIC_API_URL` | your public web origin, e.g. `https://medspace.example.com` |
| `CORS_ORIGINS` | the same origin |
| `QUEUE_MODE` | `inline` for a single free instance, `arq` with Redis + a worker |
| `EMBEDDING_PROVIDER` | `fastembed` (model downloads once; give the disk ~300 MB) |
| `LLM_PROVIDER` / `GROQ_API_KEY` | optional, for real extraction and answers |
| `GOOGLE_PROVIDER` + client id/secret | optional, see README |

With `QUEUE_MODE=arq`, run a second process from the same image:
`arq app.worker.WorkerSettings` (it also purges expired demo accounts and stale share links).

## 4. Web: static build with an `/api` rewrite

**Vercel / Netlify:** build `frontend/` with `npm run build` (output `dist`) and add a rewrite:

```json
// vercel.json
{ "rewrites": [
  { "source": "/api/(.*)", "destination": "https://YOUR-API-HOST/api/$1" },
  { "source": "/(.*)", "destination": "/index.html" }
] }
```

```text
# netlify: public/_redirects
/api/*  https://YOUR-API-HOST/api/:splat  200
/*      /index.html                       200
```

**Single host:** build `frontend/Dockerfile` with `--target prod`. It serves the SPA with nginx and
proxies `/api` to `API_UPSTREAM` (streaming-friendly for Ask MedSpace's SSE).

## 5. Google OAuth (optional)

Add `https://YOUR-WEB-ORIGIN/api/integrations/google/callback` as an authorized redirect URI and
set `PUBLIC_API_URL` to the web origin so the redirect stays same-origin. Calendar and Tasks
scopes are sensitive: without Google verification, only listed test users can connect.

## Checklist

- [ ] `GET /api/ready` returns `{"status": "ready"}`
- [ ] "Try the demo" lands on a seeded dashboard
- [ ] Uploading a sample PDF reaches "Needs review"
- [ ] Response headers include HSTS and `X-Frame-Options: DENY`
