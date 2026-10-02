import { expect, it } from "vitest";
import { clinicianFrom } from "./clinician";

it("reads the clinician from an appointment title", () => {
  expect(clinicianFrom("Follow-up with Dr. Imani Oduya")).toBe("Dr. Imani Oduya");
  expect(clinicianFrom("Follow-up visit")).toBeNull();
  expect(clinicianFrom(undefined)).toBeNull();
});
