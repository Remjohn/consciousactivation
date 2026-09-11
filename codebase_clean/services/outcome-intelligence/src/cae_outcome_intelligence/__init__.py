"""
cae_outcome_intelligence
------------------------
The Outcome Measurement and Selective Learning package for CAE.
"""

from .domain import (
    OutcomeDomain,
    FailureMode,
    ObservedOutcome,
    EvaluationReceipt,
    LearningProposal,
    PerformanceMemory,
)
from .errors import (
    OutcomeIntelligenceError,
    EngagementWithoutTruthError,
    MisleadingContextRewardHackError,
    AveragedDisagreementLaunderingError,
    OntologyMutationViolationError,
)
from .collector import OutcomeCollector
from .learner import SelectiveLearningEngine
from .verifier import OutcomeIntelligenceVerifier

__all__ = [
    "OutcomeDomain",
    "FailureMode",
    "ObservedOutcome",
    "EvaluationReceipt",
    "LearningProposal",
    "PerformanceMemory",
    "OutcomeIntelligenceError",
    "EngagementWithoutTruthError",
    "MisleadingContextRewardHackError",
    "AveragedDisagreementLaunderingError",
    "OntologyMutationViolationError",
    "OutcomeCollector",
    "SelectiveLearningEngine",
    "OutcomeIntelligenceVerifier",
]
