import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation } from "@tanstack/react-query";
import { Eye, EyeSlash, Sparkle } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Field, Input } from "@/components/ui/Field";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useDemoLogin } from "./useDemoLogin";

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

function PasswordInput(props) {
  const [visible, setVisible] = useState(false);
  return (
    <div className="relative">
      <Input type={visible ? "text" : "password"} className="pr-11" {...props} />
      <button
        type="button"
        onClick={() => setVisible((v) => !v)}
        aria-label={visible ? "Hide password" : "Show password"}
        className="absolute right-1.5 top-1/2 grid size-8 -translate-y-1/2 place-items-center rounded-lg text-ink-3 hover:text-ink"
      >
        {visible ? <EyeSlash size={17} /> : <Eye size={17} />}
      </button>
    </div>
  );
}

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

function useAuthMutation(path, setError) {
  const { setSession } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  return useMutation({
    mutationFn: (values) => api.post(path, values),
    onSuccess: (session) => {
      setSession(session);
      navigate(params.get("next") || "/app", { replace: true });
    },
    onError: (err) => {
      if (err instanceof ApiError) {
        for (const [field, msg] of Object.entries(err.fieldErrors))
          setError(field, { message: msg });
      }
    },
  });
}

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });
  const login = useAuthMutation("/api/auth/login", form.setError);
  const { errors } = form.formState;

  return (
    <>
      <h1 className="text-3xl font-semibold tracking-tight">Welcome back</h1>
      <p className="mt-2 text-ink-2">Sign in to pick up where you left off.</p>
      <form
        className="mt-8 grid gap-4"
        noValidate
        onSubmit={form.handleSubmit((v) => login.mutate(v))}
      >
        <FormError error={login.error?.status !== 422 && login.error?.message} />
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
      <form
        className="mt-8 grid gap-4"
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
