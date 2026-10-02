import { Suspense } from "react";
import { Navigate, Outlet, useLocation } from "react-router";
import { AppNav } from "@/components/nav/AppNav";
import { useAuth } from "@/lib/auth";
import { Skeleton } from "@/components/ui/Skeleton";
import { PageSkeleton } from "@/components/layout/PageSkeleton";
import { useGoogleWelcome } from "@/features/auth/useGoogleWelcome";

function ShellSkeleton() {
  return (
    <div aria-hidden>
      <div className="flex h-[var(--nav-h)] items-center gap-4 px-6">
        <Skeleton className="h-7 w-32" />
        <div className="hidden gap-2 md:flex">
          {Array.from({ length: 6 }, (_, i) => (
            <Skeleton key={i} className="h-5 w-20" />
          ))}
        </div>
        <Skeleton variant="circle" className="ml-auto size-8" />
      </div>
      <PageSkeleton />
    </div>
  );
}

export default function AppLayout() {
  const { user, isLoading } = useAuth();
  const location = useLocation();
  useGoogleWelcome();

  if (isLoading) return <ShellSkeleton />;
  if (!user) {
    const next = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/login?next=${next}`} replace />;
  }

  return (
    <>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-3 focus:z-[100] focus:rounded-lg focus:bg-surface focus:px-3 focus:py-2"
      >
        Skip to content
      </a>
      <AppNav />
      {user.is_demo && (
        <div className="border-b border-line bg-accent-soft/60 px-4 py-2 text-center text-[13px] text-accent-soft-ink">
          You're exploring a demo account with synthetic records. It resets in 24 hours.
        </div>
      )}
      <main id="main" className="mx-auto max-w-[1280px] px-4 pb-24 pt-8 sm:px-6 sm:pt-10">
        <Suspense fallback={<PageSkeleton />}>
          <Outlet />
        </Suspense>
      </main>
    </>
  );
}
