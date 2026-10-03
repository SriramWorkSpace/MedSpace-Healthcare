import { describe, expect, it } from "vitest";
import { evidenceKeys, findSpot, itemName } from "./evidence";

const values = {
  "medications.0._ev": "medications.1", // the reader's first medicine was removed while reviewing
  "medications.0": { name: "Metformin" },
  "medications.1._ev": undefined, // added by the user
  "lab_results.0._ev": "lab_results.0",
  "lab_results.0": { name: "HbA1c" },
};
const getValues = (path) => values[path];

const evidence = {
  fields: {
    "medications.1.strength": { page: 1, boxes: [[0.1, 0.2, 0.3, 0.25]] },
    "prescriber.name": { page: 1, boxes: [[0.1, 0.05, 0.4, 0.08]] },
  },
  items: {
    "medications.1": { page: 1, boxes: [[0.05, 0.2, 0.9, 0.25]] },
    prescriber: { page: 1, boxes: [[0.05, 0.02, 0.6, 0.1]] },
  },
};

describe("evidence lookups", () => {
  it("follows an item's original position, not its current index", () => {
    const keys = evidenceKeys("medications.0.strength", getValues);
    expect(keys).toEqual({ field: "medications.1.strength", item: "medications.1" });
    expect(findSpot(evidence, keys)).toBe(evidence.fields["medications.1.strength"]);
  });

  it("falls back to the whole line when the field itself wasn't found", () => {
    const keys = evidenceKeys("medications.0.times.0", getValues);
    expect(keys.field).toBe("medications.1.times");
    expect(findSpot(evidence, keys)).toBe(evidence.items["medications.1"]);
  });

  it("has nothing for items the reader didn't produce", () => {
    expect(evidenceKeys("medications.1.name", getValues)).toBeNull();
    expect(findSpot(evidence, null)).toBeNull();
  });

  it("maps top-level fields directly, with the letterhead as the prescriber item", () => {
    expect(evidenceKeys("prescriber.clinic", getValues)).toEqual({
      field: "prescriber.clinic",
      item: "prescriber",
    });
    expect(findSpot(evidence, evidenceKeys("prescriber.clinic", getValues))).toBe(
      evidence.items.prescriber,
    );
    expect(evidenceKeys("issued_on", getValues)).toEqual({ field: "issued_on", item: null });
  });

  it("names the item a field belongs to", () => {
    expect(itemName("lab_results.0.value", getValues)).toBe("HbA1c");
    expect(itemName("issued_on", getValues)).toBe("");
  });
});
