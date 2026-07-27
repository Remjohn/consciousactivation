"""Assembly planning repositories for TS-CMF-039."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.assembly import (
    AnimationPlan,
    AssemblyPlan,
    AssemblyPlanReceipt,
    AudioMixManifest,
    CaptionManifest,
    EditDecisionList,
    LayerManifest,
    TimelineManifest,
)


@dataclass
class InMemoryAssemblyRepository:
    layer_manifests: dict[UUID, LayerManifest] = field(default_factory=dict)
    animation_plans: dict[UUID, AnimationPlan] = field(default_factory=dict)
    edit_decision_lists: dict[UUID, EditDecisionList] = field(default_factory=dict)
    timeline_manifests: dict[UUID, TimelineManifest] = field(default_factory=dict)
    caption_manifests: dict[UUID, CaptionManifest] = field(default_factory=dict)
    audio_mix_manifests: dict[UUID, AudioMixManifest] = field(default_factory=dict)
    assembly_plans: dict[UUID, AssemblyPlan] = field(default_factory=dict)
    receipts: dict[UUID, AssemblyPlanReceipt] = field(default_factory=dict)

    def put_layer_manifest(self, manifest: LayerManifest) -> LayerManifest:
        self.layer_manifests[manifest.layer_manifest_id] = manifest
        return manifest

    def put_animation_plan(self, plan: AnimationPlan) -> AnimationPlan:
        self.animation_plans[plan.animation_plan_id] = plan
        return plan

    def put_edit_decision_list(self, edl: EditDecisionList) -> EditDecisionList:
        self.edit_decision_lists[edl.edit_decision_list_id] = edl
        return edl

    def put_timeline_manifest(self, manifest: TimelineManifest) -> TimelineManifest:
        self.timeline_manifests[manifest.timeline_manifest_id] = manifest
        return manifest

    def put_caption_manifest(self, manifest: CaptionManifest) -> CaptionManifest:
        self.caption_manifests[manifest.caption_manifest_id] = manifest
        return manifest

    def put_audio_mix_manifest(self, manifest: AudioMixManifest) -> AudioMixManifest:
        self.audio_mix_manifests[manifest.audio_mix_manifest_id] = manifest
        return manifest

    def put_assembly_plan(self, plan: AssemblyPlan) -> AssemblyPlan:
        self.assembly_plans[plan.assembly_plan_id] = plan
        return plan

    def put_receipt(self, receipt: AssemblyPlanReceipt) -> AssemblyPlanReceipt:
        self.receipts[receipt.assembly_plan_receipt_id] = receipt
        return receipt
