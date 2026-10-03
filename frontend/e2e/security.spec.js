import { createHmac } from "node:crypto";
import { expect, test } from "@playwright/test";
import { expectAccessible, signUp } from "./helpers";

const PASSWORD = "a-long-enough-password";

/** RFC 6238 code for `secret` (base32) at the current step plus `offset`. */
function totp(secret, offset = 0) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
  let bits = "";
  for (const ch of secret.replace(/\s+/g, "").toUpperCase())
    bits += alphabet.indexOf(ch).toString(2).padStart(5, "0");
  const key = Buffer.from(bits.match(/.{8}/g).map((b) => parseInt(b, 2)));
  const counter = Buffer.alloc(8);
  counter.writeBigUInt64BE(BigInt(Math.floor(Date.now() / 30_000) + offset));
  const digest = createHmac("sha1", key).update(counter).digest();
  const at = digest[digest.length - 1] & 0x0f;
  return String((digest.readUInt32BE(at) & 0x7fffffff) % 1_000_000).padStart(6, "0");
}

async function signIn(page, email) {
  await page.goto("/login");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password", { exact: true }).fill(PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Check your phone" })).toBeVisible();
}

test("two-step verification guards sign-in, and other devices can be signed out", async ({
  page,
  browser,
}) => {
  const email = `mfa-${Date.now()}@example.com`;
  await signUp(page, email);
  await page.goto("/app/settings#security");
  const security = page.locator("#security");
  await expect(security.getByText("Two-step verification")).toBeVisible();
  await expectAccessible(page);

  // Set up: scan (or type) the key, confirm a code, save the recovery codes.
  await security.getByRole("button", { name: "Turn on" }).click();
  const setup = page.getByRole("dialog", { name: "Set up two-step verification" });
  await expect(setup.getByRole("img", { name: /QR code/ })).toBeVisible();
  const secret = await setup.getByLabel("Setup key").innerText();
  await setup.getByLabel("Code from the app").fill(totp(secret));
  await setup.getByRole("button", { name: "Turn on" }).click();

  const saved = page.getByRole("dialog", { name: "Save your recovery codes" });
  await expect(saved.locator("li")).toHaveCount(10);
  const codes = await saved
    .getByRole("list", { name: "Recovery codes" })
    .locator("li")
    .allInnerTexts();
  expect(codes).toHaveLength(10);
  await expectAccessible(page);
  await saved.getByRole("button", { name: "I've saved them" }).click();
  await expect(security.getByText("10 recovery codes left")).toBeVisible();

  // Another device: the password alone is no longer enough.
  const phone = await browser.newContext();
  const other = await phone.newPage();
  await signIn(other, email);
  await expectAccessible(other);
  await other.getByLabel("Code").fill("000000");
  await other.getByRole("button", { name: "Verify" }).click();
  await expect(other.getByRole("alert")).toContainText("didn't work");
  await other.getByLabel("Code").fill(totp(secret, 1));
  await other.getByRole("button", { name: "Verify" }).click();
  await other.waitForURL("**/app");

  // A recovery code works too, once.
  const laptop = await browser.newContext();
  const third = await laptop.newPage();
  await signIn(third, email);
  await third.getByRole("button", { name: "Use a recovery code" }).click();
  await third.getByLabel("Recovery code").fill(codes[0]);
  await third.getByRole("button", { name: "Verify" }).click();
  await third.waitForURL("**/app");

  // Back on the first device: three sessions, sign out the others.
  await page.reload();
  const devices = page.getByRole("list", { name: "Signed-in devices" });
  await expect(devices.locator("li")).toHaveCount(3);
  await expect(devices.locator("li").first()).toContainText("This device");
  await expect(security.getByText("9 recovery codes left")).toBeVisible();
  await security.getByRole("button", { name: "Sign out other devices" }).click();
  await page.getByRole("dialog").getByRole("button", { name: "Sign them out" }).click();
  await expect(devices.locator("li")).toHaveCount(1);

  for (const p of [other, third]) {
    await p.goto("/app/medications");
    await p.waitForURL(/\/login/);
  }
  await phone.close();
  await laptop.close();
});
