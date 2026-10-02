import { expect, test } from "@playwright/test";
import { expectAccessible, startDemo } from "./helpers";

test("dose ticks are saved to the account", async ({ page }) => {
  await startDemo(page);
  const schedule = page.locator("section", { hasText: "Today's doses" }).first();

  await page
    .getByRole("button", { name: /^Mark taken:/ })
    .first()
    .click();
  await expect(page.getByRole("button", { name: /^Taken:/ }).first()).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await page
    .getByRole("button", { name: /^Skip:/ })
    .first()
    .click();
  await expect(page.getByText("Skipped", { exact: true }).first()).toBeVisible();
  await expectAccessible(page);

  // A reload (or another device) sees the same marks.
  await page.reload();
  await expect(page.getByRole("button", { name: /^Taken:/ })).toHaveCount(1);
  await expect(page.getByRole("button", { name: /^Undo skip:/ })).toHaveCount(1);
  await expect(schedule).toContainText("1 of");
});

test("dose history can be reviewed and filled in", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/medications");
  const card = page.locator("[data-med-id]", { hasText: "Metformin" });
  await expect(card).toContainText(/Taken \d+ of \d+ in the last 14 days/);
  await card.getByRole("link", { name: /Dose history for Metformin/ }).click();

  await expect(page.getByRole("heading", { name: "Metformin 500 mg" })).toBeVisible();
  await expect(page.getByText("Marked taken")).toBeVisible();
  await expectAccessible(page);

  // Pick an earlier day and change its first dose; the day panel follows.
  const days = page.getByRole("button", { name: /: \d+ of \d+ taken$/ });
  await days.nth(2).click();
  const panel = page.locator("section", { has: page.locator("#day-heading") });
  // Demo history is random per account: pick whichever mark this dose doesn't have yet.
  const alreadySkipped =
    (await panel.getByRole("button", { name: "Skipped" }).first().getAttribute("aria-pressed")) ===
    "true";
  const target = alreadySkipped ? "Taken" : "Skipped";
  const button = panel.getByRole("button", { name: target }).first();
  await Promise.all([
    page.waitForResponse((r) => r.url().includes("/api/doses") && r.request().method() === "PUT"),
    button.click(),
  ]);
  await expect(button).toHaveAttribute("aria-pressed", "true");
  await page.reload();
  await days.nth(2).click();
  await expect(panel.getByRole("button", { name: target }).first()).toHaveAttribute(
    "aria-pressed",
    "true",
  );

  await page.setViewportSize({ width: 390, height: 844 });
  const { scrollWidth, clientWidth } = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));
  expect(scrollWidth).toBeLessThanOrEqual(clientWidth);
});
