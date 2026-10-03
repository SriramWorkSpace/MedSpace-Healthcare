import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ArrowsIn, ArrowsOut, CaretLeft, CaretRight, X } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Skeleton } from "@/components/ui/Skeleton";
import { cn } from "@/lib/cn";
import { previewUrl } from "@/features/documents/api";

const STATUS_NOTE = {
  missing: "Not marked: it isn't printed this way on the page",
  photo: "Not marked: highlights need a PDF with selectable text",
  added: "Added by you, so there's nothing to show on the page",
};

/** Marker-style boxes over the page image, at fractions of its size (any zoom, any width). */
function Highlights({ boxes, scrollRoot }) {
  const reduce = useReducedMotion();
  const first = useRef(null);
  const key = boxes.map((b) => b.join(",")).join("|");

  useEffect(() => {
    // Bring the first box into view inside the viewer only; never scroll the page itself.
    const el = first.current;
    const root = scrollRoot.current;
    if (!el || !root) return;
    const box = el.getBoundingClientRect();
    const view = root.getBoundingClientRect();
    const outside =
      box.top < view.top + 12 ||
      box.bottom > view.bottom - 12 ||
      box.left < view.left ||
      box.right > view.right;
    if (!outside) return;
    root.scrollBy({
      top: box.top - view.top - view.height / 3,
      left: box.left < view.left || box.right > view.right ? box.left - view.left - 24 : 0,
      behavior: reduce ? "auto" : "smooth",
    });
  }, [key, reduce, scrollRoot]);

  return (
    <div aria-hidden className="pointer-events-none absolute inset-0">
      {boxes.map(([x0, y0, x1, y1], i) => (
        <motion.span
          key={`${key}-${i}`}
          ref={i === 0 ? first : undefined}
          data-highlight
          initial={reduce ? false : { opacity: 0, transform: "scale(1.12)" }}
          animate={{ opacity: 1, transform: "scale(1)" }}
          transition={{ duration: 0.22, ease: [0.23, 1, 0.32, 1], delay: i * 0.03 }}
          className="absolute rounded-[3px] bg-warn/40 mix-blend-multiply ring-2 ring-warn"
          style={{
            left: `${x0 * 100}%`,
            top: `${y0 * 100}%`,
            width: `${(x1 - x0) * 100}%`,
            height: `${(y1 - y0) * 100}%`,
          }}
        />
      ))}
    </div>
  );
}

function PageImage({ docId, page, zoomed, boxes, scrollRoot }) {
  const [loaded, setLoaded] = useState(false);
  return (
    <div
      className={cn("relative", !loaded && "aspect-[0.707] w-full")}
      style={zoomed ? { width: "160%" } : undefined}
    >
      {!loaded && <Skeleton className="absolute inset-0" />}
      <img
        src={previewUrl(docId, page)}
        alt={`Page ${page} of the source document`}
        onLoad={() => setLoaded(true)}
        className={cn(
          "w-full rounded-lg bg-white shadow-sm ring-1 ring-line transition-opacity duration-300",
          loaded ? "opacity-100" : "opacity-0",
        )}
      />
      {loaded && boxes.length > 0 && <Highlights boxes={boxes} scrollRoot={scrollRoot} />}
    </div>
  );
}

/** Left pane of the review workspace: the original document, page by page. */
export function SourceViewer({ doc, page, onPageChange, highlight, onClearHighlight }) {
  const [zoomed, setZoomed] = useState(false);
  const scrollRoot = useRef(null);
  const pages = doc.page_count;
  const boxes = highlight?.page === page ? highlight.boxes : [];
  const note = highlight ? STATUS_NOTE[highlight.status] : null;

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
        <div role="status" aria-live="polite" className="flex min-w-0 justify-end">
          <AnimatePresence mode="popLayout">
            {highlight && (
              <motion.span
                key="highlight"
                initial={{ opacity: 0, transform: "translateY(-4px)" }}
                animate={{ opacity: 1, transform: "translateY(0px)" }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.16 }}
                className="chip chip--warn min-w-0 gap-1 pr-1"
              >
                <span className="truncate">
                  {highlight.status === "found" ? "Showing" : "Checking"}: {highlight.label}
                </span>
                <button
                  type="button"
                  aria-label="Clear highlight"
                  onClick={onClearHighlight}
                  className="tap grid size-5 shrink-0 place-items-center rounded-full hover:bg-[color-mix(in_oklch,var(--warn),transparent_75%)]"
                >
                  <X size={11} weight="bold" />
                </button>
              </motion.span>
            )}
          </AnimatePresence>
        </div>
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
      {note && (
        <p className="border-b border-line bg-warn-soft px-4 py-2 text-xs text-warn-ink">{note}</p>
      )}
      <div
        ref={scrollRoot}
        className="relative flex-1 overflow-auto bg-surface-2 p-4"
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
            <PageImage
              docId={doc.id}
              page={page}
              zoomed={zoomed}
              boxes={boxes}
              scrollRoot={scrollRoot}
            />
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
