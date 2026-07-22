"""Production Brand Context gate repository for TS-CMF-022."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.brand_context_gate import (
    BrandContextGateReceipt,
    BrandContextGateResult,
    BrandContextLineageView,
    ProviderBrandContextReceipt,
    SceneSpecBrandContextBinding,
    SupersededContextDecision,
)


@dataclass
class InMemoryBrandContextGateRepository:
    gate_results: dict[UUID, BrandContextGateResult] = field(default_factory=dict)
    scene_bindings: dict[UUID, SceneSpecBrandContextBinding] = field(default_factory=dict)
    superseded_decisions: dict[UUID, SupersededContextDecision] = field(default_factory=dict)
    provider_receipts: dict[UUID, ProviderBrandContextReceipt] = field(default_factory=dict)
    lineage_views: dict[UUID, BrandContextLineageView] = field(default_factory=dict)
    receipts: dict[UUID, BrandContextGateReceipt] = field(default_factory=dict)

    def put_gate_result(self, result: BrandContextGateResult) -> BrandContextGateResult:
        self.gate_results[result.brand_context_gate_result_id] = result
        return result

    def put_scene_binding(self, binding: SceneSpecBrandContextBinding) -> SceneSpecBrandContextBinding:
        self.scene_bindings[binding.scene_spec_id] = binding
        return binding

    def put_superseded_decision(self, decision: SupersededContextDecision) -> SupersededContextDecision:
        self.superseded_decisions[decision.superseded_context_decision_id] = decision
        return decision

    def put_provider_receipt(self, receipt: ProviderBrandContextReceipt) -> ProviderBrandContextReceipt:
        self.provider_receipts[receipt.provider_brand_context_receipt_id] = receipt
        return receipt

    def put_lineage_view(self, view: BrandContextLineageView) -> BrandContextLineageView:
        self.lineage_views[view.brand_context_lineage_view_id] = view
        return view

    def put_receipt(self, receipt: BrandContextGateReceipt) -> BrandContextGateReceipt:
        self.receipts[receipt.brand_context_gate_receipt_id] = receipt
        return receipt
