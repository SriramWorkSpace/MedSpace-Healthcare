import { Heartbeat } from "@phosphor-icons/react";
import { MARQUEE_PUNS } from "@/easter-eggs/puns";

/** The page's single marquee: a running strip of health puns. Pauses on hover, static on reduced motion. */
export function PunMarquee() {
  const items = [...MARQUEE_PUNS, ...MARQUEE_PUNS];
  return (
    <section aria-label="A dose of humor" className="marquee group overflow-hidden py-10">
      <ul className="marquee__track flex w-max gap-10">
        {items.map((pun, i) => (
          <li
            key={i}
            aria-hidden={i >= MARQUEE_PUNS.length}
            className="flex items-center gap-10 whitespace-nowrap text-xl font-medium tracking-tight text-ink-3 sm:text-2xl"
          >
            {pun}
            <Heartbeat size={22} weight="bold" className="text-accent" />
          </li>
        ))}
      </ul>
      <style>{`
        .marquee { mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); }
        .marquee__track { animation: marquee 60s linear infinite; }
        .marquee:hover .marquee__track { animation-play-state: paused; }
        @keyframes marquee { to { transform: translateX(-50%); } }
        @media (prefers-reduced-motion: reduce) {
          .marquee__track { animation: none; flex-wrap: wrap; width: auto; justify-content: center; padding-inline: 16px; }
          .marquee__track li[aria-hidden="true"] { display: none; }
        }
      `}</style>
    </section>
  );
}
