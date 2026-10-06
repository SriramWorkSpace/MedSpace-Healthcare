# Launch guide: the steps only you can do

Everything in the code is done. What's left needs your accounts, secrets and decisions. Work
through these in order; each part says why it matters, what to do, and how to check it worked.
Technical reference for every setting: [deployment.md](deployment.md).

The plan has two editions from the same code (ADR-034):

| | Free edition (hosted) | Full edition (Phase 25) |
|---|---|---|
| Where | A public URL anyone can try | `docker compose up` locally, or a small paid server |
| OCR for photos | Off (`OCR_PROVIDER=none`) | On (`OCR_PROVIDER=tesseract`) |
| Cost | $0 (plus an optional ~$10/year domain) | $0 locally, ~$5 to $7/month hosted |

Free-tier limits change. Check each provider's current pricing page before you rely on a limit
mentioned here.

---

## Part 1. Accounts to create (about 30 minutes)

| Service | Used for | Notes |
|---|---|---|
| [Neon](https://neon.tech) | Postgres database (with pgvector) | Free plan; no card needed |
| [Cloudflare](https://dash.cloudflare.com) | R2 file storage | Free allowance; R2 may ask for a payment method even on the free tier |
| [Render](https://render.com) | The API container | Free web service: about 512 MB of memory, sleeps after ~15 idle minutes |
| [Vercel](https://vercel.com) | The web app | Free hobby plan; sign in with GitHub |
| [Resend](https://resend.com) or [Brevo](https://www.brevo.com) | Email (SMTP) | See Part 5 for which to pick |
| [Groq](https://console.groq.com) | AI extraction and Ask MedSpace (optional) | Free API key with rate limits |
| A domain (optional) | A tidy URL, and reliable email | About $10/year from Cloudflare, Namecheap or Porkbun |

---

## Part 2. Generate your secrets (5 minutes, on your computer)

From `backend/` with the virtual environment active:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"                               # JWT_SECRET
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"  # TOKEN_ENCRYPTION_KEY
python -m app.shared.push                                                                   # VAPID keys
```

Save the outputs in a password manager. Never commit them. Keep the VAPID keys stable forever:
changing them breaks every device's reminder subscription.

---

## Part 3. Database: Neon (10 minutes)

1. Create a project (pick a region close to where Render will run the API).
2. Copy the connection string and change its start to `postgresql+asyncpg://`, and make sure it
   ends with `?ssl=require`. This is your `DATABASE_URL`.
3. Nothing else: migrations run automatically when the API starts and create the `vector`
   extension.

**Check:** the API's `/api/ready` returns `{"status": "ready"}` once it's deployed (Part 6).

---

## Part 4. File storage: Cloudflare R2 (10 minutes)

1. R2, then **Create bucket**, e.g. `medspace-documents`. Keep it private; files always stream
   through the API.
2. **Manage R2 API tokens**, then create a token with object read and write on that bucket.
3. Note: the account ID (for the endpoint), access key and secret key.

Settings: `STORAGE_PROVIDER=s3`, `S3_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com`,
`S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET=medspace-documents`, `S3_REGION=auto`.

---

## Part 5. Email (15 to 30 minutes)

Without email, nobody can reset a forgotten password, confirm an address or change their email.

**Option A, with a domain (recommended, reliable):** Resend.
1. Add your domain and create the DNS records it shows (SPF, DKIM). Wait until it says verified.
2. Create an API key, then use SMTP: host `smtp.resend.com`, port `587`, username `resend`,
   password = the API key.
3. `MAIL_FROM=MedSpace <no-reply@yourdomain.com>`.

**Option B, no domain (free, but may land in spam):** Brevo.
1. Verify a single sender address (your own email).
2. Use its SMTP credentials (host `smtp-relay.brevo.com`, port `587`).
3. `MAIL_FROM=MedSpace <the-address-you-verified>`. Gmail addresses as senders often go to
   spam; that's the trade-off for not owning a domain.

**Check:** sign up on the live site with your own email; the confirmation email arrives.

---

## Part 6. The API on Render (20 minutes)

1. **New, then Web Service**, connect the GitHub repo.
2. Root directory `backend`, runtime **Docker**, instance type **Free**.
3. Start command:
   ```bash
   sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT --no-proxy-headers --no-access-log"
   ```
4. Health check path: `/api/ready`.
5. Environment variables (full list in [deployment.md](deployment.md)):

   | Variable | Value |
   |---|---|
   | `ENV` | `prod` |
   | `DATABASE_URL` | from Part 3 |
   | `JWT_SECRET`, `TOKEN_ENCRYPTION_KEY` | from Part 2 |
   | `COOKIE_SECURE` | `true` |
   | `FRONTEND_URL`, `PUBLIC_API_URL`, `CORS_ORIGINS` | your Vercel URL (Part 7), e.g. `https://medspace.vercel.app` |
   | `QUEUE_MODE` | `inline` (no worker on the free plan; the API runs reminders and clean-up itself) |
   | `TRUSTED_PROXY_HOPS` | `2` (Vercel's rewrite plus Render's load balancer) |
   | `RATE_LIMIT_BACKEND` | `memory` (one process) |
   | `EMBEDDING_PROVIDER` | `fastembed`; if Render reports out-of-memory restarts, switch to `hash` (Ask still works, slightly less smart) |
   | `OCR_PROVIDER` | `none` (once Phase 25 exists) |
   | Storage | from Part 4 |
   | Email | from Part 5 |
   | `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT` | from Part 2; subject `mailto:you@example.com` |
   | `LLM_PROVIDER`, `GROQ_API_KEY` | `groq` and your key (Part 8), or leave `fake` |
   | `GOOGLE_PROVIDER` | leave `fake` (see Part 9) |

You don't need to fill in `FRONTEND_URL` before Part 7: deploy, create the web app, then come
back and set it.

**Check:** `https://<your-api>.onrender.com/api/ready` returns ready. The first request after
idling takes up to a minute while the free instance wakes; that's normal.

---

## Part 7. The web app on Vercel (15 minutes)

1. In `frontend/vercel.json`, replace `YOUR-API.onrender.com` with your Render host and commit
   it. Leave the `headers` section as it is: it's the site's security policy.
   The rewrite keeps the API on the same origin as the site, which the sign-in cookies need.
2. Vercel, then **Add New Project**, import the repo, root directory `frontend`. Framework
   Vite, build `npm run build`, output `dist`.
3. Deploy, then put the Vercel URL into the Render variables from Part 6 and redeploy the API.
4. Optional: add your domain in Vercel and use it everywhere instead.

**Check:** open the site, click **Try the demo**, and the dashboard loads with sample data. Ask
MedSpace streams its answer word by word (if it arrives all at once, the rewrite is buffering;
it still works). Upload a sample PDF of a few MB to confirm uploads pass through the rewrite.
Open the browser's developer tools console: no red "Content Security Policy" messages.

---

## Part 8. AI: Groq (5 minutes, optional)

1. Create an API key at console.groq.com.
2. On Render: `LLM_PROVIDER=groq`, `GROQ_API_KEY=...`.

Without it the site still works with the built-in offline extractor, which handles typed
prescriptions well. Groq makes photo uploads and Ask MedSpace much better.

---

## Part 9. Google Calendar and Tasks (decide, then 30 minutes if you want it)

For the public demo, **keep `GOOGLE_PROVIDER=fake`**. Calendar and Tasks are sensitive scopes:
until Google verifies your app (a review that can take weeks), only test users you list can
connect. The simulation shows the whole flow to recruiters without that.

If you want it working for your own account:
1. Google Cloud Console: new project, enable **Google Calendar API** and **Google Tasks API**.
2. OAuth consent screen: External, Testing, add yourself as a test user.
3. Credentials: OAuth client ID, type Web application, redirect URI
   `https://YOUR-SITE/api/integrations/google/callback`.
4. On Render: `GOOGLE_PROVIDER=google`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.

---

## Part 10. Keep reminders working on the free plan (5 minutes)

Render's free instance sleeps after about 15 idle minutes, and a sleeping API can't send dose
reminders. A free uptime monitor such as [cron-job.org](https://cron-job.org) or UptimeRobot
calling `https://YOUR-SITE/api/health` every 10 minutes keeps it awake. One always-on service
fits inside Render's monthly free hours (check the current allowance).

---

## Part 11. Final checks (15 minutes)

Run through the checklist at the end of [deployment.md](deployment.md). The ones that matter
most:

- [ ] `/api/ready` is ready; **Try the demo** works.
- [ ] Sign up with your real email: the confirmation email arrives; **Forgot password?** works.
- [ ] Upload a sample PDF from `samples/`; it reaches "Needs review" and highlights work.
- [ ] Turn on reminders on your phone (Settings, This device), send a test notification.
- [ ] `/api/dev/outbox?to=x` returns 404 (the dev outbox is off in production).

If the API won't start and its log says **Unsafe production settings**, it lists exactly which
variables to fix. That's deliberate: production never runs with development secrets.

### Keep the data safe

- **Backups:** Neon's free plan keeps only a short restore window. Every few weeks, export a
  copy: `pg_dump "<your Neon URL, starting postgresql://>" -Fc -f medspace.dump`, and keep
  it somewhere private.
- **Secrets:** if a secret ever leaks (pasted in a chat, committed by mistake), rotate it at
  the provider and on Render. A new `JWT_SECRET` signs everyone out; a new
  `TOKEN_ENCRYPTION_KEY` makes stored two-step secrets and Google tokens unreadable, so keep
  that one stable.
- **Logs:** MedSpace keeps share-link tokens out of its own logs, but Vercel's and Render's
  request logs record full URLs. Don't grant others access to those dashboards.
- **Known limit:** a deliberately crafted PDF with huge embedded images can still use a lot
  of memory while pages render. Sizes and page counts are capped, and Render restarts the
  instance if it runs out.

---

## Part 12. Make it shine on your resume

1. **README:** add the live link at the very top ("Try it live: ...") and a line that the demo
   resets every 24 hours with synthetic data only.
2. **Repository:** pin it on your GitHub profile; set the description, website and topics
   (`fastapi`, `react`, `pgvector`, `rag`, `healthcare`, `pwa`).
3. **Full edition (after Phase 25):** record a 60 to 90 second clip of uploading a phone photo
   and clicking into fields to show the highlights; link it from the README's Editions section.
4. **Resume bullets** (adapt the numbers if they change):
   - Built MedSpace, a full-stack health records app (FastAPI, PostgreSQL with pgvector, React)
     that turns prescription PDFs and photos into reviewable records, reminders and
     source-cited answers.
   - Designed a review workflow with evidence highlights that locate every extracted value on
     the source page; extraction accuracy is measured on a labelled corpus and gated in CI.
   - Implemented production security: two-step verification (RFC 6238), session-bound tokens
     with instant sign-out, rate limiting, audited care-circle access, and email-verified
     account recovery.
   - Shipped an installable PWA with offline access and Web Push dose reminders, verified by
     262 backend, 31 unit and 41 end-to-end tests with WCAG 2.1 AA scans in CI.
5. **Interview story:** the two-editions decision (ADR-034) is a good one to tell: same
   codebase, free hosted deployment, full OCR edition, chosen by configuration.

---

## Housekeeping

- `logo.jpg` and `logo-removebg-preview.png` in the repo root are untracked originals; the app
  uses the copies in `frontend/public/brand/`. Delete them or move them out of the repo.
- `backend/uv.lock` is untracked on purpose; the project installs from `pyproject.toml`.
