/**
 * Offline copy of the user's records on this device (ADR-025).
 *
 * Opt-in per device. When on, a snapshot of selected query data (and dose ticks still waiting to
 * sync) is kept in IndexedDB and restored before the app renders, so records stay readable without
 * a connection. It is tied to the signed-in user, expires after 7 days, and is deleted on sign-out
 * or when the setting is turned off. The service worker never stores health data.
 */
import { dehydrate, hydrate } from "@tanstack/react-query";

const DB = "medspace-offline";
const STORE = "kv";
const KEY = "snapshot";
const FLAG = "ms-offline";
export const MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000;

// Query roots worth reading offline. Not persisted: assistant threads, search, shares, audit.
const PERSISTED = new Set([
  "auth",
  "dashboard",
  "records",
  "adherence",
  "visits",
  "supply",
  "documents",
]);

let savedAt = null;
const listeners = new Set();
const emit = () => listeners.forEach((fn) => fn(savedAt));

export function onSavedAtChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}
export const getSavedAt = () => savedAt;

export function isOfflineEnabled() {
  try {
    return localStorage.getItem(FLAG) === "1";
  } catch {
    return false;
  }
}

function open() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(STORE);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function tx(mode, run) {
  const db = await open();
  try {
    return await new Promise((resolve, reject) => {
      const t = db.transaction(STORE, mode);
      const req = run(t.objectStore(STORE));
      t.oncomplete = () => resolve(req?.result);
      t.onerror = () => reject(t.error);
    });
  } finally {
    db.close();
  }
}

export async function clearOfflineCopy() {
  savedAt = null;
  emit();
  try {
    await tx("readwrite", (s) => s.delete(KEY));
  } catch {
    /* storage unavailable: nothing to clear */
  }
}

export async function setOfflineEnabled(on, queryClient) {
  try {
    localStorage.setItem(FLAG, on ? "1" : "0");
  } catch {
    /* ignore */
  }
  if (on) await saveNow(queryClient);
  else await clearOfflineCopy();
}

function currentUserId(queryClient) {
  return queryClient.getQueryData(["auth", "me"])?.id ?? null;
}

async function saveNow(queryClient) {
  const userId = currentUserId(queryClient);
  if (!userId || !isOfflineEnabled()) return;
  const state = dehydrate(queryClient, {
    shouldDehydrateQuery: (q) => q.state.status === "success" && PERSISTED.has(q.queryKey[0]),
    shouldDehydrateMutation: (m) => m.state.isPaused && m.options.mutationKey?.[0] === "dose",
  });
  const now = Date.now();
  try {
    await tx("readwrite", (s) => s.put({ userId, savedAt: now, state }, KEY));
    savedAt = now;
    emit();
  } catch {
    /* quota or private mode: keep working online */
  }
}

/** Before first render: bring back the snapshot if it belongs to a recent session. */
export async function restoreOfflineCopy(queryClient) {
  if (!isOfflineEnabled()) return;
  try {
    const snap = await tx("readonly", (s) => s.get(KEY));
    if (!snap) return;
    if (Date.now() - snap.savedAt > MAX_AGE_MS) {
      await clearOfflineCopy();
      return;
    }
    hydrate(queryClient, snap.state);
    savedAt = snap.savedAt;
    emit();
  } catch {
    /* unreadable snapshot: start fresh */
  }
}

/** Keep the snapshot current (throttled), and drop it if a different user signs in. */
export function startPersisting(queryClient) {
  let timer = null;
  let lastUser = currentUserId(queryClient);
  const schedule = () => {
    const user = currentUserId(queryClient);
    if (lastUser && user && user !== lastUser) clearOfflineCopy();
    lastUser = user ?? lastUser;
    if (!isOfflineEnabled() || timer) return;
    timer = setTimeout(() => {
      timer = null;
      saveNow(queryClient);
    }, 1000);
  };
  const a = queryClient.getQueryCache().subscribe(schedule);
  const b = queryClient.getMutationCache().subscribe(schedule);
  return () => {
    a();
    b();
  };
}
