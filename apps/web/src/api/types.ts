// Health / error DTOs mirror TS-APP-API-001 §6 exactly — keep in sync.
export interface ServiceHealthItem {
  readonly service: string;
  readonly product_id: string;
  readonly product_version: string;
  readonly authority_state: string;
  readonly database_path: string;
  readonly integrity: "ok" | "error";
  readonly command_count: number;
  readonly event_count: number;
  readonly receipt_count: number;
  readonly production_authorized: boolean;
  readonly certified: boolean;
  readonly claim_ceiling: string;
}

export interface HealthResponse {
  readonly status: "ok" | "degraded" | "error";
  readonly timestamp: string;
  readonly gateway_version: string;
  readonly ca_data_root: string;
  readonly services: Readonly<Record<string, ServiceHealthItem>>;
}

export interface ErrorResponse {
  readonly error_code: string;
  readonly message: string;
  readonly service?: string | null;
  readonly timestamp: string;
}

// WebSocket message envelope union mirrors TS-APP-API-005 §6 exactly — keep in sync.
interface NodeStatus {
  readonly node_id: string;
  readonly state: string;
  readonly attempt_count: number;
  readonly dispatch_ordinal: number | null;
  readonly output_ref: Record<string, unknown> | null;
  readonly failure: Record<string, unknown> | null;
}

interface RunStatus {
  readonly run_id: string;
  readonly workflow_id: string;
  readonly state: string;
  readonly revision: number;
  readonly cancel_requested: boolean;
  readonly current_checkpoint_id: string | null;
  readonly nodes: ReadonlyArray<NodeStatus>;
}

export type WSMessage =
  | { readonly type: "snapshot"; readonly retrieved_at_utc: string; readonly run: RunStatus }
  | { readonly type: "history"; readonly retrieved_at_utc: string; readonly event_count: number; readonly event_stream_sha256: string; readonly events: ReadonlyArray<unknown> }
  | { readonly type: "node_state_changed"; readonly retrieved_at_utc: string; readonly run_id: string; readonly node: NodeStatus }
  | { readonly type: "run_state_changed"; readonly retrieved_at_utc: string; readonly run_id: string; readonly workflow_id: string; readonly state: string; readonly revision: number; readonly cancel_requested: boolean; readonly current_checkpoint_id: string | null }
  | { readonly type: "run_terminal"; readonly retrieved_at_utc: string; readonly run: RunStatus };

// Harness Library DTOs mirror TS-APP-API-002 §6 / api/routers/harnesses.py exactly
// (field names confirmed directly against the real Pydantic models) — keep in sync.

// From services/builder/src/cmf_builder/domain/category_binding.py — the five
// CanonicalCategory(category_id, canonical_name, governance_owner) tuples, hand-copied
// because the frontend has no Python import path (TS-APP-UI-004 §1).
export type CanonicalCategoryId =
  | "short_form_edited_video"
  | "2d_character_animation"
  | "carousels"
  | "supervisuals"
  | "conversational_activation_expression";

export const CANONICAL_CATEGORIES: ReadonlyArray<{
  readonly id: CanonicalCategoryId;
  readonly label: string;
}> = [
  { id: "short_form_edited_video", label: "Short-Form Edited Video" },
  { id: "2d_character_animation", label: "2D Character Animation" },
  { id: "carousels", label: "Carousels" },
  { id: "supervisuals", label: "Supervisuals" },
  {
    id: "conversational_activation_expression",
    label: "Conversational Activation / Human Expression",
  },
];

export type HarnessMode = "generic" | "activative";

export interface HarnessSummary {
  readonly definition_id: string;
  readonly definition_hash: string;
  readonly manifest_id: string;
  readonly manifest_version: string;
  readonly task_id: string;
  readonly mode: HarnessMode;
  readonly category_id: CanonicalCategoryId | null;
  readonly category_name: string | null;
  readonly classification: ReadonlyArray<string>;
  readonly capability_requirements: ReadonlyArray<string>;
  readonly production_ready: boolean; // always false today — never hidden or restyled
  readonly certified: boolean; // always false today — never hidden or restyled
  readonly package_file: string;
  readonly package_hash: string;
  readonly added_at: string | null; // RFC 3339, non-authoritative (file mtime), display only
}

// Discriminated union derived from CategoryBinding.canonical_dict() vs
// .portable_projection() (services/builder/src/cmf_builder/domain/category_binding.py,
// read directly — TS-APP-UI-004 §1); TS-APP-API-002 §6 types this field as a bare
// `dict`, this models it precisely instead (TS-APP-UI-004 §3).
export type CategoryBindingDetail =
  | {
      readonly applicability: "NOT_APPLICABLE";
      readonly basis: string | null;
      readonly category_id: null;
    }
  | {
      readonly applicability: "REQUIRED";
      readonly harness_id: string;
      readonly harness_version: string;
      readonly category_id: CanonicalCategoryId;
      readonly category_name: string;
      readonly category_registry_version: string;
      readonly category_registry_hash: string;
      readonly constitutional_authority_ref: string;
      readonly runtime_law: string;
      readonly harness_development_law: string;
      readonly semantic_lineage_refs: ReadonlyArray<string>;
      readonly wrong_reading_locks: ReadonlyArray<string>;
      readonly not_applicable_basis: null;
      readonly certification_state: string;
      readonly production_ready: boolean;
      readonly certified: boolean;
      readonly binding_hash: string;
    };

export interface HarnessDetail extends HarnessSummary {
  readonly goal: string;
  readonly success_condition: string;
  readonly atomic_boundary: string;
  readonly input_contract: Record<string, unknown>; // JSON Schema fragment
  readonly output_contract: Record<string, unknown>; // JSON Schema fragment
  readonly minimum_complete_context: ReadonlyArray<string>;
  readonly acceptance_tests: ReadonlyArray<string>;
  readonly authority_chain: ReadonlyArray<string>;
  readonly provenance_refs: ReadonlyArray<string>;
  readonly execution_plan: ReadonlyArray<string>;
  readonly category_binding: CategoryBindingDetail;
  readonly activative_intelligence: Record<string, unknown> | null;
  readonly lineage: ReadonlyArray<string>;
  readonly compiler_id: string;
  readonly compiler_version: string;
  readonly schema_id: string;
  readonly schema_version: string;
}

export type EligibilityStatus = "ELIGIBLE" | "INELIGIBLE" | "NOT_APPLICABLE";

export interface EligibilityResponse {
  readonly definition_id: string;
  readonly harness_category: CanonicalCategoryId | null;
  readonly source_category: string;
  readonly status: EligibilityStatus;
  readonly reason: string | null;
}

// apps/web/src/routes/harnesses/index.tsx's validateSearch shape — declared here so it
// can be imported by both the route file and the co-located validator (TS-APP-UI-004 §7
// Stage 8).
export interface HarnessLibrarySearch {
  readonly category?: CanonicalCategoryId;
  readonly mode?: HarnessMode;
  readonly q?: string;
  readonly sourceCategory?: string;
}

// ---------------------------------------------------------------------------
// Campaign API types — mirrors TS-APP-API-004 §6 field-for-field.
// These are API-specific response/request shapes not present in domain.ts.
// ---------------------------------------------------------------------------

import type {
  CampaignOrder,
  CampaignState,
  CampaignLifecycleState,
  AutonomyMode,
  OutputTarget,
} from "@ca/studio/domain";

export interface CampaignSummary {
  readonly campaign_id: string;
  readonly order_id: string;
  readonly workspace_id: string;
  readonly project_id: string;
  readonly category_id: string;
  readonly lifecycle_state: CampaignLifecycleState;
  readonly autonomy_mode: AutonomyMode;
  readonly output_target_count: number;
  readonly budget_units: number;
  readonly version: number;
}

export interface CampaignDetailResponse {
  readonly order: CampaignOrder;
  readonly state: CampaignState;
  readonly source_derivative_eligible: boolean;
  readonly source_lifecycle_state: string;
  readonly pipeline_ingestion_status: "NOT_YET_TRIGGERED";
  readonly idempotent_replay: boolean;
}

export interface CampaignCreateRequest {
  readonly idempotency_key: string;
  readonly workspace_id: string;
  readonly project_id: string;
  readonly source_package_id: string;
  readonly harness_definition_id: string;
  readonly category_id: string;
  readonly format_profile_id: string;
  readonly objective: string;
  readonly initial_seed: string;
  readonly taste_direction: string[];
  readonly output_targets: OutputTarget[];
  readonly budget_units: number;
  readonly deadline_utc: string | null;
  readonly autonomy_mode: AutonomyMode;
  readonly operator_id: string;
}

// ---------------------------------------------------------------------------
// Interview API types — mirrors TS-APP-API-003 §6 exactly.
// ---------------------------------------------------------------------------

export interface ImportInterviewResponse {
  readonly package_id: string;
  readonly revision: number;
  readonly lifecycle_state: string;
  readonly admission_mode: "IMPORTED" | "BRIEF_LED";
  readonly derivative_eligible: boolean;
  readonly planning_lineage: Record<string, unknown>;
  readonly word_count: number;
  readonly phrase_count: number;
  readonly shot_count: number;
  readonly keyframe_count: number;
  readonly idempotent_replay: boolean;
}

export interface InterviewStatusResponse {
  readonly package_id: string;
  readonly revision: number;
  readonly lifecycle_state: string;
  readonly admission_mode: "IMPORTED" | "BRIEF_LED";
  readonly derivative_eligible: boolean;
  readonly word_count?: number;
  readonly phrase_count?: number;
}

// Re-export of the Studio domain types this scaffold exists to make available.
// No modification. See TS-APP-UI-001 §3 ("consumed by source import").
export type {
  CampaignOrder,
  CampaignState,
  ControlTowerProjection,
  TimelineProjection,
  ChangeRequestProgram,
  ShipDecision,
  ShipRequest,
  HumanResolutionEpisode,
  AuditExportManifest,
  AutonomyMode,
  CampaignLifecycleState,
  OutputTarget,
} from "@ca/studio/domain";
