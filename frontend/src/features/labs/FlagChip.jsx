import { cn } from "@/lib/cn";
import { FLAG_LABELS } from "./format";

/** Compares a value with the range printed on its own report, nothing more. */
export function FlagChip({ flag, className }) {
  if (!flag) return null;
  return (
    <span
      className={cn("chip shrink-0", flag === "normal" ? "" : "chip--warn", className)}
      title="Compared with the reference range printed on the report"
    >
      {FLAG_LABELS[flag]}
    </span>
  );
}
