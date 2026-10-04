import { Link } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { Flask } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useLabTrends } from "@/features/labs/api";
import { FlagChip } from "@/features/labs/FlagChip";
import { RangeNote } from "@/features/labs/RangeNote";
import { Sparkline } from "@/features/labs/Sparkline";
import { describeChange } from "@/features/labs/format";
import { formatDate } from "@/lib/format";
import { sourceLink } from "@/features/documents/links";

function TrendCard({ trend, index }) {
  const reduce = useReducedMotion();
  const { latest } = trend;
  const change = describeChange(latest, trend.previous);
  return (
    <motion.li
      initial={reduce ? false : { opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: Math.min(index, 8) * 0.04, ease: [0.23, 1, 0.32, 1] }}
    >
      <Link
        to={`/app/labs/${trend.key}`}
        className="card card--interactive flex h-full flex-col gap-4 p-5"
      >
        <div className="flex items-start justify-between gap-3">
          <h3 className="min-w-0 truncate font-semibold">{trend.name}</h3>
          <FlagChip flag={latest.flag} />
        </div>
        <div className="flex items-end justify-between gap-3">
          <p className="tabular text-[28px] font-semibold leading-none tracking-tight">
            {latest.value_text}
            {latest.unit && (
              <span className="ml-1.5 text-sm font-normal tracking-normal text-ink-3">
                {latest.unit}
              </span>
            )}
          </p>
          <Sparkline points={trend.points} refLow={latest.ref_low} refHigh={latest.ref_high} />
        </div>
        <div className="mt-auto grid grid-cols-1 gap-0.5 text-xs text-ink-3">
          {change && <p className="text-ink-2">{change}</p>}
          <p>
            {latest.ref_range ? `Printed range ${latest.ref_range}` : "No range printed"}
            {" · "}
            {trend.count} result{trend.count === 1 ? "" : "s"}
          </p>
        </div>
      </Link>
    </motion.li>
  );
}

function LabsSkeleton() {
  return (
    <LoadingRegion label="Loading lab results">
      <Skeleton className="mb-4 h-5 w-64" />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        {Array.from({ length: 6 }, (_, i) => (
          <div key={i} className="card card--flat grid grid-cols-1 gap-4 p-5">
            <Skeleton className="h-5 w-36" />
            <div className="flex items-end justify-between">
              <Skeleton className="h-8 w-24" />
              <Skeleton className="h-10 w-28" />
            </div>
            <Skeleton className="h-3 w-40" />
          </div>
        ))}
      </div>
    </LoadingRegion>
  );
}

/** Group tests under the report their newest result came from, keeping API order. */
function byReport(trends) {
  const groups = new Map();
  trends.forEach((t, index) => {
    const id = t.latest.document_id;
    if (!groups.has(id)) groups.set(id, { id, latest: t.latest, trends: [] });
    groups.get(id).trends.push({ trend: t, index });
  });
  return [...groups.values()];
}

export default function Labs() {
  const { data, isPending, isError, refetch } = useLabTrends();
  return (
    <>
      <PageHeader
        title="Lab results"
        description="Test results from your confirmed lab reports, charted over time."
      />
      {isPending ? (
        <LabsSkeleton />
      ) : isError ? (
        <EmptyState
          icon={Flask}
          title="Lab results didn't load"
          description="A quick retry usually fixes it."
          action={<Button onClick={() => refetch()}>Try again</Button>}
        />
      ) : data.length === 0 ? (
        <EmptyState
          icon={Flask}
          title="No lab results yet"
          description="Upload a lab report and confirm it. Each test shows up here with its value, unit and the range printed on the report."
          action={
            <Button as={Link} to="/app/documents?upload=1">
              Upload a lab report
            </Button>
          }
          quip={EMPTY_QUIPS.labs}
        />
      ) : (
        <div className="grid grid-cols-1 gap-10">
          <RangeNote className="-mt-4" />
          {byReport(data).map((group) => (
            <section key={group.id} aria-labelledby={`report-${group.id}`}>
              <div className="mb-3 flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
                <h2 id={`report-${group.id}`} className="text-lg font-semibold">
                  {group.latest.document_title}
                </h2>
                <Link
                  to={sourceLink({ ...group.latest, document_id: group.id })}
                  className="tap text-sm text-ink-3 hover:text-accent hover:underline"
                >
                  Collected {formatDate(group.latest.collected_on)}. View report
                </Link>
              </div>
              <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
                {group.trends.map(({ trend, index }) => (
                  <TrendCard key={trend.key} trend={trend} index={index} />
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}
    </>
  );
}
