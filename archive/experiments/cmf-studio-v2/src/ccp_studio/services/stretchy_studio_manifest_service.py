from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import (
    AvatarMeshCandidate,
    AvatarPropSocketSpec,
    AvatarRigBoneHint,
    AvatarShapeKeyCandidate,
    CanonicalBodyLayerName,
    MeshCandidateKind,
    PropSocketName,
    ShapeKeyKind,
    StretchyStudioImportManifest,
)


class StretchyStudioManifestService:
    def compile_import_manifest(self, *, avatar_id: str, source_psd_ref: str, layer_requirements, action_timeline_ref: str | None = None) -> StretchyStudioImportManifest:
        skeleton_hints = [
            AvatarRigBoneHint(bone_name="torso", parent_bone_name=None, target_layer=CanonicalBodyLayerName.TORSO),
            AvatarRigBoneHint(bone_name="neck", parent_bone_name="torso", target_layer=CanonicalBodyLayerName.HEAD_ANCHOR),
            AvatarRigBoneHint(bone_name="head_anchor", parent_bone_name="neck", target_layer=CanonicalBodyLayerName.HEAD_ANCHOR),
            AvatarRigBoneHint(bone_name="left_arm", parent_bone_name="torso", target_layer=CanonicalBodyLayerName.LEFT_ARM),
            AvatarRigBoneHint(bone_name="right_arm", parent_bone_name="torso", target_layer=CanonicalBodyLayerName.RIGHT_ARM),
            AvatarRigBoneHint(bone_name="left_hand", parent_bone_name="left_arm", target_layer=CanonicalBodyLayerName.LEFT_HAND),
            AvatarRigBoneHint(bone_name="right_hand", parent_bone_name="right_arm", target_layer=CanonicalBodyLayerName.RIGHT_HAND),
        ]
        mesh_candidates = [
            AvatarMeshCandidate(kind=MeshCandidateKind.LIMB_BEND, target_layer=CanonicalBodyLayerName.LEFT_ARM, reason="paper arm bend"),
            AvatarMeshCandidate(kind=MeshCandidateKind.LIMB_BEND, target_layer=CanonicalBodyLayerName.RIGHT_ARM, reason="paper arm bend"),
            AvatarMeshCandidate(kind=MeshCandidateKind.CLOTH_DEFORM, target_layer=CanonicalBodyLayerName.CLOTHES, reason="subtle paper cloth movement"),
        ]
        shape_keys = [
            AvatarShapeKeyCandidate(kind=ShapeKeyKind.BLINK, target_layer=CanonicalBodyLayerName.HEAD_ANCHOR, reason="optional blink expression plate blend"),
            AvatarShapeKeyCandidate(kind=ShapeKeyKind.PAPER_SETTLE, target_layer=CanonicalBodyLayerName.CLOTHES, reason="paper settle motion"),
        ]
        prop_sockets = [
            AvatarPropSocketSpec(socket_name=PropSocketName.LEFT_HAND, target_bone_name="left_hand", target_layer=CanonicalBodyLayerName.LEFT_HAND),
            AvatarPropSocketSpec(socket_name=PropSocketName.RIGHT_HAND, target_bone_name="right_hand", target_layer=CanonicalBodyLayerName.RIGHT_HAND),
            AvatarPropSocketSpec(socket_name=PropSocketName.CARD_SURFACE, target_bone_name="torso", target_layer=CanonicalBodyLayerName.TORSO),
        ]
        return StretchyStudioImportManifest(
            avatar_id=avatar_id,
            source_psd_ref=source_psd_ref,
            layer_requirements=layer_requirements,
            skeleton_hints=skeleton_hints,
            mesh_candidates=mesh_candidates,
            shape_key_candidates=shape_keys,
            prop_sockets=prop_sockets,
            action_timeline_ref=action_timeline_ref,
            see_through_source=False,
            notes="Manifest only. No Stretchy Studio runtime call executed.",
        )
