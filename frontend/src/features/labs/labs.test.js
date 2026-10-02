import { describe, expect, it } from "vitest";
import { describeChange, formatNumber } from "./format";
import { buildScale, niceTicks } from "./scale";

const r = (value, collected_on, unit = "mg/dL") => ({
  value,
  value_text: String(value),
  unit,
  collected_on,
});

describe("describeChange", () => {
  it("states direction and size, never good or bad", () => {
    expect(describeChange(r(138, "2026-08-16"), r(149, "2026-02-13"))).toBe(
      "Down 11 mg/dL since Feb 13, 2026",
    );
    expect(describeChange(r(6.8, "2026-09-11", "%"), r(6.1, "2026-03-12", "%"))).toBe(
      "Up 0.7 % since Mar 12, 2026",
    );
  });

  it("stays quiet when results cannot be compared", () => {
    expect(describeChange(r(138, "2026-08-16"), null)).toBeNull();
    expect(describeChange(r(3.6, "2026-08-16", "mmol/L"), r(149, "2026-02-13"))).toBeNull();
    expect(
      describeChange({ ...r(null, "2026-08-16"), value: null }, r(1, "2026-01-01")),
    ).toBeNull();
  });
});

describe("chart scale", () => {
  const pad = { top: 0, right: 0, bottom: 0, left: 0 };
  const points = [
    { value: 158, collected_on: "2025-08-16" },
    { value: 138, collected_on: "2026-08-16" },
  ];

  it("keeps the printed range inside the domain so the band is visible", () => {
    const { lo, hi, band } = buildScale(points, null, 130, { width: 100, height: 100, pad });
    expect(lo).toBeLessThan(130);
    expect(hi).toBeGreaterThan(158);
    expect(band.bottom).toBe(100); // a "< 130" band runs from the bottom of the chart
    expect(band.top).toBeGreaterThan(0);
  });

  it("maps dates to real time and handles a single point", () => {
    const { coords } = buildScale(points, null, null, { width: 100, height: 100, pad });
    expect(coords[0].x).toBe(0);
    expect(coords[1].x).toBe(100);
    const single = buildScale(points.slice(0, 1), null, null, { width: 100, height: 100, pad });
    expect(single.coords[0].x).toBeCloseTo(50);
    expect(Number.isFinite(single.coords[0].y)).toBe(true);
  });

  it("produces round ticks", () => {
    expect(niceTicks(100, 180)).toEqual([100, 120, 140, 160, 180]);
    expect(formatNumber(0.1 + 0.2)).toBe("0.3");
  });
});
