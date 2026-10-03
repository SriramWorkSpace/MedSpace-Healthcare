import { Link, useParams } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { toast } from "sonner";
import { ArrowLeft, Flask, Trash } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { useDeleteLabResult, useLabTrend } from "@/features/labs/api";
import { FlagChip } from "@/features/labs/FlagChip";
import { RangeNote } from "@/features/labs/RangeNote";
import { TrendChart } from "@/features/labs/TrendChart";
import { describeChange, resultLabel } from "@/features/labs/format";
import { formatDate } from "@/lib/format";
import { useActing } from "@/features/circle/api";

function sourceHref(r) {
  return `/app/documents/${r.document_id}${r.source_page ? `?page=${r.source_page}` : ""}`;
}

function DetailSkeleton() {
  return (
    <LoadingRegion label="Loading results">
      <Skeleton className="mb-3 h-4 w-28" />
      <Skeleton className="mb-8 h-9 w-64" />
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,2.2fr)]">
        <Skeleton className="h-64 rounded-card" />
        <Skeleton className="h-64 rounded-card" />
      </div>
      <Skeleton className="mt-6 h-48 rounded-card" />
    </LoadingRegion>
  );
}

function BackLink() {
  return (
    <Link
      to="/app/labs"
      className="tap mb-4 inline-flex items-center gap-1.5 rounded-lg text-sm text-ink-2 hover:text-accent"
    >
      <ArrowLeft size={14} weight="bold" />
      All lab results
    </Link>
  );
}

export default function LabDetail() {
  const { isActing } = useActing();
  const { key } = useParams();
  const { data, isPending, isError, error, refetch } = useLabTrend(key);
  const remove = useDeleteLabResult();
  const reduce = useReducedMotion();

  if (isPending) return <DetailSkeleton />;
  if (isError) {
    const missing = error?.status === 404 || error?.status === 422;
    return (
      <>
        <BackLink />
        <EmptyState
          icon={Flask}
          title={missing ? "No results for this test" : "Results didn't load"}
          description={
            missing
              ? "It may have been removed, or the report it came from was deleted."
              : "A quick retry usually fixes it."
          }
          action={
            missing ? (
              <Button as={Link} to="/app/labs">
                See all lab results
              </Button>
            ) : (
              <Button onClick={() => refetch()}>Try again</Button>
            )
          }
        />
      </>
    );
  }

  const { latest } = data;
  const change = describeChange(latest, data.previous);
  const onRemove = (r) =>
    remove.mutate(r.id, {
      onSuccess: () =>
        toast("Result removed", {
          description: "Reprocess its report if you ever want it back.",
        }),
      onError: (e) => toast.error(e.message),
    });

  return (
    <>
      <BackLink />
      <PageHeader
        title={data.name}
        description={`${data.count} result${data.count === 1 ? "" : "s"} from your lab reports.`}
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,2.2fr)]">
        <motion.section
          initial={reduce ? false : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: [0.23, 1, 0.32, 1] }}
          className="card flex flex-col gap-5 p-6"
          aria-labelledby="latest-heading"
        >
          <div className="flex items-start justify-between gap-3">
            <h2 id="latest-heading" className="text-sm font-medium text-ink-2">
              Latest result
            </h2>
            <FlagChip flag={latest.flag} />
          </div>
          <p className="tabular text-5xl font-semibold leading-none tracking-tight">
            {latest.value_text}
            {latest.unit && (
              <span className="ml-2 text-lg font-normal tracking-normal text-ink-3">
                {latest.unit}
              </span>
            )}
          </p>
          <dl className="grid grid-cols-1 gap-3 text-sm">
            <div>
              <dt className="text-ink-3">Collected</dt>
              <dd>{formatDate(latest.collected_on)}</dd>
            </div>
            <div>
              <dt className="text-ink-3">Range printed on the report</dt>
              <dd className="tabular">{latest.ref_range ?? "None printed"}</dd>
            </div>
            {change && (
              <div>
                <dt className="text-ink-3">Change</dt>
                <dd>{change}</dd>
              </div>
            )}
          </dl>
          <Link to={sourceHref(latest)} className="mt-auto text-sm text-accent hover:underline">
            Open {latest.document_title}
            {latest.source_page ? `, page ${latest.source_page}` : ""}
          </Link>
        </motion.section>

        <motion.section
          initial={reduce ? false : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.05, ease: [0.23, 1, 0.32, 1] }}
          className="card p-5 sm:p-6"
          aria-labelledby="trend-heading"
        >
          <h2 id="trend-heading" className="mb-4 text-sm font-medium text-ink-2">
            Over time{data.unit ? `, in ${data.unit}` : ""}
          </h2>
          {data.points.length > 0 ? (
            <TrendChart
              points={data.points}
              refLow={latest.ref_low}
              refHigh={latest.ref_high}
              unit={data.unit}
              label={data.name}
            />
          ) : (
            <p className="py-16 text-center text-sm text-ink-2">
              These results are not numbers, so there is nothing to chart.
            </p>
          )}
          {data.uncharted > 0 && data.points.length > 0 && (
            <p className="mt-3 text-xs text-ink-3">
              {data.uncharted} result{data.uncharted === 1 ? " is" : "s are"} in another unit or not
              a number, so {data.uncharted === 1 ? "it is" : "they are"} listed below but not
              charted.
            </p>
          )}
        </motion.section>
      </div>

      <section className="card mt-6 p-5 sm:p-6" aria-labelledby="history-heading">
        <h2 id="history-heading" className="mb-3 text-sm font-medium text-ink-2">
          Every result
        </h2>
        <div
          className="relative overflow-x-auto"
          tabIndex={0}
          role="region"
          aria-label="Results table"
        >
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs text-ink-3">
                <th className="py-2 pr-4 font-medium">Collected</th>
                <th className="py-2 pr-4 font-medium">Result</th>
                <th className="py-2 pr-4 font-medium">Printed range</th>
                <th className="py-2 pr-4 font-medium">Compared with range</th>
                <th className="py-2 pr-4 font-medium">Source</th>
                <th className="py-2 font-medium">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {data.results.map((r) => (
                <tr key={r.id} className="align-middle">
                  <td className="py-3 pr-4 whitespace-nowrap">{formatDate(r.collected_on)}</td>
                  <td className="tabular py-3 pr-4 font-semibold whitespace-nowrap">
                    {resultLabel(r)}
                  </td>
                  <td className="tabular py-3 pr-4 text-ink-2">{r.ref_range ?? "None"}</td>
                  <td className="py-3 pr-4">
                    {r.flag ? <FlagChip flag={r.flag} /> : <span className="text-ink-3">-</span>}
                  </td>
                  <td className="py-3 pr-4">
                    <Link
                      to={sourceHref(r)}
                      className="text-ink-2 hover:text-accent hover:underline"
                    >
                      {r.document_title}
                      {r.source_page ? `, p.${r.source_page}` : ""}
                    </Link>
                  </td>
                  <td className="py-3 text-right">
                    {!isActing && (
                      <Button
                        variant="ghost"
                        size="sm"
                        icon
                        aria-label={`Remove the ${formatDate(r.collected_on)} result`}
                        onClick={() => onRemove(r)}
                      >
                        <Trash size={15} />
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <RangeNote className="mt-6" />
    </>
  );
}
