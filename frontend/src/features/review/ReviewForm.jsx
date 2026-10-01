import { useFieldArray, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { AnimatePresence, motion } from "motion/react";
import { CheckCircle, Plus, Trash, Warning } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Field, Input, Select, Textarea } from "@/components/ui/Field";
import { MedicationEditor } from "./MedicationEditor";
import {
  CARE_KINDS,
  emptyCareAction,
  emptyMedication,
  formToConfirm,
  payloadToForm,
  reviewSchema,
} from "./mapping";

function Section({ title, description, action, children }) {
  return (
    <section className="grid gap-4">
      <div className="flex items-end justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>
          {description && <p className="text-sm text-ink-3">{description}</p>}
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

export function ReviewForm({ extraction, onConfirm, onDiscard, confirming, onCheckSource }) {
  const payload = extraction.payload;
  const form = useForm({
    resolver: zodResolver(reviewSchema),
    defaultValues: payloadToForm(payload),
    mode: "onBlur",
  });
  const { control, register, handleSubmit, formState, getValues } = form;
  const meds = useFieldArray({ control, name: "medications" });
  const actions = useFieldArray({ control, name: "care_actions" });
  const errors = formState.errors;
  const flagged = (payload.medications ?? []).filter(
    (m) => (m.confidence ?? 1) < 0.85 || m.uncertain_fields?.length,
  ).length;

  return (
    <form
      noValidate
      onSubmit={handleSubmit((values) => onConfirm(formToConfirm(values)))}
      className="grid gap-10 pb-28"
    >
      {payload.warnings?.length > 0 && (
        <div className="flex gap-3 rounded-card bg-warn-soft px-4 py-3.5 text-sm text-warn-ink">
          <Warning size={18} weight="fill" className="mt-0.5 shrink-0" />
          <div className="grid gap-1">
            {payload.warnings.map((w) => (
              <p key={w}>{w}</p>
            ))}
          </div>
        </div>
      )}

      {flagged > 0 && (
        <p className="flex items-center gap-2 text-sm text-ink-2">
          <span className="chip chip--warn">{flagged} to check</span>
          Highlighted fields were hard to read. Compare them with the source before confirming.
        </p>
      )}

      <Section title="Document details">
        <div className="card card--flat grid gap-4 p-5 sm:grid-cols-2">
          <Field label="Type">
            <Select {...register("document_kind")}>
              <option value="prescription">Prescription</option>
              <option value="lab_report">Lab report</option>
              <option value="other">Other document</option>
            </Select>
          </Field>
          <Field label="Date on the document" optional>
            <Input type="date" {...register("issued_on")} />
          </Field>
          <Field label="Prescriber" optional>
            <Input placeholder="Dr. ..." {...register("prescriber.name")} />
          </Field>
          <Field label="Specialty" optional>
            <Input {...register("prescriber.specialty")} />
          </Field>
          <Field label="Clinic" optional>
            <Input {...register("prescriber.clinic")} />
          </Field>
          <Field label="Follow-up date" optional>
            <Input type="date" {...register("follow_up.date")} />
          </Field>
          <Field
            label="Summary"
            optional
            className="sm:col-span-2"
            hint="A neutral description of what the document says."
          >
            <Textarea rows={2} {...register("summary")} />
          </Field>
        </div>
      </Section>

      <Section
        title="Medications"
        description={`${meds.fields.length} found. Edit anything that doesn't match the page.`}
        action={
          <Button
            variant="secondary"
            size="sm"
            onClick={() => meds.append(emptyMedication(getValues("issued_on")))}
          >
            <Plus size={14} weight="bold" /> Add
          </Button>
        }
      >
        {meds.fields.length === 0 ? (
          <p className="rounded-card border border-dashed border-line-strong px-5 py-8 text-center text-sm text-ink-2">
            No medications on this one. Lab reports and letters often have none.
          </p>
        ) : (
          <ul className="grid gap-4">
            <AnimatePresence initial={false}>
              {meds.fields.map((f, i) => (
                <MedicationEditor
                  key={f.id}
                  index={i}
                  control={control}
                  register={register}
                  errors={errors}
                  onRemove={() => meds.remove(i)}
                  onCheckSource={onCheckSource}
                />
              ))}
            </AnimatePresence>
          </ul>
        )}
      </Section>

      <Section
        title="To-dos and follow-ups"
        description="One-off actions. These can go to Google Tasks later."
        action={
          <Button variant="secondary" size="sm" onClick={() => actions.append(emptyCareAction())}>
            <Plus size={14} weight="bold" /> Add
          </Button>
        }
      >
        {actions.fields.length === 0 ? (
          <p className="rounded-card border border-dashed border-line-strong px-5 py-6 text-center text-sm text-ink-2">
            Nothing to follow up on.
          </p>
        ) : (
          <ul className="card card--flat divide-y divide-line">
            <AnimatePresence initial={false}>
              {actions.fields.map((f, i) => (
                <motion.li
                  key={f.id}
                  layout
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0, transition: { duration: 0.12 } }}
                  className="grid gap-3 p-4 sm:grid-cols-[1.6fr_1fr_0.9fr_auto] sm:items-end"
                >
                  <Field label="Task" error={errors.care_actions?.[i]?.title?.message}>
                    <Input {...register(`care_actions.${i}.title`)} />
                  </Field>
                  <Field label="Kind">
                    <Select {...register(`care_actions.${i}.kind`)}>
                      {CARE_KINDS.map((k) => (
                        <option key={k.value} value={k.value}>
                          {k.label}
                        </option>
                      ))}
                    </Select>
                  </Field>
                  <Field label="Due" optional>
                    <Input type="date" {...register(`care_actions.${i}.due_on`)} />
                  </Field>
                  <Button
                    variant="ghost"
                    size="sm"
                    icon
                    aria-label="Remove task"
                    onClick={() => actions.remove(i)}
                    className="justify-self-end sm:mb-1"
                  >
                    <Trash size={15} />
                  </Button>
                </motion.li>
              ))}
            </AnimatePresence>
          </ul>
        )}
      </Section>

      {/* Sticky action bar */}
      <div
        className="fixed inset-x-0 bottom-0 border-t border-line bg-[color-mix(in_oklch,var(--bg),transparent_10%)] backdrop-blur-md"
        style={{ zIndex: "var(--z-nav)" }}
      >
        <div className="mx-auto flex max-w-[1280px] items-center justify-between gap-3 px-4 py-3 sm:px-6">
          <p className="hidden text-sm text-ink-2 sm:block">
            Nothing is saved to your records until you confirm.
          </p>
          <div className="ml-auto flex gap-2">
            <Button variant="ghost" onClick={onDiscard} disabled={confirming}>
              Discard draft
            </Button>
            <Button type="submit" loading={confirming}>
              <CheckCircle size={16} weight="bold" /> Confirm records
            </Button>
          </div>
        </div>
      </div>
    </form>
  );
}
