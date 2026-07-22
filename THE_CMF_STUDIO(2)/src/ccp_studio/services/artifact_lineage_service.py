from __future__ import annotations

from ccp_studio.contracts.project_workspace_artifact_store import (
    ArtifactLineage,
    ArtifactReceipt,
    LineageRelation,
    PassStatus,
)
from ccp_studio.repositories.project_workspace_artifact_store import InMemoryProjectWorkspaceArtifactStoreRepository


class ArtifactLineageService:
    def __init__(self, repository: InMemoryProjectWorkspaceArtifactStoreRepository | None = None):
        self.repository = repository or InMemoryProjectWorkspaceArtifactStoreRepository()

    def record_lineage(
        self,
        *,
        source_artifact_ref_ids: list[str],
        derived_artifact_ref_id: str,
        relation: LineageRelation,
        operation: str,
        tool_or_service: str | None = None,
        source_receipt_refs: list[str] | None = None,
    ) -> ArtifactLineage:
        lineage = ArtifactLineage(
            source_artifact_ref_ids=source_artifact_ref_ids,
            derived_artifact_ref_id=derived_artifact_ref_id,
            relation=relation,
            operation=operation,
            tool_or_service=tool_or_service,
            source_receipt_refs=source_receipt_refs or [],
        )
        self.repository.upsert("lineages", lineage.artifact_lineage_id, lineage)
        return lineage

    def record_receipt(
        self,
        *,
        artifact_ref_id: str,
        receipt_type: str,
        pass_status: PassStatus,
        checks: dict | None = None,
        blockers: list[str] | None = None,
    ) -> ArtifactReceipt:
        receipt = ArtifactReceipt(
            artifact_ref_id=artifact_ref_id,
            receipt_type=receipt_type,
            pass_status=pass_status,
            checks=checks or {},
            blockers=blockers or [],
        )
        self.repository.upsert("receipts", receipt.artifact_receipt_id, receipt)
        return receipt
