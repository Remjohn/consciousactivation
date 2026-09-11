"""
verifier.py
-----------
Gating and verification logic for Collision Hypotheses (CAE-M03).
"""

from __future__ import annotations

from .domain import CollisionHypothesis
from .errors import (
    ClicheTropeError,
    LowTruthQuarantineError,
    MissingFalsificationError,
    UngroundedAnalogyError,
    VectorTruthFallacyError,
)


class CollisionHypothesisVerifier:
    """Enforces constitutional validity and anti-reward hacking gates on CollisionHypotheses."""

    @classmethod
    def verify(cls, hypothesis: CollisionHypothesis) -> bool:
        """
        Validate a CollisionHypothesis. Raises structured errors if any constitutional gate fails.
        """
        # 1. Grounded Guest Lived Proof Gate
        if not hypothesis.guest_lived_proof_citation or len(hypothesis.guest_lived_proof_citation.strip()) < 10:
            raise UngroundedAnalogyError("CollisionHypothesis lacks verified guest lived proof citation.")

        # 2. Evidence Citation Gate
        if not hypothesis.evidence_references or len(hypothesis.evidence_references) == 0:
            raise UngroundedAnalogyError("CollisionHypothesis has zero evidence references attached.")

        # 3. Falsification Gate
        f = hypothesis.falsification_condition
        if not f.refuting_observation or len(f.refuting_observation.strip()) < 10:
            raise MissingFalsificationError("Hypothesis lacks explicit refuting observation condition.")
        if not f.disconfirming_testimony or len(f.disconfirming_testimony.strip()) < 10:
            raise MissingFalsificationError("Hypothesis lacks disconfirming guest testimony condition.")
        if not f.boundary_limitation or len(f.boundary_limitation.strip()) < 10:
            raise MissingFalsificationError("Hypothesis lacks defined boundary limitations.")

        # 4. Anti-Cliché / Trope Quarantine Gate
        if hypothesis.novelty_assessment.is_cliche_quarantined:
            raise ClicheTropeError(
                f"Hypothesis '{hypothesis.title}' is quarantined due to excessive cliché/trope score ({hypothesis.novelty_assessment.cliche_risk_score:.2f})."
            )

        # 5. Low-Truth / High-Slop Quarantine Gate
        if hypothesis.heritage_eval.ai_slop_risk > 0.60:
            raise LowTruthQuarantineError(
                f"Hypothesis quarantined: AI slop risk ({hypothesis.heritage_eval.ai_slop_risk:.2f}) exceeds acceptable threshold (0.60)."
            )

        # 6. Vector Truth Fallacy Guard
        if hypothesis.metadata.get("is_derived_solely_from_vector_similarity", False):
            raise VectorTruthFallacyError("Hypothesis rejected: Semantic embedding proximity alone cannot substantiate editorial truth.")

        return True
