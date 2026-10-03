import { useState } from "react";
import { Link, useParams } from "react-router";
import { addDays, format, parseISO, startOfWeek } from "date-fns";
import { motion, useReducedMotion } from "motion/react";
import { ArrowLeft, Info, Pill } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { SegmentedTabs } from "@/components/ui/Tabs";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { STREAK_LINE } from "@/easter-eggs/puns";
import { useMedicationAdherence, useSetDose } from "@/features/doses/api";
import { STATE_LABELS, daySummary, percent } from "@/features/doses/states";
import { cn } from "@/lib/cn";
import { formatClock, formatDate } from "@/lib/format";
import { useActing } from "@/features/circle/api";

const RANGES = [
  { key: 28, label: "4 weeks" },
  { key: 56, label: "8 weeks" },
  { key: 84, label: "12 weeks" },
];
const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const DOT = {
  taken: "bg-accent",
  skipped: "bg-warn",
  unlogged: "bg-line-strong",
  upcoming: "border border-line-strong bg-transparent",
};

function BackLink() {
  return (
    <Link
      to="/app/medications"
      className="tap mb-4 inline-flex items-center gap-1.5 rounded-lg text-sm text-ink-2 hover:text-accent"
    >
      <ArrowLeft size={14} weight="bold" />
      All medications
    </Link>
  );
}

function Stat({ label, value, hint }) {
  return (
    <div className="card card--flat p-4">
      <p className="text-xs text-ink-3">{label}</p>
      <p className="tabular mt-1 text-2xl font-semibold tracking-tight">{value}</p>
      {hint && <p className="mt-0.5 text-xs text-ink-3">{hint}</p>}
    </div>
  );
}

/** Weeks as rows, Monday first. Days outside the window or without doses are inert. */
function Calendar({ start, end, days, selected, onSelect }) {
  // The first visible day and every 1st carry the month, so month boundaries read clearly.
  const dayLabel = (date) =>
    date === start || date.endsWith("-01") ? formatDate(date, "MMM d") : Number(date.slice(8));
  const byDate = new Map(days.map((d) => [d.date, d]));
  const weeks = [];
  let cursor = startOfWeek(parseISO(start), { weekStartsOn: 1 });
  while (format(cursor, "yyyy-MM-dd") <= end) {
    weeks.push(Array.from({ length: 7 }, (_, i) => format(addDays(cursor, i), "yyyy-MM-dd")));
    cursor = addDays(cursor, 7);
  }
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[320px] table-fixed border-separate border-spacing-1">
        <caption className="sr-only">Doses by day. Select a day to review or change it.</caption>
        <thead>
          <tr>
            {WEEKDAYS.map((d) => (
              <th key={d} scope="col" className="pb-1 text-xs font-medium text-ink-3">
                {d}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {weeks.map((week) => (
            <tr key={week[0]}>
              {week.map((date) => {
                const entry = date >= start && date <= end ? byDate.get(date) : null;
                if (!entry) {
                  return (
                    <td key={date} className="h-14 rounded-[var(--radius-control)] align-top">
                      {date >= start && date <= end && (
                        <span className="tabular block p-1.5 text-xs text-ink-3/70">
                          {dayLabel(date)}
                        </span>
                      )}
                    </td>
                  );
                }
                const summary = daySummary(entry.doses);
                const isSelected = date === selected;
                return (
                  <td key={date} className="h-14 p-0 align-top">
                    <button
                      type="button"
                      onClick={() => onSelect(date)}
                      aria-pressed={isSelected}
                      aria-label={`${formatDate(date, "EEEE, MMM d")}: ${
                        summary.tone === "upcoming"
                          ? "later today"
                          : `${summary.taken} of ${summary.total} taken`
                      }`}
                      className={cn(
                        "flex h-full w-full flex-col justify-between rounded-[var(--radius-control)] border p-1.5 text-left transition-[background-color,border-color,transform] duration-150 active:scale-[0.97]",
                        isSelected
                          ? "border-accent bg-accent-soft"
                          : "border-line bg-surface hover:border-line-strong",
                      )}
                    >
                      <span className="tabular text-xs font-medium">{dayLabel(date)}</span>
                      <span className="flex flex-wrap gap-[3px]" aria-hidden>
                        {entry.doses.map((s) => (
                          <span key={s.time} className={cn("size-2 rounded-full", DOT[s.state])} />
                        ))}
                      </span>
                    </button>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function DayPanel({ medicationId, day, today }) {
  const setDose = useSetDose();
  if (!day) return null;
  return (
    <section className="card p-5" aria-labelledby="day-heading">
      <h2 id="day-heading" className="font-semibold">
        {day.date === today ? "Today" : formatDate(day.date, "EEEE, MMM d")}
      </h2>
      <p className="mt-0.5 text-sm text-ink-3">Mark what happened, or leave it as not logged.</p>
      <ul className="mt-4 grid grid-cols-1 gap-2">
        {day.doses.map((s) => {
          const set = (status) =>
            setDose.mutate({
              medication_id: medicationId,
              date: day.date,
              time: s.time,
              status: s.state === status ? null : status,
              fallbackState: s.state === "upcoming" ? "upcoming" : "unlogged",
            });
          return (
            <li
              key={s.time}
              className="flex flex-wrap items-center justify-between gap-3 rounded-[var(--radius-control)] bg-surface-2 px-3.5 py-2.5"
            >
              <span className="flex items-center gap-3">
                <span className="tabular w-[70px] text-sm font-semibold text-ink-2">
                  {formatClock(s.time)}
                </span>
                <span className="text-sm text-ink-2">{STATE_LABELS[s.state]}</span>
              </span>
              <span
                className="flex gap-1"
                role="group"
                aria-label={`Dose at ${formatClock(s.time)}`}
              >
                {["taken", "skipped"].map((status) => (
                  <button
                    key={status}
                    type="button"
                    aria-pressed={s.state === status}
                    onClick={() => set(status)}
                    className={cn(
                      "rounded-full border px-3 py-1 text-xs font-medium transition-[background-color,border-color,color,transform] duration-150 active:scale-[0.97]",
                      s.state === status
                        ? status === "taken"
                          ? "border-accent bg-accent text-accent-ink"
                          : "border-warn bg-warn-soft text-warn-ink"
                        : "border-line bg-surface text-ink-2 hover:border-line-strong",
                    )}
                  >
                    {STATE_LABELS[status]}
                  </button>
                ))}
              </span>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

function HistorySkeleton() {
  return (
    <LoadingRegion label="Loading dose history">
      <Skeleton className="mb-3 h-4 w-32" />
      <Skeleton className="mb-8 h-9 w-72" />
      <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
        {[0, 1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-24 rounded-card" />
        ))}
      </div>
      <Skeleton className="h-80 rounded-card" />
    </LoadingRegion>
  );
}

export default function MedicationHistory() {
  const { readOnly } = useActing();
  const { id } = useParams();
  const [range, setRange] = useState(28);
  const [picked, setPicked] = useState(null);
  const reduce = useReducedMotion();
  const { data, isPending, isError, error, refetch } = useMedicationAdherence(id, range);

  if (isPending) return <HistorySkeleton />;
  if (isError) {
    const missing = error?.status === 404 || error?.status === 422;
    return (
      <>
        <BackLink />
        <EmptyState
          icon={Pill}
          title={missing ? "We couldn't find that medicine" : "Dose history didn't load"}
          description={
            missing
              ? "It may have been removed when its prescription was reprocessed."
              : "A quick retry usually fixes it."
          }
          action={
            missing ? (
              <Button as={Link} to="/app/medications">
                See all medications
              </Button>
            ) : (
              <Button onClick={() => refetch()}>Try again</Button>
            )
          }
        />
      </>
    );
  }

  const med = data.medications[0];
  if (!med) {
    return (
      <>
        <BackLink />
        <EmptyState
          icon={Pill}
          title="Nothing to track"
          description="This medicine is taken as needed or hasn't started yet, so it has no scheduled doses."
        />
      </>
    );
  }

  const days = med.days;
  const selectedDate =
    picked && days.some((d) => d.date === picked) ? picked : (days.at(-1)?.date ?? null);
  const selectedDay = days.find((d) => d.date === selectedDate);
  const c = med.counts;

  return (
    <>
      <BackLink />
      <PageHeader
        title={`${med.name}${med.strength ? ` ${med.strength}` : ""}`}
        description={[med.schedule_label, med.status === "active" ? null : med.status]
          .filter(Boolean)
          .join(" · ")}
        actions={
          <SegmentedTabs label="History range" items={RANGES} value={range} onChange={setRange} />
        }
      />

      <motion.div
        initial={reduce ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
        className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4"
      >
        <Stat
          label="Marked taken"
          value={percent(med.taken_rate) ?? "-"}
          hint={`${c.taken} of ${c.due} doses due`}
        />
        <Stat label="Skipped" value={c.skipped} />
        <Stat label="Not logged" value={c.unlogged} />
        <Stat
          label="Days in a row"
          value={med.streak_days}
          hint={med.streak_days >= 7 ? STREAK_LINE : "Every due dose taken"}
        />
      </motion.div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)] lg:items-start">
        <section className="card p-4 sm:p-5" aria-labelledby="calendar-heading">
          <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
            <h2 id="calendar-heading" className="font-semibold">
              {formatDate(days[0]?.date ?? data.start, "MMM d")} to {formatDate(data.end, "MMM d")}
            </h2>
            <ul className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-ink-3">
              {["taken", "skipped", "unlogged"].map((s) => (
                <li key={s} className="flex items-center gap-1.5">
                  <span className={cn("size-2 rounded-full", DOT[s])} aria-hidden />
                  {STATE_LABELS[s]}
                </li>
              ))}
            </ul>
          </div>
          <Calendar
            start={days[0]?.date ?? data.start}
            end={data.end}
            days={days}
            selected={selectedDate}
            onSelect={setPicked}
          />
        </section>
        {!readOnly && (
          <DayPanel medicationId={med.medication_id} day={selectedDay} today={data.end} />
        )}
      </div>

      <p className="mt-6 flex items-start gap-2 text-sm text-ink-2">
        <Info size={16} className="mt-0.5 shrink-0 text-ink-3" />
        Doses you didn't mark stay "not logged". MedSpace never assumes a dose was missed, and this
        history isn't a substitute for advice from your prescriber or pharmacist.
      </p>
    </>
  );
}
