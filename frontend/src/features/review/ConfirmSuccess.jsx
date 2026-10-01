import { Link } from "react-router";
import { motion, useReducedMotion } from "motion/react";
import { Button } from "@/components/ui/Button";

/** The moment a draft becomes records. Rare enough to earn a little delight. */
export function ConfirmSuccess({ prescriptionId, medCount, taskCount }) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.35, ease: [0.23, 1, 0.32, 1] }}
      className="card mx-auto max-w-lg px-8 py-12 text-center"
    >
      <svg viewBox="0 0 64 64" className="mx-auto size-16 text-accent" aria-hidden>
        <motion.circle
          cx="32"
          cy="32"
          r="29"
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          initial={{ pathLength: reduce ? 1 : 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.6, ease: [0.77, 0, 0.175, 1] }}
        />
        <motion.path
          d="M20 33 L28.5 41.5 L45 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="4"
          strokeLinecap="round"
          strokeLinejoin="round"
          initial={{ pathLength: reduce ? 1 : 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.4, delay: 0.45, ease: [0.23, 1, 0.32, 1] }}
        />
      </svg>
      <h2 className="mt-6 text-2xl font-semibold tracking-tight">Records confirmed</h2>
      <p className="mt-2 text-ink-2">
        {medCount} medication{medCount === 1 ? "" : "s"} and {taskCount} to-do
        {taskCount === 1 ? "" : "s"} are now part of your health record. A clean bill of paperwork.
      </p>
      <div className="mt-8 flex flex-wrap justify-center gap-2">
        {prescriptionId && (
          <Button as={Link} to={`/app/prescriptions/${prescriptionId}`}>
            View report
          </Button>
        )}
        <Button as={Link} to="/app/medications" variant="secondary">
          See schedule
        </Button>
      </div>
    </motion.div>
  );
}
