import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { useForm } from "react-hook-form";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  ArrowsClockwise,
  DownloadSimple,
  Egg,
  DeviceMobile,
  UsersThree,
  GoogleLogo,
  LockSimple,
  ShieldCheck,
  Trash,
  User,
} from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { Dialog } from "@/components/ui/Dialog";
import { Field, Input, Select } from "@/components/ui/Field";
import { Skeleton } from "@/components/ui/Skeleton";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { api } from "@/lib/api";
import { useAuth, meKey } from "@/lib/auth";
import { formatDate, timeAgo } from "@/lib/format";
import { queryClient } from "@/lib/queryClient";
import { cn } from "@/lib/cn";
import { EGGS, useEasterEggs } from "@/easter-eggs/EasterEggs";
import {
  connectGoogle,
  useDisconnectGoogle,
  useGoogleStatus,
  usePullTasks,
} from "@/features/integrations/api";
import { describeAudit, deviceFrom, useAuditLog } from "@/features/settings/audit";
import { DeviceSettings } from "@/features/offline/DeviceSettings";
import { CareCircleSettings } from "@/features/circle/CareCircleSettings";

const SECTIONS = [
  { id: "profile", label: "Profile", icon: User },
  { id: "integrations", label: "Integrations", icon: GoogleLogo },
  { id: "device", label: "This device", icon: DeviceMobile },
  { id: "circle", label: "Care circle", icon: UsersThree },
  { id: "activity", label: "Activity", icon: ShieldCheck },
  { id: "eggs", label: "Easter eggs", icon: Egg },
  { id: "danger", label: "Account", icon: LockSimple },
];

const SLOTS = [
  ["morning", "Morning"],
  ["afternoon", "Afternoon"],
  ["evening", "Evening"],
  ["bedtime", "Bedtime"],
];

function Section({ id, title, description, children }) {
  return (
    <section id={id} className="scroll-mt-[calc(var(--nav-h)+24px)]">
      <h2 className="text-lg font-semibold">{title}</h2>
      {description && <p className="mt-1 text-sm text-ink-2">{description}</p>}
      <div className="mt-4">{children}</div>
    </section>
  );
}

function ProfileForm() {
  const { user } = useAuth();
  const zones = useMemo(() => {
    let list = [];
    try {
      list = Intl.supportedValuesOf("timeZone");
    } catch {
      /* older browsers */
    }
    // Intl omits "UTC"; always keep the saved zone selectable.
    return [...new Set(["UTC", user.timezone, ...list])];
  }, [user.timezone]);
  const form = useForm({
    defaultValues: {
      display_name: user.display_name,
      timezone: user.timezone,
      dose_times: user.dose_times,
    },
  });
  const save = useMutation({
    mutationFn: (body) => api.patch("/api/me", body),
    onSuccess: (u) => {
      queryClient.setQueryData(meKey, u);
      form.reset({ display_name: u.display_name, timezone: u.timezone, dose_times: u.dose_times });
      toast.success("Profile saved");
    },
    onError: (e) => toast.error(e.message),
  });

  return (
    <form
      onSubmit={form.handleSubmit((v) => save.mutate(v))}
      className="card card--flat grid grid-cols-1 gap-5 p-5 sm:grid-cols-2"
    >
      <div className="flex flex-wrap items-center gap-2 text-sm text-ink-2 sm:col-span-2">
        <span className="font-medium text-ink">Sign-in:</span>
        {user.google_linked && (
          <Chip tone="accent">
            <GoogleLogo size={12} weight="bold" /> Google
          </Chip>
        )}
        {user.has_password && <Chip>Email and password</Chip>}
        <span className="truncate text-ink-3">{user.email}</span>
      </div>
      <Field label="Name">
        <Input {...form.register("display_name", { required: true, maxLength: 80 })} />
      </Field>
      <Field label="Time zone" hint="Used for today's doses and calendar reminders.">
        <Select {...form.register("timezone")}>
          {zones.map((z) => (
            <option key={z} value={z}>
              {z.replaceAll("_", " ")}
            </option>
          ))}
        </Select>
      </Field>
      <div className="sm:col-span-2">
        <p className="field__label">Preferred dose times</p>
        <p className="field__hint mb-3">
          Shorthand like BD or 1-0-1 becomes these clock times for new prescriptions.
        </p>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {SLOTS.map(([key, label]) => (
            <Field key={key} label={label}>
              <Input type="time" {...form.register(`dose_times.${key}`)} />
            </Field>
          ))}
        </div>
      </div>
      <div className="flex justify-end sm:col-span-2">
        <Button type="submit" loading={save.isPending} disabled={!form.formState.isDirty}>
          Save changes
        </Button>
      </div>
    </form>
  );
}

function GoogleCard() {
  const { user } = useAuth();
  const status = useGoogleStatus();
  const disconnect = useDisconnectGoogle();
  const pull = usePullTasks();
  const [askDisconnect, setAskDisconnect] = useState(false);
  const s = status.data;

  if (status.isPending) return <Skeleton className="h-28 rounded-card" />;
  return (
    <div className="card card--flat flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-start gap-4">
        <span className="grid grid-cols-1 size-11 shrink-0 place-items-center rounded-2xl bg-surface-2">
          <GoogleLogo size={22} weight="bold" />
        </span>
        <div>
          <p className="flex flex-wrap items-center gap-2 font-semibold">
            Google Calendar &amp; Tasks
            {s.connected ? (
              <Chip tone="accent">Connected</Chip>
            ) : s.status === "revoked" ? (
              <Chip tone="danger">Reconnect needed</Chip>
            ) : (
              <Chip>Not connected</Chip>
            )}
            {s.mode === "simulation" && <Chip>Simulation</Chip>}
          </p>
          <p className="mt-1 text-sm text-ink-2">
            {s.connected
              ? `${s.email ?? "Google account"} · connected ${timeAgo(s.connected_at)}`
              : user.google_linked
                ? "You sign in with Google. Connect Calendar and Tasks to get dose reminders and to-dos."
                : "Recurring dose reminders in Calendar, one-off to-dos in Tasks."}
          </p>
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        {s.connected ? (
          <>
            <Button
              variant="ghost"
              size="sm"
              loading={pull.isPending}
              onClick={() =>
                pull.mutate(undefined, {
                  onSuccess: (r) =>
                    toast(
                      r.updated
                        ? `Marked ${r.updated} to-do${r.updated === 1 ? "" : "s"} done from Google Tasks`
                        : "Everything's already up to date",
                    ),
                })
              }
            >
              <ArrowsClockwise size={14} /> Check Tasks
            </Button>
            <Button variant="secondary" size="sm" onClick={() => setAskDisconnect(true)}>
              Disconnect
            </Button>
          </>
        ) : (
          <Button size="sm" onClick={connectGoogle}>
            Connect Google
          </Button>
        )}
      </div>
      <Dialog
        open={askDisconnect}
        onClose={() => setAskDisconnect(false)}
        title="Disconnect Google?"
        description="MedSpace will stop syncing and revoke its access."
        size="sm"
        footer={
          <>
            <Button
              variant="ghost"
              loading={disconnect.isPending && disconnect.variables === false}
              onClick={() => disconnect.mutate(false, { onSuccess: () => setAskDisconnect(false) })}
            >
              Keep synced items
            </Button>
            <Button
              variant="danger"
              loading={disconnect.isPending && disconnect.variables === true}
              onClick={() => disconnect.mutate(true, { onSuccess: () => setAskDisconnect(false) })}
            >
              Remove them too
            </Button>
          </>
        }
      >
        <p className="text-sm text-ink-2">
          You can keep the events and tasks already in Google, or have MedSpace remove the ones it
          created.
        </p>
      </Dialog>
    </div>
  );
}

function ActivityLog() {
  const { data, isPending, fetchNextPage, hasNextPage, isFetchingNextPage } = useAuditLog();
  const items = data?.pages.flatMap((p) => p.items) ?? [];
  if (isPending) {
    return (
      <div className="card card--flat grid grid-cols-1 gap-3 p-5">
        {[0, 1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-10" />
        ))}
      </div>
    );
  }
  return (
    <div className="card card--flat overflow-hidden">
      <ul className="divide-y divide-line">
        {items.map((e) => {
          const { icon: Icon, label, tone } = describeAudit(e);
          return (
            <li key={e.id} className="flex items-center gap-3 px-5 py-3">
              <span
                className={cn(
                  "grid size-8 shrink-0 place-items-center rounded-lg",
                  tone === "danger" ? "bg-danger-soft text-danger-ink" : "bg-surface-2 text-ink-2",
                )}
              >
                <Icon size={16} />
              </span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-medium">{label}</span>
                <span className="block truncate text-xs text-ink-3">
                  {[deviceFrom(e.user_agent), e.ip, e.actor === "public" ? "via share link" : null]
                    .filter(Boolean)
                    .join(" · ")}
                </span>
              </span>
              <time
                className="shrink-0 text-xs text-ink-3"
                dateTime={e.created_at}
                title={formatDate(e.created_at, "PPpp")}
              >
                {timeAgo(e.created_at)}
              </time>
            </li>
          );
        })}
      </ul>
      {hasNextPage && (
        <div className="border-t border-line p-3 text-center">
          <Button
            variant="ghost"
            size="sm"
            loading={isFetchingNextPage}
            onClick={() => fetchNextPage()}
          >
            Show older activity
          </Button>
        </div>
      )}
    </div>
  );
}

function EggTracker() {
  const { found, total } = useEasterEggs();
  const hints = {
    konami: "A classic code from 1986",
    apple: "Type a fruit that keeps the doctor away",
    logo: "Show the logo some enthusiasm",
    notFound: "Get a little lost",
    themeFlip: "Can't decide between light and dark?",
  };
  return (
    <div className="card card--flat p-5">
      <p className="text-sm text-ink-2">
        <span className="tabular font-semibold text-ink">{found.length}</span> of {total} found.{" "}
        {found.length === total
          ? "Full marks. The doctor will see you never."
          : "Laughter is the best medicine."}
      </p>
      <ul className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
        {Object.keys(EGGS).map((id) => {
          const got = found.includes(id);
          return (
            <li
              key={id}
              className={cn(
                "flex items-center gap-2.5 rounded-[var(--radius-control)] px-3 py-2.5 text-sm",
                got ? "bg-accent-soft text-accent-soft-ink" : "bg-surface-2 text-ink-3",
              )}
            >
              <Egg size={16} weight={got ? "fill" : "regular"} />
              {got ? EGGS[id] : hints[id]}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

function DangerZone() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const del = useMutation({
    mutationFn: () => api.delete("/api/me"),
    onSuccess: () => {
      queryClient.clear();
      queryClient.setQueryData(meKey, null);
      navigate("/", { replace: true });
      toast("Your account and documents were deleted.");
    },
  });
  return (
    <div className="card card--flat flex flex-col gap-4 border-danger/30 p-5 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="font-semibold">Your data</p>
        <p className="text-sm text-ink-2">
          Export everything as JSON, or delete your documents, records, conversations, share links
          and Google connection for good.
          {user.is_demo && " Demo accounts are also removed automatically after 24 hours."}
        </p>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button as="a" href="/api/me/export" variant="secondary">
          <DownloadSimple size={15} /> Download my data
        </Button>
        <Button variant="danger" onClick={() => setOpen(true)}>
          <Trash size={15} /> Delete account
        </Button>
      </div>
      <ConfirmDialog
        open={open}
        onClose={() => setOpen(false)}
        title="Delete everything?"
        description="This permanently deletes your account and every file in it. There's no undo."
        confirmLabel="Delete my account"
        loading={del.isPending}
        onConfirm={() => del.mutate()}
      />
    </div>
  );
}

export default function Settings() {
  const [params, setParams] = useSearchParams();

  // Arriving with #device (from the offline banner) or another section anchor.
  useEffect(() => {
    const id = window.location.hash.slice(1);
    if (id) document.getElementById(id)?.scrollIntoView({ block: "start" });
  }, []);

  // Result of the Google OAuth round trip.
  useEffect(() => {
    const result = params.get("google");
    if (!result) return;
    const messages = {
      connected: [
        "success",
        "Google connected",
        "You can now add prescriptions to Calendar and Tasks.",
      ],
      denied: ["error", "Google wasn't connected", "Permission was declined."],
      expired: ["error", "That took a little too long", "Please try connecting again."],
      error: ["error", "Couldn't connect Google", "Please try again in a moment."],
    };
    const [kind, title, description] = messages[result] ?? messages.error;
    toast[kind](title, { description });
    params.delete("google");
    setParams(params, { replace: true });
  }, [params, setParams]);

  return (
    <>
      <PageHeader
        title="Settings"
        description="Your profile, connections and a record of everything that happened."
      />
      <div className="grid grid-cols-1 gap-10 lg:grid-cols-[200px_minmax(0,1fr)]">
        <nav aria-label="Settings sections" className="hidden lg:block">
          <ul className="sticky top-[calc(var(--nav-h)+24px)] grid grid-cols-1 gap-0.5">
            {SECTIONS.map(({ id, label, icon: Icon }) => (
              <li key={id}>
                <a
                  href={`#${id}`}
                  className="flex items-center gap-2.5 rounded-[var(--radius-control)] px-3 py-2 text-sm text-ink-2 transition-colors hover:bg-surface-2 hover:text-ink"
                >
                  <Icon size={16} /> {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <div className="grid grid-cols-1 max-w-3xl gap-12">
          <Section id="profile" title="Profile">
            <ProfileForm />
          </Section>
          <Section
            id="integrations"
            title="Integrations"
            description="Optional. Only confirmed records are ever synced."
          >
            <GoogleCard />
          </Section>
          <Section
            id="circle"
            title="Care circle"
            description="Let a family member or carer see your records, or help by ticking doses. You can change or end access at any time."
          >
            <CareCircleSettings />
          </Section>
          <Section
            id="device"
            title="This device"
            description="Install the app and choose whether this browser keeps an offline copy."
          >
            <DeviceSettings />
          </Section>
          <Section
            id="activity"
            title="Activity"
            description="Sign-ins, uploads, confirmations, syncs and share-link views."
          >
            <ActivityLog />
          </Section>
          <Section id="eggs" title="Easter eggs" description="Some things are just for fun.">
            <EggTracker />
          </Section>
          <Section id="danger" title="Account">
            <DangerZone />
          </Section>
        </div>
      </div>
    </>
  );
}
