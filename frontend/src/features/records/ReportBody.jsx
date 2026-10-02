import { Chip } from "@/components/ui/Chip";
import { Logo } from "@/components/ui/Logo";
import { formatClock, formatDate } from "@/lib/format";
import { CARE_KINDS } from "@/features/review/mapping";

const KIND_LABEL = Object.fromEntries(CARE_KINDS.map((k) => [k.value, k.label]));

function Meta({ label, value }) {
  return (
    <div>
      <dt className="text-xs font-medium text-ink-3">{label}</dt>
      <dd className="mt-1 text-sm font-medium">{value || "Not stated"}</dd>
    </div>
  );
}

/** A clean, printable summary of one confirmed prescription. Rendered from the same records the
 *  rest of the app uses, so it can never disagree with the dashboard. */
export function ReportBody({ rx, compact = false }) {
  return (
    <article className="report card overflow-hidden">
      <header className="flex flex-col gap-4 border-b border-line px-6 py-6 sm:flex-row sm:items-start sm:justify-between sm:px-8">
        <div>
          <p className="text-xs font-medium text-ink-3">Prescription summary</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight">
            {rx.prescriber_name || rx.clinic_name || rx.document_title}
          </h1>
          {rx.clinic_name && rx.prescriber_name && (
            <p className="text-sm text-ink-2">{rx.clinic_name}</p>
          )}
        </div>
        <Logo size={24} className="print-only-show opacity-90" />
      </header>

      <dl className="grid grid-cols-1 gap-5 border-b border-line px-6 py-5 sm:grid-cols-4 sm:px-8">
        <Meta label="Issued" value={rx.issued_on && formatDate(rx.issued_on)} />
        <Meta label="Specialty" value={rx.prescriber_specialty} />
        <Meta label="Follow-up" value={rx.follow_up_on && formatDate(rx.follow_up_on)} />
        <Meta label="Medications" value={`${rx.medication_count} (${rx.active_count} active)`} />
      </dl>

      <section className="px-6 py-6 sm:px-8">
        <h2 className="mb-3 text-sm font-semibold">Medications</h2>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs text-ink-3">
                <th className="py-2 pr-4 font-medium">Medicine</th>
                <th className="py-2 pr-4 font-medium">Schedule</th>
                <th className="py-2 pr-4 font-medium">Duration</th>
                <th className="py-2 pr-4 font-medium">Instructions</th>
                {!compact && <th className="py-2 font-medium">Source</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {rx.medications.map((m) => (
                <tr key={m.id} className="align-top">
                  <td className="py-3 pr-4">
                    <p className="font-semibold">{m.name}</p>
                    <p className="text-xs text-ink-3">
                      {[m.strength, m.form].filter(Boolean).join(" · ")}
                    </p>
                  </td>
                  <td className="py-3 pr-4">
                    <p>{m.schedule.label}</p>
                    {m.schedule.times.length > 0 && (
                      <p className="tabular text-xs text-ink-3">
                        {m.schedule.times.map(formatClock).join(", ")}
                      </p>
                    )}
                    {m.frequency_raw && (
                      <p className="font-mono text-[11px] text-ink-3">
                        as written: {m.frequency_raw}
                      </p>
                    )}
                  </td>
                  <td className="py-3 pr-4">
                    {m.duration_days ? `${m.duration_days} days` : "Ongoing"}
                    <p className="text-xs text-ink-3">
                      {formatDate(m.start_date, "MMM d")}
                      {m.end_date && ` to ${formatDate(m.end_date, "MMM d")}`}
                    </p>
                  </td>
                  <td className="py-3 pr-4 text-ink-2">{m.instructions || "None"}</td>
                  {!compact && (
                    <td className="py-3">
                      <Chip>Page {m.source_page}</Chip>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {rx.care_actions.length > 0 && (
        <section className="border-t border-line px-6 py-6 sm:px-8">
          <h2 className="mb-3 text-sm font-semibold">Follow-ups and to-dos</h2>
          <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            {rx.care_actions.map((a) => (
              <li key={a.id} className="rounded-[var(--radius-control)] bg-surface-2 px-4 py-3">
                <p
                  className={`text-sm font-medium ${a.completed_at ? "text-ink-3 line-through" : ""}`}
                >
                  {a.title}
                </p>
                <p className="text-xs text-ink-3">
                  {KIND_LABEL[a.kind] ?? "To-do"}
                  {a.due_on && ` · due ${formatDate(a.due_on, "MMM d")}`}
                </p>
              </li>
            ))}
          </ul>
        </section>
      )}

      {rx.diet_notes?.length > 0 && (
        <section className="border-t border-line px-6 py-6 sm:px-8">
          <h2 className="mb-3 text-sm font-semibold">Diet and lifestyle notes</h2>
          <ul className="grid gap-2">
            {rx.diet_notes.map((n) => (
              <li key={n.id} className="flex items-start gap-3 text-sm">
                <Chip
                  tone={
                    n.category === "avoid" ? "danger" : n.category === "limit" ? "warn" : "accent"
                  }
                  className="shrink-0 capitalize"
                >
                  {n.category}
                </Chip>
                <span className="text-ink-2">{n.text}</span>
                {!compact && n.source_page && (
                  <span className="ml-auto shrink-0 text-xs text-ink-3">p.{n.source_page}</span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {rx.summary && (
        <section className="border-t border-line px-6 py-5 sm:px-8">
          <h2 className="mb-1.5 text-sm font-semibold">Summary</h2>
          <p className="text-sm text-ink-2">{rx.summary}</p>
        </section>
      )}

      <footer className="border-t border-line bg-surface-2 px-6 py-4 text-xs text-ink-3 sm:px-8">
        This summary reflects what the source document says, as reviewed and confirmed by the
        account holder. It is not medical advice. Generated by MedSpace on{" "}
        {formatDate(new Date(), "MMMM d, yyyy")}.
      </footer>
    </article>
  );
}
