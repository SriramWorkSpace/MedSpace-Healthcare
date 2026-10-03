import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { toast } from "sonner";
import {
  ArrowLeft,
  Check,
  ClipboardText,
  Plus,
  Printer,
  ShareNetwork,
  Sparkle,
  Trash,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { Field, Input } from "@/components/ui/Field";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { useDeleteVisit, useUpdateVisit, useVisitBrief } from "@/features/visits/api";
import { VisitBrief } from "@/features/visits/VisitBrief";
import { cn } from "@/lib/cn";
import { useActing } from "@/features/circle/api";

const newId = () => Math.random().toString(36).slice(2, 12);

function BackLink() {
  return (
    <Link
      to="/app/visits"
      className="tap no-print mb-4 inline-flex items-center gap-1.5 rounded-lg text-sm text-ink-2 hover:text-accent"
    >
      <ArrowLeft size={14} weight="bold" />
      All visits
    </Link>
  );
}

/** Saves a text/date field when it loses focus (or on Enter), only if it changed. */
function SavedInput({ value, onSave, ...props }) {
  const [draft, setDraft] = useState(value ?? "");
  const [seen, setSeen] = useState(value ?? "");
  if ((value ?? "") !== seen) {
    // The server value changed (another save, a refetch): follow it.
    setSeen(value ?? "");
    setDraft(value ?? "");
  }
  const commit = () => {
    if (draft !== (value ?? "")) onSave(draft);
  };
  return (
    <Input
      value={draft}
      onChange={(e) => setDraft(e.target.value)}
      onBlur={commit}
      onKeyDown={(e) => e.key === "Enter" && e.currentTarget.blur()}
      {...props}
    />
  );
}

function Details({ visit, update }) {
  const save = (field) => (v) =>
    update.mutate({ [field]: v === "" ? null : v }, { onError: (e) => toast.error(e.message) });
  return (
    <section className="card grid grid-cols-1 gap-4 p-5" aria-labelledby="details-heading">
      <h2 id="details-heading" className="font-semibold">
        Details
      </h2>
      <Field label="Title">
        <SavedInput value={visit.title} onSave={(v) => v.trim() && save("title")(v.trim())} />
      </Field>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
        <Field label="Visit date" optional>
          <SavedInput type="date" value={visit.visit_date} onSave={save("visit_date")} />
        </Field>
        <Field label="With" optional>
          <SavedInput
            value={visit.clinician}
            onSave={save("clinician")}
            placeholder="Dr. Imani Oduya"
          />
        </Field>
      </div>
      <Field
        label="Changes since"
        optional
        hint="Leave empty to cover everything since your last visit, or the last 90 days."
      >
        <SavedInput type="date" value={visit.since} onSave={save("since")} />
      </Field>
    </section>
  );
}

function Questions({ visit, update }) {
  const [text, setText] = useState("");
  const questions = visit.questions;
  const save = (next) =>
    update.mutate({ questions: next }, { onError: (e) => toast.error(e.message) });

  const add = (e) => {
    e.preventDefault();
    const value = text.trim();
    if (!value) return;
    if (questions.length >= 30) {
      toast.error("That's 30 questions. Your clinician's calendar thanks you for stopping here.");
      return;
    }
    save([...questions, { id: newId(), text: value, done: false, prompt_key: null }]);
    setText("");
  };

  return (
    <section className="card p-5" aria-labelledby="questions-heading">
      <h2 id="questions-heading" className="font-semibold">
        Your questions
      </h2>
      <p className="mt-0.5 text-sm text-ink-3">
        Write them down now so nothing gets forgotten in the room.
      </p>
      {questions.length > 0 && (
        <ul className="mt-4 grid grid-cols-1 gap-1.5">
          <AnimatePresence initial={false}>
            {questions.map((q) => (
              <motion.li
                key={q.id}
                layout
                initial={{ opacity: 0, y: -4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, transition: { duration: 0.12 } }}
                transition={{ duration: 0.2, ease: [0.23, 1, 0.32, 1] }}
                className="group flex items-start gap-3 rounded-[var(--radius-control)] bg-surface-2 px-3 py-2.5"
              >
                <button
                  type="button"
                  role="checkbox"
                  aria-checked={q.done}
                  aria-label={`Answered: ${q.text}`}
                  onClick={() =>
                    save(questions.map((x) => (x.id === q.id ? { ...x, done: !x.done } : x)))
                  }
                  className={cn(
                    "mt-0.5 grid size-5 shrink-0 place-items-center rounded-md border-2 transition-colors duration-150",
                    q.done
                      ? "border-accent bg-accent text-accent-ink"
                      : "border-line-strong hover:border-ink-3",
                  )}
                >
                  {q.done && <Check size={12} weight="bold" />}
                </button>
                <span
                  className={cn(
                    "min-w-0 flex-1 text-[15px] break-words",
                    q.done && "text-ink-3 line-through",
                  )}
                >
                  {q.text}
                </span>
                <button
                  type="button"
                  aria-label={`Remove question: ${q.text}`}
                  onClick={() => save(questions.filter((x) => x.id !== q.id))}
                  className="grid size-7 shrink-0 place-items-center rounded-lg text-ink-3 transition-opacity hover:bg-surface-3 hover:text-danger-ink pointer-fine:opacity-0 pointer-fine:group-hover:opacity-100 pointer-fine:focus-visible:opacity-100"
                >
                  <Trash size={14} />
                </button>
              </motion.li>
            ))}
          </AnimatePresence>
        </ul>
      )}
      <form onSubmit={add} className="mt-4 flex gap-2">
        <label htmlFor="new-question" className="sr-only">
          New question
        </label>
        <Input
          id="new-question"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ask about…"
          maxLength={300}
          className="flex-1"
        />
        <Button type="submit" variant="secondary" disabled={!text.trim()}>
          <Plus size={14} weight="bold" /> Add
        </Button>
      </form>
    </section>
  );
}

function Prompts({ prompts, visit, update }) {
  if (!prompts.length) return null;
  const added = new Set(visit.questions.map((q) => q.prompt_key).filter(Boolean));
  const add = (p) =>
    update.mutate(
      {
        questions: [
          ...visit.questions,
          { id: newId(), text: `Ask about: ${p.text}`, done: false, prompt_key: p.key },
        ],
      },
      { onError: (e) => toast.error(e.message) },
    );
  return (
    <section className="card p-5" aria-labelledby="prompts-heading">
      <h2 id="prompts-heading" className="flex items-center gap-2 font-semibold">
        <Sparkle size={16} weight="duotone" className="text-accent" />
        From your records
      </h2>
      <p className="mt-0.5 text-sm text-ink-3">
        Facts you might want to bring up. MedSpace doesn't say what they mean.
      </p>
      <ul className="mt-4 grid grid-cols-1 gap-2">
        {prompts.map((p) => {
          const isAdded = added.has(p.key);
          return (
            <li
              key={p.key}
              className="flex flex-col gap-2 rounded-[var(--radius-control)] border border-line px-3 py-2.5 text-sm sm:flex-row sm:items-start sm:justify-between"
            >
              <span className="text-ink-2">{p.text}</span>
              <Button
                size="sm"
                variant={isAdded ? "ghost" : "secondary"}
                disabled={isAdded}
                onClick={() => add(p)}
                className="shrink-0 self-start"
              >
                {isAdded ? (
                  <>
                    <Check size={13} weight="bold" /> Added
                  </>
                ) : (
                  <>
                    <Plus size={13} weight="bold" /> Add as question
                  </>
                )}
              </Button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

function PrepSkeleton() {
  return (
    <LoadingRegion label="Loading visit prep">
      <Skeleton className="mb-3 h-4 w-24" />
      <Skeleton className="mb-8 h-9 w-72" />
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.6fr)]">
        <div className="grid grid-cols-1 content-start gap-4">
          <Skeleton className="h-64 rounded-card" />
          <Skeleton className="h-48 rounded-card" />
        </div>
        <Skeleton className="h-[640px] rounded-card" />
      </div>
    </LoadingRegion>
  );
}

export default function VisitPrep() {
  const { isActing } = useActing();
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, isPending, isError, error, refetch } = useVisitBrief(id);
  const update = useUpdateVisit(id);
  const remove = useDeleteVisit();
  const [confirming, setConfirming] = useState(false);

  if (isPending) return <PrepSkeleton />;
  if (isError) {
    const missing = error?.status === 404 || error?.status === 422;
    return (
      <>
        <BackLink />
        <EmptyState
          icon={ClipboardText}
          title={missing ? "We couldn't find that visit" : "The visit brief didn't load"}
          description={missing ? "It may have been deleted." : "A quick retry usually fixes it."}
          action={
            missing ? (
              <Button as={Link} to="/app/visits">
                See all visits
              </Button>
            ) : (
              <Button onClick={() => refetch()}>Try again</Button>
            )
          }
        />
      </>
    );
  }

  const { visit } = data;

  return (
    <>
      <BackLink />
      <div className="no-print mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="mb-1.5 text-sm font-medium text-accent">Visit prep</p>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-[34px]">{visit.title}</h1>
        </div>
        <div className="flex flex-wrap gap-1.5">
          <Button variant="secondary" size="sm" onClick={() => window.print()}>
            <Printer size={15} /> Print
          </Button>
          {!isActing && (
            <Button as={Link} to={`/app/sharing?visit=${visit.id}`} variant="secondary" size="sm">
              <ShareNetwork size={15} /> Share
            </Button>
          )}
          {!isActing && (
            <Button variant="ghost" size="sm" onClick={() => setConfirming(true)}>
              <Trash size={15} /> Delete
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.6fr)] lg:items-start">
        {!isActing && (
          <div className="no-print grid grid-cols-1 content-start gap-4">
            <Questions visit={visit} update={update} />
            <Prompts prompts={data.prompts} visit={visit} update={update} />
            <Details key={visit.id} visit={visit} update={update} />
          </div>
        )}
        <VisitBrief brief={data} />
      </div>

      <ConfirmDialog
        open={confirming}
        onClose={() => setConfirming(false)}
        title="Delete this visit prep?"
        description="Your questions for it are deleted too. Records are not affected, and any share link to it stops showing it."
        confirmLabel="Delete"
        loading={remove.isPending}
        onConfirm={() =>
          remove.mutate(visit.id, {
            onSuccess: () => {
              toast("Visit prep deleted");
              navigate("/app/visits");
            },
            onError: (e) => toast.error(e.message),
          })
        }
      />
    </>
  );
}
