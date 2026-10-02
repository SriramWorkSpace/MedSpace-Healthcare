import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const visitKeys = {
  all: ["visits"],
  one: (id) => ["visits", id],
  brief: (id) => ["visits", id, "brief"],
};

export function useVisits() {
  return useQuery({ queryKey: visitKeys.all, queryFn: () => api.get("/api/visits") });
}

export function useVisitBrief(id) {
  return useQuery({
    queryKey: visitKeys.brief(id),
    queryFn: () => api.get(`/api/visits/${id}/brief`),
    retry: (count, error) => error?.status !== 404 && error?.status !== 422 && count < 2,
  });
}

export function useCreateVisit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body) => api.post("/api/visits", body),
    onSuccess: () => qc.invalidateQueries({ queryKey: visitKeys.all, exact: true }),
  });
}

/** Patch a visit. Question edits land instantly in the cached brief, then the server confirms. */
export function useUpdateVisit(id) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (patch) => api.patch(`/api/visits/${id}`, patch),
    onMutate: async (patch) => {
      await qc.cancelQueries({ queryKey: visitKeys.brief(id) });
      const previous = qc.getQueryData(visitKeys.brief(id));
      if (previous) {
        qc.setQueryData(visitKeys.brief(id), {
          ...previous,
          visit: { ...previous.visit, ...patch },
        });
      }
      return { previous };
    },
    onError: (_e, _patch, ctx) => {
      if (ctx?.previous) qc.setQueryData(visitKeys.brief(id), ctx.previous);
    },
    onSettled: (_data, _e, patch) => {
      qc.invalidateQueries({ queryKey: visitKeys.all, exact: true });
      // Dates change what the brief covers, so it is rebuilt; question edits need no refetch.
      if (!("questions" in patch) || Object.keys(patch).length > 1) {
        qc.invalidateQueries({ queryKey: visitKeys.brief(id) });
      }
    },
  });
}

export function useDeleteVisit() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.delete(`/api/visits/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: visitKeys.all, exact: true }),
  });
}
