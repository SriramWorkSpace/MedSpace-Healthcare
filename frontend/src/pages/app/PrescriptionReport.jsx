import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import {
  ArrowLeft,
  ArrowSquareOut,
  CalendarPlus,
  Printer,
  ShareNetwork,
  FileX,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton, SkeletonText } from "@/components/ui/Skeleton";
import { usePrescription } from "@/features/records/api";
import { ReportBody } from "@/features/records/ReportBody";
import { SyncDialog } from "@/features/integrations/SyncDialog";

export default function PrescriptionReport() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: rx, isPending, isError } = usePrescription(id);
  const [syncOpen, setSyncOpen] = useState(false);

  if (isPending) {
    return (
      <LoadingRegion label="Loading report" className="mx-auto max-w-4xl">
        <Skeleton className="h-4 w-24" />
        <div className="card card--flat mt-6 p-8">
          <Skeleton className="h-7 w-64" />
          <SkeletonText lines={6} className="mt-8" />
        </div>
      </LoadingRegion>
    );
  }
  if (isError) {
    return (
      <EmptyState
        icon={FileX}
        title="Report not found"
        description="It may have been removed when its document was deleted."
        action={
          <Button as={Link} to="/app/documents">
            Back to documents
          </Button>
        }
      />
    );
  }

  // React Router records the in-app history index; 0 means this tab started on this page.
  const canGoBack = (window.history.state?.idx ?? 0) > 0;

  return (
    <div className="mx-auto max-w-4xl">
      <div className="no-print mb-6 flex flex-wrap items-center justify-between gap-3">
        {/* Reports open from the dashboard, search, medications and the timeline: go back to
            wherever the user came from, or to the timeline on a fresh visit. */}
        {canGoBack ? (
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="inline-flex items-center gap-1.5 rounded-lg text-sm text-ink-2 hover:text-ink"
          >
            <ArrowLeft size={14} weight="bold" /> Back
          </button>
        ) : (
          <Link
            to="/app/timeline"
            className="inline-flex items-center gap-1.5 rounded-lg text-sm text-ink-2 hover:text-ink"
          >
            <ArrowLeft size={14} weight="bold" /> Timeline
          </Link>
        )}
        <div className="flex flex-wrap gap-1.5">
          <Button as={Link} to={`/app/documents/${rx.document_id}`} variant="ghost" size="sm">
            <ArrowSquareOut size={15} /> Source document
          </Button>
          <Button as={Link} to={`/app/sharing?prescription=${rx.id}`} variant="ghost" size="sm">
            <ShareNetwork size={15} /> Share
          </Button>
          <Button variant="ghost" size="sm" onClick={() => window.print()}>
            <Printer size={15} /> Print
          </Button>
          <Button size="sm" onClick={() => setSyncOpen(true)}>
            <CalendarPlus size={15} weight="bold" /> Add to Google
          </Button>
        </div>
      </div>
      <ReportBody rx={rx} />
      <SyncDialog open={syncOpen} onClose={() => setSyncOpen(false)} prescriptionId={rx.id} />
    </div>
  );
}
