import { useId, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { Plus } from "@phosphor-icons/react";
import { Reveal } from "./Reveal";

const FAQ = [
  {
    q: "Is MedSpace a medical device?",
    a: "No. It organizes and explains what is written in documents you upload. It does not diagnose conditions, recommend treatment or change doses. Always follow your prescriber.",
  },
  {
    q: "Whose data is in the demo?",
    a: "Nobody's. The demo uses synthetic prescriptions with fictional clinics, prescribers and patients. Each demo session gets its own isolated account that is deleted after 24 hours.",
  },
  {
    q: "How does the extraction work?",
    a: "Text-based PDFs are read directly; scans and photos go through a vision model. The results are validated, shorthand like 1-0-1 or TDS is converted by deterministic rules, and every field keeps its confidence and source page.",
  },
  {
    q: "What does Ask MedSpace know?",
    a: "Only your own records. Questions are matched against your documents with hybrid search, and every answer cites the document and page it came from. If the answer is not in your records, it says so.",
  },
  {
    q: "What happens with Google Calendar and Tasks?",
    a: "Connecting Google is optional. Once connected, you choose what to sync. Recurring dose reminders become Calendar events, one-off actions become Tasks, and you can remove them from MedSpace at any time.",
  },
];

function Item({ q, a }) {
  const [open, setOpen] = useState(false);
  const id = useId();
  return (
    <li className="border-b border-line">
      <h3>
        <button
          type="button"
          aria-expanded={open}
          aria-controls={id}
          onClick={() => setOpen((v) => !v)}
          className="flex w-full items-center justify-between gap-6 py-5 text-left text-[17px] font-medium"
        >
          {q}
          <motion.span
            animate={{ rotate: open ? 45 : 0 }}
            transition={{ duration: 0.2, ease: [0.23, 1, 0.32, 1] }}
            className="grid grid-cols-1 size-8 shrink-0 place-items-center rounded-full bg-surface-2 text-ink-2"
          >
            <Plus size={14} weight="bold" />
          </motion.span>
        </button>
      </h3>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            id={id}
            role="region"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.23, 1, 0.32, 1] }}
            className="overflow-hidden"
          >
            <p className="max-w-[64ch] pb-6 text-[15px] leading-relaxed text-ink-2">{a}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </li>
  );
}

export function Faq() {
  return (
    <section
      id="faq"
      className="mx-auto grid grid-cols-1 max-w-[1280px] gap-10 px-4 py-20 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:py-28"
    >
      <Reveal>
        <h2 className="text-3xl font-semibold tracking-tight sm:text-5xl">Questions, answered.</h2>
        <p className="mt-4 max-w-[36ch] text-lg text-ink-2">
          The fine print, without the fine print.
        </p>
      </Reveal>
      <Reveal delay={0.08}>
        <ul className="border-t border-line">
          {FAQ.map((item) => (
            <Item key={item.q} {...item} />
          ))}
        </ul>
      </Reveal>
    </section>
  );
}
