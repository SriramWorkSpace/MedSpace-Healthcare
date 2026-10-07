# Launch guide: the steps only you can do

Everything in the code is done. What's left needs your accounts, secrets and decisions. Work
through these in order; each part says why it matters, what to do, and how to check it worked.
Technical reference for every setting: [deployment.md](deployment.md).

**Everything here is free.** No domain, no paid plan. The site lives at a free
`your-project.vercel.app` address. The only card request you may see is Cloudflare asking for one
to activate R2; usage stays inside the free allowance.

**Region:** Render **Singapore** and Supabase **Southeast Asia (Singapore)**, side by side so
the API and database talk quickly.

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
| [Supabase](https://supabase.com) | Postgres with pgvector | Free plan; the project itself is created in Part 3 |
| [Cloudflare](https://dash.cloudflare.com) | R2 file storage | May ask for a card to activate R2; the free allowance covers this project |
| A new Gmail account | The address MedSpace's emails come from | e.g. `medspace.mail.yourname@gmail.com`; turn on 2-Step Verification |
| [Brevo](https://www.brevo.com) | Sending email over HTTPS | Free plan, 300 emails a day (Part 5) |
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

## Part 3. Database: Supabase (15 minutes)

Supabase's free Postgres stays on all month. (Neon's free plan counts active hours, and the
every-minute reminder check would use them up mid-month; ADR-038.)

1. **New project:** name `medspace`, region **Southeast Asia (Singapore)**.
2. **Database password:** click **Generate a password**. If it contains anything other than
   letters and digits, generate again (other characters would need escaping in the URL). Save
   it in your password manager as `SUPABASE_DB_PASSWORD`.
3. **Security options:** if asked which connections you'll use, choose **Only Connection
   String**. MedSpace never uses Supabase's Data API, and leaving it on would expose the tables
   over a REST endpoint. If you don't see the option, turn it off after creation:
   **Project Settings**, **Data API**, untick **Enable Data API**.
4. Create the project and wait until it's ready (a minute or two). Don't enable any extensions
   in the dashboard; the API's migrations create `vector` themselves.
5. **Connect** (top of the dashboard), **Connection String** tab, then pick **Session pooler**.
   Not "Direct connection" (IPv6 only on the free plan, which Render can't reach) and not
   "Transaction pooler" (it breaks the database driver). It looks like:
   `postgresql://postgres.abcdefghijkl:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres`
6. Turn it into your `DATABASE_URL`, in your password manager, not in a file:
   - change the start to `postgresql+asyncpg://`
   - replace `[YOUR-PASSWORD]` (brackets included) with the password from step 2
   - add `?ssl=require` at the end

   Result: `postgresql+asyncpg://postgres.abcdefghijkl:PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?ssl=require`

**Check:** the API's `/api/ready` returns `{"status": "ready"}` once it's deployed (Part 6).

---

## Part 4. File storage: Cloudflare R2 (15 minutes)

Uploaded documents live here. The bucket stays private: files only ever stream through the API,
which checks who's asking.

1. Cloudflare dashboard, **R2 Object Storage**. If asked, add a payment method to activate R2;
   the free allowance (10 GB stored) covers this project.
2. **Create bucket:** name `medspace-documents`, location **Automatic** with the hint
   **Asia-Pacific (APAC)**, default storage class **Standard**. Leave **Public access** and the
   `r2.dev` subdomain off, and add no CORS rules.
3. **Manage API tokens** (R2 overview page), **Create Account API token**:
   - name `medspace-api`
   - permissions **Object Read & Write** (not Admin)
   - **Apply to specific buckets only**: `medspace-documents`
   - TTL: forever (or a date you'll remember to rotate it by)
4. Create. Cloudflare shows the **Access Key ID**, the **Secret Access Key** and the S3 endpoint
   **once**. Save all three in your password manager: `S3_ACCESS_KEY`, `S3_SECRET_KEY`, and
   `S3_ENDPOINT_URL` (`https://<account-id>.r2.cloudflarestorage.com`, without the bucket name
   at the end). You don't need the "Token value".

Settings: `STORAGE_PROVIDER=s3`, `S3_ENDPOINT_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`,
`S3_BUCKET=medspace-documents`, `S3_REGION=auto`.

---

## Part 5. Email through Brevo (15 minutes)

Without email, nobody can confirm an address, reset a forgotten password or change their email.
Render's free plan blocks outbound email ports (25, 465, 587), so MedSpace sends through Brevo's
HTTPS API instead (port 443, free, 300 emails a day; ADR-039). The sender is your sending Gmail.

1. Sign up at [brevo.com](https://www.brevo.com) on the free plan and turn on two-factor
   authentication. If Brevo asks for company details, a personal project is fine. New accounts
   are sometimes reviewed before sending is enabled; that can take a day.
2. **Sender:** **Settings**, **Senders, domains & dedicated IPs**, **Senders**, **Add a sender**:
   name `MedSpace`, email = your sending Gmail. Confirm it with the code Brevo emails there.
3. **API key:** **Settings**, **SMTP & API**, **API keys**, **Generate a new API key**, name
   `medspace-render`. It starts with `xkeysib-` (not the `xsmtpsib-` SMTP key). It's shown once:
   save it as `BREVO_API_KEY`.
4. **Authorised IPs:** Brevo blocks API calls from addresses it hasn't seen. After Part 6, copy
   your Render service's **Outbound IP addresses** (its **Connect** menu) into Brevo:
   **Security**, **Authorised IPs**, **Add IP**. If emails still fail with "unrecognised IP",
   Brevo also lets you deactivate the blocking there; then only the API key protects sending, so
   keep it secret.

Settings: `MAIL_PROVIDER=brevo`, `BREVO_API_KEY`, `MAIL_FROM=MedSpace <your sending Gmail>`.

**Honest limit:** without a domain of your own, mail sent "from" a Gmail address through another
service can't pass Gmail's sender checks. Expect some messages in spam, and Brevo may show its own
address as the sender. Links in them work either way. A domain (about $10 a year) would fix it.

**Check (after Part 7):** sign up on the live site with your personal email; the confirmation
email arrives (check spam). Brevo's **Transactional**, **Logs** page shows every send.

---

## Part 6. The API on Render (30 minutes)

The image runs migrations and then starts the API on Render's port by itself, so there's no start
command to paste. It was rehearsed locally at Render's 512 MB limit: about 325 MB idle and 430 MB
at peak while processing documents and rendering pages.

**1. Create the service.** Render dashboard, **New**, **Web Service**, **GitHub**, pick
`MedSpace-Healthcare`, then:

| Field | Value |
|---|---|
| Name | `medspace-api` (it becomes `https://medspace-api.onrender.com`, or with a suffix if taken) |
| Language | **Docker** |
| Branch | `main` |
| Region | **Singapore** |
| Root Directory | `backend` |
| Dockerfile Path | `./Dockerfile` (the default) |
| Instance Type | **Free** |

**2. Environment variables.** **Add from .env** lets you paste them all at once; type the values in
Render's form, never into a file in the repo. You'll fill the Vercel URL in properly in Part 7:
until then use `https://medspace.vercel.app` (it only needs to be an https URL to start).

```
ENV=prod
COOKIE_SECURE=true
FRONTEND_URL=https://medspace.vercel.app
PUBLIC_API_URL=https://medspace.vercel.app
CORS_ORIGINS=https://medspace.vercel.app
QUEUE_MODE=inline
TRUSTED_PROXY_HOPS=2
RATE_LIMIT_BACKEND=memory
EMBEDDING_PROVIDER=fastembed
DATABASE_URL=<secret: Part 3>
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=5
JWT_SECRET=<secret: Part 2>
TOKEN_ENCRYPTION_KEY=<secret: Part 2>
STORAGE_PROVIDER=s3
S3_ENDPOINT_URL=<Part 4>
S3_ACCESS_KEY=<Part 4>
S3_SECRET_KEY=<secret: Part 4>
S3_BUCKET=medspace-documents
S3_REGION=auto
MAIL_PROVIDER=brevo
BREVO_API_KEY=<secret: Part 5>
MAIL_FROM=MedSpace <your sending Gmail>
VAPID_PUBLIC_KEY=<Part 2>
VAPID_PRIVATE_KEY=<secret: Part 2>
VAPID_SUBJECT=mailto:<your sending Gmail>
LLM_PROVIDER=fake
GOOGLE_PROVIDER=fake
```

`LLM_PROVIDER` and `GOOGLE_PROVIDER` change in Parts 8 and 9.

**3. Advanced** (expand it before creating):

| Field | Value |
|---|---|
| Health Check Path | `/api/health` (not `/api/ready`: that one queries the database, and Render calls the health check every few seconds) |
| Auto-Deploy | **On Commit** |
| Build Filters, Included Paths | `backend/**` (commits that only touch the web app or docs don't redeploy the API) |

Leave Docker Command, Pre-Deploy Command and Secret Files empty.

**4. Create Web Service** and watch the **Logs**. The first build takes 5 to 10 minutes (it bakes
the AI search model into the image). A good start ends with `Application startup complete`.
- **Unsafe production settings: ...**: the line lists exactly which variables to fix.
- **Database errors**: recheck `DATABASE_URL` (session pooler, `postgresql+asyncpg://`, password
  filled in, `?ssl=require`).

**Check:** open `https://<your-service>.onrender.com/api/health` (`{"status":"ok"}`), then
`/api/ready` (`{"status":"ready"}`: the database is reachable and migrations ran).

**5. Let Brevo accept the server.** Render service page, **Connect** (top right), **Outbound**: copy
each IP address listed. In Brevo: **Security**, **Authorised IPs**, add each one. If Brevo won't
take Render's addresses, deactivate IP blocking there instead; the API key then protects sending
on its own, so keep it secret.

**6. Send me the service URL** (`https://...onrender.com`; it isn't secret) so `vercel.json` can
point at it, or edit that one line yourself (Part 7).

If Render ever reports the instance ran out of memory, set `EMBEDDING_PROVIDER=hash`: Ask MedSpace
keeps working with slightly less smart search.

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
schedules become recurring reminders in a separate **MedSpace** calendar, and to-dos go to a
**MedSpace** list in Google Tasks. Access is least-privilege (ADR-037):

- "Continue with Google" asks for name and email only.
- Connecting reminders asks for `calendar.app.created` (only calendars MedSpace itself creates,
  never your others) and `tasks`, plus your email to show which account is connected.
- Tokens are encrypted in the database and never reach the browser or the logs.

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
3. **Data access:** **Add or remove scopes**, then tick exactly these five and nothing else:
   `openid`, `.../auth/userinfo.email`, `.../auth/userinfo.profile`,
   `.../auth/calendar.app.created` and `.../auth/tasks`. If `calendar.app.created` isn't in the
   list, paste `https://www.googleapis.com/auth/calendar.app.created` under **Manually add
   scopes**. Save.

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
4. Open the prescription and **Add to Google**. A **MedSpace** calendar appears in Google
   Calendar with the dose reminders, and a **MedSpace** list appears in Google Tasks. Your other
   calendars are untouched.

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

- **Backups:** Supabase's free plan has no backups you can restore. Every few weeks, export a
  copy with Docker (match the image to your project's Postgres version, shown under **Project
  Settings**, **Infrastructure**):
  `docker run --rm -v "${PWD}:/out" postgres:17 pg_dump "<session pooler URL, starting postgresql://, with ?sslmode=require>" -Fc -f /out/medspace.dump`.
  Run it outside the repo folder and keep the file somewhere private: it contains everyone's
  data.
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
