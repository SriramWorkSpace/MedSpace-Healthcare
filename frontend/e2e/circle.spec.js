import { expect, test } from "@playwright/test";
import { confirmEmail, expectAccessible, signUp, startDemo } from "./helpers";

test("a helper switches to a family member's records and back", async ({ page }) => {
  await startDemo(page);
  await page.getByRole("button", { name: "Account menu" }).click();
  await page.getByRole("menuitem", { name: /Rosa Lindqvist/ }).click();

  const banner = page.getByRole("complementary", { name: "Viewing someone else's records" });
  await expect(banner).toContainText("Viewing Rosa Lindqvist's records as a helper");
  await expect(page.getByText("Today's doses")).toBeVisible();
  const nav = page.getByRole("navigation", { name: "Primary" });
  await expect(nav.getByRole("link", { name: "Ask", exact: true })).toHaveCount(0);
  await expect(nav.getByRole("link", { name: "Sharing", exact: true })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Upload" })).toHaveCount(0);
  await expectAccessible(page);

  // Helpers can tick doses for the person they help.
  await page
    .getByRole("button", { name: /^Mark taken: Metformin/ })
    .first()
    .click();
  await expect(page.getByRole("button", { name: /^Taken: Metformin/ }).first()).toBeVisible();

  await page.goto("/app/medications");
  await expect(page.getByRole("button", { name: "Edit times" })).toHaveCount(0);
  await expect(page.locator("[data-med-id]")).toHaveCount(3);

  await banner.getByRole("button", { name: "Back to your records" }).click();
  await expect(banner).toBeHidden();
  await expect(nav.getByRole("link", { name: "Ask", exact: true })).toBeVisible();
});

test("an invitation is accepted and gives read-only access", async ({ page, browser }) => {
  await startDemo(page);
  await page.goto("/app/settings#circle");
  const email = `viewer-${Date.now()}@example.com`;
  await page.getByLabel("Their email").fill(email);
  await page.getByRole("button", { name: "Create invitation" }).click();
  const url = await page.getByLabel("Invitation link", { exact: true }).inputValue();
  await page.getByRole("button", { name: "Done" }).click();
  await expect(
    page.getByRole("list", { name: "People with access to your records" }),
  ).toContainText("Invited");

  const other = await browser.newContext();
  const viewer = await other.newPage();
  await signUp(viewer, email);
  await confirmEmail(viewer, email); // invitations need a confirmed address
  await viewer.goto(new URL(url).pathname);
  await expect(
    viewer.getByRole("heading", { name: /invited you to their care circle/ }),
  ).toBeVisible();
  await expectAccessible(viewer);
  await viewer.getByRole("button", { name: "Accept and open their records" }).click();

  const banner = viewer.getByRole("complementary", { name: "Viewing someone else's records" });
  await expect(banner).toContainText("as a viewer (read only)");
  await expect(viewer.getByText("Today's doses")).toBeVisible();
  // Viewers can't tick doses.
  await expect(viewer.getByRole("button", { name: /^Mark taken:/ }).first()).toBeDisabled();
  await other.close();

  await page.reload();
  const list = page.getByRole("list", { name: "People with access to your records" });
  await expect(list).toContainText("Active");
  await list.getByRole("button", { name: "Remove" }).click();
  await page.getByRole("button", { name: "Remove", exact: true }).last().click();
  await expect(list).toHaveCount(0);
});
