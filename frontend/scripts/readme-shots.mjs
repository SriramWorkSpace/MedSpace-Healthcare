// Captures the screenshots used in the README. Run against a live stack:
//   node scripts/readme-shots.mjs ../docs/screenshots
import { chromium } from "@playwright/test";

const out = process.argv[2] ?? "../docs/screenshots";
const base = process.env.BASE_URL ?? "http://localhost:5173";
const browser = await chromium.launch();

async function context(theme = "light", viewport = { width: 1440, height: 900 }) {
  // A daytime zone keeps the greeting friendly regardless of when the shots are taken.
  return browser.newContext({
    viewport,
    colorScheme: theme,
    deviceScaleFactor: 1,
    timezoneId: "Pacific/Honolulu",
  });
}

async function demo(page) {
  await page.goto(base + "/login");
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
}

const settle = (page, ms = 1600) => page.waitForTimeout(ms);

for (const theme of ["light", "dark"]) {
  const ctx = await context(theme);
  const page = await ctx.newPage();
  await page.goto(base + "/");
  await settle(page, 6800); // let the hero preview reach its final state
  await page.screenshot({ path: `${out}/landing-${theme}.png` });
  await ctx.close();
}

{
  const ctx = await context();
  const page = await ctx.newPage();
  await demo(page);
  await settle(page, 2200);
  await page.screenshot({ path: `${out}/dashboard.png` });

  // The review workspace on the demo's pending prescription.
  await page.locator('a[href^="/app/documents/"]', { hasText: "Review" }).first().click();
  await settle(page, 2200);
  await page.screenshot({ path: `${out}/review.png` });

  await page.goto(base + "/app/timeline");
  await settle(page);
  await page.screenshot({ path: `${out}/timeline.png` });

  await page.goto(base + "/app/labs/ldl-cholesterol");
  await settle(page);
  const chart = page.getByRole("img", { name: /LDL cholesterol/ });
  const box = await chart.boundingBox();
  if (box) await page.mouse.move(box.x + box.width / 2 - 30, box.y + box.height / 2);
  await settle(page, 400);
  await page.screenshot({ path: `${out}/labs.png` });

  await page.mouse.move(0, 0);
  await page.keyboard.press("Control+k");
  await page.getByRole("combobox").fill("chol");
  await settle(page, 900);
  await page.screenshot({ path: `${out}/search.png` });
  await page.keyboard.press("Escape");

  await page.goto(base + "/app/ask");
  await settle(page, 800);
  await page.getByRole("button", { name: "How often do I take Amoxicillin?" }).click();
  await settle(page, 3000);
  await page.locator("#ask-input").fill("When is my next follow-up?");
  await page.keyboard.press("Enter");
  await settle(page, 3000);
  await page.screenshot({ path: `${out}/ask.png` });

  await page.goto(base + "/app/timeline");
  await settle(page, 800);
  await page.locator('a[href^="/app/prescriptions/"]').first().click();
  await settle(page);
  const reportUrl = page.url();
  await page.getByRole("button", { name: "Add to Google" }).click();
  await settle(page, 800);
  await page.getByRole("button", { name: "Connect Google" }).click();
  await page.waitForURL("**/app/settings**");
  await page.goto(reportUrl);
  await settle(page);
  await page.screenshot({ path: `${out}/report.png` });
  await ctx.close();
}

{
  const ctx = await context("dark");
  const page = await ctx.newPage();
  await demo(page);
  await settle(page, 2200);
  await page.screenshot({ path: `${out}/dashboard-dark.png` });
  await ctx.close();
}

{
  const ctx = await context("light", { width: 390, height: 844 });
  const page = await ctx.newPage();
  await page.goto(base + "/");
  await settle(page, 6800);
  await page.screenshot({ path: `${out}/mobile-landing.png` });
  await demo(page);
  await settle(page, 2000);
  await page.screenshot({ path: `${out}/mobile-dashboard.png` });
  await page.getByRole("button", { name: "Open menu" }).click();
  await settle(page, 700);
  await page.screenshot({ path: `${out}/mobile-menu.png` });
  await ctx.close();
}

await browser.close();
console.log(`Screenshots written to ${out}`);
