"""Review decision repositories for TS-CMF-052."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.review_decisions import (
    ManualEscalation,
    ReviewApprovalEvent,
    ReviewDecision,
    ReviewDecisionReceipt,
    ReviewDecisionType,
    ReviewRevisionRequest,
    VoiceDnaBoostRequest,
)


@dataclass
class InMemoryReviewDecisionRepository:
    decisions: dict[UUID, ReviewDecision] = field(default_factory=dict)
    revision_requests: dict[UUID, ReviewRevisionRequest] = field(default_factory=dict)
    manual_escalations: dict[UUID, ManualEscalation] = field(default_factory=dict)
    approval_events: dict[UUID, ReviewApprovalEvent] = field(default_factory=dict)
    voice_dna_boost_requests: dict[UUID, VoiceDnaBoostRequest] = field(default_factory=dict)
    receipts: dict[UUID, ReviewDecisionReceipt] = field(default_factory=dict)
    idempotency_index: dict[tuple[UUID, ReviewDecisionType, str], UUID] = field(default_factory=dict)

    def put_decision(self, decision: ReviewDecision) -> ReviewDecision:
        self.decisions[decision.review_decision_id] = decision
        return decision

    def put_revision_request(self, request: ReviewRevisionRequest) -> ReviewRevisionRequest:
        self.revision_requests[request.revision_request_id] = request
        return request

    def put_manual_escalation(self, escalation: ManualEscalation) -> ManualEscalation:
        self.manual_escalations[escalation.manual_escalation_id] = escalation
        return escalation

    def put_approval_event(self, event: ReviewApprovalEvent) -> ReviewApprovalEvent:
        self.approval_events[event.approval_event_id] = event
        return event

    def put_voice_dna_boost_request(self, request: VoiceDnaBoostRequest) -> VoiceDnaBoostRequest:
        self.voice_dna_boost_requests[request.request_id] = request
        return request

    def put_receipt(
        self,
        receipt: ReviewDecisionReceipt,
        *,
        idempotency_key: str | None = None,
    ) -> ReviewDecisionReceipt:
        self.receipts[receipt.receipt_id] = receipt
        if idempotency_key:
            self.idempotency_index[(receipt.review_state_id, receipt.decision_type, idempotency_key)] = receipt.receipt_id
        return receipt

    def receipt_for_idempotency(
        self,
        review_state_id: UUID,
        decision_type: ReviewDecisionType,
        idempotency_key: str,
    ) -> ReviewDecisionReceipt | None:
        receipt_id = self.idempotency_index.get((review_state_id, decision_type, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

