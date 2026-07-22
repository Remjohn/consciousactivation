"""Revision and reconstruction audit contracts for TS-CMF-040."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class RevisionDelta(BaseModel):
    schema_version: Literal["cmf.revision_delta.v1"] = "cmf.revision_delta.v1"
    field_path: str = Field(min_length=1)
    previous_value_hash: str = Field(min_length=1)
    new_value_hash: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class RevisionLineageRefs(BaseModel):
    schema_version: Literal["cmf.revision_lineage_refs.v1"]
    complete_editing_session_id: UUID
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    brand_context_version_id: UUID
    scene_spec_ids: list[UUID] = Field(default_factory=list)
    composition_job_ids: list[UUID] = Field(default_factory=list)
    provider_receipt_ids: list[UUID] = Field(default_factory=list)
    render_manifest_ids: list[UUID] = Field(default_factory=list)
    evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    approval_event_ids: list[UUID] = Field(default_factory=list)
    revision_receipt_ids: list[UUID] = Field(default_factory=list)


class RevisionRequest(BaseModel):
    schema_version: Literal["cmf.revision_request.v1"]
    revision_request_id: UUID
    complete_editing_session_id: UUID
    requested_by_user_id: UUID
    reason: str = Field(min_length=1)
    target_object_type: str = Field(min_length=1)
    target_object_id: UUID
    deltas: list[RevisionDelta] = Field(min_length=1)
    prior_version_id: UUID
    lineage_refs: RevisionLineageRefs
    evaluation_state: str = Field(min_length=1)
    created_at: datetime


class RevisionVersion(BaseModel):
    schema_version: Literal["cmf.revision_version.v1"]
    revision_version_id: UUID
    revision_request_id: UUID
    complete_editing_session_id: UUID
    target_object_type: str = Field(min_length=1)
    target_object_id: UUID
    prior_version_id: UUID
    version_hash: str = Field(min_length=1)
    lineage_refs: RevisionLineageRefs
    created_at: datetime


class RevisionChain(BaseModel):
    schema_version: Literal["cmf.revision_chain.v1"]
    revision_chain_id: UUID
    complete_editing_session_id: UUID
    target_object_type: str = Field(min_length=1)
    target_object_id: UUID
    version_ids: list[UUID] = Field(min_length=1)
    revision_request_ids: list[UUID] = Field(min_length=1)
    revision_receipt_ids: list[UUID] = Field(default_factory=list)
    updated_at: datetime


class FinalApprovalBinding(BaseModel):
    schema_version: Literal["cmf.final_approval_binding.v1"]
    final_approval_binding_id: UUID
    complete_editing_session_id: UUID
    final_version_id: UUID
    revision_chain_id: UUID
    prior_version_ids: list[UUID] = Field(default_factory=list)
    approved_by_actor_id: UUID
    human_decision_ref: str = Field(min_length=1)
    approved_at: datetime


class ReconstructionAuditView(BaseModel):
    schema_version: Literal["cmf.reconstruction_audit_view.v1"]
    complete_editing_session_id: UUID
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    brand_context_version_id: UUID
    scene_spec_versions: list[UUID] = Field(default_factory=list)
    composition_job_ids: list[UUID] = Field(default_factory=list)
    provider_job_ids: list[UUID] = Field(default_factory=list)
    render_manifest_ids: list[UUID] = Field(default_factory=list)
    evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    approval_event_ids: list[UUID] = Field(default_factory=list)
    revision_receipt_ids: list[UUID] = Field(default_factory=list)


class RevisionReceipt(BaseModel):
    schema_version: Literal["cmf.revision_receipt.v1"]
    revision_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    complete_editing_session_id: UUID | None = None
    revision_request_id: UUID | None = None
    prior_version_id: UUID | None = None
    new_version_id: UUID | None = None
    target_object_type: str | None = None
    target_object_id: UUID | None = None
    deltas: list[RevisionDelta] = Field(default_factory=list)
    lineage_refs: RevisionLineageRefs | None = None
    evaluation_state: str | None = None
    actor_id: UUID
    approval_binding_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    command_id: UUID | None = None
    written_at: datetime


def revision_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_revision_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    complete_editing_session_id: UUID | None = None,
    revision_request_id: UUID | None = None,
    prior_version_id: UUID | None = None,
    new_version_id: UUID | None = None,
    target_object_type: str | None = None,
    target_object_id: UUID | None = None,
    deltas: list[RevisionDelta] | None = None,
    lineage_refs: RevisionLineageRefs | None = None,
    evaluation_state: str | None = None,
    approval_binding_id: UUID | None = None,
    command_id: UUID | None = None,
) -> RevisionReceipt:
    return RevisionReceipt(
        schema_version="cmf.revision_receipt.v1",
        revision_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        complete_editing_session_id=complete_editing_session_id,
        revision_request_id=revision_request_id,
        prior_version_id=prior_version_id,
        new_version_id=new_version_id,
        target_object_type=target_object_type,
        target_object_id=target_object_id,
        deltas=deltas or [],
        lineage_refs=lineage_refs,
        evaluation_state=evaluation_state,
        actor_id=actor_id,
        approval_binding_id=approval_binding_id,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        command_id=command_id,
        written_at=utc_now(),
    )
