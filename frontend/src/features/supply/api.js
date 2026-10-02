import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const supplyKeys = { all: ["supply"] };

export function useSupplies() {
  return useQuery({ queryKey: supplyKeys.all, queryFn: () => api.get("/api/supply") });
}

function useSupplyMutation(fn) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: fn,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: supplyKeys.all });
      qc.invalidateQueries({ queryKey: ["dashboard"] });
      qc.invalidateQueries({ queryKey: ["visits"] });
    },
  });
}

export function useSetSupply() {
  return useSupplyMutation(({ medicationId, ...body }) =>
    api.put(`/api/supply/${medicationId}`, body),
  );
}

export function useRefill() {
  return useSupplyMutation(({ medicationId, added }) =>
    api.post(`/api/supply/${medicationId}/refill`, { added }),
  );
}

export function useClearSupply() {
  return useSupplyMutation((medicationId) => api.delete(`/api/supply/${medicationId}`));
}
