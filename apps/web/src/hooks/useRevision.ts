// TS-APP-UI-003 - Revision hooks
// Handles revision compile and execute mutations

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { compileRevision, executeRevision } from "../api/campaigns";
import type { NaturalLanguageRevisionInput, ActorInput } from "../api/campaigns";

// Mock operator actor - in production this would come from auth context
const currentOperatorActor: ActorInput = {
  actor_id: "operator-web-001",
  actor_type: "human",
  product_id: "conscious-activations-web",
  workflow_role: "operator",
};

export function useRevisionCompose(campaignId: string) {
  return useMutation({
    mutationFn: (input: NaturalLanguageRevisionInput) =>
      compileRevision(campaignId, input, currentOperatorActor),
    onError: (error: Error) => {
      console.error("[useRevisionCompose] Failed to compile revision:", error);
    },
  });
}

export function useRevisionExecute(campaignId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (programId: string) => executeRevision(campaignId, programId),
    onSuccess: () => {
      // Invalidate all campaign data to refresh tower, timeline, exceptions
      queryClient.invalidateQueries({ queryKey: ["campaign", campaignId] });
    },
    onError: (error: Error) => {
      console.error("[useRevisionExecute] Failed to execute revision:", error);
    },
  });
}
