import { cn } from "@/lib/cn";

/** Geometric mark: a rounded square holding a soft plus. Paired with the wordmark. */
export function LogoMark({ size = 28, className }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      aria-hidden
      className={cn("shrink-0", className)}
    >
      <rect width="32" height="32" rx="9" fill="var(--accent)" />
      <rect x="9" y="14" width="14" height="4" rx="2" fill="var(--accent-ink)" />
      <rect x="14" y="9" width="4" height="14" rx="2" fill="var(--accent-ink)" />
    </svg>
  );
}

export function Logo({ className, size = 28 }) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <LogoMark size={size} />
      <span className="text-[17px] font-semibold tracking-[-0.03em]">MedSpace</span>
    </span>
  );
}
