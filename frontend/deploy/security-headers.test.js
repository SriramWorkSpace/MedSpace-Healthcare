import { readFileSync } from "node:fs";
import { SECURITY_HEADERS } from "./security-headers.js";

const read = (path) => readFileSync(new URL(path, import.meta.url), "utf8");

describe("security headers", () => {
  it("vercel.json carries exactly the shared headers", () => {
    const vercel = JSON.parse(read("../vercel.json"));
    const sent = Object.fromEntries(vercel.headers[0].headers.map((h) => [h.key, h.value]));
    expect(sent).toEqual(SECURITY_HEADERS);
  });

  it("vercel.json uses only keys Vercel's schema accepts", () => {
    // Vercel rejects the project on any unknown top-level key (even "$comment").
    const vercel = JSON.parse(read("../vercel.json"));
    expect(Object.keys(vercel).sort()).toEqual(["headers", "rewrites"]);
  });

  it("nginx sends every shared header on HTML", () => {
    const nginx = read("./nginx.conf.template");
    for (const [key, value] of Object.entries(SECURITY_HEADERS)) {
      expect(nginx).toContain(`add_header ${key} "${value}" always;`);
    }
  });

  it("allows no inline or remote script", () => {
    const csp = SECURITY_HEADERS["Content-Security-Policy"];
    expect(csp).toContain("script-src 'self';");
    expect(csp).not.toMatch(/script-src[^;]*(unsafe|https?:)/);
    expect(read("../index.html")).not.toMatch(/<script>(?!\s*<\/script>)/);
  });
});
