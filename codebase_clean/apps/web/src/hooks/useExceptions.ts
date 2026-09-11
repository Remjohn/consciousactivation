// TS-APP-UI-003 - Exception hooks
// Handles exception resolution mutations

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { resolveException } from "../api/campaigns";
import type { ActorInput } from "../api/campaigns";

// Mock operator actor - in production this would come from auth context
const currentOperatorActor: ActorInput = {
  actor_id: "operator-web-001",
  actor_type: "human",
  product_id: "conscious-activations-web",
  workflow_role: "operator",
};

export interface ResolveExceptionInput {
  packageId: string;
  decision: "REQUEST_REVISION" | "REJECT";
  notes?: string;
}

export function useExceptionResolve(campaignId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: ResolveExceptionInput) =>
      resolveException(campaignId, input.packageId, input.decision, currentOperatorActor, input.notes),
    onSuccess: () => {
      // Invalidate all campaign data to refresh tower, timeline, exceptions
      queryClient.invalidateQueries({ queryKey: ["campaign", campaignId] });
    },
    onError: (error: Error) => {
      console.error("[useExceptionResolve] Failed to resolve exception:", error);
    },
  });
}
