// UI audit: every route x viewport x theme. Records console errors, failed requests, horizontal
// overflow, broken images, axe violations (all severities, incl. best practices) and the
// computed styles of buttons, cards, inputs and headings, so inconsistencies stand out.
// Usage: node scripts/ui-audit.mjs [baseUrl] [outDir]   (dev server or `vite preview`, API up)
import { mkdirSync, writeFileSync } from "node:fs";
import AxeBuilder from "@axe-core/playwright";
import { chromium } from "@playwright/test";

const base = process.argv[2] ?? "http://localhost:5173";
const out = process.argv[3] ?? "ui-audit";
mkdirSync(`${out}/shots`, { recursive: true });

const VIEWPORTS = {
  desktop: { width: 1440, height: 900 },
  laptop: { width: 1024, height: 768 },
  tablet: { width: 768, height: 1024 },
  phone: { width: 390, height: 844, isMobile: true, hasTouch: true },
};
const THEMES = ["light", "dark"];

const browser = await chromium.launch();

// ---- Fixtures: a demo account, IDs to visit, a share link --------------------------------------
const setup = await browser.newContext();
const sp = await setup.newPage();
await sp.goto(`${base}/login`);
await sp.getByRole("button", { name: "Try the demo" }).click();
await sp.waitForURL("**/app");
const storage = await setup.storageState();
const get = async (path) => (await sp.request.get(`${base}${path}`)).json();
const docs = (await get("/api/documents")).items;
const draft = docs.find((d) => d.status === "needs_review");
const confirmed = docs.find((d) => d.status === "confirmed");
const meds = await get("/api/medications");
const labs = await get("/api/labs");
const rx = await get("/api/prescriptions");
const visits = await get("/api/visits");
const csrf = storage.cookies.find((c) => c.name === "ms_csrf")?.value;
const share = await (
  await sp.request.post(`${base}/api/shares`, {
    headers: { "X-CSRF-Token": csrf },
    data: { label: "For Dr. Varga", items: [{ type: "prescription", id: rx[0].id }] },
  })
).json();
await setup.close();

const PAGES = [
  // [name, path, signedIn]
  ["landing", "/", false],
  ["login", "/login", false],
  ["signup", "/signup", false],
  ["forgot", "/forgot-password", false],
  ["reset-expired", "/reset-password?token=expired-token-for-audit-0000", false],
  ["share", `/s/${share.token}`, false],
  ["notfound", "/no-such-page", false],
  ["dashboard", "/app", true],
  ["documents", "/app/documents", true],
  ["review-draft", `/app/documents/${draft.id}`, true],
  ["review-confirmed", `/app/documents/${confirmed.id}`, true],
  ["report", `/app/prescriptions/${rx[0].id}`, true],
  ["medications", "/app/medications", true],
  ["dose-history", `/app/medications/${meds[0].id}`, true],
  ["labs", "/app/labs", true],
  ["lab-detail", `/app/labs/${labs[0].key}`, true],
  ["diet", "/app/diet", true],
  ["timeline", "/app/timeline", true],
  ["visits", "/app/visits", true],
  ["visit-prep", `/app/visits/${visits[0].id}`, true],
  ["ask", "/app/ask", true],
  ["sharing", "/app/sharing", true],
  ["settings", "/app/settings", true],
];

const STYLE_PROBE = () => {
  const pick = (sel, props) =>
    [...document.querySelectorAll(sel)]
      .filter((el) => el.getBoundingClientRect().width > 0)
      .map((el) => {
        const cs = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        return {
          sel,
          text: (el.innerText || el.getAttribute("aria-label") || "").trim().slice(0, 30),
          cls: (el.className?.baseVal ?? el.className ?? "").toString().slice(0, 60),
          h: Math.round(r.height),
          ...Object.fromEntries(props.map((p) => [p, cs[p]])),
        };
      });
  const fonts = new Set();
  for (const el of document.querySelectorAll("body *")) {
    if ([...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()))
      fonts.add(getComputedStyle(el).fontFamily.split(",")[0].replaceAll('"', ""));
  }
  return {
    buttons: pick(".btn", ["borderRadius", "fontSize", "fontWeight", "paddingLeft"]),
    inputs: pick(".input", ["borderRadius", "fontSize", "height"]),
    cards: pick(".card", ["borderRadius", "boxShadow"]),
    headings: pick("h1, h2", ["fontSize", "fontWeight", "letterSpacing"]),
    fonts: [...fonts],
  };
};

const report = [];
for (const [name, path, signedIn] of PAGES) {
  for (const [vpName, vp] of Object.entries(VIEWPORTS)) {
    for (const theme of THEMES) {
      const { isMobile, hasTouch, ...viewport } = vp;
      const ctx = await browser.newContext({
        viewport,
        isMobile,
        hasTouch,
        colorScheme: theme,
        reducedMotion: "reduce",
        storageState: signedIn ? storage : undefined,
      });
      const page = await ctx.newPage();
      const issues = { console: [], requests: [] };
      page.on(
        "console",
        (m) => m.type() === "error" && issues.console.push(m.text().slice(0, 200)),
      );
      page.on("pageerror", (e) => issues.console.push(`pageerror: ${e.message}`.slice(0, 200)));
      page.on("response", (r) => {
        const url = r.url();
        const expected =
          (url.endsWith("/api/auth/session") && r.status() === 401) ||
          (name === "reset-expired" && url.includes("/password/reset"));
        if (r.status() >= 400 && !expected) issues.requests.push(`${r.status()} ${url.slice(-80)}`);
      });
      await page.goto(base + path);
      await page.waitForLoadState("networkidle").catch(() => {});
      await page
        .waitForFunction(() => !document.querySelector('[aria-busy="true"]'), null, {
          timeout: 8000,
        })
        .catch(() => issues.console.push("still loading after 8 s"));
      // Reveal scroll-triggered content, then settle at the top.
      const height = await page.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < height; y += 600) await page.evaluate((v) => window.scrollTo(0, v), y);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(400);

      const layout = await page.evaluate(() => ({
        overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        brokenImages: [...document.images]
          .filter((i) => i.complete && i.naturalWidth === 0)
          .map((i) => i.src.slice(-60)),
      }));
      const axe = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa", "best-practice"])
        .analyze();
      const styles =
        vpName === "desktop" && theme === "light" ? await page.evaluate(STYLE_PROBE) : null;
      const file = `${name}-${vpName}-${theme}.png`;
      await page.screenshot({ path: `${out}/shots/${file}`, fullPage: true });
      report.push({
        page: name,
        viewport: vpName,
        theme,
        ...issues,
        ...layout,
        axe: axe.violations.map((v) => ({
          id: v.id,
          impact: v.impact,
          nodes: v.nodes.length,
          example: v.nodes[0]?.target?.join(" "),
          summary: v.nodes[0]?.failureSummary?.split("\n").slice(0, 2).join(" ").slice(0, 160),
        })),
        styles,
        shot: file,
      });
      process.stdout.write(".");
      await ctx.close();
    }
  }
}
await browser.close();
writeFileSync(`${out}/report.json`, JSON.stringify(report, null, 2));
console.log(`\n${report.length} page views audited -> ${out}/report.json`);
