"""
test_collision_adversarial_cases.py
-----------------------------------
Adversarial and false-proof test suite defending against ungrounded analogies, clichés, and vector fallacies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "collision-intelligence" / "src"))

import pytest

from cae_collision_intelligence.composer import CollisionHypothesisComposer
from cae_collision_intelligence.domain import (
    CollisionHypothesis,
    CollisionRelationType,
    FalsificationCondition,
    HeritageCMFEval,
    NoveltyClicheAssessment,
)
from cae_collision_intelligence.errors import (
    ClicheTropeError,
    MissingFalsificationError,
    UngroundedAnalogyError,
    VectorTruthFallacyError,
)
from cae_collision_intelligence.verifier import CollisionHypothesisVerifier


def create_base_falsification() -> FalsificationCondition:
    return FalsificationCondition(
        refuting_observation="Empirical counter-study proving the null hypothesis across randomized trials.",
        disconfirming_testimony="Guest lived contradiction showing the reverse mechanism occurred in practice.",
        boundary_limitation="Valid only under high-complexity knowledge work environments.",
    )


def test_ungrounded_analogy_rejection():
    # Attempting to compose an analogy where guest has zero lived proof / authority
    with pytest.raises(UngroundedAnalogyError, match="Guest lived proof citation is missing"):
        CollisionHypothesisComposer.compose(
            workspace_id="ws-client-99",
            title="Clever Metaphor Without Authority",
            relation_type=CollisionRelationType.ANALOGY,
            audience_id="AUD-1",
            audience_tension_ref="AET-1",
            guest_id="GST-1",
            guest_lived_proof_citation="",  # Empty proof!
            research_signal_id="SIG-1",
            bridge_statement="A witty poetic analogy comparing quantum spin to marketing funnels.",
            falsification_condition=create_base_falsification(),
            evidence_references=["https://example.com/test"],
        )


def test_generic_viral_cliche_recombination_quarantine():
    # Hypothesis packed with generic viral tropes: '10x your', 'secret hack', 'unlock your potential'
    cliche_bridge = "Use this 10x your secret hack to unlock your potential and crush your goals!"

    hyp = CollisionHypothesisComposer.compose(
        workspace_id="ws-client-99",
        title="Generic Viral Trope Title",
        relation_type=CollisionRelationType.INVERSION,
        audience_id="AUD-1",
        audience_tension_ref="AET-1",
        guest_id="GST-1",
        guest_lived_proof_citation="10 years running high performance executive coaching",
        research_signal_id="SIG-1",
        bridge_statement=cliche_bridge,
        falsification_condition=create_base_falsification(),
        evidence_references=["https://example.com/test"],
    )

    assert hyp.novelty_assessment.is_cliche_quarantined is True

    with pytest.raises(ClicheTropeError, match="quarantined due to excessive cliché"):
        CollisionHypothesisVerifier.verify(hyp)


def test_missing_falsification_condition_rejection():
    # Use model_construct to test Verifier's explicit gate on invalid/empty conditions
    invalid_falsification = FalsificationCondition.model_construct(
        refuting_observation="",  # Empty!
        disconfirming_testimony="Valid testimony",
        boundary_limitation="Valid boundary",
    )

    hyp = CollisionHypothesis.model_construct(
        workspace_id="ws-client-99",
        title="Unfalsifiable Pseudo-Thesis",
        relation_type=CollisionRelationType.SYSTEMS_LENS,
        audience_id="AUD-1",
        audience_tension_ref="AET-1",
        guest_id="GST-1",
        guest_lived_proof_citation="Valid guest proof citation over 10 characters",
        research_signal_id="SIG-1",
        bridge_statement="A long enough bridge statement to pass basic length checks.",
        evidence_references=["ref_1"],
        novelty_assessment=NoveltyClicheAssessment(
            semantic_distance_score=0.8,
            cliche_risk_score=0.1,
            trope_penalty=0.0,
            is_cliche_quarantined=False,
        ),
        falsification_condition=invalid_falsification,
        heritage_eval=HeritageCMFEval(
            surprise_score=0.8,
            emotion_score=0.8,
            specificity_score=0.8,
            ai_slop_risk=0.1,
            composite_viral_potential=0.75,
        ),
        metadata={},
    )

    with pytest.raises(MissingFalsificationError, match="lacks explicit refuting observation"):
        CollisionHypothesisVerifier.verify(hyp)


def test_vector_truth_fallacy_rejection():
    hyp = CollisionHypothesis(
        workspace_id="ws-client-99",
        title="Vector Similarity Claim",
        relation_type=CollisionRelationType.ANALOGY,
        audience_id="AUD-1",
        audience_tension_ref="AET-1",
        guest_id="GST-1",
        guest_lived_proof_citation="Valid guest proof citation over 10 characters",
        research_signal_id="SIG-1",
        bridge_statement="A long enough bridge statement to pass basic length checks.",
        evidence_references=["ref_1"],
        novelty_assessment=NoveltyClicheAssessment(
            semantic_distance_score=0.8,
            cliche_risk_score=0.1,
            trope_penalty=0.0,
            is_cliche_quarantined=False,
        ),
        falsification_condition=create_base_falsification(),
        heritage_eval=HeritageCMFEval(
            surprise_score=0.8,
            emotion_score=0.8,
            specificity_score=0.8,
            ai_slop_risk=0.1,
            composite_viral_potential=0.75,
        ),
        metadata={"is_derived_solely_from_vector_similarity": True},
    )

    with pytest.raises(VectorTruthFallacyError, match="Semantic embedding proximity alone cannot substantiate editorial truth"):
        CollisionHypothesisVerifier.verify(hyp)
