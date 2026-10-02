import { buildScale, linePath } from "./scale";

const W = 120;
const H = 40;
const PAD = { top: 5, right: 5, bottom: 5, left: 5 };

/** Decorative mini trend for a card; the card text carries the actual numbers. */
export function Sparkline({ points, refLow, refHigh }) {
  if (points.length < 2) return null;
  const { coords, band } = buildScale(points, refLow, refHigh, { width: W, height: H, pad: PAD });
  const last = coords.at(-1);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H} aria-hidden="true" className="shrink-0">
      {band && (
        <rect
          x={0}
          y={band.top}
          width={W}
          height={Math.max(0, band.bottom - band.top)}
          rx={4}
          fill="var(--accent-soft)"
        />
      )}
      <path
        d={linePath(coords)}
        fill="none"
        stroke="var(--accent)"
        strokeWidth={1.75}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle
        cx={last.x}
        cy={last.y}
        r={3}
        fill={last.flag === "high" || last.flag === "low" ? "var(--warn)" : "var(--accent)"}
        stroke="var(--surface)"
        strokeWidth={1.5}
      />
    </svg>
  );
}
