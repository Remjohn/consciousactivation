"""
composer.py
-----------
Interview Brief Composer compiling approved CollisionHypotheses into 4-stage elicitation programs.
"""

from __future__ import annotations

from typing import List, Optional

from .domain import (
    AdaptiveFollowUpPolicy,
    DesiredEvidenceClass,
    InterviewBrief,
    InterviewQuestion,
    MatrixOfEdgingConfig,
    QuestionStage,
)
from .errors import (
    ScriptedAnswerViolationError,
)


class InterviewBriefComposer:
    """Compiles structured, non-scripted InterviewBrief contracts from CollisionHypotheses."""

    FORBIDDEN_LEADING_PHRASES = [
        "don't you agree",
        "isn't it true that",
        "would you agree that",
        "obviously you believe",
        "surely you think",
        "as we all know",
    ]

    @classmethod
    def assert_non_scripted_prompt(cls, prompt: str) -> None:
        """Enforces that elicitation questions do not embed scripted or leading conclusions."""
        lower = prompt.lower()
        for phrase in cls.FORBIDDEN_LEADING_PHRASES:
            if phrase in lower:
                raise ScriptedAnswerViolationError(
                    f"Scripted answer violation: Prompt contains leading phrase '{phrase}'. Elicitation must remain open-ended."
                )

    @classmethod
    def compose_standard_brief(
        cls,
        *,
        workspace_id: str,
        hypothesis_id: str,
        guest_id: str,
        audience_id: str,
        target_activation: str,
        context_premise: str,
        collision_thesis: str,
        orientation_prompt: str,
        tension_prompt: str,
        crucible_prompt: str,
        resolution_prompt: str,
        forbidden_territories: Optional[List[str]] = None,
    ) -> InterviewBrief:
        """Compose a canonical 4-stage InterviewBrief from explicit prompts."""
        prompts = [
            (QuestionStage.ORIENTATION, orientation_prompt, DesiredEvidenceClass.CONTRARIAN_DECISION),
            (QuestionStage.TENSION_PROBE, tension_prompt, DesiredEvidenceClass.FAILURE_ANALYSIS),
            (QuestionStage.CRUCIBLE_EXPOSURE, crucible_prompt, DesiredEvidenceClass.CRUCIBLE_MOMENT),
            (QuestionStage.RESOLUTION_SYNTHESIS, resolution_prompt, DesiredEvidenceClass.COST_PAID_RECEIPT),
        ]

        questions = []
        for stage, text, ev_class in prompts:
            cls.assert_non_scripted_prompt(text)
            questions.append(
                InterviewQuestion(
                    stage=stage,
                    prompt_text=text,
                    expected_evidence_class=ev_class,
                    forbidden_presumptions=[collision_thesis],
                )
            )

        edging = MatrixOfEdgingConfig(
            target_vulnerability_depth=0.80,
            pressure_gradient="PROGRESSIVE_EXPONENTIAL",
            forbidden_territories=forbidden_territories or [],
            safety_ceiling_threshold=0.90,
        )

        return InterviewBrief(
            workspace_id=workspace_id,
            hypothesis_ref=hypothesis_id,
            guest_id=guest_id,
            audience_id=audience_id,
            target_activation_state=target_activation,
            context_premise=context_premise,
            collision_anchor_thesis=collision_thesis,
            question_progression=questions,
            follow_up_policy=AdaptiveFollowUpPolicy(),
            edging_config=edging,
        )
