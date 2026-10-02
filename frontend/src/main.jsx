import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router";
import { onlineManager } from "@tanstack/react-query";
import "@fontsource-variable/geist";
import "@fontsource-variable/geist-mono";
import "./styles/index.css";
import "./lib/install";
import { Providers } from "./app/providers";
import { router } from "./app/router";
import { queryClient } from "./lib/queryClient";
import { restoreOfflineCopy, startPersisting } from "./lib/offline";

// TanStack Query assumes "online" until an online/offline event fires; a page loaded without a
// connection must start paused instead of firing requests that fail.
onlineManager.setOnline(navigator.onLine);

// Restore this device's offline copy (if the user turned it on) before the first render.
await restoreOfflineCopy(queryClient);
startPersisting(queryClient);
queryClient.resumePausedMutations();

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Providers>
      <RouterProvider router={router} />
    </Providers>
  </StrictMode>,
);

if (import.meta.env.PROD && "serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      /* offline support is a bonus; the app works without it */
    });
  });
}
