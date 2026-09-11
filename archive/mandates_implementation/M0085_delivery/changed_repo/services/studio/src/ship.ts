import { canonicalSha256, deterministicId } from "./canonical";
import { StudioValidationError } from "./errors";
export function evaluateShipRequest(input: any): any {
  const request = input.request ?? input;
  if (request.autonomy_mode === "SHADOW") throw new StudioValidationError("SHADOW_CANNOT_SHIP", "SHADOW campaigns cannot transition to SHIPPED");
  const unresolved = Array.isArray(request.unresolved_exception_ids) ? request.unresolved_exception_ids : [];
  const status = unresolved.length ? "DENIED" : "AUTHORIZED";
  const decision = { decision_id: deterministicId("ship-decision", { request }), request_ref: request.campaign_ref, status, denial_codes: unresolved.length ? ["UNRESOLVED_EXCEPTIONS"] : [], authorized_artifact_refs: status === "AUTHORIZED" ? (request.artifact_refs ?? []) : [], acknowledgement_required: true, decision_actor: request.operator_actor, decision_sha256: canonicalSha256({ request, status }) };
  return decision;
}
