"""SceneSpec repositories for TS-CMF-037."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.scene_spec import (
    AssetSelection,
    CreativeState,
    EvaluationRequirement,
    PlatformVariant,
    RenderContract,
    RevisionPolicy,
    SceneSpec,
    SceneSpecReceipt,
)


@dataclass
class InMemorySceneSpecRepository:
    scene_specs: dict[UUID, SceneSpec] = field(default_factory=dict)
    creative_states: dict[UUID, CreativeState] = field(default_factory=dict)
    render_contracts: dict[UUID, RenderContract] = field(default_factory=dict)
    asset_selections: dict[UUID, AssetSelection] = field(default_factory=dict)
    platform_variants: dict[UUID, PlatformVariant] = field(default_factory=dict)
    evaluation_requirements: dict[UUID, EvaluationRequirement] = field(default_factory=dict)
    revision_policies: dict[UUID, RevisionPolicy] = field(default_factory=dict)
    receipts: dict[UUID, SceneSpecReceipt] = field(default_factory=dict)

    def put_scene_spec(self, scene_spec: SceneSpec) -> SceneSpec:
        self.scene_specs[scene_spec.scene_spec_id] = scene_spec
        return scene_spec

    def put_creative_state(self, creative_state: CreativeState) -> CreativeState:
        self.creative_states[creative_state.creative_state_id] = creative_state
        return creative_state

    def put_render_contract(self, render_contract: RenderContract) -> RenderContract:
        self.render_contracts[render_contract.render_contract_id] = render_contract
        return render_contract

    def put_asset_selection(self, selection: AssetSelection) -> AssetSelection:
        self.asset_selections[selection.asset_selection_id] = selection
        return selection

    def put_platform_variant(self, variant: PlatformVariant) -> PlatformVariant:
        self.platform_variants[variant.platform_variant_id] = variant
        return variant

    def put_evaluation_requirement(self, requirement: EvaluationRequirement) -> EvaluationRequirement:
        self.evaluation_requirements[requirement.evaluation_requirement_id] = requirement
        return requirement

    def put_revision_policy(self, policy: RevisionPolicy) -> RevisionPolicy:
        self.revision_policies[policy.revision_policy_id] = policy
        return policy

    def put_receipt(self, receipt: SceneSpecReceipt) -> SceneSpecReceipt:
        self.receipts[receipt.scene_spec_receipt_id] = receipt
        return receipt
