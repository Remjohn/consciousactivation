from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import (
    AvatarPSDLayerRequirement,
    CanonicalBodyLayerName,
)


class AvatarPSDLayerService:
    def compile_canonical_layer_requirements(self, source_prefix: str = "assets/avatar/coach") -> list[AvatarPSDLayerRequirement]:
        return [
            AvatarPSDLayerRequirement(
                layer_name=layer.value,
                canonical_layer=layer,
                source_path=f"{source_prefix}/{layer.value}.png",
                z_index=index,
                mesh_candidate=layer not in {CanonicalBodyLayerName.SHADOW, CanonicalBodyLayerName.PAPER_EDGE},
            )
            for index, layer in enumerate(CanonicalBodyLayerName, start=1)
        ]
