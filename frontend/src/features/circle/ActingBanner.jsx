import { useEffect } from "react";
import { useNavigate } from "react-router";
import { toast } from "sonner";
import { UsersThree } from "@phosphor-icons/react";
import { useActing, useCircle, useSwitchProfile } from "./api";

/**
 * Shown on every page while a caregiver views someone else's records, and the place that notices
 * when that access has been revoked.
 */
export function ActingBanner() {
  const { acting } = useActing();
  const circle = useCircle();
  const switchProfile = useSwitchProfile();
  const navigate = useNavigate();

  const stillAllowed =
    !acting || !circle.data || circle.data.caring_for.some((c) => c.person.id === acting.id);

  useEffect(() => {
    if (stillAllowed) return;
    switchProfile(null);
    toast("You no longer have access to those records", {
      description: "You're back on your own records.",
    });
    navigate("/app", { replace: true });
  }, [stillAllowed, switchProfile, navigate]);

  if (!acting) return null;
  return (
    <aside
      aria-label="Viewing someone else's records"
      className="no-print border-b border-accent/30 bg-accent px-4 py-2 text-center text-[13px] text-accent-ink"
    >
      <UsersThree size={14} className="mr-1.5 inline-block align-[-2px]" />
      Viewing <strong className="font-semibold">{acting.name}</strong>'s records as a{" "}
      {acting.role === "helper"
        ? "helper: you can tick doses, to-dos and refills"
        : "viewer (read only)"}
      .{" "}
      <button
        type="button"
        onClick={() => {
          switchProfile(null);
          navigate("/app");
        }}
        className="ml-1 rounded font-semibold underline underline-offset-2"
      >
        Back to your records
      </button>
    </aside>
  );
}
