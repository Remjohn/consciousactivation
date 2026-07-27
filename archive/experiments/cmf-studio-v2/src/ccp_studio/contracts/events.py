"""Domain event contracts for CMF STUDIO."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEventEnvelope(BaseModel):
    schema_version: Literal["cmf.domain_event.v1"]
    event_id: UUID
    event_type: str = Field(min_length=1)
    organization_id: UUID
    brand_id: UUID
    command_id: UUID
    correlation_id: UUID
    aggregate_type: str = Field(min_length=1)
    aggregate_id: UUID
    payload: dict[str, Any]
    occurred_at: datetime


def new_domain_event(
    *,
    event_type: str,
    organization_id: UUID,
    brand_id: UUID,
    command_id: UUID,
    correlation_id: UUID,
    aggregate_type: str,
    aggregate_id: UUID,
    payload: dict[str, Any] | None = None,
) -> DomainEventEnvelope:
    return DomainEventEnvelope(
        schema_version="cmf.domain_event.v1",
        event_id=uuid4(),
        event_type=event_type,
        organization_id=organization_id,
        brand_id=brand_id,
        command_id=command_id,
        correlation_id=correlation_id,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        payload=payload or {},
        occurred_at=datetime.now(timezone.utc),
    )

