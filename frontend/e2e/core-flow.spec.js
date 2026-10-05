import path from "node:path";
import { fileURLToPath } from "node:url";
import { expect, test } from "@playwright/test";
import { expectAccessible, signUp, startDemo } from "./helpers";

const here = path.dirname(fileURLToPath(import.meta.url));
const SAMPLE = path.resolve(here, "../../samples/rx-riverside-acute.pdf");

test("upload, review, confirm, report", async ({ page }) => {
  await signUp(page);
  await expect(page.getByText("Start with your first prescription")).toBeVisible();

  await page.goto("/app/documents");
  await page.locator('input[type="file"]').setInputFiles(SAMPLE);
  const card = page.locator("a", { hasText: "Rx riverside acute" });
  await expect(card).toContainText("Needs review", { timeout: 30_000 });
  await card.click();

  // Side-by-side review: the source page next to the extracted medicines.
  await expect(page.getByRole("img", { name: /Page 1 of the source document/ })).toBeVisible();
  await expect(page.getByLabel("Medicine").first()).toHaveValue("Amoxicillin");
  await expectAccessible(page);

  await page.getByRole("button", { name: "Confirm records" }).click();
  await expect(page.getByText("Records confirmed")).toBeVisible();
  await page.getByRole("link", { name: "View report" }).click();
  await expect(page.getByRole("heading", { name: "Dr. Imani Oduya" })).toBeVisible();
  await expect(page.getByRole("cell", { name: /Amoxicillin/ })).toBeVisible();
});

test("dashboard, medications and timeline for a seeded demo", async ({ page }) => {
  await startDemo(page);
  await expect(page.getByText("Today's doses")).toBeVisible();
  await expect(page.getByText("waiting for your review")).toBeVisible();
  await expectAccessible(page);

  await page.goto("/app/medications");
  await expect(page.getByText("Amoxicillin").first()).toBeVisible();
  await page.goto("/app/timeline");
  await expect(page.getByRole("heading", { name: "Upcoming" })).toBeVisible();
});

test("Ask MedSpace answers with citations and refuses advice", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/ask");
  await page.locator("#ask-input").fill("How often do I take Amoxicillin?");
  await page.keyboard.press("Enter");
  await expect(page.getByText(/twice daily at 8:00 AM and 8:00 PM/).first()).toBeVisible();
  await expect(
    page.getByRole("button", { name: /Amoxicillin \(confirmed record\)/ }).first(),
  ).toBeVisible();

  await page.locator("#ask-input").fill("Should I stop taking Metformin?");
  await page.keyboard.press("Enter");
  await expect(page.getByText(/can't give medical advice/)).toBeVisible();
});

test("share a prescription, open it anonymously, then revoke", async ({ page, browser }) => {
  await startDemo(page);
  await page.goto("/app/sharing");
  await page.getByRole("button", { name: "New link" }).click();
  await page.getByLabel("Label").fill("For Dr. Reyes");
  await page
    .locator("label", { hasText: "Prescription from Dr. Imani Oduya" })
    .locator("input")
    .check();
  await page.getByRole("button", { name: "Create link" }).click();
  const url = await page.getByLabel("Share link").inputValue();
  await page.getByRole("button", { name: "Done" }).click();

  const visitor = await browser.newContext();
  const v = await visitor.newPage();
  await v.goto(new URL(url).pathname);
  await expect(v.getByRole("heading", { name: "For Dr. Reyes" })).toBeVisible();
  await expect(v.getByText(/Shared by/)).toBeVisible();

  await page.getByRole("button", { name: "Revoke" }).click();
  await page.getByRole("button", { name: "Revoke link" }).click();
  await expect(page.getByText("Revoked", { exact: true })).toBeVisible();
  await v.reload();
  await expect(v.getByText("This link has been discharged")).toBeVisible();
  await visitor.close();
});

test("Google sync works in simulation mode", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/settings");
  await page.getByRole("button", { name: "Connect Google" }).click();
  await expect(page.getByText("Google connected")).toBeVisible();
  await expect(page.getByText(/@gmail\.simulated/)).toBeVisible();
});

test("Continue with Google signs in and connects reminders (simulated)", async ({ page }) => {
  await page.goto("/login");
  await page.getByRole("button", { name: "Continue with Google" }).click();
  await page.waitForURL("**/app");
  await expect(page.getByText("Signed in with Google")).toBeVisible();
  await expect(page.getByText(/Calendar and Tasks are connected/)).toBeVisible();
  await expect(page).not.toHaveURL(/google=/);

  await page.goto("/app/settings");
  await expect(page.getByText("Connected", { exact: true })).toBeVisible();
  await expect(page.getByText("Email and password")).toHaveCount(0);
});

test("diet notes from the care team are grouped with their sources", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/diet");
  await expect(page.getByRole("heading", { name: "Diet notes" })).toBeVisible();
  await expect(page.getByRole("heading", { name: /^Avoid/ })).toBeVisible();
  await expect(page.getByText("Avoid alcohol while on antibiotics.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "With your medicines" })).toBeVisible();
  await expectAccessible(page);

  await page.getByRole("button", { name: "Remove note: Avoid sugary drinks." }).click();
  await expect(page.getByText("Avoid sugary drinks.")).toHaveCount(0);
});
