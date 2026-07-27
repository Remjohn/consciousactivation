"""Anchor hit and Expression Moment candidate contracts for TS-CMF-031."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class CandidateStatus(str, Enum):
    needs_review = "needs_review"
    rejected_unsupported = "rejected_unsupported"
    ready_for_review = "ready_for_review"
    superseded = "superseded"


class AnchorType(str, Enum):
    first_line = "first_line"
    depth_anchor = "depth_anchor"
    emotional_shift = "emotional_shift"
    source_scene = "source_scene"


class ExtractionRunStatus(str, Enum):
    started = "started"
    completed = "completed"
    failed = "failed"


class SourceCue(BaseModel):
    schema_version: Literal["cmf.source_cue.v1"]
    source_cue_id: UUID
    expression_session_id: UUID
    transcript_revision_id: UUID
    source_artifact_id: UUID
    transcript_segment_ids: list[UUID] = Field(min_length=1)
    cue_type: str = Field(min_length=1)
    description: str = Field(min_length=1)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    confidence: float = Field(ge=0, le=1)


class TimestampedAnchorHit(BaseModel):
    schema_version: Literal["cmf.timestamped_anchor_hit.v1"]
    anchor_hit_id: UUID
    expression_session_id: UUID
    interview_asset_contract_id: UUID
    anchor_type: AnchorType
    transcript_segment_ids: list[UUID] = Field(min_length=1)
    source_artifact_id: UUID
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    confidence: float = Field(ge=0, le=1)
    evidence_text: str = Field(min_length=1)


class SkillExtractionContribution(BaseModel):
    schema_version: Literal["cmf.skill_extraction_contribution.v1"]
    skill_invocation_receipt_id: UUID
    skill_key: str = Field(min_length=1)
    saturation_context_hash: str = Field(min_length=1)
    contrast_output: list[str] = Field(min_length=1)
    anti_draft_passed: bool


class ExpressionMomentCandidate(BaseModel):
    schema_version: Literal["cmf.expression_moment_candidate.v1"]
    candidate_id: UUID
    expression_session_id: UUID
    transcript_revision_id: UUID
    source_artifact_id: UUID
    timestamp_start_ms: int = Field(ge=0)
    timestamp_end_ms: int = Field(ge=0)
    transcript_segment_ids: list[UUID] = Field(min_length=1)
    source_quote: str = Field(min_length=1)
    induction_context_ids: list[UUID] = Field(default_factory=list)
    interview_asset_contract_id: UUID | None = None
    anchor_hit_ids: list[UUID] = Field(default_factory=list)
    emotional_shift_evidence: list[str] = Field(default_factory=list)
    primitive_candidate_ids: list[UUID] = Field(default_factory=list)
    route_rationale: str = Field(min_length=1)
    skill_contribution_ids: list[UUID] = Field(default_factory=list)
    source_truth_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    status: CandidateStatus
    created_at: datetime


class ExtractionRun(BaseModel):
    schema_version: Literal["cmf.extraction_run.v1"]
    extraction_run_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    transcript_revision_id: UUID
    retry_of_run_id: UUID | None = None
    status: ExtractionRunStatus
    started_at: datetime
    completed_at: datetime | None = None


class ExtractionReceipt(BaseModel):
    schema_version: Literal["cmf.extraction_receipt.v1"]
    extraction_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    extraction_run_id: UUID
    selected_transcript_revision_id: UUID
    source_artifact_hashes: dict[UUID, str] = Field(default_factory=dict)
    anchor_hit_ids: list[UUID] = Field(default_factory=list)
    candidate_ids: list[UUID] = Field(default_factory=list)
    skill_invocation_receipt_ids: list[UUID] = Field(default_factory=list)
    evaluator_results: list[str] = Field(default_factory=list)
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


def new_extraction_run(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_session_id: UUID,
    transcript_revision_id: UUID,
    retry_of_run_id: UUID | None = None,
) -> ExtractionRun:
    return ExtractionRun(
        schema_version="cmf.extraction_run.v1",
        extraction_run_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        transcript_revision_id=transcript_revision_id,
        retry_of_run_id=retry_of_run_id,
        status=ExtractionRunStatus.started,
        started_at=utc_now(),
    )


def new_extraction_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_session_id: UUID,
    extraction_run_id: UUID,
    selected_transcript_revision_id: UUID,
    source_artifact_hashes: dict[UUID, str],
    anchor_hit_ids: list[UUID],
    candidate_ids: list[UUID],
    skill_invocation_receipt_ids: list[UUID],
    evaluator_results: list[str],
    decision_code: str,
    reviewer_actor_id: UUID | None = None,
) -> ExtractionReceipt:
    return ExtractionReceipt(
        schema_version="cmf.extraction_receipt.v1",
        extraction_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        extraction_run_id=extraction_run_id,
        selected_transcript_revision_id=selected_transcript_revision_id,
        source_artifact_hashes=source_artifact_hashes,
        anchor_hit_ids=anchor_hit_ids,
        candidate_ids=candidate_ids,
        skill_invocation_receipt_ids=skill_invocation_receipt_ids,
        evaluator_results=evaluator_results,
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
