import { Link, useNavigate, useParams } from "react-router";
import { toast } from "sonner";
import { UsersThree } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { useAccept, useInvitePreview, useSwitchProfile } from "@/features/circle/api";
import { useAuth } from "@/lib/auth";
import { useResendVerification } from "@/features/auth/useResendVerification";

const ROLE_TEXT = {
  viewer: "read their medicines, schedule, lab results, documents and visit preps",
  helper: "read their records, and tick doses, complete to-dos and update supply counts for them",
};

export default function CircleAccept() {
  const { token } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const preview = useInvitePreview(token);
  const accept = useAccept();
  const switchProfile = useSwitchProfile();
  const resend = useResendVerification();

  if (preview.isPending) {
    return (
      <LoadingRegion label="Loading invitation" className="mx-auto max-w-lg pt-10">
        <Skeleton className="h-64 rounded-card" />
      </LoadingRegion>
    );
  }
  if (preview.isError) {
    return (
      <EmptyState
        icon={UsersThree}
        title="This invitation doesn't exist"
        description="It may have been withdrawn, or the link was copied incompletely."
        action={
          <Button as={Link} to="/app">
            Go to your dashboard
          </Button>
        }
      />
    );
  }

  const inv = preview.data;
  const wrongAccount = user && user.email.toLowerCase() !== inv.email.toLowerCase();
  const unusable = inv.status !== "pending";
  const unverified = user && !user.email_verified;

  return (
    <div className="mx-auto max-w-lg pt-6">
      <div className="card p-6 text-center sm:p-8">
        <span className="mx-auto grid size-12 place-items-center rounded-2xl bg-accent-soft text-accent-soft-ink">
          <UsersThree size={24} weight="duotone" />
        </span>
        <h1 className="mt-4 text-2xl font-semibold tracking-tight">
          {inv.owner_name} invited you to their care circle
        </h1>
        <p className="mt-2 text-ink-2">
          As a <strong>{inv.role}</strong> you can {ROLE_TEXT[inv.role]}. They can change or end
          this at any time.
        </p>
        {unusable ? (
          <p className="mt-6 rounded-[var(--radius-control)] bg-surface-2 p-3 text-sm text-ink-2">
            {inv.status === "expired"
              ? "This invitation has expired. Ask for a new one."
              : "This invitation has already been used or withdrawn."}
          </p>
        ) : wrongAccount ? (
          <p className="mt-6 rounded-[var(--radius-control)] bg-warn-soft p-3 text-sm text-warn-ink">
            This invitation is for {inv.email}, but you're signed in as {user.email}. Sign in with
            that account to accept it.
          </p>
        ) : unverified ? (
          <div className="mt-6 rounded-[var(--radius-control)] bg-warn-soft p-3 text-sm text-warn-ink">
            <p>
              Confirm your email address first. We sent a link to {user.email}; open it, then come
              back to this page.
            </p>
            <Button
              size="sm"
              variant="secondary"
              className="mt-3"
              loading={resend.isPending}
              onClick={() => resend.mutate()}
            >
              Resend link
            </Button>
          </div>
        ) : (
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            <Button
              loading={accept.isPending}
              onClick={() =>
                accept.mutate(token, {
                  onSuccess: (link) => {
                    toast(`You can now open ${link.person.name}'s records`);
                    switchProfile({ ...link.person, role: link.role });
                    navigate("/app", { replace: true });
                  },
                  onError: (e) => toast.error(e.message),
                })
              }
            >
              Accept and open their records
            </Button>
            <Button as={Link} to="/app" variant="ghost">
              Not now
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
