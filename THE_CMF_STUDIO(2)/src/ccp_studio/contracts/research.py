"""Research field and evidence contracts for TS-CMF-023."""

from __future__ import annotations

import hashlib
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from ccp_studio.contracts.orchestration import utc_now


class ResearchEvidenceStatus(str, Enum):
    draft = "draft"
    provenance_ready = "provenance_ready"
    approved_for_use = "approved_for_use"
    stale_review_required = "stale_review_required"
    rejected = "rejected"


class SourceRole(str, Enum):
    primary_source = "primary_source"
    public_context = "public_context"
    audience_signal = "audience_signal"
    cral_signal = "cral_signal"
    operator_note = "operator_note"
    inference = "inference"


class TemporalSensitivity(str, Enum):
    evergreen = "evergreen"
    low = "low"
    medium = "medium"
    high = "high"


class EvidenceCitation(BaseModel):
    schema_version: Literal["cmf.evidence_citation.v1"]
    citation_id: UUID
    uri: HttpUrl | None = None
    title: str = Field(min_length=1)
    retrieved_at: datetime
    quoted_span_ref: str | None = None
    source_hash: str | None = None


class ResearchEvidence(BaseModel):
    schema_version: Literal["cmf.research_evidence.v1"]
    evidence_id: UUID
    research_field_id: UUID
    organization_id: UUID
    brand_id: UUID
    claim: str = Field(min_length=1)
    source_role: SourceRole
    citations: list[EvidenceCitation] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    temporal_sensitivity: TemporalSensitivity
    freshness_due_at: datetime | None = None
    provenance_summary: str = ""
    contradiction_notes: list[str] = Field(default_factory=list)
    research_gap: bool = False
    primitive_family_hints: list[str] = Field(default_factory=list)
    status: ResearchEvidenceStatus
    created_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ResearchField(BaseModel):
    schema_version: Literal["cmf.research_field.v1"]
    research_field_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    objective: str = Field(min_length=1)
    source_scope: list[str] = Field(min_length=1)
    evidence_ids: list[UUID] = Field(default_factory=list)
    approved_evidence_ids: list[UUID] = Field(default_factory=list)
    frozen_snapshot_ids: list[UUID] = Field(default_factory=list)
    created_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ResearchEvidenceReceipt(BaseModel):
    schema_version: Literal["cmf.research_evidence_receipt.v1"]
    research_evidence_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    evidence_ids: list[UUID]
    citation_hashes: list[str] = Field(default_factory=list)
    freshness_policy: str
    validator_actor_id: UUID
    decision_code: str
    written_at: datetime


class ResearchSnapshot(BaseModel):
    schema_version: Literal["cmf.research_snapshot.v1"]
    research_snapshot_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    approved_evidence_ids: list[UUID]
    research_evidence_receipt_ids: list[UUID]
    saturation_quality: str
    frozen_by_actor_id: UUID
    frozen_at: datetime


def citation_hash(citation: EvidenceCitation) -> str:
    return hashlib.sha256(
        "|".join(
            [
                str(citation.uri or ""),
                citation.title,
                citation.retrieved_at.isoformat(),
                citation.quoted_span_ref or "",
                citation.source_hash or "",
            ]
        ).encode("utf-8")
    ).hexdigest()


def new_research_evidence_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    research_field_id: UUID,
    evidence_ids: list[UUID],
    citations: list[EvidenceCitation],
    freshness_policy: str,
    validator_actor_id: UUID,
    decision_code: str,
) -> ResearchEvidenceReceipt:
    return ResearchEvidenceReceipt(
        schema_version="cmf.research_evidence_receipt.v1",
        research_evidence_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=research_field_id,
        evidence_ids=evidence_ids,
        citation_hashes=[citation_hash(item) for item in citations],
        freshness_policy=freshness_policy,
        validator_actor_id=validator_actor_id,
        decision_code=decision_code,
        written_at=utc_now(),
    )
