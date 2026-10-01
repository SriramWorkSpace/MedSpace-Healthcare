import { describe, expect, it } from "vitest";
import { firstName, formatBytes, formatClock, greeting } from "./format";

describe("format helpers", () => {
  it("formats 24h clock strings for humans", () => {
    expect(formatClock("08:00")).toBe("8:00 AM");
    expect(formatClock("20:30")).toBe("8:30 PM");
    expect(formatClock("00:05")).toBe("12:05 AM");
    expect(formatClock("12:00")).toBe("12:00 PM");
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
