import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { toast } from "sonner";
import {
  ArrowSquareOut,
  Clock,
  PauseCircle,
  PencilSimple,
  Pill,
  PlayCircle,
  Plus,
  X,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { Dialog } from "@/components/ui/Dialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { SegmentedTabs } from "@/components/ui/Tabs";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useMedications, useUpdateMedication } from "@/features/records/api";
import { formatClock, formatDate } from "@/lib/format";
import { scheduleLabel } from "@/features/review/mapping";
import { useAdherence } from "@/features/doses/api";
import { AdherenceLine } from "@/features/doses/AdherenceLine";
import { useSupplies } from "@/features/supply/api";
import { SupplyDialog } from "@/features/supply/SupplyDialog";
import { SupplyLine } from "@/features/supply/SupplyLine";
import { useActing } from "@/features/circle/api";

const TABS = [
  { key: "active", label: "Active" },
  { key: "upcoming", label: "Upcoming" },
  { key: "completed", label: "Completed" },
  { key: "stopped", label: "Stopped" },
];

function EditTimesDialog({ med, onClose }) {
  const update = useUpdateMedication();
  const [times, setTimes] = useState(med?.schedule.times ?? []);
  const [draft, setDraft] = useState("");
  if (!med) return null;

  const save = () =>
    update.mutate(
      {
        id: med.id,
        schedule: { ...med.schedule, times, label: scheduleLabel({ ...med.schedule, times }) },
      },
      {
        onSuccess: () => {
          toast.success("Schedule updated");
          onClose();
        },
        onError: (e) => toast.error(e.message),
      },
    );

  return (
    <Dialog
      open
      onClose={onClose}
      title={`Dose times for ${med.name}`}
      description="Reminders and the dashboard use these times."
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={save} loading={update.isPending} disabled={!times.length}>
            Save times
          </Button>
        </>
      }
    >
      <div className="flex flex-wrap items-center gap-2">
        {times.map((t) => (
          <span key={t} className="chip chip--accent tabular gap-1 pr-1">
            {formatClock(t)}
            <button
              type="button"
              aria-label={`Remove ${formatClock(t)}`}
              onClick={() => setTimes(times.filter((x) => x !== t))}
              className="tap grid grid-cols-1 size-4 place-items-center rounded-full"
            >
              <X size={10} weight="bold" />
            </button>
          </span>
        ))}
      </div>
      <div className="mt-4 flex items-center gap-2">
        <input
          type="time"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          className="input w-36"
          aria-label="New dose time"
        />
        <Button
          variant="secondary"
          size="sm"
          onClick={() => {
            if (draft) setTimes([...new Set([...times, draft])].sort());
            setDraft("");
          }}
        >
          <Plus size={13} weight="bold" /> Add time
        </Button>
      </div>
    </Dialog>
  );
}

function CourseProgress({ med }) {
  if (!med.duration_days || med.status !== "active" || !med.day_of_course) return null;
  const pct = Math.min(100, (med.day_of_course / med.duration_days) * 100);
  return (
    <div className="mt-4">
      <div className="mb-1.5 flex justify-between text-xs text-ink-3">
        <span>
          Day <span className="tabular font-semibold text-ink">{med.day_of_course}</span> of{" "}
          {med.duration_days}
        </span>
        <span>Ends {formatDate(med.end_date, "MMM d")}</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-surface-3">
        <motion.div
          className="h-full rounded-full bg-accent"
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.7, ease: [0.23, 1, 0.32, 1] }}
        />
      </div>
    </div>
  );
}

function MedicationCard({ med, onEdit, index, focused, history, window, supply, onSupply }) {
  const { isActing, readOnly } = useActing();
  const update = useUpdateMedication();
  const stopped = med.status === "stopped";
  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ duration: 0.3, delay: Math.min(index, 8) * 0.035, ease: [0.23, 1, 0.32, 1] }}
      data-med-id={med.id}
      data-focused={focused || undefined}
      className="card flex flex-col p-5"
    >
      {/* The schedule chip drops below the name when both don't fit (narrow phones). */}
      <div className="flex flex-wrap items-start justify-between gap-x-3 gap-y-2">
        <div className="flex min-w-0 flex-1 basis-48 items-center gap-3">
          <span className="grid grid-cols-1 size-10 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
            <Pill size={19} weight="duotone" />
          </span>
          <div className="min-w-0">
            <p className="line-clamp-2 font-semibold break-words">
              {med.name}{" "}
              {med.strength && (
                <span className="font-normal whitespace-nowrap text-ink-3">{med.strength}</span>
              )}
            </p>
            <p className="truncate text-xs text-ink-3">
              {[med.form, med.prescriber_name].filter(Boolean).join(" · ") || "Prescription"}
            </p>
          </div>
        </div>
        <Chip tone={med.as_needed ? "neutral" : "accent"}>{med.schedule.label || "Schedule"}</Chip>
      </div>

      {!med.as_needed && med.schedule.times.length > 0 && (
        <div className="mt-4 flex flex-wrap items-center gap-1.5">
          <Clock size={14} className="text-ink-3" />
          {med.schedule.times.map((t) => (
            <span
              key={t}
              className="tabular rounded-md bg-surface-2 px-2 py-0.5 text-xs font-medium"
            >
              {formatClock(t)}
            </span>
          ))}
        </div>
      )}
      {med.instructions && <p className="mt-3 text-sm text-ink-2">{med.instructions}</p>}
      <CourseProgress med={med} />
      {history && <AdherenceLine history={history} window={window} />}
      {(med.status === "active" || med.status === "upcoming") && !(readOnly && !supply) && (
        <SupplyLine
          supply={supply}
          onCount={readOnly ? null : () => onSupply(med, "count")}
          onRefill={readOnly ? null : () => onSupply(med, "refill")}
        />
      )}
      {med.status === "upcoming" && (
        <p className="mt-3 text-xs text-ink-3">Starts {formatDate(med.start_date)}</p>
      )}
      {med.status === "completed" && med.end_date && (
        <p className="mt-3 text-xs text-ink-3">Finished {formatDate(med.end_date)}</p>
      )}

      <div className="mt-auto flex flex-wrap gap-1 pt-4">
        {!isActing && !med.as_needed && !stopped && (
          <Button variant="ghost" size="sm" onClick={() => onEdit(med)}>
            <PencilSimple size={14} /> Edit times
          </Button>
        )}
        {!isActing && (med.status === "active" || stopped) && (
          <Button
            variant="ghost"
            size="sm"
            loading={update.isPending}
            onClick={() =>
              update.mutate(
                { id: med.id, stopped: !stopped },
                {
                  onSuccess: () => toast(stopped ? "Marked as active again" : "Marked as stopped"),
                },
              )
            }
          >
            {stopped ? <PlayCircle size={14} /> : <PauseCircle size={14} />}
            {stopped ? "Resume" : "Mark stopped"}
          </Button>
        )}
        {med.document_id && (
          <Button as={Link} to={`/app/documents/${med.document_id}`} variant="ghost" size="sm">
            <ArrowSquareOut size={14} /> Source
          </Button>
        )}
      </div>
    </motion.li>
  );
}

export default function Medications() {
  const [params] = useSearchParams();
  const focusId = params.get("focus");
  const [chosenTab, setTab] = useState(null);
  const [editing, setEditing] = useState(null);
  const { data, isPending } = useMedications();
  const adherence = useAdherence(14);
  const supplies = useSupplies();
  const [supplying, setSupplying] = useState(null); // { med, mode }
  const supplyById = useMemo(
    () => new Map((supplies.data ?? []).map((s) => [s.medication_id, s])),
    [supplies.data],
  );
  const historyById = useMemo(
    () => new Map((adherence.data?.medications ?? []).map((h) => [h.medication_id, h])),
    [adherence.data],
  );
  // Search links here with ?focus={id}: open that medicine's tab and bring its card into view.
  const focusMed = focusId ? data?.find((m) => m.id === focusId) : undefined;
  const tab = chosenTab ?? focusMed?.status ?? "active";

  useEffect(() => {
    if (!focusMed) return;
    document
      .querySelector(`[data-med-id="${focusMed.id}"]`)
      ?.scrollIntoView({ block: "center", behavior: "smooth" });
  }, [focusMed]);

  const tabs = useMemo(
    () => TABS.map((t) => ({ ...t, count: data?.filter((m) => m.status === t.key).length ?? 0 })),
    [data],
  );
  const visible = data?.filter((m) => m.status === tab) ?? [];

  return (
    <>
      <PageHeader
        title="Medications"
        description="Everything you've confirmed, with the schedule MedSpace uses for reminders."
      />
      {isPending ? (
        <LoadingRegion label="Loading medications">
          <Skeleton className="mb-5 h-10 w-80 rounded-full" />
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
            {Array.from({ length: 6 }, (_, i) => (
              <Skeleton key={i} className="h-48 rounded-card" />
            ))}
          </div>
        </LoadingRegion>
      ) : data.length === 0 ? (
        <EmptyState
          icon={Pill}
          title="No medications yet"
          description="Confirm a prescription and its medicines will show up here with their schedules."
          action={
            <Button as={Link} to="/app/documents">
              Go to documents
            </Button>
          }
          quip={EMPTY_QUIPS.medications}
        />
      ) : (
        <>
          <SegmentedTabs
            label="Medication status"
            items={tabs}
            value={tab}
            onChange={setTab}
            className="mb-5"
          />
          {visible.length === 0 ? (
            <p className="rounded-card border border-line bg-surface px-5 py-10 text-center text-sm text-ink-2">
              Nothing {tab} right now.
            </p>
          ) : (
            <ul className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
              <AnimatePresence mode="popLayout">
                {visible.map((m, i) => (
                  <MedicationCard
                    key={m.id}
                    med={m}
                    index={i}
                    onEdit={setEditing}
                    focused={m.id === focusMed?.id && chosenTab === null}
                    history={historyById.get(m.id)}
                    window={adherence.data}
                    supply={supplyById.get(m.id)}
                    onSupply={(med, mode) => setSupplying({ med, mode })}
                  />
                ))}
              </AnimatePresence>
            </ul>
          )}
        </>
      )}
      {supplying && (
        <SupplyDialog
          key={`${supplying.med.id}-${supplying.mode}`}
          med={supplying.med}
          supply={supplyById.get(supplying.med.id)}
          mode={
            supplying.mode === "refill" && supplyById.get(supplying.med.id) ? "refill" : "count"
          }
          onClose={() => setSupplying(null)}
        />
      )}
      {editing && (
        <EditTimesDialog key={editing.id} med={editing} onClose={() => setEditing(null)} />
      )}
    </>
  );
}
