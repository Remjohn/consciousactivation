from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import (
    AudienceProxyPersona,
    AudienceProxyPlacementPlan,
    AvatarPlacementPlan,
    CognitiveLoadBudget,
    CompositionRole,
    CompositionSceneProgram,
    FrameFormatProfile,
    RealLifeCutoutPlacementPlan,
    SafeZonePlan,
)
from ccp_studio.contracts.format02_composition_intelligence import (
    Format02AvatarActionRequirement,
    Format02ConceptMotionBudget,
    Format02ConceptUnit,
    Format02PaperCardLayout,
    Format02SceneProgram,
    Format02SceneRole,
    Format02VisualAction,
    Format02VisualActionType,
)
from ccp_studio.services.attention_path_service import AttentionPathService
from ccp_studio.services.composition_intelligence_service import CompositionIntelligenceService
from ccp_studio.services.composition_template_service import CompositionTemplateService
from ccp_studio.services.text_placement_service import TextPlacementService


class Format02CompositionService:
    def __init__(self):
        self.core = CompositionIntelligenceService()
        self.templates = CompositionTemplateService()
        self.text = TextPlacementService()
        self.attention = AttentionPathService()

    def compile_scene_program(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        source_span_refs: list[str],
        scene_id: str,
        scene_role: Format02SceneRole,
        concept_statement: str,
        headline_text: str,
        format_program_id: str | None = None,
        avatar_ref: str = "coach_avatar_v1",
        avatar_action_ref: str = "avatar_action_001",
        avatar_pose_hint: str = "point_to_card",
        avatar_expression_hint: str = "curious_thinking",
        audience_proxy: AudienceProxyPersona | None = AudienceProxyPersona.CONFUSED_SEEKER,
        audience_proxy_sfl_function: str = "relevant_open_question",
        hero_object_asset_id: str | None = "hero_object_001",
        hero_object_source_ref: str | None = "visual_research_ref_001",
        hero_object_role: CompositionRole = CompositionRole.HERO_OBJECT,
        negative_space_ratio: float = 0.35,
        support_labels: list[str] | None = None,
    ) -> Format02SceneProgram:
        context = self.core.hydrate_context(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            format_program_id=format_program_id,
            format_id="format_02_avatar_papercut_explainer",
            sub_format_id="paper_cut_explainer",
            source_span_refs=source_span_refs,
            frame_profile=FrameFormatProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
        )
        concept = Format02ConceptUnit(concept_statement=concept_statement, source_span_refs=source_span_refs)
        visual_action = Format02VisualAction(
            action_type=self._visual_action_for_scene(scene_role),
            concept_unit_id=concept.concept_unit_id,
            sfl_function=audience_proxy_sfl_function or "concept_reveal",
            primitive_function="clarity",
        )
        motion_budget = Format02ConceptMotionBudget(
            concept_unit_id=concept.concept_unit_id,
            primary_visual_actions=[visual_action.visual_action_id],
        )
        avatar_requirement = Format02AvatarActionRequirement(
            action_ref=avatar_action_ref,
            pose_hint=avatar_pose_hint,
            expression_hint=avatar_expression_hint,
        )
        avatar_plan = AvatarPlacementPlan(
            avatar_ref=avatar_ref,
            placement="right_third",
            action_ref=avatar_action_ref,
            action_serves_concept=True,
        )
        proxy_plan = None
        proxy_req = None
        proxy_ref = None
        if audience_proxy:
            proxy_plan = AudienceProxyPlacementPlan(
                persona=audience_proxy,
                placement="lower_left",
                sfl_function=audience_proxy_sfl_function,
                primitive_function="audience_mirror",
            )
            proxy_req = None
            proxy_ref = proxy_plan.audience_proxy_placement_plan_id

        cutout_plan = None
        object_refs = []
        cutout_reqs = []
        if hero_object_asset_id and hero_object_source_ref:
            cutout_plan = RealLifeCutoutPlacementPlan(
                asset_id=hero_object_asset_id,
                source_ref=hero_object_source_ref,
                role=hero_object_role,
                placement="left_or_center_hero",
            )
            object_refs.append(cutout_plan.real_life_cutout_placement_plan_id)

        text_plan = self.text.compile_text_plan(
            headline_text=headline_text,
            support_labels=support_labels or [],
            max_visible_words=14,
        )
        text_reveal = self.text.compile_reveal_policy([text_plan.text_placement_plan_id])
        attention = self.attention.compile_default_format02_path(
            headline_ref=text_plan.text_placement_plan_id,
            avatar_ref=avatar_plan.avatar_placement_plan_id,
            object_ref=object_refs[0] if object_refs else None,
            proxy_ref=proxy_ref,
        )
        layer_plan, layer_manifest = self.core.compile_layer_plan(
            text_ref=text_plan.text_placement_plan_id,
            avatar_ref=avatar_plan.avatar_placement_plan_id,
            object_refs=object_refs,
            proxy_ref=proxy_ref,
        )
        template = self.templates.get_format02_template()
        scene_program = CompositionSceneProgram(
            context_id=context.composition_context_id,
            scene_id=scene_id,
            scene_role=scene_role.value,
            concept_statement=concept_statement,
            composition_template_id=template.composition_template_id,
            cognitive_load_budget=CognitiveLoadBudget(minimum_negative_space_ratio=0.30),
            attention_path_plan=attention,
            safe_zone_plan=SafeZonePlan(frame_profile=FrameFormatProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER),
            text_placement_plan=text_plan,
            text_reveal_policy=text_reveal,
            avatar_placement_plan=avatar_plan,
            audience_proxy_placement_plan=proxy_plan,
            real_life_cutout_plans=[cutout_plan] if cutout_plan else [],
            layer_plan=layer_plan,
            layer_manifest=layer_manifest,
        )
        return Format02SceneProgram(
            scene_id=scene_id,
            scene_role=scene_role,
            concept_unit=concept,
            visual_action=visual_action,
            motion_budget=motion_budget,
            avatar_requirement=avatar_requirement,
            audience_proxy_requirement=proxy_req,
            real_life_cutout_requirements=cutout_reqs,
            paper_card_layout=Format02PaperCardLayout(
                headline_card_position="upper_card",
                avatar_position="right_third",
                object_position="left_or_center_hero" if object_refs else None,
                proxy_position="lower_left" if proxy_ref else None,
                negative_space_ratio=negative_space_ratio,
            ),
            composition_scene_program=scene_program,
        )

    def _visual_action_for_scene(self, scene_role: Format02SceneRole) -> Format02VisualActionType:
        mapping = {
            Format02SceneRole.MYTH_SETUP: Format02VisualActionType.PAPER_STRIP_DROP,
            Format02SceneRole.TRUTH_DEFINE: Format02VisualActionType.CARD_SLIDE_IN,
            Format02SceneRole.PROOF_CONTRAST: Format02VisualActionType.PROOF_CARD_STAMP,
            Format02SceneRole.BETTER_FRAME: Format02VisualActionType.COMPASS_NEEDLE_ROTATE,
            Format02SceneRole.DOSE_CONTRAST: Format02VisualActionType.RAIN_SUN_CONTRAST,
            Format02SceneRole.PROCESS_STEP: Format02VisualActionType.CHECKLIST_STAMP,
            Format02SceneRole.REFRAME: Format02VisualActionType.SEEDLING_GROW,
            Format02SceneRole.TAKEAWAY: Format02VisualActionType.SOFT_PUSH_IN,
        }
        return mapping[scene_role]
