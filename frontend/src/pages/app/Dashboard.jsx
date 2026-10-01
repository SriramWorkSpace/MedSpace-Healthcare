import { Link } from "react-router";
import { UploadSimple, FileText } from "@phosphor-icons/react";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/layout/PageSkeleton";
import { useAuth } from "@/lib/auth";
import { firstName, greeting } from "@/lib/format";
import { EMPTY_QUIPS } from "@/easter-eggs/puns";

export default function Dashboard() {
  const { user } = useAuth();
  return (
    <>
      <PageHeader
        title={`${greeting()}, ${firstName(user.display_name)}.`}
        description="Here's what your records say about today."
      />
      <EmptyState
        icon={FileText}
        title="Start with your first prescription"
        description="Upload a PDF or a photo. We'll pull out the medicines and schedule so you can review them."
        action={
          <Button as={Link} to="/app/documents?upload=1">
            <UploadSimple size={15} weight="bold" /> Upload a document
          </Button>
        }
        quip={EMPTY_QUIPS.documents}
      />
    </>
  );
}
