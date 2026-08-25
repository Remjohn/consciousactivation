"""Pydantic v2 typed data models for CA-IMPL-01A Tenant Foundation & Staging Containment.

Governed by TS-CAE-TEN-001, CA-CAN-01A/B/C object constitutions, and FR-CAE-TEN-001 through FR-CAE-TEN-015.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================================
# 1. Workspace & Tenancy Root (FR-CAE-TEN-001 / CA-ENT-001)
# ============================================================================


class WorkspaceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class WorkspaceModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    workspace_id: UUID = Field(default_factory=uuid4)
    slug: str = Field(..., pattern=r"^[a-z0-9-]+$", min_length=2, max_length=64)
    display_name: str = Field(..., min_length=1, max_length=255)
    status: WorkspaceStatus = Field(default=WorkspaceStatus.ACTIVE)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 2. Workspace Membership (FR-CAE-TEN-003 / CA-REL-001)
# ============================================================================


class MembershipRole(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    OBSERVER = "OBSERVER"
    SYSTEM_AGENT = "SYSTEM_AGENT"


class MembershipStatus(str, Enum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"


class WorkspaceMembershipModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    membership_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    actor_id: str = Field(..., min_length=1, max_length=128)
    role: MembershipRole = Field(default=MembershipRole.MEMBER)
    status: MembershipStatus = Field(default=MembershipStatus.ACTIVE)
    created_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 3. Operator Governance Root (FR-CAE-TEN-002 / CA-CAN-01A)
# ============================================================================


class OperatorOrgStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class OperatorOrganizationModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    operator_org_id: UUID = Field(default_factory=uuid4)
    org_name: str = Field(..., min_length=1, max_length=255)
    status: OperatorOrgStatus = Field(default=OperatorOrgStatus.ACTIVE)
    created_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 4. Operator Access Grant (FR-CAE-TEN-004, FR-CAE-TEN-005 / CA-REL-002)
# ============================================================================


class OperatorAccessGrantModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    grant_id: UUID = Field(default_factory=uuid4)
    operator_org_id: UUID
    operator_actor_id: str = Field(..., min_length=1, max_length=128)
    workspace_id: UUID
    justification: str = Field(..., min_length=10)
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("expires_at")
    @classmethod
    def validate_expiry(cls, value: datetime) -> datetime:
        return value

    @property
    def is_active(self) -> bool:
        now = _utc_now()
        if self.revoked_at is not None:
            return False
        return self.expires_at > now


# ============================================================================
# 5. Engagement Project Envelope (FR-CAE-TEN-006 / CA-ENT-004)
# ============================================================================


class EngagementLifecycleState(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class EngagementModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    engagement_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    lifecycle_state: EngagementLifecycleState = Field(default=EngagementLifecycleState.PLANNED)
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 6. Guest - Workspace Local Participant (FR-CAE-TEN-007 / CA-ENT-003)
# ============================================================================


class ConsentStatus(str, Enum):
    PENDING = "PENDING"
    GRANTED = "GRANTED"
    REVOKED = "REVOKED"


class GuestModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    guest_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    external_reference_id: Optional[str] = Field(default=None, max_length=128)
    pseudonym: str = Field(..., min_length=1, max_length=128)
    consent_status: ConsentStatus = Field(default=ConsentStatus.PENDING)
    created_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 7. Media Asset Verification Metadata (FR-CAE-TEN-010, FR-CAE-TEN-011 / CA-ENT-002)
# ============================================================================


class MediaAssetLifecycleState(str, Enum):
    REGISTERED = "REGISTERED"
    STAGED = "STAGED"
    VERIFIED = "VERIFIED"
    QUARANTINED = "QUARANTINED"
    REVOKED = "REVOKED"


class MediaAssetModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    media_asset_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    engagement_id: Optional[UUID] = None
    storage_path: str = Field(..., min_length=5)
    canonical_sha256: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    byte_size: int = Field(..., ge=0)
    mime_type: str = Field(..., min_length=3, max_length=128)
    lifecycle_state: MediaAssetLifecycleState = Field(default=MediaAssetLifecycleState.REGISTERED)
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 8. Harness Template - Canonical Plane Grammar (FR-CAE-TEN-012 / CA-STR-001)
# ============================================================================


class HarnessTemplateModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    template_id: str = Field(..., min_length=2, max_length=64)
    version: str = Field(..., min_length=1, max_length=32)
    definition_yaml: str = Field(..., min_length=10)
    definition_sha256: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 9. Harness Run Operational Instance (FR-CAE-TEN-013 / CA-EXE-001)
# ============================================================================


class HarnessRunLifecycleState(str, Enum):
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class HarnessRunModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    run_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    engagement_id: UUID
    template_id: str = Field(..., min_length=2, max_length=64)
    template_version: str = Field(..., min_length=1, max_length=32)
    current_step: str = Field(..., min_length=1, max_length=64)
    lifecycle_state: HarnessRunLifecycleState = Field(default=HarnessRunLifecycleState.INITIALIZED)
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


# ============================================================================
# 10. Receipt & Reality Contact Ledger (FR-CAE-TEN-014, FR-CAE-TEN-015 / CA-REC-001)
# ============================================================================


class ReceiptModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    receipt_id: str = Field(..., min_length=5, max_length=128)
    workspace_id: UUID
    operation_id: str = Field(..., min_length=3, max_length=128)
    idempotency_key: str = Field(..., min_length=1, max_length=128)
    actor_id: str = Field(..., min_length=1, max_length=128)
    canonical_payload: str = Field(..., min_length=2)
    payload_jsonb: dict[str, Any]
    payload_sha256: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    created_at: datetime = Field(default_factory=_utc_now)


class ReceiptEvidenceLinkModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    link_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    receipt_id: str = Field(..., min_length=5, max_length=128)
    evidence_item_id: UUID
    created_at: datetime = Field(default_factory=_utc_now)
