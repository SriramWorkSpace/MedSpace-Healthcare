import { cn } from "@/lib/cn";

/** @param {{ tone?: "neutral"|"accent"|"warn"|"danger", live?: boolean } & Record<string, any>} props */
export function Chip({ tone = "neutral", live = false, className, children, ...props }) {
  return (
    <span
      className={cn("chip", tone !== "neutral" && `chip--${tone}`, live && "chip--live", className)}
      {...props}
    >
      {children}
    </span>
  );
}
