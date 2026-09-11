"""
cae_collision_intelligence
--------------------------
The Collision Intelligence and Hypothesis Formation package for CAE.
"""

from .domain import (
    CollisionRelationType,
    ObliqueLens,
    NoveltyClicheAssessment,
    FalsificationCondition,
    HeritageCMFEval,
    CollisionHypothesis,
)
from .errors import (
    CollisionIntelligenceError,
    UngroundedAnalogyError,
    ClicheTropeError,
    LowTruthQuarantineError,
    MissingFalsificationError,
    VectorTruthFallacyError,
    TenantMismatchError,
)
from .composer import CollisionHypothesisComposer
from .verifier import CollisionHypothesisVerifier

__all__ = [
    "CollisionRelationType",
    "ObliqueLens",
    "NoveltyClicheAssessment",
    "FalsificationCondition",
    "HeritageCMFEval",
    "CollisionHypothesis",
    "CollisionIntelligenceError",
    "UngroundedAnalogyError",
    "ClicheTropeError",
    "LowTruthQuarantineError",
    "MissingFalsificationError",
    "VectorTruthFallacyError",
    "TenantMismatchError",
    "CollisionHypothesisComposer",
    "CollisionHypothesisVerifier",
]
