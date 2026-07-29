import { apiFetch } from "./http";
import type {
  CampaignSummary,
  CampaignDetailResponse,
  CampaignCreateRequest,
  CampaignLifecycleState,
} from "./types";

// Control Tower types - imported from Studio domain
// These will be available once the path alias is configured
export interface RefInput { object_id: string; sha256: string; version: string; }
export interface ActorInput {
  actor_id: string; actor_type: "human"; product_id: "conscious-activations-web";
  workflow_role: "operator";
}

export interface NaturalLanguageRevisionInput {
  mode: "natural_language";
  target_refs: RefInput[];
  target_node_ids: string[];
  category_id: string;
  natural_language_request: string;
  current_state_ref: RefInput;
}

export interface ExecuteRevisionResponse { campaign: unknown; rerun: unknown; episode: unknown; }
export interface ResolveExceptionResponse { campaign: unknown; episode: unknown; repair_plan: unknown | null; }

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

// Control Tower API endpoints (TS-APP-API-006)
export async function getControlTower(campaignId: string): Promise<unknown> {
  return apiFetch<unknown>(`/api/campaigns/${campaignId}/tower`);
}

export async function getTimeline(campaignId: string): Promise<unknown> {
  return apiFetch<unknown>(`/api/campaigns/${campaignId}/timeline`);
}

export async function getExceptions(campaignId: string): Promise<unknown[]> {
  return apiFetch<unknown[]>(`/api/campaigns/${campaignId}/exceptions`);
}

export async function compileRevision(
  campaignId: string,
  revision: NaturalLanguageRevisionInput,
  operator_actor: ActorInput
): Promise<unknown> {
  return apiFetch<unknown>(`/api/campaigns/${campaignId}/revisions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ revision, operator_actor }),
  });
}

export async function executeRevision(campaignId: string, programId: string): Promise<ExecuteRevisionResponse> {
  return apiFetch<ExecuteRevisionResponse>(`/api/campaigns/${campaignId}/revisions/${programId}/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
  });
}

export async function resolveException(
  campaignId: string,
  packageId: string,
  decision: "REQUEST_REVISION" | "REJECT",
  operator_actor: ActorInput,
  notes?: string
): Promise<ResolveExceptionResponse> {
  return apiFetch<ResolveExceptionResponse>(`/api/campaigns/${campaignId}/exceptions/${packageId}/resolve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, operator_actor, notes }),
  });
}
