from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import AvatarRemotionLayerPayload


class AvatarRemotionLayerPayloadService:
    def compile_payload(self, *, avatar_id: str, layer_refs: list[str], action_timeline_ref: str, rig_export_manifest_ref: str) -> AvatarRemotionLayerPayload:
        return AvatarRemotionLayerPayload(
            avatar_id=avatar_id,
            layer_refs=layer_refs,
            action_timeline_ref=action_timeline_ref,
            rig_export_manifest_ref=rig_export_manifest_ref,
            runtime_props={"avatar_id": avatar_id, "no_lipsync": True},
        )
