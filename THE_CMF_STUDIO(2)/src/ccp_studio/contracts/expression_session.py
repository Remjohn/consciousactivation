"""Complete Expression Session contracts for TS-CMF-029."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.source import RecordingConfiguration


class ExpressionSessionStatus(str, Enum):
    draft = "draft"
    ready_for_recording = "ready_for_recording"
    in_progress = "in_progress"
    paused = "paused"
    ingestion_pending = "ingestion_pending"
    extraction_pending = "extraction_pending"
    closed = "closed"
    failed = "failed"


class RecordingConfigurationRef(BaseModel):
    schema_version: Literal["cmf.recording_configuration_ref.v1"]
    recording_configuration_id: UUID
    session_mode: str = Field(min_length=1)
    master_recording_source: str = Field(min_length=1)
    backup_recording_source: str | None = None
    orientation: str = Field(min_length=1)
    quality_gate_required: bool = True
    source_configuration_id: UUID


class SessionQualityGateRef(BaseModel):
    schema_version: Literal["cmf.session_quality_gate_ref.v1"]
    pre_session_quality_gate_id: UUID
    gate_version: str = Field(min_length=1)
    required_checks: list[str] = Field(min_length=1)
    passed: bool


class CompleteExpressionSession(BaseModel):
    schema_version: Literal["cmf.complete_expression_session.v1"]
    expression_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID
    operator_id: UUID
    conversation_language: str = Field(min_length=1)
    system_label_language: str = "en"
    interview_deck_id: UUID
    interview_asset_contract_ids: list[UUID] = Field(min_length=1)
    consent_record_version_id: UUID
    recording_configuration: RecordingConfigurationRef
    pre_session_quality_gate: SessionQualityGateRef
    status: ExpressionSessionStatus
    created_at: datetime
    started_at: datetime | None = None
    updated_at: datetime


class ExpressionSessionStatusEvent(BaseModel):
    schema_version: Literal["cmf.expression_session_status_event.v1"]
    status_event_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    from_status: ExpressionSessionStatus | None = None
    to_status: ExpressionSessionStatus
    reason: str = Field(min_length=1)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


class SessionStartReceipt(BaseModel):
    schema_version: Literal["cmf.session_start_receipt.v1"]
    session_start_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    guest_id: UUID
    operator_id: UUID
    consent_record_version_id: UUID
    interview_deck_id: UUID
    interview_asset_contract_ids: list[UUID] = Field(min_length=1)
    recording_configuration_id: UUID
    pre_session_quality_gate_id: UUID
    status: ExpressionSessionStatus
    decision_code: str = Field(min_length=1)
    missing_requirements: list[str] = Field(default_factory=list)
    command_id: UUID | None = None
    reviewer_actor_id: UUID | None = None
    written_at: datetime


def recording_ref_from_configuration(
    configuration: RecordingConfiguration,
    *,
    session_mode: str,
    orientation: str,
    quality_gate_required: bool = True,
) -> RecordingConfigurationRef:
    return RecordingConfigurationRef(
        schema_version="cmf.recording_configuration_ref.v1",
        recording_configuration_id=configuration.recording_configuration_id,
        session_mode=session_mode,
        master_recording_source=configuration.expected_master_source,
        backup_recording_source=configuration.backup_route,
        orientation=orientation,
        quality_gate_required=quality_gate_required,
        source_configuration_id=configuration.recording_configuration_id,
    )


def new_session_status_event(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_session_id: UUID,
    from_status: ExpressionSessionStatus | None,
    to_status: ExpressionSessionStatus,
    reason: str,
    actor_id: UUID,
    command_id: UUID | None = None,
) -> ExpressionSessionStatusEvent:
    return ExpressionSessionStatusEvent(
        schema_version="cmf.expression_session_status_event.v1",
        status_event_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        from_status=from_status,
        to_status=to_status,
        reason=reason,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )


def new_session_start_receipt(
    *,
    session: CompleteExpressionSession,
    decision_code: str,
    status: ExpressionSessionStatus | None = None,
    missing_requirements: list[str] | None = None,
    command_id: UUID | None = None,
    reviewer_actor_id: UUID | None = None,
) -> SessionStartReceipt:
    return SessionStartReceipt(
        schema_version="cmf.session_start_receipt.v1",
        session_start_receipt_id=uuid4(),
        organization_id=session.organization_id,
        brand_id=session.brand_id,
        expression_session_id=session.expression_session_id,
        guest_id=session.guest_id,
        operator_id=session.operator_id,
        consent_record_version_id=session.consent_record_version_id,
        interview_deck_id=session.interview_deck_id,
        interview_asset_contract_ids=session.interview_asset_contract_ids,
        recording_configuration_id=session.recording_configuration.recording_configuration_id,
        pre_session_quality_gate_id=session.pre_session_quality_gate.pre_session_quality_gate_id,
        status=status or session.status,
        decision_code=decision_code,
        missing_requirements=missing_requirements or [],
        command_id=command_id,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
