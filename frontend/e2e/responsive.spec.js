import { expect, test } from "@playwright/test";
import { startDemo } from "./helpers";

test("mobile navigation uses the top drawer", async ({ page }) => {
  await startDemo(page);
  await page.getByRole("button", { name: "Open menu" }).click();
  await page.locator("#mobile-nav").getByRole("link", { name: "Timeline" }).click();
  await expect(page).toHaveURL(/\/app\/timeline/);
  await expect(page.getByRole("button", { name: "Open menu" })).toBeVisible();
});

test("the hero call to action is visible without scrolling on a phone", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("button", { name: /Try the demo/ }).first()).toBeInViewport();
});

test("no page scrolls sideways on a phone", async ({ page }) => {
  await startDemo(page);
  for (const path of [
    "/app",
    "/app/documents",
    "/app/medications",
    "/app/diet",
    "/app/labs",
    "/app/labs/ldl-cholesterol",
    "/app/timeline",
    "/app/ask",
    "/app/sharing",
    "/app/settings",
    "/",
  ]) {
    await page.goto(path);
    await page.waitForLoadState("networkidle");
    const { scrollWidth, clientWidth } = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    expect(scrollWidth, `${path} overflows horizontally`).toBeLessThanOrEqual(clientWidth);
  }
});

test("the app bar fits tablets and small laptops", async ({ page }) => {
  await startDemo(page);
  for (const width of [768, 1024, 1180]) {
    await page.setViewportSize({ width, height: 800 });
    const { scrollWidth, clientWidth } = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    expect(scrollWidth, `the app bar overflows at ${width}px`).toBeLessThanOrEqual(clientWidth);
  }
});
