import { expect, test } from "@playwright/test";
import { confirmEmail, emailLink, expectAccessible, signUp } from "./helpers";

test("a new account confirms its email from the link", async ({ page }) => {
  const email = `confirm-${Date.now()}@example.com`;
  await signUp(page, email);
  const banner = page.getByRole("complementary", { name: "Confirm your email" });
  await expect(banner).toContainText(email);
  await expectAccessible(page);

  await banner.getByRole("button", { name: "Resend link" }).click();
  await expect(page.getByText("Link sent")).toBeVisible();

  await confirmEmail(page, email);
  await expectAccessible(page);
  await page.getByRole("link", { name: "Go to MedSpace" }).click();
  await page.waitForURL("**/app");
  await expect(banner).toBeHidden();
});

test("forgot password: reset by email, then sign in with the new password", async ({
  page,
  browser,
}) => {
  const email = `reset-${Date.now()}@example.com`;
  const fresh = await browser.newContext();
  const signupPage = await fresh.newPage();
  await signUp(signupPage, email);
  await fresh.close();

  await page.goto("/login");
  await page.getByRole("link", { name: "Forgot password?" }).click();
  await expect(page.getByRole("heading", { name: "Forgot your password?" })).toBeVisible();
  await expectAccessible(page);
  await page.getByLabel("Email").fill(email);
  await page.getByRole("button", { name: "Send reset link" }).click();
  await expect(page.getByRole("heading", { name: "Check your inbox" })).toBeVisible();

  await page.goto(await emailLink(page, email, "/reset-password"));
  await expect(page.getByRole("heading", { name: "Choose a new password" })).toBeVisible();
  await expectAccessible(page);
  await page.getByLabel("New password").fill("a-fresh-new-password");
  await page.getByRole("button", { name: "Set new password" }).click();
  await expect(page.getByRole("heading", { name: "Password updated" })).toBeVisible();

  await page.getByRole("link", { name: "Sign in" }).click();
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password", { exact: true }).fill("a-fresh-new-password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("**/app");

  // The link worked once.
  await page.goto(await emailLink(page, email, "/reset-password"));
  await page.getByLabel("New password").fill("another-new-password");
  await page.getByRole("button", { name: "Set new password" }).click();
  await expect(page.getByRole("heading", { name: "This link has expired" })).toBeVisible();
});

test("changing the email waits for the new inbox, then moves the account", async ({ page }) => {
  const stamp = Date.now();
  const oldEmail = `move-${stamp}@example.com`;
  const newEmail = `moved-${stamp}@example.com`;
  await signUp(page, oldEmail);
  await page.goto("/app/settings#security");
  const card = page.locator("#security").getByText("Email address").locator("../..");
  await expect(card).toContainText(oldEmail);

  await card.getByRole("button", { name: "Change" }).click();
  const dialog = page.getByRole("dialog", { name: "Change your email" });
  await dialog.getByLabel("New email").fill(newEmail);
  await dialog.getByLabel("Current password").fill("a-long-enough-password");
  await expectAccessible(page);
  await dialog.getByRole("button", { name: "Send link" }).click();
  await expect(page.getByText("Check your new inbox")).toBeVisible();
  await expect(card).toContainText(`Waiting for you to confirm ${newEmail}`);

  await page.goto(await emailLink(page, newEmail, "/confirm-email-change"));
  await expect(page.getByRole("heading", { name: "Email changed" })).toBeVisible();
  await expectAccessible(page);
  await page.getByRole("link", { name: "Back to settings" }).click();
  await expect(page.locator("#security")).toContainText(newEmail);
  await expect(page.locator("#security")).not.toContainText("Waiting for you to confirm");
});
