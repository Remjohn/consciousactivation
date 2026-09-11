"""
classifier.py
-------------
Semantic Evidence Classifier transforming EvidenceSegments into SemanticAnnotations.
"""

from __future__ import annotations

from typing import Optional

from .domain import (
    EmotionalRegister,
    EvidenceClassification,
    EvidenceEpistemicStatus,
    ObservableEvidence,
    SemanticAnnotation,
    SemanticInference,
    SemanticRole,
    StoryArcGeometry,
)
from .errors import (
    EvidenceStatusInflationError,
    InvariantInflationError,
    PrematurePublishabilityError,
    StoryLabelingViolationError,
)


class SemanticEvidenceClassifier:
    """Classifies EvidenceSegments into typed, partitioned SemanticAnnotations."""

    SPECULATIVE_MARKERS = ["i think", "i believe", "maybe", "perhaps", "in theory", "we could speculate", "presumably"]
    MECHANISM_MARKERS = ["because", "the dynamic is", "feedback loop", "mechanism", "selection pressure", "causes"]

    @classmethod
    def classify(
        cls,
        *,
        workspace_id: str,
        session_id: str,
        segment_id: str,
        speaker: str,
        start_time_ms: int,
        end_time_ms: int,
        verbatim_text: str,
        text_sha256: str,
        semantic_role: SemanticRole,
        epistemic_status: EvidenceEpistemicStatus,
        confidence_score: float = 0.85,
        tension_ref: Optional[str] = None,
        invariant_ref: Optional[str] = None,
        emotional_register: EmotionalRegister = EmotionalRegister.NEUTRAL,
        story_arc_geometry: StoryArcGeometry = StoryArcGeometry.NONE,
        is_eligible_for_candidate_formation: bool = True,
        is_publishable: bool = False,
    ) -> SemanticAnnotation:
        """Constructs a partitioned SemanticAnnotation with strict validation."""
        # 1. Reject Premature Publishability
        if is_publishable:
            raise PrematurePublishabilityError(
                "Cannot mark annotation as publishable in M06. Publishability decisions belong to downstream production gates."
            )

        lower_text = verbatim_text.lower()

        # 2. Anti-Evidence Status Inflation Check
        if epistemic_status == EvidenceEpistemicStatus.FIRST_PARTY_FACT:
            if any(marker in lower_text for marker in cls.SPECULATIVE_MARKERS):
                raise EvidenceStatusInflationError(
                    f"Evidence status inflation: Text contains speculative markers but was labeled FIRST_PARTY_FACT: '{verbatim_text}'"
                )

        # 3. Anti-Story Labeling Violation Check
        if semantic_role == SemanticRole.STORY:
            # A STORY requires narrative length and temporal/scene progression (at least 20 words or scene indicators)
            word_count = len(verbatim_text.split())
            if word_count < 15:
                raise StoryLabelingViolationError(
                    f"Story labeling violation: Short excerpt ({word_count} words) cannot be classified as a STORY. Use QUOTE, BEAT, or CLAIM instead."
                )

        # 4. Anti-Invariant Inflation Check
        if invariant_ref is not None:
            if not any(marker in lower_text for marker in cls.MECHANISM_MARKERS) and len(verbatim_text.split()) < 8:
                raise InvariantInflationError(
                    f"Invariant inflation: Attaching deep invariant '{invariant_ref}' to generic statement without causal mechanism: '{verbatim_text}'"
                )

        obs = ObservableEvidence(
            segment_id=segment_id,
            workspace_id=workspace_id,
            session_id=session_id,
            speaker=speaker,
            start_time_ms=start_time_ms,
            end_time_ms=end_time_ms,
            verbatim_text=verbatim_text,
            text_sha256=text_sha256,
        )

        inf = SemanticInference(
            semantic_role=semantic_role,
            epistemic_status=epistemic_status,
            confidence_score=confidence_score,
            tension_ref=tension_ref,
            invariant_ref=invariant_ref,
            emotional_register=emotional_register,
            story_arc_geometry=story_arc_geometry,
            is_eligible_for_candidate_formation=is_eligible_for_candidate_formation,
            is_publishable=False,
        )

        return SemanticAnnotation(
            workspace_id=workspace_id,
            observable_evidence=obs,
            semantic_inference=inf,
        )

    @classmethod
    def create_classification_record(cls, annotation: SemanticAnnotation) -> EvidenceClassification:
        """Create a summary classification record for candidate formation."""
        return EvidenceClassification(
            workspace_id=annotation.workspace_id,
            segment_id=annotation.observable_evidence.segment_id,
            annotation_id=annotation.annotation_id,
            primary_role=annotation.semantic_inference.semantic_role,
            epistemic_tier=annotation.semantic_inference.epistemic_status,
            is_candidate_eligible=annotation.semantic_inference.is_eligible_for_candidate_formation,
        )
