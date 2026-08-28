"""
cae_operator_intelligence
-------------------------
The Human-in-the-Loop Operator Editorial Selection package for CAE.
"""

from .domain import (
    OperatorActionType,
    OperatorDecisionReceipt,
    SelectedCandidateSnapshot,
    CandidateEditorialBoardView,
    OperatorSelectionSession,
)
from .errors import (
    OperatorIntelligenceError,
    SilentSelectionViolationError,
    EvidenceMutationViolationError,
    MissingRationaleError,
    UnapprovedExecutionError,
)
from .manager import OperatorSelectionManager
from .verifier import OperatorSelectionVerifier

__all__ = [
    "OperatorActionType",
    "OperatorDecisionReceipt",
    "SelectedCandidateSnapshot",
    "CandidateEditorialBoardView",
    "OperatorSelectionSession",
    "OperatorIntelligenceError",
    "SilentSelectionViolationError",
    "EvidenceMutationViolationError",
    "MissingRationaleError",
    "UnapprovedExecutionError",
    "OperatorSelectionManager",
    "OperatorSelectionVerifier",
]
