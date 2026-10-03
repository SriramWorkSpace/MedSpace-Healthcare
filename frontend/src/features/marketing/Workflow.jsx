import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion, useInView, useReducedMotion } from "motion/react";
import {
  CalendarCheck,
  CheckCircle,
  ClockCounterClockwise,
  CloudArrowUp,
  MagnifyingGlass,
  PencilSimpleLine,
  Sparkle,
} from "@phosphor-icons/react";
import { Chip } from "@/components/ui/Chip";
import { cn } from "@/lib/cn";

const EASE = [0.23, 1, 0.32, 1];

const STEPS = [
  {
    key: "upload",
    verb: "Upload",
    title: "Drop in whatever the clinic handed you.",
    body: "PDFs, phone photos, scans. Files are checked, de-duplicated and stored privately before anything else happens.",
    icon: CloudArrowUp,
  },
  {
    key: "extract",
    verb: "Extract",
    title: "Every dose, pulled out and tied to its page.",
    body: "Medicines, strengths, frequency, duration, prescriber and follow-ups. Each field carries a confidence score and its source page.",
    icon: Sparkle,
  },
  {
    key: "review",
    verb: "Review",
    title: "You check it against the original.",
    body: "Side by side with the document. Shaky fields are flagged, shorthand like 1-0-1 or TDS becomes real clock times you can edit.",
    icon: PencilSimpleLine,
  },
  {
    key: "organize",
    verb: "Organize",
    title: "Confirmed records land on your timeline.",
    body: "Prescriptions, medications, appointments and reports in one chronological view instead of a drawer of paper.",
    icon: ClockCounterClockwise,
  },
  {
    key: "act",
    verb: "Act",
    title: "Reminders and to-dos, where you already look.",
    body: "Dose reminders go to Google Calendar, one-off tasks go to Google Tasks, and Ask MedSpace answers with citations.",
    icon: CalendarCheck,
  },
];

function Step({ step, index, onActive }) {
  const ref = useRef(null);
  const inView = useInView(ref, { amount: 0.6 });
  useEffect(() => {
    if (inView) onActive(index);
  }, [inView, index, onActive]);
  const Icon = step.icon;
  return (
    <div ref={ref} className="flex min-h-[46vh] flex-col justify-center py-10 lg:min-h-[62vh]">
      <span className="mb-4 inline-flex size-10 items-center justify-center rounded-xl bg-accent-soft text-accent-soft-ink">
        <Icon size={20} weight="duotone" />
      </span>
      <p className="text-sm font-semibold text-accent">{step.verb}</p>
      <h3 className="mt-2 max-w-[22ch] text-2xl font-semibold tracking-tight sm:text-3xl">
        {step.title}
      </h3>
      <p className="mt-3 max-w-[48ch] text-[15px] leading-relaxed text-ink-2">{step.body}</p>
    </div>
  );
}

function Preview({ stepKey }) {
  switch (stepKey) {
    case "upload":
      return (
        <div className="grid grid-cols-1 h-full place-items-center">
          <div className="w-full max-w-sm rounded-card border-2 border-dashed border-accent/50 bg-accent-soft/40 p-8 text-center">
            <CloudArrowUp size={36} weight="duotone" className="mx-auto text-accent" />
            <p className="mt-3 font-semibold">Drop files to upload</p>
            <p className="mt-1 text-sm text-ink-2">PDF, JPG or PNG up to 15 MB</p>
            <div className="mt-5 overflow-hidden rounded-full bg-surface-3">
              <motion.div
                className="h-1.5 rounded-full bg-accent"
                initial={{ width: "8%" }}
                animate={{ width: "100%" }}
                transition={{ duration: 1.6, ease: EASE }}
              />
            </div>
          </div>
        </div>
      );
    case "extract":
      return (
        <div className="grid grid-cols-1 content-center gap-2">
          {[
            ["Medicine", "Metformin 500 mg", 99],
            ["Frequency", "BD after meals", 95],
            ["Duration", "90 days", 88],
            ["Prescriber", "Dr. Tomas Varga", 97],
          ].map(([k, v, c], i) => (
            <motion.div
              key={k}
              className="flex items-center justify-between rounded-[var(--radius-control)] border border-line bg-surface px-4 py-3"
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: i * 0.08, ease: EASE }}
            >
              <div>
                <p className="text-xs text-ink-3">{k}</p>
                <p className="text-sm font-semibold">{v}</p>
              </div>
              <Chip tone={c < 90 ? "warn" : "accent"} className="tabular">
                {c}% · p.1
              </Chip>
            </motion.div>
          ))}
        </div>
      );
    case "review":
      return (
        <div className="grid h-full grid-cols-2 gap-3">
          <div className="rounded-[var(--radius-control)] bg-surface-2 p-4 font-mono text-[12px] leading-6 text-ink-2">
            <p className="text-ink">Metformin 500mg</p>
            <p className="rounded bg-warn-soft px-1 text-warn-ink">BD p.c. x 90/7</p>
            <p>Atorvastatin 20mg HS</p>
          </div>
          <div className="grid grid-cols-1 content-start gap-2">
            <label className="field">
              <span className="field__label text-xs">Frequency</span>
              <span className="input input--attention flex items-center text-sm">Twice daily</span>
            </label>
            <div className="flex gap-1.5">
              <Chip tone="accent">8:00 AM</Chip>
              <Chip tone="accent">8:00 PM</Chip>
            </div>
            <span className="btn btn--primary btn--sm mt-2 w-fit">
              <CheckCircle size={14} weight="bold" /> Confirm
            </span>
          </div>
        </div>
      );
    case "organize":
      return (
        <ol className="relative grid grid-cols-1 content-center gap-5 pl-6 before:absolute before:inset-y-2 before:left-[7px] before:w-px before:bg-line-strong">
          {[
            ["Mar 18", "Follow-up with Dr. Oduya", "Appointment"],
            ["Mar 4", "Amoxicillin course started", "Medication"],
            ["Feb 12", "Lipid panel uploaded", "Report"],
          ].map(([d, t, k], i) => (
            <motion.li
              key={t}
              className="relative"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: i * 0.1, ease: EASE }}
            >
              <span className="absolute -left-6 top-1.5 size-[15px] rounded-full border-[3px] border-bg bg-accent" />
              <p className="text-xs text-ink-3">{d}</p>
              <p className="text-sm font-semibold">{t}</p>
              <Chip className="mt-1.5">{k}</Chip>
            </motion.li>
          ))}
        </ol>
      );
    default:
      return (
        <div className="grid grid-cols-1 content-center gap-3">
          <div className="rounded-[var(--radius-control)] border border-line bg-surface p-4">
            <p className="flex items-center gap-2 text-xs font-semibold text-ink-3">
              <CalendarCheck size={14} /> Google Calendar
            </p>
            <p className="mt-1.5 text-sm font-semibold">Metformin 500 mg · 8:00 AM</p>
            <p className="text-xs text-ink-2">Daily until Jun 2</p>
          </div>
          <div className="rounded-[var(--radius-control)] border border-line bg-surface p-4">
            <p className="flex items-center gap-2 text-xs font-semibold text-ink-3">
              <MagnifyingGlass size={14} /> Ask MedSpace
            </p>
            <p className="mt-1.5 text-sm">Take it twice daily after meals for 90 days.</p>
            <Chip tone="accent" className="mt-2">
              Source · rx-0211.pdf p.1
            </Chip>
          </div>
        </div>
      );
  }
}

export function Workflow() {
  const [active, setActive] = useState(0);
  const reduce = useReducedMotion();

  return (
    <section id="how-it-works" className="shell shell--marketing py-20 lg:py-28">
      <div className="max-w-2xl">
        <h2 className="text-3xl font-semibold tracking-tight sm:text-5xl">
          From paper to plan in five steps.
        </h2>
        <p className="mt-4 max-w-[52ch] text-lg text-ink-2">
          Upload, extract, review, organize, act. Nothing becomes official until you say so.
        </p>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-x-16 lg:grid-cols-[1fr_1.05fr]">
        <div>
          {STEPS.map((s, i) => (
            <Step key={s.key} step={s} index={i} onActive={setActive} />
          ))}
        </div>

        {/* Sticky preview (desktop only; the copy carries the story on mobile) */}
        <div className="hidden lg:block">
          <div className="sticky top-[calc(var(--nav-h)+12vh)]">
            <div className="mb-4 flex gap-1.5" role="presentation">
              {STEPS.map((s, i) => (
                <span
                  key={s.key}
                  className={cn(
                    "h-1 flex-1 rounded-full transition-colors duration-300",
                    i <= active ? "bg-accent" : "bg-line",
                  )}
                />
              ))}
            </div>
            <div className="card h-[380px] overflow-hidden bg-[linear-gradient(180deg,var(--surface),var(--surface-2))] p-6">
              <AnimatePresence mode="wait">
                <motion.div
                  key={STEPS[active].key}
                  className="h-full"
                  initial={reduce ? { opacity: 0 } : { opacity: 0, y: 12, filter: "blur(3px)" }}
                  animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                  exit={reduce ? { opacity: 0 } : { opacity: 0, y: -8, filter: "blur(3px)" }}
                  transition={{ duration: 0.3, ease: EASE }}
                >
                  <Preview stepKey={STEPS[active].key} />
                </motion.div>
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
