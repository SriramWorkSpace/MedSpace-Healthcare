import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { fileURLToPath, URL } from "node:url";
import { createHash } from "node:crypto";
import { readdirSync, readFileSync } from "node:fs";
import { SECURITY_HEADERS } from "./deploy/security-headers.js";

/**
 * Emits /sw.js at build time: the template from src/pwa plus a version and the list of every
 * built asset, so each deploy ships a worker that precaches exactly its own files (ADR-025).
 */
function serviceWorker() {
  const publicFiles = (dir, prefix = "") =>
    readdirSync(new URL(dir, import.meta.url), { withFileTypes: true }).flatMap((e) =>
      e.isDirectory()
        ? publicFiles(`${dir}${e.name}/`, `${prefix}${e.name}/`)
        : [`/${prefix}${e.name}`],
    );
  return {
    name: "medspace-service-worker",
    apply: "build",
    generateBundle(_options, bundle) {
      const built = Object.keys(bundle)
        .filter((f) => /\.(js|css|woff2?|svg|png)$/.test(f))
        .map((f) => `/${f}`);
      const precache = ["/", ...publicFiles("./public/"), ...built];
      const version = createHash("sha256").update(precache.join("\n")).digest("hex").slice(0, 12);
      const template = readFileSync(new URL("./src/pwa/sw-template.js", import.meta.url), "utf8");
      this.emitFile({
        type: "asset",
        fileName: "sw.js",
        source: `const VERSION = "${version}";\nconst PRECACHE = ${JSON.stringify(precache)};\n${template}`,
      });
    },
  };
}

// The SPA calls the API same-origin through this proxy so auth cookies stay first-party.
const apiTarget = process.env.VITE_API_PROXY || "http://localhost:8000";

export default defineConfig({
  plugins: [react(), tailwindcss(), serviceWorker()],
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
  server: {
    port: 5173,
    // File events don't cross Docker bind mounts on Windows/macOS; poll inside containers.
    watch:
      process.env.VITE_USE_POLLING === "true" ? { usePolling: true, interval: 300 } : undefined,
    // xfwd: pass the browser's address as X-Forwarded-For (the API trusts one hop).
    proxy: { "/api": { target: apiTarget, changeOrigin: false, xfwd: true } },
  },
  preview: {
    port: 4173,
    // The production headers, so e2e runs against the real CSP (dev keeps Vite's inline HMR).
    headers: SECURITY_HEADERS,
    proxy: { "/api": { target: apiTarget, changeOrigin: false, xfwd: true } },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.js"],
    exclude: ["e2e/**", "node_modules/**"],
    css: false,
  },
});
