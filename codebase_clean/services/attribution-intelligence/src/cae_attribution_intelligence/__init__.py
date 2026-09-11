"""
cae_attribution_intelligence
----------------------------
The Semantic Attribution and Multi-Dimensional Evidence Classification package for CAE.
"""

from .domain import (
    SemanticRole,
    EvidenceEpistemicStatus,
    EmotionalRegister,
    StoryArcGeometry,
    ObservableEvidence,
    SemanticInference,
    SemanticAnnotation,
    EvidenceClassification,
)
from .errors import (
    AttributionIntelligenceError,
    EvidenceStatusInflationError,
    StoryLabelingViolationError,
    InvariantInflationError,
    PrematurePublishabilityError,
)
from .classifier import SemanticEvidenceClassifier
from .verifier import SemanticAttributionVerifier

__all__ = [
    "SemanticRole",
    "EvidenceEpistemicStatus",
    "EmotionalRegister",
    "StoryArcGeometry",
    "ObservableEvidence",
    "SemanticInference",
    "SemanticAnnotation",
    "EvidenceClassification",
    "AttributionIntelligenceError",
    "EvidenceStatusInflationError",
    "StoryLabelingViolationError",
    "InvariantInflationError",
    "PrematurePublishabilityError",
    "SemanticEvidenceClassifier",
    "SemanticAttributionVerifier",
]
