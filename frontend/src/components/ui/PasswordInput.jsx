import { useState } from "react";
import { Eye, EyeSlash } from "@phosphor-icons/react";
import { Input } from "./Field";

export function PasswordInput(props) {
  const [visible, setVisible] = useState(false);
  return (
    <div className="relative">
      <Input type={visible ? "text" : "password"} className="pr-11" {...props} />
      <button
        type="button"
        onClick={() => setVisible((v) => !v)}
        aria-label={visible ? "Hide password" : "Show password"}
        className="absolute right-1.5 top-1/2 grid grid-cols-1 size-8 -translate-y-1/2 place-items-center rounded-lg text-ink-3 hover:text-ink"
      >
        {visible ? <EyeSlash size={17} /> : <Eye size={17} />}
      </button>
    </div>
  );
}

/** Six-digit authenticator code: numeric keypad on phones, autofill from SMS/OS where offered. */
export function CodeInput(props) {
  return (
    <Input
      inputMode="numeric"
      autoComplete="one-time-code"
      pattern="[0-9 ]*"
      maxLength={7}
      placeholder="123456"
      className="font-mono tracking-[0.2em]"
      {...props}
    />
  );
}
