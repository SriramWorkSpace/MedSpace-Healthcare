import { addDays, format, parseISO } from "date-fns";

export const STATE_LABELS = {
  taken: "Taken",
  skipped: "Skipped",
  unlogged: "Not logged",
  upcoming: "Later today",
};

/** Summary of one day's scheduled doses for a cell: what share is taken, and the dominant state. */
export function daySummary(doses) {
  const past = doses.filter((d) => d.state !== "upcoming");
  const taken = past.filter((d) => d.state === "taken").length;
  const skipped = past.filter((d) => d.state === "skipped").length;
  if (!past.length) return { tone: "upcoming", taken, total: doses.length };
  if (taken === past.length) return { tone: "taken", taken, total: past.length };
  if (taken > 0) return { tone: "partial", taken, total: past.length };
  if (skipped === past.length) return { tone: "skipped", taken, total: past.length };
  return { tone: "unlogged", taken, total: past.length };
}

/** Every calendar day from start to end (ISO strings), with the history entry when scheduled. */
export function fillDays(start, end, days) {
  const byDate = new Map(days.map((d) => [d.date, d]));
  const out = [];
  for (let d = parseISO(start); format(d, "yyyy-MM-dd") <= end; d = addDays(d, 1)) {
    const key = format(d, "yyyy-MM-dd");
    out.push({ date: key, entry: byDate.get(key) ?? null });
  }
  return out;
}

export function percent(rate) {
  return rate == null ? null : `${Math.round(rate * 100)}%`;
}

export const TONE_CLASS = {
  taken: "bg-accent",
  partial: "bg-accent/45",
  skipped: "bg-warn-soft ring-1 ring-inset ring-warn/50",
  unlogged: "bg-surface-3",
  upcoming: "bg-transparent ring-1 ring-inset ring-line-strong",
  none: "bg-transparent",
};
