import { useInfiniteQuery } from "@tanstack/react-query";
import {
  ArrowClockwise,
  CalendarCheck,
  CalendarX,
  CheckCircle,
  Eye,
  FileArrowUp,
  GoogleLogo,
  LinkBreak,
  LinkSimple,
  ShieldWarning,
  SignIn,
  Sparkle,
  Trash,
  UserPlus,
  XCircle,
} from "@phosphor-icons/react";
import { api } from "@/lib/api";

export function useAuditLog(prefix) {
  return useInfiniteQuery({
    queryKey: ["audit", prefix ?? "all"],
    initialPageParam: null,
    queryFn: ({ pageParam }) => {
      const qs = new URLSearchParams({ limit: "25" });
      if (pageParam) qs.set("cursor", pageParam);
      if (prefix) qs.set("action", prefix);
      return api.get(`/api/audit?${qs}`);
    },
    getNextPageParam: (last) => last.next_cursor ?? undefined,
  });
}

const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

/** Human-readable descriptions for audit actions. */
export const AUDIT = {
  "auth.signup": { icon: UserPlus, label: () => "Created your account" },
  "auth.login": { icon: SignIn, label: () => "Signed in" },
  "auth.demo_login": { icon: Sparkle, label: () => "Started a demo session" },
  "auth.refresh_reuse_detected": {
    icon: ShieldWarning,
    tone: "danger",
    label: () => "Blocked a reused session token and signed out other sessions",
  },
  "document.uploaded": {
    icon: FileArrowUp,
    label: (m) => `Uploaded ${m.filename ?? "a document"}`,
  },
  "document.deleted": { icon: Trash, label: (m) => `Deleted ${m.title ?? "a document"}` },
  "document.reprocessed": { icon: ArrowClockwise, label: () => "Reprocessed a document" },
  "extraction.confirmed": {
    icon: CheckCircle,
    label: (m) =>
      `Confirmed ${plural(m.medications ?? 0, "medication")} and ${plural(m.care_actions ?? 0, "to-do")}`,
  },
  "extraction.discarded": { icon: XCircle, label: () => "Discarded an extracted draft" },
  "integration.connected": {
    icon: GoogleLogo,
    label: (m) => `Connected Google${m.mode === "simulation" ? " (simulation)" : ""}`,
  },
  "integration.disconnected": { icon: LinkBreak, label: () => "Disconnected Google" },
  "integration.synced": {
    icon: CalendarCheck,
    label: (m) =>
      `Synced ${plural(m.events ?? 0, "event")} and ${plural(m.tasks ?? 0, "task")} to Google`,
  },
  "integration.unsynced": {
    icon: CalendarX,
    label: (m) => `Removed ${plural(m.removed ?? 0, "item")} from Google`,
  },
  "share.created": {
    icon: LinkSimple,
    label: (m) => `Created a share link${m.label ? `: ${m.label}` : ""}`,
  },
  "share.revoked": { icon: LinkBreak, label: () => "Revoked a share link" },
  "share.viewed": {
    icon: Eye,
    label: (m) => `A share link was viewed${m.label ? `: ${m.label}` : ""}`,
  },
};

export function describeAudit(entry) {
  const def = AUDIT[entry.action];
  return {
    icon: def?.icon ?? ShieldWarning,
    tone: def?.tone,
    label: def ? def.label(entry.meta ?? {}) : entry.action,
  };
}

/** "Chrome on Windows" from a user agent, good enough for an activity log. */
export function deviceFrom(ua = "") {
  if (!ua) return "";
  const browser = /Edg\//.test(ua)
    ? "Edge"
    : /Chrome\//.test(ua)
      ? "Chrome"
      : /Firefox\//.test(ua)
        ? "Firefox"
        : /Safari\//.test(ua)
          ? "Safari"
          : /python-httpx|curl/.test(ua)
            ? "API client"
            : "Browser";
  const os = /Windows/.test(ua)
    ? "Windows"
    : /Mac OS X/.test(ua)
      ? "macOS"
      : /Android/.test(ua)
        ? "Android"
        : /iPhone|iPad/.test(ua)
          ? "iOS"
          : /Linux/.test(ua)
            ? "Linux"
            : "";
  return os ? `${browser} on ${os}` : browser;
}
