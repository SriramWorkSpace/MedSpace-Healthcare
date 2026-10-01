// Dev-only visual check. Usage: node scripts-shot.mjs <outDir> [route...]
import { chromium } from "@playwright/test";
const out = process.argv[2];
const base = "http://localhost:5173";
const browser = await chromium.launch();
async function shot(name, url, { theme = "light", width = 1440, height = 900, full = false, demo = false, wait = 1800, scrollTo } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height }, colorScheme: theme, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.log(`[${name}] pageerror:`, e.message));
  page.on("console", (m) => m.type() === "error" && console.log(`[${name}] console:`, m.text()));
  if (demo) {
    await page.goto(base + "/login");
    await page.getByRole("button", { name: "Try the demo" }).click();
    await page.waitForURL("**/app");
  }
  await page.goto(base + url);
  await page.waitForTimeout(wait);
  if (full) {
    const h = await page.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 500) { await page.evaluate((v) => window.scrollTo(0, v), y); await page.waitForTimeout(120); }
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(800);
  }
  if (scrollTo) { await page.evaluate((y) => window.scrollTo(0, y), scrollTo); await page.waitForTimeout(1200); }
  await page.screenshot({ path: `${out}/${name}.png`, fullPage: full });
  await ctx.close();
}
async function flow(name, theme = "light") {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: theme });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.log(`[${name}] pageerror:`, e.message));
  await page.goto(base + "/login");
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
  await page.goto(base + "/app/documents");
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${out}/documents-empty.png` });
  const input = page.locator('input[type="file"]');
  await input.setInputFiles(["../samples/rx-riverside-acute.pdf", "../samples/rx-northgate-diabetes.pdf", "../samples/rx-riverside-acute-photo.png"]);
  await page.waitForTimeout(700);
  await page.screenshot({ path: `${out}/documents-uploading.png` });
  await page.waitForTimeout(3500);
  await page.screenshot({ path: `${out}/documents-list.png` });
  await page.locator("a").filter({ hasText: "Rx riverside acute" }).filter({ hasNotText: "photo" }).first().click();
  await page.waitForTimeout(2500);
  await page.screenshot({ path: `${out}/review.png` });
  await page.screenshot({ path: `${out}/review-full.png`, fullPage: true });
  await page.getByRole("button", { name: "Confirm records" }).click();
  await page.waitForTimeout(1800);
  await page.screenshot({ path: `${out}/review-confirmed.png` });
  await ctx.close();
}
async function appTour(theme = "light") {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: theme });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.log(`[tour] pageerror:`, e.message));
  await page.goto(base + "/login");
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
  await page.waitForTimeout(1800);
  await page.screenshot({ path: `${out}/${theme}-dashboard.png` });
  for (const [name, path] of [["medications", "/app/medications"], ["timeline", "/app/timeline"]]) {
    await page.goto(base + path);
    await page.waitForTimeout(1500);
    await page.screenshot({ path: `${out}/${theme}-${name}.png` });
  }
  await page.goto(base + "/app/timeline");
  await page.waitForTimeout(800);
  await page.locator('a[href^="/app/prescriptions/"]').first().click();
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${out}/${theme}-report.png`, fullPage: true });
  await ctx.close();
}
async function askTour(theme = "light") {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: theme });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.log(`[ask] pageerror:`, e.message));
  await page.goto(base + "/login");
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
  await page.goto(base + "/app/ask");
  await page.waitForTimeout(1000);
  await page.screenshot({ path: `${out}/ask-empty.png` });
  await page.getByRole("button", { name: "How often do I take Amoxicillin?" }).click();
  await page.waitForTimeout(350);
  await page.screenshot({ path: `${out}/ask-streaming.png` });
  await page.waitForTimeout(2500);
  await page.locator("#ask-input").fill("What medications am I taking right now?");
  await page.keyboard.press("Enter");
  await page.waitForTimeout(3500);
  await page.screenshot({ path: `${out}/ask-answer.png` });
  await ctx.close();
}
async function shareTour(theme = "light") {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: theme });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.log(`[share] pageerror:`, e.message));
  await page.goto(base + "/login");
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
  // Google sync from a report
  await page.goto(base + "/app/timeline");
  await page.waitForTimeout(800);
  await page.locator('a[href^="/app/prescriptions/"]').first().click();
  await page.waitForTimeout(1000);
  const reportUrl = page.url();
  await page.getByRole("button", { name: "Add to Google" }).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: `${out}/sync-connect.png` });
  await page.getByRole("button", { name: "Connect Google" }).click();
  await page.waitForURL("**/app/settings**");
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${out}/settings.png` });
  await page.goto(reportUrl);
  await page.waitForTimeout(1200);
  await page.getByRole("button", { name: "Add to Google" }).click();
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `${out}/sync-preview.png` });
  await page.getByRole("button", { name: "Sync to Google" }).click();
  await page.waitForTimeout(1200);
  await page.keyboard.press("Escape");
  // Share
  await page.getByRole("link", { name: "Share" }).click();
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `${out}/share-create.png` });
  await page.getByRole("button", { name: "Create link" }).click();
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `${out}/share-created.png` });
  const url = await page.locator('input[aria-label="Share link"]').inputValue();
  await page.getByRole("button", { name: "Done" }).click();
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${out}/sharing.png` });
  const anon = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: theme });
  const p2 = await anon.newPage();
  await p2.goto(url.replace("http://localhost:5173", base));
  await p2.waitForTimeout(1800);
  await p2.screenshot({ path: `${out}/shared-view.png`, fullPage: true });
  await anon.close();
  await page.goto(base + "/app/settings#activity");
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${out}/settings-activity.png` });
  await ctx.close();
}
const which = process.argv.slice(3);
const all = {
  "landing-light": () => shot("landing-light", "/", { wait: 6500 }),
  "landing-dark": () => shot("landing-dark", "/", { theme: "dark", wait: 6500 }),
  "landing-full": () => shot("landing-full", "/", { full: true, wait: 2500 }),
  "landing-mobile": () => shot("landing-mobile", "/", { width: 390, height: 844, wait: 6500 }),
  "landing-full-dark": () => shot("landing-full-dark", "/", { full: true, theme: "dark", wait: 2500 }),
  "login": () => shot("login", "/login"),
  "dashboard": () => shot("dashboard", "/app", { demo: true }),
  "review": () => flow("review"),
  "app": () => appTour(),
  "ask": () => askTour(),
  "share": () => shareTour(),
  "app-dark": () => appTour("dark"),
  "notfound": () => shot("notfound", "/nope", { theme: "dark", wait: 2500 }),
};
for (const k of which.length ? which : Object.keys(all)) await all[k]();
await browser.close();
