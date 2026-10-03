import { expect, test } from "@playwright/test";
import { expectAccessible, startDemo } from "./helpers";

test("focusing a field highlights where it is printed on the page", async ({ page }) => {
  await startDemo(page);
  await page.getByRole("link", { name: "Review" }).first().click();
  const viewer = page.getByRole("region", { name: /Source document/ });
  await expect(viewer.getByRole("img", { name: /Page 1/ })).toBeVisible();

  const strength = page.getByLabel("Strength").first();
  await strength.focus();
  const status = page.getByRole("status").filter({ hasText: "Showing" });
  await expect(status).toContainText("· Strength");
  const box = viewer.locator("[data-highlight]").first();
  await expect(box).toBeVisible();
  // The box sits inside the page image.
  const img = await viewer.getByRole("img").boundingBox();
  const b = await box.boundingBox();
  expect(b.x).toBeGreaterThan(img.x);
  expect(b.y).toBeGreaterThan(img.y);
  expect(b.x + b.width).toBeLessThan(img.x + img.width);

  // The letterhead, then the whole medicine line from the "p.1" button.
  await page.getByLabel("Prescriber").focus();
  await expect(status).toContainText("Prescriber");
  await page
    .getByRole("button", { name: /^Show .+ on page 1 of the source/ })
    .first()
    .click();
  await expect(viewer.locator("[data-highlight]").first()).toBeVisible();
  await expectAccessible(page);

  // Fields that aren't on the page clear the highlight; the chip can be dismissed.
  await page.getByLabel("Summary").focus();
  await expect(viewer.locator("[data-highlight]")).toHaveCount(0);
  await page.getByLabel("Strength").first().focus();
  await page.getByRole("button", { name: "Clear highlight" }).click();
  await expect(viewer.locator("[data-highlight]")).toHaveCount(0);
});
