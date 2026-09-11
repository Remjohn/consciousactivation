"""
cae_relational_intelligence
---------------------------
The Relational Intelligence and Audience x Guest State Synthesis package for CAE.
"""

from .domain import (
    AudienceProfile,
    AudienceTemporalState,
    GuestProfile,
    GuestActivationState,
    FourAxisEvidence,
    GuestExperiencedTension,
    GuestResolvedTension,
    AudienceExperiencesTension,
    GuestAudienceCongruence,
)
from .errors import (
    RelationalIntelligenceError,
    TenantLeakageError,
    IdentityMergeForbiddenError,
    MissingTemporalProvenanceError,
    OneAxisFalseCongruenceError,
    ScoreWithoutEvidenceError,
    StaleStateError,
)
from .evaluator import RelationalCongruenceEvaluator
from .verifier import RelationalStateVerifier

__all__ = [
    "AudienceProfile",
    "AudienceTemporalState",
    "GuestProfile",
    "GuestActivationState",
    "FourAxisEvidence",
    "GuestExperiencedTension",
    "GuestResolvedTension",
    "AudienceExperiencesTension",
    "GuestAudienceCongruence",
    "RelationalIntelligenceError",
    "TenantLeakageError",
    "IdentityMergeForbiddenError",
    "MissingTemporalProvenanceError",
    "OneAxisFalseCongruenceError",
    "ScoreWithoutEvidenceError",
    "StaleStateError",
    "RelationalCongruenceEvaluator",
    "RelationalStateVerifier",
]
