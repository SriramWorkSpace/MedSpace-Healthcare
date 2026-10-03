import { useState } from "react";
import { toast } from "sonner";
import { UserPlus } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { Dialog } from "@/components/ui/Dialog";
import { Field, Input, Select } from "@/components/ui/Field";
import { Skeleton } from "@/components/ui/Skeleton";
import { formatDate } from "@/lib/format";
import { useCircle, useInvite, useRemoveLink, useSetRole } from "./api";

const ROLE_HELP = {
  viewer: "Can read your medicines, schedule, labs, documents and visit preps.",
  helper: "Can also tick doses, complete to-dos and update supply counts.",
};

function CopyInvite({ created, onClose }) {
  const [copied, setCopied] = useState(false);
  return (
    <Dialog
      open
      onClose={onClose}
      title="Send this invitation link"
      description={`Only ${created.link.person.email} can accept it, after signing in to MedSpace. It works once and expires in 7 days.`}
      footer={<Button onClick={onClose}>Done</Button>}
    >
      <div className="flex items-center gap-2 rounded-[var(--radius-control)] border border-line-strong bg-surface-2 p-1.5 pl-3">
        <label htmlFor="invite-url" className="sr-only">
          Invitation link
        </label>
        <input
          id="invite-url"
          readOnly
          value={created.url}
          onFocus={(e) => e.target.select()}
          className="min-w-0 flex-1 bg-transparent font-mono text-xs outline-none"
        />
        <Button
          size="sm"
          variant="secondary"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(created.url);
              setCopied(true);
            } catch {
              toast.error("Copy failed. Select the link and copy it manually.");
            }
          }}
        >
          {copied ? "Copied" : "Copy"}
        </Button>
      </div>
    </Dialog>
  );
}

/** Settings section: who can see (or help with) my records, and whose records I can open. */
export function CareCircleSettings() {
  const { data, isPending } = useCircle();
  const invite = useInvite();
  const setRole = useSetRole();
  const remove = useRemoveLink();
  const [email, setEmail] = useState("");
  const [role, setRoleChoice] = useState("viewer");
  const [created, setCreated] = useState(null);
  const [removing, setRemoving] = useState(null);

  const submit = (e) => {
    e.preventDefault();
    invite.mutate(
      { email: email.trim(), role },
      {
        onSuccess: (res) => {
          setCreated(res);
          setEmail("");
        },
        onError: (err) => toast.error(err.message),
      },
    );
  };

  if (isPending) return <Skeleton className="h-48 rounded-card" />;
  const caregivers = data?.caregivers ?? [];
  const caringFor = data?.caring_for ?? [];

  return (
    <div className="grid grid-cols-1 gap-4">
      <form onSubmit={submit} className="card grid grid-cols-1 gap-4 p-5">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-[minmax(0,1fr)_160px]">
          <Field label="Their email">
            <Input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
            />
          </Field>
          <Field label="Access">
            <Select value={role} onChange={(e) => setRoleChoice(e.target.value)}>
              <option value="viewer">Viewer</option>
              <option value="helper">Helper</option>
            </Select>
          </Field>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <p className="text-sm text-ink-3">{ROLE_HELP[role]}</p>
          <Button type="submit" loading={invite.isPending} disabled={!email.trim()}>
            <UserPlus size={15} /> Create invitation
          </Button>
        </div>
      </form>

      {caregivers.length > 0 && (
        <ul className="card divide-y divide-line" aria-label="People with access to your records">
          {caregivers.map((c) => (
            <li key={c.id} className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center">
              <div className="min-w-0 flex-1">
                <p className="flex flex-wrap items-center gap-2 font-medium">
                  <span className="truncate">{c.person.name}</span>
                  <span className={c.status === "active" ? "chip chip--accent" : "chip"}>
                    {c.status === "pending"
                      ? "Invited"
                      : c.status === "expired"
                        ? "Invitation expired"
                        : "Active"}
                  </span>
                </p>
                <p className="truncate text-xs text-ink-3">
                  {[
                    c.person.name !== c.person.email && c.person.email,
                    c.status === "pending" &&
                      `Invitation expires ${formatDate(c.expires_at, "MMM d")}`,
                  ]
                    .filter(Boolean)
                    .join(" · ")}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <label htmlFor={`role-${c.id}`} className="sr-only">
                  Access for {c.person.name}
                </label>
                <Select
                  id={`role-${c.id}`}
                  value={c.role}
                  disabled={c.status !== "active"}
                  onChange={(e) =>
                    setRole.mutate(
                      { id: c.id, role: e.target.value },
                      {
                        onSuccess: () => toast(`Access updated for ${c.person.name}`),
                        onError: (err) => toast.error(err.message),
                      },
                    )
                  }
                  className="w-32"
                >
                  <option value="viewer">Viewer</option>
                  <option value="helper">Helper</option>
                </Select>
                <Button variant="ghost" size="sm" onClick={() => setRemoving(c)}>
                  {c.status === "active" ? "Remove" : "Withdraw"}
                </Button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {caringFor.length > 0 && (
        <div className="card p-4">
          <p className="text-sm font-medium">You help</p>
          <ul className="mt-2 grid grid-cols-1 gap-2">
            {caringFor.map((c) => (
              <li key={c.id} className="flex items-center justify-between gap-3 text-sm">
                <span>
                  {c.person.name}{" "}
                  <span className="text-ink-3">
                    as a {c.role}. Switch to their records from your account menu.
                  </span>
                </span>
                <Button variant="ghost" size="sm" onClick={() => setRemoving(c)}>
                  Leave
                </Button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {created && <CopyInvite created={created} onClose={() => setCreated(null)} />}
      <ConfirmDialog
        open={Boolean(removing)}
        onClose={() => setRemoving(null)}
        title={
          removing && caringFor.includes(removing)
            ? `Stop helping ${removing.person.name}?`
            : `Remove ${removing?.person.name ?? ""}?`
        }
        description={
          removing && caringFor.includes(removing)
            ? "You won't be able to open their records until they invite you again."
            : "They lose access straight away. Your records are not changed."
        }
        confirmLabel={removing && caringFor.includes(removing) ? "Leave" : "Remove"}
        loading={remove.isPending}
        onConfirm={() =>
          remove.mutate(removing.id, {
            onSuccess: () => {
              toast("Care circle updated");
              setRemoving(null);
            },
            onError: (err) => toast.error(err.message),
          })
        }
      />
    </div>
  );
}
