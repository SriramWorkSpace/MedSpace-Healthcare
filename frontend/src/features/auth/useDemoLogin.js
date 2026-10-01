import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

/** One-click demo: creates an isolated synthetic account and lands on the dashboard. */
export function useDemoLogin() {
  const { setSession } = useAuth();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: () => api.post("/api/auth/demo"),
    onSuccess: (session) => {
      setSession(session);
      navigate("/app", { replace: true });
    },
    onError: (err) => {
      toast.error("The demo is taking a sick day", {
        description: err.message || "Please try again in a moment.",
      });
    },
  });
}
