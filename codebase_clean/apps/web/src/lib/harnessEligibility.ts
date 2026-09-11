import type { EligibilityStatus, HarnessMode, CanonicalCategoryId } from "../api/types";

interface EligibilityPreviewInput {
  readonly mode: HarnessMode;
  readonly category_id: CanonicalCategoryId | null;
}

/**
 * Mirrors the server's own branching in TS-APP-API-002 §5 / api/routers/harnesses.py's
 * check_eligibility exactly, using only fields already present on HarnessSummary. Returns
 * null when no sourceCategory context was supplied — the caller renders no badge at all
 * in that case, not a default status.
 */
export function computeEligibilityPreview(
  harness: EligibilityPreviewInput,
  sourceCategory: string | undefined,
): EligibilityStatus | null {
  if (!sourceCategory) return null;
  if (harness.mode === "generic") return "NOT_APPLICABLE";
  return harness.category_id === sourceCategory ? "ELIGIBLE" : "INELIGIBLE";
}
