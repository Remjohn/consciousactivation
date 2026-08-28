"""
errors.py
---------
Structured error taxonomy for Candidate Intelligence (CAE-M07).
"""

class CandidateIntelligenceError(Exception):
    """Base exception for all candidate intelligence failures."""
    pass


class UngroundedCandidateError(CandidateIntelligenceError):
    """Raised when a candidate lacks verifiable evidence links to underlying EvidenceSegments."""
    pass


class NarrativeIncompletenessError(CandidateIntelligenceError):
    """Raised when an excerpt is marked INCOMPLETE or lacks essential context for standalone understanding."""
    pass


class MissingStoryTurnError(CandidateIntelligenceError):
    """Raised when a STORY candidate contains setup/context but lacks a decisive narrative turn or resolution."""
    pass


class PrematureProductionApprovalError(CandidateIntelligenceError):
    """Raised when an operation attempts to declare a candidate APPROVED_FOR_PRODUCTION inside the candidate formation layer."""
    pass
