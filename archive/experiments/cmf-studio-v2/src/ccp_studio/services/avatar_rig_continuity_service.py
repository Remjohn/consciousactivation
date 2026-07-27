from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import AvatarRigContinuityReceipt


class AvatarRigContinuityService:
    def evaluate(self, *, avatar_id: str, identity_anchors_preserved: bool = True, face_plate_set_stable: bool = True, body_layer_set_stable: bool = True, rig_version_stable: bool = True, paper_material_profile_stable: bool = True) -> AvatarRigContinuityReceipt:
        return AvatarRigContinuityReceipt(
            avatar_id=avatar_id,
            identity_anchors_preserved=identity_anchors_preserved,
            face_plate_set_stable=face_plate_set_stable,
            body_layer_set_stable=body_layer_set_stable,
            rig_version_stable=rig_version_stable,
            paper_material_profile_stable=paper_material_profile_stable,
        )
