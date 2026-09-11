import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/http";
import type { ApiError } from "../api/ApiError";
import type { EligibilityResponse } from "../api/types";

export function useHarnessEligibility(
  definitionId: string,
  sourceCategory: string | undefined,
  mode: "generic" | "activative",
) {
  return useQuery<EligibilityResponse, ApiError>({
    queryKey: ["harnesses", definitionId, "eligibility", sourceCategory],
    queryFn: () =>
      apiFetch<EligibilityResponse>(
        `/api/harnesses/${definitionId}/eligibility?source_category=${encodeURIComponent(sourceCategory!)}`,
      ),
    // Never fires for generic-mode Harnesses or with no sourceCategory context — see
    // TS-APP-UI-004 §3, "never fetch what you already know."
    enabled: Boolean(sourceCategory) && mode === "activative",
  });
}
