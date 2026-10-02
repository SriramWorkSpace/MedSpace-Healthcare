import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { CheckCircle, CircleNotch, Circle } from "@phosphor-icons/react";
import { PROCESSING_PUNS } from "@/easter-eggs/puns";
import { cn } from "@/lib/cn";

const STEPS = [
  { key: "upload", label: "File received and stored privately" },
  { key: "read", label: "Reading every page" },
  { key: "extract", label: "Pulling out medicines, doses and dates" },
  { key: "normalize", label: "Turning shorthand into a schedule" },
];

/** Shown while a document is queued or processing. Steps advance on a gentle timer for feel;
 *  the real status comes from polling and swaps this view out as soon as it's ready. */
export function ProcessingState({ status }) {
  const reduce = useReducedMotion();
  const [tick, setTick] = useState(0);
  const [punIndex, setPunIndex] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setTick((n) => Math.min(n + 1, STEPS.length - 1)), 1400);
    const p = setInterval(() => setPunIndex((n) => (n + 1) % PROCESSING_PUNS.length), 2800);
    return () => {
      clearInterval(t);
      clearInterval(p);
    };
  }, []);

  const current = status === "queued" ? 0 : Math.max(1, tick);

  return (
    <div className="card mx-auto max-w-xl overflow-hidden" role="status" aria-live="polite">
      <div className="relative h-1.5 overflow-hidden bg-surface-3">
        <motion.div
          className="absolute inset-y-0 left-0 w-1/3 rounded-full bg-accent"
          animate={reduce ? undefined : { x: ["-100%", "300%"] }}
          transition={{ duration: 1.6, repeat: Infinity, ease: [0.77, 0, 0.175, 1] }}
        />
      </div>
      <div className="p-7">
        <h2 className="text-xl font-semibold">Reading your document</h2>
        <div className="mt-1 h-5 text-sm text-ink-3">
          <AnimatePresence mode="wait">
            <motion.p
              key={punIndex}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.25 }}
            >
              {PROCESSING_PUNS[punIndex]}
            </motion.p>
          </AnimatePresence>
        </div>
        <ol className="mt-6 grid grid-cols-1 gap-3.5">
          {STEPS.map((s, i) => {
            const done = i < current;
            const active = i === current;
            return (
              <li key={s.key} className="flex items-center gap-3 text-sm">
                <span className={cn(done ? "text-accent" : active ? "text-warn" : "text-ink-3")}>
                  {done ? (
                    <CheckCircle size={20} weight="fill" />
                  ) : active ? (
                    <CircleNotch size={20} weight="bold" className="animate-spin" />
                  ) : (
                    <Circle size={20} />
                  )}
                </span>
                <span className={cn(done || active ? "text-ink" : "text-ink-3")}>{s.label}</span>
              </li>
            );
          })}
        </ol>
        <p className="mt-6 text-xs text-ink-3">
          Usually a few seconds. You can leave this page; we'll keep working.
        </p>
      </div>
    </div>
  );
}
