import { cloneElement, forwardRef, isValidElement, useId } from "react";
import { cn } from "@/lib/cn";

/** Label above, control, then hint or error below. Wires up ids and aria automatically. */
export function Field({ label, hint, error, children, className, optional }) {
  const id = useId();
  const hintId = hint ? `${id}-hint` : undefined;
  const errorId = error ? `${id}-error` : undefined;
  const control = isValidElement(children)
    ? cloneElement(children, {
        id: children.props.id ?? id,
        "aria-invalid": error ? true : undefined,
        "aria-describedby": [errorId, hintId].filter(Boolean).join(" ") || undefined,
      })
    : children;

  return (
    <div className={cn("field", className)}>
      {label && (
        <label htmlFor={children?.props?.id ?? id} className="field__label">
          {label}
          {optional && <span className="ml-1 font-normal text-ink-3">(optional)</span>}
        </label>
      )}
      {control}
      {error ? (
        <p id={errorId} className="field__error" role="alert">
          {error}
        </p>
      ) : hint ? (
        <p id={hintId} className="field__hint">
          {hint}
        </p>
      ) : null}
    </div>
  );
}

export const Input = forwardRef(function Input({ className, ...props }, ref) {
  return <input ref={ref} className={cn("input", className)} {...props} />;
});

export const Textarea = forwardRef(function Textarea({ className, rows = 3, ...props }, ref) {
  return <textarea ref={ref} rows={rows} className={cn("input", className)} {...props} />;
});

export const Select = forwardRef(function Select({ className, children, ...props }, ref) {
  return (
    <select ref={ref} className={cn("input appearance-none pr-8", className)} {...props}>
      {children}
    </select>
  );
});
