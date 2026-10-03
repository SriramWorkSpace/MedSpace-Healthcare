import { useMemo, useState } from "react";
import { Link } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { format, parseISO } from "date-fns";
import {
  CheckCircle,
  CheckSquare,
  ClockCounterClockwise,
  Flag,
  Flask,
  Pill,
  Prescription,
  Stethoscope,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useTimeline } from "@/features/records/api";
import { cn } from "@/lib/cn";

const TYPES = {
  prescription: { label: "Prescriptions", icon: Prescription },
  appointment: { label: "Appointments", icon: Stethoscope },
  medication_start: { label: "Started", icon: Pill },
  medication_end: { label: "Course ends", icon: Flag },
  task: { label: "To-dos", icon: CheckSquare },
  document: { label: "Reports", icon: Flask },
};

function linkFor(e) {
  if (e.prescription_id) return `/app/prescriptions/${e.prescription_id}`;
  if (e.document_id) return `/app/documents/${e.document_id}`;
  return null;
}

function EventRow({ e }) {
  const reduce = useReducedMotion();
  const meta = TYPES[e.type] ?? TYPES.document;
  const Icon = e.type === "task" && e.completed ? CheckCircle : meta.icon;
  const to = linkFor(e);
  const content = (
    <>
      <span
        className={cn(
          "absolute -left-[33px] top-3 grid size-[26px] place-items-center rounded-full border-[3px] border-bg",
          e.upcoming ? "bg-accent text-accent-ink" : "bg-surface-3 text-ink-2",
        )}
      >
        <Icon size={12} weight="bold" />
      </span>
      <div className="flex items-baseline justify-between gap-3">
        <p className={cn("font-medium", e.completed && "text-ink-3 line-through")}>{e.title}</p>
        <time dateTime={e.date} className="tabular shrink-0 text-xs text-ink-3">
          {format(parseISO(e.date), "MMM d")}
        </time>
      </div>
      {e.subtitle && <p className="mt-0.5 truncate text-sm text-ink-2">{e.subtitle}</p>}
    </>
  );
  return (
    <motion.li
      initial={reduce ? false : { opacity: 0, x: -6 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ duration: 0.35, ease: [0.23, 1, 0.32, 1] }}
      className="relative"
    >
      {to ? (
        <Link
          to={to}
          className="block rounded-[var(--radius-control)] px-3 py-2.5 transition-colors hover:bg-surface"
        >
          {content}
        </Link>
      ) : (
        <div className="px-3 py-2.5">{content}</div>
      )}
    </motion.li>
  );
}

function Group({ title, events, accent }) {
  return (
    <section className="relative">
      <h2
        className={cn(
          "sticky top-[var(--nav-h)] z-[1] -mx-1 mb-2 bg-[color-mix(in_oklch,var(--bg),transparent_8%)] px-1 py-2 text-sm font-semibold backdrop-blur",
          accent ? "text-accent" : "text-ink-2",
        )}
      >
        {title}
      </h2>
      <ol className="relative ml-[13px] grid grid-cols-1 gap-0.5 border-l border-line-strong pl-5">
        {events.map((e) => (
          <EventRow key={e.id} e={e} />
        ))}
      </ol>
    </section>
  );
}

export default function Timeline() {
  const [active, setActive] = useState(() => new Set());
  const types = active.size ? [...active] : undefined;
  const { data, isPending, fetchNextPage, hasNextPage, isFetchingNextPage } = useTimeline(types);

  const { upcoming, months } = useMemo(() => {
    const items = data?.pages.flatMap((p) => p.items) ?? [];
    const up = items.filter((e) => e.upcoming).sort((a, b) => a.date.localeCompare(b.date));
    const past = items.filter((e) => !e.upcoming);
    const byMonth = new Map();
    for (const e of past) {
      const key = e.date.slice(0, 7);
      if (!byMonth.has(key)) byMonth.set(key, []);
      byMonth.get(key).push(e);
    }
    return { upcoming: up, months: [...byMonth.entries()] };
  }, [data]);

  const toggle = (t) =>
    setActive((prev) => {
      const next = new Set(prev);
      next.has(t) ? next.delete(t) : next.add(t);
      return next;
    });

  const empty = !isPending && !upcoming.length && !months.length;

  return (
    <>
      <PageHeader
        title="Timeline"
        description="Prescriptions, medications, appointments and reports, in the order they happened."
      />
      {/* Filters only make sense once there is something to filter. */}
      {!(empty && active.size === 0) && (
        <div className="mb-8 flex flex-wrap gap-2" role="group" aria-label="Filter events">
          {Object.entries(TYPES).map(([key, { label, icon: Icon }]) => {
            const on = active.has(key);
            return (
              <button
                key={key}
                type="button"
                aria-pressed={on}
                onClick={() => toggle(key)}
                className={cn(
                  "inline-flex h-8 items-center gap-1.5 rounded-full border px-3 text-[13px] font-medium transition-colors duration-150 active:scale-[0.97]",
                  on
                    ? "border-transparent bg-accent text-accent-ink"
                    : "border-line bg-surface text-ink-2 hover:border-line-strong hover:text-ink",
                )}
              >
                <Icon size={14} weight={on ? "bold" : "regular"} />
                {label}
              </button>
            );
          })}
          {active.size > 0 && (
            <Button variant="ghost" size="sm" onClick={() => setActive(new Set())}>
              Clear
            </Button>
          )}
        </div>
      )}

      {isPending ? (
        <LoadingRegion label="Loading timeline" className="grid grid-cols-1 max-w-4xl gap-8">
          {[0, 1].map((g) => (
            <div key={g}>
              <Skeleton className="mb-4 h-4 w-28" />
              <div className="ml-4 grid grid-cols-1 gap-5 border-l border-line pl-6">
                {Array.from({ length: 4 }, (_, i) => (
                  <div key={i} className="grid grid-cols-1 gap-2">
                    <Skeleton className="h-4 w-3/5" />
                    <Skeleton className="h-3 w-2/5" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </LoadingRegion>
      ) : empty ? (
        <EmptyState
          icon={ClockCounterClockwise}
          title={active.size ? "No matching events" : "Your timeline is empty"}
          description={
            active.size
              ? "Nothing in your records matches these filters."
              : "Confirmed records appear here automatically."
          }
          action={
            active.size ? (
              <Button variant="secondary" onClick={() => setActive(new Set())}>
                Clear filters
              </Button>
            ) : undefined
          }
          quip={active.size ? undefined : EMPTY_QUIPS.timeline}
        />
      ) : (
        <div className="grid grid-cols-1 max-w-4xl gap-10">
          {upcoming.length > 0 && <Group title="Upcoming" events={upcoming} accent />}
          {months.map(([key, events]) => (
            <Group key={key} title={format(parseISO(`${key}-01`), "MMMM yyyy")} events={events} />
          ))}
          {hasNextPage && (
            <Button
              variant="secondary"
              className="w-fit"
              loading={isFetchingNextPage}
              onClick={() => fetchNextPage()}
            >
              Load earlier events
            </Button>
          )}
        </div>
      )}
    </>
  );
}
