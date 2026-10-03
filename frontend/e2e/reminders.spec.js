import { expect, test } from "@playwright/test";
import { expectAccessible, startDemo } from "./helpers";

// Playwright's default headless shell denies notifications to service workers; full Chromium
// (new headless mode) supports them.
test.use({ channel: "chromium" });

// Headless Chromium has no push service, so the browser subscription is stubbed; everything
// after it (our API, the service worker's push handler) is real.
const STUB = () => {
  let current = null;
  const sub = {
    endpoint: `https://push.example.com/e2e/${Math.random().toString(36).slice(2)}`,
    toJSON() {
      return {
        endpoint: this.endpoint,
        keys: {
          p256dh:
            "BNcRdreALRFXTkOOUHK1EtK2wtaz5Ry4YfYCA_0QTpQtUbVlUls0VJXg7A8u-Ts1XbjhazAkj7I99e8QcYP7DkM",
          auth: "tBHItJI5svbpez7KI4CCXg",
        },
      };
    },
    unsubscribe: async () => {
      current = null;
      return true;
    },
  };
  if (window.PushManager) {
    PushManager.prototype.subscribe = async () => (current = sub);
    PushManager.prototype.getSubscription = async () => current;
  }
};

test("dose reminders can be turned on, tested and shown by the service worker", async ({
  page,
  context,
}) => {
  const base = test.info().project.use.baseURL;
  await context.grantPermissions(["notifications"], { origin: new URL(base).origin });
  await context.addInitScript(STUB);
  await startDemo(page);
  const hasWorker = await page.evaluate(async () =>
    Boolean(await navigator.serviceWorker?.getRegistration()),
  );
  test.skip(!hasWorker, "push needs the service worker of a production build");
  await page.waitForFunction(() => navigator.serviceWorker.controller !== null);

  await page.goto("/app/settings#device");
  const toggle = page.getByRole("switch", { name: "Dose reminders" });
  await expect(toggle).toBeEnabled();
  await toggle.click();
  await expect(toggle).toHaveAttribute("aria-checked", "true");
  const subs = await page.evaluate(() => fetch("/api/push/subscriptions").then((r) => r.json()));
  expect(subs).toHaveLength(1);
  expect(subs[0].endpoint_hint).toBe("push.example.com");

  await page.getByLabel("Remind me").selectOption("10");
  await page.getByRole("button", { name: "Send a test" }).click();
  await expect(page.getByText("Test notification sent")).toBeVisible();
  await expectAccessible(page);

  // Deliver a reminder straight to the service worker and check what it shows.
  const cdp = await context.newCDPSession(page);
  const registrationId = await new Promise((resolve) => {
    cdp.on("ServiceWorker.workerRegistrationUpdated", ({ registrations }) => {
      const reg = registrations.find((r) => !r.isDeleted);
      if (reg) resolve(reg.registrationId);
    });
    cdp.send("ServiceWorker.enable");
  });
  const origin = new URL(page.url()).origin;
  await cdp.send("ServiceWorker.deliverPushMessage", {
    origin,
    registrationId,
    data: JSON.stringify({
      title: "Time for your 8:00 PM dose",
      body: "Metformin 500 mg. After meals.",
      tag: "dose-e2e",
      token: "test-token-not-used-here",
      actions: [
        { action: "taken", title: "Taken" },
        { action: "skipped", title: "Skip" },
      ],
    }),
  });
  await expect
    .poll(() =>
      page.evaluate(async () => {
        const reg = await navigator.serviceWorker.getRegistration();
        return (await reg.getNotifications()).map((n) => ({
          title: n.title,
          actions: n.actions.map((a) => a.action),
        }));
      }),
    )
    .toContainEqual({ title: "Time for your 8:00 PM dose", actions: ["taken", "skipped"] });

  await toggle.click();
  await expect(toggle).toHaveAttribute("aria-checked", "false");
  const after = await page.evaluate(() => fetch("/api/push/subscriptions").then((r) => r.json()));
  expect(after).toHaveLength(0);
});
