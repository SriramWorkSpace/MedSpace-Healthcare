import { describe, expect, it } from "vitest";
import { daySummary, fillDays, percent } from "./states";

const doses = (...states) => states.map((state, i) => ({ time: `0${i}:00`, state }));

describe("daySummary", () => {
  it("never calls a day missed: unmarked doses stay unlogged", () => {
    expect(daySummary(doses("taken", "taken")).tone).toBe("taken");
    expect(daySummary(doses("taken", "unlogged"))).toEqual({ tone: "partial", taken: 1, total: 2 });
    expect(daySummary(doses("skipped")).tone).toBe("skipped");
    expect(daySummary(doses("skipped", "unlogged")).tone).toBe("unlogged");
  });

  it("ignores doses that are still to come today", () => {
    expect(daySummary(doses("taken", "upcoming"))).toEqual({ tone: "taken", taken: 1, total: 1 });
    expect(daySummary(doses("upcoming")).tone).toBe("upcoming");
  });
});

describe("fillDays", () => {
  it("covers every calendar day, attaching history where something was scheduled", () => {
    const filled = fillDays("2026-09-29", "2026-10-02", [{ date: "2026-10-01", doses: [] }]);
    expect(filled.map((d) => d.date)).toEqual([
      "2026-09-29",
      "2026-09-30",
      "2026-10-01",
      "2026-10-02",
    ]);
    expect(filled.filter((d) => d.entry).map((d) => d.date)).toEqual(["2026-10-01"]);
  });
});

it("formats rates", () => {
  expect(percent(0.837)).toBe("84%");
  expect(percent(null)).toBeNull();
});
