import { expect, test } from "@playwright/test";
import { expectAccessible, startDemo } from "./helpers";

test("prepare for a visit from the dashboard and share the brief", async ({ page, browser }) => {
  await startDemo(page);
  await page.getByRole("link", { name: /Prepare for Follow-up with Dr. Imani Oduya/ }).click();
  await expect(page).toHaveURL(/\/app\/visits\/[0-9a-f-]+$/);
  await expect(
    page.getByRole("heading", { name: "Visit with Dr. Imani Oduya" }).first(),
  ).toBeVisible();

  const brief = page.getByRole("article", { name: "Visit brief" });
  await expect(brief).toContainText("Do I need another CBC after this one?");
  await expect(brief).toContainText("LDL cholesterol");

  await page.getByLabel("New question").fill("Is the cough worth an X-ray?");
  await page.getByRole("button", { name: "Add", exact: true }).click();
  await expect(brief).toContainText("Is the cough worth an X-ray?");

  const prompt = page.locator("li", { hasText: "LDL cholesterol was above the range" });
  await prompt.getByRole("button", { name: "Add as question" }).click();
  await expect(prompt.getByRole("button", { name: "Added" })).toBeDisabled();
  await expect(brief).toContainText("Ask about: LDL cholesterol was above the range");

  await page.getByRole("checkbox", { name: /Answered: Do I need another CBC/ }).click();
  await expect(brief).toContainText("1 answered question not shown.");
  await expectAccessible(page);

  // Survives a reload: questions are saved to the account.
  await page.reload();
  await expect(brief).toContainText("Is the cough worth an X-ray?");

  await page.getByRole("link", { name: "Share" }).click();
  await expect(
    page.locator("label", { hasText: "Visit brief: Visit with Dr. Imani Oduya" }).locator("input"),
  ).toBeChecked();
  await page.getByLabel("Label").fill("Brief for Dr. Oduya");
  await page.getByRole("button", { name: "Create link" }).click();
  const url = await page.getByLabel("Share link").inputValue();

  const visitor = await browser.newContext();
  const v = await visitor.newPage();
  await v.goto(new URL(url).pathname);
  const shared = v.getByRole("article", { name: "Visit brief" });
  await expect(shared).toContainText("Is the cough worth an X-ray?");
  await expect(shared).toContainText("Current medications");
  await visitor.close();
});

test("a new visit prep can be created from the visits page", async ({ page }) => {
  await startDemo(page);
  await page.goto("/app/visits");
  await expect(page.getByRole("link", { name: /Visit with Dr. Imani Oduya/ })).toBeVisible();
  await expectAccessible(page);

  await page.getByRole("button", { name: "New visit prep" }).click();
  await page.getByLabel("With").fill("Dr. Lena Park");
  await page.getByRole("button", { name: "Create" }).click();
  await expect(
    page.getByRole("heading", { name: "Visit with Dr. Lena Park" }).first(),
  ).toBeVisible();
  await expect(page.getByRole("article", { name: "Visit brief" })).toContainText(
    "No open questions.",
  );
});
