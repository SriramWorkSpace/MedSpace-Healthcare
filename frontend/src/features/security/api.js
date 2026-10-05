import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { meKey } from "@/lib/auth";

export const securityKeys = {
  all: ["security"],
};

export function useSecurity() {
  return useQuery({ queryKey: securityKeys.all, queryFn: () => api.get("/api/me/security") });
}

function useSecurityMutation(mutationFn) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn,
    onSettled: () => {
      qc.invalidateQueries({ queryKey: securityKeys.all });
      qc.invalidateQueries({ queryKey: meKey });
    },
  });
}

export const useStartMfa = () => useMutation({ mutationFn: () => api.post("/api/me/mfa/setup") });
export const useEnableMfa = () =>
  useSecurityMutation((code) => api.post("/api/me/mfa/enable", { code }));
export const useDisableMfa = () =>
  useSecurityMutation((body) => api.post("/api/me/mfa/disable", body));
export const useNewRecoveryCodes = () =>
  useSecurityMutation((code) => api.post("/api/me/mfa/recovery-codes", { code }));
export const useEndSession = () =>
  useSecurityMutation((id) => api.delete(`/api/me/sessions/${id}`));
export const useEndOtherSessions = () =>
  useSecurityMutation(() => api.post("/api/me/sessions/sign-out-others"));
export const useChangePassword = () =>
  useSecurityMutation((body) => api.post("/api/me/password", body));
export const useRequestEmailChange = () =>
  useSecurityMutation((body) => api.post("/api/me/email/change", body));
export const useCancelEmailChange = () =>
  useSecurityMutation(() => api.delete("/api/me/email/change"));
