from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    AudienceProxyPersona,
    AvatarFormatUse,
    BodyPoseName,
    ExpressionPlateName,
)
from ccp_studio.contracts.format02_composition_intelligence import Format02SceneProgram, Format02SceneRole
from ccp_studio.services.audience_proxy_service import AudienceProxyService
from ccp_studio.services.avatar_performance_service import AvatarPerformanceLayerService


class Format02AvatarPerformanceAdapterService:
    def __init__(
        self,
        avatar_service: AvatarPerformanceLayerService | None = None,
        proxy_service: AudienceProxyService | None = None,
    ):
        self.avatar_service = avatar_service or AvatarPerformanceLayerService()
        self.proxy_service = proxy_service or AudienceProxyService()

    def compile_from_format02_scene(
        self,
        scene: Format02SceneProgram,
        *,
        avatar_id: str = "coach_avatar_v1",
    ):
        expression, pose = self._state_for_scene(scene.scene_role)
        avatar_plan = self.avatar_service.compile_performance_plan(
            avatar_id=avatar_id,
            scene_id=scene.scene_id,
            format_use=AvatarFormatUse.FORMAT_02,
            expression_name=expression,
            body_pose_name=pose,
            primitive_function=scene.visual_action.primitive_function,
            sfl_function=scene.visual_action.sfl_function,
        )
        proxy_plan = None
        if scene.composition_scene_program and scene.composition_scene_program.audience_proxy_placement_plan:
            proxy = scene.composition_scene_program.audience_proxy_placement_plan
            proxy_plan = self.proxy_service.compile_performance_plan(
                scene_id=scene.scene_id,
                persona=AudienceProxyPersona(proxy.persona.value),
                state_name=scene.scene_role.value,
                primitive_function=proxy.primitive_function or "audience_mirror",
                sfl_function=proxy.sfl_function,
            )
        return avatar_plan, proxy_plan

    def _state_for_scene(self, scene_role: Format02SceneRole):
        mapping = {
            Format02SceneRole.MYTH_SETUP: (ExpressionPlateName.CURIOUS_THINKING, BodyPoseName.POINT_UP),
            Format02SceneRole.TRUTH_DEFINE: (ExpressionPlateName.SERIOUS_TRUTH, BodyPoseName.OPEN_PALM_REVEAL),
            Format02SceneRole.PROOF_CONTRAST: (ExpressionPlateName.SKEPTICAL_BROW, BodyPoseName.POINT_TO_CARD),
            Format02SceneRole.BETTER_FRAME: (ExpressionPlateName.CURIOUS_THINKING, BodyPoseName.THINKING_CHIN),
            Format02SceneRole.DOSE_CONTRAST: (ExpressionPlateName.PLAYFUL_WARNING, BodyPoseName.SOFT_SHRUG),
            Format02SceneRole.PROCESS_STEP: (ExpressionPlateName.ENCOURAGING_CLOSE, BodyPoseName.PRESENT_DIAGRAM),
            Format02SceneRole.REFRAME: (ExpressionPlateName.GENTLE_SMILE, BodyPoseName.OPEN_PALM_REVEAL),
            Format02SceneRole.TAKEAWAY: (ExpressionPlateName.ENCOURAGING_CLOSE, BodyPoseName.HOLD_CUP),
        }
        return mapping[scene_role]
