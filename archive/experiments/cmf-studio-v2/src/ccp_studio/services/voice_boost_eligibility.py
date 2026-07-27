"""Voice-DNA Boost eligibility service for TS-CMF-011."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.consent import ConsentRecordVersion
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.voice import (
    CalibrationReport,
    ProviderReceipt,
    RepairHierarchyProof,
    VoiceBoostEligibilityReport,
    VoiceBridgeClaimCategory,
    VoiceBridgeManifest,
    VoiceEligibilityReceipt,
    VoiceEligibilityStatus,
)
from ccp_studio.repositories.voice import InMemoryVoiceRepository
from ccp_studio.services.consent_guard import ConsentGuardService


RESTRICTED_CLAIM_CATEGORIES = {
    VoiceBridgeClaimCategory.primary_claim,
    VoiceBridgeClaimCategory.decisive_confession,
    VoiceBridgeClaimCategory.medical_advice,
    VoiceBridgeClaimCategory.legal_advice,
    VoiceBridgeClaimCategory.financial_advice,
    VoiceBridgeClaimCategory.decisive_emotional_truth,
    VoiceBridgeClaimCategory.sensitive_assertion,
}


class VoiceBoostEligibilityError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class VoiceBoostEligibilityService:
    consent_guard: ConsentGuardService
    repository: InMemoryVoiceRepository = field(default_factory=InMemoryVoiceRepository)

    @staticmethod
    def duration_cap(final_video_duration_seconds: float) -> float:
        return min(7.0, final_video_duration_seconds * 0.15)

    def evaluate(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
        render_output_id: UUID,
        final_video_duration_seconds: float,
        requested_duration_seconds: float,
        repair_hierarchy: RepairHierarchyProof,
        visual_covering_provided: bool,
        visual_covering_ref: str | None,
        claim_categories: list[VoiceBridgeClaimCategory],
        evaluation_receipt_ids: list[UUID],
        source_evidence_refs: list[str],
        calibration_report: CalibrationReport | None = None,
    ) -> VoiceBoostEligibilityReport:
        current = self._require_current_consent(organization_id, brand_id, guest_or_client_id)
        max_duration = self.duration_cap(final_video_duration_seconds)
        blocker_codes: list[str] = []
        consent_decision = self.consent_guard.evaluate_workflow_boundary(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            command_type="RequestVoiceBoostEligibilityCommand",
            object_type="render_output",
            object_id=render_output_id,
        )
        if not consent_decision.allowed:
            blocker_codes.append(consent_decision.decision_code)
        if not repair_hierarchy.exhausted:
            blocker_codes.append("VOICE_REPAIR_HIERARCHY_INCOMPLETE")
        if requested_duration_seconds > max_duration:
            blocker_codes.append("VOICE_BRIDGE_DURATION_CAP_EXCEEDED")
        if not visual_covering_provided or not visual_covering_ref:
            blocker_codes.append("VOICE_BRIDGE_VISUAL_COVERING_REQUIRED")
        if self.has_restricted_claim(claim_categories):
            blocker_codes.append("VOICE_BRIDGE_CLAIM_RESTRICTED")
        if calibration_report is not None:
            self.repository.put_calibration_report(calibration_report)
            if not calibration_report.passed:
                blocker_codes.append("VOICE_DNA_EVALUATION_FAILED")
        status = VoiceEligibilityStatus.eligible if not blocker_codes else VoiceEligibilityStatus.blocked
        report = VoiceBoostEligibilityReport(
            schema_version="cmf.voice_boost_eligibility_report.v1",
            voice_boost_eligibility_report_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            render_output_id=render_output_id,
            status=status,
            consent_record_version_id=current.consent_record_version_id,
            repair_hierarchy=repair_hierarchy,
            max_duration_seconds=max_duration,
            requested_duration_seconds=requested_duration_seconds,
            visual_covering_required=True,
            visual_covering_provided=visual_covering_provided,
            claim_restriction_passed=not self.has_restricted_claim(claim_categories),
            evaluation_receipt_ids=evaluation_receipt_ids,
            blocker_codes=blocker_codes,
            evidence_refs=source_evidence_refs + repair_hierarchy.evidence_refs,
            created_at=utc_now(),
        )
        self.repository.put_eligibility_report(report)
        self._write_receipt(
            report=report,
            decision_code="VOICE_BOOST_ELIGIBLE" if report.status == VoiceEligibilityStatus.eligible else "VOICE_BOOST_BLOCKED",
            consent_record_version_id=current.consent_record_version_id,
        )
        return report

    def create_bridge_manifest(
        self,
        *,
        report: VoiceBoostEligibilityReport,
        provider_receipt: ProviderReceipt,
        synthetic_audio_uri: str,
        visual_covering_ref: str,
        claim_categories: list[VoiceBridgeClaimCategory],
    ) -> VoiceBridgeManifest:
        if report.status != VoiceEligibilityStatus.eligible:
            raise VoiceBoostEligibilityError("VOICE_BOOST_NOT_ELIGIBLE", "Eligible report is required.")
        manifest = VoiceBridgeManifest(
            schema_version="cmf.voice_bridge_manifest.v1",
            voice_bridge_manifest_id=uuid4(),
            voice_boost_eligibility_report_id=report.voice_boost_eligibility_report_id,
            render_output_id=report.render_output_id,
            provider_receipt_id=provider_receipt.provider_receipt_id,
            synthetic_audio_uri=synthetic_audio_uri,
            requested_duration_seconds=report.requested_duration_seconds,
            max_duration_seconds=report.max_duration_seconds,
            duration_cap_compliant=report.requested_duration_seconds <= report.max_duration_seconds,
            visual_covering_ref=visual_covering_ref,
            claim_categories=claim_categories,
            created_at=utc_now(),
        )
        self.repository.put_provider_receipt(provider_receipt)
        return self.repository.put_bridge_manifest(manifest)

    @staticmethod
    def has_restricted_claim(claim_categories: list[VoiceBridgeClaimCategory]) -> bool:
        return bool(set(claim_categories).intersection(RESTRICTED_CLAIM_CATEGORIES))

    @staticmethod
    def can_approve_voice_bridge(report: VoiceBoostEligibilityReport) -> bool:
        return report.status == VoiceEligibilityStatus.eligible and "VOICE_DNA_EVALUATION_FAILED" not in report.blocker_codes

    def _write_receipt(
        self,
        *,
        report: VoiceBoostEligibilityReport,
        decision_code: str,
        consent_record_version_id: UUID,
    ) -> VoiceEligibilityReceipt:
        receipt = VoiceEligibilityReceipt(
            schema_version="cmf.voice_eligibility_receipt.v1",
            voice_eligibility_receipt_id=uuid4(),
            organization_id=report.organization_id,
            brand_id=report.brand_id,
            render_output_id=report.render_output_id,
            voice_boost_eligibility_report_id=report.voice_boost_eligibility_report_id,
            decision_code=decision_code,
            consent_record_version_id=consent_record_version_id,
            evidence_refs=report.evidence_refs + [str(item) for item in report.evaluation_receipt_ids],
            written_at=utc_now(),
        )
        return self.repository.put_eligibility_receipt(receipt)

    def _require_current_consent(
        self,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
    ) -> ConsentRecordVersion:
        current = self.consent_guard.consent_service.repository.current_version(
            organization_id,
            brand_id,
            guest_or_client_id,
        )
        if current is None:
            raise VoiceBoostEligibilityError("CONSENT_RECORD_REQUIRED", "Current consent is required.")
        return current
