import { describe, expect, it } from "vitest";
import { firstName, formatBytes, formatClock, formatDate, greeting } from "./format";

describe("format helpers", () => {
  it("formats 24h clock strings for humans", () => {
    expect(formatClock("08:00")).toBe("8:00 AM");
    expect(formatClock("20:30")).toBe("8:30 PM");
    expect(formatClock("00:05")).toBe("12:05 AM");
    expect(formatClock("12:00")).toBe("12:00 PM");
  });

  it("formats ISO strings, Dates and epoch milliseconds alike", () => {
    const ms = new Date(2026, 9, 3, 15, 40).getTime();
    expect(formatDate("2026-10-03")).toBe("Oct 3, 2026");
    expect(formatDate(new Date(ms), "h:mm a")).toBe("3:40 PM");
    expect(formatDate(ms, "h:mm a, MMM d")).toBe("3:40 PM, Oct 3");
  });

  it("formats byte sizes", () => {
    expect(formatBytes(512)).toBe("512 B");
    expect(formatBytes(2048)).toBe("2.0 KB");
    expect(formatBytes(5 * 1024 * 1024)).toBe("5.0 MB");
  });

  it("greets by time of day", () => {
    expect(greeting(new Date(2026, 0, 1, 9))).toBe("Good morning");
    expect(greeting(new Date(2026, 0, 1, 15))).toBe("Good afternoon");
    expect(greeting(new Date(2026, 0, 1, 21))).toBe("Good evening");
    expect(greeting(new Date(2026, 0, 1, 2))).toBe("Burning the midnight oil");
  });

  it("extracts a first name", () => {
    expect(firstName("  Noor  Haddad ")).toBe("Noor");
  });
});
