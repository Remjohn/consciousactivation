"""
errors.py
---------
Structured error taxonomy for Collision Intelligence (CAE-M03).
"""

class CollisionIntelligenceError(Exception):
    """Base exception for all collision intelligence failures."""
    pass


class UngroundedAnalogyError(CollisionIntelligenceError):
    """Raised when an analogy or metaphor lacks guest lived authority or supporting evidence."""
    pass


class ClicheTropeError(CollisionIntelligenceError):
    """Raised when a hypothesis relies on overused generic viral clichés without authentic insight."""
    pass


class LowTruthQuarantineError(CollisionIntelligenceError):
    """Raised when a hypothesis has high novelty but fails fundamental credibility or truth gates."""
    pass


class MissingFalsificationError(CollisionIntelligenceError):
    """Raised when a hypothesis lacks clear, empirical refutation/falsification conditions."""
    pass


class VectorTruthFallacyError(CollisionIntelligenceError):
    """Raised when an automated process attempts to assert truth solely from embedding vector proximity."""
    pass


class TenantMismatchError(CollisionIntelligenceError):
    """Raised when objects from different workspace tenants are collided."""
    pass
