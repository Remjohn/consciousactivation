from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import (
    AudienceProxyPlacementPlan,
    CognitiveLoadBudget,
    CompositionDecisionReceipt,
    CompositionIntelligenceContext,
    CompositionRole,
    CompositionSceneProgram,
    CompositionStatus,
    FrameFormatProfile,
    LayerManifest,
    LayerPlan,
    LayerSpec,
    LockedCompositionElements,
    PassStatus,
    SafeZonePlan,
)
from ccp_studio.services.attention_path_service import AttentionPathService
from ccp_studio.services.cognitive_load_gate_service import CognitiveLoadGateService
from ccp_studio.services.composition_template_service import CompositionTemplateService
from ccp_studio.services.text_placement_service import TextPlacementService


class CompositionIntelligenceService:
    def __init__(self):
        self.templates = CompositionTemplateService()
        self.text = TextPlacementService()
        self.attention = AttentionPathService()
        self.cognitive = CognitiveLoadGateService()

    def hydrate_context(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        format_id: str,
        source_span_refs: list[str],
        format_program_id: str | None = None,
        sub_format_id: str | None = None,
        frame_profile: FrameFormatProfile = FrameFormatProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
    ) -> CompositionIntelligenceContext:
        return CompositionIntelligenceContext(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            format_program_id=format_program_id,
            format_id=format_id,
            sub_format_id=sub_format_id,
            source_span_refs=source_span_refs,
            frame_profile=frame_profile,
        )

    def compile_layer_plan(
        self,
        *,
        text_ref: str,
        avatar_ref: str | None = None,
        object_refs: list[str] | None = None,
        proxy_ref: str | None = None,
    ) -> tuple[LayerPlan, LayerManifest]:
        layers = [LayerSpec(layer_role=CompositionRole.BACKGROUND, z_index=1, ref_id="paper_background")]
        z = 2
        for object_ref in object_refs or []:
            layers.append(LayerSpec(layer_role=CompositionRole.HERO_OBJECT, z_index=z, ref_id=object_ref))
            z += 1
        if avatar_ref:
            layers.append(LayerSpec(layer_role=CompositionRole.AVATAR, z_index=z, ref_id=avatar_ref))
            z += 1
        if proxy_ref:
            layers.append(LayerSpec(layer_role=CompositionRole.AUDIENCE_PROXY, z_index=z, ref_id=proxy_ref))
            z += 1
        layers.append(LayerSpec(layer_role=CompositionRole.TEXT_ANCHOR, z_index=z, ref_id=text_ref))
        plan = LayerPlan(layers=layers)
        manifest = LayerManifest(layer_plan_id=plan.layer_plan_id, locked_layer_ids=[layer.layer_id for layer in layers])
        return plan, manifest

    def make_locked_elements(
        self,
        *,
        text_refs: list[str],
        layout_refs: list[str],
        avatar_refs: list[str] | None = None,
        source_refs: list[str] | None = None,
    ) -> LockedCompositionElements:
        return LockedCompositionElements(
            locked_text=text_refs,
            locked_layout_refs=layout_refs,
            locked_avatar_refs=avatar_refs or [],
            locked_source_refs=source_refs or [],
            locked_negative_space=True,
        )

    def compile_decision_receipt(
        self,
        scene_program: CompositionSceneProgram,
        *,
        visible_words: int,
        headline_words: int,
        support_labels: int,
        audience_proxies: int,
        hero_real_life_objects: int,
        support_real_life_objects: int,
        diagram_nodes: int,
        simultaneous_motion_events: int,
        negative_space_ratio: float,
    ) -> tuple[CompositionDecisionReceipt, object]:
        report = self.cognitive.evaluate(
            scene_program.cognitive_load_budget,
            visible_words=visible_words,
            headline_words=headline_words,
            support_labels=support_labels,
            audience_proxies=audience_proxies,
            hero_real_life_objects=hero_real_life_objects,
            support_real_life_objects=support_real_life_objects,
            diagram_nodes=diagram_nodes,
            simultaneous_motion_events=simultaneous_motion_events,
            negative_space_ratio=negative_space_ratio,
        )
        receipt = CompositionDecisionReceipt(
            composition_scene_program_id=scene_program.composition_scene_program_id,
            pass_status=report.pass_status,
            cognitive_load_report_id=report.cognitive_load_report_id,
            locked=report.pass_status == PassStatus.PASS,
            blockers=report.blockers,
        )
        scene_program.status = CompositionStatus.LOCKED if receipt.locked else CompositionStatus.BLOCKED
        return receipt, report
