import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const googleKeys = {
  status: ["google", "status"],
  preview: (rxId) => ["google", "preview", rxId],
};

export function useGoogleStatus() {
  return useQuery({
    queryKey: googleKeys.status,
    queryFn: () => api.get("/api/integrations/google/status"),
  });
}

export function useGooglePreview(prescriptionId, { enabled = true } = {}) {
  return useQuery({
    queryKey: googleKeys.preview(prescriptionId),
    queryFn: () => api.get(`/api/integrations/google/preview?prescription_id=${prescriptionId}`),
    enabled: Boolean(prescriptionId) && enabled,
  });
}

/** OAuth is a full-page redirect (Google's consent screen can't be framed). */
export function connectGoogle() {
  window.location.assign("/api/integrations/google/connect");
}

function useGoogleMutation(fn) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: fn,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["google"] });
      qc.invalidateQueries({ queryKey: ["records"] });
      qc.invalidateQueries({ queryKey: ["audit"] });
    },
  });
}

export const useSyncPrescription = () =>
  useGoogleMutation(({ prescriptionId, calendar, tasks }) =>
    api.post("/api/integrations/google/sync", { prescription_id: prescriptionId, calendar, tasks }),
  );

export const useUnsyncPrescription = () =>
  useGoogleMutation((prescriptionId) =>
    api.delete(`/api/integrations/google/sync?prescription_id=${prescriptionId}`),
  );

export const useDisconnectGoogle = () =>
  useGoogleMutation((removeItems) =>
    api.delete(`/api/integrations/google?remove_items=${removeItems ? "true" : "false"}`),
  );

export const usePullTasks = () =>
  useGoogleMutation(() => api.post("/api/integrations/google/pull"));
