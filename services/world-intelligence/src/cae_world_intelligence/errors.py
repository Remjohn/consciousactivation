"""
errors.py
---------
Structured error taxonomy for World Intelligence ingestion and verification.
"""

class WorldIntelligenceError(Exception):
    """Base error for all world intelligence failures."""
    pass


class ProvenanceError(WorldIntelligenceError):
    """Raised when an observation or signal lacks complete, verifiable provenance."""
    pass


class StaleObservationError(WorldIntelligenceError):
    """Raised when an observation exceeds freshness TTL without valid archival rationale."""
    pass


class DuplicateSourceInflationError(WorldIntelligenceError):
    """Raised when syndicated/mirror copies are falsely reported as independent sources."""
    pass


class EvidenceError(WorldIntelligenceError):
    """Raised when raw observation evidence is missing, corrupted, or fails content-hash verification."""
    pass


class TaxonomyError(WorldIntelligenceError):
    """Raised when entity or signal typing violates the canonical CAE ontology."""
    pass
