import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { toast } from "sonner";
import { ArrowRight, CalendarPlus, ClipboardText, Plus, Stethoscope } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Dialog } from "@/components/ui/Dialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { Field, Input } from "@/components/ui/Field";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useDashboard } from "@/features/records/api";
import { useCreateVisit, useVisits } from "@/features/visits/api";
import { clinicianFrom } from "@/features/visits/clinician";
import { formatDate, formatRelativeDay } from "@/lib/format";
import { useActing } from "@/features/circle/api";

function NewVisitDialog({ open, onClose, initial }) {
  const navigate = useNavigate();
  const create = useCreateVisit();
  const [title, setTitle] = useState(initial?.title ?? "");
  const [date, setDate] = useState(initial?.date ?? "");
  const [clinician, setClinician] = useState(initial?.clinician ?? "");

  const submit = (e) => {
    e.preventDefault();
    create.mutate(
      { title: title || null, visit_date: date || null, clinician: clinician || null },
      {
        onSuccess: (v) => navigate(`/app/visits/${v.id}`),
        onError: (err) => toast.error(err.message),
      },
    );
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      title="Prepare for a visit"
      description="Add your questions next. The brief fills itself in from your records."
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="new-visit" loading={create.isPending}>
            Create
          </Button>
        </>
      }
    >
      <form id="new-visit" onSubmit={submit} className="grid grid-cols-1 gap-4">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Visit date" optional>
            <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </Field>
          <Field label="With" optional>
            <Input
              value={clinician}
              onChange={(e) => setClinician(e.target.value)}
              placeholder="Dr. Imani Oduya"
            />
          </Field>
        </div>
        <Field label="Title" optional hint="Defaults to the clinician's name.">
          <Input value={title} onChange={(e) => setTitle(e.target.value)} maxLength={120} />
        </Field>
      </form>
    </Dialog>
  );
}

/**
 * `?prepare=YYYY-MM-DD&clinician=…` (from the dashboard): open that visit's prep, creating it the
 * first time.
 */
function usePrepareFromLink(visits) {
  const [params, setParams] = useSearchParams();
  const navigate = useNavigate();
  const create = useCreateVisit();
  const handled = useRef(false);
  const date = params.get("prepare");
  const clinician = params.get("clinician");

  useEffect(() => {
    if (!date || !visits || handled.current) return;
    handled.current = true;
    const existing = visits.find((v) => v.visit_date === date);
    if (existing) {
      navigate(`/app/visits/${existing.id}`, { replace: true });
      return;
    }
    create.mutate(
      { visit_date: date, clinician: clinician || null },
      {
        onSuccess: (v) => navigate(`/app/visits/${v.id}`, { replace: true }),
        onError: (e) => {
          toast.error(e.message);
          setParams({}, { replace: true });
        },
      },
    );
  }, [date, clinician, visits, create, navigate, setParams]);

  return Boolean(date);
}

function VisitCard({ visit, index }) {
  const reduce = useReducedMotion();
  const open = visit.questions.filter((q) => !q.done).length;
  return (
    <motion.li
      initial={reduce ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: Math.min(index, 6) * 0.04, ease: [0.23, 1, 0.32, 1] }}
    >
      <Link
        to={`/app/visits/${visit.id}`}
        className="card card--interactive flex items-center gap-4 p-4 sm:p-5"
      >
        <span className="grid size-11 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
          <ClipboardText size={20} weight="duotone" />
        </span>
        <span className="min-w-0 flex-1">
          <span className="block truncate font-semibold">{visit.title}</span>
          <span className="block truncate text-sm text-ink-3">
            {[
              visit.visit_date ? formatDate(visit.visit_date, "EEE, MMM d") : "No date yet",
              `${open} open question${open === 1 ? "" : "s"}`,
            ].join(" · ")}
          </span>
        </span>
        {visit.visit_date && (
          <span className="tabular hidden shrink-0 text-sm font-medium text-ink-2 sm:block">
            {formatRelativeDay(visit.visit_date)}
          </span>
        )}
        <ArrowRight size={16} className="shrink-0 text-ink-3" />
      </Link>
    </motion.li>
  );
}

function VisitsSkeleton() {
  return (
    <LoadingRegion label="Loading visits" className="grid grid-cols-1 gap-3">
      {[0, 1, 2].map((i) => (
        <div key={i} className="card card--flat flex items-center gap-4 p-5">
          <Skeleton className="size-11 rounded-xl" />
          <div className="grid flex-1 grid-cols-1 gap-2">
            <Skeleton className="h-4 w-48" />
            <Skeleton className="h-3 w-32" />
          </div>
        </div>
      ))}
    </LoadingRegion>
  );
}

export default function Visits() {
  const { isActing } = useActing();
  const { data, isPending, isError, refetch } = useVisits();
  const dashboard = useDashboard();
  const [dialog, setDialog] = useState(null); // null | { title?, date?, clinician? }
  const preparing = usePrepareFromLink(data);

  const today = dashboard.data?.today ?? new Date().toISOString().slice(0, 10);
  const preparedDates = new Set((data ?? []).map((v) => v.visit_date).filter(Boolean));
  const suggestions = (dashboard.data?.upcoming ?? []).filter(
    (e) => e.type === "appointment" && !preparedDates.has(e.date),
  );
  const upcoming = (data ?? []).filter((v) => !v.visit_date || v.visit_date >= today);
  const past = (data ?? []).filter((v) => v.visit_date && v.visit_date < today).reverse();

  return (
    <>
      <PageHeader
        title="Visits"
        description="Get ready for appointments: your questions, plus a one-page brief of what changed since last time."
        actions={
          isActing ? undefined : (
            <Button onClick={() => setDialog({})}>
              <Plus size={15} weight="bold" /> New visit prep
            </Button>
          )
        }
      />

      {suggestions.length > 0 && (
        <section className="mb-8" aria-labelledby="suggest-heading">
          <h2 id="suggest-heading" className="mb-3 text-sm font-medium text-ink-2">
            Coming up
          </h2>
          <ul className="grid grid-cols-1 gap-3 md:grid-cols-2">
            {suggestions.map((e) => (
              <li key={e.id} className="card card--flat flex items-center gap-3 border-dashed p-4">
                <span className="grid size-10 shrink-0 place-items-center rounded-xl bg-surface-2 text-ink-2">
                  <Stethoscope size={18} weight="duotone" />
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-medium">{e.title}</span>
                  <span className="block truncate text-xs text-ink-3">
                    {formatRelativeDay(e.date)}
                    {e.subtitle ? ` · ${e.subtitle}` : ""}
                  </span>
                </span>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() =>
                    setDialog({ date: e.date, clinician: clinicianFrom(e.title) ?? "" })
                  }
                >
                  <CalendarPlus size={14} /> Prepare
                </Button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {isPending || preparing ? (
        <VisitsSkeleton />
      ) : isError ? (
        <EmptyState
          icon={ClipboardText}
          title="Visits didn't load"
          description="A quick retry usually fixes it."
          action={<Button onClick={() => refetch()}>Try again</Button>}
        />
      ) : data.length === 0 ? (
        <EmptyState
          icon={ClipboardText}
          title="No visit preps yet"
          description="Before an appointment, collect your questions and get a brief of your medicines, doses, lab results and open to-dos to bring along."
          action={<Button onClick={() => setDialog({})}>Prepare for a visit</Button>}
          quip={EMPTY_QUIPS.visits}
        />
      ) : (
        <div className="grid grid-cols-1 gap-8">
          {upcoming.length > 0 && (
            <section aria-labelledby="upcoming-heading">
              <h2 id="upcoming-heading" className="mb-3 text-sm font-medium text-ink-2">
                Upcoming
              </h2>
              <ul className="grid grid-cols-1 gap-3">
                {upcoming.map((v, i) => (
                  <VisitCard key={v.id} visit={v} index={i} />
                ))}
              </ul>
            </section>
          )}
          {past.length > 0 && (
            <section aria-labelledby="past-heading">
              <h2 id="past-heading" className="mb-3 text-sm font-medium text-ink-2">
                Past
              </h2>
              <ul className="grid grid-cols-1 gap-3">
                {past.map((v, i) => (
                  <VisitCard key={v.id} visit={v} index={i} />
                ))}
              </ul>
            </section>
          )}
        </div>
      )}

      {dialog && (
        <NewVisitDialog
          key={`${dialog.date ?? ""}-${dialog.clinician ?? ""}`}
          open
          initial={dialog}
          onClose={() => setDialog(null)}
        />
      )}
    </>
  );
}
