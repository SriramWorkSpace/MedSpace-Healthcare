import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { flushSync } from "react-dom";

const ThemeContext = createContext(null);
const STORAGE_KEY = "ms-theme";

function systemTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function ThemeProvider({ children }) {
  const [preference, setPreference] = useState(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) ?? "system";
    } catch {
      return "system";
    }
  });
  const [system, setSystem] = useState(systemTheme);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => setSystem(mq.matches ? "dark" : "light");
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  const resolved = preference === "system" ? system : preference;

  useEffect(() => {
    document.documentElement.dataset.theme = resolved;
  }, [resolved]);

  const setTheme = useCallback((next) => {
    setPreference(next);
    try {
      if (next === "system") localStorage.removeItem(STORAGE_KEY);
      else localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* storage unavailable: keep in memory */
    }
  }, []);

  /**
   * Switch theme. Given an origin (the toggle's centre and radius), the new theme is revealed as
   * a circle growing out of the toggle, via the View Transitions API. Falls back to an instant
   * switch. A strong ease-out makes the first frames grow fast right at the toggle, so the reveal
   * reads as coming from it; ease-in-out kept it hidden under the button and the visible sweep
   * happened far away, in the screen's corners.
   */
  const toggle = useCallback(
    (origin) => {
      const next = resolved === "dark" ? "light" : "dark";
      const apply = () => {
        document.documentElement.dataset.theme = next;
        flushSync(() => setTheme(next));
      };
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!origin || reduce || typeof document.startViewTransition !== "function") {
        apply();
        return;
      }

      const root = document.documentElement;
      root.classList.add("theme-switching"); // no colour cross-fades inside the snapshot
      const transition = document.startViewTransition(apply);
      const { x, y, r = 0 } = origin;
      const radius = Math.hypot(
        Math.max(x, window.innerWidth - x),
        Math.max(y, window.innerHeight - y),
      );
      transition.ready
        .then(() =>
          root.animate(
            {
              clipPath: [`circle(${r}px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`],
            },
            {
              duration: 500,
              easing: "cubic-bezier(0.23, 1, 0.32, 1)",
              pseudoElement: "::view-transition-new(root)",
            },
          ),
        )
        .catch(() => {});
      transition.finished.finally(() => root.classList.remove("theme-switching"));
    },
    [resolved, setTheme],
  );

  const value = useMemo(
    () => ({ preference, resolved, setTheme, toggle }),
    [preference, resolved, setTheme, toggle],
  );
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used inside <ThemeProvider>");
  return ctx;
}
