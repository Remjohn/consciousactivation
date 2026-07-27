"""Evidence-backed memory admission contracts for TS-CMF-056."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class MemoryEventType(str, Enum):
    brand = "brand"
    interviewer = "interviewer"
    route = "route"
    anchor = "anchor"
    archetype_survival = "archetype_survival"
    rejected_pattern = "rejected_pattern"
    publishing_performance = "publishing_performance"


class MemoryScope(str, Enum):
    brand = "brand"
    guest = "guest"
    session = "session"
    route = "route"
    interviewer = "interviewer"
    global_fixture = "global_fixture"


class MemoryClaimScope(str, Enum):
    supports = "supports"
    contradicts = "contradicts"
    contextualizes = "contextualizes"


class MemoryEventStatus(str, Enum):
    approved = "approved"
    rejected = "rejected"
    quarantined = "quarantined"


class MemoryAdmissionPolicyResult(str, Enum):
    proposed = "proposed"
    approved = "approved"
    rejected = "rejected"
    quarantined = "quarantined"


class MemoryEvidenceRef(BaseModel):
    schema_version: Literal["cmf.memory_evidence_ref.v1"] = "cmf.memory_evidence_ref.v1"
    source_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    evidence_uri: str | None = None
    transcript_segment_id: str | None = None
    receipt_id: str | None = None
    claim_scope: MemoryClaimScope

    @model_validator(mode="after")
    def require_evidence_pointer(self):
        if not any([self.evidence_uri, self.transcript_segment_id, self.receipt_id]):
            raise ValueError("memory evidence requires evidence_uri, transcript_segment_id, or receipt_id")
        return self


class MemoryAdmissionCandidate(BaseModel):
    schema_version: Literal["cmf.memory_admission_candidate.v1"]
    candidate_id: UUID
    organization_id: UUID
    brand_id: UUID
    memory_type: MemoryEventType
    proposed_from_event_id: str = Field(min_length=1)
    proposed_statement: str = Field(min_length=1)
    evidence_refs: list[MemoryEvidenceRef] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    scope: MemoryScope
    consent_record_version_id: UUID | None = None
    consent_compatible: bool
    originating_route_ref: str | None = None
    provenance_summary: str = Field(min_length=1)
    proposed_by_actor_id: UUID
    downstream_usage_constraints: list[str] = Field(default_factory=lambda: ["must_cite_memory_event_and_evidence_refs"])
    created_at: datetime


class MemoryPolicyDecision(BaseModel):
    schema_version: Literal["cmf.memory_policy_decision.v1"]
    candidate_id: UUID
    evidence_valid: bool
    consent_valid: bool
    confidence_valid: bool
    provenance_valid: bool
    statement_specific: bool
    blockers: list[str] = Field(default_factory=list)
    result: MemoryAdmissionPolicyResult
    checked_at: datetime


class MemoryEvent(BaseModel):
    schema_version: Literal["cmf.memory_event.v1"]
    memory_event_id: UUID
    candidate_id: UUID
    organization_id: UUID
    brand_id: UUID
    memory_type: MemoryEventType
    status: MemoryEventStatus
    approved_by: UUID | None = None
    proposed_statement: str = Field(min_length=1)
    scope: MemoryScope
    originating_route_ref: str | None = None
    evidence_refs: list[MemoryEvidenceRef]
    provenance_summary: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    consent_record_version_id: UUID | None = None
    created_at: datetime


class MemoryUsageCitation(BaseModel):
    schema_version: Literal["cmf.memory_usage_citation.v1"]
    memory_usage_citation_id: UUID
    memory_event_id: UUID
    compiler_or_agent: str = Field(min_length=1)
    citing_object_ref: str = Field(min_length=1)
    evidence_refs: list[MemoryEvidenceRef] = Field(min_length=1)
    memory_statement: str = Field(min_length=1)
    cited_at: datetime


class MemoryAdmissionReceipt(BaseModel):
    schema_version: Literal["cmf.memory_admission_receipt.v1"]
    memory_admission_receipt_id: UUID
    candidate_id: UUID
    memory_event_id: UUID | None = None
    organization_id: UUID
    brand_id: UUID
    source_refs: list[str] = Field(default_factory=list)
    provenance_summary: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    consent_compatible: bool
    scope: MemoryScope
    reviewer_id: UUID | None = None
    policy_result: MemoryAdmissionPolicyResult
    blocker_codes: list[str] = Field(default_factory=list)
    downstream_citation_required: bool = True
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class MemoryAdmissionDomainEvent(BaseModel):
    schema_version: Literal["cmf.memory_admission_domain_event.v1"]
    memory_admission_event_id: UUID
    event_type: str = Field(min_length=1)
    candidate_id: UUID | None = None
    memory_event_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def memory_admission_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def memory_source_refs(candidate: MemoryAdmissionCandidate) -> list[str]:
    refs = [candidate.proposed_from_event_id]
    if candidate.originating_route_ref:
        refs.append(candidate.originating_route_ref)
    for ref in candidate.evidence_refs:
        refs.append(f"{ref.source_type}:{ref.source_id}")
        if ref.receipt_id:
            refs.append(f"receipt:{ref.receipt_id}")
        if ref.transcript_segment_id:
            refs.append(f"transcript_segment:{ref.transcript_segment_id}")
    return sorted(set(refs))


def new_memory_event(
    *,
    candidate: MemoryAdmissionCandidate,
    status: MemoryEventStatus,
    approved_by: UUID | None = None,
) -> MemoryEvent:
    return MemoryEvent(
        schema_version="cmf.memory_event.v1",
        memory_event_id=uuid4(),
        candidate_id=candidate.candidate_id,
        organization_id=candidate.organization_id,
        brand_id=candidate.brand_id,
        memory_type=candidate.memory_type,
        status=status,
        approved_by=approved_by,
        proposed_statement=candidate.proposed_statement,
        scope=candidate.scope,
        originating_route_ref=candidate.originating_route_ref,
        evidence_refs=candidate.evidence_refs,
        provenance_summary=candidate.provenance_summary,
        confidence=candidate.confidence,
        consent_record_version_id=candidate.consent_record_version_id,
        created_at=utc_now(),
    )


def new_memory_admission_receipt(
    *,
    candidate: MemoryAdmissionCandidate,
    policy_result: MemoryAdmissionPolicyResult,
    memory_event_id: UUID | None = None,
    reviewer_id: UUID | None = None,
    blocker_codes: list[str] | None = None,
) -> MemoryAdmissionReceipt:
    source_refs = memory_source_refs(candidate)
    payload = {
        "candidate_id": candidate.candidate_id,
        "memory_event_id": memory_event_id,
        "organization_id": candidate.organization_id,
        "brand_id": candidate.brand_id,
        "source_refs": source_refs,
        "provenance_summary": candidate.provenance_summary,
        "confidence": candidate.confidence,
        "consent_compatible": candidate.consent_compatible,
        "scope": candidate.scope.value,
        "reviewer_id": reviewer_id,
        "policy_result": policy_result.value,
        "blocker_codes": blocker_codes or [],
        "downstream_citation_required": True,
    }
    return MemoryAdmissionReceipt(
        schema_version="cmf.memory_admission_receipt.v1",
        memory_admission_receipt_id=uuid4(),
        candidate_id=candidate.candidate_id,
        memory_event_id=memory_event_id,
        organization_id=candidate.organization_id,
        brand_id=candidate.brand_id,
        source_refs=source_refs,
        provenance_summary=candidate.provenance_summary,
        confidence=candidate.confidence,
        consent_compatible=candidate.consent_compatible,
        scope=candidate.scope,
        reviewer_id=reviewer_id,
        policy_result=policy_result,
        blocker_codes=blocker_codes or [],
        downstream_citation_required=True,
        receipt_hash=memory_admission_hash(payload),
        written_at=utc_now(),
    )
