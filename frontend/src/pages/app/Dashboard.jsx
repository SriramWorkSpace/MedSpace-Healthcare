import { Link } from "react-router";
import { format, parseISO } from "date-fns";
import { motion, useReducedMotion } from "motion/react";
import {
  ForkKnife,
  CheckSquare,
  FileText,
  Pill,
  UploadSimple,
  WarningCircle,
  CalendarBlank,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { useAuth } from "@/lib/auth";
import { firstName, greeting } from "@/lib/format";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useDashboard, useDietNotes } from "@/features/records/api";
import { TodaySchedule } from "@/features/dashboard/TodaySchedule";
import { RunningLow } from "@/features/supply/RunningLow";
import { useActing } from "@/features/circle/api";
import {
  AsNeededList,
  ComingUp,
  NeedsReview,
  Panel,
  StatTile,
  WeekStrip,
} from "@/features/dashboard/Widgets";

function DashboardSkeleton() {
  return (
    <LoadingRegion label="Loading your day">
      <Skeleton className="h-9 w-72" />
      <Skeleton className="mt-3 h-4 w-48" />
      <div className="mt-8 grid grid-cols-1 gap-4 lg:grid-cols-[1.55fr_1fr]">
        <div className="card card--flat p-6">
          <Skeleton className="h-4 w-32" />
          <div className="mt-5 grid grid-cols-1 gap-2">
            {Array.from({ length: 5 }, (_, i) => (
              <Skeleton key={i} className="h-14 w-full" />
            ))}
          </div>
        </div>
        <div className="grid grid-cols-1 content-start gap-4">
          <div className="grid grid-cols-2 gap-3">
            {Array.from({ length: 4 }, (_, i) => (
              <Skeleton key={i} className="h-[76px] rounded-card" />
            ))}
          </div>
          <Skeleton className="h-56 rounded-card" />
        </div>
      </div>
    </LoadingRegion>
  );
}

export default function Dashboard() {
  const { acting, isActing, readOnly } = useActing();
  const { user } = useAuth();
  const { data, isPending, isError, refetch } = useDashboard();
  const diet = useDietNotes();
  const reduce = useReducedMotion();

  if (isPending) return <DashboardSkeleton />;
  if (isError) {
    return (
      <EmptyState
        icon={WarningCircle}
        title="Your dashboard didn't load"
        description="A quick refresh usually fixes it."
        action={<Button onClick={() => refetch()}>Try again</Button>}
      />
    );
  }

  const isNew = data.stats.documents === 0;
  const stagger = (i) => ({
    initial: reduce ? false : { opacity: 0, y: 12 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.45, delay: 0.05 * i, ease: [0.23, 1, 0.32, 1] },
  });

  return (
    <>
      <motion.div {...stagger(0)} className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-[34px]">
          {isActing
            ? `${firstName(acting.name)}'s day`
            : `${greeting()}, ${firstName(user.display_name)}.`}
        </h1>
        <p className="mt-2 text-ink-2">{format(parseISO(data.today), "EEEE, MMMM d")}</p>
      </motion.div>

      {isNew ? (
        <EmptyState
          icon={FileText}
          title="Start with your first prescription"
          description="Upload a PDF or a photo. We'll pull out the medicines and schedule so you can review them."
          action={
            <Button as={Link} to="/app/documents?upload=1">
              <UploadSimple size={15} weight="bold" /> Upload a document
            </Button>
          }
          quip={EMPTY_QUIPS.documents}
        />
      ) : (
        <div className="grid grid-cols-[minmax(0,1fr)] gap-4 lg:grid-cols-[minmax(0,1.55fr)_minmax(0,1fr)] lg:items-start">
          <motion.div {...stagger(1)} className="grid grid-cols-1 min-w-0 gap-4">
            {!isActing && <NeedsReview items={data.needs_review} processing={data.processing} />}
            <RunningLow items={data.running_low} readOnly={readOnly} />
            <Panel
              title="Today's doses"
              action={
                <Link
                  to="/app/medications"
                  className="tap text-sm font-medium text-accent hover:underline"
                >
                  All medications
                </Link>
              }
            >
              {data.doses_today.length ? (
                <TodaySchedule doses={data.doses_today} dateKey={data.today} readOnly={readOnly} />
              ) : (
                <p className="text-sm text-ink-2">{EMPTY_QUIPS.medications}</p>
              )}
              {data.as_needed.length > 0 && (
                <div className="mt-6 border-t border-line pt-5">
                  <p className="mb-2.5 text-xs font-medium text-ink-3">Only if needed</p>
                  <AsNeededList items={data.as_needed} />
                </div>
              )}
            </Panel>
          </motion.div>

          <div className="grid grid-cols-1 min-w-0 gap-4">
            <motion.div {...stagger(2)} className="grid grid-cols-2 gap-3">
              <StatTile
                label="Active medications"
                value={data.stats.active_medications}
                to="/app/medications"
                icon={Pill}
              />
              <StatTile
                label="Open to-dos"
                value={data.stats.open_tasks}
                to="/app/timeline"
                icon={CheckSquare}
              />
              <StatTile
                label="Prescriptions"
                value={data.stats.prescriptions}
                to="/app/timeline"
                icon={CalendarBlank}
              />
              <StatTile
                label="Documents"
                value={data.stats.documents}
                to="/app/documents"
                icon={FileText}
              />
            </motion.div>
            <motion.div {...stagger(3)}>
              <Panel title="Coming up">
                <ComingUp items={data.upcoming} />
              </Panel>
            </motion.div>
            <motion.div {...stagger(4)}>
              <Panel title="This week">
                <WeekStrip week={data.week} />
              </Panel>
            </motion.div>
            {diet.data?.notes?.length > 0 && (
              <motion.div {...stagger(5)}>
                <Panel
                  title="From your care team"
                  action={
                    <Link
                      to="/app/diet"
                      className="tap text-sm font-medium text-accent hover:underline"
                    >
                      All diet notes
                    </Link>
                  }
                >
                  <ul className="grid grid-cols-1 gap-2.5">
                    {diet.data.notes.slice(0, 3).map((n) => (
                      <li key={n.id} className="flex items-start gap-2.5 text-sm">
                        <ForkKnife size={15} className="mt-0.5 shrink-0 text-accent" />
                        <span className="text-ink-2">{n.text}</span>
                      </li>
                    ))}
                  </ul>
                </Panel>
              </motion.div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
