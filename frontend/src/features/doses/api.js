import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const doseKeys = {
  all: ["adherence"],
  window: (days) => ["adherence", "all", days],
  medication: (id, days) => ["adherence", id, days],
};

export function useAdherence(days = 14) {
  return useQuery({
    queryKey: doseKeys.window(days),
    queryFn: () => api.get(`/api/adherence?days=${days}`),
  });
}

export function useMedicationAdherence(id, days = 56) {
  return useQuery({
    queryKey: doseKeys.medication(id, days),
    queryFn: () => api.get(`/api/adherence/${id}?days=${days}`),
    retry: (count, error) => error?.status !== 404 && error?.status !== 422 && count < 2,
  });
}

/** Mark today's dashboard dose in place so the tick lands instantly. */
function patchDashboard(qc, { medication_id, date, time }, status) {
  qc.setQueryData(["dashboard"], (d) =>
    d && d.today === date
      ? {
          ...d,
          doses_today: d.doses_today.map((x) =>
            x.medication_id === medication_id && x.time === time ? { ...x, status } : x,
          ),
        }
      : d,
  );
}

/** Patch a dose inside any cached adherence history. */
function patchHistory(qc, { medication_id, date, time }, state) {
  for (const [key, data] of qc.getQueriesData({ queryKey: doseKeys.all })) {
    if (!data) continue;
    qc.setQueryData(key, {
      ...data,
      medications: data.medications.map((m) =>
        m.medication_id !== medication_id
          ? m
          : {
              ...m,
              days: m.days.map((day) =>
                day.date !== date
                  ? day
                  : {
                      ...day,
                      doses: day.doses.map((s) => (s.time === time ? { ...s, state } : s)),
                    },
              ),
            },
      ),
    });
  }
}

/**
 * Log or clear one scheduled dose. `status` is "taken", "skipped", or null to clear.
 * `fallbackState` is what a cleared dose shows in history ("unlogged" or "upcoming").
 */
export function useSetDose() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ medication_id, date, time, status }) =>
      status
        ? api.put("/api/doses", { medication_id, date, time, status })
        : api.delete(
            `/api/doses?medication_id=${medication_id}&date=${date}&time=${encodeURIComponent(time)}`,
          ),
    onMutate: async (vars) => {
      await qc.cancelQueries({ queryKey: ["dashboard"] });
      await qc.cancelQueries({ queryKey: doseKeys.all });
      const snapshot = [
        ["dashboard", qc.getQueryData(["dashboard"])],
        ...qc.getQueriesData({ queryKey: doseKeys.all }),
      ];
      patchDashboard(qc, vars, vars.status);
      patchHistory(qc, vars, vars.status ?? vars.fallbackState ?? "unlogged");
      return { snapshot };
    },
    onError: (_e, _vars, ctx) => {
      for (const [key, data] of ctx?.snapshot ?? []) {
        qc.setQueryData(Array.isArray(key) ? key : [key], data);
      }
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: doseKeys.all });
      qc.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}
