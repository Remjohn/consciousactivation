import type { ActorRef, ArtifactRef, AuthorityRef, ImmutableRef } from "./generated/contracts.js";

export type AutonomyMode = "AUTOPILOT" | "REVIEW_BEFORE_SHIP" | "CHECKPOINTED" | "SHADOW";
export type CampaignLifecycleState =
  | "DRAFT"
  | "LAUNCHED"
  | "RUNNING"
  | "AWAITING_REVIEW"
  | "BLOCKED_EXCEPTION"
  | "READY_TO_SHIP"
  | "SHIPPED"
  | "CANCELLED";
export type StudioSurfaceId =
  | "INTERVIEW_EXPRESSION_STUDIO"
  | "STATIC_COMPOSITION_STUDIO"
  | "VIDEO_PRODUCTION_STUDIO"
  | "VISUAL_ASSET_STUDIO"
  | "KNOWLEDGE_MODEL_STUDIO"
  | "FUTURE_CHARACTER_PERFORMANCE_STUDIO";
export type StudioModuleStatus = "ACTIVE_DEVELOPMENT" | "DEFERRED_AWAITING_FORMAT02_HARNESS";
export type ReviewDecision = "APPROVE" | "REJECT" | "REQUEST_REVISION" | "SELECT_CANDIDATE" | "SHIP";
export type ResolutionScope = "run_local" | "harness_profile" | "category" | "workspace" | "avatar_or_identity" | "candidate_doctrine";
export type RevisionCompilationStatus = "COMPILED" | "NEEDS_CLARIFICATION" | "DENIED";
export type ShipDecisionStatus = "AUTHORIZED" | "DENIED";

export interface OutputTarget {
  readonly output_type: "SOURCE_LED_SHORT" | "CAROUSEL" | "SUPERVISUAL" | "ANIMATION_SCENE_PACKAGE" | "ANIMATION_SHORT";
  readonly quantity: number;
  readonly profile_id: string;
}

export interface AutonomyPolicy {
  readonly mode: AutonomyMode;
  readonly checkpoint_ids: ReadonlyArray<string>;
  readonly exception_only: boolean;
  readonly final_review_required: boolean;
  readonly publication_authority_required: boolean;
}

export interface CampaignOrder {
  readonly order_id: string;
  readonly workspace_id: string;
  readonly project_id: string;
  readonly source_kind: "CANONICAL_INTERVIEW_SOURCE_PACKAGE" | "ASSET_PACKAGE_SPEC";
  readonly source_ref: ImmutableRef;
  readonly harness_ref: ImmutableRef;
  readonly category_id: string;
  readonly format_profile_id: string | "NOT_APPLICABLE";
  readonly objective: string;
  readonly initial_seed: string;
  readonly taste_direction: ReadonlyArray<string>;
  readonly output_targets: ReadonlyArray<OutputTarget>;
  readonly budget_units: number;
  readonly deadline_utc: string | null;
  readonly autonomy_policy: AutonomyPolicy;
  readonly operator_actor: ActorRef;
  readonly authority: AuthorityRef;
}

export interface CampaignState {
  readonly campaign_id: string;
  readonly order_ref: ImmutableRef;
  readonly lifecycle_state: CampaignLifecycleState;
  readonly autonomy_mode: AutonomyMode;
  readonly active_checkpoint_id: string | null;
  readonly exception_ids: ReadonlyArray<string>;
  readonly run_refs: ReadonlyArray<ImmutableRef>;
  readonly artifact_refs: ReadonlyArray<ArtifactRef>;
  readonly evaluation_refs: ReadonlyArray<ImmutableRef>;
  readonly version: number;
}

export interface StudioModuleDescriptor {
  readonly surface_id: StudioSurfaceId;
  readonly title: string;
  readonly status: StudioModuleStatus;
  readonly capabilities: ReadonlyArray<string>;
  readonly supported_output_types: ReadonlyArray<string>;
}

export interface StudioSurfaceBinding {
  readonly binding_id: string;
  readonly harness_ref: ImmutableRef;
  readonly category_id: string;
  readonly primary_surface: StudioSurfaceId;
  readonly supporting_surfaces: ReadonlyArray<StudioSurfaceId>;
  readonly operator_entry_policy: "EXCEPTION_ONLY" | "REVIEW_ALLOWED";
  readonly binding_reason: string;
}

export interface RunNodeProjection {
  readonly node_id: string;
  readonly node_type: string;
  readonly title: string;
  readonly status: "PENDING" | "READY" | "RUNNING" | "WAITING_HUMAN" | "SUCCEEDED" | "FAILED" | "CANCELLED" | "INVALIDATED";
  readonly owner_product: string;
  readonly dependency_ids: ReadonlyArray<string>;
  readonly artifact_refs: ReadonlyArray<ArtifactRef>;
  readonly receipt_refs: ReadonlyArray<ImmutableRef>;
  readonly blocker_codes: ReadonlyArray<string>;
}

export interface RuntimeHealthProjection {
  readonly component_id: string;
  readonly component_type: "RUNTIME" | "PROVIDER" | "WORKER" | "STORAGE" | "QUEUE" | "EVALUATOR";
  readonly status: "HEALTHY" | "DEGRADED" | "UNAVAILABLE" | "NOT_CONFIGURED";
  readonly capability_ids: ReadonlyArray<string>;
  readonly budget_units_used: number;
  readonly budget_units_limit: number;
  readonly evidence_refs: ReadonlyArray<ImmutableRef>;
}

export interface KnowledgeProjection {
  readonly skill_refs: ReadonlyArray<ImmutableRef>;
  readonly steering_recipe_refs: ReadonlyArray<ImmutableRef>;
  readonly retrieval_receipt_refs: ReadonlyArray<ImmutableRef>;
  readonly programmed_model_claim_refs: ReadonlyArray<ImmutableRef>;
  readonly exclusion_codes: ReadonlyArray<string>;
}

export interface TimelineItemProjection {
  readonly item_id: string;
  readonly track_id: string;
  readonly kind: string;
  readonly role: string;
  readonly start_frame: number;
  readonly end_frame: number;
  readonly source_start_ms: number | null;
  readonly source_end_ms: number | null;
  readonly source_ref: ImmutableRef | null;
  readonly artifact_ref: ArtifactRef | null;
  readonly editable_operations: ReadonlyArray<string>;
}

export interface TimelineTrackProjection {
  readonly track_id: string;
  readonly track_type: string;
  readonly role: string;
  readonly z_index: number;
  readonly item_ids: ReadonlyArray<string>;
}

export interface TimelineProjection {
  readonly projection_id: string;
  readonly video_edit_program_ref: ImmutableRef;
  readonly state: "READ_ONLY_CANONICAL_PROGRAM_PROJECTION";
  readonly width: number;
  readonly height: number;
  readonly fps_numerator: number;
  readonly fps_denominator: number;
  readonly duration_frames: number;
  readonly tracks: ReadonlyArray<TimelineTrackProjection>;
  readonly items: ReadonlyArray<TimelineItemProjection>;
}

export interface ExceptionReviewPackage {
  readonly package_id: string;
  readonly campaign_ref: ImmutableRef;
  readonly exception_code: string;
  readonly responsible_product: string;
  readonly summary: string;
  readonly evidence_refs: ReadonlyArray<ImmutableRef>;
  readonly candidate_refs: ReadonlyArray<ImmutableRef>;
  readonly allowed_decisions: ReadonlyArray<ReviewDecision>;
  readonly recommended_next_actions: ReadonlyArray<string>;
}

export interface ControlTowerProjection {
  readonly projection_id: string;
  readonly campaign: CampaignState;
  readonly order: CampaignOrder;
  readonly studio_binding: StudioSurfaceBinding;
  readonly source_package_ref: ImmutableRef;
  readonly observed_activative_pack_ref: ImmutableRef | null;
  readonly semantic_production_package_ref: ImmutableRef | null;
  readonly final_script_ref: ImmutableRef | null;
  readonly activation_transfer_contract_ref: ImmutableRef | null;
  readonly run_nodes: ReadonlyArray<RunNodeProjection>;
  readonly artifacts: ReadonlyArray<ArtifactRef>;
  readonly evaluations: ReadonlyArray<ImmutableRef>;
  readonly knowledge: KnowledgeProjection;
  readonly runtime_health: ReadonlyArray<RuntimeHealthProjection>;
  readonly timeline: TimelineProjection | null;
  readonly exception_packages: ReadonlyArray<ExceptionReviewPackage>;
  readonly available_actions: ReadonlyArray<string>;
  readonly projection_sha256: string;
}

export interface ToolDescriptor {
  readonly tool_id: string;
  readonly tool_version: string;
  readonly owner_product: string;
  readonly allowed_target_layers: ReadonlyArray<string>;
  readonly argument_keys: ReadonlyArray<string>;
  readonly reversible: boolean;
}

export interface SteeringRecipeBinding {
  readonly recipe_ref: ImmutableRef;
  readonly trigger_phrases: ReadonlyArray<string>;
  readonly target_layer: string;
  readonly operations: ReadonlyArray<ChangeOperationTemplate>;
  readonly preserved_properties: ReadonlyArray<string>;
}

export interface ChangeOperationTemplate {
  readonly tool_id: string;
  readonly tool_version: string;
  readonly arguments: Readonly<Record<string, string | number | boolean>>;
  readonly preconditions: ReadonlyArray<string>;
  readonly expected_effect: string;
}

export interface OperatorRevisionRequest {
  readonly request_id: string;
  readonly run_ref: ImmutableRef;
  readonly target_refs: ReadonlyArray<ImmutableRef>;
  readonly target_node_ids: ReadonlyArray<string>;
  readonly category_id: string;
  readonly natural_language_request: string;
  readonly current_state_ref: ImmutableRef;
  readonly evaluation_ref: ImmutableRef | null;
  readonly jit_capsule_ref: ImmutableRef;
  readonly permitted_tool_registry_ref: ImmutableRef;
  readonly operator_actor: ActorRef;
  readonly expected_state_version: number;
}

export interface DirectManipulationDelta {
  readonly delta_id: string;
  readonly run_ref: ImmutableRef;
  readonly target_ref: ImmutableRef;
  readonly target_node_id: string;
  readonly manipulation_type: "MOVE_BBOX" | "RESIZE_BBOX" | "TRIM_SEGMENT" | "REORDER_ITEM" | "EDIT_TEXT" | "SET_PARAMETER" | "SELECT_CANDIDATE";
  readonly arguments: Readonly<Record<string, string | number | boolean>>;
  readonly current_state_ref: ImmutableRef;
  readonly operator_actor: ActorRef;
  readonly expected_state_version: number;
}

export interface ChangeOperation {
  readonly operation_id: string;
  readonly target_ref: ImmutableRef;
  readonly target_node_id: string;
  readonly target_layer: string;
  readonly tool_id: string;
  readonly tool_version: string;
  readonly arguments: Readonly<Record<string, string | number | boolean>>;
  readonly preconditions: ReadonlyArray<string>;
  readonly expected_effect: string;
}

export interface ChangeRequestProgram {
  readonly program_id: string;
  readonly compilation_status: RevisionCompilationStatus;
  readonly request_ref: ImmutableRef;
  readonly interpretation: string;
  readonly target_layer_or_nodes: ReadonlyArray<string>;
  readonly exact_operations: ReadonlyArray<ChangeOperation>;
  readonly declared_invariants: ReadonlyArray<string>;
  readonly required_transformations: ReadonlyArray<string>;
  readonly creative_degrees_of_freedom: ReadonlyArray<string>;
  readonly invalidated_downstream_nodes: ReadonlyArray<string>;
  readonly validation_plan: ReadonlyArray<string>;
  readonly preview_required: boolean;
  readonly confidence_micros: number;
  readonly escalation: string | null;
  readonly source_kind: "NATURAL_LANGUAGE" | "DIRECT_MANIPULATION";
  readonly expected_state_version: number;
  readonly program_sha256: string;
}

export interface DependencyGraphNode {
  readonly node_id: string;
  readonly dependency_ids: ReadonlyArray<string>;
  readonly lifecycle_state: string;
}

export interface SelectiveRerunRequest {
  readonly rerun_request_id: string;
  readonly run_ref: ImmutableRef;
  readonly change_request_program_ref: ImmutableRef;
  readonly changed_node_ids: ReadonlyArray<string>;
  readonly invalidated_node_ids: ReadonlyArray<string>;
  readonly rerun_node_ids: ReadonlyArray<string>;
  readonly preserved_node_ids: ReadonlyArray<string>;
  readonly validation_node_ids: ReadonlyArray<string>;
  readonly reason: string;
}

export interface ExactChange {
  readonly target_object: string;
  readonly operation: string;
  readonly before: string;
  readonly after: string;
}

export interface ProgrammingMaterialDispositions {
  readonly retrieval_memory: "AUTOMATIC";
  readonly hard_negative: "CANDIDATE" | "NOT_APPLICABLE";
  readonly supervised_example: "CANDIDATE";
  readonly preference_pair: "CANDIDATE" | "NOT_APPLICABLE";
  readonly repair_trajectory: "CANDIDATE" | "NOT_APPLICABLE";
  readonly programmed_model_training: "CANDIDATE";
  readonly steering_recipe_evidence: "CANDIDATE";
}

export interface HumanResolutionEpisode {
  readonly episode_id: string;
  readonly workspace_id: string;
  readonly project_id: string;
  readonly campaign_id: string;
  readonly run_ref: ImmutableRef;
  readonly harness_ref: ImmutableRef;
  readonly category_id: string;
  readonly format_profile_id: string | "NOT_APPLICABLE";
  readonly resolution_kind: "initial_seed" | "taste_direction" | "approval" | "rejection" | "candidate_selection" | "revision_request" | "manual_parameter_change" | "manual_timeline_change" | "tool_override" | "escalation_resolution" | "publication_decision";
  readonly state_before_ref: ImmutableRef;
  readonly state_after_ref: ImmutableRef;
  readonly artifact_before_refs: ReadonlyArray<ArtifactRef>;
  readonly request_text: string | null;
  readonly request_structured_ref: ImmutableRef | null;
  readonly selected_or_rejected_candidate_refs: ReadonlyArray<ImmutableRef>;
  readonly exact_changes: ReadonlyArray<ExactChange>;
  readonly tool_program_ref: ImmutableRef | null;
  readonly exact_tool_calls: ReadonlyArray<ChangeOperation>;
  readonly runtime_and_model_refs: ReadonlyArray<ImmutableRef>;
  readonly retrieved_context_ref: ImmutableRef | null;
  readonly declared_invariants: ReadonlyArray<string>;
  readonly required_transformations: ReadonlyArray<string>;
  readonly creative_degrees_of_freedom: ReadonlyArray<string>;
  readonly wrong_reading_locks: ReadonlyArray<string>;
  readonly result_refs: ReadonlyArray<ImmutableRef>;
  readonly evaluation_refs: ReadonlyArray<ImmutableRef>;
  readonly accepted: boolean;
  readonly human_authority_actor: ActorRef;
  readonly scope: ResolutionScope;
  readonly programming_material_dispositions: ProgrammingMaterialDispositions;
  readonly recorded_at_utc: string;
  readonly episode_sha256: string;
}

export interface ProgrammingMaterialRecord {
  readonly record_id: string;
  readonly episode_ref: ImmutableRef;
  readonly retrieval_tokens: ReadonlyArray<string>;
  readonly category_id: string;
  readonly harness_ref: ImmutableRef;
  readonly scope: ResolutionScope;
  readonly accepted: boolean;
  readonly dispositions: ProgrammingMaterialDispositions;
}

export interface ShipRequest {
  readonly ship_request_id: string;
  readonly campaign_ref: ImmutableRef;
  readonly autonomy_mode: AutonomyMode;
  readonly target_channel: string;
  readonly artifact_refs: ReadonlyArray<ArtifactRef>;
  readonly evaluation_refs: ReadonlyArray<ImmutableRef>;
  readonly unresolved_exception_ids: ReadonlyArray<string>;
  readonly operator_actor: ActorRef;
  readonly publication_authority_ref: ImmutableRef | null;
  readonly publication_policy_ref: ImmutableRef | null;
}

export interface ShipDecision {
  readonly decision_id: string;
  readonly request_ref: ImmutableRef;
  readonly status: ShipDecisionStatus;
  readonly denial_codes: ReadonlyArray<string>;
  readonly authorized_artifact_refs: ReadonlyArray<ArtifactRef>;
  readonly acknowledgement_required: boolean;
  readonly decision_actor: ActorRef;
  readonly decision_sha256: string;
}

export interface AuditExportManifest {
  readonly export_id: string;
  readonly campaign_ref: ImmutableRef;
  readonly source_refs: ReadonlyArray<ImmutableRef>;
  readonly semantic_refs: ReadonlyArray<ImmutableRef>;
  readonly run_refs: ReadonlyArray<ImmutableRef>;
  readonly artifact_refs: ReadonlyArray<ArtifactRef>;
  readonly evaluation_refs: ReadonlyArray<ImmutableRef>;
  readonly command_refs: ReadonlyArray<ImmutableRef>;
  readonly receipt_refs: ReadonlyArray<ImmutableRef>;
  readonly human_resolution_refs: ReadonlyArray<ImmutableRef>;
  readonly ship_decision_ref: ImmutableRef | null;
  readonly replay_instructions: ReadonlyArray<string>;
  readonly export_sha256: string;
}
