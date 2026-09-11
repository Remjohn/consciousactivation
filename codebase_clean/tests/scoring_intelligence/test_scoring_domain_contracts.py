"""
test_scoring_domain_contracts.py
--------------------------------
Validates CandidateEvaluationProfile and EditorialBoard serialization, typing, and schema integrity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "scoring-intelligence" / "src"))

from cae_scoring_intelligence.domain import GateStatus
from cae_scoring_intelligence.evaluator import MultiDimensionalCandidateEvaluator
from cae_scoring_intelligence.verifier import EditorialBoardVerifier


def test_candidate_evaluation_profile_and_provenance():
    text = "We built a multi-region database replication system to prevent catastrophic downtime during data center outages."

    profile = MultiDimensionalCandidateEvaluator.evaluate(
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        text_content=text,
        semantic_strength=0.90,
        guest_authenticity=0.88,
        audience_relevance=0.85,
        novelty=0.80,
        narrative_utility=0.75,
        visual_opportunity=0.70,
        editorial_completeness=0.95,
        distribution_potential=0.65,
    )

    assert profile.profile_id.startswith("EVP-")
    assert profile.candidate_id == "CND-001"
    assert profile.gate_status == GateStatus.PASSED
    assert profile.is_eligible_for_board is True
    assert profile.provenance.evaluator_id == "EVAL-CMF-HERITAGE-V2"
    assert profile.scores.weighted_composite_score > 0.75
