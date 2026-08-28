"""
composer.py
-----------
Collision Hypothesis Composer intersecting 4 worlds into grounded editorial hypotheses.
"""

from __future__ import annotations

from typing import List, Optional

from .domain import (
    CollisionHypothesis,
    CollisionRelationType,
    FalsificationCondition,
    HeritageCMFEval,
    NoveltyClicheAssessment,
    ObliqueLens,
)
from .errors import (
    TenantMismatchError,
    UngroundedAnalogyError,
)


class CollisionHypothesisComposer:
    """Composes grounded CollisionHypothesis entities from multi-world inputs."""

    # Overused generic tropes that trigger cliché penalties
    COMMON_CLICHE_TERMS = {
        "10x your",
        "secret hack",
        "game changer",
        "unlock your potential",
        "mindset shift",
        "crush your goals",
        "hustle harder",
    }

    @classmethod
    def evaluate_cliche_risk(cls, text: str, semantic_distance: float = 0.80) -> NoveltyClicheAssessment:
        """Analyze text for overused viral clichés and tropes."""
        lower_text = text.lower()
        trope_hits = [trope for trope in cls.COMMON_CLICHE_TERMS if trope in lower_text]
        
        cliche_risk = min(1.0, len(trope_hits) * 0.40)
        is_quarantined = cliche_risk >= 0.70
        trope_pen = cliche_risk * 0.50

        return NoveltyClicheAssessment(
            semantic_distance_score=semantic_distance,
            cliche_risk_score=cliche_risk,
            trope_penalty=trope_pen,
            is_cliche_quarantined=is_quarantined,
        )

    @classmethod
    def evaluate_heritage_cmf(
        cls,
        surprise: float = 0.75,
        emotion: float = 0.80,
        specificity: float = 0.85,
        ai_slop_risk: float = 0.15,
    ) -> HeritageCMFEval:
        """Calculate OLD CMF viral potential as an advisory signal."""
        # Non-compensable: AI slop risk caps total potential
        base = (surprise * 0.35) + (emotion * 0.35) + (specificity * 0.30)
        slop_multiplier = max(0.10, 1.0 - ai_slop_risk)
        composite = base * slop_multiplier

        return HeritageCMFEval(
            surprise_score=surprise,
            emotion_score=emotion,
            specificity_score=specificity,
            ai_slop_risk=ai_slop_risk,
            composite_viral_potential=round(composite, 3),
        )

    @classmethod
    def compose(
        cls,
        *,
        workspace_id: str,
        title: str,
        relation_type: CollisionRelationType,
        audience_id: str,
        audience_tension_ref: str,
        guest_id: str,
        guest_lived_proof_citation: str,
        research_signal_id: str,
        bridge_statement: str,
        falsification_condition: FalsificationCondition,
        evidence_references: List[str],
        oblique_lens: Optional[ObliqueLens] = None,
        sda_invariant: str = "SDA-INV-001_ACTIVE_TENSION",
        surprise_score: float = 0.80,
        emotion_score: float = 0.80,
        specificity_score: float = 0.85,
    ) -> CollisionHypothesis:
        """Synthesize a complete CollisionHypothesis with 4-world grounding."""
        # Grounding check: Guest lived proof must be substantive
        if not guest_lived_proof_citation or len(guest_lived_proof_citation.strip()) < 10:
            raise UngroundedAnalogyError(
                "Cannot compose CollisionHypothesis: Guest lived proof citation is missing or unsubstantiated."
            )

        novelty_eval = cls.evaluate_cliche_risk(bridge_statement)
        cmf_eval = cls.evaluate_heritage_cmf(
            surprise=surprise_score,
            emotion=emotion_score,
            specificity=specificity_score,
            ai_slop_risk=novelty_eval.cliche_risk_score * 0.8,
        )

        return CollisionHypothesis(
            workspace_id=workspace_id,
            title=title,
            relation_type=relation_type,
            audience_id=audience_id,
            audience_tension_ref=audience_tension_ref,
            guest_id=guest_id,
            guest_lived_proof_citation=guest_lived_proof_citation,
            research_signal_id=research_signal_id,
            sda_invariant=sda_invariant,
            oblique_lens=oblique_lens,
            bridge_statement=bridge_statement,
            evidence_references=evidence_references,
            novelty_assessment=novelty_eval,
            falsification_condition=falsification_condition,
            heritage_eval=cmf_eval,
        )
