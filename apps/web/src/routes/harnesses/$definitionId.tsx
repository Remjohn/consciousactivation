import { createFileRoute, Link } from "@tanstack/react-router";
import { useHarnessDetail } from "../../hooks/useHarnessDetail";
import { useHarnessEligibility } from "../../hooks/useHarnessEligibility";
import { ModeBadge } from "../../components/harness/ModeBadge";
import { CategoryBadge } from "../../components/harness/CategoryBadge";
import { CertificationBadges } from "../../components/harness/CertificationBadges";
import { EligibilityBadge } from "../../components/harness/EligibilityBadge";
import { ContractPanel } from "../../components/harness/ContractPanel";
import { GovernancePanel } from "../../components/harness/GovernancePanel";
import { HarnessNotFoundPanel } from "../../components/harness/HarnessNotFoundPanel";
import { HarnessLibraryErrorState } from "../../components/harness/HarnessLibraryErrorState";

export const Route = createFileRoute("/harnesses/$definitionId")({
  component: HarnessDetailPage,
});

function HarnessDetailPage() {
  const { definitionId } = Route.useParams();
  const { sourceCategory } = Route.useSearch() as { sourceCategory?: string };
  const { data, isLoading, isError, error } = useHarnessDetail(definitionId);
  const eligibility = useHarnessEligibility(definitionId, sourceCategory, data?.mode ?? "generic");

  if (isError && error.status === 404) return <HarnessNotFoundPanel />;
  if (isError) return <HarnessLibraryErrorState error={error} />;
  if (isLoading || !data) return <div className="p-8 text-muted-foreground">Loading…</div>;

  return (
    <div className="p-8">
      <Link to="/harnesses" search={(prev) => prev} className="text-sm text-accent">
        ← Back to library
      </Link>
      <div className="mt-2 flex items-center gap-2">
        <h1 className="text-2xl font-semibold text-foreground">{data.task_id}</h1>
        <ModeBadge mode={data.mode} />
        <CategoryBadge categoryName={data.category_name} />
        {sourceCategory && data.mode === "generic" && <EligibilityBadge status="NOT_APPLICABLE" />}
        {eligibility.data && <EligibilityBadge status={eligibility.data.status} />}
      </div>
      {eligibility.data?.reason && (
        <p className="mt-1 text-sm text-muted-foreground">{eligibility.data.reason}</p>
      )}
      <CertificationBadges productionReady={data.production_ready} certified={data.certified} />

      <section className="mt-6">
        <h2 className="font-semibold text-foreground">What this Harness does</h2>
        <p className="text-sm">{data.goal}</p>
        <p className="mt-2 text-sm text-muted-foreground">Success condition: {data.success_condition}</p>
        <p className="mt-2 text-sm text-muted-foreground">Atomic boundary: {data.atomic_boundary}</p>
      </section>

      <ContractPanel input={data.input_contract} output={data.output_contract} />
      <GovernancePanel binding={data.category_binding} />
    </div>
  );
}