import { apiFetch } from "./http";

export type VisualFeedbackDecision = "GOOD" | "NEEDS_EDIT" | "REJECT";
export type VisualFeedbackReason = "SOURCE_MISMATCH" | "WRONG_READING" | "COMPOSITION" | "TRANSFORMATION" | "SOURCE_QUALITY" | "OTHER";
export interface VisualStudioProjection { [key: string]: any; }
export interface VisualStudioFeedbackInput { revision_ref: { object_id: string; version: string; sha256: string }; target_ref?: { object_id: string; version: string; sha256: string } | null; decision: VisualFeedbackDecision; reason?: VisualFeedbackReason | null; note?: string; operator_actor: { actor_id: string; actor_type: "human"; product_id: string; workflow_role: "operator" }; expected_state_version: number; }

export async function getVisualStudio(campaignId: string): Promise<VisualStudioProjection> {
  return apiFetch<VisualStudioProjection>(`/api/visual-studio/campaigns/${campaignId}`);
}

export async function recordVisualFeedback(campaignId: string, input: VisualStudioFeedbackInput): Promise<any> {
  return apiFetch<any>(`/api/visual-studio/campaigns/${campaignId}/feedback`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}

export async function compileVisualProposal(campaignId: string, input: { target_ref: { object_id: string; version: string; sha256: string }; target_node_id: string; natural_language_request: string; operator_actor: VisualStudioFeedbackInput["operator_actor"]; expected_state_version: number }): Promise<any> {
  return apiFetch<any>(`/api/visual-studio/campaigns/${campaignId}/proposals`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}

export type VisualTransformType = "MOVE_BBOX" | "RESIZE_BBOX" | "TRIM_SEGMENT";
export async function compileVisualTransformProposal(campaignId: string, input: { target_ref: { object_id: string; version: string; sha256: string }; target_node_id: string; manipulation_type: VisualTransformType; arguments: Record<string, string | number | boolean>; operator_actor: VisualStudioFeedbackInput["operator_actor"]; expected_state_version: number }): Promise<any> {
  return apiFetch<any>(`/api/visual-studio/campaigns/${campaignId}/transform-proposals`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}
