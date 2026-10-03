import { LoadingRegion, Skeleton, SkeletonText } from "@/components/ui/Skeleton";
import { LOADING_PUNS, pick } from "@/easter-eggs/puns";
import { useState } from "react";

/** Generic page skeleton: header + content grid. Pages provide shaped skeletons of their own. */
export function PageSkeleton() {
  const [pun] = useState(() => pick(LOADING_PUNS));
  return (
    <LoadingRegion label={pun}>
      <Skeleton className="h-9 w-64" />
      <Skeleton className="mt-3 h-4 w-80 max-w-full" />
      <p className="mt-4 text-xs text-ink-3">{pun}…</p>
      <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }, (_, i) => (
          <div key={i} className="card card--flat p-5">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="mt-4 h-8 w-16" />
          </div>
        ))}
      </div>
      <div className="card card--flat mt-4 p-6">
        <SkeletonText lines={4} />
      </div>
    </LoadingRegion>
  );
}

/** Page heading with optional actions, used across the app. */
export function PageHeader({ title, description, actions, eyebrow }) {
  return (
    <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        {eyebrow && <p className="mb-1.5 text-sm font-medium text-accent">{eyebrow}</p>}
        <h1 className="text-3xl font-semibold tracking-tight sm:text-[34px]">{title}</h1>
        {description && <p className="mt-2 max-w-[60ch] text-ink-2">{description}</p>}
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </div>
  );
}
