import AxeBuilder from "@axe-core/playwright";
import { expect } from "@playwright/test";

export async function signUp(page, email) {
  const unique = `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
  await page.goto("/signup");
  await page.getByLabel("Name").fill("Mira Castellanos");
  await page.getByLabel("Email").fill(email ?? `mira-${unique}@example.com`);
  await page.getByLabel("Password", { exact: true }).fill("a-long-enough-password");
  await page.getByRole("button", { name: "Create account" }).click();
  await page.waitForURL("**/app");
}

export async function startDemo(page) {
  await page.goto("/login");
  await page.getByRole("button", { name: "Try the demo" }).click();
  await page.waitForURL("**/app");
}

/** Fail on serious or critical WCAG A/AA violations. */
export async function expectAccessible(page, { exclude = [] } = {}) {
  // Scan the settled UI: wait for finite entrance animations (fades would skew contrast checks).
  // Wait for loading regions to be replaced (their content fades in when it arrives), and for
  // fades to finish: motion/react can animate opacity from JavaScript, which getAnimations()
  // doesn't list, so also wait until no element is part-way through an inline opacity fade.
  await page.waitForFunction(
    () =>
      !document.querySelector('[aria-busy="true"]') &&
      document
        .getAnimations()
        .every((a) => a.playState !== "running" || a.effect?.getTiming().iterations === Infinity) &&
      [...document.querySelectorAll('[style*="opacity"]')].every((el) => {
        const o = parseFloat(el.style.opacity);
        if (Number.isNaN(o) || o === 1) return true;
        // Opacity 0 is settled only off screen (sections that reveal on scroll); on screen it is
        // about to fade in, and a scan mid-fade measures blended, too-light colours.
        const r = el.getBoundingClientRect();
        const onScreen = r.bottom > 0 && r.top < innerHeight && r.width > 0 && r.height > 0;
        return o === 0 && !onScreen;
      }),
    null,
    { timeout: 8_000 },
  );
  let builder = new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]);
  for (const selector of exclude) builder = builder.exclude(selector);
  const { violations } = await builder.analyze();
  const blocking = violations.filter((v) => ["serious", "critical"].includes(v.impact));
  expect(
    blocking.map((v) => `${v.id}: ${v.help} (${v.nodes.length} nodes) e.g. ${v.nodes[0]?.target}`),
  ).toEqual([]);
}

/** The newest emailed link containing `path`, read from the dev outbox (simulated email). */
export async function emailLink(page, to, path) {
  let link;
  await expect
    .poll(async () => {
      const res = await page.request.get(`/api/dev/outbox?to=${encodeURIComponent(to)}`);
      const messages = res.ok() ? await res.json() : [];
      link = messages.flatMap((m) => m.links).find((l) => l.includes(path));
      return Boolean(link);
    })
    .toBe(true);
  const url = new URL(link);
  return url.pathname + url.search; // the app may be served from another port than FRONTEND_URL
}

/** Follow the confirmation link the signup email carries. */
export async function confirmEmail(page, email) {
  await page.goto(await emailLink(page, email, "/verify-email"));
  await expect(page.getByRole("heading", { name: "Email confirmed" })).toBeVisible();
}
