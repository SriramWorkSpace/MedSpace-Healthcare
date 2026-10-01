import { isRouteErrorResponse, Link, useRouteError } from "react-router";
import { FirstAidKit } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import NotFound from "@/pages/NotFound";

export default function RouteError() {
  const error = useRouteError();
  if (isRouteErrorResponse(error) && error.status === 404) return <NotFound />;

  if (import.meta.env.DEV) console.error(error);
  return (
    <div className="grid min-h-[70dvh] place-items-center px-4 text-center">
      <div className="max-w-md">
        <div className="mx-auto grid size-14 place-items-center rounded-2xl bg-danger-soft text-danger-ink">
          <FirstAidKit size={26} weight="duotone" />
        </div>
        <h1 className="mt-6 text-2xl font-semibold">Something needs a quick check-up</h1>
        <p className="mt-2 text-ink-2">
          This screen hit an unexpected error. Reloading usually does the trick.
        </p>
        <div className="mt-6 flex justify-center gap-2">
          <Button onClick={() => window.location.reload()}>Reload</Button>
          <Button as={Link} to="/app" variant="secondary">
            Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}
