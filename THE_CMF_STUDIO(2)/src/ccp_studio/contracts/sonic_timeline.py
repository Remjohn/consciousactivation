"""Audio, caption, timeline, and final mix contracts for TS-CMF-047."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class SonicAudioComponentRole(str, Enum):
    source_guest = "source_guest"
    interviewer = "interviewer"
    restored_source = "restored_source"
    synthetic_bridge = "synthetic_bridge"
    sfx = "sfx"
    music = "music"
    final_mix = "final_mix"


class AudioTimelineComponent(BaseModel):
    schema_version: Literal["cmf.audio_timeline_component.v1"]
    component_id: UUID
    role: SonicAudioComponentRole
    source_ref: str = Field(min_length=1)
    source_artifact_id: UUID | None = None
    provider_receipt_id: UUID | None = None
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    gain_db: float | None = None
    ducking_rule_id: str | None = None
    content_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def end_must_follow_start(self):
        if self.end_ms <= self.start_ms:
            raise ValueError("end_ms must be greater than start_ms")
        return self


class SonicAudioMixManifest(BaseModel):
    schema_version: Literal["cmf.sonic_audio_mix_manifest.v1"]
    audio_mix_manifest_id: UUID
    render_output_id: UUID
    components: list[AudioTimelineComponent] = Field(min_length=1)
    mix_hash: str = Field(min_length=1)
    created_at: datetime


class CaptionSegment(BaseModel):
    schema_version: Literal["cmf.caption_segment.v1"]
    caption_segment_id: UUID
    text: str = Field(min_length=1)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    source_start_ms: int = Field(ge=0)
    source_end_ms: int = Field(gt=0)
    text_source_ref: str = Field(min_length=1)
    style_tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def timing_must_be_valid(self):
        if self.end_ms <= self.start_ms:
            raise ValueError("caption end_ms must be greater than start_ms")
        if self.source_end_ms <= self.source_start_ms:
            raise ValueError("source_end_ms must be greater than source_start_ms")
        if self.start_ms < self.source_start_ms or self.end_ms > self.source_end_ms:
            raise ValueError("caption timing conflicts with source timing")
        return self


class SonicCaptionManifest(BaseModel):
    schema_version: Literal["cmf.sonic_caption_manifest.v1"]
    caption_manifest_id: UUID
    render_output_id: UUID
    platform_variant: str = Field(min_length=1)
    caption_segments: list[CaptionSegment] = Field(min_length=1)
    style_constraints: dict[str, Any] = Field(default_factory=dict)
    text_source_refs: list[str] = Field(min_length=1)
    manifest_hash: str = Field(min_length=1)
    created_at: datetime


class SonicTimelineSegment(BaseModel):
    schema_version: Literal["cmf.sonic_timeline_segment.v1"]
    timeline_segment_id: UUID
    track: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    component_refs: list[UUID] = Field(default_factory=list)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)

    @model_validator(mode="after")
    def end_must_follow_start(self):
        if self.end_ms <= self.start_ms:
            raise ValueError("timeline end_ms must be greater than start_ms")
        return self


class SonicTimelineManifest(BaseModel):
    schema_version: Literal["cmf.sonic_timeline_manifest.v1"]
    timeline_manifest_id: UUID
    render_output_id: UUID
    duration_ms: int = Field(gt=0)
    segments: list[SonicTimelineSegment] = Field(min_length=1)
    timeline_hash: str = Field(min_length=1)
    created_at: datetime


class DuckingDecision(BaseModel):
    schema_version: Literal["cmf.ducking_decision.v1"]
    ducking_decision_id: UUID
    audio_mix_manifest_id: UUID
    ducking_rule_id: str = Field(min_length=1)
    driver_component_ids: list[UUID] = Field(min_length=1)
    ducked_component_ids: list[UUID] = Field(min_length=1)
    affected_window_ms: tuple[int, int]
    gain_reduction_db: float = Field(lt=0)
    reason: str = Field(min_length=1)
    decision_hash: str = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def window_must_be_valid(self):
        if self.affected_window_ms[1] <= self.affected_window_ms[0]:
            raise ValueError("affected_window_ms end must be greater than start")
        return self


class VoiceBridgePolicyValidation(BaseModel):
    schema_version: Literal["cmf.voice_bridge_policy_validation.v1"]
    voice_bridge_policy_validation_id: UUID
    audio_mix_manifest_id: UUID
    voice_boost_eligibility_report_id: UUID | None = None
    voice_bridge_manifest_id: UUID | None = None
    synthetic_component_ids: list[UUID] = Field(default_factory=list)
    passed: bool
    blocker_codes: list[str] = Field(default_factory=list)
    max_duration_seconds: float | None = None
    requested_duration_seconds: float | None = None
    visual_covering_ref: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class SonicTimelineReceipt(BaseModel):
    schema_version: Literal["cmf.sonic_timeline_receipt.v1"]
    sonic_timeline_receipt_id: UUID
    render_output_id: UUID
    audio_mix_manifest_id: UUID
    caption_manifest_id: UUID
    timeline_manifest_id: UUID
    ducking_decision_ids: list[UUID] = Field(default_factory=list)
    voice_bridge_policy_validation_id: UUID | None = None
    audio_mix_hash: str = Field(min_length=1)
    caption_hash: str = Field(min_length=1)
    timeline_hash: str = Field(min_length=1)
    final_mix_ref: str = Field(min_length=1)
    validation_summary: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


class SonicTimelineReviewReadModel(BaseModel):
    schema_version: Literal["cmf.sonic_timeline_review_read_model.v1"]
    sonic_timeline_receipt_id: UUID
    render_output_id: UUID
    audio_lineage: list[dict[str, Any]]
    caption_lineage: list[dict[str, Any]]
    timeline_lineage: list[dict[str, Any]]
    mix_lineage: dict[str, Any]
    manifest_hashes: dict[str, str]
    validation_summary: str


def sonic_timeline_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_sonic_timeline_receipt(
    *,
    render_output_id: UUID,
    audio_mix_manifest: SonicAudioMixManifest,
    caption_manifest: SonicCaptionManifest,
    timeline_manifest: SonicTimelineManifest,
    final_mix_ref: str,
    actor_id: UUID,
    validation_summary: str,
    decision_code: str = "SONIC_TIMELINE_VALIDATED",
    ducking_decision_ids: list[UUID] | None = None,
    voice_bridge_policy_validation_id: UUID | None = None,
    evidence_refs: list[str] | None = None,
    command_id: UUID | None = None,
) -> SonicTimelineReceipt:
    return SonicTimelineReceipt(
        schema_version="cmf.sonic_timeline_receipt.v1",
        sonic_timeline_receipt_id=uuid4(),
        render_output_id=render_output_id,
        audio_mix_manifest_id=audio_mix_manifest.audio_mix_manifest_id,
        caption_manifest_id=caption_manifest.caption_manifest_id,
        timeline_manifest_id=timeline_manifest.timeline_manifest_id,
        ducking_decision_ids=ducking_decision_ids or [],
        voice_bridge_policy_validation_id=voice_bridge_policy_validation_id,
        audio_mix_hash=audio_mix_manifest.mix_hash,
        caption_hash=caption_manifest.manifest_hash,
        timeline_hash=timeline_manifest.timeline_hash,
        final_mix_ref=final_mix_ref,
        validation_summary=validation_summary,
        decision_code=decision_code,
        evidence_refs=evidence_refs or [],
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
