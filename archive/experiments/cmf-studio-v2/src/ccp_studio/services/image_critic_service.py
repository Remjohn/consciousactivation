"""ImageCritic-style scoring service for TS-CMF-019."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ccp_studio.contracts.acting_library import ActingReferenceEvaluation
from ccp_studio.contracts.orchestration import utc_now


@dataclass
class ImageCriticService:
    threshold: float = 0.8

    def evaluate_acting_reference(
        self,
        *,
        acting_reference_id: UUID,
        likeness_score: float,
        gesture_clarity_score: float,
        hand_quality_score: float,
        paper_texture_score: float,
        style_adherence_score: float,
        negative_space_score: float,
        production_usability_score: float,
        failure_notes: list[str] | None = None,
    ) -> ActingReferenceEvaluation:
        return ActingReferenceEvaluation(
            schema_version="cmf.acting_reference_evaluation.v1",
            evaluation_receipt_id=uuid4(),
            acting_reference_id=acting_reference_id,
            likeness_score=likeness_score,
            gesture_clarity_score=gesture_clarity_score,
            hand_quality_score=hand_quality_score,
            paper_texture_score=paper_texture_score,
            style_adherence_score=style_adherence_score,
            negative_space_score=negative_space_score,
            production_usability_score=production_usability_score,
            failure_notes=failure_notes or [],
            evaluated_at=utc_now(),
        )
