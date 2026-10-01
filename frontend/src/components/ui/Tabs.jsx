import { useId } from "react";
import { motion, useReducedMotion } from "motion/react";
import { cn } from "@/lib/cn";

/** Segmented control with a sliding pill. `items: {key,label,count?}[]` */
export function SegmentedTabs({ items, value, onChange, label, className }) {
  const id = useId();
  const reduce = useReducedMotion();
  return (
    <div
      role="tablist"
      aria-label={label}
      className={cn(
        "inline-flex max-w-full items-center gap-0.5 overflow-x-auto rounded-full border border-line bg-surface-2 p-1 [scrollbar-width:none]",
        className,
      )}
    >
      {items.map((item) => {
        const active = item.key === value;
        return (
          <button
            key={item.key}
            role="tab"
            type="button"
            aria-selected={active}
            onClick={() => onChange(item.key)}
            className={cn(
              "relative isolate inline-flex h-8 shrink-0 items-center gap-1.5 rounded-full px-3.5 text-[13px] font-medium transition-colors duration-150",
              active ? "text-ink" : "text-ink-2 hover:text-ink",
            )}
          >
            {active && (
              <motion.span
                layoutId={`seg-${id}`}
                className="absolute inset-0 -z-10 rounded-full bg-surface shadow-xs ring-1 ring-line"
                transition={
                  reduce ? { duration: 0 } : { type: "spring", bounce: 0.15, duration: 0.4 }
                }
              />
            )}
            {item.label}
            {item.count !== undefined && (
              <span
                className={cn(
                  "tabular rounded-full px-1.5 text-[11px]",
                  active ? "bg-accent-soft text-accent-soft-ink" : "bg-surface-3 text-ink-3",
                )}
              >
                {item.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
