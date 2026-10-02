import { useEffect } from "react";
import { useSearchParams } from "react-router";
import { toast } from "sonner";

/** After "Continue with Google", explain whether reminders are ready, then tidy the URL. */
export function useGoogleWelcome() {
  const [params, setParams] = useSearchParams();
  useEffect(() => {
    if (params.get("google") !== "signed_in") return;
    const connected = params.get("reminders") === "connected";
    toast.success("Signed in with Google", {
      id: "google-welcome", // dedupes StrictMode's double effect run in development
      description: connected
        ? "Calendar and Tasks are connected, so reminders are one click away."
        : "Want reminders later? Connect Calendar and Tasks any time from Settings.",
      duration: 6000,
    });
    const next = new URLSearchParams(params);
    next.delete("google");
    next.delete("reminders");
    setParams(next, { replace: true });
  }, [params, setParams]);
}
