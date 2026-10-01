import { useCallback, useState } from "react";
import { Link } from "react-router";
import { List, X } from "@phosphor-icons/react";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/nav/ThemeToggle";
import { MobileDrawer } from "@/components/nav/MobileDrawer";
import { useScrolled } from "@/components/nav/useScrolled";
import { useAuth } from "@/lib/auth";
import { useDemoLogin } from "@/features/auth/useDemoLogin";
import { useEasterEggs, useRapidClicks } from "@/easter-eggs/EasterEggs";

const LINKS = [
  { href: "#how-it-works", label: "How it works" },
  { href: "#features", label: "Features" },
  { href: "#privacy", label: "Privacy" },
  { href: "#faq", label: "FAQ" },
];

export function MarketingNav() {
  const scrolled = useScrolled();
  const [open, setOpen] = useState(false);
  const { user } = useAuth();
  const demo = useDemoLogin();
  const { discover } = useEasterEggs();
  const onSpree = useCallback(() => discover("logo"), [discover]);
  const countClick = useRapidClicks(5, 2500, onSpree);

  const ctas = user ? (
    <Button as={Link} to="/app" size="sm">
      Open dashboard
    </Button>
  ) : (
    <>
      <Button as={Link} to="/login" variant="ghost" size="sm">
        Sign in
      </Button>
      <Button size="sm" loading={demo.isPending} onClick={() => demo.mutate()}>
        Try the demo
      </Button>
    </>
  );

  return (
    <header className="topnav" data-scrolled={scrolled || open}>
      <nav
        aria-label="Primary"
        className="mx-auto flex h-full max-w-[1280px] items-center gap-6 px-4 sm:px-6"
      >
        <Link to="/" onClick={countClick} aria-label="MedSpace home" className="rounded-lg">
          <Logo />
        </Link>
        <ul className="hidden items-center gap-1 md:flex">
          {LINKS.map((l) => (
            <li key={l.href}>
              <a href={l.href} className="navlink">
                {l.label}
              </a>
            </li>
          ))}
        </ul>
        <div className="ml-auto flex items-center gap-1.5">
          <ThemeToggle />
          <div className="hidden items-center gap-1.5 sm:flex">{ctas}</div>
          <Button
            variant="ghost"
            size="sm"
            icon
            className="md:hidden"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            aria-controls="marketing-mobile-nav"
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X size={18} weight="bold" /> : <List size={18} weight="bold" />}
          </Button>
        </div>
      </nav>
      <MobileDrawer id="marketing-mobile-nav" open={open} onClose={() => setOpen(false)}>
        <ul className="grid gap-1">
          {LINKS.map((l) => (
            <li key={l.href}>
              <a
                href={l.href}
                onClick={() => setOpen(false)}
                className="block rounded-[var(--radius-control)] px-3 py-3 text-[15px] font-medium text-ink-2"
              >
                {l.label}
              </a>
            </li>
          ))}
        </ul>
        <div className="mt-4 grid gap-2 sm:hidden">{ctas}</div>
      </MobileDrawer>
    </header>
  );
}
