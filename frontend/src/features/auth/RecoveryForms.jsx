import { useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle, EnvelopeSimple, WarningCircle } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Field, Input } from "@/components/ui/Field";
import { PasswordInput } from "@/components/ui/PasswordInput";
import { api } from "@/lib/api";
import { meKey, useAuth } from "@/lib/auth";

function Notice({ icon: Icon, tone = "accent", title, children }) {
  const color = tone === "danger" ? "bg-danger-soft text-danger-ink" : "bg-accent-soft text-accent";
  return (
    <div>
      <span className={`grid size-12 place-items-center rounded-full ${color}`}>
        <Icon size={24} weight="duotone" />
      </span>
      <h1 className="mt-5 text-3xl font-semibold tracking-tight">{title}</h1>
      <div className="mt-2 text-ink-2">{children}</div>
    </div>
  );
}

function BackToSignIn() {
  return (
    <p className="mt-8 text-center text-sm text-ink-2">
      <Link to="/login" className="tap font-medium text-accent hover:underline">
        Back to sign in
      </Link>
    </p>
  );
}

/** Ask for a reset link. The answer never reveals whether the address has an account. */
export function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const send = useMutation({
    mutationFn: () => api.post("/api/auth/password/forgot", { email: email.trim() }),
  });

  if (send.isSuccess)
    return (
      <>
        <Notice icon={EnvelopeSimple} title="Check your inbox">
          <p>
            If <span className="font-medium text-ink">{email.trim()}</span> has a MedSpace account,
            a link to choose a new password is on its way. It works once and expires in 30 minutes.
          </p>
          <p className="mt-3 text-sm text-ink-3">
            Nothing arrived? Check spam, or try again in a few minutes.
          </p>
        </Notice>
        <BackToSignIn />
      </>
    );

  return (
    <>
      <h1 className="text-3xl font-semibold tracking-tight">Forgot your password?</h1>
      <p className="mt-2 text-ink-2">
        Enter the email you sign in with and we'll send you a link to choose a new one.
      </p>
      <form
        className="mt-8 grid grid-cols-1 gap-4"
        onSubmit={(e) => {
          e.preventDefault();
          send.mutate();
        }}
      >
        {send.error && (
          <p role="alert" className="text-sm text-danger-ink">
            {send.error.message}
          </p>
        )}
        <Field label="Email">
          <Input
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoFocus
          />
        </Field>
        <Button type="submit" className="mt-2 w-full" loading={send.isPending} disabled={!email}>
          Send reset link
        </Button>
      </form>
      <BackToSignIn />
    </>
  );
}

/** Choose a new password from an emailed link. Signs out every device on success. */
export function ResetPasswordForm() {
  const [params] = useSearchParams();
  const token = params.get("token") ?? "";
  const { refetch } = useAuth();
  const [password, setPassword] = useState("");
  const tooShort = password.length > 0 && password.length < 10;
  const reset = useMutation({
    mutationFn: () => api.post("/api/auth/password/reset", { token, new_password: password }),
    onSuccess: () => refetch(), // any session in this browser was just signed out
  });

  if (!token || reset.error?.status === 410)
    return (
      <>
        <Notice icon={WarningCircle} tone="danger" title="This link has expired">
          <p>Reset links work once and only for 30 minutes. Ask for a new one.</p>
        </Notice>
        <Button as={Link} to="/forgot-password" className="mt-8 w-full">
          Send a new link
        </Button>
        <BackToSignIn />
      </>
    );

  if (reset.isSuccess)
    return (
      <>
        <Notice icon={CheckCircle} title="Password updated">
          <p>
            You've been signed out on every device. Sign in with your new password. If two-step
            verification is on, you'll still need a code.
          </p>
        </Notice>
        <Button as={Link} to="/login" className="mt-8 w-full">
          Sign in
        </Button>
      </>
    );

  return (
    <>
      <h1 className="text-3xl font-semibold tracking-tight">Choose a new password</h1>
      <p className="mt-2 text-ink-2">This signs you out on every device.</p>
      <form
        className="mt-8 grid grid-cols-1 gap-4"
        onSubmit={(e) => {
          e.preventDefault();
          reset.mutate();
        }}
      >
        {reset.error && (
          <p role="alert" className="text-sm text-danger-ink">
            {reset.error.message}
          </p>
        )}
        <Field
          label="New password"
          hint="At least 10 characters."
          error={tooShort ? "Use at least 10 characters" : null}
        >
          <PasswordInput
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
          />
        </Field>
        <Button
          type="submit"
          className="mt-2 w-full"
          loading={reset.isPending}
          disabled={password.length < 10}
        >
          Set new password
        </Button>
      </form>
    </>
  );
}

/** Lands from the confirmation email. Works signed in, signed out, or in another browser. */
export function VerifyEmailResult() {
  const [params] = useSearchParams();
  const token = params.get("token") ?? "";
  const { user } = useAuth();
  const qc = useQueryClient();
  const started = useRef(false);
  const verify = useMutation({
    mutationFn: () => api.post("/api/auth/email/verify", { token }),
    onSuccess: () => qc.invalidateQueries({ queryKey: meKey }),
  });
  const { mutate } = verify;

  useEffect(() => {
    // Links work once: guard against StrictMode's double effect.
    if (started.current || !token) return;
    started.current = true;
    mutate();
  }, [token, mutate]);

  const next = user ? "/app" : "/login";
  if (verify.isSuccess)
    return (
      <>
        <Notice icon={CheckCircle} title="Email confirmed">
          <p>
            Thanks. You can now reset your password by email and accept care circle invitations.
          </p>
        </Notice>
        <Button as={Link} to={next} className="mt-8 w-full">
          {user ? "Go to MedSpace" : "Sign in"}
        </Button>
      </>
    );
  if (!token || verify.isError)
    return (
      <>
        <Notice icon={WarningCircle} tone="danger" title="This link has expired">
          <p>
            Confirmation links work once and expire after 48 hours. Sign in and use "Resend link" on
            the banner at the top of the app to get a new one.
          </p>
        </Notice>
        <Button as={Link} to={next} className="mt-8 w-full">
          {user ? "Go to MedSpace" : "Sign in"}
        </Button>
      </>
    );
  return (
    <div role="status" aria-live="polite">
      <Notice icon={EnvelopeSimple} title="Confirming your email">
        <p>One moment.</p>
      </Notice>
    </div>
  );
}

/** Lands from the link sent to a new address: the account moves to it (ADR-033). */
export function ConfirmEmailChangeResult() {
  const [params] = useSearchParams();
  const token = params.get("token") ?? "";
  const { user } = useAuth();
  const qc = useQueryClient();
  const started = useRef(false);
  const confirm = useMutation({
    mutationFn: () => api.post("/api/auth/email/change/confirm", { token }),
    onSuccess: () => qc.invalidateQueries({ queryKey: meKey }),
  });
  const { mutate } = confirm;

  useEffect(() => {
    if (started.current || !token) return; // links work once: guard StrictMode's double effect
    started.current = true;
    mutate();
  }, [token, mutate]);

  const next = user ? "/app/settings#security" : "/login";
  const cta = user ? "Back to settings" : "Sign in";
  if (confirm.isSuccess)
    return (
      <>
        <Notice icon={CheckCircle} title="Email changed">
          <p>Your account now uses this address. Sign in with it from now on.</p>
        </Notice>
        <Button as={Link} to={next} className="mt-8 w-full">
          {cta}
        </Button>
      </>
    );
  if (!token || confirm.isError)
    return (
      <>
        <Notice icon={WarningCircle} tone="danger" title="Your email wasn't changed">
          <p>
            {confirm.error?.status === 409
              ? confirm.error.message
              : "This link has expired, was already used, or the change was cancelled. Start again from Settings, Security."}
          </p>
        </Notice>
        <Button as={Link} to={next} className="mt-8 w-full">
          {cta}
        </Button>
      </>
    );
  return (
    <div role="status" aria-live="polite">
      <Notice icon={EnvelopeSimple} title="Changing your email">
        <p>One moment.</p>
      </Notice>
    </div>
  );
}
