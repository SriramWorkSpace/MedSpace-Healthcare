import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router";
import { AnimatePresence, motion } from "motion/react";
import { GearSix, SignOut, ShieldCheck } from "@phosphor-icons/react";
import { useAuth } from "@/lib/auth";

function initials(name = "") {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase())
    .join("");
}

export function UserMenu() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!open) return;
    const onDown = (e) => !ref.current?.contains(e.target) && setOpen(false);
    const onKey = (e) => e.key === "Escape" && setOpen(false);
    document.addEventListener("pointerdown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  if (!user) return null;

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label="Account menu"
        onClick={() => setOpen((v) => !v)}
        className="grid grid-cols-1 size-8 place-items-center rounded-full bg-accent-soft text-[12px] font-semibold text-accent-soft-ink ring-1 ring-line transition-transform duration-150 active:scale-95"
      >
        {initials(user.display_name)}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            role="menu"
            initial={{ opacity: 0, scale: 0.96, y: -4 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, transition: { duration: 0.12 } }}
            transition={{ duration: 0.18, ease: [0.23, 1, 0.32, 1] }}
            style={{ transformOrigin: "top right" }}
            className="card absolute right-0 top-11 w-64 overflow-hidden p-1.5 shadow-md"
          >
            <div className="px-3 py-2.5">
              <p className="truncate text-sm font-semibold">{user.display_name}</p>
              <p className="truncate text-xs text-ink-3">
                {user.is_demo ? "Demo account · synthetic data" : user.email}
              </p>
            </div>
            <div className="my-1 h-px bg-line" />
            <MenuItem as={Link} to="/app/settings" icon={GearSix} onClick={() => setOpen(false)}>
              Settings
            </MenuItem>
            <MenuItem
              as={Link}
              to="/app/settings#activity"
              icon={ShieldCheck}
              onClick={() => setOpen(false)}
            >
              Activity log
            </MenuItem>
            <MenuItem
              icon={SignOut}
              onClick={async () => {
                setOpen(false);
                await logout().catch(() => {});
                navigate("/login", { replace: true });
              }}
            >
              Sign out
            </MenuItem>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function MenuItem({ as: Comp = "button", icon: Icon, children, ...props }) {
  return (
    <Comp
      role="menuitem"
      type={Comp === "button" ? "button" : undefined}
      className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-left text-sm text-ink-2 transition-colors hover:bg-surface-2 hover:text-ink focus-visible:bg-surface-2"
      {...props}
    >
      <Icon size={16} />
      {children}
    </Comp>
  );
}
