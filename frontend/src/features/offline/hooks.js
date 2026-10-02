import { useSyncExternalStore } from "react";
import { onlineManager, useMutationState } from "@tanstack/react-query";
import { getSavedAt, onSavedAtChange } from "@/lib/offline";
import { getInstallPrompt, onInstallPromptChange } from "@/lib/install";

export function useOnline() {
  return useSyncExternalStore(
    (cb) => onlineManager.subscribe(cb),
    () => onlineManager.isOnline(),
    () => true,
  );
}

/** When this device's offline copy was last written (ms), or null. */
export function useSavedAt() {
  return useSyncExternalStore(onSavedAtChange, getSavedAt, () => null);
}

export function useInstallPrompt() {
  return useSyncExternalStore(onInstallPromptChange, getInstallPrompt, () => null);
}

/** Dose ticks made while offline that haven't reached the server yet. */
export function usePendingDoseTicks() {
  return useMutationState({
    filters: { mutationKey: ["dose"], predicate: (m) => m.state.isPaused },
  }).length;
}
