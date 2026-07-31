import { apiFetch } from "./http";
import { apiFetchMultipart } from "./http";
import type {
  GuestResearchPackageResponse,
  ActivativeInterviewBriefResponse,
  ComposerSessionResponse,
  ComposeBriefInput,
  ComposeSessionInput,
  PlannedQuestionInput,
} from "./types";

// Re-export types for convenience
export type { ComposeBriefInput, ComposeSessionInput, PlannedQuestionInput };

export interface CreateResearchPackageInput {
  guestName: string;
  sourceUrls: string[];
  documents: File[];
  workspaceId: string;
  projectId: string;
  operatorId: string;
  authorityScope: string;
  assertionId: string;
}

export async function createResearchPackage(input: CreateResearchPackageInput): Promise<GuestResearchPackageResponse> {
  const form = new FormData();
  form.set("guest_name", input.guestName);
  form.set("source_urls_json", JSON.stringify(input.sourceUrls));
  form.set("workspace_id", input.workspaceId);
  form.set("project_id", input.projectId);
  form.set("operator_id", input.operatorId);
  form.set("authority_scope", input.authorityScope);
  form.set("assertion_id", input.assertionId);
  for (const doc of input.documents) form.append("documents", doc);
  return apiFetchMultipart<GuestResearchPackageResponse>("/api/interviews/compose/research", form);
}

export async function getResearchPackage(researchPackageId: string): Promise<GuestResearchPackageResponse> {
  return apiFetch<GuestResearchPackageResponse>(`/api/interviews/compose/research/${encodeURIComponent(researchPackageId)}`);
}

export async function composeBrief(input: ComposeBriefInput): Promise<ActivativeInterviewBriefResponse> {
  return apiFetch<ActivativeInterviewBriefResponse>("/api/interviews/compose/brief", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getBrief(briefId: string): Promise<ActivativeInterviewBriefResponse> {
  return apiFetch<ActivativeInterviewBriefResponse>(`/api/interviews/compose/briefs/${encodeURIComponent(briefId)}`);
}

export async function createComposerSession(input: ComposeSessionInput): Promise<ComposerSessionResponse> {
  return apiFetch<ComposerSessionResponse>("/api/interviews/compose/sessions", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getComposerSession(sessionId: string): Promise<ComposerSessionResponse> {
  return apiFetch<ComposerSessionResponse>(`/api/interviews/compose/sessions/${encodeURIComponent(sessionId)}`);
}
