"""Audit receipt contracts for CMF STUDIO."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.commands import CommandStatus, ValidationResult


class AuditReceipt(BaseModel):
    schema_version: Literal["cmf.audit_receipt.v1"]
    receipt_id: UUID
    command_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    action: str = Field(min_length=1)
    status: CommandStatus
    policy_checks: list[ValidationResult]
    event_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def new_audit_receipt(
    *,
    command_id: UUID,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    action: str,
    status: CommandStatus,
    policy_checks: list[ValidationResult],
    event_id: UUID | None = None,
    evidence_refs: list[str] | None = None,
) -> AuditReceipt:
    return AuditReceipt(
        schema_version="cmf.audit_receipt.v1",
        receipt_id=uuid4(),
        command_id=command_id,
        organization_id=organization_id,
        brand_id=brand_id,
        actor_id=actor_id,
        action=action,
        status=status,
        policy_checks=policy_checks,
        event_id=event_id,
        evidence_refs=evidence_refs or [],
        written_at=datetime.now(timezone.utc),
    )

