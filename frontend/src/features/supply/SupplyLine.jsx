import { Package } from "@phosphor-icons/react";
import { cn } from "@/lib/cn";
import { leftLabel, runsOutLabel } from "./format";

const TONE = {
  out: "bg-danger-soft text-danger-ink",
  low: "bg-warn-soft text-warn-ink",
  ok: "bg-surface-2 text-ink-2",
  course_covered: "bg-surface-2 text-ink-2",
  as_needed: "bg-surface-2 text-ink-2",
};

/** Supply summary for a medication card; `onCount`/`onRefill` open the supply dialog. */
export function SupplyLine({ supply, onCount, onRefill }) {
  if (!supply) {
    return (
      <button
        type="button"
        onClick={onCount}
        className="mt-3 inline-flex items-center gap-1.5 self-start rounded-full text-xs font-medium text-accent hover:underline"
      >
        <Package size={14} /> Track supply
      </button>
    );
  }
  return (
    <div
      className={cn(
        "mt-3 flex flex-wrap items-center justify-between gap-x-3 gap-y-2 rounded-[var(--radius-control)] px-3 py-2.5 text-xs",
        TONE[supply.status],
      )}
    >
      <p className="flex min-w-0 items-start gap-2">
        <Package size={15} className="mt-px shrink-0" />
        <span>
          <span className="font-semibold">{leftLabel(supply)}</span>
          <span className="block opacity-90">{runsOutLabel(supply)} (estimate)</span>
        </span>
      </p>
      {onCount && (
        <span className="flex gap-1">
          <button
            type="button"
            onClick={onCount}
            className="rounded-full px-2.5 py-1 font-medium hover:bg-surface/60"
          >
            Update count
          </button>
          <button
            type="button"
            onClick={onRefill}
            className="rounded-full bg-surface px-2.5 py-1 font-medium text-ink shadow-xs hover:bg-surface-2"
          >
            Refill
          </button>
        </span>
      )}
    </div>
  );
}
