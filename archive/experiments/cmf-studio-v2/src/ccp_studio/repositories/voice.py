"""Voice and audio repositories for TS-CMF-011."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.audio import AudioMixManifest
from ccp_studio.contracts.voice import (
    CalibrationReport,
    ProviderReceipt,
    VoiceBoostEligibilityReport,
    VoiceBridgeManifest,
    VoiceEligibilityReceipt,
)


@dataclass
class InMemoryVoiceRepository:
    eligibility_reports: dict[UUID, VoiceBoostEligibilityReport] = field(default_factory=dict)
    eligibility_receipts: dict[UUID, VoiceEligibilityReceipt] = field(default_factory=dict)
    bridge_manifests: dict[UUID, VoiceBridgeManifest] = field(default_factory=dict)
    provider_receipts: dict[UUID, ProviderReceipt] = field(default_factory=dict)
    calibration_reports: dict[UUID, CalibrationReport] = field(default_factory=dict)
    audio_mix_manifests: dict[UUID, AudioMixManifest] = field(default_factory=dict)

    def put_eligibility_report(self, report: VoiceBoostEligibilityReport) -> VoiceBoostEligibilityReport:
        self.eligibility_reports[report.voice_boost_eligibility_report_id] = report
        return report

    def put_eligibility_receipt(self, receipt: VoiceEligibilityReceipt) -> VoiceEligibilityReceipt:
        self.eligibility_receipts[receipt.voice_eligibility_receipt_id] = receipt
        return receipt

    def put_bridge_manifest(self, manifest: VoiceBridgeManifest) -> VoiceBridgeManifest:
        self.bridge_manifests[manifest.voice_bridge_manifest_id] = manifest
        return manifest

    def put_provider_receipt(self, receipt: ProviderReceipt) -> ProviderReceipt:
        self.provider_receipts[receipt.provider_receipt_id] = receipt
        return receipt

    def put_calibration_report(self, report: CalibrationReport) -> CalibrationReport:
        self.calibration_reports[report.calibration_report_id] = report
        return report

    def put_audio_mix_manifest(self, manifest: AudioMixManifest) -> AudioMixManifest:
        self.audio_mix_manifests[manifest.render_output_id] = manifest
        return manifest

    def audio_manifest_for_render(self, render_output_id: UUID) -> AudioMixManifest | None:
        return self.audio_mix_manifests.get(render_output_id)
