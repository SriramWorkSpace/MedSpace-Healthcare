import { useCallback, useMemo, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Check, Pill, Sun, SunHorizon, Moon, MoonStars } from "@phosphor-icons/react";
import { cn } from "@/lib/cn";
import { formatClock } from "@/lib/format";

const SLOTS = [
  { key: "morning", label: "Morning", icon: Sun, until: "12:00" },
  { key: "afternoon", label: "Afternoon", icon: SunHorizon, until: "17:00" },
  { key: "evening", label: "Evening", icon: Moon, until: "21:00" },
  { key: "night", label: "Night", icon: MoonStars, until: "24:00" },
];

const slotFor = (time) => SLOTS.find((s) => time < s.until)?.key ?? "night";

/** Taken-dose ticks are a personal convenience stored on this device only (not health data). */
function useTaken(dateKey) {
  const storageKey = `ms-taken-${dateKey}`;
  const [taken, setTaken] = useState(() => {
    try {
      return new Set(JSON.parse(localStorage.getItem(storageKey) ?? "[]"));
    } catch {
      return new Set();
    }
  });
  const toggle = useCallback(
    (id) =>
      setTaken((prev) => {
        const next = new Set(prev);
        next.has(id) ? next.delete(id) : next.add(id);
        try {
          localStorage.setItem(storageKey, JSON.stringify([...next]));
        } catch {
          /* storage unavailable */
        }
        return next;
      }),
    [storageKey],
  );
  return [taken, toggle];
}

function nowHHMM() {
  const d = new Date();
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

export function TodaySchedule({ doses, dateKey }) {
  const [taken, toggle] = useTaken(dateKey);
  const [now] = useState(nowHHMM);
  const nextIndex = doses.findIndex(
    (d) => d.time >= now && !taken.has(`${d.medication_id}@${d.time}`),
  );

  const groups = useMemo(() => {
    const out = SLOTS.map((s) => ({ ...s, items: [] }));
    doses.forEach((d, i) =>
      out.find((g) => g.key === slotFor(d.time)).items.push({ ...d, index: i }),
    );
    return out.filter((g) => g.items.length);
  }, [doses]);

  const doneCount = doses.filter((d) => taken.has(`${d.medication_id}@${d.time}`)).length;

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-ink-2">
          <span className="tabular font-semibold text-ink">{doneCount}</span> of {doses.length}{" "}
          doses ticked off
        </p>
        <div className="h-1.5 w-28 overflow-hidden rounded-full bg-surface-3" aria-hidden>
          <motion.div
            className="h-full rounded-full bg-accent"
            animate={{ width: `${doses.length ? (doneCount / doses.length) * 100 : 0}%` }}
            transition={{ duration: 0.4, ease: [0.23, 1, 0.32, 1] }}
          />
        </div>
      </div>
      <div className="grid gap-5">
        {groups.map(({ key, label, icon: Icon, items }) => (
          <section key={key} aria-label={label}>
            <p className="mb-2 flex items-center gap-1.5 text-xs font-medium text-ink-3">
              <Icon size={14} weight="bold" /> {label}
            </p>
            <ul className="grid gap-1.5">
              {items.map((d) => {
                const id = `${d.medication_id}@${d.time}`;
                const isTaken = taken.has(id);
                const isNext = d.index === nextIndex;
                return (
                  <li key={id}>
                    <button
                      type="button"
                      onClick={() => toggle(id)}
                      aria-pressed={isTaken}
                      className={cn(
                        "group flex w-full items-center gap-3 rounded-[var(--radius-control)] border px-3.5 py-3 text-left transition-[background-color,border-color,transform] duration-150 active:scale-[0.99]",
                        isNext
                          ? "border-accent/40 bg-accent-soft/50"
                          : "border-transparent bg-surface-2 hover:bg-surface-3",
                      )}
                    >
                      <span className="tabular w-[70px] shrink-0 text-sm font-semibold text-ink-2">
                        {formatClock(d.time)}
                      </span>
                      <span className="min-w-0 flex-1">
                        <span
                          className={cn(
                            "block truncate text-[15px] font-medium transition-colors",
                            isTaken && "text-ink-3 line-through",
                          )}
                        >
                          {d.name}{" "}
                          {d.strength && (
                            <span className="font-normal text-ink-3">{d.strength}</span>
                          )}
                        </span>
                        {d.instructions && (
                          <span className="block truncate text-xs text-ink-3">
                            {d.instructions}
                          </span>
                        )}
                      </span>
                      {isNext && !isTaken && (
                        <span className="chip chip--accent shrink-0">Next</span>
                      )}
                      <span
                        className={cn(
                          "grid size-7 shrink-0 place-items-center rounded-full border-2 transition-colors duration-150",
                          isTaken
                            ? "border-accent bg-accent text-accent-ink"
                            : "border-line-strong text-transparent group-hover:border-ink-3",
                        )}
                        aria-hidden
                      >
                        <AnimatePresence>
                          {isTaken && (
                            <motion.span
                              initial={{ scale: 0.5, opacity: 0 }}
                              animate={{ scale: 1, opacity: 1 }}
                              exit={{ scale: 0.5, opacity: 0 }}
                              transition={{ type: "spring", duration: 0.3, bounce: 0.4 }}
                            >
                              <Check size={14} weight="bold" />
                            </motion.span>
                          )}
                        </AnimatePresence>
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </section>
        ))}
      </div>
      <p className="mt-4 flex items-center gap-1.5 text-xs text-ink-3">
        <Pill size={13} /> Ticks are saved on this device only.
      </p>
    </div>
  );
}
