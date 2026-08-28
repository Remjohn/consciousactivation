"""
test_four_world_intersection.py
-------------------------------
Tests multi-world intersections across all 5 canonical collision relation types.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "collision-intelligence" / "src"))

from cae_collision_intelligence.composer import CollisionHypothesisComposer
from cae_collision_intelligence.domain import (
    CollisionRelationType,
    FalsificationCondition,
)
from cae_collision_intelligence.verifier import CollisionHypothesisVerifier


def create_base_falsification() -> FalsificationCondition:
    return FalsificationCondition(
        refuting_observation="Empirical counter-study proving the null hypothesis across randomized trials.",
        disconfirming_testimony="Guest lived contradiction showing the reverse mechanism occurred in practice.",
        boundary_limitation="Valid only under high-complexity knowledge work environments.",
    )


def test_all_five_collision_relation_types():
    ws_id = "ws-client-99"
    falsification = create_base_falsification()

    relations = [
        (CollisionRelationType.INVERSION, "Motivation is the Byproduct, Not the Cause of Action"),
        (CollisionRelationType.PARADOX, "Extreme Strategic Restraint Unlocks Maximum Creative Velocity"),
        (CollisionRelationType.SYSTEMS_LENS, "Team Cynicism as an Information Signal Rather Than Cultural Toxicity"),
        (CollisionRelationType.ANALOGY, "Neural Pruning Invariants in Corporate Restructuring"),
        (CollisionRelationType.COUNTER_POSITION, "Why Portfolio Diversification is a Symptom of Conviction Collapse"),
    ]

    for rel_type, title in relations:
        hyp = CollisionHypothesisComposer.compose(
            workspace_id=ws_id,
            title=title,
            relation_type=rel_type,
            audience_id="AUD-EXEC",
            audience_tension_ref="AET-TENSION",
            guest_id="GST-AUTHORITY",
            guest_lived_proof_citation="15 years scaling high-reliability organizations through enterprise restructuring",
            research_signal_id="SIG-SIGNAL-123",
            bridge_statement=f"Structural collision proving {title} using verified operational evidence.",
            falsification_condition=falsification,
            evidence_references=["https://hbr.org/case-study-2026", "guest_interview_turn_10"],
        )

        assert hyp.relation_type == rel_type
        assert CollisionHypothesisVerifier.verify(hyp) is True
