"""Command spine contracts for CMF STUDIO.

Implements TS-CMF-001 source-of-truth command, actor, validation, and result
schemas. TypeScript consumers may be generated from these contracts, but the
Python/Pydantic contracts remain authoritative.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ActorType(str, Enum):
    human = "human"
    pi = "pi"
    dspy_program = "dspy_program"
    provider_webhook = "provider_webhook"
    workflow = "workflow"
    recovery_job = "recovery_job"


class CommandStatus(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    succeeded = "succeeded"
    failed = "failed"
    replayed = "replayed"
    quarantined = "quarantined"


class ActorContext(BaseModel):
    actor_id: UUID
    actor_type: ActorType
    role_ids: list[str] = Field(default_factory=list)
    tool_name: str | None = None
    session_id: UUID | None = None


class CommandEnvelope(BaseModel):
    schema_version: Literal["cmf.command.v1"]
    command_id: UUID
    command_type: str = Field(min_length=1)
    organization_id: UUID
    brand_id: UUID
    actor: ActorContext
    idempotency_key: str = Field(min_length=1)
    correlation_id: UUID
    payload: dict[str, Any]
    requested_at: datetime
    source_surface: str = Field(min_length=1)

    @field_validator("requested_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("requested_at must be timezone-aware")
        return value


class ValidationResult(BaseModel):
    passed: bool
    code: str
    message: str
    evidence: dict[str, Any] = Field(default_factory=dict)


class CommandResult(BaseModel):
    command_id: UUID
    status: CommandStatus
    result_payload: dict[str, Any] = Field(default_factory=dict)
    validation_results: list[ValidationResult]
    domain_event_id: UUID | None = None
    audit_receipt_id: UUID | None = None

    @property
    def passed(self) -> bool:
        return self.status in {CommandStatus.succeeded, CommandStatus.replayed}


class SubmitCommand(BaseModel):
    envelope: CommandEnvelope


class ReplayCommand(BaseModel):
    organization_id: UUID
    brand_id: UUID
    idempotency_key: str = Field(min_length=1)


def new_command_envelope(
    *,
    command_type: str,
    organization_id: UUID,
    brand_id: UUID,
    actor: ActorContext,
    payload: dict[str, Any] | None = None,
    source_surface: str = "internal",
    idempotency_key: str | None = None,
) -> CommandEnvelope:
    """Convenience factory for tests, workflows, and internal callers."""

    return CommandEnvelope(
        schema_version="cmf.command.v1",
        command_id=uuid4(),
        command_type=command_type,
        organization_id=organization_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key=idempotency_key or str(uuid4()),
        correlation_id=uuid4(),
        payload=payload or {},
        requested_at=datetime.now(timezone.utc),
        source_surface=source_surface,
    )

