"""Legacy orchestration intent repositories for TS-CMF-017."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.legacy_orchestration import (
    AuthorityOverlapReview,
    InheritedOrchestrationGates,
    LegacyOrchestrationIntentRecord,
    OrchestrationIntentReceipt,
)


@dataclass
class InMemoryLegacyOrchestrationIntentRepository:
    records: dict[UUID, LegacyOrchestrationIntentRecord] = field(default_factory=dict)
    receipts: dict[UUID, OrchestrationIntentReceipt] = field(default_factory=dict)
    overlap_reviews: dict[UUID, AuthorityOverlapReview] = field(default_factory=dict)
    inherited_gates: dict[str, InheritedOrchestrationGates] = field(default_factory=dict)

    def put_record(self, record: LegacyOrchestrationIntentRecord) -> LegacyOrchestrationIntentRecord:
        self.records[record.legacy_orchestration_intent_record_id] = record
        return record

    def put_receipt(self, receipt: OrchestrationIntentReceipt) -> OrchestrationIntentReceipt:
        self.receipts[receipt.orchestration_intent_receipt_id] = receipt
        return receipt

    def put_overlap_review(self, review: AuthorityOverlapReview) -> AuthorityOverlapReview:
        self.overlap_reviews[review.authority_overlap_review_id] = review
        return review

    def put_inherited_gates(self, inherited: InheritedOrchestrationGates) -> InheritedOrchestrationGates:
        self.inherited_gates[inherited.downstream_ref] = inherited
        return inherited
