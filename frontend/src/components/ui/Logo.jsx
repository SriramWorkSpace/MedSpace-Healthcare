import { cn } from "@/lib/cn";

/** The MedSpace mark (public/brand). A light-ink copy is swapped in on the dark theme. */
export function LogoMark({ size = 28, className }) {
  const img = (variant, file) => (
    <img
      src={`/brand/${file}`}
      srcSet={`/brand/${file.replace("128", "64")} 64w, /brand/${file} 128w`}
      sizes={`${size}px`}
      width={size}
      height={size}
      alt=""
      draggable={false}
      className={`logo-mark--${variant} size-full`}
    />
  );
  return (
    <span
      aria-hidden
      className={cn("block shrink-0", className)}
      style={{ width: size, height: size }}
    >
      {img("light", "logo-mark-128.png")}
      {img("dark", "logo-mark-128-dark.png")}
    </span>
  );
}

/** Mark plus the Zen Dots wordmark: "Med" in the logo's red, "Space" in its black. */
export function Logo({ className, size = 30 }) {
  return (
    <span className={cn("inline-flex items-center gap-2", className)}>
      <LogoMark size={size} />
      <span className="font-brand text-[17px] leading-none tracking-[0.01em]">
        <span className="text-[var(--brand-med)]">Med</span>
        <span className="text-[var(--brand-space)]">Space</span>
      </span>
    </span>
  );
}
