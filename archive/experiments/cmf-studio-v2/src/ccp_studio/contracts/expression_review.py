"""Expression Moment review and boundary-control contracts for TS-CMF-032."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from ccp_studio.contracts.orchestration import utc_now


class ExpressionMomentStatus(str, Enum):
    candidate = "candidate"
    approved = "approved"
    rejected = "rejected"
    sensitivity_hold = "sensitivity_hold"
    superseded = "superseded"


class ReviewDecisionType(str, Enum):
    approve = "approve"
    reject = "reject"
    adjust_boundary = "adjust_boundary"
    split = "split"
    merge = "merge"
    annotate = "annotate"
    place_hold = "place_hold"
    release_hold = "release_hold"
    supersede = "supersede"


class ReviewRejectionCode(str, Enum):
    source_truth_insufficient = "source_truth_insufficient"
    boundary_unclear = "boundary_unclear"
    consent_or_sensitivity_risk = "consent_or_sensitivity_risk"
    route_not_supported = "route_not_supported"
    guest_dignity_risk = "guest_dignity_risk"


class SourceBoundaryRange(BaseModel):
    schema_version: Literal["cmf.source_boundary_range.v1"]
    source_artifact_id: UUID
    transcript_revision_id: UUID
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    transcript_segment_ids: list[UUID] = Field(min_length=1)

    @field_validator("end_ms")
    @classmethod
    def end_after_start(cls, value: int, info):
        start = info.data.get("start_ms")
        if start is not None and value <= start:
            raise ValueError("end_ms must be greater than start_ms")
        return value


class ExpressionMomentBoundary(BaseModel):
    schema_version: Literal["cmf.expression_moment_boundary.v1"]
    source_artifact_id: UUID
    transcript_revision_id: UUID
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    transcript_segment_ids: list[UUID] = Field(min_length=1)
    source_ranges: list[SourceBoundaryRange] = Field(default_factory=list)

    @field_validator("end_ms")
    @classmethod
    def end_after_start(cls, value: int, info):
        start = info.data.get("start_ms")
        if start is not None and value <= start:
            raise ValueError("end_ms must be greater than start_ms")
        return value

    def normalized_ranges(self) -> list[SourceBoundaryRange]:
        if self.source_ranges:
            return self.source_ranges
        return [
            SourceBoundaryRange(
                schema_version="cmf.source_boundary_range.v1",
                source_artifact_id=self.source_artifact_id,
                transcript_revision_id=self.transcript_revision_id,
                start_ms=self.start_ms,
                end_ms=self.end_ms,
                transcript_segment_ids=self.transcript_segment_ids,
            )
        ]


class SensitivityHold(BaseModel):
    schema_version: Literal["cmf.sensitivity_hold.v1"]
    sensitivity_hold_id: UUID
    expression_moment_id: UUID
    reason: str = Field(min_length=1)
    consent_record_version_id: UUID | None = None
    placed_by_user_id: UUID
    placed_at: datetime
    released_by_user_id: UUID | None = None
    released_at: datetime | None = None

    @property
    def active(self) -> bool:
        return self.released_at is None


class ExpressionMoment(BaseModel):
    schema_version: Literal["cmf.expression_moment.v1"]
    expression_moment_id: UUID
    source_candidate_ids: list[UUID] = Field(min_length=1)
    expression_session_id: UUID
    brand_id: UUID
    boundary: ExpressionMomentBoundary
    source_quote: str = Field(min_length=1)
    induction_context_ids: list[UUID] = Field(default_factory=list)
    route_rationale: str = Field(min_length=1)
    annotations: list[str] = Field(default_factory=list)
    status: ExpressionMomentStatus
    supersedes_expression_moment_ids: list[UUID] = Field(default_factory=list)
    superseded_by_expression_moment_id: UUID | None = None
    sensitivity_hold_id: UUID | None = None
    approved_at: datetime | None = None
    created_at: datetime


class ExpressionMomentReviewDecision(BaseModel):
    schema_version: Literal["cmf.expression_moment_review_decision.v1"]
    review_decision_id: UUID
    decision_type: ReviewDecisionType
    organization_id: UUID
    brand_id: UUID
    reviewer_actor_id: UUID
    expression_session_id: UUID
    source_candidate_ids: list[UUID] = Field(default_factory=list)
    prior_expression_moment_ids: list[UUID] = Field(default_factory=list)
    new_expression_moment_ids: list[UUID] = Field(default_factory=list)
    sensitivity_hold_id: UUID | None = None
    rejection_code: ReviewRejectionCode | None = None
    rationale: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    decided_at: datetime


class ExpressionMomentReviewSurfaceItem(BaseModel):
    schema_version: Literal["cmf.expression_moment_review_surface_item.v1"]
    candidate_id: UUID
    expression_session_id: UUID
    brand_id: UUID
    source_playback_ref: str = Field(min_length=1)
    transcript_revision_id: UUID
    transcript_segment_ids: list[UUID] = Field(min_length=1)
    transcript_excerpt: str = Field(min_length=1)
    timestamp_start_ms: int = Field(ge=0)
    timestamp_end_ms: int = Field(ge=0)
    induction_context_ids: list[UUID] = Field(default_factory=list)
    route_rationale: str = Field(min_length=1)
    sensitivity_flags: list[str] = Field(default_factory=list)
    source_truth_score: float = Field(ge=0, le=1)


class ExpressionReviewReceipt(BaseModel):
    schema_version: Literal["cmf.expression_review_receipt.v1"]
    expression_review_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    reviewer_actor_id: UUID
    decision_type: ReviewDecisionType
    review_decision_id: UUID
    source_candidate_ids: list[UUID] = Field(default_factory=list)
    prior_expression_moment_ids: list[UUID] = Field(default_factory=list)
    new_expression_moment_ids: list[UUID] = Field(default_factory=list)
    source_ranges: list[SourceBoundaryRange] = Field(default_factory=list)
    sensitivity_hold_id: UUID | None = None
    rejection_code: ReviewRejectionCode | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    written_at: datetime


def boundary_from_candidate(
    *,
    source_artifact_id: UUID,
    transcript_revision_id: UUID,
    start_ms: int,
    end_ms: int,
    transcript_segment_ids: list[UUID],
    source_ranges: list[SourceBoundaryRange] | None = None,
) -> ExpressionMomentBoundary:
    return ExpressionMomentBoundary(
        schema_version="cmf.expression_moment_boundary.v1",
        source_artifact_id=source_artifact_id,
        transcript_revision_id=transcript_revision_id,
        start_ms=start_ms,
        end_ms=end_ms,
        transcript_segment_ids=transcript_segment_ids,
        source_ranges=source_ranges or [],
    )


def new_expression_moment(
    *,
    source_candidate_ids: list[UUID],
    expression_session_id: UUID,
    brand_id: UUID,
    boundary: ExpressionMomentBoundary,
    source_quote: str,
    induction_context_ids: list[UUID],
    route_rationale: str,
    status: ExpressionMomentStatus,
    annotations: list[str] | None = None,
    supersedes_expression_moment_ids: list[UUID] | None = None,
    sensitivity_hold_id: UUID | None = None,
) -> ExpressionMoment:
    return ExpressionMoment(
        schema_version="cmf.expression_moment.v1",
        expression_moment_id=uuid4(),
        source_candidate_ids=source_candidate_ids,
        expression_session_id=expression_session_id,
        brand_id=brand_id,
        boundary=boundary,
        source_quote=source_quote,
        induction_context_ids=induction_context_ids,
        route_rationale=route_rationale,
        annotations=annotations or [],
        status=status,
        supersedes_expression_moment_ids=supersedes_expression_moment_ids or [],
        sensitivity_hold_id=sensitivity_hold_id,
        approved_at=utc_now() if status == ExpressionMomentStatus.approved else None,
        created_at=utc_now(),
    )


def new_review_decision(
    *,
    decision_type: ReviewDecisionType,
    organization_id: UUID,
    brand_id: UUID,
    reviewer_actor_id: UUID,
    expression_session_id: UUID,
    rationale: str,
    evidence_refs: list[str],
    source_candidate_ids: list[UUID] | None = None,
    prior_expression_moment_ids: list[UUID] | None = None,
    new_expression_moment_ids: list[UUID] | None = None,
    sensitivity_hold_id: UUID | None = None,
    rejection_code: ReviewRejectionCode | None = None,
) -> ExpressionMomentReviewDecision:
    return ExpressionMomentReviewDecision(
        schema_version="cmf.expression_moment_review_decision.v1",
        review_decision_id=uuid4(),
        decision_type=decision_type,
        organization_id=organization_id,
        brand_id=brand_id,
        reviewer_actor_id=reviewer_actor_id,
        expression_session_id=expression_session_id,
        source_candidate_ids=source_candidate_ids or [],
        prior_expression_moment_ids=prior_expression_moment_ids or [],
        new_expression_moment_ids=new_expression_moment_ids or [],
        sensitivity_hold_id=sensitivity_hold_id,
        rejection_code=rejection_code,
        rationale=rationale,
        evidence_refs=evidence_refs,
        decided_at=utc_now(),
    )


def new_expression_review_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_session_id: UUID,
    reviewer_actor_id: UUID,
    decision_type: ReviewDecisionType,
    review_decision_id: UUID,
    evidence_refs: list[str],
    decision_code: str,
    source_candidate_ids: list[UUID] | None = None,
    prior_expression_moment_ids: list[UUID] | None = None,
    new_expression_moment_ids: list[UUID] | None = None,
    source_ranges: list[SourceBoundaryRange] | None = None,
    sensitivity_hold_id: UUID | None = None,
    rejection_code: ReviewRejectionCode | None = None,
) -> ExpressionReviewReceipt:
    return ExpressionReviewReceipt(
        schema_version="cmf.expression_review_receipt.v1",
        expression_review_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        reviewer_actor_id=reviewer_actor_id,
        decision_type=decision_type,
        review_decision_id=review_decision_id,
        source_candidate_ids=source_candidate_ids or [],
        prior_expression_moment_ids=prior_expression_moment_ids or [],
        new_expression_moment_ids=new_expression_moment_ids or [],
        source_ranges=source_ranges or [],
        sensitivity_hold_id=sensitivity_hold_id,
        rejection_code=rejection_code,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
