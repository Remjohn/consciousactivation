from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from api.schemas.campaigns import (
    ActorRefModel,
    ArtifactRefModel,
    AuthorityRefModel,
    CampaignOrderModel,
    CampaignStateModel,
    RefModel,
)


class ControlTowerProjectionModel(BaseModel):
    projection_id: str
    campaign: "CampaignStateModel"
    order: "CampaignOrderModel"
    studio_binding: "StudioSurfaceBindingModel"
    source_package_ref: RefModel
    observed_activative_pack_ref: RefModel | None
    semantic_production_package_ref: RefModel | None
    final_script_ref: RefModel | None
    activation_transfer_contract_ref: RefModel | None
    run_nodes: list["RunNodeProjectionModel"]
    artifacts: list[ArtifactRefModel]
    evaluations: list[RefModel]
    knowledge: "KnowledgeProjectionModel"
    runtime_health: list["RuntimeHealthProjectionModel"]
    timeline: "TimelineProjectionModel | None"
    exception_packages: list["ExceptionReviewPackageModel"]
    available_actions: list[str]
    projection_sha256: str


class RunNodeProjectionModel(BaseModel):
    node_id: str
    node_type: str
    title: str
    status: Literal[
        "PENDING", "READY", "RUNNING", "WAITING_HUMAN",
        "SUCCEEDED", "FAILED", "CANCELLED", "INVALIDATED",
    ]
    owner_product: str
    dependency_ids: list[str]
    artifact_refs: list[ArtifactRefModel]
    receipt_refs: list[RefModel]
    blocker_codes: list[str]


class ExceptionReviewPackageModel(BaseModel):
    package_id: str
    campaign_ref: RefModel
    exception_code: str
    responsible_product: str
    summary: str
    evidence_refs: list[RefModel]
    candidate_refs: list[RefModel]
    allowed_decisions: list[
        Literal["APPROVE", "REJECT", "REQUEST_REVISION", "SELECT_CANDIDATE", "SHIP"]
    ]
    recommended_next_actions: list[str]


class TimelineProjectionModel(BaseModel):
    projection_id: str
    video_edit_program_ref: RefModel
    state: Literal["READ_ONLY_CANONICAL_PROGRAM_PROJECTION"]
    width: int
    height: int
    fps_numerator: int
    fps_denominator: int
    duration_frames: int
    tracks: list["TimelineTrackProjectionModel"]
    items: list["TimelineItemProjectionModel"]


class TimelineTrackProjectionModel(BaseModel):
    track_id: str
    track_type: str
    role: str
    z_index: int
    item_ids: list[str]


class TimelineItemProjectionModel(BaseModel):
    item_id: str
    track_id: str
    kind: str
    role: str
    start_frame: int
    end_frame: int
    source_start_ms: int | None
    source_end_ms: int | None
    source_ref: RefModel | None
    artifact_ref: ArtifactRefModel | None
    editable_operations: list[str]


class KnowledgeProjectionModel(BaseModel):
    skill_refs: list[RefModel]
    steering_recipe_refs: list[RefModel]
    retrieval_receipt_refs: list[RefModel]
    programmed_model_claim_refs: list[RefModel]
    exclusion_codes: list[str]


class RuntimeHealthProjectionModel(BaseModel):
    component_id: str
    component_type: Literal["RUNTIME", "PROVIDER", "WORKER", "STORAGE", "QUEUE", "EVALUATOR"]
    status: Literal["HEALTHY", "DEGRADED", "UNAVAILABLE", "NOT_CONFIGURED"]
    capability_ids: list[str]
    budget_units_used: int
    budget_units_limit: int
    evidence_refs: list[RefModel]


class StudioSurfaceBindingModel(BaseModel):
    binding_id: str
    harness_ref: RefModel
    category_id: str
    primary_surface: str
    supporting_surfaces: list[str]
    operator_entry_policy: Literal["EXCEPTION_ONLY", "REVIEW_ALLOWED"]
    binding_reason: str


class NaturalLanguageRevisionInput(BaseModel):
    request_id: str
    run_ref: RefModel
    target_refs: list[RefModel]
    target_node_ids: list[str]
    category_id: str
    natural_language_request: str
    current_state_ref: RefModel
    evaluation_ref: RefModel | None
    jit_capsule_ref: RefModel
    permitted_tool_registry_ref: RefModel
    operator_actor: ActorRefModel
    expected_state_version: int = Field(ge=1)


class DirectManipulationInput(BaseModel):
    delta_id: str
    run_ref: RefModel
    target_ref: RefModel
    target_node_id: str
    manipulation_type: Literal[
        "MOVE_BBOX", "RESIZE_BBOX", "TRIM_SEGMENT", "REORDER_ITEM",
        "EDIT_TEXT", "SET_PARAMETER", "SELECT_CANDIDATE",
    ]
    arguments: dict[str, str | int | bool]
    current_state_ref: RefModel
    operator_actor: ActorRefModel
    expected_state_version: int = Field(ge=1)


class RevisionRequestInput(BaseModel):
    request_id: str
    run_ref: RefModel
    target_refs: list[RefModel]
    target_node_ids: list[str]
    category_id: str
    natural_language_request: str
    current_state_ref: RefModel
    evaluation_ref: RefModel | None
    jit_capsule_ref: RefModel
    permitted_tool_registry_ref: RefModel
    operator_actor: ActorRefModel
    expected_state_version: int = Field(ge=1)


class ChangeOperationModel(BaseModel):
    operation_id: str
    target_ref: RefModel
    target_node_id: str
    target_layer: str
    tool_id: str
    tool_version: str
    arguments: dict[str, str | int | bool]
    preconditions: list[str]
    expected_effect: str


class ChangeRequestProgramModel(BaseModel):
    program_id: str
    compilation_status: Literal["COMPILED", "NEEDS_CLARIFICATION", "DENIED"]
    request_ref: RefModel
    interpretation: str
    target_layer_or_nodes: list[str]
    exact_operations: list[ChangeOperationModel]
    declared_invariants: list[str]
    required_transformations: list[str]
    creative_degrees_of_freedom: list[str]
    invalidated_downstream_nodes: list[str]
    validation_plan: list[str]
    preview_required: bool
    confidence_micros: int
    escalation: str | None
    source_kind: Literal["NATURAL_LANGUAGE", "DIRECT_MANIPULATION"]
    expected_state_version: int
    program_sha256: str


class ExecuteRevisionResponse(BaseModel):
    program: ChangeRequestProgramModel


class ResolveExceptionInput(BaseModel):
    package_id: str
    decision: Literal["APPROVE", "REJECT", "REQUEST_REVISION", "SELECT_CANDIDATE", "SHIP"]
    operator_actor: ActorRefModel
    campaign_ref: RefModel


class ResolveExceptionResponse(BaseModel):
    campaign: "CampaignStateModel"
    exception_resolved: bool


class ShipRequestInput(BaseModel):
    ship_request_id: str
    campaign_ref: RefModel
    autonomy_mode: Literal["AUTOPILOT", "REVIEW_BEFORE_SHIP", "CHECKPOINTED", "SHADOW"]
    target_channel: str
    artifact_refs: list[ArtifactRefModel]
    evaluation_refs: list[RefModel]
    unresolved_exception_ids: list[str]
    operator_actor: ActorRefModel
    publication_authority_ref: RefModel | None
    publication_policy_ref: RefModel | None


class ShipDecisionModel(BaseModel):
    decision_id: str
    request_ref: RefModel
    status: Literal["AUTHORIZED", "DENIED"]
    denial_codes: list[str]
    authorized_artifact_refs: list[ArtifactRefModel]
    acknowledgement_required: bool
    decision_actor: ActorRefModel
    decision_sha256: str


class AuditExportManifestModel(BaseModel):
    export_id: str
    campaign_ref: RefModel
    source_refs: list[RefModel]
    semantic_refs: list[RefModel]
    run_refs: list[RefModel]
    artifact_refs: list[ArtifactRefModel]
    evaluation_refs: list[RefModel]
    command_refs: list[RefModel]
    receipt_refs: list[RefModel]
    human_resolution_refs: list[RefModel]
    ship_decision_ref: RefModel | None
    replay_instructions: list[str]
    export_sha256: str


# Re-export shared ref models from campaigns schema for convenience
RefModel = RefModel
ArtifactRefModel = ArtifactRefModel
ActorRefModel = ActorRefModel
AuthorityRefModel = AuthorityRefModel

# Resolve forward references — CampaignStateModel and CampaignOrderModel are
# defined in api.schemas.campaigns and were imported above so Pydantic can
# fully construct every model that references them via string forward refs.
ControlTowerProjectionModel.model_rebuild()
ResolveExceptionResponse.model_rebuild()
