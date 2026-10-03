import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/lib/api";

/** Send a fresh confirmation link (older links stop working). */
export function useResendVerification() {
  return useMutation({
    mutationFn: () => api.post("/api/me/email/verification"),
    onSuccess: () => toast.success("Link sent", { description: "Check your inbox." }),
    onError: (e) => toast.error(e.message),
  });
}
