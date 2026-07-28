import { http, HttpResponse } from "msw";
import type { CampaignSummary, CampaignDetailResponse, InterviewStatusResponse, ImportInterviewResponse, HarnessSummary } from "../api/types";

/**
 * MSW handlers for TS-APP-UI-002 tests.
 * Mirrors the exact JSON bodies TS-APP-API-003/004 §6 already committed to.
 */

// Harnesses
export const mockHarnesses: HarnessSummary[] = [
  {
    definition_id: "harness:short_form_001",
    definition_hash: "sha256:abc123",
    manifest_id: "manifest:short_form_001",
    manifest_version: "1.0.0",
    task_id: "task:short_form",
    mode: "activative",
    category_id: "short_form_edited_video",
    category_name: "Short-Form Edited Video",
    classification: ["video"],
    capability_requirements: ["editing"],
    production_ready: false,
    certified: false,
    package_file: "harness:short_form_001.zip",
    package_hash: "sha256:def456",
    added_at: "2026-07-20T10:00:00Z",
  },
  {
    definition_id: "harness:2d_anim_001",
    definition_hash: "sha256:ghi789",
    manifest_id: "manifest:2d_anim_001",
    manifest_version: "1.0.0",
    task_id: "task:2d_anim",
    mode: "activative",
    category_id: "2d_character_animation",
    category_name: "2D Character Animation",
    classification: ["animation"],
    capability_requirements: ["animation"],
    production_ready: false,
    certified: false,
    package_file: "harness:2d_anim_001.zip",
    package_hash: "sha256:jkl012",
    added_at: "2026-07-21T10:00:00Z",
  },
  {
    definition_id: "harness:generic_001",
    definition_hash: "sha256:mno345",
    manifest_id: "manifest:generic_001",
    manifest_version: "1.0.0",
    task_id: "task:generic",
    mode: "generic",
    category_id: null,
    category_name: null,
    classification: [],
    capability_requirements: [],
    production_ready: false,
    certified: false,
    package_file: "harness:generic_001.zip",
    package_hash: "sha256:pqr678",
    added_at: "2026-07-22T10:00:00Z",
  },
];

// Campaigns
export const mockCampaigns: CampaignSummary[] = [
  {
    campaign_id: "campaign:1a2b3c4d5e6f70819293",
    order_id: "order:1a2b3c4d5e6f70819293",
    workspace_id: "workspace:acme",
    project_id: "project:q3-launch",
    category_id: "short_form_edited_video",
    lifecycle_state: "RUNNING",
    autonomy_mode: "REVIEW_BEFORE_SHIP",
    output_target_count: 2,
    budget_units: 100,
    version: 1,
  },
  {
    campaign_id: "campaign:2b3c4d5e6f708192930",
    order_id: "order:2b3c4d5e6f708192930",
    workspace_id: "workspace:acme",
    project_id: "project:q3-launch",
    category_id: "carousels",
    lifecycle_state: "BLOCKED_EXCEPTION",
    autonomy_mode: "AUTOPILOT",
    output_target_count: 1,
    budget_units: 50,
    version: 1,
  },
  {
    campaign_id: "campaign:3c4d5e6f708192930ab",
    order_id: "order:3c4d5e6f708192930ab",
    workspace_id: "workspace:acme",
    project_id: "project:q3-launch",
    category_id: "short_form_edited_video",
    lifecycle_state: "SHIPPED",
    autonomy_mode: "CHECKPOINTED",
    output_target_count: 3,
    budget_units: 200,
    version: 1,
  },
];

export const handlers = [
  // GET /api/campaigns
  http.get("/api/campaigns", ({ request }) => {
    const url = new URL(request.url);
    const lifecycleState = url.searchParams.get("lifecycle_state");
    const filtered = lifecycleState
      ? mockCampaigns.filter((c) => c.lifecycle_state === lifecycleState)
      : mockCampaigns;
    return HttpResponse.json(filtered);
  }),

  // POST /api/campaigns
  http.post("/api/campaigns", async ({ request }) => {
    const body = await request.json() as any;
    return HttpResponse.json({
      order: {
        idempotency_key: body.idempotency_key,
        workspace_id: body.workspace_id,
        project_id: body.project_id,
        source_package_id: body.source_package_id,
        harness_definition_id: body.harness_definition_id,
        category_id: body.category_id,
        format_profile_id: body.format_profile_id,
        objective: body.objective,
        initial_seed: body.initial_seed,
        taste_direction: body.taste_direction,
        output_targets: body.output_targets,
        budget_units: body.budget_units,
        deadline_utc: body.deadline_utc,
        autonomy_mode: body.autonomy_mode,
        operator_id: body.operator_id,
      },
      state: {
        campaign_id: `campaign:${Date.now()}`,
        lifecycle_state: "LAUNCHED",
        version: 1,
      },
      source_derivative_eligible: false,
      source_lifecycle_state: "COMPONENTS_IN_PROGRESS",
      pipeline_ingestion_status: "NOT_YET_TRIGGERED",
      idempotent_replay: false,
    } as CampaignDetailResponse, { status: 201 });
  }),

  // GET /api/interviews/:id/status
  http.get("/api/interviews/:id/status", ({ params }) => {
    if (params.id === "unknown") {
      return HttpResponse.json(
        { error_code: "NOT_FOUND", message: "object not found", service: null, timestamp: new Date().toISOString() },
        { status: 404 },
      );
    }
    return HttpResponse.json({
      package_id: params.id,
      lifecycle_state: "COMPONENTS_IN_PROGRESS",
      admission_mode: "IMPORTED",
      derivative_eligible: false,
      revision: 1,
      word_count: 5000,
      phrase_count: 120,
    } as InterviewStatusResponse);
  }),

  // POST /api/interviews/import
  http.post("/api/interviews/import", () => {
    return HttpResponse.json({
      package_id: `pkg:${Date.now()}`,
      revision: 1,
      lifecycle_state: "ADMITTED",
      admission_mode: "IMPORTED",
      derivative_eligible: false,
      planning_lineage: {},
      word_count: 5000,
      phrase_count: 120,
      shot_count: 50,
      keyframe_count: 10,
      idempotent_replay: false,
    } as ImportInterviewResponse, { status: 201 });
  }),

  // GET /api/harnesses
  http.get("/api/harnesses", () => {
    return HttpResponse.json(mockHarnesses);
  }),
];
