"""Greenfield gate contracts for TS-CMF-016."""

from __future__ import annotations

import hashlib
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class GateViolationType(str, Enum):
    legacy_import = "legacy_import"
    hidden_prompt = "hidden_prompt"
    registry_conflict = "registry_conflict"
    provider_template_hash = "provider_template_hash"
    runtime_boundary = "runtime_boundary"


class GateStatus(str, Enum):
    approved = "approved"
    blocked = "blocked"
    revision_required = "revision_required"


class GateReceipt(BaseModel):
    schema_version: Literal["cmf.gate_receipt.v1"]
    gate_receipt_id: UUID
    violation_type: GateViolationType
    status: GateStatus
    object_ref: str
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
    repair_target: str | None = None
    written_at: datetime


class ProviderTemplateApproval(BaseModel):
    schema_version: Literal["cmf.provider_template_approval.v1"]
    provider_template_approval_id: UUID
    template_key: str
    content_hash: str
    compatibility_notes: str
    required_inputs: list[str]
    output_contract: str
    known_defects: list[str] = Field(default_factory=list)
    evaluation_target_id: UUID
    approved_by_actor_id: UUID


class RuntimeBoundaryFinding(BaseModel):
    schema_version: Literal["cmf.runtime_boundary_finding.v1"]
    runtime_boundary_finding_id: UUID
    object_ref: str
    finding_code: Literal["RUNTIME_BOUNDARY_DRIFT"]
    message: str
    evidence_refs: list[str] = Field(default_factory=list)


def template_hash(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def new_gate_receipt(
    *,
    violation_type: GateViolationType,
    status: GateStatus,
    object_ref: str,
    decision_code: str,
    evidence_refs: list[str] | None = None,
    repair_target: str | None = None,
) -> GateReceipt:
    return GateReceipt(
        schema_version="cmf.gate_receipt.v1",
        gate_receipt_id=uuid4(),
        violation_type=violation_type,
        status=status,
        object_ref=object_ref,
        decision_code=decision_code,
        evidence_refs=evidence_refs or [],
        repair_target=repair_target,
        written_at=utc_now(),
    )
