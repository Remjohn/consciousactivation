"""
errors.py
---------
Structured error taxonomy for Outcome Intelligence & Selective Learning (CAE-M12).
"""

class OutcomeIntelligenceError(Exception):
    """Base exception for outcome measurement and learning failures."""
    pass


class EngagementWithoutTruthError(OutcomeIntelligenceError):
    """Raised when high viral engagement is reported without valid factual/evidence grounding."""
    pass


class MisleadingContextRewardHackError(OutcomeIntelligenceError):
    """Raised when positive metrics are achieved through sensationalized or misleading context."""
    pass


class AveragedDisagreementLaunderingError(OutcomeIntelligenceError):
    """Raised when polarized evaluator or operator disagreements are improperly averaged away."""
    pass


class OntologyMutationViolationError(OutcomeIntelligenceError):
    """Raised when an outcome or proposal attempts to automatically mutate canonical ontology without Operator ratification."""
    pass
