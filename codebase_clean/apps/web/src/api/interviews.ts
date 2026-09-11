import { apiFetch } from "./http";
import type { InterviewStatusResponse, ImportInterviewResponse } from "./types";

export async function getInterviewStatus(packageId: string): Promise<InterviewStatusResponse> {
  return apiFetch<InterviewStatusResponse>(`/api/interviews/${encodeURIComponent(packageId)}/status`);
}

export interface ImportInterviewInput {
  video: File;
  transcript: File;
  workspace_id: string;
  project_id: string;
  operator_id: string;
  authority_scope: string;
  assertion_id: string;
  transcript_format: "PRE_ALIGNED_JSON" | "SRT";
  speaker_id?: string;
  visual_profile_id?: string;
}

export async function importInterview(input: ImportInterviewInput): Promise<ImportInterviewResponse> {
  const form = new FormData();
  form.set("video", input.video);
  form.set("transcript", input.transcript);
  for (const [key, value] of Object.entries(input)) {
    if (key === "video" || key === "transcript" || value === undefined) continue;
    form.set(key, String(value));
  }
  return apiFetch<ImportInterviewResponse>("/api/interviews/import", {
    method: "POST",
    body: form,
  });
}
