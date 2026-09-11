import { Link } from "@tanstack/react-router";
import { Card } from "../ui/Card";
import { ModeBadge } from "./ModeBadge";
import { CategoryBadge } from "./CategoryBadge";
import { CertificationBadges } from "./CertificationBadges";
import { EligibilityBadge } from "./EligibilityBadge";
import { computeEligibilityPreview } from "../../lib/harnessEligibility";
import type { HarnessSummary } from "../../api/types";

const CAPABILITY_PREVIEW_COUNT = 3;

export function HarnessCard({
  harness,
  sourceCategory,
}: {
  readonly harness: HarnessSummary;
  readonly sourceCategory: string | undefined;
}) {
  const preview = computeEligibilityPreview(harness, sourceCategory);
  const extraCapabilities = harness.capability_requirements.length - CAPABILITY_PREVIEW_COUNT;

  return (
    <Link
      to="/harnesses/$definitionId"
      params={{ definitionId: harness.definition_id }}
      search={(prev) => prev}
      className="block"
    >
      <Card>
        <div className="flex items-center justify-between gap-2">
          <h3 className="font-semibold text-foreground">{harness.task_id}</h3>
          {preview !== null && <EligibilityBadge status={preview} />}
        </div>
        <p className="text-sm text-muted-foreground">
          {harness.manifest_id} · v{harness.manifest_version}
        </p>
        <div className="mt-2 flex flex-wrap gap-1">
          <ModeBadge mode={harness.mode} />
          <CategoryBadge categoryName={harness.category_name} />
        </div>
        <CertificationBadges
          productionReady={harness.production_ready}
          certified={harness.certified}
        />
        <div className="mt-2 flex flex-wrap gap-1 text-xs text-muted-foreground">
          {harness.capability_requirements.slice(0, CAPABILITY_PREVIEW_COUNT).map((cap) => (
            <span key={cap} className="rounded border border-border px-1.5 py-0.5">
              {cap}
            </span>
          ))}
          {extraCapabilities > 0 && <span>+{extraCapabilities} more</span>}
        </div>
      </Card>
    </Link>
  );
}
