import { useMemo, useState } from "react";
import { useSearchParams } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { toast } from "sonner";
import { formatDistanceToNowStrict, parseISO } from "date-fns";
import {
  Check,
  Copy,
  Eye,
  ClipboardText,
  FileText,
  LinkBreak,
  LinkSimple,
  Plus,
  Prescription,
  ShareNetwork,
  ShieldCheck,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { Dialog } from "@/components/ui/Dialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { Field, Input, Select } from "@/components/ui/Field";
import { LoadingRegion, Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";
import { useDocuments } from "@/features/documents/api";
import { usePrescriptions } from "@/features/records/api";
import { useCreateShare, useRevokeShare, useShares } from "@/features/sharing/api";
import { formatDate } from "@/lib/format";
import { cn } from "@/lib/cn";
import { useVisits } from "@/features/visits/api";

const STATUS = {
  active: { tone: "accent", label: "Active" },
  expired: { tone: "neutral", label: "Expired" },
  revoked: { tone: "danger", label: "Revoked" },
  exhausted: { tone: "warn", label: "View limit reached" },
};

function CopyField({ value }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      toast.error("Copy failed. Select the link and copy it manually.");
    }
  };
  return (
    <div className="flex items-center gap-2 rounded-[var(--radius-control)] border border-line-strong bg-surface-2 p-1.5 pl-3">
      <LinkSimple size={16} className="shrink-0 text-ink-3" />
      <input
        readOnly
        value={value}
        onFocus={(e) => e.target.select()}
        aria-label="Share link"
        className="min-w-0 flex-1 bg-transparent font-mono text-[13px] outline-none"
      />
      <Button size="sm" onClick={copy} aria-live="polite">
        <AnimatePresence mode="wait" initial={false}>
          <motion.span
            key={copied ? "y" : "n"}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.15 }}
            className="inline-flex items-center gap-1.5"
          >
            {copied ? <Check size={14} weight="bold" /> : <Copy size={14} />}
            {copied ? "Copied" : "Copy"}
          </motion.span>
        </AnimatePresence>
      </Button>
    </div>
  );
}

function CreateShareDialog({ open, onClose, preselect }) {
  const rx = usePrescriptions();
  const docs = useDocuments({ status: "confirmed" });
  const create = useCreateShare();
  const visits = useVisits();
  const [label, setLabel] = useState("");
  const [days, setDays] = useState("7");
  const [maxViews, setMaxViews] = useState("");
  const [selected, setSelected] = useState(() => new Set(preselect ? [preselect] : []));
  const [created, setCreated] = useState(null);

  // Documents already covered by a prescription are offered through the prescription.
  const options = useMemo(() => {
    const rxDocIds = new Set((rx.data ?? []).map((p) => p.document_id));
    return [
      ...(visits.data ?? []).map((v) => ({
        key: `visit:${v.id}`,
        type: "visit",
        id: v.id,
        title: `Visit brief: ${v.title}`,
        meta: v.visit_date ? formatDate(v.visit_date) : "",
      })),
      ...(rx.data ?? []).map((p) => ({
        key: `prescription:${p.id}`,
        type: "prescription",
        id: p.id,
        title: `Prescription from ${p.prescriber_name || p.clinic_name || "your prescriber"}`,
        meta: p.issued_on ? formatDate(p.issued_on) : "",
      })),
      ...(docs.data?.items ?? [])
        .filter((d) => !rxDocIds.has(d.id))
        .map((d) => ({
          key: `document:${d.id}`,
          type: "document",
          id: d.id,
          title: d.title,
          meta: d.document_date ? formatDate(d.document_date) : "",
        })),
    ];
  }, [rx.data, docs.data, visits.data]);

  const toggle = (key) =>
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });

  const submit = () =>
    create.mutate(
      {
        label: label.trim() || "Shared records",
        expires_in_days: Number(days),
        max_views: maxViews ? Number(maxViews) : null,
        items: options.filter((o) => selected.has(o.key)).map((o) => ({ type: o.type, id: o.id })),
      },
      { onSuccess: setCreated, onError: (e) => toast.error(e.message) },
    );

  if (created) {
    return (
      <Dialog
        open={open}
        onClose={onClose}
        title="Your link is ready"
        description="Copy it now. For your security we only store a fingerprint of it, so it can't be shown again."
        footer={<Button onClick={onClose}>Done</Button>}
      >
        <CopyField value={created.url} />
        <p className="mt-3 flex items-center gap-1.5 text-xs text-ink-3">
          <ShieldCheck size={14} /> Expires{" "}
          {formatDate(created.share.expires_at, "MMM d 'at' h:mm a")}
          {created.share.max_views && ` · ${created.share.max_views} view limit`}
        </p>
      </Dialog>
    );
  }

  return (
    <Dialog
      open={open}
      onClose={onClose}
      title="Share records"
      description="Recipients see a read-only view. You can revoke it any time."
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={submit} loading={create.isPending} disabled={!selected.size}>
            Create link
          </Button>
        </>
      }
    >
      <div className="grid grid-cols-1 gap-5">
        <Field label="Label" hint="Only you see this. It helps you tell links apart.">
          <Input
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            placeholder="For Dr. Reyes"
            maxLength={120}
          />
        </Field>
        <div>
          <p className="field__label mb-2">What to include</p>
          {rx.isPending || docs.isPending ? (
            <Skeleton className="h-28" />
          ) : options.length === 0 ? (
            <p className="text-sm text-ink-2">
              Confirm a document first. Only confirmed records can be shared.
            </p>
          ) : (
            <ul className="grid grid-cols-1 max-h-60 gap-1.5 overflow-y-auto pr-1">
              {options.map((o) => {
                const Icon =
                  o.type === "prescription"
                    ? Prescription
                    : o.type === "visit"
                      ? ClipboardText
                      : FileText;
                const on = selected.has(o.key);
                return (
                  <li key={o.key}>
                    <label
                      className={cn(
                        "flex cursor-pointer items-center gap-3 rounded-[var(--radius-control)] border px-3 py-2.5 transition-colors",
                        on
                          ? "border-accent/50 bg-accent-soft/40"
                          : "border-line hover:bg-surface-2",
                      )}
                    >
                      <input
                        type="checkbox"
                        checked={on}
                        onChange={() => toggle(o.key)}
                        className="size-4 accent-[var(--accent)]"
                      />
                      <Icon size={17} weight="duotone" className="text-accent" />
                      <span className="min-w-0 flex-1 truncate text-sm font-medium">{o.title}</span>
                      <span className="shrink-0 text-xs text-ink-3">{o.meta}</span>
                    </label>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Expires after">
            <Select value={days} onChange={(e) => setDays(e.target.value)}>
              {[1, 3, 7, 14, 30].map((d) => (
                <option key={d} value={d}>
                  {d} day{d === 1 ? "" : "s"}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="View limit">
            <Select value={maxViews} onChange={(e) => setMaxViews(e.target.value)}>
              <option value="">No limit</option>
              {[1, 3, 5, 10].map((n) => (
                <option key={n} value={n}>
                  {n} view{n === 1 ? "" : "s"}
                </option>
              ))}
            </Select>
          </Field>
        </div>
      </div>
    </Dialog>
  );
}

function ShareCard({ link, onRevoke, index }) {
  const meta = STATUS[link.status];
  const active = link.status === "active";
  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: Math.min(index, 6) * 0.04, ease: [0.23, 1, 0.32, 1] }}
      className={cn(
        "card flex flex-wrap items-center gap-x-4 gap-y-3 p-5 sm:flex-nowrap",
        !active && "opacity-75",
      )}
    >
      <span
        className={cn(
          "grid size-11 shrink-0 place-items-center rounded-xl",
          active ? "bg-accent-soft text-accent-soft-ink" : "bg-surface-2 text-ink-3",
        )}
      >
        {active ? <LinkSimple size={20} weight="bold" /> : <LinkBreak size={20} />}
      </span>
      <div className="min-w-0 flex-1">
        <p className="flex flex-wrap items-center gap-2 font-semibold">
          {link.label}
          <Chip tone={meta.tone}>{meta.label}</Chip>
        </p>
        <p className="mt-1 truncate text-sm text-ink-2">
          {link.items.map((i) => i.title).join(", ")}
        </p>
        <p className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-ink-3">
          <span className="font-mono">…{link.token_hint}</span>
          <span className="inline-flex items-center gap-1">
            <Eye size={13} /> {link.view_count}
            {link.max_views ? ` of ${link.max_views}` : ""} view
            {link.view_count === 1 && !link.max_views ? "" : "s"}
          </span>
          <span>
            {active
              ? `Expires in ${formatDistanceToNowStrict(parseISO(link.expires_at))}`
              : link.revoked_at
                ? `Revoked ${formatDate(link.revoked_at, "MMM d")}`
                : `Ended ${formatDate(link.expires_at, "MMM d")}`}
          </span>
        </p>
      </div>
      {active && (
        <Button
          variant="secondary"
          size="sm"
          className="max-sm:w-full"
          onClick={() => onRevoke(link)}
        >
          <LinkBreak size={14} /> Revoke
        </Button>
      )}
    </motion.li>
  );
}

export default function Sharing() {
  const [params, setParams] = useSearchParams();
  const preselect = params.get("prescription")
    ? `prescription:${params.get("prescription")}`
    : params.get("visit")
      ? `visit:${params.get("visit")}`
      : null;
  const [creating, setCreating] = useState(() => Boolean(preselect));
  const [revoking, setRevoking] = useState(null);
  const shares = useShares();
  const revoke = useRevokeShare();

  const closeCreate = () => {
    setCreating(false);
    if (preselect) setParams({}, { replace: true });
  };

  return (
    <>
      <PageHeader
        title="Sharing"
        description="Temporary, read-only links for a caregiver or a new doctor. Every view is logged."
        actions={
          <Button onClick={() => setCreating(true)}>
            <Plus size={15} weight="bold" /> New link
          </Button>
        }
      />
      {shares.isPending ? (
        <LoadingRegion label="Loading share links" className="grid grid-cols-1 gap-3">
          {[0, 1, 2].map((i) => (
            <Skeleton key={i} className="h-24 rounded-card" />
          ))}
        </LoadingRegion>
      ) : shares.data.length === 0 ? (
        <EmptyState
          icon={ShareNetwork}
          title="No share links yet"
          description="Pick a prescription or report, set an expiry, and send the link. You can revoke it whenever you like."
          action={
            <Button onClick={() => setCreating(true)}>
              <Plus size={15} weight="bold" /> Create a link
            </Button>
          }
          quip={EMPTY_QUIPS.shares}
        />
      ) : (
        <ul className="grid grid-cols-1 gap-3">
          {shares.data.map((link, i) => (
            <ShareCard key={link.id} link={link} index={i} onRevoke={setRevoking} />
          ))}
        </ul>
      )}

      {creating && <CreateShareDialog open onClose={closeCreate} preselect={preselect} />}
      <ConfirmDialog
        open={Boolean(revoking)}
        onClose={() => setRevoking(null)}
        title="Revoke this link?"
        description="Anyone with the link loses access immediately. This can't be undone, but you can always create a new link."
        confirmLabel="Revoke link"
        loading={revoke.isPending}
        onConfirm={() =>
          revoke.mutate(revoking.id, {
            onSuccess: () => {
              setRevoking(null);
              toast("Link revoked");
            },
          })
        }
      />
    </>
  );
}
