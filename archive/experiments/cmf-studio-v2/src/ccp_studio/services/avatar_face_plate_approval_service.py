from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import (
    AvatarFacePlateApprovalSet,
    AvatarFacePlateAsset,
    ExpressionPlateName,
)


class AvatarFacePlateApprovalService:
    def compile_approved_face_plate_set(self, *, avatar_id: str, approved_by: str, asset_prefix: str = "assets/avatar/face") -> AvatarFacePlateApprovalSet:
        plates = [
            AvatarFacePlateAsset(
                expression_name=expression,
                asset_ref=f"{asset_prefix}/{expression.value}.png",
                approved=True,
                sha256=f"hash_{expression.value}",
            )
            for expression in ExpressionPlateName
        ]
        return AvatarFacePlateApprovalSet(
            avatar_id=avatar_id,
            face_plates=plates,
            approved_by=approved_by,
        )
