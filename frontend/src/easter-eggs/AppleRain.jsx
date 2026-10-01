import { useEffect, useState } from "react";
import { useReducedMotion } from "motion/react";
import { createPortal } from "react-dom";

const DURATION = 4200;

function makeApples(count) {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    delay: Math.random() * 1400,
    duration: 1800 + Math.random() * 1600,
    size: 18 + Math.random() * 22,
    spin: (Math.random() - 0.5) * 720,
    emoji: Math.random() > 0.85 ? "🍏" : "🍎",
  }));
}

/** A short, non-blocking shower of apples. Purely decorative: aria-hidden, pointer-events none. */
export default function AppleRain({ onDone }) {
  const reduce = useReducedMotion();
  const [apples] = useState(() => makeApples(reduce ? 0 : 42));

  useEffect(() => {
    const t = setTimeout(onDone, reduce ? 0 : DURATION);
    return () => clearTimeout(t);
  }, [onDone, reduce]);

  return createPortal(
    <div
      aria-hidden
      className="pointer-events-none fixed inset-0 overflow-hidden"
      style={{ zIndex: "var(--z-egg)" }}
    >
      {apples.map((a) => (
        <span
          key={a.id}
          className="absolute -top-12 select-none"
          style={{
            left: `${a.left}%`,
            fontSize: a.size,
            animation: `apple-fall ${a.duration}ms cubic-bezier(0.55, 0, 0.75, 0.4) ${a.delay}ms forwards`,
            "--spin": `${a.spin}deg`,
          }}
        >
          {a.emoji}
        </span>
      ))}
      <style>{`
        @keyframes apple-fall {
          to { transform: translateY(calc(100dvh + 80px)) rotate(var(--spin)); }
        }
      `}</style>
    </div>,
    document.body,
  );
}
