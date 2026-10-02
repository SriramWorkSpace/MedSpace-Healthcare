import { formatDate } from "@/lib/format";

export const UNITS = ["tablets", "capsules", "ml", "puffs", "sachets", "drops", "patches", "units"];

const trim = (n) => Number.parseFloat(Number(n).toFixed(2)).toString();

/** "About 10 tablets left" (estimates are always labelled as such). */
export function leftLabel(s) {
  return `About ${trim(s.estimated_left)} ${s.unit} left`;
}

export function runsOutLabel(s) {
  switch (s.status) {
    case "out":
      return "Estimated to have run out";
    case "course_covered":
      return "Enough for the rest of the course";
    case "as_needed":
      return "Taken as needed, so no run-out date";
    default:
      return s.runs_out_on
        ? `Runs out around ${formatDate(s.runs_out_on, "MMM d")}`
        : "No run-out date in the next year";
  }
}

export { trim as formatUnits };
