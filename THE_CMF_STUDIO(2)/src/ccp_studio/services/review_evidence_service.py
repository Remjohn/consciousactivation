"""Review evidence service for TS-CMF-012."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.consent import ConsentRecordVersion
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.review_evidence import (
    ApprovalBlocker,
    ApprovalBlockerCode,
    ApprovalEventRecorded,
    ApprovalEvidenceView,
    ReviewEvidenceReceipt,
    SourceReference,
    TranscriptRevisionSummary,
    new_transcript_revision_summary,
)
from ccp_studio.contracts.surfaces import DeepLinkTarget
from ccp_studio.contracts.voice import VoiceBoostEligibilityReport
from ccp_studio.domain.policies.approval_evidence_policy import ApprovalEvidencePolicy
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.evaluation_receipts import InMemoryEvaluationReceiptRepository
from ccp_studio.repositories.review_read_models import InMemoryReviewReadModelRepository
from ccp_studio.repositories.source_artifacts import InMemorySourceArtifactRepository
from ccp_studio.repositories.voice import InMemoryVoiceRepository


class ReviewEvidenceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ReviewEvidenceService:
    consent_repository: InMemoryConsentRepository
    source_repository: InMemorySourceArtifactRepository
    voice_repository: InMemoryVoiceRepository | None = None
    evaluation_repository: InMemoryEvaluationReceiptRepository | None = None
    repository: InMemoryReviewReadModelRepository = field(default_factory=InMemoryReviewReadModelRepository)
    policy: ApprovalEvidencePolicy = field(default_factory=ApprovalEvidencePolicy)

    def append_transcript_revision(
        self,
        *,
        source_artifact_id: UUID,
        revision_number: int,
        transcript_hash: str,
        source_hash: str,
        text_ref: str,
    ) -> TranscriptRevisionSummary:
        return self.repository.append_transcript_revision(
            new_transcript_revision_summary(
                source_artifact_id=source_artifact_id,
                revision_number=revision_number,
                transcript_hash=transcript_hash,
                source_hash=source_hash,
                text_ref=text_ref,
            )
        )

    def generate_evidence_view(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
        object_type: str,
        object_id: UUID,
        source_references: list[SourceReference],
        evaluation_receipt_ids: list[UUID],
        audio_mix_manifest_id: UUID | None,
        file_provenance_refs: list[str],
        voice_eligibility_report_id: UUID | None = None,
        telegram_complexity_score: int = 0,
    ) -> ApprovalEvidenceView:
        consent_version = self._require_current_consent(organization_id, brand_id, guest_or_client_id)
        scoped_source_references = self._filter_source_references_for_scope(
            organization_id,
            brand_id,
            source_references,
        )
        transcript_revisions = self._transcript_revisions_for(scoped_source_references)
        voice_report = self._voice_report(voice_eligibility_report_id)
        base_view = ApprovalEvidenceView(
            schema_version="cmf.approval_evidence_view.v1",
            approval_evidence_view_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=object_type,
            object_id=object_id,
            consent_record_version_id=consent_version.consent_record_version_id,
            source_references=scoped_source_references,
            transcript_revision_ids=[revision.transcript_revision_id for revision in transcript_revisions],
            transcript_revisions=transcript_revisions,
            evaluation_receipt_ids=evaluation_receipt_ids,
            audio_mix_manifest_id=audio_mix_manifest_id,
            file_provenance_refs=file_provenance_refs,
            voice_eligibility_report_id=voice_eligibility_report_id,
            telegram_complexity_score=telegram_complexity_score,
            generated_at=utc_now(),
        )
        blockers = self.policy.evaluate(
            view=base_view,
            consent_version=consent_version,
            voice_report=voice_report,
        )
        blockers.extend(self._evaluation_blockers(evaluation_receipt_ids))
        view = base_view.model_copy(update={"blockers": blockers})
        self.repository.put_evidence_view(view)
        self._write_receipt(view)
        return view

    def approve_with_evidence(
        self,
        *,
        approval_evidence_view_id: UUID,
        approved_by_actor_id: UUID,
    ) -> ApprovalEventRecorded:
        view = self.repository.evidence_views.get(approval_evidence_view_id)
        if view is None:
            raise ReviewEvidenceError("APPROVAL_EVIDENCE_VIEW_REQUIRED", "Approval evidence view is required.")
        receipt = self._receipt_for_view(view.approval_evidence_view_id)
        if receipt is None:
            raise ReviewEvidenceError("REVIEW_EVIDENCE_RECEIPT_REQUIRED", "Review evidence receipt is required.")
        if view.blockers:
            first = view.blockers[0].blocker_code.value.upper()
            raise ReviewEvidenceError(first, view.blockers[0].message)
        event = ApprovalEventRecorded(
            schema_version="cmf.approval_event_recorded.v1",
            approval_event_id=uuid4(),
            organization_id=view.organization_id,
            brand_id=view.brand_id,
            object_type=view.object_type,
            object_id=view.object_id,
            approved_by_actor_id=approved_by_actor_id,
            approval_evidence_view_id=view.approval_evidence_view_id,
            review_evidence_receipt_id=receipt.review_evidence_receipt_id,
            consent_record_version_id=view.consent_record_version_id,
            source_reference_ids=[item.source_reference_id for item in view.source_references],
            evaluation_receipt_ids=view.evaluation_receipt_ids,
            audit_evidence_refs=[
                str(view.consent_record_version_id),
                *[str(item.source_reference_id) for item in view.source_references],
                *[str(item) for item in view.evaluation_receipt_ids],
            ],
            recorded_at=utc_now(),
        )
        return self.repository.put_approval_event(event)

    def telegram_deep_link_for_review(self, view: ApprovalEvidenceView) -> DeepLinkTarget | None:
        if not any(blocker.blocker_code == ApprovalBlockerCode.pwa_review_required for blocker in view.blockers):
            return None
        return DeepLinkTarget(
            schema_version="cmf.deep_link_target.v1",
            target_surface="pwa",
            route=f"/brands/{view.brand_id}/review/{view.object_type}/{view.object_id}",
            object_type=view.object_type,
            object_id=view.object_id,
            brand_id=view.brand_id,
            required_reason="PWA_REVIEW_REQUIRED",
        )

    def _write_receipt(self, view: ApprovalEvidenceView) -> ReviewEvidenceReceipt:
        receipt = ReviewEvidenceReceipt(
            schema_version="cmf.review_evidence_receipt.v1",
            review_evidence_receipt_id=uuid4(),
            approval_evidence_view_id=view.approval_evidence_view_id,
            organization_id=view.organization_id,
            brand_id=view.brand_id,
            object_type=view.object_type,
            object_id=view.object_id,
            decision_code="APPROVAL_EVIDENCE_READY" if not view.blockers else "APPROVAL_EVIDENCE_BLOCKED",
            blocker_codes=[blocker.blocker_code for blocker in view.blockers],
            evidence_refs=[
                str(view.consent_record_version_id),
                *[str(item.source_reference_id) for item in view.source_references],
                *[str(item) for item in view.evaluation_receipt_ids],
            ],
            written_at=utc_now(),
        )
        return self.repository.put_receipt(receipt)

    def _receipt_for_view(self, approval_evidence_view_id: UUID) -> ReviewEvidenceReceipt | None:
        return next(
            (
                receipt
                for receipt in self.repository.receipts.values()
                if receipt.approval_evidence_view_id == approval_evidence_view_id
            ),
            None,
        )

    def _require_current_consent(
        self,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
    ) -> ConsentRecordVersion:
        current = self.consent_repository.current_version(organization_id, brand_id, guest_or_client_id)
        if current is None:
            raise ReviewEvidenceError("CONSENT_REVIEW_REQUIRED", "Consent review is required.")
        return current

    def _filter_source_references_for_scope(
        self,
        organization_id: UUID,
        brand_id: UUID,
        source_references: list[SourceReference],
    ) -> list[SourceReference]:
        scoped: list[SourceReference] = []
        for source_reference in source_references:
            artifact = self.source_repository.artifacts.get(source_reference.source_artifact_id)
            if artifact and artifact.organization_id == organization_id and artifact.brand_id == brand_id:
                scoped.append(source_reference)
        return scoped

    def _transcript_revisions_for(
        self,
        source_references: list[SourceReference],
    ) -> list[TranscriptRevisionSummary]:
        source_ids = {item.source_artifact_id for item in source_references}
        revisions: list[TranscriptRevisionSummary] = []
        for source_artifact_id in source_ids:
            revisions.extend(self.repository.revisions_for_source(source_artifact_id))
        return sorted(revisions, key=lambda item: (str(item.source_artifact_id), item.revision_number))

    def _voice_report(self, voice_eligibility_report_id: UUID | None) -> VoiceBoostEligibilityReport | None:
        if voice_eligibility_report_id is None or self.voice_repository is None:
            return None
        return self.voice_repository.eligibility_reports.get(voice_eligibility_report_id)

    def _evaluation_blockers(self, evaluation_receipt_ids: list[UUID]) -> list[ApprovalBlocker]:
        if self.evaluation_repository is None:
            return []
        blockers: list[ApprovalBlocker] = []
        for evaluation_receipt_id in evaluation_receipt_ids:
            receipt = self.evaluation_repository.receipts.get(evaluation_receipt_id)
            if receipt is None:
                blockers.append(
                    ApprovalBlocker(
                        schema_version="cmf.approval_blocker.v1",
                        blocker_code=ApprovalBlockerCode.evaluation_receipt_missing,
                        message="Referenced evaluation receipt is not available for approval review.",
                        evidence_refs=[str(evaluation_receipt_id)],
                        repair_action="run_evaluation",
                    )
                )
                continue
            for evaluation_blocker in self.evaluation_repository.blockers_for_receipt(evaluation_receipt_id):
                blockers.append(
                    ApprovalBlocker(
                        schema_version="cmf.approval_blocker.v1",
                        blocker_code=ApprovalBlockerCode.evaluation_hard_failure,
                        message=evaluation_blocker.message,
                        evidence_refs=evaluation_blocker.evidence_refs,
                        repair_action=evaluation_blocker.repair_action,
                    )
                )
        return blockers
