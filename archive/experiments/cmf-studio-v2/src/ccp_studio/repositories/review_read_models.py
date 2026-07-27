"""Review evidence read-model repositories for TS-CMF-012."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.review_evidence import (
    ApprovalEventRecorded,
    ApprovalEvidenceView,
    ReviewEvidenceReceipt,
    TranscriptRevisionSummary,
)


@dataclass
class InMemoryReviewReadModelRepository:
    transcript_revisions: dict[UUID, TranscriptRevisionSummary] = field(default_factory=dict)
    evidence_views: dict[UUID, ApprovalEvidenceView] = field(default_factory=dict)
    receipts: dict[UUID, ReviewEvidenceReceipt] = field(default_factory=dict)
    approval_events: dict[UUID, ApprovalEventRecorded] = field(default_factory=dict)

    def append_transcript_revision(self, revision: TranscriptRevisionSummary) -> TranscriptRevisionSummary:
        if revision.transcript_revision_id in self.transcript_revisions:
            raise ValueError("transcript revisions are append-only")
        self.transcript_revisions[revision.transcript_revision_id] = revision
        return revision

    def revisions_for_source(self, source_artifact_id: UUID) -> list[TranscriptRevisionSummary]:
        return sorted(
            [
                revision
                for revision in self.transcript_revisions.values()
                if revision.source_artifact_id == source_artifact_id
            ],
            key=lambda item: item.revision_number,
        )

    def put_evidence_view(self, view: ApprovalEvidenceView) -> ApprovalEvidenceView:
        self.evidence_views[view.approval_evidence_view_id] = view
        return view

    def put_receipt(self, receipt: ReviewEvidenceReceipt) -> ReviewEvidenceReceipt:
        self.receipts[receipt.review_evidence_receipt_id] = receipt
        return receipt

    def put_approval_event(self, event: ApprovalEventRecorded) -> ApprovalEventRecorded:
        self.approval_events[event.approval_event_id] = event
        return event
