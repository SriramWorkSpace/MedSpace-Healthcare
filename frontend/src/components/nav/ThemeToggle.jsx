import { useCallback } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Moon, Sun } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { useTheme } from "@/lib/theme";
import { useEasterEggs, useRapidClicks } from "@/easter-eggs/EasterEggs";

export function ThemeToggle() {
  const { resolved, toggle } = useTheme();
  const { discover } = useEasterEggs();
  const onRapid = useCallback(() => discover("themeFlip"), [discover]);
  const countClick = useRapidClicks(6, 4000, onRapid);
  const isDark = resolved === "dark";

  return (
    <Button
      variant="ghost"
      size="sm"
      icon
      aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
      onClick={(e) => {
        const box = e.currentTarget.getBoundingClientRect();
        toggle({ x: box.left + box.width / 2, y: box.top + box.height / 2 });
        countClick();
      }}
    >
      <AnimatePresence mode="wait" initial={false}>
        <motion.span
          key={resolved}
          initial={{ opacity: 0, rotate: -40, scale: 0.8 }}
          animate={{ opacity: 1, rotate: 0, scale: 1 }}
          exit={{ opacity: 0, rotate: 40, scale: 0.8 }}
          transition={{ duration: 0.18, ease: [0.23, 1, 0.32, 1] }}
          className="grid grid-cols-1 place-items-center"
        >
          {isDark ? <Moon size={17} weight="bold" /> : <Sun size={17} weight="bold" />}
        </motion.span>
      </AnimatePresence>
    </Button>
  );
}
