import { Wrench } from "@phosphor-icons/react";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "./PageSkeleton";

/** Temporary page body for routes whose feature phase has not landed yet. */
export function ComingSoon({ title, description }) {
  return (
    <>
      <PageHeader title={title} description={description} />
      <EmptyState
        icon={Wrench}
        title="In the operating room"
        description="This part of MedSpace is being built right now."
      />
    </>
  );
}
