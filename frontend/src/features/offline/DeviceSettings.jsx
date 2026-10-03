import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { DeviceMobile, DownloadSimple } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { isOfflineEnabled, setOfflineEnabled } from "@/lib/offline";
import { isStandalone, promptInstall } from "@/lib/install";
import { formatDate } from "@/lib/format";
import { useInstallPrompt, useSavedAt } from "./hooks";
import { ReminderSettings } from "@/features/reminders/ReminderSettings";

/** Settings section: install the app, and keep an offline copy on this device (opt-in). */
export function DeviceSettings() {
  const qc = useQueryClient();
  const [enabled, setEnabled] = useState(isOfflineEnabled);
  const [busy, setBusy] = useState(false);
  const savedAt = useSavedAt();
  const installEvent = useInstallPrompt();
  const installed = isStandalone();

  const toggle = async () => {
    setBusy(true);
    const next = !enabled;
    await setOfflineEnabled(next, qc);
    setEnabled(next);
    setBusy(false);
    toast(next ? "Offline access is on for this device" : "Offline copy deleted from this device");
  };

  return (
    <div className="card divide-y divide-line">
      <ReminderSettings />
      <div className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="max-w-[60ch]">
          <p id="offline-label" className="font-medium">
            Offline access
          </p>
          <p id="offline-desc" className="mt-0.5 text-sm text-ink-2">
            Keep a copy of your medicines, schedule, lab results and visit preps in this browser so
            you can read them without a connection. Dose ticks made offline sync when you're back.
            The copy is deleted when you sign out or turn this off.
          </p>
          {enabled && savedAt && (
            <p className="mt-1 text-xs text-ink-3">
              Last saved {formatDate(savedAt, "h:mm a, MMM d")}.
            </p>
          )}
        </div>
        <button
          type="button"
          role="switch"
          aria-checked={enabled}
          aria-labelledby="offline-label"
          aria-describedby="offline-desc"
          disabled={busy}
          onClick={toggle}
          className="relative inline-flex h-7 w-12 shrink-0 items-center rounded-full border border-line-strong bg-surface-3 transition-colors duration-150 aria-checked:border-accent aria-checked:bg-accent disabled:opacity-60"
        >
          <span
            aria-hidden
            className="size-5 translate-x-[3px] rounded-full bg-surface shadow-xs transition-transform duration-200 ease-[cubic-bezier(0.23,1,0.32,1)] [[aria-checked=true]>&]:translate-x-[23px]"
          />
        </button>
      </div>

      <div className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="grid size-9 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
            <DeviceMobile size={18} weight="duotone" />
          </span>
          <div>
            <p className="font-medium">Install MedSpace</p>
            <p className="mt-0.5 text-sm text-ink-2">
              {installed
                ? "You're using the installed app."
                : installEvent
                  ? "Open it from your home screen or dock like any other app."
                  : "Use your browser's Install option, or on iPhone: Share, then Add to Home Screen."}
            </p>
          </div>
        </div>
        {!installed && installEvent && (
          <Button
            variant="secondary"
            onClick={async () => {
              if (await promptInstall()) toast("MedSpace installed");
            }}
          >
            <DownloadSimple size={15} /> Install app
          </Button>
        )}
      </div>
    </div>
  );
}
