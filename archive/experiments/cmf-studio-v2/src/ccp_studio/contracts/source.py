"""Recording and source artifact contracts for TS-CMF-009."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class SourceArtifactKind(str, Enum):
    master_recording = "master_recording"
    backup_recording = "backup_recording"
    platform_recording = "platform_recording"
    uploaded_reference = "uploaded_reference"


class SourceQualityStatus(str, Enum):
    accepted = "accepted"
    blocked = "blocked"
    exception_required = "exception_required"
    review_required = "review_required"


class RecordingConfiguration(BaseModel):
    schema_version: Literal["cmf.recording_configuration.v1"]
    recording_configuration_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    expected_master_source: str = Field(min_length=1)
    backup_route: str = Field(min_length=1)
    platform_source: str | None = None
    upload_method: str = Field(min_length=1)
    file_safety_expectations: list[str] = Field(default_factory=list)
    quality_requirements: list[str] = Field(min_length=1)
    created_at: datetime


class RecordingArtifact(BaseModel):
    schema_version: Literal["cmf.recording_artifact.v1"]
    recording_artifact_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    kind: SourceArtifactKind
    filename: str = Field(min_length=1)
    mime_type: str = Field(min_length=1)
    size_bytes: int = Field(ge=1)
    provenance: str = Field(min_length=1)
    uploaded_at: datetime


class SourceArtifact(BaseModel):
    schema_version: Literal["cmf.source_artifact.v1"]
    source_artifact_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    kind: SourceArtifactKind
    filename: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    retention_policy_id: UUID
    provenance: str = Field(min_length=1)
    immutable_uri: str
    accepted_at: datetime | None = None


class SourceQualityReport(BaseModel):
    schema_version: Literal["cmf.source_quality_report.v1"]
    source_quality_report_id: UUID
    source_artifact_id: UUID | None = None
    status: SourceQualityStatus
    failure_category: str | None = None
    recovery_action: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class SourceArtifactManifest(BaseModel):
    schema_version: Literal["cmf.source_artifact_manifest.v1"]
    source_artifact_manifest_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    source_artifact_ids: list[UUID] = Field(min_length=1)
    source_quality_report_ids: list[UUID] = Field(default_factory=list)
    created_at: datetime


class SourceIntakeReceipt(BaseModel):
    schema_version: Literal["cmf.source_intake_receipt.v1"]
    source_intake_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    decision_code: str
    source_artifact_id: UUID | None = None
    manifest_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def new_recording_configuration(
    *,
    organization_id: UUID,
    brand_id: UUID,
    session_id: UUID,
    expected_master_source: str,
    backup_route: str,
    platform_source: str | None,
    upload_method: str,
    file_safety_expectations: list[str],
    quality_requirements: list[str],
) -> RecordingConfiguration:
    return RecordingConfiguration(
        schema_version="cmf.recording_configuration.v1",
        recording_configuration_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        session_id=session_id,
        expected_master_source=expected_master_source,
        backup_route=backup_route,
        platform_source=platform_source,
        upload_method=upload_method,
        file_safety_expectations=file_safety_expectations,
        quality_requirements=quality_requirements,
        created_at=utc_now(),
    )
