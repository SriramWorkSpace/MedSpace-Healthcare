import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router";
import { useDropzone } from "react-dropzone";
import { AnimatePresence, motion } from "motion/react";
import { CloudArrowUp, FileText, UploadSimple, WarningCircle } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { SegmentedTabs } from "@/components/ui/Tabs";
import { LoadingRegion } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useDocuments } from "@/features/documents/api";
import { DocumentCard, DocumentGridSkeleton } from "@/features/documents/DocumentCard";
import { UploadQueue } from "@/features/documents/UploadQueue";
import { useUploadQueue } from "@/features/documents/useUploadQueue";
import { FILTERS } from "@/features/documents/status";
import { cn } from "@/lib/cn";
import { useActing } from "@/features/circle/api";

const ACCEPT = {
  "application/pdf": [".pdf"],
  "image/png": [".png"],
  "image/jpeg": [".jpg", ".jpeg"],
  "image/webp": [".webp"],
};
const MAX_BYTES = 15 * 1024 * 1024;

export default function Documents() {
  const [params, setParams] = useSearchParams();
  const [filter, setFilter] = useState("all");
  const { data, isPending, isError, refetch } = useDocuments();
  const { items: uploads, enqueue, remove } = useUploadQueue();
  const [rejections, setRejections] = useState([]);

  const { isActing } = useActing();
  const { getRootProps, getInputProps, open, isDragActive } = useDropzone({
    disabled: isActing,
    accept: ACCEPT,
    maxSize: MAX_BYTES,
    noClick: true,
    noKeyboard: true,
    onDrop: (accepted, rejected) => {
      if (accepted.length) enqueue(accepted);
      setRejections(
        rejected.map((r) => ({
          name: r.file.name,
          reason:
            r.errors[0]?.code === "file-too-large"
              ? "is larger than 15 MB"
              : "isn't a PDF, JPG, PNG or WEBP",
        })),
      );
    },
  });

  // "Upload" buttons elsewhere link here with ?upload=1 to open the picker.
  useEffect(() => {
    if (params.get("upload") === "1") {
      setParams({}, { replace: true });
      open();
    }
  }, [params, setParams, open]);

  const tabs = useMemo(() => {
    const counts = data?.counts ?? {};
    return FILTERS.map((f) => ({
      key: f.key,
      label: f.label,
      count: f.statuses
        ? f.statuses.reduce((n, s) => n + (counts[s] ?? 0), 0)
        : (counts[f.key] ?? 0),
    }));
  }, [data]);

  const visible = useMemo(() => {
    const items = data?.items ?? [];
    if (filter === "all") return items;
    const f = FILTERS.find((x) => x.key === filter);
    const statuses = f?.statuses ?? [filter];
    return items.filter((d) => statuses.includes(d.status));
  }, [data, filter]);

  const isEmpty = data && data.items.length === 0 && uploads.length === 0;

  return (
    <div {...getRootProps()} className="relative outline-none">
      <input {...getInputProps()} aria-label="Upload documents" />

      <PageHeader
        title="Documents"
        description="Prescriptions, reports and anything else your care team hands you."
      />

      {/* Drop target / hint */}
      {!isEmpty && !isActing && (
        <button
          type="button"
          onClick={open}
          className="mb-6 flex w-full items-center gap-4 rounded-card border border-dashed border-line-strong bg-surface/60 px-5 py-4 text-left transition-colors hover:border-accent hover:bg-accent-soft/30"
        >
          <span className="grid grid-cols-1 size-10 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
            <CloudArrowUp size={20} weight="duotone" />
          </span>
          <span>
            <span className="block text-sm font-semibold">Drop files anywhere on this page</span>
            <span className="block text-[13px] text-ink-3">
              or click to browse. PDF, JPG, PNG or WEBP up to 15 MB.
            </span>
          </span>
        </button>
      )}

      {(uploads.length > 0 || rejections.length > 0) && (
        <div className="mb-6 grid grid-cols-1 gap-2">
          <UploadQueue items={uploads} onDismiss={remove} />
          {rejections.map((r) => (
            <p
              key={r.name}
              role="alert"
              className="flex items-center gap-2 rounded-[var(--radius-control)] bg-danger-soft px-4 py-2.5 text-sm text-danger-ink"
            >
              <WarningCircle size={16} weight="bold" /> {r.name} {r.reason}.
            </p>
          ))}
        </div>
      )}

      {isPending ? (
        <LoadingRegion label="Loading documents">
          <div className="mb-5 h-10 w-96 max-w-full rounded-full skeleton" />
          <DocumentGridSkeleton />
        </LoadingRegion>
      ) : isError ? (
        <EmptyState
          icon={WarningCircle}
          title="We couldn't load your documents"
          description="The server didn't respond. Your files are safe."
          action={<Button onClick={() => refetch()}>Try again</Button>}
        />
      ) : isEmpty ? (
        <EmptyState
          icon={FileText}
          title="No documents yet"
          description="Drag a prescription or lab report onto this page, or pick a file. PDFs and photos both work."
          action={
            isActing ? undefined : (
              <Button onClick={open}>
                <UploadSimple size={15} weight="bold" /> Choose files
              </Button>
            )
          }
          quip={EMPTY_QUIPS.documents}
        />
      ) : (
        <>
          <SegmentedTabs
            label="Filter documents"
            items={tabs}
            value={filter}
            onChange={setFilter}
            className="mb-5"
          />
          {visible.length === 0 ? (
            <p className="rounded-card border border-line bg-surface px-5 py-10 text-center text-sm text-ink-2">
              Nothing here right now. {EMPTY_QUIPS.review}
            </p>
          ) : (
            <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
              <AnimatePresence mode="popLayout">
                {visible.map((doc, i) => (
                  <DocumentCard key={doc.id} doc={doc} index={i} />
                ))}
              </AnimatePresence>
            </ul>
          )}
        </>
      )}

      {/* Full-page drag overlay */}
      <AnimatePresence>
        {isDragActive && (
          <motion.div
            className="pointer-events-none fixed inset-0 grid grid-cols-1 place-items-center bg-[color-mix(in_oklch,var(--bg),transparent_15%)] backdrop-blur-sm"
            style={{ zIndex: "var(--z-dialog)" }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
          >
            <motion.div
              initial={{ scale: 0.96 }}
              animate={{ scale: 1 }}
              className={cn(
                "grid place-items-center rounded-[28px] border-2 border-dashed border-accent bg-surface px-16 py-14 text-center shadow-lg",
              )}
            >
              <CloudArrowUp size={44} weight="duotone" className="text-accent" />
              <p className="mt-4 text-xl font-semibold">Drop to upload</p>
              <p className="mt-1 text-sm text-ink-2">We'll start reading as soon as it lands.</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
