import { useCallback, useState } from "react";
import { Link } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { useQueryClient } from "@tanstack/react-query";
import { CheckCircle, FileArrowUp, WarningCircle, X } from "@phosphor-icons/react";
import { formatBytes } from "@/lib/format";
import { docKeys, uploadDocument } from "./api";

let seq = 0;

/** Upload state machine for many files at once. Returns [items, enqueue]. */
export function useUploadQueue() {
  const qc = useQueryClient();
  const [items, setItems] = useState([]);

  const patch = useCallback((id, changes) => {
    setItems((list) => list.map((it) => (it.id === id ? { ...it, ...changes } : it)));
  }, []);

  const remove = useCallback((id) => setItems((list) => list.filter((it) => it.id !== id)), []);

  const enqueue = useCallback(
    (files) => {
      for (const file of files) {
        const id = ++seq;
        const { promise, abort } = uploadDocument(file, {
          onProgress: (p) => patch(id, { progress: p }),
        });
        setItems((list) => [...list, { id, file, progress: 0, status: "uploading", abort }]);
        promise
          .then((doc) => {
            patch(id, { status: "done", progress: 1, docId: doc.id });
            qc.invalidateQueries({ queryKey: docKeys.all });
            setTimeout(() => remove(id), 1600);
          })
          .catch((err) => {
            if (err.code === "aborted") return remove(id);
            patch(id, {
              status: "error",
              error: err.message,
              existingId: err.problem?.document_id,
            });
          });
      }
    },
    [patch, remove, qc],
  );

  return { items, enqueue, remove };
}

export function UploadQueue({ items, onDismiss }) {
  return (
    <ul className="grid gap-2" aria-live="polite">
      <AnimatePresence initial={false}>
        {items.map((it) => (
          <motion.li
            key={it.id}
            layout
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.98, transition: { duration: 0.15 } }}
            transition={{ duration: 0.22, ease: [0.23, 1, 0.32, 1] }}
            className="card card--flat flex items-center gap-3 px-4 py-3"
          >
            <span
              className={
                it.status === "error"
                  ? "text-danger"
                  : it.status === "done"
                    ? "text-accent"
                    : "text-ink-3"
              }
            >
              {it.status === "error" ? (
                <WarningCircle size={20} weight="duotone" />
              ) : it.status === "done" ? (
                <CheckCircle size={20} weight="fill" />
              ) : (
                <FileArrowUp size={20} weight="duotone" />
              )}
            </span>
            <div className="min-w-0 flex-1">
              <div className="flex items-baseline justify-between gap-3">
                <p className="truncate text-sm font-medium">{it.file.name}</p>
                <span className="tabular shrink-0 text-xs text-ink-3">
                  {it.status === "uploading"
                    ? `${Math.round(it.progress * 100)}%`
                    : it.status === "done"
                      ? "Uploaded"
                      : formatBytes(it.file.size)}
                </span>
              </div>
              {it.status === "error" ? (
                <p className="mt-0.5 text-xs text-danger-ink">
                  {it.error}{" "}
                  {it.existingId && (
                    <Link to={`/app/documents/${it.existingId}`} className="font-medium underline">
                      Open it
                    </Link>
                  )}
                </p>
              ) : (
                <div className="mt-2 h-1 overflow-hidden rounded-full bg-surface-3">
                  <motion.div
                    className="h-full rounded-full bg-accent"
                    initial={false}
                    animate={{ scaleX: it.progress }}
                    style={{ originX: 0 }}
                    transition={{ duration: 0.2 }}
                  />
                </div>
              )}
            </div>
            {(it.status === "error" || it.status === "uploading") && (
              <button
                type="button"
                onClick={() => (it.status === "uploading" ? it.abort() : onDismiss(it.id))}
                aria-label={it.status === "uploading" ? "Cancel upload" : "Dismiss"}
                className="grid size-7 place-items-center rounded-full text-ink-3 hover:bg-surface-2 hover:text-ink"
              >
                <X size={14} weight="bold" />
              </button>
            )}
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  );
}
