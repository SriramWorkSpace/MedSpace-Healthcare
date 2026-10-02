import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { useQueryClient } from "@tanstack/react-query";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { toast } from "sonner";
import {
  ArrowUp,
  ChatsCircle,
  FileText,
  List,
  Plus,
  ShieldCheck,
  Sparkle,
  Stop,
  Trash,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Skeleton } from "@/components/ui/Skeleton";
import { cn } from "@/lib/cn";
import { timeAgo } from "@/lib/format";
import { LOADING_PUNS, pick } from "@/easter-eggs/puns";
import {
  askKeys,
  streamAnswer,
  useCreateThread,
  useDeleteThread,
  useThread,
  useThreads,
} from "@/features/assistant/api";
import { AnswerText } from "@/features/assistant/AnswerText";

const SUGGESTIONS = [
  "What medications am I taking right now?",
  "How often do I take Amoxicillin?",
  "When is my next follow-up?",
  "What did my lipid panel show?",
  "What did my doctors say about food?",
  "Summarize my latest prescription",
];

function SourceChips({ sources, onOpen }) {
  if (!sources?.length) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-1.5">
      {sources.map((s) => (
        <button
          key={s.n}
          type="button"
          onClick={() => onOpen(s)}
          title={s.snippet}
          className="inline-flex max-w-full items-center gap-1.5 rounded-full border border-line bg-surface px-2.5 py-1 text-xs text-ink-2 transition-colors hover:border-accent hover:text-ink"
        >
          <span className="grid grid-cols-1 size-4 place-items-center rounded bg-accent-soft text-[10px] font-semibold text-accent-soft-ink">
            {s.n}
          </span>
          <span className="truncate">{s.title}</span>
          {s.page_no && <span className="text-ink-3">p.{s.page_no}</span>}
          {!s.confirmed && <span className="text-warn-ink">unconfirmed</span>}
        </button>
      ))}
    </div>
  );
}

function UserBubble({ text }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: [0.23, 1, 0.32, 1] }}
      className="ml-auto max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-br-md bg-ink px-4 py-2.5 text-[15px] text-bg"
    >
      {text}
    </motion.div>
  );
}

function AssistantBubble({ text, citations, streaming, searching, onOpen }) {
  const [pun] = useState(() => pick(LOADING_PUNS));
  const byN = Object.fromEntries((citations ?? []).map((c) => [c.n, c]));
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: [0.23, 1, 0.32, 1] }}
      className="flex max-w-[92%] gap-3"
    >
      <span className="mt-0.5 grid grid-cols-1 size-8 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
        <Sparkle size={16} weight="fill" />
      </span>
      <div className="min-w-0 flex-1 pt-1">
        {searching && !text ? (
          <p className="flex items-center gap-2 text-sm text-ink-3">
            <span className="inline-flex gap-1" aria-hidden>
              {[0, 1, 2].map((i) => (
                <motion.span
                  key={i}
                  className="size-1.5 rounded-full bg-accent"
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 1, repeat: Infinity, delay: i * 0.15 }}
                />
              ))}
            </span>
            {pun}…
          </p>
        ) : (
          <AnswerText text={text} streaming={streaming} onCite={(n) => byN[n] && onOpen(byN[n])} />
        )}
        <SourceChips sources={citations} onOpen={onOpen} />
      </div>
    </motion.div>
  );
}

function EmptyChat({ onPick }) {
  const reduce = useReducedMotion();
  return (
    <div className="mx-auto flex max-w-xl flex-col items-center py-10 text-center">
      <div className="grid grid-cols-1 size-14 place-items-center rounded-2xl bg-accent-soft text-accent-soft-ink">
        <ChatsCircle size={28} weight="duotone" />
      </div>
      <h2 className="mt-5 text-2xl font-semibold tracking-tight">Ask about your records</h2>
      <p className="mt-2 text-ink-2">
        Answers come only from documents you've uploaded, with the page they came from.
      </p>
      <div className="mt-8 flex flex-wrap justify-center gap-2">
        {SUGGESTIONS.map((q, i) => (
          <motion.button
            key={q}
            type="button"
            onClick={() => onPick(q)}
            initial={reduce ? false : { opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 * i, duration: 0.3 }}
            className="rounded-full border border-line bg-surface px-4 py-2 text-sm text-ink-2 shadow-xs transition-[border-color,color,transform] hover:border-accent hover:text-ink active:scale-[0.97]"
          >
            {q}
          </motion.button>
        ))}
      </div>
    </div>
  );
}

function ThreadList({ activeId, onSelect, onNew, onDelete }) {
  const { data, isPending } = useThreads();
  return (
    <div className="flex h-full flex-col">
      <Button variant="secondary" className="w-full" onClick={onNew}>
        <Plus size={15} weight="bold" /> New conversation
      </Button>
      <div className="mt-4 flex-1 overflow-y-auto">
        {isPending ? (
          <div className="grid grid-cols-1 gap-2">
            {[0, 1, 2].map((i) => (
              <Skeleton key={i} className="h-12" />
            ))}
          </div>
        ) : data.length === 0 ? (
          <p className="px-2 text-sm text-ink-3">No conversations yet.</p>
        ) : (
          <ul className="grid grid-cols-1 gap-0.5">
            {data.map((t) => (
              <li key={t.id} className="group relative">
                <button
                  type="button"
                  onClick={() => onSelect(t.id)}
                  className={cn(
                    "w-full rounded-[var(--radius-control)] px-3 py-2.5 pr-9 text-left transition-colors",
                    t.id === activeId
                      ? "bg-surface shadow-xs ring-1 ring-line"
                      : "hover:bg-surface-2",
                  )}
                >
                  <span className="block truncate text-sm font-medium">{t.title}</span>
                  <span className="block text-xs text-ink-3">{timeAgo(t.updated_at)}</span>
                </button>
                <button
                  type="button"
                  aria-label={`Delete conversation ${t.title}`}
                  onClick={() => onDelete(t.id)}
                  className="absolute right-2 top-1/2 grid grid-cols-1 size-7 -translate-y-1/2 place-items-center rounded-lg text-ink-3 opacity-0 transition-opacity hover:bg-surface-3 hover:text-danger-ink focus-visible:opacity-100 group-hover:opacity-100"
                >
                  <Trash size={14} />
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default function Ask() {
  const [params, setParams] = useSearchParams();
  const threadId = params.get("t");
  const navigate = useNavigate();
  const qc = useQueryClient();
  const thread = useThread(threadId);
  const createThread = useCreateThread();
  const deleteThread = useDeleteThread();

  const [input, setInput] = useState("");
  const [pending, setPending] = useState(null);
  const [showThreads, setShowThreads] = useState(false);
  const abortRef = useRef(null);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  const messages = thread.data?.messages ?? [];
  const busy = Boolean(pending?.streaming);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, pending?.answer, pending?.question]);

  const openSource = (s) => {
    if (s.document_id)
      navigate(`/app/documents/${s.document_id}${s.page_no ? `?page=${s.page_no}` : ""}`);
  };

  async function send(text) {
    const question = text.trim();
    if (!question || busy) return;
    setInput("");
    let tid = threadId;
    try {
      if (!tid) {
        tid = (await createThread.mutateAsync()).id;
        setParams({ t: tid }, { replace: true });
      }
    } catch (e) {
      toast.error(e.message);
      return;
    }
    const controller = new AbortController();
    abortRef.current = controller;
    setPending({ question, answer: "", sources: [], citations: null, streaming: true });
    try {
      await streamAnswer(tid, question, {
        signal: controller.signal,
        onSources: ({ sources }) => setPending((p) => ({ ...p, sources })),
        onToken: (t) => setPending((p) => ({ ...p, answer: p.answer + t })),
        onDone: ({ citations }) => setPending((p) => ({ ...p, citations, streaming: false })),
        onError: ({ detail }) => toast.error(detail),
      });
    } catch (e) {
      if (e.name !== "AbortError") toast.error(e.message || "The assistant is unavailable.");
    } finally {
      abortRef.current = null;
      await qc.invalidateQueries({ queryKey: askKeys.thread(tid) });
      qc.invalidateQueries({ queryKey: askKeys.threads });
      setPending(null);
      inputRef.current?.focus();
    }
  }

  const threadList = (
    <ThreadList
      activeId={threadId}
      onSelect={(id) => {
        setParams({ t: id });
        setShowThreads(false);
      }}
      onNew={() => {
        setParams({});
        setShowThreads(false);
        inputRef.current?.focus();
      }}
      onDelete={(id) =>
        deleteThread.mutate(id, {
          onSuccess: () => id === threadId && setParams({}),
        })
      }
    />
  );

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[260px_minmax(0,1fr)]">
      <aside className="hidden lg:block lg:h-[calc(100dvh-var(--nav-h)-120px)] lg:sticky lg:top-[calc(var(--nav-h)+24px)]">
        {threadList}
      </aside>

      <section className="flex min-h-[calc(100dvh-var(--nav-h)-120px)] flex-col">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">Ask MedSpace</h1>
            <p className="flex items-center gap-1.5 text-sm text-ink-3">
              <ShieldCheck size={14} weight="bold" /> Sourced from your records. Not medical advice.
            </p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            onClick={() => setShowThreads((v) => !v)}
          >
            <List size={15} /> Chats
          </Button>
        </div>

        <AnimatePresence>
          {showThreads && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-4 overflow-hidden lg:hidden"
            >
              <div className="card p-3">{threadList}</div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex-1" aria-live="polite">
          {threadId && thread.isPending ? (
            <div className="grid grid-cols-1 gap-4">
              <Skeleton className="ml-auto h-10 w-2/5 rounded-2xl" />
              <Skeleton className="h-24 w-4/5 rounded-2xl" />
            </div>
          ) : messages.length === 0 && !pending ? (
            <EmptyChat onPick={send} />
          ) : (
            <div className="grid grid-cols-1 gap-6 pb-6">
              {messages.map((m) =>
                m.role === "user" ? (
                  <UserBubble key={m.id} text={m.content} />
                ) : (
                  <AssistantBubble
                    key={m.id}
                    text={m.content}
                    citations={m.citations}
                    onOpen={openSource}
                  />
                ),
              )}
              {pending && (
                <>
                  <UserBubble text={pending.question} />
                  <AssistantBubble
                    text={pending.answer}
                    citations={pending.citations ?? []}
                    streaming={pending.streaming}
                    searching={pending.streaming}
                    onOpen={openSource}
                  />
                  {pending.streaming && pending.sources.length > 0 && (
                    <p className="ml-11 flex items-center gap-1.5 text-xs text-ink-3">
                      <FileText size={13} /> Checked {pending.sources.length} source
                      {pending.sources.length === 1 ? "" : "s"}
                    </p>
                  )}
                </>
              )}
            </div>
          )}
          <div ref={endRef} />
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
          className="sticky bottom-0 -mx-1 mt-2 bg-gradient-to-t from-bg from-60% to-transparent px-1 pb-4 pt-8"
        >
          <div className="card flex items-end gap-2 p-2 shadow-md focus-within:ring-2 focus-within:ring-accent/30">
            <label htmlFor="ask-input" className="sr-only">
              Ask a question about your records
            </label>
            <textarea
              id="ask-input"
              ref={inputRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  send(input);
                }
              }}
              placeholder="Ask about a medication, a date, a test result…"
              maxLength={1000}
              className="max-h-40 min-h-[44px] flex-1 resize-none bg-transparent px-3 py-2.5 text-[15px] outline-none placeholder:text-ink-3 [field-sizing:content]"
            />
            {busy ? (
              <Button
                type="button"
                variant="secondary"
                icon
                aria-label="Stop answering"
                onClick={() => abortRef.current?.abort()}
              >
                <Stop size={16} weight="fill" />
              </Button>
            ) : (
              <Button type="submit" icon aria-label="Send question" disabled={!input.trim()}>
                <ArrowUp size={17} weight="bold" />
              </Button>
            )}
          </div>
          <p className="mt-2 text-center text-xs text-ink-3">
            Enter to send, Shift+Enter for a new line.
          </p>
        </form>
      </section>
    </div>
  );
}
