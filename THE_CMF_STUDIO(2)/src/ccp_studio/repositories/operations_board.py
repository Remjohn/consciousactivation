"""Operations Board repository for TS-CMF-059."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.operations_board import (
    BlockerSummary,
    OperationsBoardState,
    OperationsDomainEvent,
    OperationsReceipt,
    RecoveryRecommendation,
)


@dataclass
class InMemoryOperationsBoardRepository:
    board_states: dict[UUID, OperationsBoardState] = field(default_factory=dict)
    receipts: dict[UUID, OperationsReceipt] = field(default_factory=dict)
    manual_blockers: list[BlockerSummary] = field(default_factory=list)
    manual_recommendations: list[RecoveryRecommendation] = field(default_factory=list)
    events: list[OperationsDomainEvent] = field(default_factory=list)
    idempotency_index: dict[str, UUID] = field(default_factory=dict)

    def put_state(self, state: OperationsBoardState, *, idempotency_key: str | None = None) -> OperationsBoardState:
        self.board_states[state.board_state_id] = state
        if idempotency_key:
            self.idempotency_index[idempotency_key] = state.board_state_id
        return state

    def state_for_idempotency(self, idempotency_key: str) -> OperationsBoardState | None:
        state_id = self.idempotency_index.get(idempotency_key)
        return self.board_states.get(state_id) if state_id else None

    def put_receipt(self, receipt: OperationsReceipt) -> OperationsReceipt:
        self.receipts[receipt.operations_receipt_id] = receipt
        return receipt

    def add_blocker(self, blocker: BlockerSummary) -> BlockerSummary:
        self.manual_blockers.append(blocker)
        return blocker

    def add_recommendation(self, recommendation: RecoveryRecommendation) -> RecoveryRecommendation:
        self.manual_recommendations.append(recommendation)
        return recommendation

    def append_event(self, event: OperationsDomainEvent) -> OperationsDomainEvent:
        self.events.append(event)
        return event
