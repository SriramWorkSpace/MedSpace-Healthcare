// Regenerates every README screenshot from a fresh demo account (synthetic data only).
// Run against the production build: `npm run build && npx vite preview`, with the API up, then
//   node scripts/readme-screenshots.mjs [baseUrl] [outDir]
// Defaults: http://localhost:4173 and ../docs/screenshots.
import { chromium } from "@playwright/test";

const base = process.argv[2] ?? "http://localhost:4173";
const out = process.argv[3] ?? "../docs/screenshots";
const DESKTOP = { width: 1440, height: 900 };
const PHONE = { width: 390, height: 844 };

const browser = await chromium.launch();

async function context({ viewport = DESKTOP, theme = "light", mobile = false } = {}) {
  const ctx = await browser.newContext({
    viewport,
    colorScheme: theme,
    deviceScaleFactor: 1,
    isMobile: mobile,
    hasTouch: mobile,
    reducedMotion: "reduce", // settled frames, no half-finished entrances
  });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.log("pageerror:", e.message));
  return { ctx, page };
}

async function demo(page) {
  await page.goto(`${base}/login`);
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
}

/** Wait for data and images to settle, then capture. */
async function shot(page, name) {
  await page.waitForLoadState("networkidle");
  await page.waitForFunction(() => !document.querySelector('[aria-busy="true"]'));
  await page.waitForFunction(() => [...document.images].every((i) => i.complete));
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${out}/${name}.png` });
  console.log("saved", name);
}

const api = async (page, path) => (await page.request.get(`${base}${path}`)).json();

// ---- Public pages --------------------------------------------------------------------------------
{
  const { ctx, page } = await context();
  await page.goto(base);
  await shot(page, "landing-light");
  await ctx.close();
}
{
  const { ctx, page } = await context({ viewport: PHONE, mobile: true });
  await page.goto(base);
  await shot(page, "mobile-landing");
  await ctx.close();
}

// ---- The app, light ------------------------------------------------------------------------------
{
  const { ctx, page } = await context();
  await demo(page);
  await shot(page, "dashboard");

  // Review: a draft with a field focused, its spot highlighted on the page.
  await page.getByRole("link", { name: "Review" }).first().click();
  await page.getByLabel("Strength").first().waitFor();
  await page.getByLabel("Strength").first().focus();
  await page.locator("[data-highlight]").first().waitFor();
  await page.evaluate(() => window.scrollTo(0, 0));
  await shot(page, "review");

  await page.goto(`${base}/app/medications`);
  await shot(page, "medications");

  const meds = await api(page, "/api/medications");
  await page.goto(`${base}/app/medications/${meds[0].id}`);
  await shot(page, "dose-history");

  const labs = await api(page, "/api/labs");
  const ldl = labs.find((l) => /ldl/i.test(l.name)) ?? labs[0];
  await page.goto(`${base}/app/labs/${ldl.key}`);
  await shot(page, "labs");

  const rx = await api(page, "/api/prescriptions");
  await page.goto(`${base}/app/prescriptions/${rx[0].id}`);
  await shot(page, "report");

  const visits = await api(page, "/api/visits");
  await page.goto(`${base}/app/visits/${visits[0].id}`);
  await shot(page, "visit-prep");

  await page.goto(`${base}/app/ask`);
  await page.getByLabel("Ask a question about your records").fill("How often do I take Metformin?");
  await page.keyboard.press("Enter");
  // The answer is done when its source chips ("… p.1") appear.
  await page.locator("button", { hasText: /p\.\d/ }).first().waitFor({ timeout: 30_000 });
  await shot(page, "ask");

  await page.goto(`${base}/app`);
  await page.getByRole("button", { name: /^Search your records/ }).click();
  await page.getByRole("combobox").fill("metf");
  await page.getByRole("option").first().waitFor();
  await shot(page, "search");
  await ctx.close();
}

// ---- Dark theme and phone ------------------------------------------------------------------------
{
  const { ctx, page } = await context({ theme: "dark" });
  await demo(page);
  await shot(page, "dashboard-dark");
  await ctx.close();
}
{
  const { ctx, page } = await context({ viewport: PHONE, mobile: true });
  await demo(page);
  await shot(page, "mobile-dashboard");
  await page.getByRole("button", { name: "Open menu" }).click();
  await page.getByRole("button", { name: "Close menu" }).waitFor();
  await shot(page, "mobile-menu");
  await ctx.close();
}

await browser.close();
