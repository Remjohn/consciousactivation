from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    AvatarFacePlate,
    AvatarFacePlateSet,
    ExpressionPlateName,
)


class AvatarFacePlateService:
    def create_canonical_face_plate_set(self, avatar_id: str, image_ref_prefix: str = "face_plate") -> AvatarFacePlateSet:
        plates = [
            AvatarFacePlate(
                avatar_id=avatar_id,
                expression_name=name,
                image_ref=f"{image_ref_prefix}_{name.value}",
            )
            for name in ExpressionPlateName
        ]
        return AvatarFacePlateSet(avatar_id=avatar_id, plates=plates)
