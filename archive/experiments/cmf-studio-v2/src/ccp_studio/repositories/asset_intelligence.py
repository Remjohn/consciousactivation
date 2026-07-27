from __future__ import annotations

from dataclasses import dataclass, field

from ccp_studio.contracts.asset_intelligence import (
    AssetCandidateMatch,
    AssetClassification,
    AssetEvaluationReceipt,
    AssetFatigueRecord,
    AssetPerformanceMemory,
    AssetRecord,
    AssetUsageReceipt,
    AssetVersion,
    CreativeIngredient,
    CreativeIngredientVariant,
    RightsProvenanceProfile,
    VisualReferenceBoard,
    WinningAssetRecord,
    AssetSemanticProfile,
)


@dataclass
class InMemoryAssetIntelligenceRepository:
    """Test-friendly repository for Asset Intelligence V1.

    This is intentionally storage-ready but not tied to a database in V1.
    Later implementations can preserve the service API and swap the repository.
    """

    asset_records: dict[str, AssetRecord] = field(default_factory=dict)
    asset_versions: dict[str, AssetVersion] = field(default_factory=dict)
    rights_profiles: dict[str, RightsProvenanceProfile] = field(default_factory=dict)
    classifications: dict[str, AssetClassification] = field(default_factory=dict)
    semantic_profiles: dict[str, AssetSemanticProfile] = field(default_factory=dict)
    creative_ingredients: dict[str, CreativeIngredient] = field(default_factory=dict)
    variants: dict[str, CreativeIngredientVariant] = field(default_factory=dict)
    evaluation_receipts: dict[str, AssetEvaluationReceipt] = field(default_factory=dict)
    usage_receipts: dict[str, AssetUsageReceipt] = field(default_factory=dict)
    performance_memory: dict[str, AssetPerformanceMemory] = field(default_factory=dict)
    fatigue_records: dict[str, AssetFatigueRecord] = field(default_factory=dict)
    winner_records: dict[str, WinningAssetRecord] = field(default_factory=dict)
    reference_boards: dict[str, VisualReferenceBoard] = field(default_factory=dict)

    def upsert_asset(self, asset: AssetRecord) -> AssetRecord:
        self.asset_records[asset.asset_id] = asset
        return asset

    def get_asset(self, asset_id: str) -> AssetRecord:
        return self.asset_records[asset_id]

    def list_assets(self) -> list[AssetRecord]:
        return list(self.asset_records.values())

    def upsert_version(self, version: AssetVersion) -> AssetVersion:
        self.asset_versions[version.asset_version_id] = version
        return version

    def upsert_rights_profile(self, rights: RightsProvenanceProfile) -> RightsProvenanceProfile:
        self.rights_profiles[rights.rights_profile_id] = rights
        return rights

    def get_rights_profile_for_asset(self, asset: AssetRecord) -> RightsProvenanceProfile | None:
        if not asset.rights_profile_id:
            return None
        return self.rights_profiles.get(asset.rights_profile_id)

    def upsert_classification(self, classification: AssetClassification) -> AssetClassification:
        self.classifications[classification.classification_id] = classification
        return classification

    def upsert_semantic_profile(self, profile: AssetSemanticProfile) -> AssetSemanticProfile:
        self.semantic_profiles[profile.semantic_profile_id] = profile
        return profile

    def upsert_ingredient(self, ingredient: CreativeIngredient) -> CreativeIngredient:
        self.creative_ingredients[ingredient.creative_ingredient_id] = ingredient
        return ingredient

    def list_ingredients_for_asset(self, asset_id: str) -> list[CreativeIngredient]:
        return [
            ingredient
            for ingredient in self.creative_ingredients.values()
            if asset_id in ingredient.source_asset_ids
        ]

    def upsert_variant(self, variant: CreativeIngredientVariant) -> CreativeIngredientVariant:
        self.variants[variant.variant_id] = variant
        return variant

    def upsert_evaluation(self, receipt: AssetEvaluationReceipt) -> AssetEvaluationReceipt:
        self.evaluation_receipts[receipt.evaluation_receipt_id] = receipt
        return receipt

    def upsert_usage(self, receipt: AssetUsageReceipt) -> AssetUsageReceipt:
        self.usage_receipts[receipt.usage_receipt_id] = receipt
        return receipt

    def list_usage_for_asset(self, asset_id: str) -> list[AssetUsageReceipt]:
        return [
            receipt
            for receipt in self.usage_receipts.values()
            if receipt.asset_id == asset_id
        ]

    def upsert_performance(self, memory: AssetPerformanceMemory) -> AssetPerformanceMemory:
        self.performance_memory[memory.performance_memory_id] = memory
        return memory

    def list_performance_for_asset(self, asset_id: str) -> list[AssetPerformanceMemory]:
        return [
            memory
            for memory in self.performance_memory.values()
            if memory.asset_id == asset_id
        ]

    def upsert_fatigue(self, fatigue: AssetFatigueRecord) -> AssetFatigueRecord:
        self.fatigue_records[fatigue.fatigue_record_id] = fatigue
        return fatigue

    def upsert_winner(self, winner: WinningAssetRecord) -> WinningAssetRecord:
        self.winner_records[winner.winning_asset_record_id] = winner
        return winner

    def upsert_reference_board(self, board: VisualReferenceBoard) -> VisualReferenceBoard:
        self.reference_boards[board.reference_board_id] = board
        return board
