import {
  createContext,
  lazy,
  Suspense,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { toast } from "sonner";

const AppleRain = lazy(() => import("./AppleRain"));

/** Every egg, with the message shown the first time it is found. */
export const EGGS = {
  konami: "An apple a day keeps the doctor away. Here's a whole orchard.",
  apple: "You typed the magic word. Fresh apples, delivered.",
  logo: "Doctor's orders: stop clicking, stretch your wrists, drink some water.",
  notFound: "You found a page that doesn't exist. That's a rare diagnosis.",
  themeFlip: "Feeling a little light-headed? Too much theme switching.",
};
const TOTAL = Object.keys(EGGS).length;
const STORAGE_KEY = "ms-eggs";
const KONAMI = [
  "ArrowUp",
  "ArrowUp",
  "ArrowDown",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "ArrowLeft",
  "ArrowRight",
  "b",
  "a",
];

const EggContext = createContext({ discover: () => {}, found: [] });

function loadFound() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
  } catch {
    return [];
  }
}

function isTyping(target) {
  return target?.closest?.("input, textarea, select, [contenteditable='true']");
}

export function EasterEggProvider({ children }) {
  const [found, setFound] = useState(loadFound);
  const [raining, setRaining] = useState(false);
  const foundRef = useRef(found);

  const discover = useCallback((id, { rain = false } = {}) => {
    if (rain) setRaining(true);
    if (foundRef.current.includes(id)) return;
    const next = [...foundRef.current, id];
    foundRef.current = next;
    setFound(next);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      /* ignore */
    }
    toast(EGGS[id], {
      description: `Easter egg ${next.length} of ${TOTAL} found.`,
      duration: 6000,
    });
  }, []);

  // Konami code and the typed word "apple".
  useEffect(() => {
    let konami = 0;
    let typed = "";
    function onKey(e) {
      if (isTyping(e.target) || e.metaKey || e.ctrlKey || e.altKey) return;
      const key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
      konami = key === KONAMI[konami] ? konami + 1 : key === KONAMI[0] ? 1 : 0;
      if (konami === KONAMI.length) {
        konami = 0;
        discover("konami", { rain: true });
      }
      if (key.length === 1) {
        typed = (typed + key).slice(-5);
        if (typed === "apple") discover("apple", { rain: true });
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [discover]);

  // A friendly note for anyone opening devtools.
  useEffect(() => {
    if (import.meta.env.MODE === "test") return;
    console.log(
      "%c MedSpace %c Looking under the hood? We appreciate a thorough examination.\nSource: https://github.com/SriramWorkSpace/MedSpace-Healthcare",
      "background:#1f7a5c;color:#f4fbf7;border-radius:6px;padding:3px 6px;font-weight:600",
      "color:inherit",
    );
  }, []);

  const value = useMemo(() => ({ discover, found, total: TOTAL }), [discover, found]);

  return (
    <EggContext.Provider value={value}>
      {children}
      {raining && (
        <Suspense fallback={null}>
          <AppleRain onDone={() => setRaining(false)} />
        </Suspense>
      )}
    </EggContext.Provider>
  );
}

export function useEasterEggs() {
  return useContext(EggContext);
}

/** Calls `onTrigger` after `count` activations within `windowMs`. */
export function useRapidClicks(count, windowMs, onTrigger) {
  const hits = useRef([]);
  return useCallback(() => {
    const now = Date.now();
    hits.current = [...hits.current.filter((t) => now - t < windowMs), now];
    if (hits.current.length >= count) {
      hits.current = [];
      onTrigger();
    }
  }, [count, windowMs, onTrigger]);
}
