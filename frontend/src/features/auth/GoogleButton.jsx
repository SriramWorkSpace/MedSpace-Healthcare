import { useState } from "react";
import { useSearchParams } from "react-router";
import { GoogleLogo } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { useAuthProviders } from "./googleAuth";

/**
 * "Continue with Google": signs in (or creates an account) and, in the same consent screen,
 * asks for Calendar and Tasks so reminders work right away. People can untick those and
 * connect later from Settings.
 */
export function GoogleButton() {
  const [params] = useSearchParams();
  const providers = useAuthProviders();
  const [leaving, setLeaving] = useState(false);
  const simulated = providers.data?.google?.mode === "simulation";
  const testersOnly = providers.data?.google?.testers_only;

  const start = () => {
    setLeaving(true);
    const next = params.get("next") || "/app";
    window.location.assign(`/api/auth/google/start?next=${encodeURIComponent(next)}`);
  };

  return (
    <div className="grid gap-2">
      <Button variant="secondary" className="w-full" loading={leaving} onClick={start}>
        {!leaving && <GoogleLogo size={17} weight="bold" />}
        Continue with Google
      </Button>
      <p className="text-center text-xs text-ink-3">
        {simulated
          ? "Simulated on this server, so no Google account is needed."
          : testersOnly
            ? "Google sign-in is open to invited testers for now. Everyone else can use email or the demo."
            : "Also offers Calendar and Tasks access for reminders. You can skip that and connect later."}
      </p>
    </div>
  );
}
