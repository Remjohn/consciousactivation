"""Memory admission repositories for TS-CMF-056."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.memory_admission import (
    MemoryAdmissionCandidate,
    MemoryAdmissionDomainEvent,
    MemoryAdmissionReceipt,
    MemoryEvent,
    MemoryUsageCitation,
)


@dataclass
class InMemoryMemoryAdmissionRepository:
    candidates: dict[UUID, MemoryAdmissionCandidate] = field(default_factory=dict)
    memory_events: dict[UUID, MemoryEvent] = field(default_factory=dict)
    receipts: dict[UUID, MemoryAdmissionReceipt] = field(default_factory=dict)
    usage_citations: dict[UUID, MemoryUsageCitation] = field(default_factory=dict)
    events: list[MemoryAdmissionDomainEvent] = field(default_factory=list)
    candidate_idempotency_index: dict[tuple[UUID, UUID, str], UUID] = field(default_factory=dict)
    receipt_idempotency_index: dict[tuple[UUID, str, str], UUID] = field(default_factory=dict)
    citation_idempotency_index: dict[tuple[UUID, str, str], UUID] = field(default_factory=dict)

    def put_candidate(
        self,
        candidate: MemoryAdmissionCandidate,
        *,
        idempotency_key: str | None = None,
    ) -> MemoryAdmissionCandidate:
        self.candidates[candidate.candidate_id] = candidate
        if idempotency_key:
            self.candidate_idempotency_index[(candidate.organization_id, candidate.brand_id, idempotency_key)] = candidate.candidate_id
        return candidate

    def candidate_for_idempotency(self, organization_id: UUID, brand_id: UUID, idempotency_key: str) -> MemoryAdmissionCandidate | None:
        candidate_id = self.candidate_idempotency_index.get((organization_id, brand_id, idempotency_key))
        return self.candidates.get(candidate_id) if candidate_id else None

    def put_memory_event(self, event: MemoryEvent) -> MemoryEvent:
        self.memory_events[event.memory_event_id] = event
        return event

    def put_receipt(
        self,
        receipt: MemoryAdmissionReceipt,
        *,
        action: str | None = None,
        idempotency_key: str | None = None,
    ) -> MemoryAdmissionReceipt:
        self.receipts[receipt.memory_admission_receipt_id] = receipt
        if action and idempotency_key:
            self.receipt_idempotency_index[(receipt.candidate_id, action, idempotency_key)] = receipt.memory_admission_receipt_id
        return receipt

    def receipt_for_idempotency(self, candidate_id: UUID, action: str, idempotency_key: str) -> MemoryAdmissionReceipt | None:
        receipt_id = self.receipt_idempotency_index.get((candidate_id, action, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

    def put_usage_citation(
        self,
        citation: MemoryUsageCitation,
        *,
        idempotency_key: str | None = None,
    ) -> MemoryUsageCitation:
        self.usage_citations[citation.memory_usage_citation_id] = citation
        if idempotency_key:
            self.citation_idempotency_index[(citation.memory_event_id, citation.compiler_or_agent, idempotency_key)] = citation.memory_usage_citation_id
        return citation

    def citation_for_idempotency(self, memory_event_id: UUID, compiler_or_agent: str, idempotency_key: str) -> MemoryUsageCitation | None:
        citation_id = self.citation_idempotency_index.get((memory_event_id, compiler_or_agent, idempotency_key))
        return self.usage_citations.get(citation_id) if citation_id else None

    def append_event(self, event: MemoryAdmissionDomainEvent) -> MemoryAdmissionDomainEvent:
        self.events.append(event)
        return event
