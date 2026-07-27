"""Research repositories for TS-CMF-023."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.research import ResearchEvidence, ResearchEvidenceReceipt, ResearchField, ResearchSnapshot


@dataclass
class InMemoryResearchRepository:
    fields: dict[UUID, ResearchField] = field(default_factory=dict)
    evidence: dict[UUID, ResearchEvidence] = field(default_factory=dict)
    receipts: dict[UUID, ResearchEvidenceReceipt] = field(default_factory=dict)
    snapshots: dict[UUID, ResearchSnapshot] = field(default_factory=dict)

    def put_field(self, research_field: ResearchField) -> ResearchField:
        self.fields[research_field.research_field_id] = research_field
        return research_field

    def put_evidence(self, evidence: ResearchEvidence) -> ResearchEvidence:
        self.evidence[evidence.evidence_id] = evidence
        return evidence

    def put_receipt(self, receipt: ResearchEvidenceReceipt) -> ResearchEvidenceReceipt:
        self.receipts[receipt.research_evidence_receipt_id] = receipt
        return receipt

    def put_snapshot(self, snapshot: ResearchSnapshot) -> ResearchSnapshot:
        self.snapshots[snapshot.research_snapshot_id] = snapshot
        return snapshot

    def evidence_for_field(self, research_field_id: UUID) -> list[ResearchEvidence]:
        return [item for item in self.evidence.values() if item.research_field_id == research_field_id]
