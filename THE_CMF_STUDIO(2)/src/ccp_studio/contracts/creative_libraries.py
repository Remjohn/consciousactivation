"""Creative library contracts for TS-CMF-020."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class CreativeItemStatus(str, Enum):
    draft = "draft"
    evaluation_failed = "evaluation_failed"
    approved = "approved"
    locked = "locked"
    rejected = "rejected"


class CreativeLibraryItemKind(str, Enum):
    rig_manifest = "rig_manifest"
    prop = "prop"
    micro_semiotic_anchor = "micro_semiotic_anchor"
    motion_recipe = "motion_recipe"
    sfx_asset = "sfx_asset"
    composition_preference = "composition_preference"
    platform_profile = "platform_profile"
    publishing_profile = "publishing_profile"


class CreativeLibraryReceipt(BaseModel):
    schema_version: Literal["cmf.creative_library_receipt.v1"]
    creative_library_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID | None = None
    item_kind: CreativeLibraryItemKind
    item_id: UUID
    action: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


class CreativeEvaluationState(BaseModel):
    schema_version: Literal["cmf.creative_evaluation_state.v1"]
    score: float = Field(ge=0, le=1)
    passed: bool
    failure_notes: list[str] = Field(default_factory=list)


class MicroSemioticAnchor(BaseModel):
    schema_version: Literal["cmf.micro_semiotic_anchor.v1"]
    micro_semiotic_anchor_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    cultural_context: str = Field(min_length=1)
    audience_signal: str = Field(min_length=1)
    recognition_effects: list[str] = Field(min_length=1)
    visual_description: str = Field(min_length=1)
    preferred_placement: list[str] = Field(min_length=1)
    subtlety_score: float = Field(ge=0, le=1)
    comment_potential_score: float = Field(ge=0, le=1)
    brand_fit_score: float = Field(ge=0, le=1)
    distraction_risk_score: float = Field(ge=0, le=1)
    legal_risk_score: float = Field(ge=0, le=1)
    use_constraints: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(min_length=1)
    version_hash: str = Field(min_length=1)
    status: CreativeItemStatus
    created_at: datetime
    updated_at: datetime


class MotionBeat(BaseModel):
    beat: str = Field(min_length=1)
    duration_seconds: float = Field(gt=0)
    actions: list[str] = Field(min_length=1)


class MotionRecipe(BaseModel):
    schema_version: Literal["cmf.motion_recipe.v1"]
    motion_recipe_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    name: str = Field(min_length=1)
    motion_language: str = Field(min_length=1)
    motion_intensity: str = Field(min_length=1)
    max_simultaneous_moving_layers: int = Field(ge=1, le=8)
    beats: list[MotionBeat] = Field(min_length=1)
    use_constraints: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(min_length=1)
    version_hash: str = Field(min_length=1)
    evaluation_state: CreativeEvaluationState | None = None
    status: CreativeItemStatus
    created_at: datetime
    updated_at: datetime


class SfxAsset(BaseModel):
    schema_version: Literal["cmf.sfx_asset.v1"]
    sfx_asset_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    category: str = Field(min_length=1)
    event_mapping: str = Field(min_length=1)
    asset_uri: str = Field(min_length=1)
    use_context: str = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    version_hash: str = Field(min_length=1)
    evaluation_state: CreativeEvaluationState | None = None
    status: CreativeItemStatus
    created_at: datetime
    updated_at: datetime


class CompositionPreference(BaseModel):
    schema_version: Literal["cmf.composition_preference.v1"]
    composition_preference_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    name: str = Field(min_length=1)
    aspect_ratio: str = Field(min_length=1)
    subject_placement: str = Field(min_length=1)
    text_safe_zones: list[str] = Field(min_length=1)
    negative_space_rules: list[str] = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    version_hash: str = Field(min_length=1)
    evaluation_state: CreativeEvaluationState | None = None
    status: CreativeItemStatus
    created_at: datetime
    updated_at: datetime


class PlatformProfile(BaseModel):
    schema_version: Literal["cmf.platform_profile.v1"]
    platform_profile_id: UUID
    organization_id: UUID
    brand_id: UUID
    platform: str = Field(min_length=1)
    aspect_ratio: str = Field(min_length=1)
    caption_requirements: list[str] = Field(min_length=1)
    negative_space_requirements: list[str] = Field(min_length=1)
    publishing_requirements: list[str] = Field(min_length=1)
    version_hash: str = Field(min_length=1)
    status: CreativeItemStatus
    created_at: datetime
    updated_at: datetime


def creative_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_creative_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    item_kind: CreativeLibraryItemKind,
    item_id: UUID,
    action: str,
    decision_code: str,
    evidence_refs: list[str],
    brand_genesis_session_id: UUID | None = None,
) -> CreativeLibraryReceipt:
    return CreativeLibraryReceipt(
        schema_version="cmf.creative_library_receipt.v1",
        creative_library_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        brand_genesis_session_id=brand_genesis_session_id,
        item_kind=item_kind,
        item_id=item_id,
        action=action,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
