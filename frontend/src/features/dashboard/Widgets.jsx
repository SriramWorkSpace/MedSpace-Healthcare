import { Link } from "react-router";
import { motion } from "motion/react";
import {
  ArrowRight,
  CalendarCheck,
  CheckSquare,
  FileText,
  Flag,
  Pill,
  Stethoscope,
} from "@phosphor-icons/react";
import { format, parseISO } from "date-fns";
import { Chip } from "@/components/ui/Chip";
import { formatRelativeDay } from "@/lib/format";
import { cn } from "@/lib/cn";

export function Panel({ title, action, children, className }) {
  return (
    <section className={cn("card p-5 sm:p-6", className)}>
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-[15px] font-semibold">{title}</h2>
        {action}
      </div>
      {children}
    </section>
  );
}

export function StatTile({ label, value, to, icon: Icon }) {
  return (
    <Link to={to} className="card card--interactive flex items-center justify-between gap-3 p-4">
      <div>
        <p className="text-xs font-medium text-ink-3">{label}</p>
        <p className="tabular mt-1 text-2xl font-semibold tracking-tight">{value}</p>
      </div>
      <span className="grid grid-cols-1 size-10 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
        <Icon size={19} weight="duotone" />
      </span>
    </Link>
  );
}

const UPCOMING_ICON = {
  appointment: Stethoscope,
  task: CheckSquare,
  medication_end: Flag,
};

export function ComingUp({ items }) {
  if (!items.length) {
    return (
      <p className="text-sm text-ink-2">
        Nothing scheduled in the next six weeks. Enjoy the quiet.
      </p>
    );
  }
  return (
    <ul className="grid grid-cols-1 gap-1">
      {items.map((e) => {
        const Icon = UPCOMING_ICON[e.type] ?? CalendarCheck;
        const to = e.prescription_id ? `/app/prescriptions/${e.prescription_id}` : "/app/timeline";
        return (
          <li key={e.id}>
            <Link
              to={to}
              className="flex items-center gap-3 rounded-[var(--radius-control)] px-2 py-2.5 transition-colors hover:bg-surface-2"
            >
              <span className="grid grid-cols-1 size-9 shrink-0 place-items-center rounded-xl bg-surface-2 text-ink-2">
                <Icon size={17} weight="duotone" />
              </span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-medium">{e.title}</span>
                {e.subtitle && (
                  <span className="block truncate text-xs text-ink-3">{e.subtitle}</span>
                )}
              </span>
              <span className="tabular shrink-0 text-xs font-medium text-ink-2">
                {formatRelativeDay(e.date)}
              </span>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

export function NeedsReview({ items, processing }) {
  if (!items.length && !processing) return null;
  return (
    <div className="card overflow-hidden border-warn/40">
      <div className="flex items-center justify-between gap-3 bg-warn-soft/60 px-5 py-3">
        <p className="flex items-center gap-2 text-sm font-semibold text-warn-ink">
          <FileText size={16} weight="duotone" />
          {items.length ? `${items.length} waiting for your review` : "Reading your uploads"}
        </p>
        {processing > 0 && (
          <Chip tone="warn" live>
            {processing} processing
          </Chip>
        )}
      </div>
      {items.length > 0 && (
        <ul className="divide-y divide-line">
          {items.map((d) => (
            <li key={d.id}>
              <Link
                to={`/app/documents/${d.id}`}
                className="flex items-center justify-between gap-3 px-5 py-3 text-sm transition-colors hover:bg-surface-2"
              >
                <span className="truncate font-medium">{d.title}</span>
                <span className="inline-flex shrink-0 items-center gap-1 text-accent">
                  Review <ArrowRight size={13} weight="bold" />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function WeekStrip({ week }) {
  const max = Math.max(1, ...week.map((d) => d.doses));
  return (
    <ol className="grid grid-cols-7 gap-2" aria-label="Scheduled doses this week">
      {week.map((d, i) => {
        const date = parseISO(d.date);
        return (
          <li key={d.date} className="flex flex-col items-center gap-2">
            <div className="flex h-20 w-full items-end justify-center">
              <motion.div
                className={cn("w-full max-w-7 rounded-md", i === 0 ? "bg-accent" : "bg-accent/35")}
                initial={{ scaleY: 0 }}
                animate={{ scaleY: 1 }}
                style={{ height: `${Math.max(6, (d.doses / max) * 100)}%`, originY: 1 }}
                transition={{ duration: 0.5, delay: i * 0.04, ease: [0.23, 1, 0.32, 1] }}
                title={`${d.doses} doses`}
              />
            </div>
            <span className="tabular text-xs font-semibold">{d.doses}</span>
            <span
              className={cn("text-[11px]", i === 0 ? "font-semibold text-accent" : "text-ink-3")}
            >
              {i === 0 ? "Today" : format(date, "EEE")}
            </span>
          </li>
        );
      })}
    </ol>
  );
}

export function AsNeededList({ items }) {
  if (!items.length) return null;
  return (
    <ul className="flex flex-wrap gap-2">
      {items.map((m) => (
        <li
          key={m.medication_id}
          className="chip gap-1.5 py-1 pl-2 pr-3"
          title={m.instructions ?? undefined}
        >
          <Pill size={13} weight="duotone" className="text-accent" />
          {m.name} {m.strength && <span className="text-ink-3">{m.strength}</span>}
        </li>
      ))}
    </ul>
  );
}
