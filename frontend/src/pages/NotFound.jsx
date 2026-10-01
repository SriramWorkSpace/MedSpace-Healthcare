import { useEffect, useState } from "react";
import { Link } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { Heartbeat } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Logo } from "@/components/ui/Logo";
import { NOT_FOUND_LINES, pick } from "@/easter-eggs/puns";
import { useEasterEggs } from "@/easter-eggs/EasterEggs";

/** A flatlining ECG that occasionally finds a beat again. */
function Flatline() {
  const reduce = useReducedMotion();
  return (
    <svg viewBox="0 0 400 80" className="w-full max-w-md text-accent" aria-hidden>
      <motion.path
        d="M0 40 H120 L135 40 L145 12 L158 68 L170 40 H400"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={{ pathLength: reduce ? 1 : 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 1.6, ease: [0.77, 0, 0.175, 1] }}
      />
    </svg>
  );
}

export default function NotFound() {
  const [line] = useState(() => pick(NOT_FOUND_LINES));
  const { discover } = useEasterEggs();
  useEffect(() => {
    const t = setTimeout(() => discover("notFound"), 900);
    return () => clearTimeout(t);
  }, [discover]);

  return (
    <div className="flex min-h-[100dvh] flex-col px-4 py-6 sm:px-10">
      <Link to="/" className="w-fit rounded-lg" aria-label="MedSpace home">
        <Logo />
      </Link>
      <main className="mx-auto flex max-w-xl flex-1 flex-col items-center justify-center text-center">
        <Flatline />
        <p className="mt-8 font-mono text-sm text-ink-3">Error 404</p>
        <h1 className="mt-2 text-4xl font-semibold tracking-tight sm:text-5xl">{line}</h1>
        <p className="mt-4 text-ink-2">
          The page you're looking for doesn't exist or was moved. Let's get you somewhere healthier.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Button as={Link} to="/app">
            <Heartbeat size={16} weight="bold" /> Back to dashboard
          </Button>
          <Button as={Link} to="/" variant="secondary">
            Home page
          </Button>
        </div>
      </main>
    </div>
  );
}
