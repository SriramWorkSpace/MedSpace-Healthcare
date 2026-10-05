import { expect, test } from "@playwright/test";
import { startDemo } from "./helpers";

/** Reads this device's offline snapshot straight from IndexedDB. */
const readSnapshot = (page) =>
  page.evaluate(
    () =>
      new Promise((resolve) => {
        const req = indexedDB.open("medspace-offline", 1);
        req.onupgradeneeded = () => req.result.createObjectStore("kv");
        req.onsuccess = () => {
          const get = req.result.transaction("kv").objectStore("kv").get("snapshot");
          get.onsuccess = () => resolve(get.result ?? null);
          get.onerror = () => resolve(null);
        };
        req.onerror = () => resolve(null);
      }),
  );

test("records stay readable offline and dose ticks sync when back online", async ({
  page,
  context,
}) => {
  await startDemo(page);
  // The service worker only exists in production builds (vite preview, CI, Docker prod).
  const hasWorker = await page.evaluate(async () => {
    if (!("serviceWorker" in navigator)) return false;
    const reg = await navigator.serviceWorker.getRegistration();
    return Boolean(reg);
  });
  test.skip(!hasWorker, "service worker runs only against a production build");

  await page.goto("/app/settings#device");
  const toggle = page.getByRole("switch", { name: "Offline access" });
  await toggle.click();
  await expect(toggle).toHaveAttribute("aria-checked", "true");

  // Browse the pages to read offline (in-app navigation, as a user would).
  const nav = page.getByRole("navigation", { name: "Primary" });
  await nav.getByRole("link", { name: "Medications", exact: true }).click();
  await expect(page.getByText("Metformin").first()).toBeVisible();
  await nav.getByRole("link", { name: "Dashboard", exact: true }).click();
  await expect(page.getByText("Today's doses")).toBeVisible();
  await page.waitForFunction(() => navigator.serviceWorker.controller !== null);
  await expect
    .poll(async () =>
      ((await readSnapshot(page))?.state?.queries ?? []).map((q) => q.queryKey[0]).sort(),
    )
    .toEqual(expect.arrayContaining(["auth", "dashboard", "records"]));

  await context.setOffline(true);
  await page.reload();
  const banner = page.getByRole("status").filter({ hasText: "You're offline" });
  await expect(banner).toContainText("Showing what this device saved");
  await expect(page.getByText("Today's doses")).toBeVisible();

  const tick = page.getByRole("button", { name: /^Mark taken:/ }).first();
  const dose = await tick.getAttribute("data-dose");
  await tick.click();
  await expect(banner).toContainText("1 dose tick will sync when you reconnect");

  // The queued tick survives a reload while still offline.
  await expect.poll(async () => (await readSnapshot(page))?.state?.mutations?.length ?? 0).toBe(1);
  await page.reload();
  await expect(page.locator(`[data-dose="${dose}"]`)).toHaveAttribute("aria-pressed", "true");

  await context.setOffline(false);
  await expect(banner).toBeHidden({ timeout: 15_000 });
  const synced = await page.evaluate(async () => {
    const dash = await (await fetch("/api/dashboard", { credentials: "include" })).json();
    return dash.doses_today.filter((d) => d.status === "taken").length;
  });
  expect(synced).toBe(1);

  // Signing out deletes the offline copy.
  await page.getByRole("button", { name: "Account menu" }).click();
  await page.getByRole("menuitem", { name: "Sign out" }).click();
  await expect(page).toHaveURL(/\/login/);
  await expect.poll(() => readSnapshot(page)).toBeNull();
});
