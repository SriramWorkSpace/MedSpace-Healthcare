import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api";

function jsonResponse(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": status >= 400 ? "application/problem+json" : "application/json" },
  });
}

describe("api client", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    document.cookie = "ms_csrf=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  });

  it("sends the CSRF header on unsafe methods", async () => {
    document.cookie = "ms_csrf=tok123";
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse(200, { ok: 1 }));
    await api.post("/api/things", { a: 1 });
    const [, init] = fetchMock.mock.calls[0];
    expect(init.headers["X-CSRF-Token"]).toBe("tok123");
    expect(init.credentials).toBe("include");
    expect(init.body).toBe(JSON.stringify({ a: 1 }));
  });

  it("raises ApiError with problem details and field errors", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse(422, {
        detail: "Some fields need attention.",
        code: "validation_error",
        errors: [{ loc: ["body", "email"], msg: "bad email" }],
      }),
    );
    const err = await api.get("/api/x").catch((e) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err.status).toBe(422);
    expect(err.fieldErrors).toEqual({ email: "bad email" });
  });

  it("refreshes once on 401 and retries when a session exists", async () => {
    document.cookie = "ms_csrf=tok";
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse(401, { detail: "expired" }))
      .mockResolvedValueOnce(jsonResponse(200, {}))
      .mockResolvedValueOnce(jsonResponse(200, { items: [] }));
    const data = await api.get("/api/documents");
    expect(data).toEqual({ items: [] });
    expect(fetchMock.mock.calls[1][0]).toContain("/api/auth/refresh");
  });

  it("does not attempt a refresh for anonymous visitors", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse(401, {}));
    await expect(api.get("/api/documents")).rejects.toBeInstanceOf(ApiError);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("tells people when they can try again after a 429", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse(429, { detail: "Slow down a little.", code: "rate_limited", retry_after: 42 }),
    );
    const err = await api.get("/api/me/export").catch((e) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err.retryAfter).toBe(42);
    expect(err.message).toBe("Slow down a little. Try again in 42 seconds.");
    expect(ApiError.message(429, { detail: "Wait.", retry_after: 600 })).toBe(
      "Wait. Try again in 10 minutes.",
    );
  });
});
