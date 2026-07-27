from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    AvatarFormatUse,
    AvatarHybridDesignSpec,
    AvatarIdentityProfile,
    AvatarPerformancePlan,
    AvatarPerformanceState,
    BodyPoseName,
    ExpressionPlateName,
    GestureClipType,
)
from ccp_studio.services.avatar_body_rig_service import AvatarBodyRigService
from ccp_studio.services.avatar_clip_library_service import AvatarClipLibraryService
from ccp_studio.services.avatar_face_plate_service import AvatarFacePlateService


class AvatarPerformanceLayerService:
    def __init__(self):
        self.face_plates = AvatarFacePlateService()
        self.body_rig = AvatarBodyRigService()
        self.clips = AvatarClipLibraryService()

    def create_avatar_identity_profile(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        avatar_id: str,
        display_name: str,
        identity_pack_ref: str | None = None,
        visual_dna_ref: str | None = None,
    ) -> AvatarIdentityProfile:
        return AvatarIdentityProfile(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            avatar_id=avatar_id,
            display_name=display_name,
            identity_pack_ref=identity_pack_ref,
            visual_dna_ref=visual_dna_ref,
        )

    def compile_hybrid_design_spec(self, avatar_id: str) -> AvatarHybridDesignSpec:
        return AvatarHybridDesignSpec(avatar_id=avatar_id)

    def compile_foundation_library(self, avatar_id: str) -> dict:
        face_set = self.face_plates.create_canonical_face_plate_set(avatar_id)
        layer_graph = self.body_rig.create_default_layer_graph(avatar_id)
        rig = self.body_rig.create_default_body_rig_manifest(avatar_id, layer_graph.avatar_layer_graph_id)
        pose_library = self.body_rig.create_canonical_pose_library(avatar_id)
        gesture_library = self.clips.create_canonical_gesture_clip_library(avatar_id)
        acting_library = self.clips.create_64_state_acting_library(avatar_id)
        return {
            "face_plate_set": face_set,
            "layer_graph": layer_graph,
            "body_rig_manifest": rig,
            "pose_library": pose_library,
            "gesture_library": gesture_library,
            "acting_library": acting_library,
        }

    def compile_performance_plan(
        self,
        *,
        avatar_id: str,
        scene_id: str,
        format_use: AvatarFormatUse = AvatarFormatUse.FORMAT_02,
        expression_name: ExpressionPlateName = ExpressionPlateName.CURIOUS_THINKING,
        body_pose_name: BodyPoseName = BodyPoseName.POINT_TO_CARD,
        gesture_clip_id: str | None = None,
        primitive_function: str = "clarity",
        sfl_function: str = "focus_target",
        start_ms: int = 0,
        end_ms: int = 900,
    ) -> AvatarPerformancePlan:
        state = AvatarPerformanceState(
            start_ms=start_ms,
            end_ms=end_ms,
            expression_name=expression_name,
            body_pose_name=body_pose_name,
            gesture_clip_id=gesture_clip_id,
            primitive_function=primitive_function,
            sfl_function=sfl_function,
        )
        return AvatarPerformancePlan(
            avatar_id=avatar_id,
            scene_id=scene_id,
            format_use=format_use,
            performance_states=[state],
            lip_sync_enabled=False,
        )
