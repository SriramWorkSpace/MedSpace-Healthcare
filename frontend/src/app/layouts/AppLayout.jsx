import { Suspense } from "react";
import { Navigate, Outlet, useLocation } from "react-router";
import { AppNav } from "@/components/nav/AppNav";
import { useAuth } from "@/lib/auth";
import { Skeleton } from "@/components/ui/Skeleton";
import { PageSkeleton } from "@/components/layout/PageSkeleton";
import { VerifyEmailBanner } from "@/features/auth/VerifyEmailBanner";
import { useOpenForParam } from "@/features/circle/useOpenForParam";
import { useGoogleWelcome } from "@/features/auth/useGoogleWelcome";
import { SearchProvider } from "@/features/search/SearchProvider";
import { OfflineBanner } from "@/features/offline/OfflineBanner";
import { useOnline } from "@/features/offline/hooks";
import { EmptyState } from "@/components/ui/EmptyState";
import { CloudSlash } from "@phosphor-icons/react";
import { ActingBanner } from "@/features/circle/ActingBanner";

function ShellSkeleton() {
  return (
    <div aria-hidden>
      <div className="shell flex h-[var(--nav-h)] items-center gap-4">
        <Skeleton className="h-7 w-32" />
        <div className="hidden gap-2 lg:flex">
          {Array.from({ length: 6 }, (_, i) => (
            <Skeleton key={i} className="h-5 w-20" />
          ))}
        </div>
        <Skeleton variant="circle" className="ml-auto size-8" />
      </div>
      <div className="shell shell--page pt-8 sm:pt-10">
        <PageSkeleton />
      </div>
    </div>
  );
}

export default function AppLayout() {
  const { user, isLoading } = useAuth();
  const location = useLocation();
  const online = useOnline();
  useGoogleWelcome();
  useOpenForParam(Boolean(user));

  if (isLoading) return <ShellSkeleton />;
  if (!user && !online) {
    // Signing in needs a connection; don't bounce to a login page that can't work.
    return (
      <main id="main" className="shell shell--page pt-16">
        <EmptyState
          icon={CloudSlash}
          title="You're offline"
          description="Reconnect to open MedSpace. To read your records without a connection next time, turn on offline access in Settings."
        />
      </main>
    );
  }
  if (!user) {
    const next = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/login?next=${next}`} replace />;
  }

  return (
    <SearchProvider>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-3 focus:z-[100] focus:rounded-lg focus:bg-surface focus:px-3 focus:py-2"
      >
        Skip to content
      </a>
      <AppNav />
      <OfflineBanner />
      <ActingBanner />
      <VerifyEmailBanner />
      {user.is_demo && (
        <aside
          aria-label="Demo account"
          className="no-print border-b border-line bg-accent-soft/60 px-4 py-2 text-center text-[13px] text-accent-soft-ink"
        >
          You're exploring a demo account with synthetic records. It resets in 24 hours.
        </aside>
      )}
      <main id="main" className="shell shell--page pb-24 pt-8 sm:pt-10">
        <Suspense fallback={<PageSkeleton />}>
          <Outlet />
        </Suspense>
      </main>
    </SearchProvider>
  );
}
