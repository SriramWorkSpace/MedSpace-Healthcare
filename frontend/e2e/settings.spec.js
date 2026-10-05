import { expect, test } from "@playwright/test";
import { startDemo } from "./helpers";

test.use({ viewport: { width: 1440, height: 900 } });

test("the settings menu glides to a section instead of jumping", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/settings");
  const nav = page.getByRole("navigation", { name: "Settings sections" });
  await expect(nav.getByRole("link", { name: "Profile" })).toHaveAttribute(
    "aria-current",
    "location",
  );

  // Sample the scroll position while it moves: several in-between positions, not one jump.
  await page.evaluate(() => {
    window.__ys = [];
    const sample = () => {
      window.__ys.push(window.scrollY);
      if (window.__ys.length < 40) requestAnimationFrame(sample);
    };
    requestAnimationFrame(sample);
  });
  await nav.getByRole("link", { name: "Activity" }).click();
  await expect(nav.getByRole("link", { name: "Activity" })).toHaveAttribute(
    "aria-current",
    "location",
  );
  await expect(page.locator("#activity h2")).toBeFocused();
  await expect(page).toHaveURL(/#activity$/);
  const ys = await page.evaluate(() => window.__ys);
  const distinct = new Set(ys.map(Math.round));
  expect(distinct.size).toBeGreaterThan(5);
  // It lands with the heading just below the top bar.
  const top = await page.locator("#activity").evaluate((el) => el.getBoundingClientRect().top);
  expect(top).toBeGreaterThan(60);
  expect(top).toBeLessThan(120);
});

test("with reduced motion, the settings menu jumps straight there", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await startDemo(page);
  await page.goto("/app/settings");
  const nav = page.getByRole("navigation", { name: "Settings sections" });
  await nav.getByRole("link", { name: "Account" }).click();
  await expect(page.locator("#danger h2")).toBeFocused();
  await expect(page).toHaveURL(/#danger$/);
});
