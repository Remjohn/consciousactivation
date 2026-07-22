"""Approval evidence blocker policy for TS-CMF-012."""

from __future__ import annotations

from ccp_studio.contracts.consent import ConsentRecordVersion, ConsentVersionStatus
from ccp_studio.contracts.review_evidence import (
    ApprovalBlocker,
    ApprovalBlockerCode,
    ApprovalEvidenceView,
)
from ccp_studio.contracts.voice import VoiceBoostEligibilityReport, VoiceEligibilityStatus


class ApprovalEvidencePolicy:
    telegram_complexity_threshold = 3

    def evaluate(
        self,
        *,
        view: ApprovalEvidenceView,
        consent_version: ConsentRecordVersion,
        voice_report: VoiceBoostEligibilityReport | None = None,
    ) -> list[ApprovalBlocker]:
        blockers: list[ApprovalBlocker] = []
        if not view.source_references or any(item.claim_ref is None for item in view.source_references):
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.missing_source_reference,
                    "Claim or asset segment is missing a timestamped source reference.",
                    "add_source_reference_or_remove_claim",
                )
            )
        if consent_version.status != ConsentVersionStatus.active:
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.consent_incompatible,
                    "Current consent is not active for approval.",
                    "request_updated_consent",
                    [str(consent_version.consent_record_version_id)],
                )
            )
        if not view.file_provenance_refs:
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.provenance_missing,
                    "File provenance is required before approval.",
                    "repair_file_provenance",
                )
            )
        if view.audio_mix_manifest_id is None:
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.voice_classification_missing,
                    "Audio mix classification is required before approval.",
                    "classify_audio_segments",
                )
            )
        if voice_report is not None and voice_report.status == VoiceEligibilityStatus.blocked:
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.voice_eligibility_failed,
                    "Voice eligibility failed for this asset.",
                    "remove_or_repair_voice_bridge",
                    voice_report.blocker_codes,
                )
            )
        if not view.evaluation_receipt_ids:
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.evaluation_receipt_missing,
                    "Evaluation receipt is required before approval.",
                    "run_evaluation",
                )
            )
        if view.telegram_complexity_score > self.telegram_complexity_threshold:
            blockers.append(
                self._blocker(
                    ApprovalBlockerCode.pwa_review_required,
                    "Evidence is too complex for Telegram quick approval.",
                    "open_pwa_review",
                )
            )
        return blockers

    @staticmethod
    def _blocker(
        code: ApprovalBlockerCode,
        message: str,
        repair_action: str,
        evidence_refs: list[str] | None = None,
    ) -> ApprovalBlocker:
        return ApprovalBlocker(
            schema_version="cmf.approval_blocker.v1",
            blocker_code=code,
            message=message,
            repair_action=repair_action,
            evidence_refs=evidence_refs or [],
        )
