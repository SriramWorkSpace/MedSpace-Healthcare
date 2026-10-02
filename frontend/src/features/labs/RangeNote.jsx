import { Info } from "@phosphor-icons/react";
import { cn } from "@/lib/cn";

export function RangeNote({ className }) {
  return (
    <p className={cn("flex items-start gap-2 text-sm text-ink-2", className)}>
      <Info size={16} className="mt-0.5 shrink-0 text-ink-3" />
      Each result is compared only with the reference range printed on its own report. Your
      clinician can tell you what a result means for you.
    </p>
  );
}
