import { formatDate } from "@/lib/format";

export const FLAG_LABELS = {
  high: "Above range",
  low: "Below range",
  normal: "In range",
};

/** Trim floating-point noise: 0.30000000000000004 -> "0.3", 11 -> "11". */
export function formatNumber(n) {
  return Number.parseFloat(n.toFixed(2)).toString();
}

/** "Down 11 mg/dL since Mar 13, 2026". Direction only: whether that is good is not ours to say. */
export function describeChange(latest, previous) {
  if (!previous || latest.value == null || previous.value == null) return null;
  if ((latest.unit ?? "").toLowerCase() !== (previous.unit ?? "").toLowerCase()) return null;
  const diff = latest.value - previous.value;
  const since = `since ${formatDate(previous.collected_on)}`;
  if (Math.abs(diff) < 1e-9) return `No change ${since}`;
  const unit = latest.unit ? ` ${latest.unit}` : "";
  return `${diff > 0 ? "Up" : "Down"} ${formatNumber(Math.abs(diff))}${unit} ${since}`;
}

export function resultLabel(r) {
  return r.unit ? `${r.value_text} ${r.unit}` : r.value_text;
}
