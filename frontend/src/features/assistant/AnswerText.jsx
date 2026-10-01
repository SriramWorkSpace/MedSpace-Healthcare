import { Fragment } from "react";

/** Renders an answer: "- " lines become a list, [n] markers become citation buttons. */
export function AnswerText({ text, onCite, streaming }) {
  const lines = text.split("\n");
  const blocks = [];
  let list = null;
  lines.forEach((line, i) => {
    if (line.startsWith("- ")) {
      list ??= [];
      list.push(line.slice(2));
    } else {
      if (list) {
        blocks.push({ type: "ul", items: list, key: `ul-${i}` });
        list = null;
      }
      if (line.trim()) blocks.push({ type: "p", text: line, key: `p-${i}` });
    }
  });
  if (list) blocks.push({ type: "ul", items: list, key: "ul-end" });

  const inline = (str) =>
    str.split(/(\[\d{1,2}\])/g).map((part, i) => {
      const m = part.match(/^\[(\d{1,2})\]$/);
      if (!m) return <Fragment key={i}>{part}</Fragment>;
      const n = Number(m[1]);
      return (
        <button
          key={i}
          type="button"
          onClick={() => onCite?.(n)}
          className="mx-0.5 inline-grid h-[18px] min-w-[18px] translate-y-[-1px] place-items-center rounded-md bg-accent-soft px-1 align-middle text-[10.5px] font-semibold text-accent-soft-ink transition-transform hover:scale-110"
          aria-label={`Source ${n}`}
        >
          {n}
        </button>
      );
    });

  return (
    <div className="grid gap-2 text-[15px] leading-relaxed">
      {blocks.map((b, bi) =>
        b.type === "ul" ? (
          <ul key={b.key} className="grid gap-1.5 pl-1">
            {b.items.map((item, i) => (
              <li key={i} className="flex gap-2">
                <span className="mt-[9px] size-1.5 shrink-0 rounded-full bg-accent" aria-hidden />
                <span>{inline(item)}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p key={b.key}>
            {inline(b.text)}
            {streaming && bi === blocks.length - 1 && <Caret />}
          </p>
        ),
      )}
      {streaming && (blocks.length === 0 || blocks.at(-1).type === "ul") && <Caret />}
    </div>
  );
}

function Caret() {
  return <span className="ml-0.5 inline-block h-4 w-[2px] translate-y-[3px] animate-pulse bg-accent" aria-hidden />;
}
