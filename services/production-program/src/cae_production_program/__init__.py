"""
cae_production_program
----------------------
The Production Semantic Program and Compiler package for CAE.
"""

from .domain import (
    AssetDemandSpec,
    SceneRole,
    SFLModulationProfile,
    VisualAudioSpecs,
    SemanticSceneSpec,
    SemanticProgram,
    CompositionHandoffReceipt,
)
from .errors import (
    ProductionProgramError,
    EvidenceQuoteMismatchError,
    UnapprovedAssetInsertionError,
    StoryArcGeometryMutationError,
    TimingDiscontinuityError,
)
from .compiler import ProductionProgramCompiler
from .composition_asset_pack import (
    AssetBindingError,
    AssetBindingInvalidatedError,
    AssetLineageValidationError,
    CompositionAssetBinding,
    CompositionAssetPack,
    ExplicitSelectionReceipt,
    apply_composition_asset_pack,
    bind_selected_retrieval_candidates,
    build_selection_receipt,
    candidate_identity_snapshot,
    invalidate_composition_asset_pack,
    validate_composition_asset_pack,
)
from .verifier import ProductionProgramVerifier

__all__ = [
    "AssetDemandSpec",
    "SceneRole",
    "SFLModulationProfile",
    "VisualAudioSpecs",
    "SemanticSceneSpec",
    "SemanticProgram",
    "CompositionHandoffReceipt",
    "ProductionProgramError",
    "EvidenceQuoteMismatchError",
    "UnapprovedAssetInsertionError",
    "StoryArcGeometryMutationError",
    "TimingDiscontinuityError",
    "ProductionProgramCompiler",
    "AssetBindingError",
    "AssetBindingInvalidatedError",
    "AssetLineageValidationError",
    "CompositionAssetBinding",
    "CompositionAssetPack",
    "ExplicitSelectionReceipt",
    "apply_composition_asset_pack",
    "bind_selected_retrieval_candidates",
    "build_selection_receipt",
    "candidate_identity_snapshot",
    "invalidate_composition_asset_pack",
    "validate_composition_asset_pack",
    "ProductionProgramVerifier",
]
