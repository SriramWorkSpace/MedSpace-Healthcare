import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useAuthProviders() {
  return useQuery({
    queryKey: ["auth", "providers"],
    queryFn: () => api.get("/api/auth/google/providers"),
    staleTime: Infinity,
  });
}

export const GOOGLE_ERRORS = {
  denied: "Google sign-in was cancelled.",
  email_taken:
    "An account with that email already exists. Sign in with your password, then connect Google from Settings.",
  expired: "That took a little too long. Please try Google sign-in again.",
  error: "Google sign-in didn't work this time. Please try again.",
};
