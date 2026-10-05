// Lighthouse audit of the production build (`npm run build && npx vite preview`), signed in as a
// fresh demo account for app pages. Usage: node scripts/lighthouse.mjs [baseUrl] [outDir]
// Writes one JSON report per page and form factor, and prints scores and failed audits.
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { chromium } from "@playwright/test";

const base = process.argv[2] ?? "http://localhost:4173";
const out = process.argv[3] ?? "lighthouse";
mkdirSync(out, { recursive: true });

const PAGES = [
  ["landing", "/", false],
  ["login", "/login", false],
  ["dashboard", "/app", true],
  ["medications", "/app/medications", true],
  ["labs", "/app/labs", true],
];

async function demoCookie() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`${base}/login`);
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
  const cookies = await page.context().cookies();
  await browser.close();
  return cookies.map((c) => `${c.name}=${c.value}`).join("; ");
}

const cookie = await demoCookie();
// A headers file, not inline JSON: shells mangle the quotes (Windows especially).
const headersFile = `${out}/headers.json`;
writeFileSync(headersFile, JSON.stringify({ Cookie: cookie }));
const chrome = chromium.executablePath();
const rows = [];
for (const [name, path, auth] of PAGES) {
  for (const preset of ["mobile", "desktop"]) {
    const file = `${out}/${name}-${preset}.json`;
    const args = [
      "--yes",
      "lighthouse@12",
      `${base}${path}`,
      "--output=json",
      `--output-path=${file}`,
      "--quiet",
      "--only-categories=performance,accessibility,best-practices,seo",
      `--chrome-flags="--headless=new --no-sandbox"`,
      ...(preset === "desktop" ? ["--preset=desktop"] : []),
      ...(auth ? [`--extra-headers=${headersFile}`] : []),
    ];
    execFileSync("npx", args, {
      stdio: "inherit",
      shell: true,
      env: { ...process.env, CHROME_PATH: chrome },
    });
    const report = JSON.parse(readFileSync(file, "utf8"));
    const score = (k) => Math.round((report.categories[k]?.score ?? 0) * 100);
    const failed = Object.values(report.audits)
      .filter((a) => a.score !== null && a.score < 0.9 && a.scoreDisplayMode !== "informative")
      .map((a) => `${a.id}${a.displayValue ? ` (${a.displayValue})` : ""}`);
    rows.push({
      page: `${name} (${preset})`,
      perf: score("performance"),
      a11y: score("accessibility"),
      bp: score("best-practices"),
      seo: score("seo"),
      lcp: report.audits["largest-contentful-paint"]?.displayValue,
      cls: report.audits["cumulative-layout-shift"]?.displayValue,
      failed: failed.join(", "),
    });
  }
}
console.table(rows.map(({ failed: _, ...r }) => r));
for (const r of rows) if (r.failed) console.log(`${r.page}: ${r.failed}`);
