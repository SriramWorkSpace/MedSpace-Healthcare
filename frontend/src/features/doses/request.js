import { api } from "@/lib/api";

/**
 * The dose-mark request, registered as the default for mutations keyed ["dose"] so ticks made
 * offline can resume after a reload (the function itself can't be stored with them).
 */
export function doseRequest({ medication_id, date, time, status }) {
  return status
    ? api.put("/api/doses", { medication_id, date, time, status })
    : api.delete(
        `/api/doses?medication_id=${medication_id}&date=${date}&time=${encodeURIComponent(time)}`,
      );
}
