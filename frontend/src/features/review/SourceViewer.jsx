import { useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { ArrowsIn, ArrowsOut, CaretLeft, CaretRight } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Skeleton } from "@/components/ui/Skeleton";
import { cn } from "@/lib/cn";
import { previewUrl } from "@/features/documents/api";

function PageImage({ docId, page, zoomed }) {
  const [loaded, setLoaded] = useState(false);
  return (
    <div className={cn("relative w-full", !loaded && "aspect-[0.707]")}>
      {!loaded && <Skeleton className="absolute inset-0" />}
      <img
        src={previewUrl(docId, page)}
        alt={`Page ${page} of the source document`}
        onLoad={() => setLoaded(true)}
        className={cn(
          "w-full rounded-lg bg-white shadow-sm ring-1 ring-line transition-opacity duration-300",
          loaded ? "opacity-100" : "opacity-0",
          zoomed ? "max-w-none" : "",
        )}
        style={zoomed ? { width: "160%" } : undefined}
      />
    </div>
  );
}

/** Left pane of the review workspace: the original document, page by page. */
export function SourceViewer({ doc, page, onPageChange, highlight }) {
  const [zoomed, setZoomed] = useState(false);
  const pages = doc.page_count;

  return (
    <div className="card flex h-full flex-col overflow-hidden">
      <div className="flex items-center justify-between gap-2 border-b border-line px-4 py-2.5">
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            icon
            aria-label="Previous page"
            disabled={page <= 1}
            onClick={() => onPageChange(page - 1)}
          >
            <CaretLeft size={15} weight="bold" />
          </Button>
          <span className="tabular min-w-[76px] text-center text-[13px] text-ink-2">
            Page {page} of {pages}
          </span>
          <Button
            variant="ghost"
            size="sm"
            icon
            aria-label="Next page"
            disabled={page >= pages}
            onClick={() => onPageChange(page + 1)}
          >
            <CaretRight size={15} weight="bold" />
          </Button>
        </div>
        <AnimatePresence>
          {highlight && (
            <motion.span
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="chip chip--warn truncate"
            >
              Checking: {highlight}
            </motion.span>
          )}
        </AnimatePresence>
        <Button
          variant="ghost"
          size="sm"
          icon
          aria-label={zoomed ? "Fit to width" : "Zoom in"}
          onClick={() => setZoomed((z) => !z)}
        >
          {zoomed ? <ArrowsIn size={15} weight="bold" /> : <ArrowsOut size={15} weight="bold" />}
        </Button>
      </div>
      <div
        className="flex-1 overflow-auto bg-surface-2 p-4"
        tabIndex={0}
        role="region"
        aria-label={`Source document, page ${page}`}
      >
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={page}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.18 }}
          >
            <PageImage docId={doc.id} page={page} zoomed={zoomed} />
          </motion.div>
        </AnimatePresence>
      </div>
      {pages > 1 && (
        <div className="flex gap-1.5 overflow-x-auto border-t border-line px-4 py-2.5">
          {Array.from({ length: pages }, (_, i) => i + 1).map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => onPageChange(n)}
              aria-label={`Go to page ${n}`}
              aria-current={n === page ? "page" : undefined}
              className={cn(
                "tabular grid h-8 min-w-8 place-items-center rounded-lg px-2 text-xs font-medium transition-colors",
                n === page
                  ? "bg-accent text-accent-ink"
                  : "bg-surface text-ink-2 hover:bg-surface-3",
              )}
            >
              {n}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
