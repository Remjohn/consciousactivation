import { Badge } from "../ui/Badge";
import type { EligibilityStatus } from "../../api/types";

const TONE: Record<EligibilityStatus, "success" | "danger" | "muted"> = {
  ELIGIBLE: "success",
  INELIGIBLE: "danger",
  NOT_APPLICABLE: "muted",
};

const LABEL: Record<EligibilityStatus, string> = {
  ELIGIBLE: "Eligible",
  INELIGIBLE: "Not eligible",
  NOT_APPLICABLE: "Category-neutral",
};

export function EligibilityBadge({ status }: { readonly status: EligibilityStatus }) {
  return (
    <Badge tone={TONE[status]} data-testid={`eligibility-badge-${status}`}>
      {LABEL[status]}
    </Badge>
  );
}
