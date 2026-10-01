/**
 * Thin fetch wrapper for the MedSpace API.
 * - Same-origin `/api` (Vite proxy in dev, reverse proxy in prod) so cookies stay first-party.
 * - Sends the CSRF double-submit header on unsafe methods.
 * - On 401, performs ONE shared refresh attempt and retries the request.
 */

const BASE = import.meta.env.VITE_API_URL ?? "";
const UNSAFE = new Set(["POST", "PUT", "PATCH", "DELETE"]);
const NO_REFRESH = ["/api/auth/login", "/api/auth/signup", "/api/auth/demo", "/api/auth/refresh"];

export class ApiError extends Error {
  /** @param {number} status @param {any} problem */
  constructor(status, problem) {
    super(problem?.detail || problem?.title || `Request failed (${status})`);
    this.name = "ApiError";
    this.status = status;
    this.code = problem?.code;
    this.problem = problem;
  }

  /** Field errors from a 422 problem, keyed by the last path segment. */
  get fieldErrors() {
    const out = {};
    for (const e of this.problem?.errors ?? []) {
      const key = e.loc?.[e.loc.length - 1];
      if (key) out[key] = e.msg;
    }
    return out;
  }
}

export function readCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

let refreshing = null;
let onSessionExpired = () => {};

export function setSessionExpiredHandler(fn) {
  onSessionExpired = fn;
}

export async function refreshSession() {
  refreshing ??= fetch(`${BASE}/api/auth/refresh`, {
    method: "POST",
    credentials: "include",
    headers: { "X-CSRF-Token": readCookie("ms_csrf") ?? "" },
  })
    .then((r) => r.ok)
    .catch(() => false)
    .finally(() => {
      setTimeout(() => (refreshing = null), 0);
    });
  return refreshing;
}

/**
 * @param {string} path
 * @param {{ method?: string, body?: any, signal?: AbortSignal, headers?: Record<string,string>, raw?: boolean }} [opts]
 */
export async function api(path, opts = {}) {
  const method = (opts.method ?? "GET").toUpperCase();
  const isForm = typeof FormData !== "undefined" && opts.body instanceof FormData;

  const doFetch = () => {
    const headers = { Accept: "application/json", ...opts.headers };
    if (opts.body !== undefined && !isForm) headers["Content-Type"] = "application/json";
    if (UNSAFE.has(method)) headers["X-CSRF-Token"] = readCookie("ms_csrf") ?? "";
    return fetch(`${BASE}${path}`, {
      method,
      credentials: "include",
      headers,
      signal: opts.signal,
      body: opts.body === undefined ? undefined : isForm ? opts.body : JSON.stringify(opts.body),
    });
  };

  let res = await doFetch();
  if (res.status === 401 && readCookie("ms_csrf") && !NO_REFRESH.some((p) => path.startsWith(p))) {
    const ok = await refreshSession();
    if (ok) {
      res = await doFetch();
    } else {
      onSessionExpired();
    }
  }

  if (opts.raw) return res;
  if (res.status === 204) return null;

  const isJson = res.headers.get("content-type")?.includes("json");
  const data = isJson ? await res.json().catch(() => null) : await res.text();
  if (!res.ok) throw new ApiError(res.status, isJson ? data : { detail: data });
  return data;
}

api.get = (path, opts) => api(path, { ...opts, method: "GET" });
api.post = (path, body, opts) => api(path, { ...opts, method: "POST", body });
api.patch = (path, body, opts) => api(path, { ...opts, method: "PATCH", body });
api.put = (path, body, opts) => api(path, { ...opts, method: "PUT", body });
api.delete = (path, opts) => api(path, { ...opts, method: "DELETE" });
