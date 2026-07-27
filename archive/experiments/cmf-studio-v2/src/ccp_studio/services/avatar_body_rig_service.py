from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    AvatarBodyPose,
    AvatarBodyPoseLibrary,
    AvatarBodyRigManifest,
    AvatarLayer,
    AvatarLayerGraph,
    AvatarPivotMap,
    AvatarRigBone,
    BodyPoseName,
    RuntimeTarget,
)


class AvatarBodyRigService:
    def create_default_layer_graph(self, avatar_id: str) -> AvatarLayerGraph:
        roles = ["body", "torso", "left_arm", "right_arm", "left_hand", "right_hand", "neck", "head_anchor", "clothes"]
        layers = [
            AvatarLayer(layer_name=role, layer_role=role, source_ref=f"{avatar_id}_{role}", z_index=index)
            for index, role in enumerate(roles, start=1)
        ]
        return AvatarLayerGraph(avatar_id=avatar_id, layers=layers)

    def create_default_body_rig_manifest(self, avatar_id: str, layer_graph_id: str) -> AvatarBodyRigManifest:
        bone_names = ["torso", "neck", "head_anchor", "left_arm", "right_arm", "left_hand", "right_hand"]
        bones = [
            AvatarRigBone(
                bone_name=name,
                parent_bone_name="torso" if name not in {"torso", "neck"} else ("torso" if name == "neck" else None),
                pivot_x=0.5,
                pivot_y=0.5,
            )
            for name in bone_names
        ]
        pivot_map = AvatarPivotMap(pivot_by_layer={name: (0.5, 0.5) for name in bone_names})
        return AvatarBodyRigManifest(
            avatar_id=avatar_id,
            layer_graph_id=layer_graph_id,
            bones=bones,
            pivot_map=pivot_map,
            runtime_targets=[RuntimeTarget.REMOTION_LAYER, RuntimeTarget.SPINE_RUNTIME],
        )

    def create_canonical_pose_library(self, avatar_id: str) -> AvatarBodyPoseLibrary:
        poses = [
            AvatarBodyPose(
                pose_name=pose,
                primitive_function=self._primitive_for_pose(pose),
                sfl_function=self._sfl_for_pose(pose),
            )
            for pose in BodyPoseName
        ]
        return AvatarBodyPoseLibrary(avatar_id=avatar_id, poses=poses)

    def _primitive_for_pose(self, pose: BodyPoseName) -> str:
        mapping = {
            BodyPoseName.POINT_UP: "attention",
            BodyPoseName.POINT_TO_CARD: "clarity",
            BodyPoseName.OPEN_PALM_REVEAL: "permission",
            BodyPoseName.THINKING_CHIN: "discernment",
            BodyPoseName.STOP_HAND: "integrity",
            BodyPoseName.SOFT_SHRUG: "nuance",
            BodyPoseName.HOLD_CUP: "support",
            BodyPoseName.PRESENT_DIAGRAM: "teaching",
        }
        return mapping[pose]

    def _sfl_for_pose(self, pose: BodyPoseName) -> str:
        mapping = {
            BodyPoseName.POINT_UP: "perceptual_entry",
            BodyPoseName.POINT_TO_CARD: "focus_target",
            BodyPoseName.OPEN_PALM_REVEAL: "truthful_payoff",
            BodyPoseName.THINKING_CHIN: "active_prediction",
            BodyPoseName.STOP_HAND: "myth_interruption",
            BodyPoseName.SOFT_SHRUG: "nuance_preservation",
            BodyPoseName.HOLD_CUP: "closure_warmth",
            BodyPoseName.PRESENT_DIAGRAM: "process_confidence",
        }
        return mapping[pose]
