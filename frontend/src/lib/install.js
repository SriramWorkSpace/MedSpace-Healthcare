/**
 * Captures the browser's install prompt as early as possible (it fires once, often before React
 * mounts) so Settings can offer an "Install app" button.
 */
let deferred = null;
const listeners = new Set();
const emit = () => listeners.forEach((fn) => fn(deferred));

if (typeof window !== "undefined") {
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferred = event;
    emit();
  });
  window.addEventListener("appinstalled", () => {
    deferred = null;
    emit();
  });
}

export const getInstallPrompt = () => deferred;

export function onInstallPromptChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

/** Shows the browser's install dialog; resolves to true when the user accepts. */
export async function promptInstall() {
  if (!deferred) return false;
  const event = deferred;
  deferred = null;
  emit();
  await event.prompt();
  const { outcome } = await event.userChoice;
  return outcome === "accepted";
}

export function isStandalone() {
  return (
    window.matchMedia?.("(display-mode: standalone)").matches ||
    window.navigator.standalone === true
  );
}
