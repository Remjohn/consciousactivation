import { apiFetch } from "./http";
import type {
  CampaignSummary,
  CampaignDetailResponse,
  CampaignCreateRequest,
  CampaignLifecycleState,
} from "./types";

export interface CampaignListFilters {
  workspace_id?: string;
  project_id?: string;
  lifecycle_state?: CampaignLifecycleState;
}

export async function listCampaigns(filters: CampaignListFilters): Promise<CampaignSummary[]> {
  const params = new URLSearchParams(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== "") as [string, string][],
  );
  const queryString = params.toString();
  return apiFetch<CampaignSummary[]>(`/api/campaigns${queryString ? `?${queryString}` : ""}`);
}

export async function createCampaign(payload: CampaignCreateRequest): Promise<CampaignDetailResponse> {
  return apiFetch<CampaignDetailResponse>("/api/campaigns", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
