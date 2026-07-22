"""Review state repositories for TS-CMF-051."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.review_state import (
    ReviewEvidenceState,
    ReviewStateDomainEvent,
    ReviewStateReceipt,
)


@dataclass
class InMemoryReviewStateRepository:
    states: dict[UUID, ReviewEvidenceState] = field(default_factory=dict)
    receipts: dict[UUID, ReviewStateReceipt] = field(default_factory=dict)
    events: list[ReviewStateDomainEvent] = field(default_factory=list)

    def put_state(self, state: ReviewEvidenceState) -> ReviewEvidenceState:
        self.states[state.review_state_id] = state
        return state

    def put_receipt(self, receipt: ReviewStateReceipt) -> ReviewStateReceipt:
        self.receipts[receipt.review_state_receipt_id] = receipt
        return receipt

    def append_event(self, event: ReviewStateDomainEvent) -> ReviewStateDomainEvent:
        self.events.append(event)
        return event

    def states_for_object(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: str,
        object_id: UUID,
    ) -> list[ReviewEvidenceState]:
        states = [
            state
            for state in self.states.values()
            if state.organization_id == organization_id
            and state.brand_id == brand_id
            and state.object_type == object_type
            and state.object_id == object_id
        ]
        return sorted(states, key=lambda item: item.generated_at)

