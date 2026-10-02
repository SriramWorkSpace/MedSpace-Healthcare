import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { Check, Pill, Sun, SunHorizon, Moon, MoonStars } from "@phosphor-icons/react";
import { cn } from "@/lib/cn";
import { useSetDose } from "@/features/doses/api";
import { formatClock } from "@/lib/format";

const SLOTS = [
  { key: "morning", label: "Morning", icon: Sun, until: "12:00" },
  { key: "afternoon", label: "Afternoon", icon: SunHorizon, until: "17:00" },
  { key: "evening", label: "Evening", icon: Moon, until: "21:00" },
  { key: "night", label: "Night", icon: MoonStars, until: "24:00" },
];

const slotFor = (time) => SLOTS.find((s) => time < s.until)?.key ?? "night";

/**
 * Ticks used to live in localStorage. Move today's leftovers to the account once, then forget them.
 */
function useMigrateDeviceTicks(dateKey, doses, setDose) {
  const done = useRef(false);
  useEffect(() => {
    if (done.current) return;
    done.current = true;
    const key = `ms-taken-${dateKey}`;
    let ids;
    try {
      ids = JSON.parse(localStorage.getItem(key) ?? "[]");
      localStorage.removeItem(key);
    } catch {
      return;
    }
    for (const id of ids) {
      const dose = doses.find((d) => `${d.medication_id}@${d.time}` === id);
      if (dose && !dose.status) {
        setDose.mutate({
          medication_id: dose.medication_id,
          date: dateKey,
          time: dose.time,
          status: "taken",
        });
      }
    }
  }, [dateKey, doses, setDose]);
}

function nowHHMM() {
  const d = new Date();
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

export function TodaySchedule({ doses, dateKey }) {
  const setDose = useSetDose();
  useMigrateDeviceTicks(dateKey, doses, setDose);
  const [now] = useState(nowHHMM);
  const nextIndex = doses.findIndex((d) => d.time >= now && !d.status);
  const mark = (d, status) =>
    setDose.mutate({
      medication_id: d.medication_id,
      date: dateKey,
      time: d.time,
      status,
      fallbackState: d.time > now ? "upcoming" : "unlogged",
    });

  const groups = useMemo(() => {
    const out = SLOTS.map((s) => ({ ...s, items: [] }));
    doses.forEach((d, i) =>
      out.find((g) => g.key === slotFor(d.time)).items.push({ ...d, index: i }),
    );
    return out.filter((g) => g.items.length);
  }, [doses]);

  const doneCount = doses.filter((d) => d.status === "taken").length;

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
      <div className="grid grid-cols-1 gap-5">
        {groups.map(({ key, label, icon: Icon, items }) => (
          <section key={key} aria-label={label}>
            <p className="mb-2 flex items-center gap-1.5 text-xs font-medium text-ink-3">
              <Icon size={14} weight="bold" /> {label}
            </p>
            <ul className="grid grid-cols-1 gap-1.5">
              {items.map((d) => {
                const id = `${d.medication_id}@${d.time}`;
                const isTaken = d.status === "taken";
                const isSkipped = d.status === "skipped";
                const isNext = d.index === nextIndex;
                const label = `${d.name}${d.strength ? ` ${d.strength}` : ""} at ${formatClock(d.time)}`;
                return (
                  <li
                    key={id}
                    className={cn(
                      "group flex items-center gap-1 rounded-[var(--radius-control)] border pr-1.5 transition-colors duration-150",
                      isNext
                        ? "border-accent/40 bg-accent-soft/50"
                        : "border-transparent bg-surface-2 hover:bg-surface-3",
                    )}
                  >
                    <button
                      type="button"
                      onClick={() => mark(d, isTaken ? null : "taken")}
                      aria-pressed={isTaken}
                      aria-label={`${isTaken ? "Taken: " : "Mark taken: "}${label}`}
                      className="flex min-w-0 flex-1 items-center gap-3 rounded-[var(--radius-control)] px-3.5 py-3 text-left transition-transform duration-150 active:scale-[0.99]"
                    >
                      <span className="tabular w-[70px] shrink-0 text-sm font-semibold text-ink-2">
                        {formatClock(d.time)}
                      </span>
                      <span className="min-w-0 flex-1">
                        <span
                          className={cn(
                            "block truncate text-[15px] font-medium transition-colors",
                            isTaken && "text-ink-3 line-through",
                            isSkipped && "text-ink-3",
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
                      {isNext && (
                        <span className="chip chip--accent hidden shrink-0 sm:inline-flex">
                          Next
                        </span>
                      )}
                      {isSkipped && <span className="chip shrink-0">Skipped</span>}
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
                    {!isTaken && (
                      <button
                        type="button"
                        onClick={() => mark(d, isSkipped ? null : "skipped")}
                        aria-label={`${isSkipped ? "Undo skip" : "Skip"}: ${label}`}
                        className="rounded-full px-2.5 py-1.5 text-xs font-medium text-ink-3 transition-[opacity,color] hover:bg-surface hover:text-ink-2 focus-visible:opacity-100 sm:opacity-0 sm:group-hover:opacity-100"
                      >
                        {isSkipped ? "Undo" : "Skip"}
                      </button>
                    )}
                  </li>
                );
              })}
            </ul>
          </section>
        ))}
      </div>
      <p className="mt-4 flex flex-wrap items-center gap-x-1.5 gap-y-1 text-xs text-ink-3">
        <Pill size={13} /> Saved to your account, so every device stays in sync.
        <Link to="/app/medications" className="text-accent hover:underline">
          See dose history
        </Link>
      </p>
    </div>
  );
}
