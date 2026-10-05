import { ArrowRight } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { useDemoLogin } from "@/features/auth/useDemoLogin";
import { Reveal } from "./Reveal";

export function FinalCta() {
  const demo = useDemoLogin();
  return (
    <section className="shell shell--marketing pb-20 lg:pb-28">
      <Reveal className="relative overflow-hidden rounded-[28px] bg-panel-brand px-6 py-16 text-panel-ink ring-1 ring-line sm:px-12 lg:py-24">
        <div className="pointer-events-none absolute -right-24 -top-24 size-[420px] rounded-full bg-[radial-gradient(closest-side,color-mix(in_oklch,var(--accent),transparent_55%),transparent)]" />
        <div className="relative max-w-2xl">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-5xl">
            Your paperwork, in good health.
          </h2>
          <p className="mt-4 max-w-[46ch] text-lg opacity-75">
            Explore a fully loaded account with synthetic records. No sign-up, no real data.
          </p>
          <Button size="lg" className="mt-8" loading={demo.isPending} onClick={() => demo.mutate()}>
            Try the demo
            <ArrowRight size={16} weight="bold" />
          </Button>
        </div>
      </Reveal>
    </section>
  );
}
