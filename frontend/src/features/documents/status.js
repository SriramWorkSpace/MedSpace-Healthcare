export const STATUS_META = {
  queued: { label: "Queued", tone: "neutral", live: true },
  processing: { label: "Reading", tone: "warn", live: true },
  needs_review: { label: "Needs review", tone: "warn", live: false },
  confirmed: { label: "Confirmed", tone: "accent", live: false },
  failed: { label: "Needs attention", tone: "danger", live: false },
};

export const KIND_LABEL = {
  prescription: "Prescription",
  lab_report: "Lab report",
  other: "Document",
};

export const FILTERS = [
  { key: "all", label: "All" },
  { key: "needs_review", label: "Needs review" },
  { key: "confirmed", label: "Confirmed" },
  { key: "processing", label: "Processing", statuses: ["queued", "processing"] },
  { key: "failed", label: "Failed" },
];
