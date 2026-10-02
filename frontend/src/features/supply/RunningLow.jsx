import { useState } from "react";
import { Package } from "@phosphor-icons/react";
import { SupplyDialog } from "./SupplyDialog";
import { leftLabel, runsOutLabel } from "./format";

/** Dashboard card: supplies estimated to run out within their warning window. */
export function RunningLow({ items }) {
  const [refilling, setRefilling] = useState(null);
  if (!items?.length) return null;
  return (
    <section className="card overflow-hidden border-warn/40" aria-labelledby="running-low">
      <h2
        id="running-low"
        className="flex items-center gap-2 bg-warn-soft/60 px-5 py-3 text-sm font-semibold text-warn-ink"
      >
        <Package size={16} weight="duotone" />
        Running low
      </h2>
      <ul className="divide-y divide-line">
        {items.map((s) => (
          <li key={s.medication_id} className="flex items-center justify-between gap-3 px-5 py-3">
            <span className="min-w-0">
              <span className="block truncate text-sm font-medium">
                {s.name}{" "}
                {s.strength && <span className="font-normal text-ink-3">{s.strength}</span>}
              </span>
              <span className="block text-xs text-ink-3">
                {leftLabel(s)}. {runsOutLabel(s)} (estimate).
              </span>
            </span>
            <button
              type="button"
              onClick={() => setRefilling(s)}
              className="shrink-0 rounded-full border border-line bg-surface px-3 py-1.5 text-xs font-medium hover:border-line-strong"
            >
              Refill
            </button>
          </li>
        ))}
      </ul>
      {refilling && (
        <SupplyDialog
          med={{ id: refilling.medication_id, name: refilling.name, strength: refilling.strength }}
          supply={refilling}
          mode="refill"
          onClose={() => setRefilling(null)}
        />
      )}
    </section>
  );
}
