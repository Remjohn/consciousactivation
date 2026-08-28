"""
errors.py
---------
Structured error taxonomy for Attribution Intelligence (CAE-M06).
"""

class AttributionIntelligenceError(Exception):
    """Base exception for all attribution intelligence failures."""
    pass


class EvidenceStatusInflationError(AttributionIntelligenceError):
    """Raised when an unverified speculation or abstract opinion is mislabeled as first-party fact."""
    pass


class StoryLabelingViolationError(AttributionIntelligenceError):
    """Raised when an isolated one-line quote or claim is mislabeled as a narrative story without setting/crisis/resolution."""
    pass


class InvariantInflationError(AttributionIntelligenceError):
    """Raised when a deep SDA invariant is attached to generic emotional phrases lacking structural mechanics."""
    pass


class PrematurePublishabilityError(AttributionIntelligenceError):
    """Raised when an operation attempts to declare an annotated segment publishable inside the attribution layer."""
    pass
