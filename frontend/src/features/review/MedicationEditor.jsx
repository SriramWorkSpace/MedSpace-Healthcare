import { useState } from "react";
import { useController, useWatch } from "react-hook-form";
import { motion } from "motion/react";
import { Eye, Plus, Trash, X } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { Field, Input } from "@/components/ui/Field";
import { formatClock } from "@/lib/format";
import { cn } from "@/lib/cn";
import { scheduleLabel } from "./mapping";

function ScheduleEditor({ control, index }) {
  const { field: times } = useController({ control, name: `medications.${index}.times` });
  const { field: asNeeded } = useController({ control, name: `medications.${index}.as_needed` });
  const period = useWatch({ control, name: `medications.${index}.period` });
  const [draft, setDraft] = useState("");

  const add = () => {
    if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(draft)) return;
    times.onChange([...new Set([...times.value, draft])].sort());
    setDraft("");
  };

  return (
    <div className="grid gap-2.5">
      <div className="flex items-center justify-between gap-3">
        <span className="field__label">Schedule</span>
        <label className="inline-flex cursor-pointer items-center gap-2 text-[13px] text-ink-2">
          <input
            type="checkbox"
            checked={asNeeded.value}
            onChange={(e) => asNeeded.onChange(e.target.checked)}
            className="size-4 accent-[var(--accent)]"
          />
          Only as needed
        </label>
      </div>
      {asNeeded.value ? (
        <p className="rounded-[var(--radius-control)] bg-surface-2 px-3 py-2.5 text-[13px] text-ink-2">
          As-needed medicines never get calendar reminders.
        </p>
      ) : (
        <div className="flex flex-wrap items-center gap-1.5">
          {times.value.map((t) => (
            <span key={t} className="chip chip--accent tabular gap-1 pr-1">
              {formatClock(t)}
              <button
                type="button"
                aria-label={`Remove ${formatClock(t)}`}
                onClick={() => times.onChange(times.value.filter((x) => x !== t))}
                className="grid size-4 place-items-center rounded-full hover:bg-[color-mix(in_oklch,var(--accent),transparent_80%)]"
              >
                <X size={10} weight="bold" />
              </button>
            </span>
          ))}
          <span className="inline-flex items-center gap-1">
            <input
              type="time"
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), add())}
              aria-label="Add a dose time"
              className="input h-7 w-[112px] px-2 text-xs"
            />
            <Button
              size="sm"
              variant="ghost"
              icon
              aria-label="Add dose time"
              onClick={add}
              className="!h-7 !w-7"
            >
              <Plus size={13} weight="bold" />
            </Button>
          </span>
        </div>
      )}
      {!asNeeded.value && (
        <p className="text-xs text-ink-3">
          {scheduleLabel({ times: times.value, as_needed: false, period })}
        </p>
      )}
    </div>
  );
}

export function MedicationEditor({ index, control, register, errors, onRemove, onCheckSource }) {
  const med = useWatch({ control, name: `medications.${index}` });
  const uncertain = new Set(med?.uncertain_fields ?? []);
  const confidence = Math.round((med?.confidence ?? 1) * 100);
  const lowConfidence = confidence < 85;
  const err = errors?.medications?.[index] ?? {};
  const attn = (f) => (uncertain.has(f) ? "input--attention" : undefined);

  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98, transition: { duration: 0.15 } }}
      transition={{ duration: 0.25, ease: [0.23, 1, 0.32, 1] }}
      className={cn("card card--flat p-5", lowConfidence && "ring-1 ring-warn/50")}
    >
      <div className="mb-4 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate font-semibold">{med?.name || "New medication"}</p>
          <p className="text-xs text-ink-3">
            {med?.frequency_raw ? (
              <>
                Written as <span className="font-mono text-ink-2">{med.frequency_raw}</span>
              </>
            ) : (
              "Added by you"
            )}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-1.5">
          <Chip tone={lowConfidence ? "warn" : "accent"} className="tabular">
            {confidence}%
          </Chip>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onCheckSource(med.source_page, med.name)}
            aria-label={`Show page ${med?.source_page} of the source`}
          >
            <Eye size={14} /> p.{med?.source_page}
          </Button>
          <Button variant="ghost" size="sm" icon aria-label="Remove medication" onClick={onRemove}>
            <Trash size={15} />
          </Button>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Medicine" error={err.name?.message}>
          <Input className={attn("name")} {...register(`medications.${index}.name`)} />
        </Field>
        <Field label="Strength" optional>
          <Input
            className={attn("strength")}
            placeholder="500 mg"
            {...register(`medications.${index}.strength`)}
          />
        </Field>
        <Field label="Form" optional>
          <Input placeholder="tablet, capsule, syrup" {...register(`medications.${index}.form`)} />
        </Field>
        <Field
          label="Frequency as written"
          optional
          hint="Kept for reference. The schedule below is what we use."
        >
          <Input
            className={cn("font-mono", attn("frequency_raw"))}
            {...register(`medications.${index}.frequency_raw`)}
          />
        </Field>
        <div className="sm:col-span-2">
          <ScheduleEditor control={control} index={index} />
        </div>
        <Field label="Start date" optional>
          <Input type="date" {...register(`medications.${index}.start_date`)} />
        </Field>
        <Field label="Duration (days)" optional hint="Leave blank if ongoing.">
          <Input
            type="number"
            min={1}
            max={3650}
            inputMode="numeric"
            className={attn("duration_raw")}
            {...register(`medications.${index}.duration_days`)}
          />
        </Field>
        <Field label="Instructions" optional className="sm:col-span-2">
          <Input
            placeholder="after food, with water"
            {...register(`medications.${index}.instructions`)}
          />
        </Field>
      </div>
    </motion.li>
  );
}
