"""Complete Editing Session contracts for TS-CMF-036."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class CompleteEditingSessionStatus(str, Enum):
    created = "created"
    scene_spec_pending = "scene_spec_pending"
    composition_pending = "composition_pending"
    render_pending = "render_pending"
    evaluation_pending = "evaluation_pending"
    revision_requested = "revision_requested"
    approved = "approved"
    rejected = "rejected"


class EditingSessionSourceBinding(BaseModel):
    schema_version: Literal["cmf.editing_session_source_binding.v1"]
    editing_session_source_binding_id: UUID
    complete_editing_session_id: UUID
    source_expression_session_id: UUID
    source_expression_moment_id: UUID
    source_refs: list[str] = Field(min_length=1)


class EditingSessionRouteBinding(BaseModel):
    schema_version: Literal["cmf.editing_session_route_binding.v1"]
    editing_session_route_binding_id: UUID
    complete_editing_session_id: UUID
    asset_route_receipt_id: UUID
    accepted_route_ids: list[UUID] = Field(min_length=1)
    registry_bundle_version: str = Field(min_length=1)
    registry_refs: list[str] = Field(min_length=1)


class EditingSessionBrandContextBinding(BaseModel):
    schema_version: Literal["cmf.editing_session_brand_context_binding.v1"]
    editing_session_brand_context_binding_id: UUID
    complete_editing_session_id: UUID
    brand_context_version_id: UUID
    brand_context_version_hash: str = Field(min_length=1)
    clearance_certificate_id: UUID | None = None


class CompleteEditingSession(BaseModel):
    schema_version: Literal["cmf.complete_editing_session.v1"]
    complete_editing_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    source_expression_session_id: UUID
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    asset_package_item_id: UUID | None = None
    brand_context_version_id: UUID
    brand_context_version_hash: str = Field(min_length=1)
    registry_bundle_version: str = Field(min_length=1)
    created_by_user_id: UUID
    status: CompleteEditingSessionStatus
    production_readiness: str = Field(min_length=1)
    created_at: datetime
    updated_at: datetime


class EditingSessionStatusEvent(BaseModel):
    schema_version: Literal["cmf.editing_session_status_event.v1"]
    editing_session_status_event_id: UUID
    complete_editing_session_id: UUID
    previous_status: CompleteEditingSessionStatus | None = None
    next_status: CompleteEditingSessionStatus
    reason: str = Field(min_length=1)
    actor_id: UUID
    occurred_at: datetime


class EditingSessionReceipt(BaseModel):
    schema_version: Literal["cmf.editing_session_receipt.v1"]
    editing_session_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    complete_editing_session_id: UUID | None = None
    source_expression_moment_id: UUID | None = None
    asset_route_receipt_id: UUID | None = None
    asset_package_item_id: UUID | None = None
    brand_context_version_id: UUID | None = None
    brand_context_version_hash: str | None = None
    registry_bundle_version: str | None = None
    actor_id: UUID
    command_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


class CompleteEditingSessionReadModel(BaseModel):
    schema_version: Literal["cmf.complete_editing_session_read_model.v1"]
    complete_editing_session_id: UUID
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    asset_package_item_id: UUID | None = None
    brand_context_version_id: UUID
    brand_context_version_hash: str
    registry_bundle_version: str
    status: CompleteEditingSessionStatus
    production_readiness: str
    source_refs: list[str]
    registry_refs: list[str]


def new_editing_session_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    complete_editing_session_id: UUID | None = None,
    source_expression_moment_id: UUID | None = None,
    asset_route_receipt_id: UUID | None = None,
    asset_package_item_id: UUID | None = None,
    brand_context_version_id: UUID | None = None,
    brand_context_version_hash: str | None = None,
    registry_bundle_version: str | None = None,
    command_id: UUID | None = None,
) -> EditingSessionReceipt:
    return EditingSessionReceipt(
        schema_version="cmf.editing_session_receipt.v1",
        editing_session_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        complete_editing_session_id=complete_editing_session_id,
        source_expression_moment_id=source_expression_moment_id,
        asset_route_receipt_id=asset_route_receipt_id,
        asset_package_item_id=asset_package_item_id,
        brand_context_version_id=brand_context_version_id,
        brand_context_version_hash=brand_context_version_hash,
        registry_bundle_version=registry_bundle_version,
        actor_id=actor_id,
        command_id=command_id,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
