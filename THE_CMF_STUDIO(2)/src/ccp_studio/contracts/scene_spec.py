"""SceneSpec, Creative State, and Render Contract contracts for TS-CMF-037."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class CreativeStateStage(str, Enum):
    created = "created"
    scene_spec_validated = "scene_spec_validated"
    composition_requested = "composition_requested"
    render_contract_ready = "render_contract_ready"
    evaluated = "evaluated"


class AssetSourceKind(str, Enum):
    brand_context = "brand_context"
    source_artifact = "source_artifact"
    provider_output = "provider_output"


class SceneSubjectSpec(BaseModel):
    schema_version: Literal["cmf.scene_subject_spec.v1"] = "cmf.scene_subject_spec.v1"
    identity_asset_ref: str = Field(min_length=1)
    emotion: str = Field(min_length=1)
    gesture: str = Field(min_length=1)
    position: str = Field(min_length=1)
    text_space: str | None = None


class AssetSelection(BaseModel):
    schema_version: Literal["cmf.asset_selection.v1"]
    asset_selection_id: UUID
    scene_spec_id: UUID
    asset_id: UUID
    asset_type: str = Field(min_length=1)
    asset_ref: str = Field(min_length=1)
    asset_hash: str = Field(min_length=1)
    source_kind: AssetSourceKind
    brand_context_version_id: UUID | None = None
    source_ref: str | None = None
    approved_for_scene: bool


class PlatformVariant(BaseModel):
    schema_version: Literal["cmf.platform_variant.v1"]
    platform_variant_id: UUID
    scene_spec_id: UUID
    platform: str = Field(min_length=1)
    aspect_ratio: str = Field(min_length=1)
    duration_seconds: float = Field(gt=0)
    captions_required: bool
    caption_plan: str | None = None
    negative_space_required: bool
    text_space: str | None = None
    safe_zone: str = Field(min_length=1)


class EvaluationRequirement(BaseModel):
    schema_version: Literal["cmf.evaluation_requirement.v1"]
    evaluation_requirement_id: UUID
    scene_spec_id: UUID
    requirement_type: str = Field(min_length=1)
    success_criteria: str = Field(min_length=1)
    evidence_required: list[str] = Field(min_length=1)


class RevisionPolicy(BaseModel):
    schema_version: Literal["cmf.revision_policy.v1"]
    revision_policy_id: UUID
    scene_spec_id: UUID
    max_revision_cycles: int = Field(ge=1)
    requires_human_review: bool = True
    allowed_change_scope: list[str] = Field(min_length=1)
    rollback_strategy: str = Field(min_length=1)


class SceneSpec(BaseModel):
    schema_version: Literal["cmf.scene_spec.v1"]
    scene_spec_id: UUID
    complete_editing_session_id: UUID
    format: str = Field(min_length=1)
    aspect_ratio: str = Field(min_length=1)
    duration_seconds: float = Field(gt=0)
    content_type: str = Field(min_length=1)
    visual_style: str = Field(min_length=1)
    platform_targets: list[str] = Field(min_length=1)
    message_role: str = Field(min_length=1)
    emotional_intent: str = Field(min_length=1)
    subject: SceneSubjectSpec
    composition_requirements: dict[str, Any]
    negative_constraints: dict[str, Any]
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    reaction_template_route_id: UUID | None = None
    reaction_template_code: str | None = None
    brand_context_version_id: UUID
    brand_context_version_hash: str = Field(min_length=1)
    input_hash: str = Field(min_length=1)
    asset_selection_ids: list[UUID] = Field(min_length=1)
    platform_variant_ids: list[UUID] = Field(min_length=1)
    evaluation_requirement_ids: list[UUID] = Field(min_length=1)
    revision_policy_id: UUID
    created_at: datetime


class CreativeState(BaseModel):
    schema_version: Literal["cmf.creative_state.v1"]
    creative_state_id: UUID
    complete_editing_session_id: UUID
    scene_spec_id: UUID
    stage: CreativeStateStage
    source_lineage_refs: list[str] = Field(min_length=1)
    state_payload_hash: str = Field(min_length=1)
    latest_scene_spec_receipt_id: UUID | None = None
    status_reason: str = Field(min_length=1)
    updated_at: datetime


class RenderContract(BaseModel):
    schema_version: Literal["cmf.render_contract.v1"]
    render_contract_id: UUID
    scene_spec_id: UUID
    complete_editing_session_id: UUID
    renderer_route: str = Field(min_length=1)
    platform_variant_ids: list[UUID] = Field(min_length=1)
    selected_asset_ids: list[UUID] = Field(min_length=1)
    evaluation_requirement_ids: list[UUID] = Field(min_length=1)
    revision_policy_id: UUID
    reaction_template_code: str | None = None
    renderer_props: dict[str, Any]
    created_at: datetime


class SceneSpecReceipt(BaseModel):
    schema_version: Literal["cmf.scene_spec_receipt.v1"]
    scene_spec_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    complete_editing_session_id: UUID | None = None
    scene_spec_id: UUID | None = None
    creative_state_id: UUID | None = None
    render_contract_id: UUID | None = None
    source_expression_moment_id: UUID | None = None
    asset_route_receipt_id: UUID | None = None
    reaction_template_route_id: UUID | None = None
    reaction_template_code: str | None = None
    brand_context_version_id: UUID | None = None
    brand_context_version_hash: str | None = None
    input_hash: str | None = None
    selected_asset_hashes: list[str] = Field(default_factory=list)
    platform_variant_ids: list[UUID] = Field(default_factory=list)
    revision_policy_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def scene_input_hash(parts: dict[str, Any]) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def new_scene_spec_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    complete_editing_session_id: UUID | None = None,
    scene_spec_id: UUID | None = None,
    creative_state_id: UUID | None = None,
    render_contract_id: UUID | None = None,
    source_expression_moment_id: UUID | None = None,
    asset_route_receipt_id: UUID | None = None,
    reaction_template_route_id: UUID | None = None,
    reaction_template_code: str | None = None,
    brand_context_version_id: UUID | None = None,
    brand_context_version_hash: str | None = None,
    input_hash: str | None = None,
    selected_asset_hashes: list[str] | None = None,
    platform_variant_ids: list[UUID] | None = None,
    revision_policy_id: UUID | None = None,
    command_id: UUID | None = None,
) -> SceneSpecReceipt:
    return SceneSpecReceipt(
        schema_version="cmf.scene_spec_receipt.v1",
        scene_spec_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        complete_editing_session_id=complete_editing_session_id,
        scene_spec_id=scene_spec_id,
        creative_state_id=creative_state_id,
        render_contract_id=render_contract_id,
        source_expression_moment_id=source_expression_moment_id,
        asset_route_receipt_id=asset_route_receipt_id,
        reaction_template_route_id=reaction_template_route_id,
        reaction_template_code=reaction_template_code,
        brand_context_version_id=brand_context_version_id,
        brand_context_version_hash=brand_context_version_hash,
        input_hash=input_hash,
        selected_asset_hashes=selected_asset_hashes or [],
        platform_variant_ids=platform_variant_ids or [],
        revision_policy_id=revision_policy_id,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
