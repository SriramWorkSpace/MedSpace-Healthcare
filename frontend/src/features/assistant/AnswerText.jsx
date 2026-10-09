import { Fragment } from "react";
import { normalizeAnswer } from "./answerFormat";

const BULLET = /^\s*[-*•]\s+/;
const NUMBERED = /^\s*\d{1,2}[.)]\s+/;
const HEADING = /^\s*#{1,6}\s+/;
const RULE = /^\s*(?:-{3,}|\*{3,}|_{3,})\s*$/;

/** Splits text into paragraphs, bullet lists and numbered lists. */
function toBlocks(text) {
  const blocks = [];
  let list = null;
  const flush = () => {
    if (list) blocks.push(list);
    list = null;
  };
  text.split("\n").forEach((line, i) => {
    const kind = BULLET.test(line) ? "ul" : NUMBERED.test(line) ? "ol" : null;
    if (kind) {
      if (list?.type !== kind) {
        flush();
        list = { type: kind, items: [], key: `${kind}-${i}` };
      }
      list.items.push(line.replace(kind === "ul" ? BULLET : NUMBERED, ""));
      return;
    }
    flush();
    if (!line.trim() || RULE.test(line)) return;
    if (HEADING.test(line)) {
      blocks.push({ type: "h", text: line.replace(HEADING, ""), key: `h-${i}` });
    } else {
      blocks.push({ type: "p", text: line, key: `p-${i}` });
    }
  });
  flush();
  return blocks;
}

/**
 * **bold** and __bold__ become <strong>. A marker without its pair (mid-stream, or a stray one)
 * is dropped rather than shown. Returns [{ text, bold }].
 */
function boldSegments(str) {
  const parts = str.split(/(\*\*|__)/g);
  const markers = parts.filter((p) => p === "**" || p === "__").length;
  const usable = markers - (markers % 2); // an unpaired last marker is not a toggle
  const out = [];
  let bold = false;
  let seen = 0;
  for (const part of parts) {
    if (part === "**" || part === "__") {
      seen += 1;
      if (seen <= usable) bold = !bold;
      continue;
    }
    if (part) out.push({ text: part, bold });
  }
  return out;
}

/** Renders an answer: lists, headings, bold, and [n] markers as citation buttons. */
export function AnswerText({ text, onCite, streaming }) {
  const blocks = toBlocks(normalizeAnswer(text));

  const citations = (str, keyPrefix) =>
    str.split(/(\[\d{1,2}\])/g).map((part, i) => {
      const m = part.match(/^\[(\d{1,2})\]$/);
      if (!m) return <Fragment key={`${keyPrefix}-${i}`}>{part}</Fragment>;
      const n = Number(m[1]);
      return (
        <button
          key={`${keyPrefix}-${i}`}
          type="button"
          onClick={() => onCite?.(n)}
          className="mx-0.5 inline-grid h-[18px] min-w-[18px] translate-y-[-1px] place-items-center rounded-md bg-accent-soft px-1 align-middle text-[10.5px] font-semibold text-accent-soft-ink transition-transform hover:scale-110"
          aria-label={`Source ${n}`}
        >
          {n}
        </button>
      );
    });

  const inline = (str) =>
    boldSegments(str).map((seg, i) =>
      seg.bold ? (
        <strong key={i} className="font-semibold text-ink">
          {citations(seg.text, i)}
        </strong>
      ) : (
        <Fragment key={i}>{citations(seg.text, i)}</Fragment>
      ),
    );

  const last = blocks.at(-1);
  return (
    <div className="grid grid-cols-1 gap-2 text-[15px] leading-relaxed">
      {blocks.map((b) => {
        if (b.type === "ul" || b.type === "ol") {
          const List = b.type;
          return (
            <List key={b.key} className="grid grid-cols-1 gap-1.5 pl-1">
              {b.items.map((item, i) => (
                <li key={i} className="flex gap-2">
                  {b.type === "ul" ? (
                    <span
                      className="mt-[9px] size-1.5 shrink-0 rounded-full bg-accent"
                      aria-hidden
                    />
                  ) : (
                    <span className="min-w-4 shrink-0 font-semibold text-ink-2" aria-hidden>
                      {i + 1}.
                    </span>
                  )}
                  <span>{inline(item)}</span>
                </li>
              ))}
            </List>
          );
        }
        return (
          <p key={b.key} className={b.type === "h" ? "font-semibold text-ink" : undefined}>
            {inline(b.text)}
            {streaming && b === last && <Caret />}
          </p>
        );
      })}
      {streaming && (blocks.length === 0 || last.type === "ul" || last.type === "ol") && <Caret />}
    </div>
  );
}

function Caret() {
  return (
    <span
      className="ml-0.5 inline-block h-4 w-[2px] translate-y-[3px] animate-pulse bg-accent"
      aria-hidden
    />
  );
}
