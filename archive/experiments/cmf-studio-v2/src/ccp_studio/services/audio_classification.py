"""Audio segment classification service for TS-CMF-011."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.audio import (
    AudioMixManifest,
    AudioSegmentClassification,
    AudioSourceType,
    new_audio_mix_manifest,
    new_audio_segment_classification,
)
from ccp_studio.repositories.voice import InMemoryVoiceRepository


class AudioClassificationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class AudioClassificationService:
    repository: InMemoryVoiceRepository = field(default_factory=InMemoryVoiceRepository)

    def classify_segment(
        self,
        *,
        source_type: AudioSourceType,
        start_seconds: float,
        end_seconds: float,
        source_ref: str,
        provider_receipt_id: UUID | None = None,
    ) -> AudioSegmentClassification:
        return new_audio_segment_classification(
            source_type=source_type,
            start_seconds=start_seconds,
            end_seconds=end_seconds,
            source_ref=source_ref,
            provider_receipt_id=provider_receipt_id,
        )

    def create_manifest(
        self,
        *,
        render_output_id: UUID,
        segments: list[AudioSegmentClassification],
    ) -> AudioMixManifest:
        manifest = new_audio_mix_manifest(render_output_id=render_output_id, segments=segments)
        return self.repository.put_audio_mix_manifest(manifest)

    def require_manifest_before_publishing(self, *, render_output_id: UUID) -> AudioMixManifest:
        manifest = self.repository.audio_manifest_for_render(render_output_id)
        if manifest is None:
            raise AudioClassificationError(
                "AUDIO_CLASSIFICATION_REQUIRED",
                "Audio mix manifest is required before publishing.",
            )
        return manifest
