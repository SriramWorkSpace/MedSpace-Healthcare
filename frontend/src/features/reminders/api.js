import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const pushKeys = {
  config: ["push", "config"],
  settings: ["push", "settings"],
};

export const usePushConfig = () =>
  useQuery({ queryKey: pushKeys.config, queryFn: () => api.get("/api/push/config") });

export const usePushSettings = () =>
  useQuery({ queryKey: pushKeys.settings, queryFn: () => api.get("/api/push/settings") });

export function useSavePushSettings() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body) => api.put("/api/push/settings", body),
    onSuccess: (data) => qc.setQueryData(pushKeys.settings, data),
  });
}

export const useSendTest = () => useMutation({ mutationFn: () => api.post("/api/push/test") });
