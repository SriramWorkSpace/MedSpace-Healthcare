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
  await page.waitForFunction(
    () =>
      document
        .getAnimations()
        .every((a) => a.playState !== "running" || a.effect?.getTiming().iterations === Infinity),
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
