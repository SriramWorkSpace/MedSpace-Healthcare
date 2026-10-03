import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation } from "@tanstack/react-query";
import { ShieldCheck, Sparkle } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Field, Input } from "@/components/ui/Field";
import { CodeInput, PasswordInput } from "@/components/ui/PasswordInput";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useDemoLogin } from "./useDemoLogin";
import { GoogleButton } from "./GoogleButton";
import { GOOGLE_ERRORS } from "./googleAuth";

const loginSchema = z.object({
  email: z.email("Enter a valid email address"),
  password: z.string().min(1, "Enter your password"),
});

const signupSchema = z.object({
  display_name: z.string().trim().min(1, "Tell us what to call you").max(80),
  email: z.email("Enter a valid email address"),
  password: z
    .string()
    .min(10, "Use at least 10 characters")
    .max(128, "That's a little long. 128 characters max"),
});

function FormError({ error }) {
  if (!error) return null;
  return (
    <div
      role="alert"
      className="rounded-[var(--radius-control)] bg-danger-soft px-3.5 py-3 text-sm text-danger-ink"
    >
      {error}
    </div>
  );
}

function DemoDivider() {
  const demo = useDemoLogin();
  return (
    <>
      <div className="my-6 flex items-center gap-3 text-xs text-ink-3">
        <span className="h-px flex-1 bg-line" /> or <span className="h-px flex-1 bg-line" />
      </div>
      <Button
        variant="secondary"
        className="w-full"
        loading={demo.isPending}
        onClick={() => demo.mutate()}
      >
        <Sparkle size={15} weight="fill" className="text-accent" />
        Try the demo
      </Button>
    </>
  );
}

function useAuthMutation(path, setError, onMfa) {
  const { setSession } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  return useMutation({
    mutationFn: (values) => api.post(path, values),
    onSuccess: (session) => {
      if (session.mfa_required) return onMfa?.(session.mfa_token);
      setSession(session);
      navigate(session.next || params.get("next") || "/app", { replace: true });
    },
    onError: (err) => {
      if (err instanceof ApiError) {
        for (const [field, msg] of Object.entries(err.fieldErrors))
          setError(field, { message: msg });
      }
    },
  });
}

function GoogleFirst() {
  return (
    <div className="mt-8">
      <GoogleButton />
      <div className="mt-6 flex items-center gap-3 text-xs text-ink-3">
        <span className="h-px flex-1 bg-line" /> or with email{" "}
        <span className="h-px flex-1 bg-line" />
      </div>
    </div>
  );
}

/** Second sign-in step: a code from the authenticator app, or a one-time recovery code. */
function MfaStep({ token, onCancel }) {
  const [code, setCode] = useState("");
  const [useRecovery, setUseRecovery] = useState(false);
  const verify = useAuthMutation("/api/auth/login/mfa", () => {});
  const expired = verify.error?.status === 401 && /took too long/.test(verify.error.message);

  return (
    <>
      <span className="grid size-12 place-items-center rounded-full bg-accent-soft text-accent">
        <ShieldCheck size={24} weight="duotone" />
      </span>
      <h1 className="mt-5 text-3xl font-semibold tracking-tight">Check your phone</h1>
      <p className="mt-2 text-ink-2">
        {useRecovery
          ? "Enter one of the recovery codes you saved. Each one works once."
          : "Enter the 6-digit code from your authenticator app."}
      </p>
      <form
        className="mt-8 grid grid-cols-1 gap-4"
        noValidate
        onSubmit={(e) => {
          e.preventDefault();
          verify.mutate({
            mfa_token: token,
            [useRecovery ? "recovery_code" : "code"]: code.trim(),
          });
        }}
      >
        <FormError error={verify.error?.message} />
        <Field label={useRecovery ? "Recovery code" : "Code"}>
          {useRecovery ? (
            <Input
              autoComplete="off"
              className="font-mono"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              autoFocus
            />
          ) : (
            <CodeInput value={code} onChange={(e) => setCode(e.target.value)} autoFocus />
          )}
        </Field>
        {expired ? (
          <Button className="mt-2 w-full" onClick={onCancel}>
            Start again
          </Button>
        ) : (
          <Button
            type="submit"
            className="mt-2 w-full"
            loading={verify.isPending}
            disabled={useRecovery ? code.trim().length < 8 : code.trim().length < 6}
          >
            Verify
          </Button>
        )}
      </form>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-sm">
        <button
          type="button"
          className="font-medium text-accent hover:underline"
          onClick={() => {
            setUseRecovery((v) => !v);
            setCode("");
            verify.reset();
          }}
        >
          {useRecovery ? "Use your authenticator app" : "Use a recovery code"}
        </button>
        <button type="button" className="text-ink-2 hover:text-ink" onClick={onCancel}>
          Back to sign in
        </button>
      </div>
    </>
  );
}

export function LoginForm() {
  const [params, setParams] = useSearchParams();
  const [mfaToken, setMfaToken] = useState(() => params.get("mfa"));
  const form = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });
  const login = useAuthMutation("/api/auth/login", form.setError, setMfaToken);
  const { errors } = form.formState;
  const googleError = GOOGLE_ERRORS[params.get("google")];

  if (mfaToken)
    return (
      <MfaStep
        token={mfaToken}
        onCancel={() => {
          setMfaToken(null);
          login.reset();
          if (params.has("mfa")) {
            params.delete("mfa");
            setParams(params, { replace: true });
          }
        }}
      />
    );

  return (
    <>
      <h1 className="text-3xl font-semibold tracking-tight">Welcome back</h1>
      <p className="mt-2 text-ink-2">Sign in to pick up where you left off.</p>
      <GoogleFirst />
      <form
        className="mt-6 grid grid-cols-1 gap-4"
        noValidate
        onSubmit={form.handleSubmit((v) => login.mutate(v))}
      >
        <FormError error={googleError || (login.error?.status !== 422 && login.error?.message)} />
        <Field label="Email" error={errors.email?.message}>
          <Input type="email" autoComplete="email" {...form.register("email")} />
        </Field>
        <Field label="Password" error={errors.password?.message}>
          <PasswordInput autoComplete="current-password" {...form.register("password")} />
        </Field>
        <Button type="submit" className="mt-2 w-full" loading={login.isPending}>
          Sign in
        </Button>
      </form>
      <DemoDivider />
      <p className="mt-8 text-center text-sm text-ink-2">
        New here?{" "}
        <Link to="/signup" className="font-medium text-accent hover:underline">
          Create account
        </Link>
      </p>
    </>
  );
}

export function SignupForm() {
  const form = useForm({
    resolver: zodResolver(signupSchema),
    defaultValues: { display_name: "", email: "", password: "" },
  });
  const signup = useAuthMutation("/api/auth/signup", form.setError);
  const { errors } = form.formState;

  return (
    <>
      <h1 className="text-3xl font-semibold tracking-tight">Create your space</h1>
      <p className="mt-2 text-ink-2">It takes a minute. No paperwork required, ironically.</p>
      <GoogleFirst />
      <form
        className="mt-6 grid grid-cols-1 gap-4"
        noValidate
        onSubmit={form.handleSubmit((v) =>
          signup.mutate({ ...v, timezone: Intl.DateTimeFormat().resolvedOptions().timeZone }),
        )}
      >
        <FormError error={signup.error?.status !== 422 && signup.error?.message} />
        <Field label="Name" error={errors.display_name?.message}>
          <Input autoComplete="name" {...form.register("display_name")} />
        </Field>
        <Field label="Email" error={errors.email?.message}>
          <Input type="email" autoComplete="email" {...form.register("email")} />
        </Field>
        <Field label="Password" hint="At least 10 characters." error={errors.password?.message}>
          <PasswordInput autoComplete="new-password" {...form.register("password")} />
        </Field>
        <Button type="submit" className="mt-2 w-full" loading={signup.isPending}>
          Create account
        </Button>
      </form>
      <DemoDivider />
      <p className="mt-8 text-center text-sm text-ink-2">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-accent hover:underline">
          Sign in
        </Link>
      </p>
    </>
  );
}
