import { EnvelopeSimple } from "@phosphor-icons/react";
import { useAuth } from "@/lib/auth";
import { useResendVerification } from "./useResendVerification";

/** Shown until the account's email is confirmed (never for demo accounts). */
export function VerifyEmailBanner() {
  const { user } = useAuth();
  const resend = useResendVerification();
  if (!user || user.email_verified || user.is_demo) return null;

  return (
    <aside
      aria-label="Confirm your email"
      className="no-print border-b border-line bg-warn-soft px-4 py-2 text-center text-[13px] text-warn-ink"
    >
      <EnvelopeSimple size={14} className="mr-1.5 inline-block align-[-2px]" />
      Confirm <span className="font-medium">{user.email}</span> to reset your password by email and
      accept care circle invitations.{" "}
      <button
        type="button"
        className="tap font-semibold underline underline-offset-2 disabled:opacity-60"
        disabled={resend.isPending}
        onClick={() => resend.mutate()}
      >
        {resend.isPending ? "Sending..." : "Resend link"}
      </button>
    </aside>
  );
}
