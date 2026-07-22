"""Cross-workflow consent blocker contracts for TS-CMF-010."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ConsentRepairAction(str, Enum):
    quarantine = "quarantine"
    request_updated_consent = "request_updated_consent"
    remove_likeness = "remove_likeness"
    remove_claim = "remove_claim"
    human_review = "human_review"


class ConsentSensitiveCommand(BaseModel):
    schema_version: Literal["cmf.consent_sensitive_command.v1"]
    command_type: str
    required_scopes: list[str] = Field(min_length=1)
    applies_to_stages: list[str] = Field(min_length=1)
    external_side_effect: bool = False


class ConsentGuardDecision(BaseModel):
    schema_version: Literal["cmf.consent_guard_decision.v1"]
    command_type: str
    allowed: bool
    decision_code: str
    consent_record_version_id: UUID | None = None
    blocked_scope: str | None = None
    repair_actions: list[ConsentRepairAction] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_receipt_id: UUID | None = None
    affected_pending_work_ids: list[UUID] = Field(default_factory=list)


class ConsentBlockerReceipt(BaseModel):
    schema_version: Literal["cmf.consent_blocker_receipt.v1"]
    consent_blocker_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    command_id: UUID
    object_type: str
    object_id: UUID
    consent_record_version_id: UUID | None
    blocked_scope: str
    decision_code: str
    repair_actions: list[ConsentRepairAction]
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


class AffectedPendingWork(BaseModel):
    schema_version: Literal["cmf.affected_pending_work.v1"]
    affected_pending_work_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    command_id: UUID
    object_type: str
    object_id: UUID
    pending_work_ids: list[UUID] = Field(default_factory=list)
    status: Literal["flagged_for_consent_review"]
    reason_code: str
    written_at: datetime


def new_consent_sensitive_command(
    *,
    command_type: str,
    required_scopes: list[str],
    applies_to_stages: list[str],
    external_side_effect: bool = False,
) -> ConsentSensitiveCommand:
    return ConsentSensitiveCommand(
        schema_version="cmf.consent_sensitive_command.v1",
        command_type=command_type,
        required_scopes=required_scopes,
        applies_to_stages=applies_to_stages,
        external_side_effect=external_side_effect,
    )


def new_consent_blocker_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    command_id: UUID,
    object_type: str,
    object_id: UUID,
    consent_record_version_id: UUID | None,
    blocked_scope: str,
    decision_code: str,
    repair_actions: list[ConsentRepairAction],
    evidence_refs: list[str],
) -> ConsentBlockerReceipt:
    return ConsentBlockerReceipt(
        schema_version="cmf.consent_blocker_receipt.v1",
        consent_blocker_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        command_id=command_id,
        object_type=object_type,
        object_id=object_id,
        consent_record_version_id=consent_record_version_id,
        blocked_scope=blocked_scope,
        decision_code=decision_code,
        repair_actions=repair_actions,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )


def new_affected_pending_work(
    *,
    organization_id: UUID,
    brand_id: UUID,
    guest_or_client_id: UUID,
    command_id: UUID,
    object_type: str,
    object_id: UUID,
    pending_work_ids: list[UUID],
    reason_code: str,
) -> AffectedPendingWork:
    return AffectedPendingWork(
        schema_version="cmf.affected_pending_work.v1",
        affected_pending_work_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        guest_or_client_id=guest_or_client_id,
        command_id=command_id,
        object_type=object_type,
        object_id=object_id,
        pending_work_ids=pending_work_ids,
        status="flagged_for_consent_review",
        reason_code=reason_code,
        written_at=utc_now(),
    )
