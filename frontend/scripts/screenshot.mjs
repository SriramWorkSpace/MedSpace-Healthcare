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
const which = process.argv.slice(3);
const all = {
  "landing-light": () => shot("landing-light", "/", { wait: 6500 }),
  "landing-dark": () => shot("landing-dark", "/", { theme: "dark", wait: 6500 }),
  "landing-full": () => shot("landing-full", "/", { full: true, wait: 2500 }),
  "landing-mobile": () => shot("landing-mobile", "/", { width: 390, height: 844, wait: 6500 }),
  "landing-full-dark": () => shot("landing-full-dark", "/", { full: true, theme: "dark", wait: 2500 }),
  "login": () => shot("login", "/login"),
  "dashboard": () => shot("dashboard", "/app", { demo: true }),
  "notfound": () => shot("notfound", "/nope", { theme: "dark", wait: 2500 }),
};
for (const k of which.length ? which : Object.keys(all)) await all[k]();
await browser.close();
