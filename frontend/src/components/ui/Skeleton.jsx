import { cn } from "@/lib/cn";

export function Skeleton({ className, variant, style }) {
  return (
    <div
      aria-hidden
      className={cn("skeleton", variant && `skeleton--${variant}`, className)}
      style={style}
    />
  );
}

/** Multiple text lines with a natural ragged right edge. */
export function SkeletonText({ lines = 3, className }) {
  const widths = ["100%", "92%", "78%", "86%", "64%"];
  return (
    <div className={cn("grid gap-2.5", className)} aria-hidden>
      {Array.from({ length: lines }, (_, i) => (
        <Skeleton
          key={i}
          variant="text"
          style={{ width: i === lines - 1 ? "58%" : widths[i % widths.length] }}
        />
      ))}
    </div>
  );
}

/** Screen-reader announcement paired with visual skeletons. */
export function LoadingRegion({ label = "Loading", children, className }) {
  return (
    <div role="status" aria-live="polite" aria-busy="true" className={className}>
      <span className="sr-only">{label}</span>
      {children}
    </div>
  );
}
