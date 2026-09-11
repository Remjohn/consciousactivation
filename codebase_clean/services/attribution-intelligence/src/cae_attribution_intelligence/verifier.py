"""
verifier.py
-----------
Verification and gating logic for Semantic Annotations and Evidence Classifications (CAE-M06).
"""

from __future__ import annotations

from .domain import (
    EvidenceEpistemicStatus,
    SemanticAnnotation,
    SemanticRole,
)
from .errors import (
    EvidenceStatusInflationError,
    InvariantInflationError,
    PrematurePublishabilityError,
    StoryLabelingViolationError,
)


class SemanticAttributionVerifier:
    """Enforces constitutional validity on SemanticAnnotations."""

    SPECULATIVE_MARKERS = ["i think", "i believe", "maybe", "perhaps", "in theory", "we could speculate", "presumably"]
    MECHANISM_MARKERS = ["because", "the dynamic is", "feedback loop", "mechanism", "selection pressure", "causes"]

    @classmethod
    def verify_annotation(cls, annotation: SemanticAnnotation) -> bool:
        """Validates a SemanticAnnotation against constitutional rules."""
        inf = annotation.semantic_inference
        obs = annotation.observable_evidence
        lower_text = obs.verbatim_text.lower()
        word_count = len(obs.verbatim_text.split())

        # 1. Reject Premature Publishability
        if inf.is_publishable:
            raise PrematurePublishabilityError(
                f"Annotation '{annotation.annotation_id}' violates constitutional boundary: "
                f"is_publishable must be False in M06."
            )

        # 2. Epistemic Status Inflation Gate
        if inf.epistemic_status == EvidenceEpistemicStatus.FIRST_PARTY_FACT:
            if any(marker in lower_text for marker in cls.SPECULATIVE_MARKERS):
                raise EvidenceStatusInflationError(
                    f"Evidence status inflation on '{annotation.annotation_id}': "
                    f"Text contains speculative language but is marked FIRST_PARTY_FACT."
                )

        # 3. Story Labeling Violation Gate
        if inf.semantic_role == SemanticRole.STORY and word_count < 15:
            raise StoryLabelingViolationError(
                f"Story labeling violation on '{annotation.annotation_id}': "
                f"Excerpt ({word_count} words) lacks multi-beat narrative structure."
            )

        # 4. Invariant Inflation Gate
        if inf.invariant_ref is not None:
            if not any(marker in lower_text for marker in cls.MECHANISM_MARKERS) and word_count < 8:
                raise InvariantInflationError(
                    f"Invariant inflation on '{annotation.annotation_id}': "
                    f"Attaching invariant '{inf.invariant_ref}' to text lacking causal mechanisms."
                )

        return True
