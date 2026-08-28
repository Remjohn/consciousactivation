"""
test_collision_composition.py
------------------------------
Tests the automated composition of CollisionHypotheses from multi-world inputs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "collision-intelligence" / "src"))

from cae_collision_intelligence.composer import CollisionHypothesisComposer
from cae_collision_intelligence.domain import (
    CollisionRelationType,
    FalsificationCondition,
    ObliqueLens,
)
from cae_collision_intelligence.verifier import CollisionHypothesisVerifier


def test_composer_generates_valid_hypothesis():
    ws_id = "ws-client-99"

    falsification = FalsificationCondition(
        refuting_observation="Cognitive neuroscience papers proving that willpower operates without metabolic glucose limits.",
        disconfirming_testimony="Guest accounts demonstrating that sheer mental force prevented burnout over a 5-year sustained sprint.",
        boundary_limitation="Does not apply to acute emergency crisis responses under 72 hours.",
    )

    lens = ObliqueLens(
        domain_name="Thermodynamics",
        source_reference="Prigogine Dissipative Structures",
        invariant_principle="Open thermodynamic systems must dissipate entropy to maintain internal structural order.",
    )

    hyp = CollisionHypothesisComposer.compose(
        workspace_id=ws_id,
        title="Human Energy as a Dissipative System: Why Willpower Without Dissipation Breaks",
        relation_type=CollisionRelationType.ANALOGY,
        audience_id="AUD-TECH-LEADERS",
        audience_tension_ref="AET-EXHAUSTION",
        guest_id="GST-DR-THORNE",
        guest_lived_proof_citation="Pioneered circadian entropy recovery protocols across 500 venture-backed founders",
        research_signal_id="SIG-SIGNAL-001",
        bridge_statement="Applying thermodynamic dissipative structures to cognitive labor reveals why willpower cannot replace biological recovery entropy cycles.",
        falsification_condition=falsification,
        evidence_references=["https://nature.com/articles/entropy-cognition-2026", "guest_onboarding_session_1"],
        oblique_lens=lens,
        surprise_score=0.88,
        emotion_score=0.82,
        specificity_score=0.91,
    )

    assert hyp.title.startswith("Human Energy")
    assert hyp.heritage_eval.composite_viral_potential > 0.70
    assert CollisionHypothesisVerifier.verify(hyp) is True
