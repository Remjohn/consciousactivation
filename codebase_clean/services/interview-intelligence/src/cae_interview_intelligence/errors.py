"""
errors.py
---------
Structured error taxonomy for Interview Intelligence (CAE-M04).
"""

class InterviewIntelligenceError(Exception):
    """Base exception for all interview intelligence failures."""
    pass


class ScriptedAnswerViolationError(InterviewIntelligenceError):
    """Raised when an interview question embeds its own desired answer or attempts to force a conclusion."""
    pass


class GenericResponseFailureError(InterviewIntelligenceError):
    """Raised when an interview run completes all turns but produces only generic or platitudinous responses."""
    pass


class UnauthenticatedSessionError(InterviewIntelligenceError):
    """Raised when an interview session lacks authentic voice/biometric/presence signatures."""
    pass


class EdgingBoundaryExceededError(InterviewIntelligenceError):
    """Raised when elicitation pressure breaches the guest's declared safety ceiling or forbidden territories."""
    pass


class PrematureContentError(InterviewIntelligenceError):
    """Raised when an operation attempts to generate publishable finished content inside the interview planning layer."""
    pass
