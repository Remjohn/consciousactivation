"""Creative library item repositories for TS-CMF-020."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ccp_studio.contracts.creative_libraries import (
    CompositionPreference,
    CreativeLibraryReceipt,
    MicroSemioticAnchor,
    MotionRecipe,
    PlatformProfile,
    SfxAsset,
)


@dataclass
class InMemoryCreativeLibraryRepository:
    micro_semiotic_anchors: dict[UUID, MicroSemioticAnchor] = field(default_factory=dict)
    motion_recipes: dict[UUID, MotionRecipe] = field(default_factory=dict)
    sfx_assets: dict[UUID, SfxAsset] = field(default_factory=dict)
    composition_preferences: dict[UUID, CompositionPreference] = field(default_factory=dict)
    platform_profiles: dict[UUID, PlatformProfile] = field(default_factory=dict)
    receipts: dict[UUID, CreativeLibraryReceipt] = field(default_factory=dict)

    def put_anchor(self, anchor: MicroSemioticAnchor) -> MicroSemioticAnchor:
        self.micro_semiotic_anchors[anchor.micro_semiotic_anchor_id] = anchor
        return anchor

    def put_motion_recipe(self, recipe: MotionRecipe) -> MotionRecipe:
        self.motion_recipes[recipe.motion_recipe_id] = recipe
        return recipe

    def put_sfx_asset(self, asset: SfxAsset) -> SfxAsset:
        self.sfx_assets[asset.sfx_asset_id] = asset
        return asset

    def put_composition_preference(self, preference: CompositionPreference) -> CompositionPreference:
        self.composition_preferences[preference.composition_preference_id] = preference
        return preference

    def put_platform_profile(self, profile: PlatformProfile) -> PlatformProfile:
        self.platform_profiles[profile.platform_profile_id] = profile
        return profile

    def put_receipt(self, receipt: CreativeLibraryReceipt) -> CreativeLibraryReceipt:
        self.receipts[receipt.creative_library_receipt_id] = receipt
        return receipt

    def get_item(self, item_id: UUID) -> Any | None:
        for collection in [
            self.micro_semiotic_anchors,
            self.motion_recipes,
            self.sfx_assets,
            self.composition_preferences,
            self.platform_profiles,
        ]:
            if item_id in collection:
                return collection[item_id]
        return None
