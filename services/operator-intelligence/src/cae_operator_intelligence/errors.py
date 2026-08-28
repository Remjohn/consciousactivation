"""
errors.py
---------
Structured error taxonomy for Operator Intelligence (CAE-M09).
"""

class OperatorIntelligenceError(Exception):
    """Base exception for all operator intelligence failures."""
    pass


class SilentSelectionViolationError(OperatorIntelligenceError):
    """Raised when an automated algorithm attempts to approve a candidate without explicit human operator action."""
    pass


class EvidenceMutationViolationError(OperatorIntelligenceError):
    """Raised when an operator modification mutates underlying verbatim evidence or checksums."""
    pass


class MissingRationaleError(OperatorIntelligenceError):
    """Raised when an operator action lacks a mandatory explanatory rationale."""
    pass


class UnapprovedExecutionError(OperatorIntelligenceError):
    """Raised when downstream production attempts to execute an unapproved candidate."""
    pass
