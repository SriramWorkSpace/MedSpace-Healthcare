import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/Button";
import { Dialog } from "@/components/ui/Dialog";
import { Field, Input, Select } from "@/components/ui/Field";
import { formatDate } from "@/lib/format";
import { useClearSupply, useRefill, useSetSupply } from "./api";
import { UNITS, formatUnits, leftLabel } from "./format";

/**
 * mode "count": enter what you have now (also edits unit, dose size, warning window).
 * mode "refill": add a refill on top of the current estimate.
 */
export function SupplyDialog({ med, supply, mode, onClose }) {
  const set = useSetSupply();
  const refill = useRefill();
  const clear = useClearSupply();
  const [onHand, setOnHand] = useState(supply ? formatUnits(supply.estimated_left) : "");
  const [unit, setUnit] = useState(
    supply?.unit ?? (med.form === "capsule" ? "capsules" : "tablets"),
  );
  const [perDose, setPerDose] = useState(String(supply?.units_per_dose ?? 1));
  const [lowDays, setLowDays] = useState(String(supply?.low_days ?? 7));
  const [added, setAdded] = useState("");
  const name = `${med.name}${med.strength ? ` ${med.strength}` : ""}`;

  const done = (message) => () => {
    toast(message);
    onClose();
  };
  const fail = (e) => toast.error(e.message);

  const submit = (e) => {
    e.preventDefault();
    if (mode === "refill") {
      refill.mutate(
        { medicationId: med.id, added: Number(added) },
        { onSuccess: done(`Added ${added} ${supply.unit}`), onError: fail },
      );
    } else {
      set.mutate(
        {
          medicationId: med.id,
          on_hand: Number(onHand),
          unit,
          units_per_dose: Number(perDose),
          low_days: Number(lowDays),
        },
        { onSuccess: done("Supply count saved"), onError: fail },
      );
    }
  };

  const pending = set.isPending || refill.isPending;
  const valid =
    mode === "refill"
      ? Number(added) > 0
      : onHand !== "" && Number(onHand) >= 0 && Number(perDose) > 0 && Number(lowDays) >= 1;

  return (
    <Dialog
      open
      onClose={onClose}
      title={mode === "refill" ? `Refill ${name}` : `Supply of ${name}`}
      description={
        mode === "refill"
          ? `${leftLabel(supply)} by the estimate. Add what you picked up.`
          : "Count what you have now. MedSpace subtracts scheduled doses (not ones you mark skipped) to estimate the rest."
      }
      footer={
        <>
          {mode === "count" && supply && (
            <Button
              variant="ghost"
              className="mr-auto"
              loading={clear.isPending}
              onClick={() =>
                clear.mutate(med.id, { onSuccess: done("Stopped tracking supply"), onError: fail })
              }
            >
              Stop tracking
            </Button>
          )}
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="supply-form" loading={pending} disabled={!valid}>
            {mode === "refill" ? "Add refill" : "Save count"}
          </Button>
        </>
      }
    >
      <form id="supply-form" onSubmit={submit} className="grid grid-cols-1 gap-4">
        {mode === "refill" ? (
          <Field label={`Units added (${supply.unit})`}>
            <Input
              type="number"
              inputMode="decimal"
              min="0"
              step="any"
              autoFocus
              value={added}
              onChange={(e) => setAdded(e.target.value)}
            />
          </Field>
        ) : (
          <>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-[1fr_1fr]">
              <Field label="On hand now">
                <Input
                  type="number"
                  inputMode="decimal"
                  min="0"
                  step="any"
                  autoFocus
                  value={onHand}
                  onChange={(e) => setOnHand(e.target.value)}
                />
              </Field>
              <Field label="Unit">
                <Select value={unit} onChange={(e) => setUnit(e.target.value)}>
                  {[...new Set([unit, ...UNITS])].map((u) => (
                    <option key={u} value={u}>
                      {u}
                    </option>
                  ))}
                </Select>
              </Field>
            </div>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-[1fr_1fr]">
              <Field label="Per dose" hint={`${unit} taken each time`}>
                <Input
                  type="number"
                  inputMode="decimal"
                  min="0"
                  step="any"
                  value={perDose}
                  onChange={(e) => setPerDose(e.target.value)}
                />
              </Field>
              <Field label="Warn me" hint="days before it runs out">
                <Input
                  type="number"
                  inputMode="numeric"
                  min="1"
                  max="60"
                  value={lowDays}
                  onChange={(e) => setLowDays(e.target.value)}
                />
              </Field>
            </div>
            {supply && (
              <p className="text-xs text-ink-3">
                Last counted {formatUnits(supply.counted)} {supply.unit} on{" "}
                {formatDate(supply.counted_at)}.
              </p>
            )}
          </>
        )}
      </form>
    </Dialog>
  );
}
