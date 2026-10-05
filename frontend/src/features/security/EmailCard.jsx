import { useState } from "react";
import { toast } from "sonner";
import { EnvelopeSimple } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Dialog } from "@/components/ui/Dialog";
import { Field, Input } from "@/components/ui/Field";
import { CodeInput, PasswordInput } from "@/components/ui/PasswordInput";
import { useAuth } from "@/lib/auth";
import { useCancelEmailChange, useRequestEmailChange } from "./api";

function ChangeEmailDialog({ state, onClose }) {
  const request = useRequestEmailChange();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");

  return (
    <Dialog
      open
      onClose={onClose}
      title="Change your email"
      description="We'll send a link to the new address. Your account moves to it only when you open that link, and your current address is told."
    >
      <form
        className="grid grid-cols-1 gap-4"
        onSubmit={(e) => {
          e.preventDefault();
          request.mutate(
            { new_email: email.trim(), password, code: state.mfa_enabled ? code : null },
            {
              onSuccess: () => {
                toast.success("Check your new inbox", {
                  description: `Open the link we sent to ${email.trim()} to finish.`,
                });
                onClose();
              },
            },
          );
        }}
      >
        {request.error && (
          <p role="alert" className="text-sm text-danger-ink">
            {request.error.message}
          </p>
        )}
        <Field label="New email">
          <Input
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoFocus
          />
        </Field>
        <Field label="Current password">
          <PasswordInput
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Field>
        {state.mfa_enabled && (
          <Field label="Code from your app">
            <CodeInput value={code} onChange={(e) => setCode(e.target.value)} />
          </Field>
        )}
        <div className="flex justify-end gap-2">
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="submit"
            loading={request.isPending}
            disabled={!email.trim() || !password || (state.mfa_enabled && code.trim().length < 6)}
          >
            Send link
          </Button>
        </div>
      </form>
    </Dialog>
  );
}

/** Settings, Security: the sign-in address, and moving the account to another one (ADR-033). */
export function EmailCard({ state }) {
  const { user } = useAuth();
  const cancel = useCancelEmailChange();
  const [open, setOpen] = useState(false);

  return (
    <div className="card card--flat p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <span className="grid size-10 shrink-0 place-items-center rounded-xl bg-surface-2 text-ink-3">
          <EnvelopeSimple size={20} />
        </span>
        <div className="min-w-0 flex-1">
          <p className="font-medium">Email address</p>
          <p className="mt-1 truncate text-sm text-ink-2">{user.email}</p>
          {state.pending_email && (
            <p className="mt-2 text-sm text-warn-ink">
              Waiting for you to confirm{" "}
              <span className="font-medium break-all">{state.pending_email}</span>. Open the link we
              sent there; until then, nothing changes.
            </p>
          )}
          {!state.has_password && !user.is_demo && (
            <p className="mt-2 text-sm text-ink-3">
              Add a password below before changing your email.
            </p>
          )}
        </div>
        {!user.is_demo && (
          <div className="flex flex-wrap gap-2">
            {state.pending_email && (
              <Button
                variant="ghost"
                size="sm"
                loading={cancel.isPending}
                onClick={() =>
                  cancel.mutate(undefined, {
                    onSuccess: () => toast("Email change cancelled"),
                    onError: (e) => toast.error(e.message),
                  })
                }
              >
                Cancel change
              </Button>
            )}
            <Button
              variant="secondary"
              size="sm"
              disabled={!state.has_password}
              onClick={() => setOpen(true)}
            >
              {state.pending_email ? "Use another" : "Change"}
            </Button>
          </div>
        )}
      </div>
      {open && <ChangeEmailDialog state={state} onClose={() => setOpen(false)} />}
    </div>
  );
}
