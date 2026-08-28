"""
cae_interview_intelligence
--------------------------
The Interview Semantic Program and Human-First Elicitation package for CAE.
"""

from .domain import (
    QuestionStage,
    DesiredEvidenceClass,
    InterviewQuestion,
    AdaptiveFollowUpPolicy,
    MatrixOfEdgingConfig,
    InterviewBrief,
    InterviewTurnResponse,
    InterviewSessionResult,
)
from .errors import (
    InterviewIntelligenceError,
    ScriptedAnswerViolationError,
    GenericResponseFailureError,
    UnauthenticatedSessionError,
    EdgingBoundaryExceededError,
    PrematureContentError,
)
from .composer import InterviewBriefComposer
from .verifier import InterviewSessionVerifier

__all__ = [
    "QuestionStage",
    "DesiredEvidenceClass",
    "InterviewQuestion",
    "AdaptiveFollowUpPolicy",
    "MatrixOfEdgingConfig",
    "InterviewBrief",
    "InterviewTurnResponse",
    "InterviewSessionResult",
    "InterviewIntelligenceError",
    "ScriptedAnswerViolationError",
    "GenericResponseFailureError",
    "UnauthenticatedSessionError",
    "EdgingBoundaryExceededError",
    "PrematureContentError",
    "InterviewBriefComposer",
    "InterviewSessionVerifier",
]
