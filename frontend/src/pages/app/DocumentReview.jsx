import { useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router";
import { toast } from "sonner";
import {
  ArrowClockwise,
  ArrowLeft,
  CheckCircle,
  DownloadSimple,
  FileX,
  Trash,
  WarningCircle,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton, SkeletonText } from "@/components/ui/Skeleton";
import {
  downloadUrl,
  isProcessing,
  useConfirmExtraction,
  useDeleteDocument,
  useDiscardExtraction,
  useDocument,
  useEvidence,
  useExtraction,
  useReprocessDocument,
} from "@/features/documents/api";
import { KIND_LABEL, STATUS_META } from "@/features/documents/status";
import { SourceViewer } from "@/features/review/SourceViewer";
import { ProcessingState } from "@/features/review/ProcessingState";
import { ReviewForm } from "@/features/review/ReviewForm";
import { ConfirmSuccess } from "@/features/review/ConfirmSuccess";
import { formatBytes, formatDate } from "@/lib/format";
import { useActing } from "@/features/circle/api";
import { findSpot } from "@/features/review/evidence";

function ReviewSkeleton() {
  return (
    <LoadingRegion label="Loading document">
      <Skeleton className="h-4 w-24" />
      <Skeleton className="mt-4 h-9 w-72" />
      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.15fr)]">
        <Skeleton className="aspect-[0.75] w-full rounded-card" />
        <div className="grid grid-cols-1 content-start gap-4">
          {[0, 1, 2].map((i) => (
            <div key={i} className="card card--flat p-5">
              <Skeleton className="h-4 w-40" />
              <SkeletonText lines={3} className="mt-4" />
            </div>
          ))}
        </div>
      </div>
    </LoadingRegion>
  );
}

export default function DocumentReview() {
  const { isActing } = useActing();
  const { id } = useParams();
  const navigate = useNavigate();
  const doc = useDocument(id);
  const status = doc.data?.status;
  const extraction = useExtraction(id, {
    enabled: status === "needs_review" || status === "confirmed",
  });
  const evidence = useEvidence(id, { enabled: Boolean(extraction.data) });
  const confirm = useConfirmExtraction();
  const discard = useDiscardExtraction();
  const reprocess = useReprocessDocument();
  const del = useDeleteDocument();

  const [searchParams] = useSearchParams();
  const [page, setPage] = useState(() => Number(searchParams.get("page")) || 1);
  const [highlight, setHighlight] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [confirmDiscard, setConfirmDiscard] = useState(false);
  const [success, setSuccess] = useState(null);

  if (doc.isPending) return <ReviewSkeleton />;
  if (doc.isError) {
    return (
      <EmptyState
        icon={FileX}
        title="Document not found"
        description="It may have been deleted, or it belongs to another account."
        action={
          <Button as={Link} to="/app/documents">
            Back to documents
          </Button>
        }
      />
    );
  }

  const d = doc.data;
  const meta = STATUS_META[d.status] ?? STATUS_META.queued;

  // Evidence highlights (ADR-031): a focused field (or the "p.N" button) shows its spot.
  const locate = ({ keys, page: fallbackPage, label, explicit }) => {
    const ev = evidence.data;
    const spot = findSpot(ev, keys);
    if (spot) {
      setPage(spot.page);
      setHighlight({ label, page: spot.page, boxes: spot.boxes, status: "found" });
      return;
    }
    if (!explicit) {
      setHighlight(null); // focusing a field with nothing to show clears the last highlight
      return;
    }
    if (fallbackPage) setPage(fallbackPage);
    const status = !keys ? "added" : ev && !ev.available ? "photo" : "missing";
    setHighlight({ label, page: fallbackPage, boxes: [], status });
  };

  const onConfirm = (body) =>
    confirm.mutate(
      { extractionId: extraction.data.id, body },
      {
        onSuccess: (ex) => {
          setSuccess({
            prescriptionId: ex.prescription_id,
            meds: body.medications.length,
            tasks: body.care_actions.length,
          });
          window.scrollTo({ top: 0, behavior: "smooth" });
        },
        onError: (err) => toast.error("Couldn't confirm yet", { description: err.message }),
      },
    );

  const doReprocess = () =>
    reprocess.mutate(d.id, {
      onSuccess: () => {
        setSuccess(null);
        toast("Reading it again", { description: "A fresh draft will be ready shortly." });
      },
      onError: (err) => toast.error(err.message),
    });

  let body;
  if (success) {
    body = (
      <ConfirmSuccess
        prescriptionId={success.prescriptionId}
        medCount={success.meds}
        taskCount={success.tasks}
      />
    );
  } else if (isProcessing(d.status)) {
    body = <ProcessingState status={d.status} />;
  } else if (d.status === "failed") {
    body = (
      <EmptyState
        icon={WarningCircle}
        title="We couldn't finish reading this one"
        description={d.error || "Something went wrong while processing the file."}
        action={
          <div className="flex flex-wrap justify-center gap-2">
            <Button onClick={doReprocess} loading={reprocess.isPending}>
              <ArrowClockwise size={15} weight="bold" /> Try again
            </Button>
            <Button variant="secondary" onClick={() => setConfirmDelete(true)}>
              Delete file
            </Button>
          </div>
        }
      />
    );
  } else if (extraction.isPending) {
    body = <ReviewSkeleton />;
  } else if (extraction.isError) {
    body = (
      <EmptyState
        icon={WarningCircle}
        title="No draft to review"
        description="Reprocess the document to create a new draft."
        action={<Button onClick={doReprocess}>Reprocess</Button>}
      />
    );
  } else {
    const ex = extraction.data;
    const isDraft = ex.status === "draft";
    body = (
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.15fr)] lg:gap-8">
        <div className="lg:sticky lg:top-[calc(var(--nav-h)+20px)] lg:h-[calc(100dvh-var(--nav-h)-140px)]">
          <SourceViewer
            doc={d}
            page={page}
            onPageChange={setPage}
            highlight={highlight}
            onClearHighlight={() => setHighlight(null)}
          />
        </div>
        <div>
          {isDraft && isActing ? (
            <div className="card p-6 text-sm text-ink-2">
              This document is waiting for its owner to review it. Records appear once they confirm.
            </div>
          ) : isDraft ? (
            <ReviewForm
              key={ex.id}
              extraction={ex}
              confirming={confirm.isPending}
              onConfirm={onConfirm}
              onDiscard={() => setConfirmDiscard(true)}
              onLocate={locate}
            />
          ) : (
            <div className="card grid grid-cols-1 gap-4 p-6">
              <p className="flex items-center gap-2 font-semibold">
                <CheckCircle size={20} weight="fill" className="text-accent" /> Confirmed
                {ex.confirmed_at && ` on ${formatDate(ex.confirmed_at)}`}
              </p>
              <p className="text-sm text-ink-2">
                {ex.payload.summary ?? "These records are part of your health timeline."}
              </p>
              <div className="flex flex-wrap gap-2">
                {ex.prescription_id && (
                  <Button as={Link} to={`/app/prescriptions/${ex.prescription_id}`}>
                    View report
                  </Button>
                )}
                <Button variant="secondary" onClick={doReprocess} loading={reprocess.isPending}>
                  <ArrowClockwise size={15} weight="bold" /> Review again
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <>
      <Link
        to="/app/documents"
        className="tap mb-4 inline-flex items-center gap-1.5 text-sm text-ink-2 hover:text-ink"
      >
        <ArrowLeft size={14} weight="bold" /> Documents
      </Link>
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2.5">
            <h1 className="truncate text-2xl font-semibold tracking-tight sm:text-3xl">
              {d.title}
            </h1>
            <Chip tone={meta.tone} live={meta.live}>
              {meta.label}
            </Chip>
          </div>
          <p className="mt-1.5 text-sm text-ink-3">
            {KIND_LABEL[d.kind]} · {d.page_count} page{d.page_count === 1 ? "" : "s"} ·{" "}
            {formatBytes(d.size_bytes)} · {d.original_filename}
          </p>
        </div>
        <div className="flex gap-1.5">
          <Button as="a" href={downloadUrl(d.id)} variant="ghost" size="sm">
            <DownloadSimple size={15} /> Download
          </Button>
          <Button variant="ghost" size="sm" onClick={() => setConfirmDelete(true)}>
            <Trash size={15} /> Delete
          </Button>
        </div>
      </div>

      {body}

      <ConfirmDialog
        open={confirmDelete}
        onClose={() => setConfirmDelete(false)}
        title="Delete this document?"
        description="The file, its extracted data and any records confirmed from it will be removed. This can't be undone."
        confirmLabel="Delete"
        loading={del.isPending}
        onConfirm={() =>
          del.mutate(d.id, {
            onSuccess: () => {
              toast("Document deleted");
              navigate("/app/documents", { replace: true });
            },
          })
        }
      />
      <ConfirmDialog
        open={confirmDiscard}
        onClose={() => setConfirmDiscard(false)}
        title="Discard this draft?"
        description="Nothing from it will be saved. You can reprocess the document later."
        confirmLabel="Discard"
        loading={discard.isPending}
        onConfirm={() =>
          discard.mutate(extraction.data.id, {
            onSuccess: () => {
              setConfirmDiscard(false);
              doc.refetch();
            },
          })
        }
      />
    </>
  );
}
