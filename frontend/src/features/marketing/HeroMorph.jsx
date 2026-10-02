import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { CalendarCheck, CheckCircle, FilePdf, ListChecks, Sparkle } from "@phosphor-icons/react";
import { Chip } from "@/components/ui/Chip";

const EASE = [0.23, 1, 0.32, 1];

const RX = [
  {
    name: "Amoxicillin",
    strength: "500 mg",
    raw: "1-0-1 x 7 days",
    sched: "8:00 AM, 8:00 PM",
    conf: 98,
  },
  { name: "Ibuprofen", strength: "400 mg", raw: "SOS, max TDS", sched: "As needed", conf: 91 },
  { name: "Cetirizine", strength: "10 mg", raw: "HS x 5 days", sched: "10:00 PM", conf: 96 },
];

// paper -> scanning -> extracted -> actions -> (hold) -> paper ...
const PHASES = ["paper", "scanning", "extracted", "actions"];
const DURATIONS = { paper: 1400, scanning: 1900, extracted: 2300, actions: 3600 };

function usePhase(reduce) {
  const [phase, setPhase] = useState(reduce ? "actions" : "paper");
  useEffect(() => {
    if (reduce) return;
    const t = setTimeout(() => {
      setPhase((p) => PHASES[(PHASES.indexOf(p) + 1) % PHASES.length]);
    }, DURATIONS[phase]);
    return () => clearTimeout(t);
  }, [phase, reduce]);
  return phase;
}

/** The hero's live product preview: a prescription becomes structured rows, then actions. */
export function HeroMorph() {
  const reduce = useReducedMotion();
  const phase = usePhase(reduce);
  const showRows = phase === "extracted" || phase === "actions";

  return (
    <div className="relative mx-auto w-full max-w-[540px] lg:max-w-none" aria-hidden>
      {/* Soft evergreen glow behind the stack */}
      <div className="absolute -inset-10 -z-10 rounded-[48px] bg-[radial-gradient(60%_55%_at_60%_40%,var(--accent-soft),transparent_70%)] opacity-90" />

      {/* The source document */}
      <motion.div
        className="card relative overflow-hidden p-5 sm:p-6"
        initial={reduce ? false : { opacity: 0, rotate: -4, y: 24 }}
        animate={{ opacity: 1, rotate: -2.5, y: 0 }}
        transition={{ duration: 0.9, ease: EASE, delay: 0.15 }}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-[13px] font-semibold">Riverside Family Clinic</p>
            <p className="text-xs text-ink-3">Dr. Imani Oduya, MD · Internal Medicine</p>
          </div>
          <span className="hidden shrink-0 items-center gap-1.5 whitespace-nowrap text-xs text-ink-3 sm:inline-flex">
            <FilePdf size={15} weight="duotone" />
            rx-0304.pdf
          </span>
        </div>
        <div className="divider-dashed my-4" />
        <p className="font-mono text-[11px] uppercase tracking-wider text-ink-3">
          Rx · Mar 4, 2026
        </p>
        <ul className="mt-3 grid grid-cols-1 gap-2.5 font-mono text-[13px] text-ink-2">
          {RX.map((r) => (
            <li key={r.name} className="flex flex-wrap gap-x-3">
              <span className="text-ink">
                {r.name} {r.strength}
              </span>
              <span>{r.raw}</span>
            </li>
          ))}
        </ul>
        <p className="mt-4 font-mono text-[12px] text-ink-3">
          Review in 2 weeks. CBC before visit.
        </p>

        {/* Scan beam */}
        <AnimatePresence>
          {phase === "scanning" && (
            <motion.div
              key="beam"
              className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-transparent via-[color-mix(in_oklch,var(--accent),transparent_82%)] to-transparent"
              initial={{ y: "-100%" }}
              animate={{ y: "420%" }}
              exit={{ opacity: 0 }}
              transition={{ duration: 1.7, ease: [0.77, 0, 0.175, 1] }}
            />
          )}
        </AnimatePresence>
      </motion.div>

      {/* The structured result */}
      <motion.div
        className="card relative -mt-10 ml-6 p-4 shadow-lg sm:-mt-14 sm:ml-14 sm:p-5"
        initial={reduce ? false : { opacity: 0, y: 32 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.9, ease: EASE, delay: 0.35 }}
      >
        <div className="mb-3 flex items-center justify-between">
          <p className="flex items-center gap-2 text-[13px] font-semibold">
            <Sparkle size={15} weight="fill" className="text-accent" />
            Extracted for review
          </p>
          <Chip tone={phase === "scanning" ? "warn" : "accent"} live={phase === "scanning"}>
            {phase === "scanning" ? "Reading" : phase === "paper" ? "Queued" : "3 medications"}
          </Chip>
        </div>

        <ul className="grid grid-cols-1 gap-1.5">
          {RX.map((r, i) => (
            <li
              key={r.name}
              className="relative h-[52px] overflow-hidden rounded-[var(--radius-control)]"
            >
              <AnimatePresence mode="popLayout" initial={false}>
                {showRows ? (
                  <motion.div
                    key="row"
                    className="absolute inset-0 flex items-center justify-between gap-3 rounded-[var(--radius-control)] bg-surface-2 px-3"
                    initial={{ opacity: 0, y: 10, filter: "blur(4px)" }}
                    animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                    exit={{ opacity: 0, transition: { duration: 0.2 } }}
                    transition={{ duration: 0.45, ease: EASE, delay: i * 0.12 }}
                  >
                    <div className="min-w-0">
                      <p className="truncate text-[13px] font-semibold">
                        {r.name} <span className="font-normal text-ink-3">{r.strength}</span>
                      </p>
                      <p className="truncate text-xs text-ink-2">{r.sched}</p>
                    </div>
                    <Chip tone={r.conf < 95 ? "warn" : "accent"} className="tabular">
                      {r.conf}%
                    </Chip>
                  </motion.div>
                ) : (
                  <motion.div
                    key="skeleton"
                    className="absolute inset-0 flex items-center gap-3 px-3"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0, transition: { duration: 0.15 } }}
                  >
                    <div className="grid grid-cols-1 flex-1 gap-2">
                      <div className="skeleton skeleton--text w-2/5" />
                      <div className="skeleton skeleton--text w-1/4" />
                    </div>
                    <div className="skeleton h-5 w-11 rounded-full" />
                  </motion.div>
                )}
              </AnimatePresence>
            </li>
          ))}
        </ul>

        <div className="mt-3 flex min-h-[28px] flex-wrap gap-2">
          <AnimatePresence>
            {phase === "actions" &&
              [
                { icon: CalendarCheck, label: "2 reminders to Calendar" },
                { icon: ListChecks, label: "CBC test added to Tasks" },
                { icon: CheckCircle, label: "Follow-up Mar 18" },
              ].map(({ icon: Icon, label }, i) => (
                <motion.span
                  key={label}
                  className="chip chip--accent"
                  initial={{ opacity: 0, scale: 0.92, y: 6 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, transition: { duration: 0.15 } }}
                  transition={{ duration: 0.35, ease: EASE, delay: i * 0.1 }}
                >
                  <Icon size={13} weight="bold" />
                  {label}
                </motion.span>
              ))}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
}
