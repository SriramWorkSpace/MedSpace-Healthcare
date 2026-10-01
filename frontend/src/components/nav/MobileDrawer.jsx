import { useEffect } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";

/** Compact top drawer used for navigation below the md breakpoint. */
export function MobileDrawer({ open, onClose, children, id }) {
  const reduce = useReducedMotion();

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === "Escape" && onClose();
    const { overflow } = document.body.style;
    document.body.style.overflow = "hidden";
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = overflow;
    };
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            className="fixed inset-0 top-[var(--nav-h)] bg-[oklch(0.2_0.02_165/0.3)] md:hidden"
            style={{ zIndex: "var(--z-drawer)" }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
          />
          <motion.div
            id={id}
            className="fixed inset-x-0 top-[var(--nav-h)] origin-top border-b border-line bg-bg px-4 pb-6 pt-2 shadow-md md:hidden"
            style={{ zIndex: "var(--z-drawer)" }}
            initial={reduce ? { opacity: 0 } : { opacity: 0, y: -12, scaleY: 0.98 }}
            animate={{ opacity: 1, y: 0, scaleY: 1 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, y: -8, transition: { duration: 0.14 } }}
            transition={{ duration: 0.26, ease: [0.32, 0.72, 0, 1] }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
