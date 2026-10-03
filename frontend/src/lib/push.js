/**
 * Browser side of dose reminders (ADR-028): permission, the push subscription, and what this
 * device supports. Push needs the service worker, which only production builds register.
 */

export function pushSupport() {
  if (!("serviceWorker" in navigator) || !("PushManager" in window) || !("Notification" in window))
    return "unsupported";
  return "supported";
}

export async function swRegistration() {
  if (!("serviceWorker" in navigator)) return null;
  return (await navigator.serviceWorker.getRegistration()) ?? null;
}

function keyToBytes(base64url) {
  const padded = (base64url + "=".repeat((4 - (base64url.length % 4)) % 4))
    .replace(/-/g, "+")
    .replace(/_/g, "/");
  return Uint8Array.from(atob(padded), (c) => c.charCodeAt(0));
}

export async function currentSubscription() {
  const reg = await swRegistration();
  return reg ? reg.pushManager.getSubscription() : null;
}

/** Ask permission (if needed) and subscribe. Throws "denied" or "no-worker". */
export async function subscribePush(publicKey) {
  const reg = await swRegistration();
  if (!reg) throw new Error("no-worker");
  const permission =
    Notification.permission === "default"
      ? await Notification.requestPermission()
      : Notification.permission;
  if (permission !== "granted") throw new Error("denied");
  const existing = await reg.pushManager.getSubscription();
  if (existing) return existing;
  return reg.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: keyToBytes(publicKey),
  });
}

/** Unsubscribe this browser; returns the endpoint that was removed (or null). */
export async function unsubscribePush() {
  const sub = await currentSubscription();
  if (!sub) return null;
  const { endpoint } = sub;
  await sub.unsubscribe();
  return endpoint;
}
