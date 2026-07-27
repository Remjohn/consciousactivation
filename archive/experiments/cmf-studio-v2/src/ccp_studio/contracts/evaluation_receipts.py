"""Evaluation receipt contracts for TS-CMF-050."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from ccp_studio.contracts.orchestration import utc_now


class EvaluationCategory(str, Enum):
    source_truth = "source_truth"
    doctrine_alignment = "doctrine_alignment"
    ccf_orchestration_lineage = "ccf_orchestration_lineage"
    primitive_registry_fidelity = "primitive_registry_fidelity"
    context_premise_integrity = "context_premise_integrity"
    narrative_induction_integrity = "narrative_induction_integrity"
    anchor_contract_integrity = "anchor_contract_integrity"
    brand_genesis_completeness = "brand_genesis_completeness"
    acting_library_coverage = "acting_library_coverage"
    papercut_rig_integrity = "papercut_rig_integrity"
    micro_semiotic_integrity = "micro_semiotic_integrity"
    animation_readiness = "animation_readiness"
    asset_generation_policy = "asset_generation_policy"
    archetype_fit = "archetype_fit"
    expression_depth = "expression_depth"
    identity_consistency = "identity_consistency"
    likeness = "likeness"
    composition = "composition"
    style = "style"
    motion_restraint = "motion_restraint"
    platform_fit = "platform_fit"
    negative_space = "negative_space"
    micro_semiotic_anchors = "micro_semiotic_anchors"
    routeability = "routeability"
    evaluation_target_coverage = "evaluation_target_coverage"
    publishing_readiness = "publishing_readiness"


class EvaluationObjectType(str, Enum):
    interview_brief = "interview_brief"
    interview_asset_contract = "interview_asset_contract"
    context_premise = "context_premise"
    matrix_brief = "matrix_brief"
    skill_output = "skill_output"
    expression_moment = "expression_moment"
    brand_genesis_session = "brand_genesis_session"
    brand_context_version = "brand_context_version"
    acting_library = "acting_library"
    acting_reference = "acting_reference"
    papercut_rig = "papercut_rig"
    rig_manifest = "rig_manifest"
    animation_plan = "animation_plan"
    render_output = "render_output"
    asset_package = "asset_package"
    scene_output = "scene_output"


class EvaluationDecision(str, Enum):
    passes_for_human_review = "passes_for_human_review"
    needs_revision = "needs_revision"
    blocked = "blocked"


class EvidenceClaimScope(str, Enum):
    supports = "supports"
    contradicts = "contradicts"
    contextualizes = "contextualizes"


class EvidencePointer(BaseModel):
    schema_version: Literal["cmf.evaluation_evidence_pointer.v1"] = "cmf.evaluation_evidence_pointer.v1"
    source_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    start_ms: int | None = Field(default=None, ge=0)
    end_ms: int | None = Field(default=None, ge=0)
    transcript_segment_id: str | None = None
    route: str | None = None
    claim_scope: EvidenceClaimScope
    note: str | None = None

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_ms is not None and self.start_ms is not None and self.end_ms <= self.start_ms:
            raise ValueError("end_ms must be greater than start_ms")
        return self


class EvaluationScore(BaseModel):
    schema_version: Literal["cmf.evaluation_score.v1"] = "cmf.evaluation_score.v1"
    category: EvaluationCategory
    score: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)
    passed: bool
    evidence: list[EvidencePointer] = Field(min_length=1)
    evaluator_version: str = Field(min_length=1)

    @model_validator(mode="after")
    def score_pass_matches_threshold(self):
        expected = self.score >= self.threshold
        if self.passed != expected:
            raise ValueError("passed must match score >= threshold")
        return self


class HardFailure(BaseModel):
    schema_version: Literal["cmf.evaluation_hard_failure.v1"] = "cmf.evaluation_hard_failure.v1"
    category: EvaluationCategory
    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    evidence: list[EvidencePointer] = Field(min_length=1)
    approval_blocker_code: str = Field(min_length=1)


class EvaluationThresholdProfile(BaseModel):
    schema_version: Literal["cmf.evaluation_threshold_profile.v1"]
    threshold_profile_id: str = Field(min_length=1)
    profile_name: str = Field(min_length=1)
    evaluator_version: str = Field(min_length=1)
    thresholds: dict[EvaluationCategory, float]
    hard_failure_categories: list[EvaluationCategory] = Field(default_factory=list)
    created_at: datetime

    @field_validator("thresholds")
    @classmethod
    def require_all_categories(cls, value: dict[EvaluationCategory, float]) -> dict[EvaluationCategory, float]:
        missing = [category.value for category in EvaluationCategory if category not in value]
        if missing:
            raise ValueError(f"threshold profile missing categories: {', '.join(missing)}")
        return value

    @model_validator(mode="after")
    def validate_threshold_values(self):
        invalid = [category.value for category, threshold in self.thresholds.items() if threshold < 0 or threshold > 1]
        if invalid:
            raise ValueError(f"thresholds must be between 0 and 1: {', '.join(invalid)}")
        return self


class EvaluationCategoryInput(BaseModel):
    category: EvaluationCategory
    score: float = Field(ge=0, le=1)
    evidence: list[EvidencePointer] = Field(min_length=1)
    evaluator_version: str = Field(min_length=1)
    hard_failure: bool = False
    hard_failure_code: str | None = None
    hard_failure_message: str | None = None
    approval_blocker_code: str = "evaluation_hard_failure"

    @model_validator(mode="after")
    def hard_failure_needs_code_and_message(self):
        if self.hard_failure and (not self.hard_failure_code or not self.hard_failure_message):
            raise ValueError("hard failure inputs require code and message")
        return self


class EvaluationReceipt(BaseModel):
    schema_version: Literal["cmf.evaluation_receipt.v1"]
    evaluation_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: EvaluationObjectType
    object_id: UUID
    object_hash: str = Field(min_length=1)
    previous_receipt_id: UUID | None = None
    threshold_profile_id: str = Field(min_length=1)
    scores: list[EvaluationScore] = Field(min_length=1)
    hard_failures: list[HardFailure] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    decision: EvaluationDecision
    created_by_actor_id: UUID
    command_id: UUID | None = None
    receipt_hash: str = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def require_unique_complete_categories(self):
        categories = [score.category for score in self.scores]
        if len(categories) != len(set(categories)):
            raise ValueError("evaluation receipt cannot contain duplicate category scores")
        missing = [category.value for category in EvaluationCategory if category not in categories]
        if missing:
            raise ValueError(f"evaluation receipt missing categories: {', '.join(missing)}")
        if self.hard_failures and self.decision != EvaluationDecision.blocked:
            raise ValueError("hard failures require blocked decision")
        if not self.hard_failures and self.decision == EvaluationDecision.blocked:
            raise ValueError("blocked decision requires at least one hard failure")
        return self


class EvaluationApprovalBlocker(BaseModel):
    schema_version: Literal["cmf.evaluation_approval_blocker.v1"]
    evaluation_approval_blocker_id: UUID
    evaluation_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: EvaluationObjectType
    object_id: UUID
    blocker_code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    repair_action: str = Field(min_length=1)
    created_at: datetime


class EvaluationDomainEvent(BaseModel):
    schema_version: Literal["cmf.evaluation_domain_event.v1"]
    evaluation_event_id: UUID
    event_type: str = Field(min_length=1)
    evaluation_receipt_id: UUID | None = None
    object_type: EvaluationObjectType | None = None
    object_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class EvaluationReviewReadModel(BaseModel):
    schema_version: Literal["cmf.evaluation_review_read_model.v1"]
    evaluation_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: EvaluationObjectType
    object_id: UUID
    object_hash: str
    previous_receipt_id: UUID | None = None
    threshold_profile_id: str
    category_scores: list[EvaluationScore]
    hard_failures: list[HardFailure]
    approval_blocker_ids: list[UUID]
    decision: EvaluationDecision
    evidence_source_ids: list[str]
    created_at: datetime


def evaluation_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def default_evaluation_threshold_profile() -> EvaluationThresholdProfile:
    return EvaluationThresholdProfile(
        schema_version="cmf.evaluation_threshold_profile.v1",
        threshold_profile_id="cmf.default.thresholds.v1",
        profile_name="CMF Default Evaluation Thresholds",
        evaluator_version="cmf-evaluator.v1",
        thresholds={category: 0.74 for category in EvaluationCategory},
        hard_failure_categories=list(EvaluationCategory),
        created_at=utc_now(),
    )


def evidence_ref(pointer: EvidencePointer) -> str:
    parts = [pointer.source_type, pointer.source_id]
    if pointer.transcript_segment_id:
        parts.append(pointer.transcript_segment_id)
    if pointer.start_ms is not None or pointer.end_ms is not None:
        parts.append(f"{pointer.start_ms or 0}-{pointer.end_ms or 0}ms")
    if pointer.route:
        parts.append(pointer.route)
    return ":".join(parts)


def new_evaluation_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    object_type: EvaluationObjectType | str,
    object_id: UUID,
    object_hash: str,
    threshold_profile_id: str,
    scores: list[EvaluationScore],
    hard_failures: list[HardFailure],
    warnings: list[str],
    created_by_actor_id: UUID,
    previous_receipt_id: UUID | None = None,
    command_id: UUID | None = None,
) -> EvaluationReceipt:
    failed_scores = [score for score in scores if not score.passed]
    if hard_failures:
        decision = EvaluationDecision.blocked
    elif failed_scores:
        decision = EvaluationDecision.needs_revision
    else:
        decision = EvaluationDecision.passes_for_human_review
    payload = {
        "organization_id": organization_id,
        "brand_id": brand_id,
        "object_type": str(object_type),
        "object_id": object_id,
        "object_hash": object_hash,
        "previous_receipt_id": previous_receipt_id,
        "threshold_profile_id": threshold_profile_id,
        "scores": [score.model_dump(mode="json") for score in scores],
        "hard_failures": [failure.model_dump(mode="json") for failure in hard_failures],
        "warnings": warnings,
        "decision": decision.value,
    }
    return EvaluationReceipt(
        schema_version="cmf.evaluation_receipt.v1",
        evaluation_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        object_type=EvaluationObjectType(object_type),
        object_id=object_id,
        object_hash=object_hash,
        previous_receipt_id=previous_receipt_id,
        threshold_profile_id=threshold_profile_id,
        scores=scores,
        hard_failures=hard_failures,
        warnings=warnings,
        decision=decision,
        created_by_actor_id=created_by_actor_id,
        command_id=command_id,
        receipt_hash=evaluation_hash(payload),
        created_at=utc_now(),
    )
