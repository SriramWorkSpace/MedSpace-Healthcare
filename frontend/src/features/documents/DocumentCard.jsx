import { useState } from "react";
import { Link } from "react-router";
import { motion } from "motion/react";
import { FileText, Image as ImageIcon } from "@phosphor-icons/react";
import { Chip } from "@/components/ui/Chip";
import { Skeleton } from "@/components/ui/Skeleton";
import { cn } from "@/lib/cn";
import { formatDate, timeAgo } from "@/lib/format";
import { previewUrl } from "./api";
import { KIND_LABEL, STATUS_META } from "./status";

export function DocumentThumb({ doc, className }) {
  const [loaded, setLoaded] = useState(false);
  const [failed, setFailed] = useState(false);
  return (
    <div className={cn("relative overflow-hidden bg-surface-2 px-6 pt-12", className)}>
      {!loaded && !failed && <Skeleton className="absolute inset-0 rounded-none" />}
      {failed ? (
        <div className="grid h-full place-items-center text-ink-3">
          {doc.mime_type === "application/pdf" ? <FileText size={32} /> : <ImageIcon size={32} />}
        </div>
      ) : (
        <img
          src={previewUrl(doc.id, 1)}
          alt=""
          loading="lazy"
          decoding="async"
          onLoad={() => setLoaded(true)}
          onError={() => setFailed(true)}
          className={cn(
            "h-full w-full rounded-t-md bg-white object-cover object-top shadow-sm ring-1 ring-line transition-[opacity,transform] duration-500",
            "group-hover:-translate-y-1",
            loaded ? "opacity-100" : "opacity-0",
          )}
        />
      )}
    </div>
  );
}

export function DocumentCard({ doc, index = 0 }) {
  const meta = STATUS_META[doc.status] ?? STATUS_META.queued;
  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.97 }}
      transition={{ duration: 0.3, delay: Math.min(index, 8) * 0.03, ease: [0.23, 1, 0.32, 1] }}
    >
      <Link
        to={`/app/documents/${doc.id}`}
        className="card card--interactive group flex h-full flex-col overflow-hidden"
      >
        <div className="relative">
          <DocumentThumb doc={doc} className="aspect-[4/3] border-b border-line" />
          <div className="absolute left-3 top-3">
            <Chip tone={meta.tone} live={meta.live} className="shadow-xs backdrop-blur">
              {meta.label}
            </Chip>
          </div>
        </div>
        <div className="flex flex-1 flex-col p-4">
          <p className="truncate font-semibold">{doc.title}</p>
          <p className="mt-1 text-[13px] text-ink-3">
            {KIND_LABEL[doc.kind] ?? "Document"} ·{" "}
            {doc.document_date ? formatDate(doc.document_date) : `Added ${timeAgo(doc.created_at)}`}
          </p>
          {doc.status === "failed" && doc.error && (
            <p className="mt-2 line-clamp-2 text-xs text-danger-ink">{doc.error}</p>
          )}
        </div>
      </Link>
    </motion.li>
  );
}

export function DocumentGridSkeleton({ count = 6 }) {
  return (
    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-hidden>
      {Array.from({ length: count }, (_, i) => (
        <li key={i} className="card card--flat overflow-hidden">
          <Skeleton className="aspect-[4/3] rounded-none" />
          <div className="grid gap-2 p-4">
            <Skeleton className="h-4 w-3/5" />
            <Skeleton className="h-3 w-2/5" />
          </div>
        </li>
      ))}
    </ul>
  );
}
