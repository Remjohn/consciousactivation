"""Interviewer pre-induction contracts for TS-CMF-026."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class InductionRiskLevel(str, Enum):
    low = "low"
    review = "review"
    blocked = "blocked"


class PreInductionPlanStatus(str, Enum):
    draft = "draft"
    evaluated = "evaluated"
    blocked = "blocked"
    approved = "approved"
    superseded = "superseded"


class QuestionAvoidanceRule(BaseModel):
    schema_version: Literal["cmf.question_avoidance_rule.v1"]
    rule_id: UUID
    reason: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(min_length=1)
    safer_route: str = Field(min_length=1)


class InductionBridge(BaseModel):
    schema_version: Literal["cmf.induction_bridge.v1"]
    bridge_id: UUID
    emotional_bridge: str = Field(min_length=1)
    guest_specific_resonance: str = Field(min_length=1)
    matrix_edge_product_id: UUID | None = None
    evidence_ids: list[UUID] = Field(min_length=1)


class PreInductionQuestion(BaseModel):
    schema_version: Literal["cmf.pre_induction_question.v1"]
    question_id: UUID
    natural_question: str = Field(min_length=1)
    authentic_curiosity: str = Field(min_length=1)
    first_line_anchor_options: list[str] = Field(default_factory=list)
    depth_anchor: str | None = None
    centroid_risk: InductionRiskLevel
    manipulation_risk: InductionRiskLevel
    rationale_id: UUID | None = None
    evidence_ids: list[UUID] = Field(min_length=1)
    matrix_edge_product_id: UUID | None = None


class OperatorEdit(BaseModel):
    schema_version: Literal["cmf.operator_edit.v1"]
    operator_edit_id: UUID
    pre_induction_plan_id: UUID
    question_id: UUID
    previous_question: str = Field(min_length=1)
    revised_question: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(min_length=1)
    rationale: str = Field(min_length=1)
    edited_by_actor_id: UUID
    edited_at: datetime


class LiveInterviewModeBinding(BaseModel):
    schema_version: Literal["cmf.live_interview_mode_binding.v1"]
    live_interview_mode_binding_id: UUID
    pre_induction_plan_id: UUID
    organization_id: UUID
    brand_id: UUID
    read_only: bool = True
    operator_judgment_required: bool = True
    bound_at: datetime


class PreInductionPlan(BaseModel):
    schema_version: Literal["cmf.pre_induction_plan.v1"]
    pre_induction_plan_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    operator_id: UUID
    context_premise_id: UUID
    matrix_brief_id: UUID
    resonance_context_id: UUID | None = None
    opening_state: str = Field(min_length=1)
    bridges: list[InductionBridge] = Field(min_length=1)
    questions_to_avoid: list[QuestionAvoidanceRule] = Field(min_length=1)
    planned_questions: list[PreInductionQuestion] = Field(min_length=1)
    operator_edit_ids: list[UUID] = Field(default_factory=list)
    status: PreInductionPlanStatus
    version: int = 1
    approved_at: datetime | None = None
    live_interview_mode_binding_id: UUID | None = None
    created_at: datetime
    updated_at: datetime


class PreInductionReceipt(BaseModel):
    schema_version: Literal["cmf.pre_induction_receipt.v1"]
    pre_induction_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    pre_induction_plan_id: UUID
    context_premise_id: UUID
    matrix_brief_id: UUID
    risk_scores: dict[str, float] = Field(default_factory=dict)
    edit_trail_ids: list[UUID] = Field(default_factory=list)
    approval_state: str = Field(min_length=1)
    live_interview_mode_binding_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


def new_pre_induction_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    pre_induction_plan_id: UUID,
    context_premise_id: UUID,
    matrix_brief_id: UUID,
    risk_scores: dict[str, float],
    edit_trail_ids: list[UUID],
    approval_state: str,
    decision_code: str,
    live_interview_mode_binding_id: UUID | None = None,
    reviewer_actor_id: UUID | None = None,
) -> PreInductionReceipt:
    return PreInductionReceipt(
        schema_version="cmf.pre_induction_receipt.v1",
        pre_induction_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        pre_induction_plan_id=pre_induction_plan_id,
        context_premise_id=context_premise_id,
        matrix_brief_id=matrix_brief_id,
        risk_scores=risk_scores,
        edit_trail_ids=edit_trail_ids,
        approval_state=approval_state,
        live_interview_mode_binding_id=live_interview_mode_binding_id,
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
