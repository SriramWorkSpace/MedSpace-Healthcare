import { useState } from "react";
import { toast } from "sonner";
import { CalendarBlank, CheckCircle, CheckSquare, GoogleLogo, Info } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { Dialog } from "@/components/ui/Dialog";
import { Skeleton } from "@/components/ui/Skeleton";
import { cn } from "@/lib/cn";
import {
  connectGoogle,
  useGooglePreview,
  useGoogleStatus,
  useSyncPrescription,
  useUnsyncPrescription,
} from "./api";

function Toggle({ checked, onChange, icon: Icon, title, description, count }) {
  return (
    <label
      className={cn(
        "flex cursor-pointer items-start gap-3 rounded-[var(--radius-control)] border p-3.5 transition-colors",
        checked ? "border-accent/50 bg-accent-soft/40" : "border-line hover:bg-surface-2",
      )}
    >
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="mt-1 size-4 accent-[var(--accent)]"
      />
      <Icon size={20} weight="duotone" className="mt-0.5 shrink-0 text-accent" />
      <span className="min-w-0 flex-1">
        <span className="flex items-center justify-between gap-2 text-sm font-semibold">
          {title} <Chip className="tabular">{count}</Chip>
        </span>
        <span className="block text-xs text-ink-3">{description}</span>
      </span>
    </label>
  );
}

function ItemList({ items, kind }) {
  if (!items.length) return <p className="text-xs text-ink-3">Nothing to add.</p>;
  return (
    <ul className="grid max-h-44 gap-1 overflow-y-auto pr-1">
      {items.map((it, i) => (
        <li key={i} className="flex items-center justify-between gap-3 rounded-lg bg-surface-2 px-3 py-2 text-[13px]">
          <span className="min-w-0">
            <span className="block truncate font-medium">{it.summary}</span>
            <span className="block truncate text-xs text-ink-3">
              {it.when}
              {it.repeat && ` · ${it.repeat}`}
            </span>
          </span>
          {it.synced && (
            <span className="inline-flex shrink-0 items-center gap-1 text-xs text-accent">
              <CheckCircle size={13} weight="fill" /> {kind === "task" ? "In Tasks" : "On calendar"}
            </span>
          )}
        </li>
      ))}
    </ul>
  );
}

export function SyncDialog({ open, onClose, prescriptionId }) {
  const status = useGoogleStatus();
  const connected = status.data?.connected;
  const preview = useGooglePreview(prescriptionId, { enabled: open && Boolean(connected) });
  const sync = useSyncPrescription();
  const unsync = useUnsyncPrescription();
  const [calendar, setCalendar] = useState(true);
  const [tasks, setTasks] = useState(true);

  const events = preview.data?.events ?? [];
  const todo = preview.data?.tasks ?? [];
  const anySynced = [...events, ...todo].some((x) => x.synced);
  const simulated = status.data?.mode === "simulation";

  const doSync = () =>
    sync.mutate(
      { prescriptionId, calendar, tasks },
      {
        onSuccess: (r) =>
          toast.success("Synced with Google", {
            description: `${r.events} calendar event${r.events === 1 ? "" : "s"} and ${r.tasks} task${r.tasks === 1 ? "" : "s"}${simulated ? " (simulated)" : ""}.`,
          }),
        onError: (e) => toast.error(e.message),
      },
    );

  return (
    <Dialog
      open={open}
      onClose={onClose}
      title="Add to Google"
      description="Dose reminders go to Calendar. One-off to-dos go to Tasks."
      footer={
        connected ? (
          <>
            {anySynced && (
              <Button
                variant="ghost"
                loading={unsync.isPending}
                onClick={() =>
                  unsync.mutate(prescriptionId, {
                    onSuccess: (r) => toast(`Removed ${r.removed} item${r.removed === 1 ? "" : "s"} from Google`),
                  })
                }
              >
                Remove from Google
              </Button>
            )}
            <Button onClick={doSync} loading={sync.isPending} disabled={!calendar && !tasks}>
              {anySynced ? "Update in Google" : "Sync to Google"}
            </Button>
          </>
        ) : null
      }
    >
      {status.isPending ? (
        <Skeleton className="h-24" />
      ) : !connected ? (
        <div className="grid justify-items-center gap-3 py-4 text-center">
          <span className="grid size-12 place-items-center rounded-2xl bg-surface-2">
            <GoogleLogo size={24} weight="bold" />
          </span>
          <p className="max-w-sm text-sm text-ink-2">
            Connect your Google account once, then choose what to add. You can remove everything
            later in one click.
          </p>
          <Button onClick={connectGoogle}>Connect Google</Button>
          {status.data?.mode === "simulation" && (
            <p className="text-xs text-ink-3">This server runs a Google simulation, so nothing leaves MedSpace.</p>
          )}
        </div>
      ) : preview.isPending ? (
        <div className="grid gap-2">
          <Skeleton className="h-16" />
          <Skeleton className="h-16" />
        </div>
      ) : (
        <div className="grid gap-4">
          {simulated && (
            <p className="flex items-center gap-2 rounded-[var(--radius-control)] bg-surface-2 px-3 py-2 text-xs text-ink-2">
              <Info size={14} /> Simulation mode: syncing is fully functional but stays inside MedSpace.
            </p>
          )}
          <Toggle
            checked={calendar}
            onChange={setCalendar}
            icon={CalendarBlank}
            title="Google Calendar"
            description="Recurring reminders for each dose time, plus your follow-up visit."
            count={events.length}
          />
          {calendar && <ItemList items={events} kind="event" />}
          <Toggle
            checked={tasks}
            onChange={setTasks}
            icon={CheckSquare}
            title="Google Tasks"
            description='In a "MedSpace" list. Tasks keep dates only, so reminders stay on the calendar.'
            count={todo.length}
          />
          {tasks && <ItemList items={todo} kind="task" />}
        </div>
      )}
    </Dialog>
  );
}
