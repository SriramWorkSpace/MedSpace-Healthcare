import { useCallback, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import {
  ChatsCircle,
  ClockCounterClockwise,
  FileText,
  Flask,
  ForkKnife,
  List,
  MagnifyingGlass,
  Pill,
  ShareNetwork,
  SquaresFour,
  UploadSimple,
  X,
} from "@phosphor-icons/react";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "./ThemeToggle";
import { UserMenu } from "./UserMenu";
import { MobileDrawer } from "./MobileDrawer";
import { useScrolled } from "./useScrolled";
import { useEasterEggs, useRapidClicks } from "@/easter-eggs/EasterEggs";
import { cn } from "@/lib/cn";
import { useSearchPalette } from "@/features/search/searchContext";

const IS_MAC = typeof navigator !== "undefined" && /Mac|iPhone|iPad/.test(navigator.platform);

const APP_LINKS = [
  { to: "/app", label: "Dashboard", icon: SquaresFour, end: true },
  { to: "/app/documents", label: "Documents", icon: FileText },
  { to: "/app/medications", label: "Medications", icon: Pill },
  { to: "/app/labs", label: "Labs", icon: Flask },
  { to: "/app/diet", label: "Diet", icon: ForkKnife },
  { to: "/app/timeline", label: "Timeline", icon: ClockCounterClockwise },
  { to: "/app/ask", label: "Ask", icon: ChatsCircle },
  { to: "/app/sharing", label: "Sharing", icon: ShareNetwork },
];

export function AppNav() {
  const scrolled = useScrolled();
  const reduce = useReducedMotion();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const { openSearch } = useSearchPalette();
  const { discover } = useEasterEggs();
  const onLogoSpree = useCallback(() => discover("logo"), [discover]);
  const countLogoClick = useRapidClicks(5, 2500, onLogoSpree);

  return (
    <header className="topnav" data-scrolled={scrolled || open}>
      <nav
        aria-label="Primary"
        className="mx-auto flex h-full max-w-[1280px] items-center gap-3 px-4 sm:px-6"
      >
        <Link
          to="/app"
          onClick={countLogoClick}
          aria-label="MedSpace dashboard"
          className="mr-2 rounded-lg"
        >
          <Logo />
        </Link>

        <ul className="hidden items-center gap-0.5 lg:flex">
          {APP_LINKS.map(({ to, label, end }) => (
            <li key={to}>
              <NavLink to={to} end={end} className="navlink isolate">
                {({ isActive }) => (
                  <>
                    {isActive && (
                      <motion.span
                        layoutId="nav-pill"
                        className="navlink__pill"
                        transition={
                          reduce
                            ? { duration: 0 }
                            : { type: "spring", bounce: 0.18, duration: 0.45 }
                        }
                      />
                    )}
                    {label}
                  </>
                )}
              </NavLink>
            </li>
          ))}
        </ul>

        <div className="ml-auto flex items-center gap-1.5">
          <button
            type="button"
            onClick={openSearch}
            aria-label="Search your records"
            aria-keyshortcuts={IS_MAC ? "Meta+K" : "Control+K"}
            className="searchpill"
          >
            <MagnifyingGlass size={16} weight="bold" />
            <span className="hidden xl:inline">Search…</span>
            <kbd className="kbd hidden xl:inline">{IS_MAC ? "⌘K" : "Ctrl K"}</kbd>
          </button>
          <Button
            size="sm"
            className="hidden sm:inline-flex"
            onClick={() => navigate("/app/documents?upload=1")}
          >
            <UploadSimple size={15} weight="bold" />
            Upload
          </Button>
          <ThemeToggle />
          <UserMenu />
          <Button
            variant="ghost"
            size="sm"
            icon
            className="lg:hidden"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            aria-controls="mobile-nav"
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X size={18} weight="bold" /> : <List size={18} weight="bold" />}
          </Button>
        </div>
      </nav>

      <MobileDrawer
        id="mobile-nav"
        open={open}
        onClose={() => setOpen(false)}
        hiddenFrom="lg:hidden"
      >
        <ul className="grid grid-cols-1 gap-1">
          {APP_LINKS.map(({ to, label, icon: Icon, end }, i) => (
            <motion.li
              key={to}
              initial={reduce ? false : { opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.03 * i, duration: 0.22, ease: [0.23, 1, 0.32, 1] }}
            >
              <NavLink
                to={to}
                end={end}
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-[var(--radius-control)] px-3 py-3 text-[15px] font-medium",
                    isActive ? "bg-surface text-ink shadow-xs" : "text-ink-2",
                  )
                }
              >
                <Icon size={19} weight="duotone" />
                {label}
              </NavLink>
            </motion.li>
          ))}
        </ul>
        <Button
          className="mt-4 w-full"
          onClick={() => {
            setOpen(false);
            navigate("/app/documents?upload=1");
          }}
        >
          <UploadSimple size={16} weight="bold" />
          Upload a document
        </Button>
      </MobileDrawer>
    </header>
  );
}
