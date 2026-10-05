import { startTransition, useEffect, useRef, useState } from "react";
import { smoothScrollTo } from "@/lib/smoothScroll";
import { cn } from "@/lib/cn";

/**
 * Settings' section list: a click glides to the section (quick, interruptible, instant with
 * reduced motion), and the current section stays marked while you scroll.
 */
export function SettingsNav({ sections }) {
  const [active, setActive] = useState(sections[0].id);
  // While we scroll on purpose, the clicked item stays current. A counter, so a glide that a
  // newer click cancelled can't unlock the newer one.
  const gliding = useRef(0);
  const visible = useRef(new Set());

  useEffect(() => {
    // A section is current once its top passes into the upper third of the screen.
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) visible.current.add(e.target.id);
          else visible.current.delete(e.target.id);
        }
        if (gliding.current) return;
        const first = sections.find((s) => visible.current.has(s.id));
        if (first) startTransition(() => setActive(first.id));
      },
      { rootMargin: "-90px 0px -65% 0px" },
    );
    for (const { id } of sections) {
      const el = document.getElementById(id);
      if (el) io.observe(el);
    }
    return () => io.disconnect();
  }, [sections]);

  const go = (e, id) => {
    const el = document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    // Cosmetic: let React fit this between scroll frames instead of delaying the first one.
    startTransition(() => setActive(id));
    const glide = gliding.current + 1;
    gliding.current = glide;
    smoothScrollTo(el, {
      onDone: (arrived) => {
        if (gliding.current === glide) gliding.current = 0;
        if (!arrived) return;
        history.replaceState(null, "", `#${id}`); // shareable, without a second jump
        el.querySelector("h2")?.focus({ preventScroll: true }); // keyboard and screen readers land here
      },
    });
  };

  return (
    <nav aria-label="Settings sections" className="hidden lg:block">
      <ul className="sticky top-[calc(var(--nav-h)+24px)] grid grid-cols-1 gap-0.5">
        {sections.map(({ id, label, icon: Icon }) => (
          <li key={id}>
            <a
              href={`#${id}`}
              onClick={(e) => go(e, id)}
              aria-current={active === id ? "location" : undefined}
              className={cn(
                "flex items-center gap-2.5 rounded-[var(--radius-control)] px-3 py-2 text-sm transition-colors duration-150",
                active === id
                  ? "bg-surface-2 font-medium text-ink"
                  : "text-ink-2 hover:bg-surface-2 hover:text-ink",
              )}
            >
              <Icon size={16} weight={active === id ? "bold" : "regular"} /> {label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
