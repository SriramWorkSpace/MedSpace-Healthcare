import { Link, Navigate, Outlet, useSearchParams } from "react-router";
import { Quotes } from "@phosphor-icons/react";
import { Logo } from "@/components/ui/Logo";
import { ThemeToggle } from "@/components/nav/ThemeToggle";
import { useAuth } from "@/lib/auth";
import { Skeleton } from "@/components/ui/Skeleton";

export default function AuthLayout() {
  const { user, isLoading } = useAuth();
  const [params] = useSearchParams();
  if (user) return <Navigate to={params.get("next") || "/app"} replace />;

  return (
    <div className="grid grid-cols-1 min-h-[100dvh] lg:grid-cols-[1fr_1fr]">
      <div className="flex flex-col px-4 py-6 sm:px-10">
        <div className="flex items-center justify-between">
          <Link to="/" className="rounded-lg" aria-label="MedSpace home">
            <Logo />
          </Link>
          <ThemeToggle />
        </div>
        <main className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center py-12">
          {isLoading ? (
            <div className="grid grid-cols-1 gap-4" aria-hidden>
              <Skeleton className="h-8 w-2/3" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="mt-6 h-11 w-full" />
              <Skeleton className="h-11 w-full" />
            </div>
          ) : (
            <Outlet />
          )}
        </main>
        <p className="text-center text-xs text-ink-3">Synthetic data only. Not a medical device.</p>
      </div>

      <aside className="relative hidden overflow-hidden bg-[oklch(0.25_0.035_165)] text-[oklch(0.96_0.01_160)] lg:block">
        <div className="absolute -left-40 top-1/3 size-[640px] rounded-full bg-[radial-gradient(closest-side,color-mix(in_oklch,var(--accent),transparent_50%),transparent)] opacity-70" />
        <div className="absolute inset-0 bg-[radial-gradient(oklch(1_0_0/0.07)_1px,transparent_1px)] [background-size:22px_22px]" />
        <div className="relative flex h-full flex-col justify-end p-14">
          <Quotes size={36} weight="fill" className="opacity-60" />
          <p className="mt-6 max-w-[24ch] text-4xl font-semibold leading-tight tracking-tight">
            An apple a day keeps the doctor away.
          </p>
          <p className="mt-4 max-w-[38ch] text-lg opacity-70">
            For everything else, there's a place to keep the paperwork.
          </p>
        </div>
      </aside>
    </div>
  );
}
