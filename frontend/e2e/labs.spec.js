import path from "node:path";
import { fileURLToPath } from "node:url";
import { expect, test } from "@playwright/test";
import { expectAccessible, signUp, startDemo } from "./helpers";

const here = path.dirname(fileURLToPath(import.meta.url));
const LAB_SAMPLE = path.resolve(here, "../../samples/lab-cedar-lipid.pdf");

test("lab results are charted over time with the printed range", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/labs");
  await expect(page.getByRole("heading", { name: "Diabetes monitoring panel" })).toBeVisible();
  const ldl = page.getByRole("link", { name: /LDL cholesterol/ });
  await expect(ldl).toContainText("138");
  await expect(ldl).toContainText("Above range");
  await expect(ldl).toContainText("Down 11 mg/dL");
  await expectAccessible(page);

  await ldl.click();
  await expect(page).toHaveURL(/\/app\/labs\/ldl-cholesterol$/);
  await expect(page.getByRole("img", { name: /LDL cholesterol: 3 results/ })).toBeVisible();
  const rows = page.getByRole("region", { name: "Every result" }).locator("tbody tr");
  await expect(rows).toHaveCount(3);
  await expect(rows.first()).toContainText("138 mg/dL");
  await expectAccessible(page);
});

test("a lab report is reviewed and confirmed into results", async ({ page }) => {
  await signUp(page);
  await page.goto("/app/labs");
  await expect(page.getByRole("heading", { name: "No lab results yet" })).toBeVisible();

  await page.goto("/app/documents");
  await page.locator('input[type="file"]').setInputFiles(LAB_SAMPLE);
  const card = page.locator("a", { hasText: "Lab cedar lipid" });
  await expect(card).toContainText("Needs review", { timeout: 30_000 });
  await card.click();

  // On a lab report the results come first, exactly as printed.
  await expect(page.getByLabel("Type")).toHaveValue("lab_report");
  const results = page.getByRole("heading", { name: "Lab results" });
  await expect(results).toBeVisible();
  await expect(page.getByLabel("Test", { exact: true }).nth(1)).toHaveValue("LDL cholesterol");
  await expect(page.getByLabel("Reference range").nth(1)).toHaveValue("< 130");
  await page.getByLabel("Result", { exact: true }).nth(1).fill("128"); // fix a misread value

  await page.getByRole("button", { name: "Confirm records" }).click();
  await expect(page.getByText("Records confirmed")).toBeVisible();

  await page.goto("/app/labs");
  const ldl = page.getByRole("link", { name: /LDL cholesterol/ });
  await expect(ldl).toContainText("128");
  await expect(ldl).toContainText("In range");
  await expect(page.getByRole("link", { name: /Total cholesterol/ })).toContainText("Above range");
});
