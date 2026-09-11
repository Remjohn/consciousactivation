"""
errors.py
---------
Structured error taxonomy for Scoring Intelligence (CAE-M08).
"""

class ScoringIntelligenceError(Exception):
    """Base exception for all scoring intelligence failures."""
    pass


class NonCompensableGateFailureError(ScoringIntelligenceError):
    """Raised when a candidate fails a non-compensable threshold (e.g. authenticity < 0.40)."""
    pass


class LowEvidenceViralityError(ScoringIntelligenceError):
    """Raised when high predicted virality attempts to pass without grounded evidence."""
    pass


class LengthGamingDetectedError(ScoringIntelligenceError):
    """Raised when artificial filler or excessive repetitive padding is detected."""
    pass


class KeywordStuffingDetectedError(ScoringIntelligenceError):
    """Raised when clickbait buzzwords are stuffed without semantic coherence."""
    pass


class DuplicateCandidateError(ScoringIntelligenceError):
    """Raised when redundant duplicate candidates proliferate in the portfolio."""
    pass
