import { useEffect, useRef, useState } from "react";
import { motion, useInView, useReducedMotion } from "motion/react";
import {
  ArrowSquareOut,
  CalendarBlank,
  ChatsCircle,
  CheckSquare,
  ClockCounterClockwise,
  LinkSimple,
  Square,
} from "@phosphor-icons/react";
import { Chip } from "@/components/ui/Chip";
import { Reveal } from "./Reveal";
import { cn } from "@/lib/cn";

const EASE = [0.23, 1, 0.32, 1];
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function Cell({ className, title, body, icon: Icon, children, delay = 0, tone = "surface" }) {
  return (
    <Reveal
      delay={delay}
      className={cn(
        "card card--interactive relative flex flex-col overflow-hidden p-6",
        // Fixed deep evergreen in both themes so the translucent chips keep AA contrast.
        tone === "accent" &&
          "border-transparent bg-[oklch(0.36_0.075_163)] text-[oklch(0.97_0.01_160)]",
        tone === "sunken" && "bg-surface-2",
        className,
      )}
    >
      <div className="flex items-center gap-2.5">
        <Icon size={20} weight="duotone" className={tone === "accent" ? "" : "text-accent"} />
        <h3 className="text-[17px] font-semibold">{title}</h3>
      </div>
      <p
        className={cn("mt-2 max-w-[44ch] text-sm", tone === "accent" ? "opacity-85" : "text-ink-2")}
      >
        {body}
      </p>
      <div className="mt-6 flex-1">{children}</div>
    </Reveal>
  );
}

function CalendarWeek() {
  // Mock schedule: morning and evening doses, last two days of the course faded.
  return (
    <div className="grid grid-cols-7 gap-1.5 bg-[radial-gradient(var(--line)_1px,transparent_1px)] [background-size:14px_14px]">
      {DAYS.map((d, i) => (
        <div key={d} className="rounded-[var(--radius-control)] border border-line bg-surface p-2">
          <p className="text-center text-[11px] font-medium text-ink-3">{d}</p>
          <div className="mt-2 grid grid-cols-1 gap-1">
            {["8:00", "20:00"].map((t) => (
              <span
                key={t}
                className={cn(
                  "rounded-md px-1 py-1 text-center font-mono text-[10px]",
                  i < 5 ? "bg-accent-soft text-accent-soft-ink" : "bg-surface-2 text-ink-3",
                )}
              >
                {t}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function ChatPreview() {
  return (
    <div className="grid grid-cols-1 gap-3">
      <div className="ml-auto max-w-[85%] rounded-2xl rounded-br-md bg-ink px-3.5 py-2.5 text-sm text-bg">
        How often do I take Metformin?
      </div>
      <div className="max-w-[92%] rounded-2xl rounded-bl-md border border-line bg-surface px-3.5 py-2.5 text-sm">
        Twice daily after meals, for 90 days, according to your Feb 11 prescription.
        <span className="ml-1 align-super text-[10px] font-semibold text-accent">[1]</span>
        <div className="mt-2.5 flex flex-wrap gap-1.5">
          <Chip tone="accent">
            <ArrowSquareOut size={12} /> rx-0211.pdf · page 1
          </Chip>
        </div>
      </div>
      <p className="text-xs text-ink-3">Answers come only from your records, with sources.</p>
    </div>
  );
}

function TaskList() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, amount: 0.6 });
  const reduce = useReducedMotion();
  const [done, setDone] = useState(reduce ? 1 : 0);
  useEffect(() => {
    if (!inView || reduce) return;
    const t = setTimeout(() => setDone(1), 700);
    return () => clearTimeout(t);
  }, [inView, reduce]);

  const items = ["Get CBC test before Mar 18", "Finish Amoxicillin course", "Upload lab report"];
  return (
    <ul ref={ref} className="grid grid-cols-1 gap-2">
      {items.map((t, i) => {
        const checked = i < done;
        return (
          <li key={t} className="flex items-center gap-2.5 text-sm">
            <motion.span
              animate={{ scale: checked ? [1, 1.2, 1] : 1 }}
              transition={{ duration: 0.35, ease: EASE }}
              className={checked ? "text-accent" : "text-ink-3"}
            >
              {checked ? <CheckSquare size={18} weight="fill" /> : <Square size={18} />}
            </motion.span>
            <span className={cn("transition-colors", checked && "text-ink-3 line-through")}>
              {t}
            </span>
          </li>
        );
      })}
    </ul>
  );
}

function MiniTimeline() {
  const rows = [
    ["Mar 18", "Follow-up visit"],
    ["Mar 4", "Prescription confirmed"],
    ["Feb 12", "Lipid panel added"],
  ];
  return (
    <ol className="relative grid grid-cols-1 gap-3 pl-5 before:absolute before:inset-y-1 before:left-[5px] before:w-px before:bg-line-strong">
      {rows.map(([d, t]) => (
        <li key={t} className="relative text-sm">
          <span className="absolute -left-5 top-1.5 size-[11px] rounded-full border-2 border-surface bg-accent" />
          <span className="text-xs text-ink-3">{d}</span>
          <p className="font-medium">{t}</p>
        </li>
      ))}
    </ol>
  );
}

function ShareLink() {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex min-w-0 items-center gap-3 rounded-full bg-[oklch(1_0_0/0.14)] py-2 pl-4 pr-2 ring-1 ring-[oklch(1_0_0/0.2)]">
        <LinkSimple size={16} weight="bold" />
        <span className="truncate font-mono text-[13px]">medspace.app/s/k3J9q-Wm…</span>
        <span className="ml-auto shrink-0 rounded-full px-2.5 py-1 text-[11px] font-semibold ring-1 ring-[oklch(1_0_0/0.35)]">
          Expires in 6 days
        </span>
      </div>
      <div className="flex flex-wrap gap-2 text-[12px] font-medium">
        {["2 documents", "Max 5 views", "Every view logged", "Revoke anytime"].map((t) => (
          <span key={t} className="rounded-full bg-[oklch(1_0_0/0.12)] px-3 py-1.5">
            {t}
          </span>
        ))}
      </div>
    </div>
  );
}

export function FeatureBento() {
  return (
    <section id="features" className="mx-auto max-w-[1280px] px-4 py-20 sm:px-6 lg:py-28">
      <Reveal className="max-w-2xl">
        <h2 className="text-3xl font-semibold tracking-tight sm:text-5xl">
          One space for the whole routine.
        </h2>
        <p className="mt-4 max-w-[54ch] text-lg text-ink-2">
          Confirmed records flow into the tools you already use, and stay searchable when you need
          them.
        </p>
      </Reveal>

      <div className="mt-12 grid grid-cols-1 gap-4 md:grid-cols-6">
        <Cell
          className="md:col-span-4"
          icon={CalendarBlank}
          title="Google Calendar reminders"
          body="Recurring dose reminders built from your confirmed schedule. Appointments and follow-ups too."
        >
          <CalendarWeek />
        </Cell>
        <Cell
          className="md:col-span-2 md:row-span-2"
          tone="sunken"
          icon={ChatsCircle}
          title="Ask MedSpace"
          body="Questions about your own records, answered with the exact document and page."
          delay={0.06}
        >
          <ChatPreview />
        </Cell>
        <Cell
          className="md:col-span-2"
          icon={CheckSquare}
          title="Google Tasks"
          body="One-off actions become to-dos you can tick off."
          delay={0.1}
        >
          <TaskList />
        </Cell>
        <Cell
          className="md:col-span-2"
          icon={ClockCounterClockwise}
          title="Health timeline"
          body="Everything confirmed, in order."
          delay={0.14}
        >
          <MiniTimeline />
        </Cell>
        <Cell
          className="md:col-span-6"
          tone="accent"
          icon={LinkSimple}
          title="Secure sharing"
          body="Send a caregiver or a new doctor exactly what they need through scoped links that expire on schedule."
          delay={0.08}
        >
          <ShareLink />
        </Cell>
      </div>
    </section>
  );
}
