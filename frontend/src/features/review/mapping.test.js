import { describe, expect, it } from "vitest";
import { formToConfirm, payloadToForm, reviewSchema, scheduleLabel } from "./mapping";

const payload = {
  document_type: "prescription",
  issued_on: "2026-03-04",
  prescriber: {
    name: "Dr. Imani Oduya",
    specialty: "Internal Medicine",
    clinic: null,
    contact: null,
  },
  follow_up: { date: "2026-03-18", notes: "Review in 2 weeks" },
  summary: "Prescription with 2 medications.",
  medications: [
    {
      name: "Amoxicillin",
      strength: "500 mg",
      form: "capsule",
      frequency_raw: "1-0-1",
      duration_days: 7,
      instructions: "after food",
      source_page: 1,
      confidence: 0.9,
      uncertain_fields: [],
      schedule: {
        times: ["20:00", "08:00"],
        period: "daily",
        as_needed: false,
        label: "Twice daily",
      },
    },
    {
      name: "Ibuprofen",
      strength: "400 mg",
      frequency_raw: "SOS",
      source_page: 1,
      schedule: { times: [], period: "as_needed", as_needed: true, label: "As needed" },
    },
  ],
  care_actions: [
    { kind: "lab_test", title: "Get CBC test", due_on: null, notes: null, source_page: 1 },
  ],
  diet_notes: [{ text: "Avoid alcohol.", category: "avoid", source_page: 1, confidence: 0.9 }],
};

describe("review mapping", () => {
  it("round-trips an extraction into a confirm body", () => {
    const form = payloadToForm(payload);
    expect(reviewSchema.safeParse(form).success).toBe(true);
    expect(form.medications[0].start_date).toBe("2026-03-04");

    const body = formToConfirm(form);
    expect(body.prescriber).toEqual({
      name: "Dr. Imani Oduya",
      specialty: "Internal Medicine",
      clinic: null,
      contact: null,
    });
    expect(body.medications[0].schedule.times).toEqual(["08:00", "20:00"]);
    expect(body.medications[0].duration_days).toBe(7);
    expect(body.medications[1].schedule).toMatchObject({
      as_needed: true,
      times: [],
      period: "as_needed",
    });
    expect(body.care_actions[0].due_on).toBeNull();
    expect(body.diet_notes).toEqual([
      { text: "Avoid alcohol.", category: "avoid", source_page: 1, source_ref: "diet_notes.0" },
    ]);
    // Each record remembers which item of the reading it came from (for highlights).
    expect(body.medications.map((m) => m.source_ref)).toEqual(["medications.0", "medications.1"]);
    expect(body.care_actions[0].source_ref).toBe("care_actions.0");
  });

  it("keeps original positions through validation, and none for added items", () => {
    const form = payloadToForm(payload);
    form.medications.splice(0, 1); // the reviewer removed the first medicine
    form.medications.push({ ...form.medications[0], _ev: undefined, name: "Added" });
    const parsed = reviewSchema.parse(form);
    expect(formToConfirm(parsed).medications.map((m) => m.source_ref)).toEqual([
      "medications.1",
      null,
    ]);
  });

  it("nulls out an empty prescriber and follow-up", () => {
    const body = formToConfirm(payloadToForm({ medications: [] }));
    expect(body.prescriber).toBeNull();
    expect(body.follow_up).toBeNull();
  });

  it("labels schedules from the chosen times", () => {
    expect(scheduleLabel({ times: ["08:00", "14:00", "20:00"], period: "daily" })).toBe(
      "Three times daily",
    );
    expect(scheduleLabel({ times: [], as_needed: true })).toBe("As needed");
    expect(scheduleLabel({ times: ["08:00"], period: "weekly" })).toBe("Once a week");
  });

  it("rejects malformed times", () => {
    const form = payloadToForm(payload);
    form.medications[0].times = ["8am"];
    expect(reviewSchema.safeParse(form).success).toBe(false);
  });
});
