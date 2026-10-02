import { FlagChip } from "@/features/labs/FlagChip";
import { formatClock, formatDate } from "@/lib/format";
import { cn } from "@/lib/cn";

const CHANGE_LABELS = {
  started: "Started",
  starts: "Starts",
  stopped: "Stopped",
  finished: "Finished",
};

function Section({ title, count, children, empty }) {
  return (
    <section className="brief-section border-t border-line px-6 py-5 sm:px-8">
      <h2 className="mb-3 flex items-baseline gap-2 text-sm font-semibold">
        {title}
        {count != null && <span className="tabular text-xs font-normal text-ink-3">{count}</span>}
      </h2>
      {empty ? <p className="text-sm text-ink-3">{empty}</p> : children}
    </section>
  );
}

const label = (name, strength) => (strength ? `${name} ${strength}` : name);

/**
 * The printable, shareable visit brief. Read-only: editing happens around it on the visit page.
 * Everything here is quoted from records; nothing is interpreted.
 */
export function VisitBrief({ brief, className }) {
  const { visit } = brief;
  const questions = visit.questions.filter((q) => !q.done);
  const answered = visit.questions.filter((q) => q.done);

  return (
    <article className={cn("card overflow-hidden", className)} aria-label="Visit brief">
      <header className="px-6 pb-5 pt-6 sm:px-8">
        <p className="text-xs font-medium text-ink-3">Visit brief for {brief.patient}</p>
        <h2 className="mt-1 text-2xl font-semibold tracking-tight">{visit.title}</h2>
        <dl className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-sm text-ink-2">
          {visit.visit_date && (
            <div className="flex gap-1.5">
              <dt className="text-ink-3">Visit</dt>
              <dd>{formatDate(visit.visit_date, "EEE, MMM d, yyyy")}</dd>
            </div>
          )}
          {visit.clinician && (
            <div className="flex gap-1.5">
              <dt className="text-ink-3">With</dt>
              <dd>{visit.clinician}</dd>
            </div>
          )}
          <div className="flex gap-1.5">
            <dt className="text-ink-3">Covers</dt>
            <dd>
              {formatDate(brief.since)} to {formatDate(brief.until)}
            </dd>
          </div>
        </dl>
      </header>

      <Section
        title="Questions"
        count={questions.length || null}
        empty={questions.length ? null : "No open questions."}
      >
        <ol className="grid list-decimal gap-1.5 pl-5 text-[15px] marker:text-ink-3">
          {questions.map((q) => (
            <li key={q.id}>{q.text}</li>
          ))}
        </ol>
        {answered.length > 0 && (
          <p className="mt-3 text-xs text-ink-3">
            {answered.length} answered question{answered.length === 1 ? "" : "s"} not shown.
          </p>
        )}
      </Section>

      <Section
        title="Current medications"
        count={brief.medications.length}
        empty={brief.medications.length ? null : "No current medications on record."}
      >
        <div
          className="relative overflow-x-auto"
          tabIndex={0}
          role="region"
          aria-label="Current medications"
        >
          <table className="w-full min-w-[520px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs text-ink-3">
                <th className="py-2 pr-4 font-medium">Medicine</th>
                <th className="py-2 pr-4 font-medium">Schedule</th>
                <th className="py-2 pr-4 font-medium">Course</th>
                <th className="py-2 font-medium">Prescriber</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {brief.medications.map((m) => (
                <tr key={m.id} className="align-top">
                  <td className="py-2.5 pr-4">
                    <p className="font-medium">{label(m.name, m.strength)}</p>
                    {m.instructions && <p className="text-xs text-ink-3">{m.instructions}</p>}
                  </td>
                  <td className="py-2.5 pr-4">
                    <p>{m.schedule}</p>
                    {m.times.length > 0 && (
                      <p className="tabular text-xs text-ink-3">
                        {m.times.map(formatClock).join(", ")}
                      </p>
                    )}
                  </td>
                  <td className="tabular py-2.5 pr-4 text-ink-2">
                    {m.end_date
                      ? `${formatDate(m.start_date, "MMM d")} to ${formatDate(m.end_date, "MMM d")}`
                      : `${m.status === "upcoming" ? "Starts" : "Since"} ${formatDate(m.start_date, "MMM d")}`}
                  </td>
                  <td className="py-2.5 text-ink-2">{m.prescriber_name ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <div className="grid grid-cols-1 md:grid-cols-2 md:[&>section:nth-child(even)]:border-l">
        <Section
          title="Medication changes"
          count={brief.changes.length || null}
          empty={brief.changes.length ? null : "No changes in this period."}
        >
          <ul className="grid grid-cols-1 gap-1.5 text-sm">
            {brief.changes.map((c, i) => (
              <li key={i} className="flex justify-between gap-3">
                <span>
                  <span className="text-ink-3">{CHANGE_LABELS[c.kind]}</span>{" "}
                  {label(c.name, c.strength)}
                </span>
                <span className="tabular shrink-0 text-ink-3">{formatDate(c.date, "MMM d")}</span>
              </li>
            ))}
          </ul>
        </Section>

        <Section
          title="Doses marked"
          empty={brief.doses.length ? null : "No scheduled doses in this period."}
        >
          <ul className="grid grid-cols-1 gap-1.5 text-sm">
            {brief.doses.map((d) => (
              <li key={d.medication_id} className="flex justify-between gap-3">
                <span className="min-w-0 truncate">{label(d.name, d.strength)}</span>
                <span className="tabular shrink-0 text-ink-2">
                  {d.taken} of {d.due} taken
                  {d.skipped > 0 && <span className="text-ink-3">, {d.skipped} skipped</span>}
                </span>
              </li>
            ))}
          </ul>
        </Section>
      </div>

      <Section
        title="Lab results in this period"
        count={brief.labs.length || null}
        empty={brief.labs.length ? null : "No lab results in this period."}
      >
        <div
          className="relative overflow-x-auto"
          tabIndex={0}
          role="region"
          aria-label="Lab results"
        >
          <table className="w-full min-w-[520px] text-left text-sm">
            <thead>
              <tr className="border-b border-line text-xs text-ink-3">
                <th className="py-2 pr-4 font-medium">Test</th>
                <th className="py-2 pr-4 font-medium">Result</th>
                <th className="py-2 pr-4 font-medium">Printed range</th>
                <th className="py-2 font-medium">Previous</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {brief.labs.map((l) => (
                <tr key={l.key} className="align-middle">
                  <td className="py-2.5 pr-4">
                    <p className="font-medium">{l.name}</p>
                    <p className="text-xs text-ink-3">{formatDate(l.collected_on)}</p>
                  </td>
                  <td className="tabular py-2.5 pr-4">
                    <span className="inline-flex flex-wrap items-center gap-2">
                      <span className="font-semibold">
                        {l.value_text}
                        {l.unit && <span className="font-normal text-ink-3"> {l.unit}</span>}
                      </span>
                      <FlagChip flag={l.flag === "normal" ? null : l.flag} />
                    </span>
                  </td>
                  <td className="tabular py-2.5 pr-4 text-ink-2">{l.ref_range ?? "None"}</td>
                  <td className="tabular py-2.5 text-ink-2">
                    {l.previous_value_text
                      ? `${l.previous_value_text} on ${formatDate(l.previous_collected_on, "MMM d, yyyy")}`
                      : "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {brief.labs.length > 0 && (
          <p className="mt-2 text-xs text-ink-3">
            Flags compare each value only with the range printed on its own report.
          </p>
        )}
      </Section>

      <div className="grid grid-cols-1 md:grid-cols-2 md:[&>section:nth-child(even)]:border-l">
        <Section
          title="Open to-dos"
          count={brief.todos.length || null}
          empty={brief.todos.length ? null : "Nothing open."}
        >
          <ul className="grid grid-cols-1 gap-1.5 text-sm">
            {brief.todos.map((t) => (
              <li key={t.id} className="flex justify-between gap-3">
                <span>{t.title}</span>
                {t.due_on && (
                  <span className="tabular shrink-0 text-ink-3">
                    {formatDate(t.due_on, "MMM d")}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </Section>
        <Section
          title="Upcoming appointments"
          empty={brief.appointments.length ? null : "None on record."}
        >
          <ul className="grid grid-cols-1 gap-1.5 text-sm">
            {brief.appointments.map((a, i) => (
              <li key={i} className="flex justify-between gap-3">
                <span>
                  {a.title}
                  {a.subtitle && <span className="text-ink-3"> · {a.subtitle}</span>}
                </span>
                <span className="tabular shrink-0 text-ink-3">{formatDate(a.date, "MMM d")}</span>
              </li>
            ))}
          </ul>
        </Section>
      </div>

      {brief.diet_notes.length > 0 && (
        <Section title="Diet notes from your documents">
          <ul className="grid list-disc gap-1 pl-5 text-sm marker:text-ink-3">
            {brief.diet_notes.map((n, i) => (
              <li key={i}>{n}</li>
            ))}
          </ul>
        </Section>
      )}

      {brief.documents.length > 0 && (
        <Section title="Documents in this period" count={brief.documents.length}>
          <ul className="grid grid-cols-1 gap-1.5 text-sm">
            {brief.documents.map((d) => (
              <li key={d.id} className="flex justify-between gap-3">
                <span>{d.title}</span>
                <span className="tabular shrink-0 text-ink-3">{formatDate(d.date, "MMM d")}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}

      <footer className="border-t border-line bg-surface-2 px-6 py-3 text-xs text-ink-3 sm:px-8">
        Prepared with MedSpace from records the patient confirmed. Not medical advice.
      </footer>
    </article>
  );
}
