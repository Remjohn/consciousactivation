"""Versioned consent contracts for TS-CMF-008."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ConsentVersionStatus(str, Enum):
    active = "active"
    narrowed = "narrowed"
    expired = "expired"
    revoked = "revoked"


class ConsentScope(BaseModel):
    recording_allowed: bool
    source_storage_allowed: bool
    likeness_use_allowed: bool
    derivative_generation_allowed: bool
    provider_processing_allowed: bool
    synthetic_voice_eligible: bool
    reuse_allowed: bool
    retention_allowed: bool
    publication_allowed: bool


class ConsentRecordVersion(BaseModel):
    schema_version: Literal["cmf.consent_record_version.v1"]
    consent_record_version_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    version_number: int = Field(ge=1)
    status: ConsentVersionStatus
    scope: ConsentScope
    effective_at: datetime
    expires_at: datetime | None = None
    replaces_version_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    created_by_actor_id: UUID
    created_at: datetime


class ConsentCompatibilityResult(BaseModel):
    schema_version: Literal["cmf.consent_compatibility_result.v1"]
    consent_record_version_id: UUID | None = None
    command_type: str
    allowed: bool
    blocked_scope: str | None = None
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)


class ConsentReceipt(BaseModel):
    schema_version: Literal["cmf.consent_receipt.v1"]
    consent_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    consent_record_version_id: UUID
    action: str
    decision_code: str
    command_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    storage_path: str
    written_at: datetime


class PendingWorkItem(BaseModel):
    pending_work_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    work_type: str
    status: str
    source_ref: str


class ConsentChangeImpact(BaseModel):
    schema_version: Literal["cmf.consent_change_impact.v1"]
    impact_id: UUID
    consent_record_version_id: UUID
    affected_pending_work_ids: list[UUID] = Field(default_factory=list)
    quarantine_required: bool
    review_required: bool
    created_at: datetime


class ConsentReviewView(BaseModel):
    schema_version: Literal["cmf.consent_review_view.v1"]
    active_version: ConsentRecordVersion
    compatibility: ConsentCompatibilityResult
    source_evidence_refs: list[str]
    revocation_risk: str


def new_consent_version(
    *,
    organization_id: UUID,
    brand_id: UUID,
    guest_or_client_id: UUID,
    version_number: int,
    status: ConsentVersionStatus,
    scope: ConsentScope,
    created_by_actor_id: UUID,
    evidence_refs: list[str],
    replaces_version_id: UUID | None = None,
    expires_at: datetime | None = None,
) -> ConsentRecordVersion:
    now = utc_now()
    return ConsentRecordVersion(
        schema_version="cmf.consent_record_version.v1",
        consent_record_version_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        guest_or_client_id=guest_or_client_id,
        version_number=version_number,
        status=status,
        scope=scope,
        effective_at=now,
        expires_at=expires_at,
        replaces_version_id=replaces_version_id,
        evidence_refs=evidence_refs,
        created_by_actor_id=created_by_actor_id,
        created_at=now,
    )
