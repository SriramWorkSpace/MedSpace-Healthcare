# Launch guide: the steps only you can do

Everything in the code is done. What's left needs your accounts, secrets and decisions. Work
through these in order; each part says why it matters, what to do, and how to check it worked.
Technical reference for every setting: [deployment.md](deployment.md).

**Everything here is free.** No domain, no paid plan. The site lives at a free
`your-project.vercel.app` address. The only card request you may see is Cloudflare asking for one
to activate R2; usage stays inside the free allowance.

**Region:** Render **Singapore** and Neon **AWS Asia Pacific (Singapore)**, side by side so the
API and database talk quickly.

**Never paste a password, key, client secret or connection string into a chat, an issue or a
commit.** They go into a password manager and into Render's or Vercel's environment settings,
nowhere else. `.gitignore` blocks `.env` files and Google's downloaded `client_secret*.json`.

The plan has two editions from the same code (ADR-034):

| | Free edition (hosted) | Full edition (Phase 25) |
|---|---|---|
| Where | A public URL anyone can try | `docker compose up` locally, or a small paid server |
| OCR for photos | Off (`OCR_PROVIDER=none`) | On (`OCR_PROVIDER=tesseract`) |
| Cost | $0 | $0 locally |

Free-tier limits change. Check each provider's current pricing page before you rely on a limit
mentioned here.

---

## Part 1. Accounts to create (about 30 minutes)

Use **Sign in with GitHub** wherever it's offered, and turn on two-factor authentication on
every account.

| Service | Used for | Notes |
|---|---|---|
| [Vercel](https://vercel.com) | The web app | Hobby plan; let it access the MedSpace repo |
| [Render](https://render.com) | The API container | Free web service, no card |
| [Neon](https://neon.tech) | Postgres with pgvector | Create a project `medspace`, region **AWS Asia Pacific (Singapore)**, Postgres 17 |
| [Cloudflare](https://dash.cloudflare.com) | R2 file storage | May ask for a card to activate R2; the free allowance covers this project |
| A new Gmail account | Sending MedSpace's emails | e.g. `medspace.mail.yourname@gmail.com`; turn on 2-Step Verification (needed in Part 5) |
| [Google Cloud](https://console.cloud.google.com) | Google Calendar and Tasks sign-in | Your own Google account; no billing account needed |
| [Groq](https://console.groq.com) | AI extraction and Ask MedSpace | Free API key with rate limits |

---

## Part 2. Generate your secrets (5 minutes, on your computer)

From `backend/` with the virtual environment active:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"                               # JWT_SECRET
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"  # TOKEN_ENCRYPTION_KEY
python -m app.shared.push                                                                   # VAPID keys
```

Save the outputs in a password manager. Never commit them. Keep `TOKEN_ENCRYPTION_KEY` and the
VAPID keys stable forever: changing the first makes stored Google tokens and two-step secrets
unreadable, changing the second breaks every device's reminder subscription.

---

## Part 3. Database: Neon (10 minutes)

1. In the `medspace` project (Singapore), open **Connect** and copy the connection string.
2. Change its start from `postgresql://` to `postgresql+asyncpg://`, and replace everything
   after `?` with `ssl=require` (the driver doesn't accept `sslmode` or `channel_binding`).
   This is your `DATABASE_URL`.
3. Nothing else: migrations run automatically when the API starts and create the `vector`
   extension.

**Check:** the API's `/api/ready` returns `{"status": "ready"}` once it's deployed (Part 6).

---

## Part 4. File storage: Cloudflare R2 (10 minutes)

1. R2, then **Create bucket**, e.g. `medspace-documents`, location hint **Asia-Pacific**. Keep it
   private; files always stream through the API.
2. **Manage R2 API tokens**, then create a token with object read and write on that bucket only.
3. Note the account ID (for the endpoint), access key and secret key.

Settings: `STORAGE_PROVIDER=s3`, `S3_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com`,
`S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET=medspace-documents`, `S3_REGION=auto`.

---

## Part 5. Email through Gmail (10 minutes)

Without email, nobody can confirm an address, reset a forgotten password or change their email.
Gmail's SMTP server is free (about 500 emails a day) and reaches inboxes well.

1. Sign in to the new sending Gmail (Part 1). 2-Step Verification must be on.
2. Open [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords), create an
   app password named `MedSpace`, and copy the 16 characters (without spaces). It only allows
   sending mail as this account, and you can revoke it there at any time.
3. Settings: `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_SECURITY=starttls`,
   `SMTP_USERNAME=<the sending Gmail address>`, `SMTP_PASSWORD=<the app password>`,
   `MAIL_FROM=MedSpace <the sending Gmail address>`.

**Check (after Part 7):** sign up on the live site with your personal email; the confirmation
email arrives. If it's in spam the first time, mark it "Not spam".

---

## Part 6. The API on Render (20 minutes)

1. **New, then Web Service**, connect the GitHub repo.
2. Root directory `backend`, runtime **Docker**, region **Singapore**, instance type **Free**.
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
   | `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT` | from Part 2; subject `mailto:<the sending Gmail>` |
   | `LLM_PROVIDER`, `GROQ_API_KEY` | `groq` and your key (Part 8) |
   | Google | added in Part 9 |

You don't need the Vercel URL before Part 7: deploy, create the web app, then come back and set
`FRONTEND_URL`, `PUBLIC_API_URL` and `CORS_ORIGINS`.

If the API won't start and its log says **Unsafe production settings**, it lists exactly which
variables to fix. That's deliberate: production never runs with development secrets.

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

**Check:** open the site, click **Try the demo**, and the dashboard loads with sample data. Ask
MedSpace streams its answer word by word (if it arrives all at once, the rewrite is buffering;
it still works). Upload a sample PDF of a few MB to confirm uploads pass through the rewrite.
Open the browser's developer tools console: no red "Content Security Policy" messages.

---

## Part 8. AI: Groq (5 minutes)

1. Create an API key at console.groq.com.
2. On Render: `LLM_PROVIDER=groq`, `GROQ_API_KEY=...`.

Without it the site still works with the built-in offline extractor, which handles typed
prescriptions well. Groq makes photo uploads and Ask MedSpace much better.

---

## Part 9. Google Calendar and Tasks (30 minutes)

MedSpace connects to Google with OAuth 2.0 (authorization code with PKCE). Confirmed medication
schedules become recurring Google Calendar reminders, and to-dos become Google Tasks. MedSpace
asks only for `calendar.events` (its own events, not your whole calendar settings) and `tasks`.

The OAuth app stays in Google's **Testing** status, which is free and needs no review: only the
test users you list (up to 100) can connect. Demo accounts always use a built-in simulation, so
recruiters trying the demo still see the whole flow, and nothing fake lands in a real calendar.

**1. Project and APIs**
1. [console.cloud.google.com](https://console.cloud.google.com), signed in with your own Google
   account: project picker, then **New project**, name `MedSpace`. No billing account needed.
2. **APIs & Services**, then **Library**: enable **Google Calendar API** and **Google Tasks API**.

**2. Consent screen** (Google Auth Platform in the left menu)
1. **Branding:** app name `MedSpace`, user support email and developer contact = your email.
   Leave the logo empty (a logo triggers a brand review).
2. **Audience:** user type **External**, publishing status **Testing**. Under **Test users**,
   add your own Gmail and anyone else who should be able to connect.
3. **Data access:** **Add or remove scopes**, then tick `openid`, `.../auth/userinfo.email`,
   `.../auth/userinfo.profile`, `.../auth/calendar.events` and `.../auth/tasks`. Save.

**3. OAuth client**
1. **Clients**, then **Create client**: application type **Web application**, name `MedSpace web`.
2. **Authorized redirect URIs**, add exactly (your Vercel URL, no trailing slash):
   `https://YOUR-SITE.vercel.app/api/integrations/google/callback`
3. Create. Copy the **Client ID** and **Client secret** straight into Render (next step). Don't
   download the JSON file; if you do, delete it, and never put it in the repo folder.

**4. On Render**, add and redeploy:

| Variable | Value |
|---|---|
| `GOOGLE_PROVIDER` | `google` |
| `GOOGLE_CLIENT_ID` | the client ID |
| `GOOGLE_CLIENT_SECRET` | the client secret |
| `GOOGLE_OAUTH_TESTING` | `true` |
| `PUBLIC_API_URL` | your Vercel URL (already set in Part 6; the redirect URI is built from it) |

**Check:**
1. Sign up on the live site with the Gmail you listed as a test user (not the demo).
2. Upload a sample prescription from `samples/`, review it, confirm.
3. Settings, **Google Calendar & Tasks**, **Connect Google**. Google shows "Google hasn't
   verified this app": that's expected in Testing; choose **Continue**, then allow access.
4. Open the prescription and **Add to Google**. Dose reminders appear in Google Calendar, and a
   **MedSpace** list appears in Google Tasks.

**Good to know**
- In Testing, Google expires each tester's access after 7 days. MedSpace notices and shows
  **Reconnect needed** in Settings; one click reconnects.
- People not on the test-user list see Google's "access blocked" page. The site says so next to
  the Google buttons. Email sign-up and the demo work for everyone.
- To open Google to everyone later, publish the app and complete Google's verification (free,
  but it needs a privacy policy page and a short video, and takes a few weeks).
- If the client secret ever leaks, open the client in Google Cloud, add a new secret, update
  Render, then delete the old secret.

---

## Part 10. Keep reminders working on the free plan (5 minutes)

Render's free instance sleeps after about 15 idle minutes, and a sleeping API can't send dose
reminders. A free uptime monitor such as [cron-job.org](https://cron-job.org) or UptimeRobot
calling `https://YOUR-SITE.vercel.app/api/health` every 10 minutes keeps it awake. One
always-on service fits inside Render's monthly free hours (check the current allowance).

---

## Part 11. Final checks (15 minutes)

Run through the checklist at the end of [deployment.md](deployment.md). The ones that matter
most:

- [ ] `/api/ready` is ready; **Try the demo** works.
- [ ] Sign up with your real email: the confirmation email arrives; **Forgot password?** works.
- [ ] Upload a sample PDF from `samples/`; it reaches "Needs review" and highlights work.
- [ ] A test user connects Google and a confirmed prescription appears in Calendar and Tasks.
- [ ] Turn on reminders on your phone (Settings, This device), send a test notification.
- [ ] `/api/dev/outbox?to=x` returns 404 (the dev outbox is off in production).

### Keep the data safe

- **Backups:** Neon's free plan keeps only a short restore window. Every few weeks, export a
  copy: `pg_dump "<your Neon URL, starting postgresql://>" -Fc -f medspace.dump`, and keep
  it somewhere private.
- **Secrets:** if a secret ever leaks (pasted in a chat, committed by mistake), rotate it at
  the provider and on Render. A new `JWT_SECRET` signs everyone out; keep
  `TOKEN_ENCRYPTION_KEY` stable (see Part 2).
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
   (`fastapi`, `react`, `pgvector`, `rag`, `healthcare`, `pwa`, `oauth2`).
3. **Clip:** record 60 to 90 seconds of upload, review, confirm, then the reminders appearing in
   Google Calendar; link it from the README.
4. **Resume bullets** (adapt the numbers if they change):
   - Built MedSpace, a full-stack health records app (FastAPI, PostgreSQL with pgvector, React)
     that turns prescription PDFs and photos into reviewable records, reminders and
     source-cited answers.
   - Integrated Google Calendar and Tasks over OAuth 2.0 with PKCE: confirmed schedules sync as
     recurring reminders, idempotently, with encrypted tokens, refresh and revocation.
   - Designed a review workflow with evidence highlights that locate every extracted value on
     the source page; extraction accuracy is measured on a labelled corpus and gated in CI.
   - Implemented production security: two-step verification (RFC 6238), session-bound tokens
     with instant sign-out, rate limiting, a strict CSP, and email-verified account recovery.
   - Shipped an installable PWA with offline access and Web Push dose reminders, verified by
     300+ backend, 34 unit and 41 end-to-end tests with WCAG 2.1 AA scans in CI.
5. **Interview story:** the two-editions decision (ADR-034) and the Google client routing
   (ADR-036: real OAuth for accounts, a simulation for the public demo) are good ones to tell.

---

## Housekeeping

- `logo.jpg` and `logo-removebg-preview.png` in the repo root are untracked originals; the app
  uses the copies in `frontend/public/brand/`. Delete them or move them out of the repo.
- `backend/uv.lock` is untracked on purpose; the project installs from `pyproject.toml`.
