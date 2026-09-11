"""
errors.py
---------
Structured error taxonomy for Relational Intelligence and Audience x Guest state synthesis.
"""

class RelationalIntelligenceError(Exception):
    """Base exception for relational intelligence layer."""
    pass


class TenantLeakageError(RelationalIntelligenceError):
    """Raised when an operation attempts to link or evaluate entities across different workspace boundaries."""
    pass


class IdentityMergeForbiddenError(RelationalIntelligenceError):
    """Raised when an automated process attempts to merge distinct guest identities."""
    pass


class MissingTemporalProvenanceError(RelationalIntelligenceError):
    """Raised when a dynamic temporal state or activation claim lacks required observation timestamps/evidence."""
    pass


class StaleStateError(RelationalIntelligenceError):
    """Raised when a temporal state exceeds freshness TTL without an explicit refresh or archival marker."""
    pass


class OneAxisFalseCongruenceError(RelationalIntelligenceError):
    """Raised when a high one-axis match is improperly promoted to general congruence without multi-axis evidence."""
    pass


class ScoreWithoutEvidenceError(RelationalIntelligenceError):
    """Raised when a congruence score is emitted without corresponding 4-axis relation evidence."""
    pass
