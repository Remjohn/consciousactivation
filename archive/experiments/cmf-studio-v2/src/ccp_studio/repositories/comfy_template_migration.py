"""ComfyUI template migration repositories for TS-CMF-046."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.comfy_template_migration import MigratedComfyWorkflowAsset, TemplateMigrationReceipt


@dataclass
class InMemoryComfyTemplateMigrationRepository:
    assets: dict[UUID, MigratedComfyWorkflowAsset] = field(default_factory=dict)
    receipts: dict[UUID, TemplateMigrationReceipt] = field(default_factory=dict)

    def put_asset(self, asset: MigratedComfyWorkflowAsset) -> MigratedComfyWorkflowAsset:
        self.assets[asset.comfy_workflow_asset_id] = asset
        return asset

    def put_receipt(self, receipt: TemplateMigrationReceipt) -> TemplateMigrationReceipt:
        self.receipts[receipt.template_migration_receipt_id] = receipt
        return receipt
