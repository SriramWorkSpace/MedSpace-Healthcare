import { useState } from "react";
import { useMotionValueEvent, useScroll } from "motion/react";

/** True once the page has scrolled past `threshold` px (via motion's scroll observer, no listeners). */
export function useScrolled(threshold = 8) {
  const { scrollY } = useScroll();
  const [scrolled, setScrolled] = useState(false);
  useMotionValueEvent(scrollY, "change", (y) => {
    const next = y > threshold;
    setScrolled((prev) => (prev === next ? prev : next));
  });
  return scrolled;
}
