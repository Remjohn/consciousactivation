from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import (
    AvatarPaperBodyLayer,
    AvatarPaperBodyLayerSet,
    CanonicalBodyLayerName,
)


class AvatarPaperBodyLayerService:
    def compile_body_layer_set(self, *, avatar_id: str, asset_prefix: str = "assets/avatar/body") -> AvatarPaperBodyLayerSet:
        layers = [
            AvatarPaperBodyLayer(
                canonical_layer=layer,
                asset_ref=f"{asset_prefix}/{layer.value}.png",
                z_index=index,
                riggable=layer not in {CanonicalBodyLayerName.SHADOW, CanonicalBodyLayerName.PAPER_EDGE},
                mesh_candidate=layer not in {CanonicalBodyLayerName.SHADOW},
            )
            for index, layer in enumerate(CanonicalBodyLayerName, start=1)
        ]
        return AvatarPaperBodyLayerSet(avatar_id=avatar_id, layers=layers)
