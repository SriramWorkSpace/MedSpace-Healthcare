import { CheckCircle, Eye, FileMagnifyingGlass, LockKey, Warning } from "@phosphor-icons/react";
import { Chip } from "@/components/ui/Chip";
import { Reveal } from "./Reveal";

const PRINCIPLES = [
  {
    icon: FileMagnifyingGlass,
    title: "Every field shows its source",
    body: "Page references on every extracted value, so checking takes seconds.",
  },
  {
    icon: Warning,
    title: "Uncertainty is flagged, not hidden",
    body: "Low-confidence fields and unreadable shorthand are highlighted for you.",
  },
  {
    icon: CheckCircle,
    title: "Nothing syncs until you confirm",
    body: "Calendar, Tasks, timeline and reports only use data you approved.",
  },
  {
    icon: LockKey,
    title: "Sharing is scoped and audited",
    body: "Links expire, can be revoked, and every view lands in your activity log.",
  },
];

export function Trust() {
  return (
    <section id="privacy" className="border-y border-line bg-bg-sunken">
      <div className="shell shell--marketing grid grid-cols-1 gap-14 py-20 lg:grid-cols-2 lg:py-28">
        <Reveal>
          <h2 className="text-3xl font-semibold tracking-tight sm:text-5xl">
            AI reads it.
            <br />
            <span className="text-ink-3">You confirm it.</span>
          </h2>
          <p className="mt-5 max-w-[46ch] text-lg text-ink-2">
            MedSpace organizes what your documents say. It never diagnoses, suggests treatment or
            changes a dose.
          </p>

          <div className="card mt-10 max-w-md p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold">Duration</p>
              <Chip tone="warn">
                <Eye size={12} weight="bold" /> Check page 1
              </Chip>
            </div>
            <div className="mt-3 rounded-[var(--radius-control)] bg-surface-2 p-3 font-mono text-[12px] text-ink-2">
              Metformin 500mg BD p.c.{" "}
              <mark className="rounded bg-warn-soft px-1 text-warn-ink">x 90/7</mark>
            </div>
            <div className="input input--attention mt-3 flex items-center text-sm">90 days</div>
            <p className="mt-2 text-xs text-ink-3">Confidence 88%. We read "90/7" as 90 days.</p>
          </div>
        </Reveal>

        <ul className="grid grid-cols-1 content-center gap-0 divide-y divide-line">
          {PRINCIPLES.map(({ icon: Icon, title, body }, i) => (
            <Reveal
              as="li"
              key={title}
              delay={i * 0.06}
              className="flex gap-4 py-6 first:pt-0 last:pb-0"
            >
              <span className="mt-0.5 grid grid-cols-1 size-10 shrink-0 place-items-center rounded-xl bg-surface text-accent shadow-xs ring-1 ring-line">
                <Icon size={20} weight="duotone" />
              </span>
              <div>
                <h3 className="font-semibold">{title}</h3>
                <p className="mt-1 text-[15px] text-ink-2">{body}</p>
              </div>
            </Reveal>
          ))}
        </ul>
      </div>
    </section>
  );
}
