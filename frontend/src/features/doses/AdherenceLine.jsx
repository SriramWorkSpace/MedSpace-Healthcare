import { Link } from "react-router";
import { ArrowRight } from "@phosphor-icons/react";
import { DoseStrip } from "./DoseStrip";

/** Compact "last 14 days" summary for a medication card. */
export function AdherenceLine({ history, window }) {
  const { counts } = history;
  return (
    <div className="mt-4 grid grid-cols-1 gap-2 rounded-[var(--radius-control)] bg-surface-2 p-3">
      <div className="flex items-baseline justify-between gap-2 text-xs">
        <p className="text-ink-2">
          {counts.due ? (
            <>
              Taken <span className="tabular font-semibold text-ink">{counts.taken}</span> of{" "}
              <span className="tabular">{counts.due}</span> in the last 14 days
            </>
          ) : (
            "No doses due yet"
          )}
        </p>
        <Link
          to={`/app/medications/${history.medication_id}`}
          className="tap inline-flex shrink-0 items-center gap-1 font-medium text-accent hover:underline"
          aria-label={`Dose history for ${history.name}`}
        >
          History <ArrowRight size={12} weight="bold" />
        </Link>
      </div>
      <DoseStrip start={window.start} end={window.end} days={history.days} />
    </div>
  );
}
