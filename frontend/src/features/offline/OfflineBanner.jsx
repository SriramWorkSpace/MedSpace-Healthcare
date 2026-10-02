import { Link } from "react-router";
import { CloudSlash } from "@phosphor-icons/react";
import { isOfflineEnabled } from "@/lib/offline";
import { formatDate } from "@/lib/format";
import { useOnline, usePendingDoseTicks, useSavedAt } from "./hooks";

/** Shown under the app bar while the connection is down, and while ticks wait to sync. */
export function OfflineBanner() {
  const online = useOnline();
  const savedAt = useSavedAt();
  const pending = usePendingDoseTicks();
  if (online && !pending) return null;

  const waiting =
    pending > 0
      ? ` ${pending} dose tick${pending === 1 ? "" : "s"} will sync when you reconnect.`
      : "";

  return (
    <aside
      aria-label="Connection status"
      role="status"
      className="no-print border-b border-line bg-surface-2 px-4 py-2 text-center text-[13px] text-ink-2"
    >
      <CloudSlash size={14} className="mr-1.5 inline-block align-[-2px]" />
      {online ? (
        <>Back online. Syncing your changes…</>
      ) : isOfflineEnabled() && savedAt ? (
        <>
          You're offline. Showing what this device saved at {formatDate(savedAt, "h:mm a, MMM d")}.
          {waiting}
        </>
      ) : (
        <>
          You're offline.{waiting} To read your records without a connection, turn on{" "}
          <Link to="/app/settings#device" className="font-medium text-accent underline">
            offline access
          </Link>
          .
        </>
      )}
    </aside>
  );
}
