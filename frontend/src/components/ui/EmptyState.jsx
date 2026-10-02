import { motion, useReducedMotion } from "motion/react";
import { cn } from "@/lib/cn";

export function EmptyState({ icon: Icon, title, description, action, quip, className }) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.23, 1, 0.32, 1] }}
      className={cn(
        "flex flex-col items-center rounded-card border border-dashed border-line-strong bg-surface/60 px-6 py-14 text-center",
        className,
      )}
    >
      {Icon && (
        <div className="mb-5 grid grid-cols-1 size-14 place-items-center rounded-2xl bg-accent-soft text-accent-soft-ink">
          <Icon size={26} weight="duotone" />
        </div>
      )}
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && <p className="mt-2 max-w-[42ch] text-sm text-ink-2">{description}</p>}
      {action && <div className="mt-6">{action}</div>}
      {quip && <p className="mt-6 text-xs italic text-ink-3">{quip}</p>}
    </motion.div>
  );
}
