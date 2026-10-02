import { expect, test } from "@playwright/test";
import { expectAccessible } from "./helpers";

test("landing page tells the story and is accessible", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Your health, all in one space.",
  );
  await expect(page.getByText("From paper to plan in five steps.")).toBeVisible();
  await expectAccessible(page);
});

test("login page is accessible in dark mode", async ({ page }) => {
  await page.emulateMedia({ colorScheme: "dark" });
  await page.goto("/login");
  await expect(page.getByRole("heading", { name: "Welcome back" })).toBeVisible();
  await expectAccessible(page);
});

test("typing 'apple' reveals an easter egg", async ({ page }) => {
  await page.goto("/");
  await page.locator("body").click({ position: { x: 5, y: 300 } });
  await page.keyboard.type("apple");
  await expect(page.getByText("You typed the magic word")).toBeVisible();
});

test("unknown routes show the 404 pun", async ({ page }) => {
  await page.goto("/definitely-not-a-page");
  await expect(page.getByText("Error 404")).toBeVisible();
  await expect(page.getByRole("link", { name: "Home page" })).toBeVisible();
});
