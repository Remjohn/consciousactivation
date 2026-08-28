"""
cae_production_program
----------------------
The Production Semantic Program and Compiler package for CAE.
"""

from .domain import (
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
from .verifier import ProductionProgramVerifier

__all__ = [
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
    "ProductionProgramVerifier",
]
