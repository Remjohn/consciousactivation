"""PWA and Telegram surface parity contracts for TS-CMF-007."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class SurfaceKey(str, Enum):
    pwa = "pwa"
    telegram_bot = "telegram_bot"
    telegram_mini_app = "telegram_mini_app"


class ObjectStateSnapshot(BaseModel):
    schema_version: Literal["cmf.object_state_snapshot.v1"]
    object_type: str = Field(min_length=1)
    object_id: UUID
    organization_id: UUID
    brand_id: UUID
    state: str = Field(min_length=1)
    state_version: str = Field(min_length=1)
    evidence_sufficient_for_surface: bool
    evidence_refs: list[str] = Field(default_factory=list)


class SurfaceActionEnvelope(BaseModel):
    schema_version: Literal["cmf.surface_action.v1"]
    surface_action_id: UUID
    source_surface: SurfaceKey
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    command_type: str = Field(min_length=1)
    idempotency_key: str = Field(min_length=1)
    object_snapshot: ObjectStateSnapshot
    payload: dict[str, Any]
    requested_at: datetime


class TelegramActionPayload(BaseModel):
    schema_version: Literal["cmf.telegram_action_payload.v1"]
    init_data: str
    callback_data: str
    message_id: str | None = None


class PWAActionPayload(BaseModel):
    schema_version: Literal["cmf.pwa_action_payload.v1"]
    route: str
    browser_session_id: str | None = None


class DeepLinkTarget(BaseModel):
    schema_version: Literal["cmf.deep_link_target.v1"]
    target_surface: Literal["pwa"]
    route: str
    object_type: str
    object_id: UUID
    brand_id: UUID
    required_reason: str


class SurfaceCommandResult(BaseModel):
    schema_version: Literal["cmf.surface_command_result.v1"]
    surface_action_id: UUID
    command_id: UUID | None = None
    accepted: bool
    result_code: str
    message: str
    deep_link: DeepLinkTarget | None = None
    latest_state: ObjectStateSnapshot | None = None
    receipt_id: UUID | None = None


class NotificationIntent(BaseModel):
    schema_version: Literal["cmf.notification_intent.v1"]
    notification_intent_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_snapshot: ObjectStateSnapshot
    target_surface: SurfaceKey
    message_key: str = Field(min_length=1)
    deep_link: DeepLinkTarget | None = None
    created_at: datetime


def new_surface_action(
    *,
    source_surface: SurfaceKey,
    actor_id: UUID,
    organization_id: UUID,
    brand_id: UUID,
    command_type: str,
    idempotency_key: str,
    object_snapshot: ObjectStateSnapshot,
    payload: dict[str, Any] | None = None,
) -> SurfaceActionEnvelope:
    return SurfaceActionEnvelope(
        schema_version="cmf.surface_action.v1",
        surface_action_id=uuid4(),
        source_surface=source_surface,
        actor_id=actor_id,
        organization_id=organization_id,
        brand_id=brand_id,
        command_type=command_type,
        idempotency_key=idempotency_key,
        object_snapshot=object_snapshot,
        payload=payload or {},
        requested_at=utc_now(),
    )
