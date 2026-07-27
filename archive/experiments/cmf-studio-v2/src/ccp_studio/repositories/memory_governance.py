"""Memory governance repositories for TS-CMF-057."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.memory_governance import (
    MemoryGovernanceAction,
    MemoryGovernanceDomainEvent,
    MemoryGovernanceEvent,
    MemoryGovernanceReceipt,
    MemoryProjectionUpdateEvent,
)


@dataclass
class InMemoryMemoryGovernanceRepository:
    actions: dict[UUID, MemoryGovernanceAction] = field(default_factory=dict)
    governance_events: dict[UUID, MemoryGovernanceEvent] = field(default_factory=dict)
    receipts: dict[UUID, MemoryGovernanceReceipt] = field(default_factory=dict)
    projection_events: dict[UUID, MemoryProjectionUpdateEvent] = field(default_factory=dict)
    events: list[MemoryGovernanceDomainEvent] = field(default_factory=list)
    idempotency_index: dict[tuple[UUID, str, str], UUID] = field(default_factory=dict)

    def put_action(self, action: MemoryGovernanceAction) -> MemoryGovernanceAction:
        self.actions[action.action_id] = action
        return action

    def put_governance_event(self, event: MemoryGovernanceEvent) -> MemoryGovernanceEvent:
        self.governance_events[event.event_id] = event
        return event

    def put_projection_event(self, event: MemoryProjectionUpdateEvent) -> MemoryProjectionUpdateEvent:
        self.projection_events[event.projection_event_id] = event
        return event

    def put_receipt(
        self,
        receipt: MemoryGovernanceReceipt,
        *,
        idempotency_key: str | None = None,
    ) -> MemoryGovernanceReceipt:
        self.receipts[receipt.memory_governance_receipt_id] = receipt
        if idempotency_key:
            self.idempotency_index[(receipt.memory_event_id, receipt.action_type.value, idempotency_key)] = receipt.memory_governance_receipt_id
        return receipt

    def receipt_for_idempotency(self, memory_event_id: UUID, action_type: str, idempotency_key: str) -> MemoryGovernanceReceipt | None:
        receipt_id = self.idempotency_index.get((memory_event_id, action_type, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

    def append_event(self, event: MemoryGovernanceDomainEvent) -> MemoryGovernanceDomainEvent:
        self.events.append(event)
        return event

    def history_for_memory(self, memory_event_id: UUID) -> list[MemoryGovernanceEvent]:
        events = [
            event for event in self.governance_events.values()
            if event.memory_event_id == memory_event_id
        ]
        return sorted(events, key=lambda item: item.created_at)
