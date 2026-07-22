"""Rig manifest repositories for TS-CMF-020."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.creative_libraries import CreativeItemStatus
from ccp_studio.contracts.rig_manifest import RigManifest, RigPreviewReceipt, RigValidationReport


@dataclass
class InMemoryRigManifestRepository:
    manifests: dict[UUID, RigManifest] = field(default_factory=dict)
    validation_reports: dict[UUID, RigValidationReport] = field(default_factory=dict)
    preview_receipts: dict[UUID, RigPreviewReceipt] = field(default_factory=dict)

    def put_manifest(self, manifest: RigManifest) -> RigManifest:
        existing = self.manifests.get(manifest.rig_manifest_id)
        if existing and existing.status == CreativeItemStatus.locked and existing != manifest:
            raise ValueError("locked rig manifest is immutable")
        self.manifests[manifest.rig_manifest_id] = manifest
        return manifest

    def put_validation_report(self, report: RigValidationReport) -> RigValidationReport:
        self.validation_reports[report.rig_manifest_id] = report
        return report

    def put_preview_receipt(self, receipt: RigPreviewReceipt) -> RigPreviewReceipt:
        self.preview_receipts[receipt.rig_preview_receipt_id] = receipt
        return receipt

    def manifests_for_brand(self, organization_id: UUID, brand_id: UUID) -> list[RigManifest]:
        return [
            manifest
            for manifest in self.manifests.values()
            if manifest.organization_id == organization_id and manifest.brand_id == brand_id
        ]
