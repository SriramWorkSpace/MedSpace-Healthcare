import { lazy, Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { SearchContext } from "./searchContext";

const SearchPalette = lazy(() => import("./SearchPalette"));

function isTyping(target) {
  return target?.closest?.("input, textarea, select, [contenteditable='true']");
}

/** Provides openSearch() and the global shortcuts: Ctrl/Cmd+K anywhere, "/" outside inputs. */
export function SearchProvider({ children }) {
  const [open, setOpen] = useState(false);
  const openSearch = useCallback(() => setOpen(true), []);
  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      } else if (e.key === "/" && !isTyping(e.target) && !e.metaKey && !e.ctrlKey) {
        e.preventDefault();
        setOpen(true);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const value = useMemo(() => ({ openSearch }), [openSearch]);
  return (
    <SearchContext.Provider value={value}>
      {children}
      {open && (
        <Suspense fallback={null}>
          <SearchPalette onClose={close} />
        </Suspense>
      )}
    </SearchContext.Provider>
  );
}
