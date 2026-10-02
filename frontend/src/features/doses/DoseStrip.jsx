import { cn } from "@/lib/cn";
import { formatDate } from "@/lib/format";
import { TONE_CLASS, daySummary, fillDays } from "./states";

function describe(date, entry) {
  const day = formatDate(date, "EEE, MMM d");
  if (!entry) return `${day}: nothing scheduled`;
  const s = daySummary(entry.doses);
  if (s.tone === "upcoming") return `${day}: later today`;
  return `${day}: ${s.taken} of ${s.total} taken`;
}

/** One small cell per day; color shows how much of that day's schedule was marked taken. */
export function DoseStrip({ start, end, days, className }) {
  const cells = fillDays(start, end, days);
  return (
    <ol className={cn("flex gap-[3px]", className)} aria-label="Daily doses">
      {cells.map(({ date, entry }) => {
        const tone = entry ? daySummary(entry.doses).tone : "none";
        return (
          <li
            key={date}
            title={describe(date, entry)}
            className={cn(
              "h-4 min-w-0 flex-1 rounded-[3px]",
              TONE_CLASS[tone],
              !entry && "border border-dashed border-line",
            )}
          >
            <span className="sr-only">{describe(date, entry)}</span>
          </li>
        );
      })}
    </ol>
  );
}
