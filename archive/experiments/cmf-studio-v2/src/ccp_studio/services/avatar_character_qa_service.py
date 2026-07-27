from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import AvatarCharacterQAReport


class AvatarCharacterQAService:
    def run_qa(self, *, avatar_id: str, face_plate_count: int, body_layer_count: int, required_bones_present: bool, prop_sockets_present: bool, no_lipsync_policy_pass: bool, path_safety_pass: bool, export_manifests_valid: bool) -> AvatarCharacterQAReport:
        return AvatarCharacterQAReport(
            avatar_id=avatar_id,
            face_plate_count=face_plate_count,
            body_layer_count=body_layer_count,
            required_bones_present=required_bones_present,
            prop_sockets_present=prop_sockets_present,
            no_lipsync_policy_pass=no_lipsync_policy_pass,
            path_safety_pass=path_safety_pass,
            export_manifests_valid=export_manifests_valid,
        )
