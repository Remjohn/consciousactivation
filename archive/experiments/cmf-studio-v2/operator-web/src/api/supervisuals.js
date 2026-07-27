const API_BASE = import.meta.env.VITE_CMF_API_BASE_URL || "";

export const operatorId = "11111111-1111-4111-8111-111111111111";

export async function createSupervisualProject(payload) {
  return requestJson("/api/v1/supervisual/projects", {
    method: "POST",
    body: payload,
  });
}

export async function getSupervisualProject(projectId) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}`);
}

export async function buildSupervisualProject(projectId, payload = {}) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}/build`, {
    method: "POST",
    body: payload,
  });
}

export async function reviseSupervisualProject(projectId, payload) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}/revise`, {
    method: "POST",
    body: payload,
  });
}

export async function approveSupervisualProject(projectId, payload = {}) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}/approve`, {
    method: "POST",
    body: {
      operator_id: operatorId,
      ...payload,
    },
  });
}

export async function rejectSupervisualProject(projectId, payload = {}) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}/reject`, {
    method: "POST",
    body: {
      operator_id: operatorId,
      reason: "Operator requested revision before approval.",
      ...payload,
    },
  });
}

export async function exportSupervisualProject(projectId, payload = {}) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}/export`, {
    method: "POST",
    body: payload,
  });
}

export async function fetchSupervisualTimeline(projectId) {
  return requestJson(`/api/v1/supervisual/projects/${projectId}/timeline`);
}

async function requestJson(path, { method = "GET", body } = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const detail = data?.detail;
    const message = typeof detail === "object" ? `${detail.code}: ${detail.message}` : detail || `HTTP ${response.status}`;
    throw new Error(message);
  }
  return data;
}

export function createProjectPayload({ activeGuest, draft }) {
  return {
    project_name: draft.projectName,
    workspace_id: draft.workspaceId,
    brand_id: draft.brandId,
    brand_context_version_ref: draft.brandContextVersionRef,
    source_evidence_refs: splitLines(draft.sourceEvidenceRefs),
    context_type: draft.contextType,
    interview_brief_ref: draft.interviewBriefRef || null,
    transcript_ref: draft.transcriptRef || null,
    frame_profile_code: draft.frameProfileCode,
    style_route_code: draft.styleRouteCode,
    context_payload: {
      guest_code: activeGuest.code,
      guest_workspace: activeGuest.workspace,
      voice_dna: activeGuest.voiceDna,
      emotional_dna: activeGuest.emotionalDna,
      primary_claim: draft.primaryClaim,
      proof_detail: draft.proofDetail,
      audience_context_premise: draft.audiencePremise,
    },
  };
}

export function splitLines(value) {
  return String(value || "")
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}
