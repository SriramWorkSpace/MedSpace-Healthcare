import { useState } from "react";
import { toast } from "sonner";
import {
  Copy,
  Desktop,
  DeviceMobile,
  Key,
  ShieldCheck,
  ShieldSlash,
  SignOut,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { Dialog } from "@/components/ui/Dialog";
import { Field } from "@/components/ui/Field";
import { CodeInput, PasswordInput } from "@/components/ui/PasswordInput";
import { Skeleton } from "@/components/ui/Skeleton";
import { formatDate, timeAgo } from "@/lib/format";
import { EmailCard } from "./EmailCard";
import {
  useChangePassword,
  useDisableMfa,
  useEnableMfa,
  useEndOtherSessions,
  useEndSession,
  useNewRecoveryCodes,
  useSecurity,
  useStartMfa,
} from "./api";

const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

function errorText(mutation) {
  return mutation.error?.message ?? null;
}

// ---- Recovery codes (shown exactly once) ------------------------------------------------------

function RecoveryCodes({ codes, onClose }) {
  const [copied, setCopied] = useState(false);
  return (
    <Dialog
      open
      onClose={onClose}
      title="Save your recovery codes"
      description="If you lose your phone, each code signs you in once. This is the only time they are shown, so keep them somewhere safe, like a password manager."
      footer={<Button onClick={onClose}>I've saved them</Button>}
    >
      <ul
        aria-label="Recovery codes"
        className="grid grid-cols-2 gap-x-6 gap-y-2 rounded-[var(--radius-control)] bg-surface-2 p-4 font-mono text-sm"
      >
        {codes.map((c) => (
          <li key={c}>{c}</li>
        ))}
      </ul>
      <Button
        variant="secondary"
        size="sm"
        className="mt-3"
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(codes.join("\n"));
            setCopied(true);
          } catch {
            toast.error("Copy failed. Select the codes and copy them manually.");
          }
        }}
      >
        <Copy size={14} /> {copied ? "Copied" : "Copy all"}
      </Button>
    </Dialog>
  );
}

// ---- Turning two-step verification on ---------------------------------------------------------

function SetupDialog({ setup, onClose, onEnabled }) {
  const enable = useEnableMfa();
  const [code, setCode] = useState("");
  const grouped = setup.secret.match(/.{1,4}/g).join(" ");

  return (
    <Dialog
      open
      onClose={onClose}
      title="Set up two-step verification"
      description="Scan the code with an authenticator app such as Google Authenticator, 1Password or Authy."
    >
      <form
        className="grid grid-cols-1 gap-5"
        onSubmit={(e) => {
          e.preventDefault();
          enable.mutate(code, { onSuccess: (res) => onEnabled(res.codes) });
        }}
      >
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:items-start">
          <img
            src={setup.qr_svg}
            alt="QR code for your authenticator app"
            width={180}
            height={180}
            className="shrink-0 rounded-[var(--radius-control)] bg-white p-1"
          />
          <div className="min-w-0 text-sm text-ink-2">
            <p>Can't scan it? Enter this key instead:</p>
            <p
              className="mt-2 break-all rounded-[var(--radius-control)] bg-surface-2 px-3 py-2 font-mono text-xs text-ink"
              aria-label="Setup key"
            >
              {grouped}
            </p>
          </div>
        </div>
        <Field label="Code from the app" error={errorText(enable)}>
          <CodeInput value={code} onChange={(e) => setCode(e.target.value)} autoFocus />
        </Field>
        <div className="flex justify-end gap-2">
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" loading={enable.isPending} disabled={code.trim().length < 6}>
            Turn on
          </Button>
        </div>
      </form>
    </Dialog>
  );
}

// ---- Turning it off / new codes ---------------------------------------------------------------

function DisableDialog({ hasPassword, onClose }) {
  const disable = useDisableMfa();
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [useRecovery, setUseRecovery] = useState(false);

  return (
    <Dialog
      open
      onClose={onClose}
      title="Turn off two-step verification?"
      description="Your password alone will be enough to sign in again."
    >
      <form
        className="grid grid-cols-1 gap-4"
        onSubmit={(e) => {
          e.preventDefault();
          disable.mutate(
            {
              password: hasPassword ? password : null,
              [useRecovery ? "recovery_code" : "code"]: code,
            },
            {
              onSuccess: () => {
                toast("Two-step verification is off");
                onClose();
              },
            },
          );
        }}
      >
        {disable.error && (
          <p role="alert" className="text-sm text-danger-ink">
            {disable.error.message}
          </p>
        )}
        {hasPassword && (
          <Field label="Password">
            <PasswordInput
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Field>
        )}
        <Field label={useRecovery ? "Recovery code" : "Code from your app"}>
          {useRecovery ? (
            <input
              className="input font-mono"
              autoComplete="off"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          ) : (
            <CodeInput value={code} onChange={(e) => setCode(e.target.value)} />
          )}
        </Field>
        <button
          type="button"
          className="justify-self-start text-sm text-accent hover:underline"
          onClick={() => {
            setUseRecovery((v) => !v);
            setCode("");
          }}
        >
          {useRecovery ? "Use your authenticator app" : "Use a recovery code instead"}
        </button>
        <div className="flex justify-end gap-2">
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant="danger" loading={disable.isPending} disabled={!code}>
            Turn off
          </Button>
        </div>
      </form>
    </Dialog>
  );
}

function NewCodesDialog({ onClose, onCodes }) {
  const regenerate = useNewRecoveryCodes();
  const [code, setCode] = useState("");
  return (
    <Dialog
      open
      onClose={onClose}
      title="Get new recovery codes"
      description="Your current codes stop working as soon as new ones are made."
    >
      <form
        className="grid grid-cols-1 gap-4"
        onSubmit={(e) => {
          e.preventDefault();
          regenerate.mutate(code, { onSuccess: (res) => onCodes(res.codes) });
        }}
      >
        <Field label="Code from your app" error={errorText(regenerate)}>
          <CodeInput value={code} onChange={(e) => setCode(e.target.value)} autoFocus />
        </Field>
        <div className="flex justify-end gap-2">
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" loading={regenerate.isPending} disabled={code.trim().length < 6}>
            Make new codes
          </Button>
        </div>
      </form>
    </Dialog>
  );
}

function TwoStepCard({ state }) {
  const start = useStartMfa();
  const [setup, setSetup] = useState(null);
  const [codes, setCodes] = useState(null);
  const [dialog, setDialog] = useState(null); // "disable" | "codes"
  const on = state.mfa_enabled;
  const low = on && state.recovery_codes_left <= 3;

  return (
    <div className="card card--flat p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <span
          className={
            on
              ? "grid size-10 shrink-0 place-items-center rounded-full bg-accent-soft text-accent"
              : "grid size-10 shrink-0 place-items-center rounded-full bg-surface-2 text-ink-3"
          }
        >
          {on ? <ShieldCheck size={20} weight="duotone" /> : <ShieldSlash size={20} />}
        </span>
        <div className="min-w-0 flex-1">
          <p className="flex flex-wrap items-center gap-2 font-medium">
            Two-step verification <Chip tone={on ? "accent" : "neutral"}>{on ? "On" : "Off"}</Chip>
          </p>
          <p className="mt-1 text-sm text-ink-2">
            {on
              ? `Signing in needs your password and a code from your authenticator app. ${plural(state.recovery_codes_left, "recovery code")} left.`
              : "Ask for a code from your phone when you sign in, so a leaked password isn't enough."}
          </p>
          {low && (
            <p className="mt-2 text-sm text-warn-ink">
              You're running low on recovery codes. Make a new set.
            </p>
          )}
        </div>
        <div className="flex flex-wrap gap-2">
          {on ? (
            <>
              <Button variant="secondary" size="sm" onClick={() => setDialog("codes")}>
                <Key size={14} /> New codes
              </Button>
              <Button variant="ghost" size="sm" onClick={() => setDialog("disable")}>
                Turn off
              </Button>
            </>
          ) : (
            <Button
              size="sm"
              loading={start.isPending}
              onClick={() =>
                start.mutate(undefined, {
                  onSuccess: setSetup,
                  onError: (e) => toast.error(e.message),
                })
              }
            >
              Turn on
            </Button>
          )}
        </div>
      </div>

      {setup && (
        <SetupDialog
          setup={setup}
          onClose={() => setSetup(null)}
          onEnabled={(c) => {
            setSetup(null);
            setCodes(c);
            toast.success("Two-step verification is on", {
              description: "Other devices were signed out and will need a code next time.",
            });
          }}
        />
      )}
      {dialog === "disable" && (
        <DisableDialog hasPassword={state.has_password} onClose={() => setDialog(null)} />
      )}
      {dialog === "codes" && (
        <NewCodesDialog
          onClose={() => setDialog(null)}
          onCodes={(c) => {
            setDialog(null);
            setCodes(c);
          }}
        />
      )}
      {codes && <RecoveryCodes codes={codes} onClose={() => setCodes(null)} />}
    </div>
  );
}

// ---- Password ---------------------------------------------------------------------------------

function PasswordCard({ hasPassword }) {
  const change = useChangePassword();
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const tooShort = next.length > 0 && next.length < 10;

  return (
    <form
      className="card card--flat grid grid-cols-1 gap-4 p-5 sm:grid-cols-2"
      onSubmit={(e) => {
        e.preventDefault();
        change.mutate(
          { current_password: hasPassword ? current : null, new_password: next },
          {
            onSuccess: (res) => {
              setCurrent("");
              setNext("");
              toast.success(hasPassword ? "Password changed" : "Password set", {
                description: res.signed_out
                  ? `Signed out ${plural(res.signed_out, "other device")}.`
                  : undefined,
              });
            },
          },
        );
      }}
    >
      <div className="sm:col-span-2">
        <p className="font-medium">{hasPassword ? "Change password" : "Add a password"}</p>
        <p className="mt-1 text-sm text-ink-2">
          {hasPassword
            ? "Other devices are signed out when it changes."
            : "You sign in with Google today. A password gives you a second way in."}
        </p>
      </div>
      {change.error && (
        <p role="alert" className="text-sm text-danger-ink sm:col-span-2">
          {change.error.message}
        </p>
      )}
      {hasPassword && (
        <Field label="Current password">
          <PasswordInput
            autoComplete="current-password"
            value={current}
            onChange={(e) => setCurrent(e.target.value)}
          />
        </Field>
      )}
      <Field
        label="New password"
        hint="At least 10 characters."
        error={tooShort ? "Use at least 10 characters" : null}
      >
        <PasswordInput
          autoComplete="new-password"
          value={next}
          onChange={(e) => setNext(e.target.value)}
        />
      </Field>
      <div className="flex justify-end sm:col-span-2">
        <Button
          type="submit"
          loading={change.isPending}
          disabled={next.length < 10 || (hasPassword && !current)}
        >
          {hasPassword ? "Change password" : "Set password"}
        </Button>
      </div>
    </form>
  );
}

// ---- Sessions ---------------------------------------------------------------------------------

function SessionsCard({ sessions }) {
  const end = useEndSession();
  const endOthers = useEndOtherSessions();
  const [confirmAll, setConfirmAll] = useState(false);
  const others = sessions.filter((s) => !s.current).length;

  return (
    <div className="card card--flat">
      <div className="flex flex-wrap items-center justify-between gap-3 p-5 pb-3">
        <div>
          <p className="font-medium">Where you're signed in</p>
          <p className="mt-1 text-sm text-ink-2">Sign out of anything you don't recognise.</p>
        </div>
        {others > 0 && (
          <Button variant="secondary" size="sm" onClick={() => setConfirmAll(true)}>
            <SignOut size={14} /> Sign out other devices
          </Button>
        )}
      </div>
      <ul className="divide-y divide-line" aria-label="Signed-in devices">
        {sessions.map((s) => {
          const Icon = /iPhone|Android|iPad/.test(s.device) ? DeviceMobile : Desktop;
          return (
            <li key={s.id} className="flex items-center gap-3 px-5 py-3.5">
              <Icon size={20} className="shrink-0 text-ink-3" />
              <div className="min-w-0 flex-1">
                <p className="flex flex-wrap items-center gap-2 text-sm font-medium">
                  {s.device}
                  {s.current && <Chip tone="accent">This device</Chip>}
                </p>
                <p className="truncate text-xs text-ink-3">
                  {[
                    s.ip,
                    s.current ? "Active now" : `Active ${timeAgo(s.last_active_at)}`,
                    `Signed in ${formatDate(s.signed_in_at, "MMM d")}`,
                  ]
                    .filter(Boolean)
                    .join(" · ")}
                </p>
              </div>
              {!s.current && (
                <Button
                  variant="ghost"
                  size="sm"
                  loading={end.isPending && end.variables === s.id}
                  onClick={() =>
                    end.mutate(s.id, {
                      onSuccess: () => toast(`Signed out ${s.device}`),
                      onError: (e) => toast.error(e.message),
                    })
                  }
                  aria-label={`Sign out ${s.device}`}
                >
                  Sign out
                </Button>
              )}
            </li>
          );
        })}
      </ul>
      <ConfirmDialog
        open={confirmAll}
        onClose={() => setConfirmAll(false)}
        title="Sign out every other device?"
        description={`${plural(others, "device")} will need to sign in again. This one stays signed in.`}
        confirmLabel="Sign them out"
        loading={endOthers.isPending}
        onConfirm={() =>
          endOthers.mutate(undefined, {
            onSuccess: (res) => {
              setConfirmAll(false);
              toast(`Signed out ${plural(res.signed_out, "device")}`);
            },
            onError: (e) => toast.error(e.message),
          })
        }
      />
    </div>
  );
}

/** Settings section: two-step verification, password and signed-in devices (ADR-029). */
export function SecuritySettings() {
  const { data, isPending, isError, refetch } = useSecurity();

  if (isPending)
    return (
      <div className="grid grid-cols-1 gap-4">
        <Skeleton className="h-28 rounded-card" />
        <Skeleton className="h-44 rounded-card" />
        <Skeleton className="h-40 rounded-card" />
      </div>
    );
  if (isError)
    return (
      <div className="card card--flat flex items-center justify-between gap-3 p-5 text-sm">
        <span className="text-ink-2">Couldn't load your security settings.</span>
        <Button variant="secondary" size="sm" onClick={() => refetch()}>
          Try again
        </Button>
      </div>
    );

  return (
    <div className="grid grid-cols-1 gap-4">
      <EmailCard state={data} />
      <TwoStepCard state={data} />
      <SessionsCard sessions={data.sessions} />
      <PasswordCard hasPassword={data.has_password} />
    </div>
  );
}
