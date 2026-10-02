import { expect, test } from "@playwright/test";
import { expectAccessible, startDemo } from "./helpers";

test("Ctrl+K searches records and jumps to the result", async ({ page }) => {
  await startDemo(page);
  await expect(page.getByText("Today's doses")).toBeVisible();
  await page.keyboard.press("Control+k");
  const dialog = page.getByRole("dialog", { name: "Search MedSpace" });
  const input = dialog.getByRole("combobox");
  await expect(input).toBeFocused();
  await expect(dialog.getByRole("option", { name: /Timeline/ })).toBeVisible();

  // Partial medicine name, then keyboard selection lands on the card in the Medications page.
  await input.fill("amox");
  const med = dialog.getByRole("option", { name: /Amoxicillin 500 mg/ }).first();
  await expect(med).toHaveAttribute("aria-selected", "true");
  await expectAccessible(page);
  await page.keyboard.press("Enter");
  await expect(dialog).toBeHidden();
  await expect(page).toHaveURL(/\/app\/medications\?focus=/);
  await expect(page.locator("[data-focused]")).toContainText("Amoxicillin");

  // Text inside a document comes back with the matching words highlighted.
  await page.getByRole("button", { name: "Search your records" }).click();
  await page.getByRole("combobox").fill("triglycerides");
  const doc = page.getByRole("option", { name: /Lipid profile results/ });
  await expect(doc.locator("mark").first()).toHaveText(/triglycerides/i);
  await doc.click();
  await expect(page).toHaveURL(/\/app\/documents\/.+\?page=1/);
});

test("search hands a question over to Ask MedSpace", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/timeline");
  await expect(page.getByRole("heading", { name: "Upcoming" })).toBeVisible();
  await page.keyboard.press("/");
  await page.getByRole("combobox").fill("what is my cholesterol");
  await page.getByRole("option", { name: /Ask MedSpace about/ }).click();
  await expect(page).toHaveURL(/\/app\/ask\?t=/);
  await expect(page.getByText("what is my cholesterol").first()).toBeVisible();
});
