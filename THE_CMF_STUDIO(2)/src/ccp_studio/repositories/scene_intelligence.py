"""Scene intelligence repositories for TS-CMF-041."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.scene_intelligence import (
    AssetRollPlan,
    CreativeSubsystemDecision,
    SceneComponentSelection,
    SceneContainerPlan,
    SceneIntelligenceAuditView,
    SceneIntelligenceReceipt,
)


@dataclass
class InMemorySceneIntelligenceRepository:
    container_plans: dict[UUID, SceneContainerPlan] = field(default_factory=dict)
    component_selections: dict[UUID, SceneComponentSelection] = field(default_factory=dict)
    subsystem_decisions: dict[UUID, CreativeSubsystemDecision] = field(default_factory=dict)
    asset_roll_plans: dict[UUID, AssetRollPlan] = field(default_factory=dict)
    audit_views: dict[UUID, SceneIntelligenceAuditView] = field(default_factory=dict)
    receipts: dict[UUID, SceneIntelligenceReceipt] = field(default_factory=dict)

    def put_container_plan(self, plan: SceneContainerPlan) -> SceneContainerPlan:
        self.container_plans[plan.scene_container_plan_id] = plan
        return plan

    def put_component_selection(self, selection: SceneComponentSelection) -> SceneComponentSelection:
        self.component_selections[selection.scene_component_selection_id] = selection
        return selection

    def put_subsystem_decision(self, decision: CreativeSubsystemDecision) -> CreativeSubsystemDecision:
        self.subsystem_decisions[decision.creative_subsystem_decision_id] = decision
        return decision

    def put_asset_roll_plan(self, plan: AssetRollPlan) -> AssetRollPlan:
        self.asset_roll_plans[plan.asset_roll_plan_id] = plan
        return plan

    def put_audit_view(self, view: SceneIntelligenceAuditView) -> SceneIntelligenceAuditView:
        self.audit_views[view.scene_spec_id] = view
        return view

    def put_receipt(self, receipt: SceneIntelligenceReceipt) -> SceneIntelligenceReceipt:
        self.receipts[receipt.scene_intelligence_receipt_id] = receipt
        return receipt
