/* global VERSION, PRECACHE */
/*
 * MedSpace service worker (ADR-025). The build prepends VERSION and PRECACHE (every built asset),
 * so each deploy produces a new worker that installs the matching files.
 *
 * - App shell and assets: precached, served cache-first (they are content-hashed).
 * - Navigations: network first, falling back to the cached app shell when offline.
 * - /api: never touched. Health data is never stored by the service worker; offline reading
 *   uses the opt-in, sign-out-cleared copy kept by the app itself.
 */

const CACHE = `medspace-${VERSION}`;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.filter((k) => k.startsWith("medspace-") && k !== CACHE).map((k) => caches.delete(k)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith("/api/")) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => caches.match("/", { cacheName: CACHE, ignoreVary: true })),
    );
    return;
  }
  // Assets are content-hashed, so the URL alone identifies them. ignoreVary matters: module
  // scripts are CORS requests with an Origin header, and servers often send "Vary: Origin".
  event.respondWith(
    caches
      .match(request.url, { cacheName: CACHE, ignoreVary: true })
      .then((hit) => hit || fetch(request)),
  );
});

// ---- Dose reminders (ADR-028) ----------------------------------------------------------------
self.addEventListener("push", (event) => {
  let data;
  try {
    data = event.data ? event.data.json() : {};
  } catch {
    data = { body: event.data?.text() };
  }
  event.waitUntil(
    self.registration.showNotification(data.title || "MedSpace", {
      body: data.body || "",
      tag: data.tag,
      renotify: Boolean(data.tag),
      icon: "/icons/icon-192.png",
      badge: "/icons/icon-192.png",
      data: { url: data.url || "/app", token: data.token || null },
      actions: data.token && Array.isArray(data.actions) ? data.actions : [],
    }),
  );
});

self.addEventListener("notificationclick", (event) => {
  const { url = "/app", token } = event.notification.data || {};
  event.notification.close();
  const openApp = () =>
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((windows) => {
      const open = windows.find((w) => new URL(w.url).origin === self.location.origin);
      if (open) return open.focus().then((w) => (w && "navigate" in w ? w.navigate(url) : w));
      return self.clients.openWindow(url);
    });

  if (token && (event.action === "taken" || event.action === "skipped")) {
    // The signed token is the credential: no cookies, so no session is needed or exposed.
    event.waitUntil(
      fetch("/api/push/actions", {
        method: "POST",
        credentials: "omit",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, action: event.action }),
      })
        .then((r) => {
          if (!r.ok) throw new Error(String(r.status));
        })
        .catch(openApp),
    );
    return;
  }
  event.waitUntil(openApp());
});
