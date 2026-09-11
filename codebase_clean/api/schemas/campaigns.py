from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from api.schemas.interviews import RefModel  # {object_id, version, sha256}, reused unchanged

OutputType = Literal["SOURCE_LED_SHORT", "CAROUSEL", "SUPERVISUAL", "ANIMATION_SCENE_PACKAGE", "ANIMATION_SHORT"]
AutonomyMode = Literal["AUTOPILOT", "REVIEW_BEFORE_SHIP", "CHECKPOINTED", "SHADOW"]
LifecycleState = Literal[
    "DRAFT", "LAUNCHED", "RUNNING", "AWAITING_REVIEW",
    "BLOCKED_EXCEPTION", "READY_TO_SHIP", "SHIPPED", "CANCELLED",
]


class OutputTargetModel(BaseModel):
    output_type: OutputType
    quantity: int = Field(ge=1)
    profile_id: str


class AutonomyPolicyModel(BaseModel):
    mode: AutonomyMode
    checkpoint_ids: list[str]
    exception_only: bool
    final_review_required: bool
    publication_authority_required: bool


class ActorRefModel(BaseModel):
    actor_id: str
    actor_type: Literal["deterministic_module", "model_program", "human"]
    product_id: str
    workflow_role: Literal["hunter", "analyst", "composer", "commander", "evaluator", "operator"]


class AuthorityRefModel(BaseModel):
    authority_id: str
    authority_version: str
    authority_sha256: str
    authority_state: Literal["current", "candidate_not_current"]


class ArtifactRefModel(BaseModel):
    artifact_id: str
    artifact_kind: str
    bytes: int
    media_type: str
    sha256: str
    uri: str


class CampaignCreateRequest(BaseModel):
    idempotency_key: str
    workspace_id: str
    project_id: str
    source_package_id: str
    harness_definition_id: str
    category_id: str
    format_profile_id: str
    objective: str
    initial_seed: str
    taste_direction: list[str] = Field(default_factory=list)
    output_targets: list[OutputTargetModel]
    budget_units: int
    deadline_utc: str | None = None
    autonomy_mode: AutonomyMode
    operator_id: str
    # --- patch-in-real-refs fields (TS-APP-API-004 patched per original prompt) ---
    pipeline_trigger: dict | None = Field(
        default=None,
        description=(
            "When supplied, the router calls AIR endpoints and"
            " compile_portable_to_intake() to obtain real refs before"
            " recording the campaign. When absent (the default),"
            " pipeline_ingestion_status remains NOT_YET_TRIGGERED."
        ),
    )


class CampaignOrderModel(BaseModel):
    order_id: str
    workspace_id: str
    project_id: str
    source_kind: Literal["CANONICAL_INTERVIEW_SOURCE_PACKAGE", "ASSET_PACKAGE_SPEC"]
    source_ref: RefModel
    harness_ref: RefModel
    category_id: str
    format_profile_id: str
    objective: str
    initial_seed: str
    taste_direction: list[str]
    output_targets: list[OutputTargetModel]
    budget_units: int
    deadline_utc: str | None
    autonomy_policy: AutonomyPolicyModel
    operator_actor: ActorRefModel
    authority: AuthorityRefModel


class CampaignStateModel(BaseModel):
    campaign_id: str
    order_ref: RefModel
    lifecycle_state: LifecycleState
    autonomy_mode: AutonomyMode
    active_checkpoint_id: str | None
    exception_ids: list[str]
    run_refs: list[RefModel]
    artifact_refs: list[ArtifactRefModel]
    evaluation_refs: list[RefModel]
    version: int


class CampaignDetailResponse(BaseModel):
    order: CampaignOrderModel
    state: CampaignStateModel
    source_derivative_eligible: bool
    source_lifecycle_state: str
    pipeline_ingestion_status: Literal[
        "NOT_YET_TRIGGERED", "BRIDGE_SUCCEEDED", "BRIDGE_BLOCKED"
    ]
    pipeline_ingestion_blocked_reason: str | None = None
    pipeline_refs: dict | None = None
    idempotent_replay: bool


class CampaignSummary(BaseModel):
    campaign_id: str
    order_id: str
    workspace_id: str
    project_id: str
    category_id: str
    lifecycle_state: LifecycleState
    autonomy_mode: AutonomyMode
    output_target_count: int
    budget_units: int
    version: int


class CampaignCancelRequest(BaseModel):
    expected_version: int
    reason: str = ""
