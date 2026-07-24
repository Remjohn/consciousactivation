import { canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import type { ImmutableRef } from "./generated/contracts.js";
import type { CampaignState, ShipDecision, ShipRequest } from "./domain.js";
import { validateActor, validateArtifactRef, validateImmutableRef } from "./validators.js";

export function evaluateShipRequest(request: ShipRequest, campaign: CampaignState): ShipDecision {
  validateImmutableRef(request.campaign_ref, "campaign_ref");
  validateActor(request.operator_actor);
  for (const artifact of request.artifact_refs) validateArtifactRef(artifact);
  for (const evaluation of request.evaluation_refs) validateImmutableRef(evaluation, "evaluation_ref");
  const denialCodes: string[] = [];
  if (campaign.lifecycle_state !== "READY_TO_SHIP") denialCodes.push("CAMPAIGN_NOT_READY_TO_SHIP");
  if (request.autonomy_mode === "SHADOW") denialCodes.push("SHADOW_PUBLICATION_FORBIDDEN");
  if (!request.publication_authority_ref) denialCodes.push("PUBLICATION_AUTHORITY_REQUIRED");
  if (!request.publication_policy_ref) denialCodes.push("PUBLICATION_POLICY_REQUIRED");
  if (!request.artifact_refs.length) denialCodes.push("ARTIFACT_REQUIRED");
  if (!request.evaluation_refs.length) denialCodes.push("EVALUATION_EVIDENCE_REQUIRED");
  if (request.unresolved_exception_ids.length) denialCodes.push("UNRESOLVED_EXCEPTION");
  const body = {
    request_ref: { object_id: request.ship_request_id, version: "1.0.0", sha256: canonicalSha256(request) } as ImmutableRef,
    status: denialCodes.length ? "DENIED" : "AUTHORIZED",
    denial_codes: uniqueSorted(denialCodes),
    authorized_artifact_refs: denialCodes.length ? [] : request.artifact_refs,
    acknowledgement_required: true,
    decision_actor: request.operator_actor,
  } as const;
  const decisionId = deterministicId("ship-decision", body);
  const withoutHash = { decision_id: decisionId, ...body };
  return { ...withoutHash, decision_sha256: canonicalSha256(withoutHash) };
}
