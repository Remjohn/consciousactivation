"""Brand Genesis repositories for TS-CMF-018."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.brand_genesis import (
    BrandGenesisMissingEvidenceReport,
    BrandGenesisSession,
    BrandGenesisWorkflowRun,
    GenesisStartReceipt,
)


@dataclass
class InMemoryBrandGenesisRepository:
    sessions: dict[UUID, BrandGenesisSession] = field(default_factory=dict)
    missing_evidence_reports: dict[UUID, BrandGenesisMissingEvidenceReport] = field(default_factory=dict)
    start_receipts: dict[UUID, GenesisStartReceipt] = field(default_factory=dict)
    workflow_runs: dict[UUID, BrandGenesisWorkflowRun] = field(default_factory=dict)

    def put_session(self, session: BrandGenesisSession) -> BrandGenesisSession:
        self.sessions[session.brand_genesis_session_id] = session
        return session

    def get_session(self, session_id: UUID) -> BrandGenesisSession | None:
        return self.sessions.get(session_id)

    def get_session_for_brand(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        session_id: UUID,
    ) -> BrandGenesisSession | None:
        session = self.sessions.get(session_id)
        if session is None:
            return None
        if session.organization_id != organization_id or session.brand_id != brand_id:
            return None
        return session

    def list_sessions_for_brand(self, *, organization_id: UUID, brand_id: UUID) -> list[BrandGenesisSession]:
        return [
            session
            for session in self.sessions.values()
            if session.organization_id == organization_id and session.brand_id == brand_id
        ]

    def put_missing_evidence_report(self, report: BrandGenesisMissingEvidenceReport) -> BrandGenesisMissingEvidenceReport:
        self.missing_evidence_reports[report.brand_genesis_session_id] = report
        return report

    def put_start_receipt(self, receipt: GenesisStartReceipt) -> GenesisStartReceipt:
        self.start_receipts[receipt.genesis_start_receipt_id] = receipt
        return receipt

    def latest_start_receipt(self, session_id: UUID) -> GenesisStartReceipt | None:
        matching = [
            receipt for receipt in self.start_receipts.values() if receipt.brand_genesis_session_id == session_id
        ]
        if not matching:
            return None
        return max(matching, key=lambda receipt: receipt.written_at)

    def put_workflow_run(self, run: BrandGenesisWorkflowRun) -> BrandGenesisWorkflowRun:
        self.workflow_runs[run.workflow_run_id] = run
        return run
