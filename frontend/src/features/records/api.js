import { useInfiniteQuery, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const recordKeys = {
  all: ["records"],
  prescriptions: ["records", "prescriptions"],
  prescription: (id) => ["records", "prescription", id],
  medications: (status) => ["records", "medications", status ?? "all"],
  careActions: (openOnly) => ["records", "care-actions", openOnly ? "open" : "all"],
};

export function useDashboard() {
  return useQuery({ queryKey: ["dashboard"], queryFn: () => api.get("/api/dashboard") });
}

export function usePrescriptions() {
  return useQuery({ queryKey: recordKeys.prescriptions, queryFn: () => api.get("/api/prescriptions") });
}

export function usePrescription(id) {
  return useQuery({
    queryKey: recordKeys.prescription(id),
    queryFn: () => api.get(`/api/prescriptions/${id}`),
  });
}

export function useMedications(status) {
  return useQuery({
    queryKey: recordKeys.medications(status),
    queryFn: () => api.get(`/api/medications${status ? `?status=${status}` : ""}`),
  });
}

export function useCareActions(openOnly = false) {
  return useQuery({
    queryKey: recordKeys.careActions(openOnly),
    queryFn: () => api.get(`/api/care-actions${openOnly ? "?open_only=true" : ""}`),
  });
}

function useInvalidateRecords() {
  const qc = useQueryClient();
  return () => {
    qc.invalidateQueries({ queryKey: recordKeys.all });
    qc.invalidateQueries({ queryKey: ["dashboard"] });
    qc.invalidateQueries({ queryKey: ["timeline"] });
  };
}

export function useUpdateMedication() {
  const invalidate = useInvalidateRecords();
  return useMutation({
    mutationFn: ({ id, ...body }) => api.patch(`/api/medications/${id}`, body),
    onSuccess: invalidate,
  });
}

export function useUpdateCareAction() {
  const qc = useQueryClient();
  const invalidate = useInvalidateRecords();
  return useMutation({
    mutationFn: ({ id, ...body }) => api.patch(`/api/care-actions/${id}`, body),
    // Optimistic tick: the checkbox responds instantly; we roll back if the server disagrees.
    onMutate: async ({ id, completed }) => {
      await qc.cancelQueries({ queryKey: recordKeys.all });
      const snapshots = qc.getQueriesData({ queryKey: ["records", "care-actions"] });
      for (const [key, data] of snapshots) {
        if (!Array.isArray(data)) continue;
        qc.setQueryData(
          key,
          data.map((a) =>
            a.id === id ? { ...a, completed_at: completed ? new Date().toISOString() : null } : a,
          ),
        );
      }
      return { snapshots };
    },
    onError: (_err, _vars, ctx) => ctx?.snapshots.forEach(([key, data]) => qc.setQueryData(key, data)),
    onSettled: invalidate,
  });
}

export function useTimeline(types) {
  const typeKey = [...(types ?? [])].sort().join(",");
  return useInfiniteQuery({
    queryKey: ["timeline", typeKey],
    initialPageParam: null,
    queryFn: ({ pageParam }) => {
      const qs = new URLSearchParams({ limit: "40" });
      if (typeKey) qs.set("types", typeKey);
      if (pageParam) qs.set("before", pageParam);
      return api.get(`/api/timeline?${qs}`);
    },
    getNextPageParam: (last) => last.next_cursor ?? undefined,
  });
}
