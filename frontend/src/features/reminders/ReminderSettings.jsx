import { useEffect, useState } from "react";
import { toast } from "sonner";
import { BellRinging } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Select } from "@/components/ui/Field";
import { api } from "@/lib/api";
import {
  currentSubscription,
  pushSupport,
  subscribePush,
  swRegistration,
  unsubscribePush,
} from "@/lib/push";
import { usePushConfig, usePushSettings, useSavePushSettings, useSendTest } from "./api";

const LEADS = [
  [0, "At dose time"],
  [5, "5 minutes before"],
  [10, "10 minutes before"],
  [15, "15 minutes before"],
  [30, "30 minutes before"],
];

/** Settings row: dose reminders as notifications on this browser or installed app. */
export function ReminderSettings() {
  const config = usePushConfig();
  const settings = usePushSettings();
  const save = useSavePushSettings();
  const test = useSendTest();
  const [state, setState] = useState("checking"); // checking | unsupported | no-worker | off | on
  const [permission, setPermission] = useState(() =>
    "Notification" in window ? Notification.permission : "default",
  );
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let alive = true;
    (async () => {
      if (pushSupport() === "unsupported") return alive && setState("unsupported");
      if (!(await swRegistration())) return alive && setState("no-worker");
      const sub = await currentSubscription();
      if (alive) setState(sub ? "on" : "off");
    })();
    return () => {
      alive = false;
    };
  }, []);

  const turnOn = async () => {
    setBusy(true);
    try {
      const sub = await subscribePush(config.data.public_key);
      const json = sub.toJSON();
      await api.post("/api/push/subscriptions", { endpoint: json.endpoint, keys: json.keys });
      setState("on");
      toast("Reminders are on for this device");
    } catch (e) {
      if (e.message === "denied") {
        setPermission(Notification.permission);
        toast.error("Notifications are blocked for MedSpace in this browser.");
      } else {
        toast.error(e.message === "no-worker" ? "Reload the page and try again." : e.message);
      }
    } finally {
      setBusy(false);
    }
  };

  const turnOff = async () => {
    setBusy(true);
    try {
      const endpoint = await unsubscribePush();
      if (endpoint) {
        await api
          .delete(`/api/push/subscriptions?endpoint=${encodeURIComponent(endpoint)}`)
          .catch(() => {});
      }
      setState("off");
      toast("Reminders are off for this device");
    } finally {
      setBusy(false);
    }
  };

  const on = state === "on";
  const unavailable = state === "unsupported" || state === "no-worker";

  return (
    <div className="flex flex-col gap-4 p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="grid size-9 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent-soft-ink">
            <BellRinging size={18} weight="duotone" />
          </span>
          <div className="max-w-[60ch]">
            <p id="reminders-label" className="font-medium">
              Dose reminders
            </p>
            <p id="reminders-desc" className="mt-0.5 text-sm text-ink-2">
              {state === "unsupported"
                ? "This browser can't show notifications from websites."
                : state === "no-worker"
                  ? "Notifications need the installed app or the published site; they aren't available in this development build."
                  : permission === "denied"
                    ? "Notifications are blocked for MedSpace. Allow them in your browser's site settings, then turn this on."
                    : "A notification when a dose is due, with Taken and Skip buttons. Works when MedSpace is closed. Doses you've already ticked aren't reminded."}
            </p>
          </div>
        </div>
        <button
          type="button"
          role="switch"
          aria-checked={on}
          aria-labelledby="reminders-label"
          aria-describedby="reminders-desc"
          disabled={busy || unavailable || state === "checking" || !config.data}
          onClick={on ? turnOff : turnOn}
          className="relative inline-flex h-7 w-12 shrink-0 items-center rounded-full border border-line-strong bg-surface-3 transition-colors duration-150 aria-checked:border-accent aria-checked:bg-accent disabled:opacity-60"
        >
          <span
            aria-hidden
            className="size-5 translate-x-[3px] rounded-full bg-surface shadow-xs transition-transform duration-200 ease-[cubic-bezier(0.23,1,0.32,1)] [[aria-checked=true]>&]:translate-x-[23px]"
          />
        </button>
      </div>

      {on && settings.data && (
        <div className="flex flex-wrap items-end gap-3 sm:pl-12">
          <label className="grid gap-1 text-sm">
            <span className="font-medium">Remind me</span>
            <Select
              value={settings.data.lead_minutes}
              onChange={(e) =>
                save.mutate(
                  { enabled: true, lead_minutes: Number(e.target.value) },
                  { onError: (err) => toast.error(err.message) },
                )
              }
              className="w-52"
            >
              {LEADS.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
          </label>
          <Button
            variant="secondary"
            loading={test.isPending}
            onClick={() =>
              test.mutate(undefined, {
                onSuccess: (r) =>
                  toast(
                    r.sent
                      ? "Test notification sent"
                      : "No device received it. Try turning reminders off and on again.",
                    {
                      description:
                        config.data?.provider === "fake"
                          ? "This server simulates delivery, so nothing will pop up."
                          : undefined,
                    },
                  ),
                onError: (err) => toast.error(err.message),
              })
            }
          >
            Send a test
          </Button>
        </div>
      )}
    </div>
  );
}
