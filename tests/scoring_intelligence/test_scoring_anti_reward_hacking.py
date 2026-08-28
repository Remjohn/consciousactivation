"""
test_scoring_anti_reward_hacking.py
-----------------------------------
Adversarial tests for low-evidence virality, length gaming, keyword stuffing, and gate enforcement.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "scoring-intelligence" / "src"))

import pytest

from cae_scoring_intelligence.domain import (
    CandidateEvaluationProfile,
    DimensionScores,
    EditorialBoard,
    EvaluatorProvenance,
    GateStatus,
)
from cae_scoring_intelligence.errors import (
    KeywordStuffingDetectedError,
    LengthGamingDetectedError,
    LowEvidenceViralityError,
    NonCompensableGateFailureError,
)
from cae_scoring_intelligence.evaluator import MultiDimensionalCandidateEvaluator
from cae_scoring_intelligence.verifier import EditorialBoardVerifier


def test_high_virality_low_evidence_rejection():
    # Attempting to assign high distribution potential (>0.80) with low authenticity (<0.50)
    with pytest.raises(LowEvidenceViralityError, match="violates grounding"):
        MultiDimensionalCandidateEvaluator.evaluate(
            candidate_id="CND-CLICKBAIT",
            workspace_id="ws-client-99",
            text_content="A viral marketing hook with unverified claims.",
            semantic_strength=0.40,
            guest_authenticity=0.30,  # VIOLATION! <0.50 while distribution > 0.80
            audience_relevance=0.80,
            novelty=0.70,
            narrative_utility=0.50,
            visual_opportunity=0.60,
            editorial_completeness=0.80,
            distribution_potential=0.95,  # HIGH VIRALITY
        )


def test_length_gaming_rejection():
    # Highly repetitive padded text to game word counts
    repetitive_text = " ".join(["we repeat this same sentence over and over again without adding any new meaning"] * 15)

    with pytest.raises(LengthGamingDetectedError, match="length gaming"):
        MultiDimensionalCandidateEvaluator.evaluate(
            candidate_id="CND-GAMING",
            workspace_id="ws-client-99",
            text_content=repetitive_text,
            semantic_strength=0.60,
            guest_authenticity=0.60,
            audience_relevance=0.60,
            novelty=0.50,
            narrative_utility=0.50,
            visual_opportunity=0.50,
            editorial_completeness=0.60,
            distribution_potential=0.50,
        )


def test_keyword_stuffing_rejection():
    # Text stuffed with sensationalist clickbait keywords
    stuffed_text = "This shocking secret will make you a millionaire with insane miracle hacks exposed."

    with pytest.raises(KeywordStuffingDetectedError, match="keyword stuffing"):
        MultiDimensionalCandidateEvaluator.evaluate(
            candidate_id="CND-STUFFED",
            workspace_id="ws-client-99",
            text_content=stuffed_text,
            semantic_strength=0.50,
            guest_authenticity=0.50,
            audience_relevance=0.50,
            novelty=0.50,
            narrative_utility=0.50,
            visual_opportunity=0.50,
            editorial_completeness=0.50,
            distribution_potential=0.50,
        )


def test_non_compensable_gate_enforcement_in_board():
    # Profile that failed gate cannot be verified on board if marked is_eligible_for_board=True
    scores = DimensionScores.calculate_composite(
        semantic_strength=0.7,
        guest_authenticity=0.3,
        audience_relevance=0.7,
        novelty=0.7,
        narrative_utility=0.7,
        visual_opportunity=0.7,
        editorial_completeness=0.7,
        distribution_potential=0.7,
    )
    prov = EvaluatorProvenance(evaluator_id="EVAL-TEST", evaluator_version="1.0", rationale="Test validation rationale")

    bad_profile = CandidateEvaluationProfile(
        candidate_id="CND-BAD",
        workspace_id="ws-client-99",
        scores=scores,
        gate_status=GateStatus.FAILED_AUTHENTICITY,
        is_eligible_for_board=True,  # CONSTITUTIONAL VIOLATION!
        provenance=prov,
    )

    board = EditorialBoard(
        workspace_id="ws-client-99",
        evaluated_candidates=[bad_profile],
        clusters=[],
    )

    with pytest.raises(NonCompensableGateFailureError, match="failed gate"):
        EditorialBoardVerifier.verify_board(board)
