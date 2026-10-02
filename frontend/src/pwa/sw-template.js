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
