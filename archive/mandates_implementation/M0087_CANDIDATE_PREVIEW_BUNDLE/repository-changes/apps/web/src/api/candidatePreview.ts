import { apiFetch } from "./http";

export interface CandidatePreviewProjection { [key: string]: any; }

export async function createCandidateSession(campaignId: string, input: any): Promise<CandidatePreviewProjection> {
  return apiFetch<CandidatePreviewProjection>(`/api/visual-studio/campaigns/${campaignId}/candidate-sessions`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}
export async function getCandidateSession(sessionId: string): Promise<CandidatePreviewProjection> {
  return apiFetch<CandidatePreviewProjection>(`/api/visual-studio/candidate-sessions/${sessionId}`);
}
export async function navigateCandidateSession(sessionId: string, input: { direction: "NEXT" | "PREVIOUS"; expected_version: number }): Promise<CandidatePreviewProjection> {
  return apiFetch<CandidatePreviewProjection>(`/api/visual-studio/candidate-sessions/${sessionId}/navigate`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}
export async function decideCandidate(sessionId: string, input: { candidate_id: string; decision: "ACCEPT" | "REJECT" | "AUTO_ACCEPT"; expected_version: number; operator_actor?: any; rationale?: string }): Promise<CandidatePreviewProjection> {
  return apiFetch<CandidatePreviewProjection>(`/api/visual-studio/candidate-sessions/${sessionId}/decisions`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}
export async function promoteCandidate(sessionId: string, input: { expected_version: number; operator_actor: any }): Promise<CandidatePreviewProjection> {
  return apiFetch<CandidatePreviewProjection>(`/api/visual-studio/candidate-sessions/${sessionId}/promote`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
  });
}
