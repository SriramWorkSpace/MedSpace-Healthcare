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

test("the theme switch animates from the toggle and settles in both directions", async ({
  page,
}) => {
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "no-preference" });
  await page.goto("/");
  const html = page.locator("html");
  await expect(html).toHaveAttribute("data-theme", "light");

  await page.getByRole("button", { name: "Switch to dark theme" }).click();
  await expect(html).toHaveAttribute("data-theme", "dark");
  await expect(html).not.toHaveClass(/theme-switching/);

  await page.getByRole("button", { name: "Switch to light theme" }).click();
  await expect(html).toHaveAttribute("data-theme", "light");
  await expect(html).not.toHaveClass(/theme-switching/);
  expect(await page.evaluate(() => localStorage.getItem("ms-theme"))).toBe("light");
});
