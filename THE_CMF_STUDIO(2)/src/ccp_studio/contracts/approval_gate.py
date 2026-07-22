"""Approval gate contracts for TS-CMF-053."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ApprovalBlockerSeverity(str, Enum):
    hard = "hard"
    soft = "soft"
    escalate = "escalate"


class ApprovalGateDecision(str, Enum):
    approved_allowed = "approved_allowed"
    blocked = "blocked"
    escalate = "escalate"


class ApprovalGateBlocker(BaseModel):
    schema_version: Literal["cmf.approval_gate_blocker.v1"] = "cmf.approval_gate_blocker.v1"
    blocker_id: UUID
    code: str = Field(min_length=1)
    severity: ApprovalBlockerSeverity
    source_object_ref: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    message: str = Field(min_length=1)
    repair_hint: str = Field(min_length=1)


class ContentFormatValidation(BaseModel):
    schema_version: Literal["cmf.content_format_validation.v1"]
    platform_variant_id: str = Field(min_length=1)
    format_key: str = Field(min_length=1)
    valid_content_format: bool
    registry_version_id: str = Field(min_length=1)
    blocker_code: str | None = None


class ApprovalGateInput(BaseModel):
    schema_version: Literal["cmf.approval_gate_input.v1"]
    approval_request_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    object_version_hash: str = Field(min_length=1)
    lineage_refs: dict[str, str] = Field(default_factory=dict)
    required_lineage_keys: list[str] = Field(default_factory=lambda: [
        "complete_editing_session_id",
        "scene_spec_id",
        "provider_receipt_id",
        "render_output_ref",
        "archetype_route_receipt_id",
    ])
    consent_compatible: bool
    consent_blocker_codes: list[str] = Field(default_factory=list)
    source_truth_passed: bool
    disputed_source_refs: list[str] = Field(default_factory=list)
    identity_passed: bool
    identity_failure_refs: list[str] = Field(default_factory=list)
    evaluation_passed: bool
    evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    evaluation_hard_failure_codes: list[str] = Field(default_factory=list)
    platform_format_passed: bool
    platform_blocker_codes: list[str] = Field(default_factory=list)
    platform_variant_id: str = Field(min_length=1)
    content_format_key: str = Field(min_length=1)
    content_format_registry_version_id: str = Field(min_length=1)
    valid_content_formats: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


class ApprovalPolicyReport(BaseModel):
    schema_version: Literal["cmf.approval_policy_report.v1"]
    approval_policy_report_id: UUID
    approval_request_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    object_version_hash: str = Field(min_length=1)
    lineage_complete: bool
    consent_compatible: bool
    source_truth_passed: bool
    identity_passed: bool
    evaluation_passed: bool
    platform_format_passed: bool
    content_format_passed: bool
    content_format_validation: ContentFormatValidation
    blockers: list[ApprovalGateBlocker] = Field(default_factory=list)
    decision: ApprovalGateDecision
    policy_version: str = Field(min_length=1)
    created_at: datetime


class ApprovalBlockerReceipt(BaseModel):
    schema_version: Literal["cmf.approval_blocker_receipt.v1"]
    approval_blocker_receipt_id: UUID
    approval_policy_report_id: UUID
    approval_request_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    blocker_ids: list[UUID] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    policy_version: str = Field(min_length=1)
    content_format_validation: ContentFormatValidation
    decision: ApprovalGateDecision
    repair_hints: list[str] = Field(default_factory=list)
    cleared_blocker_ids: list[UUID] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class ApprovalGateDomainEvent(BaseModel):
    schema_version: Literal["cmf.approval_gate_domain_event.v1"]
    approval_gate_event_id: UUID
    event_type: str = Field(min_length=1)
    approval_request_id: UUID
    object_type: str
    object_id: UUID
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def approval_gate_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_approval_blocker_receipt(*, report: ApprovalPolicyReport) -> ApprovalBlockerReceipt:
    evidence_refs = sorted({ref for blocker in report.blockers for ref in blocker.evidence_refs})
    repair_hints = [blocker.repair_hint for blocker in report.blockers]
    payload = {
        "approval_policy_report_id": report.approval_policy_report_id,
        "approval_request_id": report.approval_request_id,
        "organization_id": report.organization_id,
        "brand_id": report.brand_id,
        "object_type": report.object_type,
        "object_id": report.object_id,
        "blocker_codes": [blocker.code for blocker in report.blockers],
        "decision": report.decision.value,
        "policy_version": report.policy_version,
        "content_format_validation": report.content_format_validation.model_dump(mode="json"),
    }
    return ApprovalBlockerReceipt(
        schema_version="cmf.approval_blocker_receipt.v1",
        approval_blocker_receipt_id=uuid4(),
        approval_policy_report_id=report.approval_policy_report_id,
        approval_request_id=report.approval_request_id,
        organization_id=report.organization_id,
        brand_id=report.brand_id,
        object_type=report.object_type,
        object_id=report.object_id,
        blocker_ids=[blocker.blocker_id for blocker in report.blockers],
        blocker_codes=[blocker.code for blocker in report.blockers],
        evidence_refs=evidence_refs,
        policy_version=report.policy_version,
        content_format_validation=report.content_format_validation,
        decision=report.decision,
        repair_hints=repair_hints,
        receipt_hash=approval_gate_hash(payload),
        written_at=utc_now(),
    )

