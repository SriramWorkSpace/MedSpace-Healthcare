import { z } from "zod";

const TIME = /^([01]\d|2[0-3]):[0-5]\d$/;
const blank = (v) => (v === "" || v === undefined ? null : v);
const num = (v) =>
  v === "" || v === null || v === undefined || Number.isNaN(Number(v)) ? null : Number(v);

export const DIET_CATEGORIES = [
  { value: "avoid", label: "Avoid" },
  { value: "limit", label: "Limit" },
  { value: "include", label: "Include" },
  { value: "timing", label: "Timing" },
  { value: "general", label: "General" },
];

export const CARE_KINDS = [
  { value: "follow_up", label: "Follow-up visit" },
  { value: "lab_test", label: "Lab test" },
  { value: "course_completion", label: "Finish a course" },
  { value: "upload_report", label: "Upload a report" },
  { value: "prepare_documents", label: "Prepare documents" },
  { value: "other", label: "Other" },
];

export const reviewSchema = z.object({
  document_kind: z.enum(["prescription", "lab_report", "other"]),
  issued_on: z.string().optional(),
  prescriber: z.object({
    name: z.string().max(120).optional(),
    specialty: z.string().max(120).optional(),
    clinic: z.string().max(160).optional(),
    contact: z.string().max(160).optional(),
  }),
  follow_up: z.object({ date: z.string().optional(), notes: z.string().max(500).optional() }),
  summary: z.string().max(2000).optional(),
  medications: z.array(
    z.object({
      name: z.string().trim().min(1, "Name is required").max(120),
      strength: z.string().max(60).optional(),
      form: z.string().max(40).optional(),
      dose: z.string().max(60).optional(),
      route: z.string().max(40).optional(),
      frequency_raw: z.string().max(120).optional(),
      times: z.array(z.string().regex(TIME, "Use HH:MM")),
      as_needed: z.boolean(),
      period: z.string(),
      label: z.string().optional(),
      interval_hours: z.any().optional(),
      duration_days: z.union([z.string(), z.number()]).optional(),
      start_date: z.string().optional(),
      instructions: z.string().max(500).optional(),
      source_page: z.number(),
      _ev: z.string().optional(),
      confidence: z.number().optional(),
      uncertain_fields: z.array(z.string()).optional(),
      needs_attention: z.boolean().optional(),
    }),
  ),
  care_actions: z.array(
    z.object({
      kind: z.string(),
      title: z.string().trim().min(1, "Give this task a title").max(200),
      due_on: z.string().optional(),
      notes: z.string().max(500).optional(),
      source_page: z.number().nullable().optional(),
      _ev: z.string().optional(),
    }),
  ),
  diet_notes: z.array(
    z.object({
      text: z.string().trim().min(1, "Write the note or remove it").max(300),
      category: z.enum(["avoid", "limit", "include", "timing", "general"]),
      source_page: z.number().nullable().optional(),
      _ev: z.string().optional(),
    }),
  ),
  lab_results: z.array(
    z.object({
      name: z.string().trim().min(1, "Name the test or remove it").max(120),
      value: z.string().trim().min(1, "Enter the result as printed").max(40),
      unit: z.string().max(30).optional(),
      ref_range: z.string().max(60).optional(),
      flag: z.enum(["high", "low", "normal"]).nullable().optional(),
      source_page: z.number().nullable().optional(),
      _ev: z.string().optional(),
    }),
  ),
});

/** Extraction payload -> form values (strings for inputs, never null). */
export function payloadToForm(payload) {
  const p = payload ?? {};
  return {
    document_kind: p.document_type ?? "prescription",
    issued_on: p.issued_on ?? "",
    prescriber: {
      name: p.prescriber?.name ?? "",
      specialty: p.prescriber?.specialty ?? "",
      clinic: p.prescriber?.clinic ?? "",
      contact: p.prescriber?.contact ?? "",
    },
    follow_up: { date: p.follow_up?.date ?? "", notes: p.follow_up?.notes ?? "" },
    summary: p.summary ?? "",
    medications: (p.medications ?? []).map((m, i) => ({
      _ev: `medications.${i}`,
      name: m.name ?? "",
      strength: m.strength ?? "",
      form: m.form ?? "",
      dose: m.dose ?? "",
      route: m.route ?? "",
      frequency_raw: m.frequency_raw ?? "",
      times: m.schedule?.times ?? [],
      as_needed: m.schedule?.as_needed ?? m.as_needed ?? false,
      period: m.schedule?.period ?? "daily",
      label: m.schedule?.label ?? "",
      interval_hours: m.schedule?.interval_hours ?? null,
      needs_attention: m.schedule?.needs_attention ?? false,
      duration_days: m.duration_days ?? "",
      start_date: p.issued_on ?? "",
      instructions: m.instructions ?? "",
      source_page: m.source_page ?? 1,
      confidence: m.confidence ?? 1,
      uncertain_fields: m.uncertain_fields ?? [],
    })),
    care_actions: (p.care_actions ?? []).map((a, i) => ({
      _ev: `care_actions.${i}`,
      kind: a.kind ?? "other",
      title: a.title ?? "",
      due_on: a.due_on ?? "",
      notes: a.notes ?? "",
      source_page: a.source_page ?? null,
    })),
    diet_notes: (p.diet_notes ?? []).map((n, i) => ({
      _ev: `diet_notes.${i}`,
      text: n.text ?? "",
      category: n.category ?? "general",
      source_page: n.source_page ?? null,
    })),
    lab_results: (p.lab_results ?? []).map((r, i) => ({
      _ev: `lab_results.${i}`,
      name: r.name ?? "",
      value: r.value ?? "",
      unit: r.unit ?? "",
      ref_range: r.ref_range ?? "",
      flag: r.flag ?? null,
      source_page: r.source_page ?? null,
    })),
  };
}

export function emptyMedication(issuedOn = "") {
  return {
    name: "",
    strength: "",
    form: "",
    dose: "",
    route: "",
    frequency_raw: "",
    times: ["08:00"],
    as_needed: false,
    period: "daily",
    label: "Once daily",
    interval_hours: null,
    needs_attention: false,
    duration_days: "",
    start_date: issuedOn,
    instructions: "",
    source_page: 1,
    confidence: 1,
    uncertain_fields: [],
  };
}

export function emptyCareAction() {
  return { kind: "other", title: "", due_on: "", notes: "", source_page: null };
}

export function emptyDietNote() {
  return { text: "", category: "general", source_page: null };
}

export function emptyLabResult() {
  return { name: "", value: "", unit: "", ref_range: "", flag: null, source_page: null };
}

/** Form values -> ConfirmIn body for POST /api/extractions/{id}/confirm. */
export function formToConfirm(v) {
  const prescriber = Object.fromEntries(
    Object.entries(v.prescriber).map(([k, val]) => [k, blank(val?.trim?.() ?? val)]),
  );
  const hasPrescriber = Object.values(prescriber).some(Boolean);
  return {
    document_kind: v.document_kind,
    issued_on: blank(v.issued_on),
    prescriber: hasPrescriber ? prescriber : null,
    follow_up:
      v.follow_up.date || v.follow_up.notes
        ? { date: blank(v.follow_up.date), notes: blank(v.follow_up.notes) }
        : null,
    summary: blank(v.summary),
    medications: v.medications.map((m) => ({
      name: m.name.trim(),
      strength: blank(m.strength),
      form: blank(m.form),
      dose: blank(m.dose),
      route: blank(m.route),
      frequency_raw: blank(m.frequency_raw),
      schedule: {
        times: m.as_needed ? [] : [...new Set(m.times)].sort(),
        period: m.as_needed
          ? "as_needed"
          : m.period === "unknown" || m.period === "as_needed"
            ? "daily"
            : m.period,
        as_needed: m.as_needed,
        interval_hours: num(m.interval_hours),
        label: scheduleLabel(m),
        needs_attention: false,
      },
      start_date: blank(m.start_date),
      duration_days: num(m.duration_days),
      instructions: blank(m.instructions),
      source_page: m.source_page,
      source_ref: m._ev ?? null,
    })),
    care_actions: v.care_actions.map((a) => ({
      kind: a.kind,
      title: a.title.trim(),
      due_on: blank(a.due_on),
      notes: blank(a.notes),
      source_page: a.source_page ?? null,
      source_ref: a._ev ?? null,
    })),
    diet_notes: (v.diet_notes ?? []).map((n) => ({
      text: n.text.trim(),
      category: n.category,
      source_page: n.source_page ?? null,
      source_ref: n._ev ?? null,
    })),
    lab_results: (v.lab_results ?? []).map((r) => ({
      name: r.name.trim(),
      value: r.value.trim(),
      unit: blank(r.unit?.trim()),
      ref_range: blank(r.ref_range?.trim()),
      flag: r.flag ?? null,
      source_page: r.source_page ?? null,
      source_ref: r._ev ?? null,
    })),
  };
}

export function scheduleLabel(m) {
  if (m.as_needed) return "As needed";
  const n = new Set(m.times).size;
  if (m.period === "weekly") return "Once a week";
  if (m.period === "alternate_days") return "Every other day";
  if (m.period === "interval" && m.interval_hours) return `Every ${m.interval_hours} hours`;
  return (
    ["No doses set", "Once daily", "Twice daily", "Three times daily", "Four times daily"][n] ??
    `${n} times daily`
  );
}
