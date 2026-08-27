import { http, HttpResponse } from "msw";
import type {
  CampaignSummary,
  CampaignDetailResponse,
  InterviewStatusResponse,
  ImportInterviewResponse,
  HarnessSummary,
} from "../api/types";
import type {
  Workspace,
  WorkspaceMembership,
  OperatorGrant,
} from "../api/tenancy";

/**
 * MSW handlers for TS-APP-UI-002 and SPEC-TWC-UI-001 tests.
 * Mirrors the exact JSON bodies TS-APP-API-003/004 §6 and TS-CAE-TEN-001 commit to.
 */

// Tenancy Mock Data
export const mockWorkspaces: Workspace[] = [
  {
    workspace_id: "11111111-1111-1111-1111-111111111111",
    slug: "acme-production",
    display_name: "Acme Production",
    status: "ACTIVE",
    created_at: "2026-08-01T10:00:00Z",
    updated_at: "2026-08-01T10:00:00Z",
    receipt_id: "rcpt-ws-acme-1111",
  },
  {
    workspace_id: "22222222-2222-2222-2222-222222222222",
    slug: "acme-suspended",
    display_name: "Acme Suspended Lab",
    status: "SUSPENDED",
    created_at: "2026-08-02T10:00:00Z",
    updated_at: "2026-08-02T10:00:00Z",
    receipt_id: "rcpt-ws-acme-2222",
  },
];

export const mockMemberships: Record<string, WorkspaceMembership[]> = {
  "11111111-1111-1111-1111-111111111111": [
    {
      membership_id: "mem-1111",
      workspace_id: "11111111-1111-1111-1111-111111111111",
      actor_id: "dev-operator",
      role: "ADMIN",
      status: "ACTIVE",
      created_at: "2026-08-01T10:00:00Z",
      receipt_id: "rcpt-mem-1111",
    },
    {
      membership_id: "mem-1112",
      workspace_id: "11111111-1111-1111-1111-111111111111",
      actor_id: "alice@acme.com",
      role: "MEMBER",
      status: "ACTIVE",
      created_at: "2026-08-03T12:00:00Z",
      receipt_id: "rcpt-mem-1112",
    },
  ],
  "22222222-2222-2222-2222-222222222222": [
    {
      membership_id: "mem-2221",
      workspace_id: "22222222-2222-2222-2222-222222222222",
      actor_id: "dev-operator",
      role: "ADMIN",
      status: "ACTIVE",
      created_at: "2026-08-02T10:00:00Z",
      receipt_id: "rcpt-mem-2221",
    },
  ],
};

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
  // Tenancy: GET /api/v1/workspaces
  http.get("/api/v1/workspaces", () => {
    return HttpResponse.json(mockWorkspaces);
  }),

  // Tenancy: POST /api/v1/workspaces
  http.post("/api/v1/workspaces", async ({ request }) => {
    const body = (await request.json()) as { slug?: string; display_name?: string };
    if (!body.slug || !body.display_name) {
      return HttpResponse.json(
        {
          error_code: "VALIDATION_FAILED",
          message: "slug and display_name are required",
          timestamp: new Date().toISOString(),
        },
        { status: 422 },
      );
    }

    if (body.slug === "duplicate-slug" || body.slug === "conflict-slug") {
      return HttpResponse.json(
        {
          error_code: "WORKSPACE_CONFLICT",
          message: `Workspace slug "${body.slug}" already exists`,
          timestamp: new Date().toISOString(),
        },
        { status: 409 },
      );
    }

    const created: Workspace = {
      workspace_id: `ws-${Date.now()}`,
      slug: body.slug,
      display_name: body.display_name,
      status: "ACTIVE",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      receipt_id: `rcpt-create-${Date.now()}`,
    };
    return HttpResponse.json(created, { status: 201 });
  }),

  // Tenancy: GET /api/v1/workspaces/:workspaceId
  http.get("/api/v1/workspaces/:workspaceId", ({ params }) => {
    const { workspaceId } = params;
    if (workspaceId === "not-found" || workspaceId === "unknown") {
      return HttpResponse.json(
        {
          error_code: "WORKSPACE_NOT_FOUND",
          message: `Workspace "${workspaceId}" not found`,
          timestamp: new Date().toISOString(),
        },
        { status: 404 },
      );
    }

    const found = mockWorkspaces.find((w) => w.workspace_id === workspaceId);
    if (found) {
      return HttpResponse.json(found);
    }

    return HttpResponse.json({
      workspace_id: workspaceId,
      slug: `workspace-${workspaceId}`,
      display_name: `Workspace ${workspaceId}`,
      status: "ACTIVE",
      created_at: "2026-08-01T10:00:00Z",
      updated_at: "2026-08-01T10:00:00Z",
      receipt_id: `rcpt-${workspaceId}`,
    } as Workspace);
  }),

  // Tenancy: PATCH /api/v1/workspaces/:workspaceId
  http.patch("/api/v1/workspaces/:workspaceId", async ({ params, request }) => {
    const { workspaceId } = params;
    const body = (await request.json()) as { display_name?: string; status?: "ACTIVE" | "SUSPENDED" | "ARCHIVED" };
    return HttpResponse.json({
      workspace_id: workspaceId,
      slug: "acme-production",
      display_name: body.display_name || "Updated Workspace",
      status: body.status || "ACTIVE",
      created_at: "2026-08-01T10:00:00Z",
      updated_at: new Date().toISOString(),
      receipt_id: `rcpt-patch-${Date.now()}`,
    } as Workspace);
  }),

  // Tenancy: POST /api/v1/workspaces/:workspaceId/memberships
  http.post("/api/v1/workspaces/:workspaceId/memberships", async ({ params, request }) => {
    const { workspaceId } = params;
    const body = (await request.json()) as { actor_id?: string; role?: string };

    if (workspaceId === "22222222-2222-2222-2222-222222222222" || workspaceId === "suspended-ws") {
      return HttpResponse.json(
        {
          error_code: "WORKSPACE_SUSPENDED",
          message: "Cannot add membership to a SUSPENDED workspace",
          timestamp: new Date().toISOString(),
        },
        { status: 409 },
      );
    }

    if (body.actor_id === "duplicate-member@test.com" || body.actor_id === "dev-operator") {
      return HttpResponse.json(
        {
          error_code: "MEMBERSHIP_DUPLICATE",
          message: `Actor "${body.actor_id}" already holds membership`,
          timestamp: new Date().toISOString(),
        },
        { status: 409 },
      );
    }

    if (!["ADMIN", "MEMBER", "VIEWER"].includes(body.role || "")) {
      return HttpResponse.json(
        {
          error_code: "VALIDATION_FAILED",
          message: `Invalid role enum "${body.role}"`,
          timestamp: new Date().toISOString(),
        },
        { status: 422 },
      );
    }

    const created: WorkspaceMembership = {
      membership_id: `mem-${Date.now()}`,
      workspace_id: String(workspaceId),
      actor_id: body.actor_id || "new-user",
      role: (body.role as "ADMIN" | "MEMBER" | "VIEWER") || "MEMBER",
      status: "ACTIVE",
      created_at: new Date().toISOString(),
      receipt_id: `rcpt-mem-${Date.now()}`,
    };
    return HttpResponse.json(created, { status: 201 });
  }),

  // Tenancy: DELETE /api/v1/workspaces/:workspaceId/memberships/:actorId
  http.delete("/api/v1/workspaces/:workspaceId/memberships/:actorId", ({ params }) => {
    const { workspaceId, actorId } = params;
    if (actorId === "non-existent") {
      return HttpResponse.json(
        {
          error_code: "MEMBERSHIP_NOT_FOUND",
          message: `Membership for actor "${actorId}" not found`,
          timestamp: new Date().toISOString(),
        },
        { status: 404 },
      );
    }

    return HttpResponse.json({
      membership_id: `mem-revoked-${Date.now()}`,
      workspace_id: String(workspaceId),
      actor_id: String(actorId),
      role: "MEMBER",
      status: "REVOKED",
      created_at: "2026-08-01T10:00:00Z",
      updated_at: new Date().toISOString(),
      receipt_id: `rcpt-revoke-${Date.now()}`,
    } as WorkspaceMembership);
  }),

  // Tenancy: POST /api/v1/workspaces/:workspaceId/operator-grants
  http.post("/api/v1/workspaces/:workspaceId/operator-grants", async ({ params, request }) => {
    const { workspaceId } = params;
    const body = (await request.json()) as {
      operator_org_id: string;
      operator_actor_id: string;
      justification: string;
      expires_at: string;
    };

    const grant: OperatorGrant = {
      grant_id: `grant-${Date.now()}`,
      operator_org_id: body.operator_org_id,
      workspace_id: String(workspaceId),
      operator_actor_id: body.operator_actor_id,
      justification: body.justification,
      expires_at: body.expires_at,
      created_at: new Date().toISOString(),
      receipt_id: `rcpt-grant-${Date.now()}`,
    };
    return HttpResponse.json(grant, { status: 201 });
  }),

  // Tenancy: DELETE /api/v1/workspaces/:workspaceId/operator-grants/:grantId
  http.delete("/api/v1/workspaces/:workspaceId/operator-grants/:grantId", ({ params }) => {
    const { workspaceId, grantId } = params;
    return HttpResponse.json({
      grant_id: String(grantId),
      operator_org_id: "00000000-0000-0000-0000-000000000001",
      workspace_id: String(workspaceId),
      operator_actor_id: "op-test",
      justification: "Revoked test grant",
      expires_at: new Date(Date.now() + 3600000).toISOString(),
      revoked_at: new Date().toISOString(),
      created_at: "2026-08-01T10:00:00Z",
      receipt_id: `rcpt-grant-revoked-${Date.now()}`,
    } as OperatorGrant);
  }),

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
    const body = (await request.json()) as any;
    return HttpResponse.json(
      {
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
      } as unknown as CampaignDetailResponse,
      { status: 201 },
    );
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
    return HttpResponse.json(
      {
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
      } as ImportInterviewResponse,
      { status: 201 },
    );
  }),

  // GET /api/harnesses
  http.get("/api/harnesses", () => {
    return HttpResponse.json(mockHarnesses);
  }),
];
