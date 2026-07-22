"""Interview Asset Contract contracts for TS-CMF-027."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ExpressionState(str, Enum):
    cinematic = "cinematic"
    vulnerability = "vulnerability"
    authority = "authority"
    meaning = "meaning"
    invitation = "invitation"
    teaching = "teaching"


class InterviewContractStatus(str, Enum):
    draft = "draft"
    evaluated = "evaluated"
    rejected = "rejected"
    approved = "approved"
    bound_to_session = "bound_to_session"
    superseded = "superseded"


class FirstLineAnchorSet(BaseModel):
    schema_version: Literal["cmf.first_line_anchor_set.v1"]
    cinematic: str | None = None
    emotional: str | None = None
    reels_hook: str | None = None

    @property
    def complete(self) -> bool:
        return bool(self.cinematic and self.emotional and self.reels_hook)


class RepairFollowups(BaseModel):
    schema_version: Literal["cmf.repair_followups.v1"]
    too_historical: str = Field(min_length=1)
    too_abstract: str = Field(min_length=1)
    too_flat: str = Field(min_length=1)
    not_clip_ready: str = Field(min_length=1)


class ContractRouteTarget(BaseModel):
    schema_version: Literal["cmf.contract_route_target.v1"]
    core_archetype_ref: str = Field(min_length=1)
    asset_derivative_refs: list[str] = Field(default_factory=list)
    meme_mechanism_refs: list[str] = Field(default_factory=list)
    reaction_archetype_refs: list[str] = Field(default_factory=list)
    cmf_render_mode_refs: list[str] = Field(default_factory=list)
    guest_asset_pack_potential: list[str] = Field(default_factory=list)


class InterviewAssetContract(BaseModel):
    schema_version: Literal["cmf.interview_asset_contract.v1"]
    contract_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    operator_id: UUID
    pre_induction_plan_id: UUID
    question_id: UUID
    main_question: str = Field(min_length=1)
    target_expression_states: list[ExpressionState] = Field(min_length=1)
    route_target: ContractRouteTarget
    edge_product_id: UUID
    first_line_anchors: FirstLineAnchorSet
    depth_anchor: str = Field(min_length=1)
    expected_source_material: list[str] = Field(min_length=1)
    clip_start_rule: str = Field(min_length=1)
    depth_eval_rule: str = Field(min_length=1)
    landing_eval_targets: list[str] = Field(min_length=1)
    repair_followups: RepairFollowups
    evidence_ids: list[UUID] = Field(default_factory=list)
    matrix_brief_id: UUID
    induction_rationale_ids: list[UUID] = Field(default_factory=list)
    status: InterviewContractStatus
    created_at: datetime
    updated_at: datetime


class InterviewDeck(BaseModel):
    schema_version: Literal["cmf.interview_deck.v1"]
    interview_deck_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    pre_induction_plan_id: UUID
    matrix_brief_id: UUID
    contract_ids: list[UUID] = Field(min_length=1)
    evaluation_receipt_id: UUID | None = None
    approved_for_session: bool = False
    status: InterviewContractStatus
    created_at: datetime
    updated_at: datetime


class InterviewPlanEvaluationScores(BaseModel):
    schema_version: Literal["cmf.interview_plan_evaluation_scores.v1"]
    saturation_score: float = Field(ge=0, le=1)
    collision_strength_score: float = Field(ge=0, le=1)
    specificity_score: float = Field(ge=0, le=1)
    routeability_score: float = Field(ge=0, le=1)
    expression_archetype_separation_score: float = Field(ge=0, le=1)


class ContractCompilationReceipt(BaseModel):
    schema_version: Literal["cmf.contract_compilation_receipt.v1"]
    contract_compilation_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    interview_deck_id: UUID | None = None
    contract_ids: list[UUID] = Field(default_factory=list)
    input_artifact_ids: dict[str, UUID] = Field(default_factory=dict)
    registry_versions: dict[str, str] = Field(default_factory=dict)
    route_targets: list[ContractRouteTarget] = Field(default_factory=list)
    evaluation_scores: InterviewPlanEvaluationScores | None = None
    failure_reasons: list[str] = Field(default_factory=list)
    approval_state: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


class DeckSessionBinding(BaseModel):
    schema_version: Literal["cmf.deck_session_binding.v1"]
    deck_session_binding_id: UUID
    organization_id: UUID
    brand_id: UUID
    interview_deck_id: UUID
    expression_session_id: UUID
    contract_ids: list[UUID] = Field(min_length=1)
    read_only_contracts: bool = True
    bound_at: datetime


class ContractInductionContext(BaseModel):
    schema_version: Literal["cmf.contract_induction_context.v1"]
    contract_id: UUID
    pre_induction_plan_id: UUID
    matrix_brief_id: UUID
    edge_product_id: UUID
    target_expression_states: list[ExpressionState] = Field(min_length=1)
    route_target: ContractRouteTarget
    evidence_ids: list[UUID] = Field(min_length=1)
    induction_rationale_ids: list[UUID] = Field(default_factory=list)


def new_contract_compilation_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    interview_deck_id: UUID | None,
    contract_ids: list[UUID],
    input_artifact_ids: dict[str, UUID],
    registry_versions: dict[str, str],
    route_targets: list[ContractRouteTarget],
    evaluation_scores: InterviewPlanEvaluationScores | None,
    failure_reasons: list[str],
    approval_state: str,
    decision_code: str,
    reviewer_actor_id: UUID | None = None,
) -> ContractCompilationReceipt:
    return ContractCompilationReceipt(
        schema_version="cmf.contract_compilation_receipt.v1",
        contract_compilation_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        interview_deck_id=interview_deck_id,
        contract_ids=contract_ids,
        input_artifact_ids=input_artifact_ids,
        registry_versions=registry_versions,
        route_targets=route_targets,
        evaluation_scores=evaluation_scores,
        failure_reasons=failure_reasons,
        approval_state=approval_state,
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
