"""Rejected candidate and coalition-fatality memory contracts for TS-CMF-035."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class RejectionCategory(str, Enum):
    source_unsupported = "source_unsupported"
    route_fit_failed = "route_fit_failed"
    boundary_bad = "boundary_bad"
    generic_or_centroid = "generic_or_centroid"
    sensitivity_or_consent = "sensitivity_or_consent"
    coalition_fatality = "coalition_fatality"


class NegativeEvidenceKind(str, Enum):
    rejected_candidate = "rejected_candidate"
    rejected_route = "rejected_route"
    coalition_fatality = "coalition_fatality"


class MemoryAdmissionCandidateStatus(str, Enum):
    proposed_requires_memory_gate = "proposed_requires_memory_gate"
    reviewed_by_memory_gate = "reviewed_by_memory_gate"
    rejected_by_memory_gate = "rejected_by_memory_gate"


class RejectedExpressionCandidate(BaseModel):
    schema_version: Literal["cmf.rejected_expression_candidate.v1"]
    rejected_candidate_id: UUID
    candidate_id: UUID
    expression_session_id: UUID
    category: RejectionCategory
    reason: str = Field(min_length=1)
    source_reference_ids: list[str] = Field(min_length=1)
    route_attempt_receipt_id: UUID | None = None
    reviewer_id: UUID | None = None
    consent_record_version_id: UUID | None = None
    consent_compatible: bool
    quarantined: bool = False
    usable_as_negative_evidence: bool
    admitted_as_truth: bool = False
    created_at: datetime


class RejectedRouteAttempt(BaseModel):
    schema_version: Literal["cmf.rejected_route_attempt.v1"]
    rejected_route_attempt_id: UUID
    asset_route_receipt_id: UUID
    expression_moment_id: UUID | None = None
    route_refs: list[str] = Field(default_factory=list)
    category: RejectionCategory
    source_gap: str | None = None
    route_fit_score: float | None = Field(default=None, ge=0, le=1)
    consent_record_version_id: UUID | None = None
    consent_compatible: bool
    quarantined: bool = False
    usable_as_negative_evidence: bool
    admitted_as_truth: bool = False
    created_at: datetime


class CoalitionFatalityRecord(BaseModel):
    schema_version: Literal["cmf.coalition_fatality_record.v1"]
    coalition_fatality_id: UUID
    matrix_brief_id: UUID | None = None
    primitive_candidate_ids: list[UUID] = Field(default_factory=list)
    edge_product_id: UUID | None = None
    failure_observation: str = Field(min_length=1)
    downstream_stage: str = Field(min_length=1)
    rejection_receipt_id: UUID
    usable_as_negative_evidence: bool
    admitted_as_truth: bool = False
    created_at: datetime


class NegativeEvidenceRef(BaseModel):
    schema_version: Literal["cmf.negative_evidence_ref.v1"]
    negative_evidence_ref_id: UUID
    evidence_kind: NegativeEvidenceKind
    source_record_id: UUID
    rejection_receipt_id: UUID
    compiler_or_evaluator: str = Field(min_length=1)
    usage_purpose: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    truth_admission_blocked: bool = True
    cited_at: datetime


class MemoryAdmissionCandidate(BaseModel):
    schema_version: Literal["cmf.memory_admission_candidate.v1"]
    memory_admission_candidate_id: UUID
    source_record_id: UUID
    rejection_receipt_id: UUID
    proposed_memory_scope: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    status: MemoryAdmissionCandidateStatus
    explicit_memory_gate_required: bool = True
    auto_admitted_to_memory: bool = False
    proposed_at: datetime


class RejectionReceipt(BaseModel):
    schema_version: Literal["cmf.rejection_receipt.v1"]
    rejection_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    category: RejectionCategory
    source_refs: list[str] = Field(min_length=1)
    reviewer_id: UUID | None = None
    rejected_candidate_id: UUID | None = None
    rejected_route_attempt_id: UUID | None = None
    coalition_fatality_id: UUID | None = None
    consent_record_version_id: UUID | None = None
    consent_compatible: bool
    quarantined: bool
    negative_evidence_eligible: bool
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    written_at: datetime


def new_rejection_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    category: RejectionCategory,
    source_refs: list[str],
    consent_compatible: bool,
    quarantined: bool,
    negative_evidence_eligible: bool,
    decision_code: str,
    evidence_refs: list[str],
    reviewer_id: UUID | None = None,
    rejected_candidate_id: UUID | None = None,
    rejected_route_attempt_id: UUID | None = None,
    coalition_fatality_id: UUID | None = None,
    consent_record_version_id: UUID | None = None,
) -> RejectionReceipt:
    return RejectionReceipt(
        schema_version="cmf.rejection_receipt.v1",
        rejection_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        category=category,
        source_refs=source_refs,
        reviewer_id=reviewer_id,
        rejected_candidate_id=rejected_candidate_id,
        rejected_route_attempt_id=rejected_route_attempt_id,
        coalition_fatality_id=coalition_fatality_id,
        consent_record_version_id=consent_record_version_id,
        consent_compatible=consent_compatible,
        quarantined=quarantined,
        negative_evidence_eligible=negative_evidence_eligible,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
