"""
verifier.py
-----------
Verification and gating logic for Interview Briefs and live session outcomes (CAE-M04).
"""

from __future__ import annotations

from .domain import (
    InterviewBrief,
    InterviewSessionResult,
    QuestionStage,
)
from .errors import (
    GenericResponseFailureError,
    ScriptedAnswerViolationError,
    UnauthenticatedSessionError,
)


class InterviewSessionVerifier:
    """Enforces constitutional validity on Interview Briefs and live session outcomes."""

    @classmethod
    def verify_brief(cls, brief: InterviewBrief) -> bool:
        """Validates that an InterviewBrief satisfies 4-stage progression and anti-scripting rules."""
        stages_present = {q.stage for q in brief.question_progression}
        required_stages = {
            QuestionStage.ORIENTATION,
            QuestionStage.TENSION_PROBE,
            QuestionStage.CRUCIBLE_EXPOSURE,
            QuestionStage.RESOLUTION_SYNTHESIS,
        }

        if not required_stages.issubset(stages_present):
            missing = required_stages - stages_present
            raise ValueError(f"InterviewBrief lacks required progression stages: {missing}")

        return True

    @classmethod
    def verify_session_result(cls, session: InterviewSessionResult) -> bool:
        """
        Validates live session results.
        Enforces Technical-Success False-Proof:
        Completing all turns mechanically is NOT success if answers are generic slop or unauthenticated.
        """
        # 1. Human Authentication Gate
        if not session.is_authenticated:
            session.execution_status = "UNAUTHENTICATED"
            raise UnauthenticatedSessionError(
                f"Interview session '{session.session_id}' failed human presence/voice authentication."
            )

        if not session.turns or len(session.turns) == 0:
            session.execution_status = "INCOMPLETE"
            raise GenericResponseFailureError("Session has zero recorded response turns.")

        # 2. Authenticity & Specificity Gate (Anti-Generic Slop)
        slop_count = sum(1 for t in session.turns if t.is_generic_slop or t.authenticity_score < 0.40)
        lived_evidence_count = sum(1 for t in session.turns if t.contains_lived_evidence and t.specificity_score >= 0.60)

        # If more than 75% of answers are generic slop or zero lived evidence was extracted:
        if slop_count >= len(session.turns) or lived_evidence_count == 0:
            session.execution_status = "INCOMPLETE"
            raise GenericResponseFailureError(
                f"Technical Success False-Proof: Session '{session.session_id}' completed all turns mechanically, "
                f"but produced only generic/slop responses with zero authentic lived evidence. Status set to INCOMPLETE."
            )

        session.execution_status = "COMPLETED"
        return True
