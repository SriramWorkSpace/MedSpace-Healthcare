import { Fragment, useEffect, useId, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useNavigate } from "react-router";
import {
  ArrowRight,
  ChatsCircle,
  CheckSquare,
  ClockCounterClockwise,
  FileText,
  Flask,
  ForkKnife,
  GearSix,
  MagnifyingGlass,
  Pill,
  Prescription,
  ShareNetwork,
  SquaresFour,
  UploadSimple,
} from "@phosphor-icons/react";
import { cn } from "@/lib/cn";
import { useSearch } from "./api";
import { useActing } from "@/features/circle/api";

const GROUPS = [
  { key: "medications", label: "Medications", icon: Pill },
  { key: "prescriptions", label: "Prescriptions", icon: Prescription },
  { key: "lab_results", label: "Lab results", icon: Flask },
  { key: "documents", label: "Documents", icon: FileText },
  { key: "to_dos", label: "To-dos", icon: CheckSquare },
  { key: "diet_notes", label: "Diet notes", icon: ForkKnife },
];

const JUMP_TO = [
  { title: "Dashboard", href: "/app", icon: SquaresFour },
  { title: "Upload a document", href: "/app/documents?upload=1", icon: UploadSimple },
  { title: "Medications", href: "/app/medications", icon: Pill },
  { title: "Lab results", href: "/app/labs", icon: Flask },
  { title: "Diet notes", href: "/app/diet", icon: ForkKnife },
  { title: "Timeline", href: "/app/timeline", icon: ClockCounterClockwise },
  { title: "Ask MedSpace", href: "/app/ask", icon: ChatsCircle },
  { title: "Sharing", href: "/app/sharing", icon: ShareNetwork },
  { title: "Settings", href: "/app/settings", icon: GearSix },
];

function useDebounced(value, ms) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return debounced;
}

/** Wraps case-insensitive occurrences of `q` in <mark>. */
function Highlight({ text, q }) {
  const needle = q.trim();
  if (!needle) return text;
  const parts = text.split(new RegExp(`(${needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "ig"));
  return parts.map((part, i) =>
    part.toLowerCase() === needle.toLowerCase() ? (
      <mark key={i} className="rounded-sm bg-accent-soft text-accent-soft-ink">
        {part}
      </mark>
    ) : (
      <Fragment key={i}>{part}</Fragment>
    ),
  );
}

/** Server snippets mark matches with <<...>>. */
function Snippet({ text }) {
  return text.split(/(<<.*?>>)/g).map((part, i) =>
    part.startsWith("<<") ? (
      <mark key={i} className="rounded-sm bg-accent-soft text-accent-soft-ink">
        {part.slice(2, -2)}
      </mark>
    ) : (
      <Fragment key={i}>{part}</Fragment>
    ),
  );
}

export default function SearchPalette({ onClose }) {
  const navigate = useNavigate();
  const listId = useId();
  const inputRef = useRef(null);
  const listRef = useRef(null);
  const [q, setQ] = useState("");
  const [active, setActive] = useState(0);
  const debounced = useDebounced(q, 160);
  const { data, isFetching } = useSearch(debounced);
  const trimmed = q.trim();
  const searching = trimmed.length >= 2;
  const askable = !useActing().isActing; // Ask MedSpace is the owner's

  // Flatten everything selectable into one list so arrow keys walk across groups.
  const items = useMemo(() => {
    if (!searching) return JUMP_TO.map((j) => ({ ...j, kind: "jump" }));
    const out = [];
    for (const g of GROUPS) {
      (data?.groups?.[g.key] ?? []).forEach((hit, n) =>
        out.push({ ...hit, kind: "hit", group: g, header: n === 0 ? g.label : null }),
      );
    }
    if (!askable) return out;
    out.push({
      kind: "ask",
      title: `Ask MedSpace about "${trimmed}"`,
      href: `/app/ask?q=${encodeURIComponent(trimmed)}`,
      icon: ChatsCircle,
    });
    return out;
  }, [searching, data, trimmed, askable]);

  const safeActive = Math.min(active, items.length - 1);

  useEffect(() => {
    const { overflow } = document.body.style;
    document.body.style.overflow = "hidden";
    const previously = document.activeElement;
    inputRef.current?.focus();
    return () => {
      document.body.style.overflow = overflow;
      previously?.focus?.();
    };
  }, []);

  useEffect(() => {
    listRef.current
      ?.querySelector(`[data-index="${safeActive}"]`)
      ?.scrollIntoView({ block: "nearest" });
  }, [safeActive]);

  const go = (item) => {
    onClose();
    navigate(item.href);
  };

  const onKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((i) => (i + 1) % items.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((i) => (i - 1 + items.length) % items.length);
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (items[safeActive]) go(items[safeActive]);
    } else if (e.key === "Escape") {
      e.preventDefault();
      onClose();
    } else if (e.key === "Tab") {
      e.preventDefault(); // focus stays in the dialog; arrows move through results
    }
  };

  const noHits = searching && data && data.total === 0 && debounced.trim() === trimmed;

  return createPortal(
    <div className="fixed inset-0" style={{ zIndex: "var(--z-dialog)" }}>
      {/* No open/close animation: this is summoned from the keyboard many times a day. */}
      <div
        className="absolute inset-0 bg-[oklch(0.2_0.02_165/0.4)] backdrop-blur-[2px]"
        onClick={onClose}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Search MedSpace"
        className="card relative mx-auto mt-[max(16px,10vh)] flex max-h-[min(560px,78dvh)] w-[min(640px,calc(100%-32px))] flex-col overflow-hidden shadow-lg"
      >
        <div className="flex items-center gap-3 border-b border-line px-4">
          <MagnifyingGlass
            size={18}
            className={cn("shrink-0", isFetching ? "text-accent" : "text-ink-3")}
          />
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setActive(0);
            }}
            onKeyDown={onKeyDown}
            placeholder="Search medicines, doctors, documents, lab results…"
            role="combobox"
            aria-expanded="true"
            aria-controls={listId}
            aria-activedescendant={items[safeActive] ? `${listId}-${safeActive}` : undefined}
            aria-autocomplete="list"
            className="h-14 min-w-0 flex-1 bg-transparent text-[15px] outline-none placeholder:text-ink-3"
          />
          <kbd className="kbd hidden sm:inline">Esc</kbd>
        </div>

        <ul
          ref={listRef}
          id={listId}
          role="listbox"
          aria-label="Results"
          className="overflow-y-auto p-2"
        >
          {!searching && (
            <li role="presentation" className="px-3 pb-1 pt-2 text-xs font-medium text-ink-3">
              Jump to
            </li>
          )}
          {noHits && (
            <li role="presentation" className="px-3 py-6 text-center text-sm text-ink-2">
              No matches in your records. Not even a placebo.
            </li>
          )}
          {items.map((item, i) => {
            const header = item.header;
            const Icon = item.kind === "hit" ? item.group.icon : item.icon;
            const selected = i === safeActive;
            return (
              <Fragment key={`${item.kind}-${item.href}-${i}`}>
                {header && (
                  <li role="presentation" className="px-3 pb-1 pt-3 text-xs font-medium text-ink-3">
                    {header}
                  </li>
                )}
                {item.kind === "ask" && i > 0 && (
                  <li role="presentation" className="my-2 h-px bg-line" />
                )}
                <li
                  id={`${listId}-${i}`}
                  data-index={i}
                  role="option"
                  aria-selected={selected}
                  onMouseMove={() => setActive(i)}
                  onClick={() => go(item)}
                  className={cn(
                    "flex cursor-pointer items-center gap-3 rounded-[var(--radius-control)] px-3 py-2.5",
                    selected ? "bg-surface-2" : "",
                  )}
                >
                  <span
                    className={cn(
                      "grid size-8 shrink-0 place-items-center rounded-lg",
                      item.kind === "ask" ? "bg-accent text-accent-ink" : "bg-surface-2 text-ink-2",
                      selected && item.kind !== "ask" && "bg-surface",
                    )}
                  >
                    <Icon size={16} weight="duotone" />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-sm font-medium">
                      {item.kind === "hit" ? (
                        <Highlight text={item.title} q={trimmed} />
                      ) : (
                        item.title
                      )}
                    </span>
                    {item.snippet ? (
                      <span className="block truncate text-xs text-ink-3">
                        {item.subtitle && <span className="text-ink-2">{item.subtitle} · </span>}
                        <Snippet text={item.snippet} />
                      </span>
                    ) : (
                      item.subtitle && (
                        <span className="block truncate text-xs text-ink-3">{item.subtitle}</span>
                      )
                    )}
                  </span>
                  {selected && <ArrowRight size={14} className="shrink-0 text-ink-3" />}
                </li>
              </Fragment>
            );
          })}
        </ul>

        <div className="hidden items-center gap-4 border-t border-line px-4 py-2.5 text-xs text-ink-3 sm:flex">
          <span>
            <kbd className="kbd">↑</kbd> <kbd className="kbd">↓</kbd> to move
          </span>
          <span>
            <kbd className="kbd">Enter</kbd> to open
          </span>
          <span className="ml-auto">Only your own records are searched.</span>
        </div>
      </div>
    </div>,
    document.body,
  );
}
