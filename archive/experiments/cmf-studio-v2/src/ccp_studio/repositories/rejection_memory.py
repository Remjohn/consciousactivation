"""Rejection memory repositories for TS-CMF-035."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.rejection_memory import (
    CoalitionFatalityRecord,
    MemoryAdmissionCandidate,
    NegativeEvidenceRef,
    RejectedExpressionCandidate,
    RejectedRouteAttempt,
    RejectionReceipt,
)


@dataclass
class InMemoryRejectionMemoryRepository:
    rejected_candidates: dict[UUID, RejectedExpressionCandidate] = field(default_factory=dict)
    rejected_routes: dict[UUID, RejectedRouteAttempt] = field(default_factory=dict)
    coalition_fatalities: dict[UUID, CoalitionFatalityRecord] = field(default_factory=dict)
    negative_evidence_refs: dict[UUID, NegativeEvidenceRef] = field(default_factory=dict)
    memory_admission_candidates: dict[UUID, MemoryAdmissionCandidate] = field(default_factory=dict)
    receipts: dict[UUID, RejectionReceipt] = field(default_factory=dict)

    def put_rejected_candidate(self, record: RejectedExpressionCandidate) -> RejectedExpressionCandidate:
        self.rejected_candidates[record.rejected_candidate_id] = record
        return record

    def put_rejected_route(self, record: RejectedRouteAttempt) -> RejectedRouteAttempt:
        self.rejected_routes[record.rejected_route_attempt_id] = record
        return record

    def put_coalition_fatality(self, record: CoalitionFatalityRecord) -> CoalitionFatalityRecord:
        self.coalition_fatalities[record.coalition_fatality_id] = record
        return record

    def put_negative_evidence_ref(self, ref: NegativeEvidenceRef) -> NegativeEvidenceRef:
        self.negative_evidence_refs[ref.negative_evidence_ref_id] = ref
        return ref

    def put_memory_admission_candidate(self, candidate: MemoryAdmissionCandidate) -> MemoryAdmissionCandidate:
        self.memory_admission_candidates[candidate.memory_admission_candidate_id] = candidate
        return candidate

    def put_receipt(self, receipt: RejectionReceipt) -> RejectionReceipt:
        self.receipts[receipt.rejection_receipt_id] = receipt
        return receipt
