import { forwardRef } from "react";
import { cn } from "@/lib/cn";

/**
 * @param {{ variant?: "primary"|"secondary"|"ghost"|"danger"|"ink", size?: "sm"|"md"|"lg",
 *   icon?: boolean, loading?: boolean, as?: any } & Record<string, any>} props
 */
export const Button = forwardRef(function Button(
  {
    variant = "primary",
    size = "md",
    icon = false,
    loading = false,
    as: Comp = "button",
    className,
    children,
    disabled,
    ...props
  },
  ref,
) {
  const isButton = Comp === "button";
  return (
    <Comp
      ref={ref}
      className={cn(
        "btn",
        `btn--${variant}`,
        size !== "md" && `btn--${size}`,
        icon && "btn--icon",
        className,
      )}
      type={isButton ? (props.type ?? "button") : undefined}
      disabled={isButton ? disabled || loading : undefined}
      aria-disabled={!isButton && disabled ? true : undefined}
      aria-busy={loading || undefined}
      {...props}
    >
      {loading && <span className="btn__spinner" aria-hidden />}
      {children}
    </Comp>
  );
});
