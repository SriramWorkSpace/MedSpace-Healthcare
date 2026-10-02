import { Link } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { toast } from "sonner";
import {
  Clock,
  ForkKnife,
  Info,
  MinusCircle,
  Pill,
  PlusCircle,
  Prohibit,
  Trash,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useDeleteDietNote, useDietNotes } from "@/features/records/api";
import { formatDate } from "@/lib/format";
import { cn } from "@/lib/cn";

const GROUPS = [
  { key: "avoid", title: "Avoid", icon: Prohibit, tone: "bg-danger-soft text-danger-ink" },
  { key: "limit", title: "Limit", icon: MinusCircle, tone: "bg-warn-soft text-warn-ink" },
  {
    key: "include",
    title: "Include",
    icon: PlusCircle,
    tone: "bg-accent-soft text-accent-soft-ink",
  },
  { key: "timing", title: "Timing", icon: Clock, tone: "bg-surface-3 text-ink-2" },
  { key: "general", title: "General", icon: Info, tone: "bg-surface-3 text-ink-2" },
];

function Source({ note }) {
  const bits = [
    note.document_title,
    note.prescriber_name,
    note.issued_on && formatDate(note.issued_on, "MMM d"),
  ].filter(Boolean);
  const href = `/app/documents/${note.document_id}${note.source_page ? `?page=${note.source_page}` : ""}`;
  return (
    <Link to={href} className="truncate text-xs text-ink-3 hover:text-accent hover:underline">
      {bits.join(" · ")}
      {note.source_page && ` · p.${note.source_page}`}
    </Link>
  );
}

function NoteGroup({ group, notes, onRemove, index }) {
  const Icon = group.icon;
  return (
    <motion.section
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.05, ease: [0.23, 1, 0.32, 1] }}
      className="card p-5"
      aria-labelledby={`diet-${group.key}`}
    >
      <h2 id={`diet-${group.key}`} className="mb-3 flex items-center gap-2.5 font-semibold">
        <span className={cn("grid size-8 place-items-center rounded-lg", group.tone)}>
          <Icon size={17} weight="duotone" />
        </span>
        {group.title}
        <span className="tabular text-sm font-normal text-ink-3">{notes.length}</span>
      </h2>
      <ul className="grid grid-cols-1 gap-1">
        <AnimatePresence initial={false}>
          {notes.map((n) => (
            <motion.li
              key={n.id}
              layout
              exit={{ opacity: 0, height: 0, transition: { duration: 0.18 } }}
              className="group flex items-start gap-3 rounded-[var(--radius-control)] px-2 py-2.5 hover:bg-surface-2"
            >
              <div className="min-w-0 flex-1">
                <p className="text-[15px]">{n.text}</p>
                <Source note={n} />
              </div>
              <Button
                variant="ghost"
                size="sm"
                icon
                aria-label={`Remove note: ${n.text}`}
                onClick={() => onRemove(n)}
                className="opacity-60 group-hover:opacity-100 focus-visible:opacity-100"
              >
                <Trash size={15} />
              </Button>
            </motion.li>
          ))}
        </AnimatePresence>
      </ul>
    </motion.section>
  );
}

function MedicineNotes({ items }) {
  return (
    <section className="card p-5" aria-labelledby="diet-meds">
      <h2 id="diet-meds" className="flex items-center gap-2.5 font-semibold">
        <span className="grid size-8 place-items-center rounded-lg bg-accent-soft text-accent-soft-ink">
          <Pill size={17} weight="duotone" />
        </span>
        With your medicines
      </h2>
      <p className="mt-1 text-sm text-ink-3">
        Food and drink instructions on current prescriptions.
      </p>
      {items.length === 0 ? (
        <p className="mt-4 text-sm text-ink-2">None of your current medicines mention food.</p>
      ) : (
        <ul className="mt-4 grid grid-cols-1 gap-2">
          {items.map((m, i) => (
            <li
              key={`${m.medication_id}-${i}`}
              className="flex items-center justify-between gap-3 text-sm"
            >
              <span className="min-w-0 truncate font-medium">
                {m.name}{" "}
                {m.strength && <span className="font-normal text-ink-3">{m.strength}</span>}
              </span>
              <span
                className={cn(
                  "chip shrink-0",
                  m.category === "avoid" ? "chip--danger" : "chip--accent",
                )}
              >
                {m.text}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function DietSkeleton() {
  return (
    <LoadingRegion
      label="Loading diet notes"
      className="grid gap-4 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]"
    >
      <div className="grid grid-cols-1 gap-4">
        {[0, 1, 2].map((i) => (
          <div key={i} className="card card--flat p-5">
            <Skeleton className="h-5 w-32" />
            <Skeleton className="mt-4 h-4 w-4/5" />
            <Skeleton className="mt-2 h-3 w-2/5" />
          </div>
        ))}
      </div>
      <Skeleton className="h-48 rounded-card" />
    </LoadingRegion>
  );
}

export default function Diet() {
  const { data, isPending, isError, refetch } = useDietNotes();
  const remove = useDeleteDietNote();

  const onRemove = (note) =>
    remove.mutate(note.id, {
      onSuccess: () =>
        toast("Note removed", {
          description: "Reprocess its document if you ever want it back.",
        }),
      onError: (e) => toast.error(e.message),
    });

  const groups = GROUPS.map((g) => ({
    ...g,
    notes: (data?.notes ?? []).filter((n) => n.category === g.key),
  })).filter((g) => g.notes.length);

  return (
    <>
      <PageHeader
        title="Diet notes"
        description="Food and drink instructions from your documents, gathered in one place."
      />
      {isPending ? (
        <DietSkeleton />
      ) : isError ? (
        <EmptyState
          icon={ForkKnife}
          title="Diet notes didn't load"
          description="A quick retry usually fixes it."
          action={<Button onClick={() => refetch()}>Try again</Button>}
        />
      ) : data.notes.length === 0 && data.medication_notes.length === 0 ? (
        <EmptyState
          icon={ForkKnife}
          title="No diet notes yet"
          description="When a document mentions food or drink, like a low-salt diet or avoiding alcohol, it shows up here after you confirm it."
          action={
            <Button as={Link} to="/app/documents">
              Go to documents
            </Button>
          }
          quip={EMPTY_QUIPS.diet}
        />
      ) : (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)] lg:items-start">
          <div className="grid grid-cols-1 gap-4">
            {groups.length ? (
              groups.map((g, i) => (
                <NoteGroup key={g.key} group={g} notes={g.notes} onRemove={onRemove} index={i} />
              ))
            ) : (
              <p className="card card--flat p-5 text-sm text-ink-2">
                No diet notes on your documents yet. {EMPTY_QUIPS.diet}
              </p>
            )}
          </div>
          <div className="grid grid-cols-1 gap-4 lg:sticky lg:top-[calc(var(--nav-h)+24px)]">
            <MedicineNotes items={data.medication_notes} />
            <aside className="rounded-card bg-surface-2 p-5 text-sm text-ink-2">
              <p className="flex items-center gap-2 font-semibold text-ink">
                <Info size={16} /> Where these come from
              </p>
              <p className="mt-2">
                Every note is copied from a document you reviewed and confirmed. MedSpace doesn't
                add its own nutrition advice. For changes to your diet, ask your care team.
              </p>
            </aside>
          </div>
        </div>
      )}
    </>
  );
}
