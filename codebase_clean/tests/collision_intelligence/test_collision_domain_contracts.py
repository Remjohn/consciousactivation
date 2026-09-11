"""
test_collision_domain_contracts.py
----------------------------------
Validates CollisionHypothesis serialization, fields, and relation typing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "collision-intelligence" / "src"))

from cae_collision_intelligence.domain import (
    CollisionHypothesis,
    CollisionRelationType,
    FalsificationCondition,
    HeritageCMFEval,
    NoveltyClicheAssessment,
    ObliqueLens,
)
from cae_collision_intelligence.verifier import CollisionHypothesisVerifier


def test_collision_hypothesis_creation_and_serialization():
    ws_id = "ws-client-99"

    lens = ObliqueLens(
        domain_name="Evolutionary Biology",
        source_reference="The Selfish Gene (Dawkins)",
        invariant_principle="Evolutionary fitness landscapes favor local optima over global efficiency.",
    )

    falsification = FalsificationCondition(
        refuting_observation="Evidence showing that unconstrained systems self-regulate without external selective pressure.",
        disconfirming_testimony="Guest testimony stating burnout occurred purely due to isolated biochemical factors rather than systemic incentives.",
        boundary_limitation="Applies strictly to competitive institutional environments, not self-directed creative flow.",
    )

    novelty = NoveltyClicheAssessment(
        semantic_distance_score=0.88,
        cliche_risk_score=0.10,
        trope_penalty=0.05,
        is_cliche_quarantined=False,
    )

    cmf = HeritageCMFEval(
        surprise_score=0.85,
        emotion_score=0.80,
        specificity_score=0.90,
        ai_slop_risk=0.10,
        composite_viral_potential=0.76,
    )

    hyp = CollisionHypothesis(
        workspace_id=ws_id,
        title="Burnout as a Rational Local Optimum in Misaligned Incentive Landscapes",
        relation_type=CollisionRelationType.SYSTEMS_LENS,
        audience_id="AUD-100",
        audience_tension_ref="AET-BURNOUT",
        guest_id="GST-200",
        guest_lived_proof_citation="12 years directing clinical ICU teams while reforming hospital shift schedules",
        research_signal_id="SIG-LATENT-VSP",
        oblique_lens=lens,
        bridge_statement="When institutional selection rewards raw throughput over systemic health, burnout is not personal failure but the biological local optimum.",
        evidence_references=["arxiv:2501.9999", "interview_turn_42"],
        novelty_assessment=novelty,
        falsification_condition=falsification,
        heritage_eval=cmf,
    )

    assert hyp.hypothesis_id.startswith("HYP-")
    assert hyp.relation_type == CollisionRelationType.SYSTEMS_LENS
    assert hyp.oblique_lens.domain_name == "Evolutionary Biology"
    assert CollisionHypothesisVerifier.verify(hyp) is True
