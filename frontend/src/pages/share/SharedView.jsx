import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { motion } from "motion/react";
import { formatDistanceToNowStrict, parseISO } from "date-fns";
import { DownloadSimple, Eye, FileText, LinkBreak, ShieldCheck } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Logo } from "@/components/ui/Logo";
import { LoadingRegion, Skeleton, SkeletonText } from "@/components/ui/Skeleton";
import { ThemeToggle } from "@/components/nav/ThemeToggle";
import { ReportBody } from "@/features/records/ReportBody";
import { publicFileUrl, publicPreviewUrl, usePublicShare } from "@/features/sharing/api";
import { formatDate } from "@/lib/format";

/** Keep the secret token out of Referer headers sent to anything this page links to. */
function useNoReferrer() {
  useEffect(() => {
    const meta = document.createElement("meta");
    meta.name = "referrer";
    meta.content = "no-referrer";
    document.head.appendChild(meta);
    return () => meta.remove();
  }, []);
}

function SharedDocument({ token, doc }) {
  const [page, setPage] = useState(1);
  const [loaded, setLoaded] = useState(false);
  return (
    <article className="card overflow-hidden">
      <header className="flex items-center justify-between gap-3 border-b border-line px-6 py-4">
        <div className="min-w-0">
          <p className="truncate font-semibold">{doc.title}</p>
          <p className="text-xs text-ink-3">
            {doc.kind === "lab_report" ? "Lab report" : "Document"}
            {doc.document_date && ` · ${formatDate(doc.document_date)}`}
          </p>
        </div>
        <Button as="a" href={publicFileUrl(token, doc.id)} variant="ghost" size="sm">
          <DownloadSimple size={15} /> Download
        </Button>
      </header>
      <div className="bg-surface-2 p-4 sm:p-6">
        <div className="relative mx-auto max-w-2xl">
          {!loaded && <Skeleton className="aspect-[0.707] w-full" />}
          <img
            src={publicPreviewUrl(token, doc.id, page)}
            alt={`${doc.title}, page ${page}`}
            onLoad={() => setLoaded(true)}
            className={
              loaded
                ? "w-full rounded-lg bg-white shadow-sm ring-1 ring-line"
                : "absolute inset-0 opacity-0"
            }
          />
        </div>
        {doc.page_count > 1 && (
          <div className="mt-4 flex justify-center gap-1.5">
            {Array.from({ length: doc.page_count }, (_, i) => i + 1).map((n) => (
              <Button
                key={n}
                size="sm"
                variant={n === page ? "primary" : "secondary"}
                onClick={() => {
                  setLoaded(false);
                  setPage(n);
                }}
              >
                {n}
              </Button>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}

function Unavailable({ status, message }) {
  const gone = status === 410;
  return (
    <div className="mx-auto grid grid-cols-1 max-w-md justify-items-center py-20 text-center">
      <span className="grid grid-cols-1 size-14 place-items-center rounded-2xl bg-surface-2 text-ink-2">
        <LinkBreak size={26} />
      </span>
      <h1 className="mt-6 text-2xl font-semibold tracking-tight">
        {gone ? "This link has been discharged" : "We couldn't find that link"}
      </h1>
      <p className="mt-2 text-ink-2">
        {message || "Check that you copied the whole link."} Ask the person who shared it for a new
        one.
      </p>
      <Button as={Link} to="/" variant="secondary" className="mt-8">
        What is MedSpace?
      </Button>
    </div>
  );
}

export default function SharedView() {
  const { token } = useParams();
  useNoReferrer();
  const { data, isPending, isError, error } = usePublicShare(token);

  return (
    <div className="min-h-[100dvh]">
      <header className="border-b border-line">
        <div className="mx-auto flex h-16 max-w-4xl items-center justify-between px-4 sm:px-6">
          <Logo />
          <div className="flex items-center gap-2">
            <span className="hidden items-center gap-1.5 text-xs text-ink-3 sm:inline-flex">
              <ShieldCheck size={14} /> Read-only shared view
            </span>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
        {isPending ? (
          <LoadingRegion label="Opening shared records">
            <Skeleton className="h-8 w-72" />
            <Skeleton className="mt-3 h-4 w-56" />
            <div className="card card--flat mt-8 p-8">
              <SkeletonText lines={6} />
            </div>
          </LoadingRegion>
        ) : isError ? (
          <Unavailable status={error.status} message={error.message} />
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <p className="text-sm font-medium text-accent">Shared by {data.shared_by}</p>
            <h1 className="mt-1 text-3xl font-semibold tracking-tight">{data.label}</h1>
            <p className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-ink-3">
              <span>Link expires in {formatDistanceToNowStrict(parseISO(data.expires_at))}</span>
              {data.views_left !== null && (
                <span className="inline-flex items-center gap-1">
                  <Eye size={14} /> {data.views_left} view{data.views_left === 1 ? "" : "s"} left
                </span>
              )}
            </p>

            <div className="mt-8 grid grid-cols-1 gap-6">
              {data.prescriptions.map((rx) => (
                <div key={rx.id} className="grid grid-cols-1 gap-3">
                  <ReportBody rx={rx} />
                  <details className="group">
                    <summary className="inline-flex cursor-pointer items-center gap-1.5 text-sm font-medium text-accent">
                      <FileText size={15} /> View the original document
                    </summary>
                    <div className="mt-3">
                      <SharedDocument
                        token={token}
                        doc={{
                          id: rx.document_id,
                          title: rx.document_title,
                          kind: "prescription",
                          page_count: 1,
                          document_date: rx.issued_on,
                        }}
                      />
                    </div>
                  </details>
                </div>
              ))}
              {data.documents.map((doc) => (
                <SharedDocument key={doc.id} token={token} doc={doc} />
              ))}
            </div>

            <p className="mt-12 text-center text-xs text-ink-3">
              Shared through MedSpace. This view reflects documents as reviewed by their owner and
              is not medical advice. Synthetic demo data.
            </p>
          </motion.div>
        )}
      </main>
    </div>
  );
}
