import { expect, test } from "@playwright/test";
import { expectAccessible, startDemo } from "./helpers";

test("a low supply shows on the dashboard until it is refilled", async ({ page }) => {
  await startDemo(page);
  const low = page.getByRole("region", { name: "Running low" });
  await expect(low).toContainText("Metformin");
  await expect(low).toContainText("(estimate)");
  await expectAccessible(page);

  await low.getByRole("button", { name: "Refill" }).click();
  const dialog = page.getByRole("dialog", { name: /Refill Metformin/ });
  await dialog.getByLabel(/Units added/).fill("60");
  await dialog.getByRole("button", { name: "Add refill" }).click();
  await expect(page.getByText("Added 60 tablets")).toBeVisible();
  await expect(low).toBeHidden();
});

test("supply can be tracked from a medication card", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/medications");
  const card = page.locator("[data-med-id]", { hasText: "Cetirizine" });
  await card.getByRole("button", { name: "Track supply" }).click();
  const dialog = page.getByRole("dialog", { name: /Supply of Cetirizine/ });
  await dialog.getByLabel("On hand now").fill("5");
  await dialog.getByRole("button", { name: "Save count" }).click();
  await expect(card).toContainText(/About \d+ tablets left/);
  await expect(card.getByRole("button", { name: "Refill" })).toBeVisible();
  await expectAccessible(page);
});
