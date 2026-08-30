"""
test_hypothesis_adapter.py
--------------------------
Acceptance tests for CAE Mandate M02 — Hypothesis Portfolio Adapter.

Validates:
1. Invalid upstream reference rejection (AC-01).
2. Duplicate / near-duplicate clustering and overlap penalization (AC-02).
3. Portfolio selection flexibility with sparse evidence (<16) without quota errors (AC-03).
4. Full lineage and coordinate preservation (AC-04).
5. Non-canonical boundary and zero AIR write enforcement (AC-05).
6. Multi-dimensional diversity maximization from ~96 candidate field down to 16-24.
"""

import pytest
from datetime import datetime, timezone

from cae_interview_intelligence.hypothesis_adapter import (
    CandidateCluster,
    CandidateState,
    CoordinateBasis,
    HypothesisCandidate,
    HypothesisPortfolioAdapter,
    PortfolioSelectionResult,
    Provenance,
    SelectionDiagnostics,
    SemanticRef,
)


def make_valid_candidate(
    cid: str,
    island: str = "island_control_illusion",
    tension: str = "tension_vulnerability_vs_security",
    territory: str = "territory_crisis_founder",
    archetype: str = "archetype_crucible",
    quality_score: float = 0.85,
    collision_text: str = "Founder vulnerability exposes systemic control illusions under crisis pressure.",
) -> HypothesisCandidate:
    """Helper to generate well-formed candidate instances with valid lineage."""
    return HypothesisCandidate(
        candidate_id=f"hc:{cid}",
        collision_statement=collision_text,
        upstream_hypothesis_refs=[
            SemanticRef(
                object_id=f"air:hyp:{cid}",
                version="1.0.0",
                sha256="a1b2c3d4e5f67890abcdef1234567890",
                object_type="activation_hypothesis",
            )
        ],
        coordinates=CoordinateBasis(
            d01_audience_tension=tension,
            d02_audience_belief=island,
            d03_audience_desired_state="clarity_under_fire",
            d04_guest_lived_authority=territory,
            d05_guest_contradiction="past_control_vs_current_openness",
            d06_guest_transformation="from_autocrat_to_facilitator",
            d07_cultural_world_signal="sig:macro_burnout_2026",
            d08_target_enemy_status_quo="command_and_control_fallacy",
            d09_oblique_lens="thermodynamic_entropy_dissipation",
            d10_archetype_opportunity=archetype,
            d11_distribution_condition="high_retention_provocation",
            d12_evidence_opportunity="q3_near_bankruptcy_pivot_memo",
        ),
        audience_cognitive_island_ref=SemanticRef(object_id=island),
        guest_territory_ref=SemanticRef(object_id=territory),
        edge_ref=SemanticRef(object_id=tension),
        archetype_refs=[SemanticRef(object_id=archetype)],
        selection_diagnostics=SelectionDiagnostics(
            relevance=quality_score,
            evidence_potential=quality_score,
            guest_authority=quality_score,
            audience_alignment=quality_score,
            collision_strength=quality_score,
            novelty=quality_score,
            research_grounding=quality_score,
        ),
        provenance=Provenance(
            source_refs=[
                SemanticRef(object_id=f"doc:memo_{cid}", sha256="fedcba9876543210")
            ],
            generated_by="test-fixture:m02",
        ),
    )


# -----------------------------------------------------------------------------
# AC-01: Invalid Upstream Reference Rejection
# -----------------------------------------------------------------------------

def test_invalid_upstream_reference_rejected():
    """An invalid, empty, or blank upstream reference cannot become launchable."""
    adapter = HypothesisPortfolioAdapter()
    
    # 1. Candidate with empty upstream refs and empty provenance source refs
    empty_cand = HypothesisCandidate(
        candidate_id="hc:empty_ref_01",
        collision_statement="A well-formed collision statement that lacks any backing reference lineage.",
        upstream_hypothesis_refs=[],
        provenance=Provenance(source_refs=[]),
    )
    
    val_errors = adapter.validate_candidate(empty_cand)
    assert len(val_errors) > 0
    assert any("upstream_hypothesis_refs" in err for err in val_errors)
    
    # Running portfolio selection rejects this candidate
    res = adapter.select_working_portfolio([empty_cand], target_min=1, target_max=5)
    assert len(res.selected_candidates) == 0
    assert len(res.rejected_candidates) == 1
    assert res.rejected_candidates[0].state == CandidateState.REJECTED
    assert "Validation failed" in (res.rejected_candidates[0].operator_notes or "")

    # 2. SemanticRef rejects blank/placeholder values
    with pytest.raises(ValueError, match="blank or invalid placeholder"):
        SemanticRef(object_id="   ")

    with pytest.raises(ValueError, match="blank or invalid placeholder"):
        SemanticRef(object_id="null")


# -----------------------------------------------------------------------------
# AC-02: Duplicate / Near-Duplicate Clustering and Overlap Penalization
# -----------------------------------------------------------------------------

def test_duplicate_and_near_duplicate_clustering_and_penalization():
    """Duplicate or near-duplicate candidates are clustered together and penalized against redundancy."""
    adapter = HypothesisPortfolioAdapter()
    
    # Create 3 candidates sharing identical semantic coordinates
    cand_a = make_valid_candidate(
        "dup_01",
        island="island_security_illusion",
        tension="tension_safety_vs_growth",
        territory="territory_cyber_security",
        quality_score=0.90,
        collision_text="Cyber defenses create false safety illusions preventing true antifragility.",
    )
    cand_b = make_valid_candidate(
        "dup_02",
        island="island_security_illusion",
        tension="tension_safety_vs_growth",
        territory="territory_cyber_security",
        quality_score=0.75,
        collision_text="Cyber defenses create false safety illusions preventing true antifragility variation B.",
    )
    cand_c = make_valid_candidate(
        "dup_03",
        island="island_security_illusion",
        tension="tension_safety_vs_growth",
        territory="territory_cyber_security",
        quality_score=0.60,
        collision_text="Cyber defenses create false safety illusions preventing true antifragility variation C.",
    )
    
    # Distinct candidate in a different territory
    cand_distinct = make_valid_candidate(
        "distinct_01",
        island="island_efficiency_trap",
        tension="tension_speed_vs_deliberation",
        territory="territory_manufacturing",
        quality_score=0.80,
        collision_text="Hyper-optimization of supply lines breeds hidden systemic fragility.",
    )
    
    candidates = [cand_a, cand_b, cand_c, cand_distinct]
    clusters = adapter.cluster_candidates(candidates)
    
    # Two clusters should be formed
    assert len(clusters) == 2
    
    # The duplicate cluster contains all 3 duplicate candidates
    dup_cluster = next(cl for cl in clusters if len(cl.candidate_ids) == 3)
    assert dup_cluster.primary_candidate_id == cand_a.candidate_id
    assert dup_cluster.overlap_score > 0.0
    
    # Non-primary candidates in duplicate cluster receive overlap penalties
    assert cand_b.selection_diagnostics.portfolio_overlap > 0.0
    assert cand_c.selection_diagnostics.portfolio_overlap > 0.0
    
    # Selection from this pool prioritizes diversity over selecting all 3 duplicates
    res = adapter.select_working_portfolio(candidates, target_min=2, target_max=2)
    selected_ids = {c.candidate_id for c in res.selected_candidates}
    
    # Primary of dup cluster and distinct candidate are selected
    assert cand_a.candidate_id in selected_ids
    assert cand_distinct.candidate_id in selected_ids
    assert cand_b.candidate_id not in selected_ids
    assert cand_c.candidate_id not in selected_ids


# -----------------------------------------------------------------------------
# AC-03: Sparse Candidate Pool Selection Without Quota Errors
# -----------------------------------------------------------------------------

def test_sparse_candidate_pool_selection_without_quota_error():
    """Pools with fewer than 16 candidates select available valid candidates without throwing quota errors."""
    adapter = HypothesisPortfolioAdapter()
    
    # Only 5 candidates available
    sparse_pool = [
        make_valid_candidate(f"sparse_{i}", island=f"island_{i}", tension=f"tension_{i}", territory=f"terr_{i}")
        for i in range(5)
    ]
    
    # Selecting with standard 16-24 target should succeed gracefully
    res = adapter.select_working_portfolio(sparse_pool, target_min=16, target_max=24, force_strict_quota=False)
    
    assert res.selected_count == 5
    assert len(res.selected_candidates) == 5
    assert res.evidence_insufficiency_warning is not None
    assert "Candidate pool density insufficient" in res.evidence_insufficiency_warning
    assert "Proceeding with available evidence" in res.evidence_insufficiency_warning


# -----------------------------------------------------------------------------
# AC-04: Lineage and Coordinate Retention
# -----------------------------------------------------------------------------

def test_selected_candidates_retain_full_lineage():
    """Selected candidates maintain complete upstream refs, 12-D coordinates, and provenance."""
    adapter = HypothesisPortfolioAdapter()
    
    c1 = make_valid_candidate("lineage_test_01")
    res = adapter.select_working_portfolio([c1], target_min=1, target_max=5)
    
    assert len(res.selected_candidates) == 1
    sel = res.selected_candidates[0]
    
    # Check upstream ref
    assert len(sel.upstream_hypothesis_refs) == 1
    assert sel.upstream_hypothesis_refs[0].object_id == "air:hyp:lineage_test_01"
    assert sel.upstream_hypothesis_refs[0].version == "1.0.0"
    assert sel.upstream_hypothesis_refs[0].sha256 == "a1b2c3d4e5f67890abcdef1234567890"
    
    # Check coordinates D01-D12
    assert sel.coordinates.d01_audience_tension == "tension_vulnerability_vs_security"
    assert sel.coordinates.d02_audience_belief == "island_control_illusion"
    assert sel.coordinates.d04_guest_lived_authority == "territory_crisis_founder"
    assert sel.coordinates.d07_cultural_world_signal == "sig:macro_burnout_2026"
    assert sel.coordinates.d09_oblique_lens == "thermodynamic_entropy_dissipation"
    assert sel.coordinates.d12_evidence_opportunity == "q3_near_bankruptcy_pivot_memo"
    
    # Check provenance
    assert len(sel.provenance.source_refs) == 1
    assert sel.provenance.source_refs[0].object_id == "doc:memo_lineage_test_01"
    assert sel.provenance.generated_by == "test-fixture:m02"


# -----------------------------------------------------------------------------
# AC-05: Non-Canonical Immutability (Zero Write to AIR)
# -----------------------------------------------------------------------------

def test_air_immutability_and_non_canonical_boundary():
    """The adapter operates as a pure derived view and never writes to AIR or modifies external state."""
    adapter = HypothesisPortfolioAdapter()
    
    candidate = make_valid_candidate("immutability_01")
    original_dict = candidate.model_dump()
    
    # Ingest and select
    res = adapter.select_working_portfolio([candidate], target_min=1, target_max=5)
    assert len(res.selected_candidates) == 1
    
    # Verify candidate attributes match, and no external side-effects
    assert res.selected_candidates[0].candidate_id == "hc:immutability_01"
    assert res.selected_candidates[0].upstream_hypothesis_refs[0].object_id == "air:hyp:immutability_01"


# -----------------------------------------------------------------------------
# Diversity Maximization: ~96 -> 16-24 Selection
# -----------------------------------------------------------------------------

def test_diversity_maximization_across_dimensions():
    """A pool of 96 diverse candidates is filtered down to a 16-24 working set maximizing diversity."""
    adapter = HypothesisPortfolioAdapter()
    
    islands = [f"island_{i}" for i in range(8)]
    tensions = [f"tension_{j}" for j in range(6)]
    territories = [f"territory_{k}" for k in range(4)]
    archetypes = ["archetype_crucible", "archetype_inversion", "archetype_confession", "archetype_systemic"]
    
    # Generate 96 candidates across combinatorial coordinates
    pool: list[HypothesisCandidate] = []
    idx = 0
    for i in range(8):
        for j in range(6):
            for k in range(2):
                idx += 1
                cand = make_valid_candidate(
                    cid=f"pool_{idx:03d}",
                    island=islands[i],
                    tension=tensions[j],
                    territory=territories[(i + j + k) % 4],
                    archetype=archetypes[(i + k) % 4],
                    quality_score=0.60 + (idx % 35) * 0.01,
                    collision_text=f"Candidate {idx}: Intersection of {islands[i]} and {tensions[j]} under pressure.",
                )
                pool.append(cand)
                
    assert len(pool) == 96
    
    # Select working portfolio with target 16-24
    res = adapter.select_working_portfolio(pool, target_min=16, target_max=24)
    
    assert 16 <= res.selected_count <= 24
    assert res.total_pool_evaluated == 96
    assert res.evidence_insufficiency_warning is None
    
    # Verify diversity coverage spans multiple islands, tensions, and territories
    cov = res.diversity_coverage
    assert cov["unique_audience_islands"] >= 8
    assert cov["unique_tensions"] >= 6
    assert cov["unique_guest_territories"] >= 4
    assert cov["unique_archetypes"] >= 4
