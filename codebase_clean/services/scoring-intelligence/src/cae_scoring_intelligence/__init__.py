"""
cae_scoring_intelligence
------------------------
The Multi-Dimensional Candidate Scoring and Clustering package for CAE.
"""

from .domain import (
    DimensionScores,
    GateStatus,
    EvaluatorProvenance,
    CandidateEvaluationProfile,
    ClusterGroup,
    EditorialBoard,
)
from .errors import (
    ScoringIntelligenceError,
    NonCompensableGateFailureError,
    LengthGamingDetectedError,
    KeywordStuffingDetectedError,
    LowEvidenceViralityError,
    DuplicateCandidateError,
)
from .evaluator import MultiDimensionalCandidateEvaluator
from .clusterer import CandidateClusterEngine
from .verifier import EditorialBoardVerifier

__all__ = [
    "DimensionScores",
    "GateStatus",
    "EvaluatorProvenance",
    "CandidateEvaluationProfile",
    "ClusterGroup",
    "EditorialBoard",
    "ScoringIntelligenceError",
    "NonCompensableGateFailureError",
    "LengthGamingDetectedError",
    "KeywordStuffingDetectedError",
    "LowEvidenceViralityError",
    "DuplicateCandidateError",
    "MultiDimensionalCandidateEvaluator",
    "CandidateClusterEngine",
    "EditorialBoardVerifier",
]
