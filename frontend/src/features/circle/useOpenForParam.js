import { useEffect } from "react";
import { useSearchParams } from "react-router";
import { useActing, useCircle, useSwitchProfile } from "./api";

/**
 * `/app?for=<person id>` (the link on a caregiver's dose alert, ADR-032) opens that person's
 * records, but only if the signed-in user actively helps them. The parameter is then removed.
 */
export function useOpenForParam(ready) {
  const [params, setParams] = useSearchParams();
  const target = params.get("for");
  const circle = useCircle({ enabled: Boolean(target && ready) });
  const switchProfile = useSwitchProfile();
  const { acting } = useActing();

  useEffect(() => {
    if (!target || !circle.data) return;
    const link = circle.data.caring_for.find(
      (c) => c.person.id === target && c.status === "active",
    );
    if (link && acting?.id !== target) switchProfile({ ...link.person, role: link.role });
    const next = new URLSearchParams(params);
    next.delete("for");
    setParams(next, { replace: true });
  }, [target, circle.data, acting?.id, switchProfile, params, setParams]);
}
