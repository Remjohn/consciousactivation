"""Audio classification contracts for TS-CMF-011."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class AudioSourceType(str, Enum):
    source_voice = "source_voice"
    repaired_source_voice = "repaired_source_voice"
    synthetic_bridge_voice = "synthetic_bridge_voice"
    interviewer_voice = "interviewer_voice"
    generated_audio = "generated_audio"
    sfx = "sfx"
    music = "music"


class AudioSegmentClassification(BaseModel):
    schema_version: Literal["cmf.audio_segment_classification.v1"]
    segment_id: UUID
    source_type: AudioSourceType
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    source_ref: str = Field(min_length=1)
    provider_receipt_id: UUID | None = None

    @model_validator(mode="after")
    def end_must_follow_start(self):
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")
        return self


class AudioMixManifest(BaseModel):
    schema_version: Literal["cmf.audio_mix_manifest.v1"]
    audio_mix_manifest_id: UUID
    render_output_id: UUID
    segments: list[AudioSegmentClassification] = Field(min_length=1)
    created_at: datetime


def new_audio_segment_classification(
    *,
    source_type: AudioSourceType,
    start_seconds: float,
    end_seconds: float,
    source_ref: str,
    provider_receipt_id: UUID | None = None,
) -> AudioSegmentClassification:
    return AudioSegmentClassification(
        schema_version="cmf.audio_segment_classification.v1",
        segment_id=uuid4(),
        source_type=source_type,
        start_seconds=start_seconds,
        end_seconds=end_seconds,
        source_ref=source_ref,
        provider_receipt_id=provider_receipt_id,
    )


def new_audio_mix_manifest(
    *,
    render_output_id: UUID,
    segments: list[AudioSegmentClassification],
) -> AudioMixManifest:
    return AudioMixManifest(
        schema_version="cmf.audio_mix_manifest.v1",
        audio_mix_manifest_id=uuid4(),
        render_output_id=render_output_id,
        segments=segments,
        created_at=utc_now(),
    )
