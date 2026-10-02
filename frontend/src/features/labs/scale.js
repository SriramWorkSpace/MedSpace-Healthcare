/**
 * Shared geometry for the sparkline and the trend chart. Dates map to real time (uneven gaps stay
 * uneven) and the value domain always includes the printed range so the band is visible.
 */
const DAY = 86_400_000;

export function buildScale(points, refLow, refHigh, { width, height, pad }) {
  const times = points.map((p) => new Date(`${p.collected_on}T00:00:00`).getTime());
  const values = points.map((p) => p.value);
  const bounds = [...values, refLow, refHigh].filter((v) => v != null);
  let lo = Math.min(...bounds);
  let hi = Math.max(...bounds);
  if (hi - lo < 1e-9) {
    lo -= Math.abs(lo) * 0.1 || 1;
    hi += Math.abs(hi) * 0.1 || 1;
  }
  const span = hi - lo;
  lo = Math.max(0, lo - span * 0.18);
  hi += span * 0.18;

  let t0 = Math.min(...times);
  let t1 = Math.max(...times);
  if (t1 - t0 < DAY) {
    t0 -= 15 * DAY;
    t1 += 15 * DAY;
  }

  const x = (t) => pad.left + ((t - t0) / (t1 - t0)) * (width - pad.left - pad.right);
  const y = (v) => pad.top + (1 - (v - lo) / (hi - lo)) * (height - pad.top - pad.bottom);
  const coords = points.map((p, i) => ({ ...p, x: x(times[i]), y: y(p.value) }));

  const bandTop = y(Math.min(refHigh ?? hi, hi));
  const bandBottom = y(Math.max(refLow ?? lo, lo));
  const band = refLow != null || refHigh != null ? { top: bandTop, bottom: bandBottom } : null;

  return { coords, band, x, y, lo, hi, t0, t1 };
}

export function linePath(coords) {
  return coords.map((c, i) => `${i ? "L" : "M"}${c.x.toFixed(1)},${c.y.toFixed(1)}`).join(" ");
}

/** Up to `count` evenly spaced, rounded tick values inside [lo, hi]. */
export function niceTicks(lo, hi, count = 4) {
  const raw = (hi - lo) / count;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) ?? raw;
  const ticks = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) ticks.push(v);
  return ticks;
}
