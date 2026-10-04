import { useCallback, useSyncExternalStore } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getActing, onActingChange, setActing } from "@/lib/acting";

export const circleKeys = { all: ["circle"], invite: (token) => ["circle", "invite", token] };

export function useCircle({ enabled = true } = {}) {
  return useQuery({ queryKey: circleKeys.all, queryFn: () => api.get("/api/circle"), enabled });
}

export function useInvitePreview(token) {
  return useQuery({
    queryKey: circleKeys.invite(token),
    queryFn: () => api.get(`/api/circle/invites/${token}`),
    retry: false,
  });
}

function useCircleMutation(fn) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: fn,
    onSuccess: () => qc.invalidateQueries({ queryKey: circleKeys.all }),
  });
}

export const useInvite = () => useCircleMutation((body) => api.post("/api/circle/invites", body));
export const useAccept = () =>
  useCircleMutation((token) => api.post("/api/circle/accept", { token }));
export const useSetRole = () =>
  useCircleMutation(({ id, role }) => api.patch(`/api/circle/${id}`, { role }));
export const useRemoveLink = () => useCircleMutation((id) => api.delete(`/api/circle/${id}`));
/** Dose alerts about someone you help (ADR-032): null, 0 (when due), 30 or 60 minutes. */
export const useSetAlerts = () =>
  useCircleMutation(({ id, minutes }) => api.put(`/api/circle/${id}/alerts`, { minutes }));

/**
 * The profile this tab is showing. `readOnly` for viewers, `canHelp` for helpers; both false
 * on your own records (where everything is allowed).
 */
export function useActing() {
  const acting = useSyncExternalStore(onActingChange, getActing, () => null);
  return {
    acting,
    isActing: Boolean(acting),
    canHelp: acting?.role === "helper",
    readOnly: acting?.role === "viewer",
  };
}

/** Switch profiles: drop every cached query so nothing from the other profile lingers. */
export function useSwitchProfile() {
  const qc = useQueryClient();
  return useCallback(
    (person) => {
      setActing(person);
      const me = qc.getQueryData(["auth", "me"]);
      qc.clear();
      qc.setQueryData(["auth", "me"], me);
    },
    [qc],
  );
}
