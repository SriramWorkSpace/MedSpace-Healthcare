import { Link } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { ArrowRight } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/lib/auth";
import { useDemoLogin } from "@/features/auth/useDemoLogin";
import { HeroMorph } from "@/features/marketing/HeroMorph";
import { Workflow } from "@/features/marketing/Workflow";
import { FeatureBento } from "@/features/marketing/FeatureBento";
import { Trust } from "@/features/marketing/Trust";
import { PunMarquee } from "@/features/marketing/PunMarquee";
import { Faq } from "@/features/marketing/Faq";
import { FinalCta } from "@/features/marketing/FinalCta";

const EASE = [0.16, 1, 0.3, 1];

function Hero() {
  const reduce = useReducedMotion();
  const demo = useDemoLogin();
  const { user } = useAuth();
  const rise = (delay) => ({
    initial: reduce ? false : { opacity: 0, y: 16, filter: "blur(6px)" },
    animate: { opacity: 1, y: 0, filter: "blur(0px)" },
    transition: { duration: 0.8, delay, ease: EASE },
  });

  return (
    <section className="relative overflow-hidden">
      <div className="shell shell--marketing grid grid-cols-1 min-h-[calc(100dvh-var(--nav-h))] items-center gap-14 pb-16 pt-10 lg:grid-cols-[1.05fr_1fr] lg:gap-10 lg:pb-20 lg:pt-12">
        <div className="max-w-xl">
          <motion.h1
            {...rise(0)}
            className="text-[44px] font-semibold leading-[1.02] tracking-[-0.04em] sm:text-6xl lg:text-[68px]"
          >
            Your health, all in one space.
          </motion.h1>
          <motion.p {...rise(0.1)} className="mt-6 max-w-[44ch] text-lg leading-relaxed text-ink-2">
            Drop in a prescription. MedSpace extracts every dose, builds your schedule and answers
            questions, citing the exact page.
          </motion.p>
          <motion.div {...rise(0.2)} className="mt-9 flex flex-wrap items-center gap-3">
            {user ? (
              <Button as={Link} to="/app" size="lg">
                Open dashboard <ArrowRight size={16} weight="bold" />
              </Button>
            ) : (
              <>
                <Button size="lg" loading={demo.isPending} onClick={() => demo.mutate()}>
                  Try the demo <ArrowRight size={16} weight="bold" />
                </Button>
                <Button as={Link} to="/signup" size="lg" variant="secondary">
                  Create account
                </Button>
              </>
            )}
          </motion.div>
        </div>
        <HeroMorph />
      </div>
    </section>
  );
}

export default function Landing() {
  return (
    <>
      <Hero />
      <Workflow />
      <FeatureBento />
      <Trust />
      <PunMarquee />
      <Faq />
      <FinalCta />
    </>
  );
}
