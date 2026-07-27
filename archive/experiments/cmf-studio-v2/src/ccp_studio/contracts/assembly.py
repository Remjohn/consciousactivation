"""Layer, animation, timeline, caption, and sonic assembly contracts for TS-CMF-039."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class AudioComponentRole(str, Enum):
    source_voice = "source_voice"
    interviewer_voice = "interviewer_voice"
    repaired_source_voice = "repaired_source_voice"
    synthetic_bridge_voice = "synthetic_bridge_voice"
    sfx = "sfx"
    music = "music"


class LayerEntry(BaseModel):
    schema_version: Literal["cmf.layer_entry.v1"]
    layer_id: UUID
    semantic_type: str = Field(min_length=1)
    file_uri: str = Field(min_length=1)
    asset_hash: str = Field(min_length=1)
    z_index: int
    bbox: tuple[int, int, int, int]
    anchor_point: tuple[float, float]
    motion_affordances: list[str] = Field(default_factory=list)
    brand_context_asset_id: UUID | None = None
    source_ref: str = Field(min_length=1)


class LayerManifest(BaseModel):
    schema_version: Literal["cmf.layer_manifest.v1"]
    layer_manifest_id: UUID
    scene_spec_id: UUID
    canvas_width: int = Field(gt=0)
    canvas_height: int = Field(gt=0)
    aspect_ratio: str = Field(min_length=1)
    layers: list[LayerEntry] = Field(min_length=1)
    manifest_hash: str = Field(min_length=1)


class AnimationPlan(BaseModel):
    schema_version: Literal["cmf.animation_plan.v1"]
    animation_plan_id: UUID
    layer_manifest_id: UUID
    fps: int = Field(gt=0)
    duration_frames: int = Field(gt=0)
    motion_style: str = Field(min_length=1)
    layer_animations: list[dict[str, Any]] = Field(min_length=1)
    plan_hash: str = Field(min_length=1)


class EditDecision(BaseModel):
    schema_version: Literal["cmf.edit_decision.v1"]
    edit_decision_id: UUID
    source_ref: str = Field(min_length=1)
    track: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    operation: str = Field(min_length=1)

    @model_validator(mode="after")
    def end_must_follow_start(self):
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")
        return self


class EditDecisionList(BaseModel):
    schema_version: Literal["cmf.edit_decision_list.v1"]
    edit_decision_list_id: UUID
    scene_spec_id: UUID
    decisions: list[EditDecision] = Field(min_length=1)
    edl_hash: str = Field(min_length=1)


class TimelineSegment(BaseModel):
    schema_version: Literal["cmf.timeline_segment.v1"]
    segment_id: UUID
    track: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)

    @model_validator(mode="after")
    def end_must_follow_start(self):
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")
        return self


class TimelineManifest(BaseModel):
    schema_version: Literal["cmf.timeline_manifest.v1"]
    timeline_manifest_id: UUID
    scene_spec_id: UUID
    duration_seconds: float = Field(gt=0)
    segments: list[TimelineSegment] = Field(min_length=1)
    timeline_hash: str = Field(min_length=1)


class CaptionCue(BaseModel):
    schema_version: Literal["cmf.caption_cue.v1"]
    caption_cue_id: UUID
    text: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    source_start_seconds: float = Field(ge=0)
    source_end_seconds: float = Field(gt=0)
    source_ref: str = Field(min_length=1)

    @model_validator(mode="after")
    def timing_must_be_valid(self):
        if self.end_seconds <= self.start_seconds:
            raise ValueError("caption end_seconds must be greater than start_seconds")
        if self.source_end_seconds <= self.source_start_seconds:
            raise ValueError("source_end_seconds must be greater than source_start_seconds")
        return self


class CaptionManifest(BaseModel):
    schema_version: Literal["cmf.caption_manifest.v1"]
    caption_manifest_id: UUID
    scene_spec_id: UUID
    cues: list[CaptionCue] = Field(min_length=1)
    negative_space_rule: str = Field(min_length=1)
    caption_hash: str = Field(min_length=1)


class AudioMixComponent(BaseModel):
    schema_version: Literal["cmf.audio_mix_component.v1"]
    audio_mix_component_id: UUID
    role: AudioComponentRole
    source_ref: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    provider_receipt_id: UUID | None = None

    @model_validator(mode="after")
    def end_must_follow_start(self):
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")
        return self


class AudioMixManifest(BaseModel):
    schema_version: Literal["cmf.assembly_audio_mix_manifest.v1"]
    audio_mix_manifest_id: UUID
    scene_spec_id: UUID
    components: list[AudioMixComponent] = Field(min_length=1)
    mix_hash: str = Field(min_length=1)


class AssemblyPlan(BaseModel):
    schema_version: Literal["cmf.assembly_plan.v1"]
    assembly_plan_id: UUID
    scene_spec_id: UUID
    complete_editing_session_id: UUID
    layer_manifest_id: UUID
    animation_plan_id: UUID
    edit_decision_list_id: UUID
    timeline_manifest_id: UUID
    caption_manifest_id: UUID
    audio_mix_manifest_id: UUID
    renderer_route: str = Field(min_length=1)
    manifest_hashes: dict[str, str] = Field(min_length=1)
    selected_asset_ids: list[UUID] = Field(default_factory=list)
    valid_for_render: bool
    created_at: datetime


class AssemblyPlanReceipt(BaseModel):
    schema_version: Literal["cmf.assembly_plan_receipt.v1"]
    assembly_plan_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    complete_editing_session_id: UUID | None = None
    scene_spec_id: UUID | None = None
    assembly_plan_id: UUID | None = None
    layer_manifest_id: UUID | None = None
    animation_plan_id: UUID | None = None
    edit_decision_list_id: UUID | None = None
    timeline_manifest_id: UUID | None = None
    caption_manifest_id: UUID | None = None
    audio_mix_manifest_id: UUID | None = None
    manifest_hashes: dict[str, str] = Field(default_factory=dict)
    selected_asset_ids: list[UUID] = Field(default_factory=list)
    brand_context_version_id: UUID | None = None
    brand_context_version_hash: str | None = None
    timing_validation_passed: bool
    caption_validation_passed: bool
    sonic_validation_passed: bool
    renderer_route: str | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def assembly_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_assembly_plan_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    complete_editing_session_id: UUID | None = None,
    scene_spec_id: UUID | None = None,
    assembly_plan_id: UUID | None = None,
    layer_manifest_id: UUID | None = None,
    animation_plan_id: UUID | None = None,
    edit_decision_list_id: UUID | None = None,
    timeline_manifest_id: UUID | None = None,
    caption_manifest_id: UUID | None = None,
    audio_mix_manifest_id: UUID | None = None,
    manifest_hashes: dict[str, str] | None = None,
    selected_asset_ids: list[UUID] | None = None,
    brand_context_version_id: UUID | None = None,
    brand_context_version_hash: str | None = None,
    timing_validation_passed: bool = False,
    caption_validation_passed: bool = False,
    sonic_validation_passed: bool = False,
    renderer_route: str | None = None,
    command_id: UUID | None = None,
) -> AssemblyPlanReceipt:
    return AssemblyPlanReceipt(
        schema_version="cmf.assembly_plan_receipt.v1",
        assembly_plan_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        complete_editing_session_id=complete_editing_session_id,
        scene_spec_id=scene_spec_id,
        assembly_plan_id=assembly_plan_id,
        layer_manifest_id=layer_manifest_id,
        animation_plan_id=animation_plan_id,
        edit_decision_list_id=edit_decision_list_id,
        timeline_manifest_id=timeline_manifest_id,
        caption_manifest_id=caption_manifest_id,
        audio_mix_manifest_id=audio_mix_manifest_id,
        manifest_hashes=manifest_hashes or {},
        selected_asset_ids=selected_asset_ids or [],
        brand_context_version_id=brand_context_version_id,
        brand_context_version_hash=brand_context_version_hash,
        timing_validation_passed=timing_validation_passed,
        caption_validation_passed=caption_validation_passed,
        sonic_validation_passed=sonic_validation_passed,
        renderer_route=renderer_route,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
