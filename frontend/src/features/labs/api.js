import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const labKeys = {
  all: ["records", "labs"],
  trend: (key) => ["records", "labs", key],
};

export function useLabTrends() {
  return useQuery({ queryKey: labKeys.all, queryFn: () => api.get("/api/labs") });
}

export function useLabTrend(key) {
  return useQuery({
    queryKey: labKeys.trend(key),
    queryFn: () => api.get(`/api/labs/${encodeURIComponent(key)}`),
    retry: (count, error) => error?.status !== 404 && count < 2,
  });
}

export function useDeleteLabResult() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.delete(`/api/lab-results/${id}`),
    onSettled: () => qc.invalidateQueries({ queryKey: labKeys.all }),
  });
}
