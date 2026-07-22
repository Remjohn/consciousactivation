"""Review evidence contracts for TS-CMF-012."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class ApprovalBlockerCode(str, Enum):
    missing_source_reference = "missing_source_reference"
    consent_incompatible = "consent_incompatible"
    provenance_missing = "provenance_missing"
    voice_classification_missing = "voice_classification_missing"
    voice_eligibility_failed = "voice_eligibility_failed"
    evaluation_receipt_missing = "evaluation_receipt_missing"
    evaluation_hard_failure = "evaluation_hard_failure"
    pwa_review_required = "pwa_review_required"


class SourceReference(BaseModel):
    schema_version: Literal["cmf.source_reference.v1"]
    source_reference_id: UUID
    source_artifact_id: UUID
    transcript_revision_id: UUID | None = None
    start_seconds: float | None = None
    end_seconds: float | None = None
    claim_ref: str | None = None

    @model_validator(mode="after")
    def validate_range(self):
        if self.start_seconds is not None and self.start_seconds < 0:
            raise ValueError("start_seconds must be non-negative")
        if self.end_seconds is not None and self.start_seconds is not None and self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")
        return self


class TranscriptRevisionSummary(BaseModel):
    schema_version: Literal["cmf.transcript_revision_summary.v1"]
    transcript_revision_id: UUID
    source_artifact_id: UUID
    revision_number: int = Field(ge=1)
    transcript_hash: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    text_ref: str = Field(min_length=1)
    created_at: datetime


class ApprovalBlocker(BaseModel):
    schema_version: Literal["cmf.approval_blocker.v1"]
    blocker_code: ApprovalBlockerCode
    message: str
    evidence_refs: list[str] = Field(default_factory=list)
    repair_action: str


class ApprovalEvidenceView(BaseModel):
    schema_version: Literal["cmf.approval_evidence_view.v1"]
    approval_evidence_view_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str
    object_id: UUID
    consent_record_version_id: UUID
    source_references: list[SourceReference]
    transcript_revision_ids: list[UUID]
    transcript_revisions: list[TranscriptRevisionSummary] = Field(default_factory=list)
    evaluation_receipt_ids: list[UUID]
    audio_mix_manifest_id: UUID | None = None
    file_provenance_refs: list[str] = Field(default_factory=list)
    voice_eligibility_report_id: UUID | None = None
    blockers: list[ApprovalBlocker] = Field(default_factory=list)
    telegram_complexity_score: int = 0
    generated_at: datetime


class ReviewEvidenceReceipt(BaseModel):
    schema_version: Literal["cmf.review_evidence_receipt.v1"]
    review_evidence_receipt_id: UUID
    approval_evidence_view_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str
    object_id: UUID
    decision_code: str
    blocker_codes: list[ApprovalBlockerCode] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


class ApprovalEventRecorded(BaseModel):
    schema_version: Literal["cmf.approval_event_recorded.v1"]
    approval_event_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str
    object_id: UUID
    approved_by_actor_id: UUID
    approval_evidence_view_id: UUID
    review_evidence_receipt_id: UUID
    consent_record_version_id: UUID
    source_reference_ids: list[UUID] = Field(min_length=1)
    evaluation_receipt_ids: list[UUID] = Field(min_length=1)
    audit_evidence_refs: list[str] = Field(min_length=1)
    recorded_at: datetime


def new_source_reference(
    *,
    source_artifact_id: UUID,
    transcript_revision_id: UUID | None = None,
    start_seconds: float | None = None,
    end_seconds: float | None = None,
    claim_ref: str | None = None,
) -> SourceReference:
    return SourceReference(
        schema_version="cmf.source_reference.v1",
        source_reference_id=uuid4(),
        source_artifact_id=source_artifact_id,
        transcript_revision_id=transcript_revision_id,
        start_seconds=start_seconds,
        end_seconds=end_seconds,
        claim_ref=claim_ref,
    )


def new_transcript_revision_summary(
    *,
    source_artifact_id: UUID,
    revision_number: int,
    transcript_hash: str,
    source_hash: str,
    text_ref: str,
) -> TranscriptRevisionSummary:
    return TranscriptRevisionSummary(
        schema_version="cmf.transcript_revision_summary.v1",
        transcript_revision_id=uuid4(),
        source_artifact_id=source_artifact_id,
        revision_number=revision_number,
        transcript_hash=transcript_hash,
        source_hash=source_hash,
        text_ref=text_ref,
        created_at=utc_now(),
    )
