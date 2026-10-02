import { useLayoutEffect, useRef, useState } from "react";
import { formatDate } from "@/lib/format";
import { buildScale, linePath, niceTicks } from "./scale";
import { formatNumber } from "./format";

const PAD = { top: 18, right: 20, bottom: 30, left: 44 };

function useWidth() {
  const ref = useRef(null);
  const [width, setWidth] = useState(0);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const ro = new ResizeObserver(([entry]) => setWidth(Math.round(entry.contentRect.width)));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, width];
}

/**
 * Values over time with the report's printed range as a band. Pointer users get a hover readout;
 * everyone gets the same numbers in the results table beneath the chart.
 */
export function TrendChart({ points, refLow, refHigh, unit, label }) {
  const [wrapRef, width] = useWidth();
  const [hover, setHover] = useState(null);
  const height = width < 480 ? 200 : 248;

  const first = points[0];
  const last = points.at(-1);
  const summary = `${label}: ${points.length} results from ${formatDate(first.collected_on)} to ${formatDate(
    last.collected_on,
  )}. Latest ${formatNumber(last.value)}${unit ? ` ${unit}` : ""}.`;

  let chart = null;
  if (width > 0) {
    const { coords, band, y, lo, hi } = buildScale(points, refLow, refHigh, {
      width,
      height,
      pad: PAD,
    });
    const ticks = niceTicks(lo, hi);
    // Show at most ~5 date labels so they never collide.
    const every = Math.max(1, Math.ceil(coords.length / Math.max(2, Math.floor(width / 120))));
    const active = hover == null ? null : coords[hover];

    chart = (
      <svg
        width={width}
        height={height}
        role="img"
        aria-label={summary}
        className="block overflow-visible"
        onPointerLeave={() => setHover(null)}
      >
        {ticks.map((t) => (
          <g key={t}>
            <line
              x1={PAD.left}
              x2={width - PAD.right}
              y1={y(t)}
              y2={y(t)}
              stroke="var(--line)"
              strokeWidth={1}
            />
            <text
              x={PAD.left - 10}
              y={y(t)}
              dy="0.32em"
              textAnchor="end"
              className="tabular fill-ink-3 text-[11px]"
            >
              {formatNumber(t)}
            </text>
          </g>
        ))}

        {band && (
          <g>
            <rect
              x={PAD.left}
              y={band.top}
              width={width - PAD.left - PAD.right}
              height={Math.max(0, band.bottom - band.top)}
              fill="var(--accent-soft)"
              opacity={0.75}
            />
            <text
              x={width - PAD.right - 6}
              y={band.top + 14}
              textAnchor="end"
              className="fill-accent-soft-ink text-[11px] font-medium"
            >
              Printed range
            </text>
          </g>
        )}

        {/* CSS draw-in (pathLength="1" normalizes the dash), off the main thread. */}
        <path
          d={linePath(coords)}
          pathLength={1}
          className="trend-line"
          fill="none"
          stroke="var(--accent)"
          strokeWidth={2.25}
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {coords.map((c, i) => {
          const flagged = c.flag === "high" || c.flag === "low";
          return (
            <g key={`${c.collected_on}-${i}`}>
              {i % every === 0 || i === coords.length - 1 ? (
                <text
                  x={c.x}
                  y={height - 8}
                  textAnchor={coords.length === 1 ? "middle" : i === 0 ? "start" : "end"}
                  className="tabular fill-ink-3 text-[11px]"
                >
                  {formatDate(c.collected_on, "MMM yyyy")}
                </text>
              ) : null}
              <circle
                cx={c.x}
                cy={c.y}
                r={hover === i ? 6 : 4.5}
                className="trend-dot"
                style={{ animationDelay: `${350 + i * 60}ms` }}
                fill={flagged ? "var(--warn)" : "var(--surface)"}
                stroke={flagged ? "var(--warn-ink)" : "var(--accent)"}
                strokeWidth={2}
              />
              {/* Generous invisible hit target for the pointer readout. */}
              <rect
                x={c.x - 18}
                y={PAD.top}
                width={36}
                height={height - PAD.top - PAD.bottom}
                fill="transparent"
                onPointerEnter={() => setHover(i)}
              />
            </g>
          );
        })}

        {active && (
          <g pointerEvents="none">
            <line
              x1={active.x}
              x2={active.x}
              y1={PAD.top}
              y2={height - PAD.bottom}
              stroke="var(--line-strong)"
              strokeDasharray="3 3"
            />
            <foreignObject
              x={Math.min(Math.max(active.x - 70, 0), width - 140)}
              y={Math.max(active.y - 58, 0)}
              width={140}
              height={46}
            >
              <div className="rounded-[var(--radius-control)] border border-line bg-surface px-2.5 py-1.5 text-center shadow-sm">
                <p className="tabular text-sm font-semibold">
                  {formatNumber(active.value)}
                  {unit && <span className="font-normal text-ink-3"> {unit}</span>}
                </p>
                <p className="text-[11px] text-ink-3">{formatDate(active.collected_on)}</p>
              </div>
            </foreignObject>
          </g>
        )}
      </svg>
    );
  }

  return (
    <div ref={wrapRef} style={{ height }} className="w-full">
      {chart}
    </div>
  );
}
