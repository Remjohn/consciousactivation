"""Audio, caption, timeline, and mix assembly repositories for TS-CMF-047."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.sonic_timeline import (
    DuckingDecision,
    SonicAudioMixManifest,
    SonicCaptionManifest,
    SonicTimelineManifest,
    SonicTimelineReceipt,
    VoiceBridgePolicyValidation,
)


@dataclass
class InMemorySonicTimelineRepository:
    audio_mix_manifests: dict[UUID, SonicAudioMixManifest] = field(default_factory=dict)
    caption_manifests: dict[UUID, SonicCaptionManifest] = field(default_factory=dict)
    timeline_manifests: dict[UUID, SonicTimelineManifest] = field(default_factory=dict)
    ducking_decisions: dict[UUID, DuckingDecision] = field(default_factory=dict)
    voice_policy_validations: dict[UUID, VoiceBridgePolicyValidation] = field(default_factory=dict)
    receipts: dict[UUID, SonicTimelineReceipt] = field(default_factory=dict)

    def put_audio_mix_manifest(self, manifest: SonicAudioMixManifest) -> SonicAudioMixManifest:
        self.audio_mix_manifests[manifest.audio_mix_manifest_id] = manifest
        return manifest

    def put_caption_manifest(self, manifest: SonicCaptionManifest) -> SonicCaptionManifest:
        self.caption_manifests[manifest.caption_manifest_id] = manifest
        return manifest

    def put_timeline_manifest(self, manifest: SonicTimelineManifest) -> SonicTimelineManifest:
        self.timeline_manifests[manifest.timeline_manifest_id] = manifest
        return manifest

    def put_ducking_decision(self, decision: DuckingDecision) -> DuckingDecision:
        self.ducking_decisions[decision.ducking_decision_id] = decision
        return decision

    def put_voice_policy_validation(self, validation: VoiceBridgePolicyValidation) -> VoiceBridgePolicyValidation:
        self.voice_policy_validations[validation.voice_bridge_policy_validation_id] = validation
        return validation

    def put_receipt(self, receipt: SonicTimelineReceipt) -> SonicTimelineReceipt:
        self.receipts[receipt.sonic_timeline_receipt_id] = receipt
        return receipt
