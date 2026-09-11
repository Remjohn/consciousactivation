"""
test_clustering_coverage_and_redundancy.py
------------------------------------------
Tests candidate clustering, thematic coverage, and redundancy detection.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "scoring-intelligence" / "src"))

from cae_scoring_intelligence.clusterer import CandidateClusterEngine
from cae_scoring_intelligence.evaluator import MultiDimensionalCandidateEvaluator
from cae_scoring_intelligence.verifier import EditorialBoardVerifier


def test_clustering_and_board_generation():
    p1 = MultiDimensionalCandidateEvaluator.evaluate(
        candidate_id="CND-101",
        workspace_id="ws-client-99",
        text_content="Our database outage story.",
        semantic_strength=0.9,
        guest_authenticity=0.9,
        audience_relevance=0.8,
        novelty=0.8,
        narrative_utility=0.8,
        visual_opportunity=0.7,
        editorial_completeness=0.9,
        distribution_potential=0.6,
    )

    p2 = MultiDimensionalCandidateEvaluator.evaluate(
        candidate_id="CND-102",
        workspace_id="ws-client-99",
        text_content="Another perspective on the database failure.",
        semantic_strength=0.85,
        guest_authenticity=0.85,
        audience_relevance=0.8,
        novelty=0.75,
        narrative_utility=0.75,
        visual_opportunity=0.6,
        editorial_completeness=0.85,
        distribution_potential=0.6,
    )

    theme_map = {
        "Infrastructure Resilience": ["CND-101", "CND-102"],
    }

    board = CandidateClusterEngine.form_clusters(
        workspace_id="ws-client-99",
        evaluations=[p1, p2],
        theme_map=theme_map,
    )

    assert len(board.clusters) == 1
    assert board.clusters[0].theme == "Infrastructure Resilience"
    assert board.clusters[0].redundancy_index == 0.35  # 2 candidates
    assert EditorialBoardVerifier.verify_board(board) is True
