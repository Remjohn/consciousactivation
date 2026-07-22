"""Review decision contracts for TS-CMF-052."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class ReviewDecisionType(str, Enum):
    approve = "approve"
    reject = "reject"
    request_revision = "request_revision"
    escalate = "escalate"
    request_voice_dna_boost = "request_voice_dna_boost"


class ReviewResultState(str, Enum):
    approved = "approved"
    rejected = "rejected"
    revision_requested = "revision_requested"
    blocked = "blocked"
    ready_for_review = "ready_for_review"
    voice_dna_boost_requested = "voice_dna_boost_requested"


class ReviewDecision(BaseModel):
    schema_version: Literal["cmf.review_decision.v1"]
    review_decision_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    reviewer_user_id: UUID
    decision_type: ReviewDecisionType
    object_version_hash: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    result_state: ReviewResultState
    blocker_codes: list[str] = Field(default_factory=list)
    created_at: datetime


class ReviewRevisionRequest(BaseModel):
    schema_version: Literal["cmf.review_revision_request.v1"]
    revision_request_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    failure_category: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    expected_repair: str = Field(min_length=8)
    requested_by_user_id: UUID
    created_at: datetime

    @model_validator(mode="after")
    def reject_vague_repairs(self):
        if self.expected_repair.strip().lower() in {"make it better", "improve", "fix"}:
            raise ValueError("revision request requires an exact repair target")
        return self


class ManualEscalation(BaseModel):
    schema_version: Literal["cmf.manual_escalation.v1"]
    manual_escalation_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    reason: str = Field(min_length=1)
    result_state: Literal["blocked", "ready_for_review"]
    blocker_codes: list[str] = Field(default_factory=list)
    escalated_by_user_id: UUID
    created_at: datetime


class ReviewApprovalEvent(BaseModel):
    schema_version: Literal["cmf.approval_event.v1"]
    approval_event_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    reviewer_user_id: UUID
    evidence_state_id: UUID
    evaluation_receipt_ids: list[UUID] = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    object_version_hash: str = Field(min_length=1)
    created_at: datetime


class VoiceDnaBoostRequest(BaseModel):
    schema_version: Literal["cmf.voice_dna_boost_request.v1"]
    request_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_id: UUID
    source_gap_ref: str = Field(min_length=1)
    eligibility_report_id: UUID
    requested_by_user_id: UUID
    evidence_refs: list[str] = Field(min_length=1)
    structural_repair_reason: str = Field(min_length=12)
    created_at: datetime


class ReviewDecisionReceipt(BaseModel):
    schema_version: Literal["cmf.review_decision_receipt.v1"]
    receipt_id: UUID
    decision_type: ReviewDecisionType
    command_id: UUID | None = None
    review_decision_id: UUID | None = None
    approval_event_id: UUID | None = None
    revision_request_id: UUID | None = None
    manual_escalation_id: UUID | None = None
    voice_dna_boost_request_id: UUID | None = None
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    object_version_hash: str = Field(min_length=1)
    result_state: ReviewResultState
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class ReviewDecisionDomainEvent(BaseModel):
    schema_version: Literal["cmf.review_decision_domain_event.v1"]
    review_decision_event_id: UUID
    event_type: str = Field(min_length=1)
    review_state_id: UUID
    object_type: str
    object_id: UUID
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def review_decision_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_review_decision_receipt(
    *,
    decision_type: ReviewDecisionType,
    organization_id: UUID,
    brand_id: UUID,
    review_state_id: UUID,
    object_type: str,
    object_id: UUID,
    object_version_hash: str,
    result_state: ReviewResultState,
    evidence_refs: list[str],
    blocker_codes: list[str] | None = None,
    command_id: UUID | None = None,
    review_decision_id: UUID | None = None,
    approval_event_id: UUID | None = None,
    revision_request_id: UUID | None = None,
    manual_escalation_id: UUID | None = None,
    voice_dna_boost_request_id: UUID | None = None,
) -> ReviewDecisionReceipt:
    payload = {
        "decision_type": decision_type.value,
        "organization_id": organization_id,
        "brand_id": brand_id,
        "review_state_id": review_state_id,
        "object_type": object_type,
        "object_id": object_id,
        "object_version_hash": object_version_hash,
        "result_state": result_state.value,
        "blocker_codes": blocker_codes or [],
        "evidence_refs": evidence_refs,
        "review_decision_id": review_decision_id,
        "approval_event_id": approval_event_id,
        "revision_request_id": revision_request_id,
        "manual_escalation_id": manual_escalation_id,
        "voice_dna_boost_request_id": voice_dna_boost_request_id,
    }
    return ReviewDecisionReceipt(
        schema_version="cmf.review_decision_receipt.v1",
        receipt_id=uuid4(),
        decision_type=decision_type,
        command_id=command_id,
        review_decision_id=review_decision_id,
        approval_event_id=approval_event_id,
        revision_request_id=revision_request_id,
        manual_escalation_id=manual_escalation_id,
        voice_dna_boost_request_id=voice_dna_boost_request_id,
        organization_id=organization_id,
        brand_id=brand_id,
        review_state_id=review_state_id,
        object_type=object_type,
        object_id=object_id,
        object_version_hash=object_version_hash,
        result_state=result_state,
        blocker_codes=blocker_codes or [],
        evidence_refs=evidence_refs,
        receipt_hash=review_decision_hash(payload),
        written_at=utc_now(),
    )

