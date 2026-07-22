"""Spec-governance contracts for TS-CMF-003."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class SpecAuditStatus(str, Enum):
    accepted = "accepted"
    revision_requested = "revision_requested"
    blocked = "blocked"


class TechSpecWorkflowStatus(str, Enum):
    opened = "opened"
    reading_sources = "reading_sources"
    tracing = "tracing"
    auditing = "auditing"
    accepted = "accepted"
    revision_requested = "revision_requested"
    blocked = "blocked"


class SourceFileRef(BaseModel):
    path: str = Field(min_length=1)
    required: bool
    source_role: str = Field(min_length=1)
    content_hash: str | None = None


class SpecWritingProtocol(BaseModel):
    schema_version: Literal["cmf.spec_writing_protocol.v1"]
    protocol_id: UUID
    protocol_name: str = Field(min_length=1)
    protocol_version: str = Field(min_length=1)
    preserved_legacy_sources: list[str] = Field(min_length=1)
    greenfield_replacements: list[str] = Field(min_length=1)
    required_sections: list[str] = Field(min_length=1)
    blocked_phrases: list[str] = Field(default_factory=list)


class TechSpecWorkflow(BaseModel):
    schema_version: Literal["cmf.tech_spec_workflow.v1"]
    workflow_id: UUID
    spec_id: str = Field(min_length=1)
    story_id: str = Field(min_length=1)
    story_path: str = Field(min_length=1)
    actor_id: UUID
    status: TechSpecWorkflowStatus
    opened_at: datetime
    updated_at: datetime


class TechSpecSourcePacket(BaseModel):
    schema_version: Literal["cmf.tech_spec_source_packet.v1"]
    source_packet_id: UUID
    workflow_id: UUID
    required_sources: list[SourceFileRef] = Field(min_length=1)
    feature_sources: list[SourceFileRef] = Field(default_factory=list)
    created_at: datetime


class FilesReadReceipt(BaseModel):
    schema_version: Literal["cmf.files_read_receipt.v1"]
    receipt_id: UUID
    workflow_id: UUID
    file_ref: SourceFileRef
    read_at: datetime
    reader_actor_id: UUID
    evidence_summary: str = Field(min_length=1)


class RequirementTrace(BaseModel):
    schema_version: Literal["cmf.requirement_trace.v1"]
    trace_id: UUID
    workflow_id: UUID
    fr_id: str = Field(min_length=1)
    story_id: str = Field(min_length=1)
    spec_sections: list[str] = Field(min_length=1)
    acceptance_criteria_refs: list[str] = Field(min_length=1)
    enforcement_mechanism: str = Field(min_length=1)


class PipelineStageTrace(BaseModel):
    schema_version: Literal["cmf.pipeline_stage_trace.v1"]
    trace_id: UUID
    workflow_id: UUID
    pipeline_stage: str = Field(min_length=1)
    entry_object: str = Field(min_length=1)
    exit_object: str = Field(min_length=1)
    allowed_actor_or_service: str = Field(min_length=1)
    validation_contract: str = Field(min_length=1)
    required_receipt: str = Field(min_length=1)


class CBARCheck(BaseModel):
    schema_version: Literal["cmf.cbar_check.v1"]
    cbar_check_id: UUID
    workflow_id: UUID
    primitive_tension: str = Field(min_length=1)
    failure_scenario: str = Field(min_length=1)
    resolution_demand: str = Field(min_length=1)
    downstream_proof: str = Field(min_length=1)
    test_or_receipt_refs: list[str] = Field(min_length=1)


class SpecAuditReceipt(BaseModel):
    schema_version: Literal["cmf.spec_audit_receipt.v1"]
    spec_audit_receipt_id: UUID
    workflow_id: UUID
    spec_id: str = Field(min_length=1)
    status: SpecAuditStatus
    files_read_receipt_ids: list[UUID] = Field(default_factory=list)
    requirement_trace_ids: list[UUID] = Field(default_factory=list)
    pipeline_trace_ids: list[UUID] = Field(default_factory=list)
    cbar_check_ids: list[UUID] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    written_at: datetime


def default_spec_writing_protocol() -> SpecWritingProtocol:
    return SpecWritingProtocol(
        schema_version="cmf.spec_writing_protocol.v1",
        protocol_id=uuid4(),
        protocol_name="CMF Python/DSPy/Pi BMad Spec Workflow",
        protocol_version="1.0",
        preserved_legacy_sources=[
            "ERA3_Tech_Spec_Writing_Protocol",
            "PROMPT_Spec_Audit",
            "PROMPT_Spec_Build",
            "CBAR_Constraint_Based_Adversarial_Reasoning",
        ],
        greenfield_replacements=[
            "Existing Backend Integration -> Greenfield Integration and Legacy Migration Context",
            "TypeScript authority -> Pydantic contract authority",
            "Legacy scripts -> typed policy, fixture, compiler prompt asset, or audit rule",
        ],
        required_sections=[
            "Files Read",
            "Requirement Trace",
            "Pipeline Stage Trace",
            "Greenfield Integration and Legacy Migration Context",
            "CBAR Constraint Pass",
            "Testing Strategy",
            "Spec Audit Receipt",
        ],
        blocked_phrases=[
            "TypeScript is the source of truth",
            "Existing Backend Integration",
            "direct legacy runtime import",
            "Neo4j is canonical",
            "bypass the Command Bus",
        ],
    )


def new_tech_spec_workflow(
    *,
    spec_id: str,
    story_id: str,
    story_path: str,
    actor_id: UUID,
) -> TechSpecWorkflow:
    now = utc_now()
    return TechSpecWorkflow(
        schema_version="cmf.tech_spec_workflow.v1",
        workflow_id=uuid4(),
        spec_id=spec_id,
        story_id=story_id,
        story_path=story_path,
        actor_id=actor_id,
        status=TechSpecWorkflowStatus.opened,
        opened_at=now,
        updated_at=now,
    )


def new_source_packet(
    *,
    workflow_id: UUID,
    required_sources: list[SourceFileRef],
    feature_sources: list[SourceFileRef] | None = None,
) -> TechSpecSourcePacket:
    return TechSpecSourcePacket(
        schema_version="cmf.tech_spec_source_packet.v1",
        source_packet_id=uuid4(),
        workflow_id=workflow_id,
        required_sources=required_sources,
        feature_sources=feature_sources or [],
        created_at=utc_now(),
    )
