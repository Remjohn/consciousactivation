"""Memory governance contracts for TS-CMF-057."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class MemoryGovernanceActionType(str, Enum):
    correct = "correct"
    reverse = "reverse"
    expire = "expire"
    quarantine = "quarantine"
    release_from_quarantine = "release_from_quarantine"


class MemoryGovernanceStatus(str, Enum):
    active = "active"
    corrected = "corrected"
    reversed = "reversed"
    expired = "expired"
    quarantined = "quarantined"


class MemoryUsagePolicy(str, Enum):
    allowed = "allowed"
    blocked = "blocked"


class MemoryGovernanceAction(BaseModel):
    schema_version: Literal["cmf.memory_governance_action.v1"]
    action_id: UUID
    memory_event_id: UUID
    action_type: MemoryGovernanceActionType
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    requested_by_user_id: UUID
    corrected_statement: str | None = None
    created_at: datetime


class MemoryGovernanceEvent(BaseModel):
    schema_version: Literal["cmf.memory_governance_event.v1"]
    event_id: UUID
    action_id: UUID
    memory_event_id: UUID
    resulting_status: MemoryGovernanceStatus
    superseding_memory_event_id: UUID | None = None
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    created_at: datetime


class MemoryReviewState(BaseModel):
    schema_version: Literal["cmf.memory_review_state.v1"]
    memory_event_id: UUID
    evidence_refs: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    route_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    consent_compatible: bool
    created_event_id: UUID
    downstream_usage_refs: list[str] = Field(default_factory=list)
    governance_status: MemoryGovernanceStatus
    superseding_memory_event_id: UUID | None = None
    governance_history: list[MemoryGovernanceEvent] = Field(default_factory=list)


class MemoryUsagePolicyDecision(BaseModel):
    schema_version: Literal["cmf.memory_usage_policy_decision.v1"]
    memory_event_id: UUID
    policy: MemoryUsagePolicy
    governance_status: MemoryGovernanceStatus
    active_memory_event_id: UUID | None = None
    reason: str = Field(min_length=1)
    checked_at: datetime


class MemoryProjectionUpdateEvent(BaseModel):
    schema_version: Literal["cmf.memory_projection_update_event.v1"]
    projection_event_id: UUID
    memory_event_id: UUID
    governance_event_id: UUID
    resulting_status: MemoryGovernanceStatus
    rebuild_required: bool = True
    created_at: datetime


class MemoryGovernanceReceipt(BaseModel):
    schema_version: Literal["cmf.memory_governance_receipt.v1"]
    memory_governance_receipt_id: UUID
    action_id: UUID
    memory_event_id: UUID
    superseding_memory_event_id: UUID | None = None
    action_type: MemoryGovernanceActionType
    reason: str = Field(min_length=1)
    actor_id: UUID
    evidence_refs: list[str] = Field(min_length=1)
    prior_status: MemoryGovernanceStatus
    resulting_status: MemoryGovernanceStatus
    downstream_usage_effect: str = Field(min_length=1)
    projection_event_id: UUID | None = None
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class MemoryGovernanceDomainEvent(BaseModel):
    schema_version: Literal["cmf.memory_governance_domain_event.v1"]
    memory_governance_domain_event_id: UUID
    event_type: str = Field(min_length=1)
    memory_event_id: UUID | None = None
    governance_event_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def memory_governance_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_memory_governance_action(
    *,
    memory_event_id: UUID,
    action_type: MemoryGovernanceActionType,
    reason: str,
    evidence_refs: list[str],
    requested_by_user_id: UUID,
    corrected_statement: str | None = None,
) -> MemoryGovernanceAction:
    return MemoryGovernanceAction(
        schema_version="cmf.memory_governance_action.v1",
        action_id=uuid4(),
        memory_event_id=memory_event_id,
        action_type=action_type,
        reason=reason,
        evidence_refs=evidence_refs,
        requested_by_user_id=requested_by_user_id,
        corrected_statement=corrected_statement,
        created_at=utc_now(),
    )


def new_memory_governance_receipt(
    *,
    action: MemoryGovernanceAction,
    prior_status: MemoryGovernanceStatus,
    resulting_status: MemoryGovernanceStatus,
    downstream_usage_effect: str,
    superseding_memory_event_id: UUID | None = None,
    projection_event_id: UUID | None = None,
) -> MemoryGovernanceReceipt:
    payload = {
        "action_id": action.action_id,
        "memory_event_id": action.memory_event_id,
        "superseding_memory_event_id": superseding_memory_event_id,
        "action_type": action.action_type.value,
        "reason": action.reason,
        "actor_id": action.requested_by_user_id,
        "evidence_refs": action.evidence_refs,
        "prior_status": prior_status.value,
        "resulting_status": resulting_status.value,
        "downstream_usage_effect": downstream_usage_effect,
        "projection_event_id": projection_event_id,
    }
    return MemoryGovernanceReceipt(
        schema_version="cmf.memory_governance_receipt.v1",
        memory_governance_receipt_id=uuid4(),
        action_id=action.action_id,
        memory_event_id=action.memory_event_id,
        superseding_memory_event_id=superseding_memory_event_id,
        action_type=action.action_type,
        reason=action.reason,
        actor_id=action.requested_by_user_id,
        evidence_refs=action.evidence_refs,
        prior_status=prior_status,
        resulting_status=resulting_status,
        downstream_usage_effect=downstream_usage_effect,
        projection_event_id=projection_event_id,
        receipt_hash=memory_governance_hash(payload),
        written_at=utc_now(),
    )
