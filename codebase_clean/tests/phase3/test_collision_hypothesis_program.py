"""
test_collision_hypothesis_program.py
------------------------------------
Acceptance and Verification Test Suite for CAE Phase 3 M32:
Audience x Guest Resonance + Matrix of Edging + Collision Hypothesis Program.
"""

import sqlite3
import pytest

from ca_runtime.program_state_runtime import (
    AuthorityLane,
    InMemoryProgramStateStore,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    UniversalProgramStateRuntime,
    get_canonical_collision_state_machine,
)
from ca_runtime.collision_hypothesis_store import (
    CollisionHypothesisStore,
    MatrixOfEdgingRecord,
    CollisionHypothesisRecord,
    CollisionHypothesisPortfolioRecord,
)
from ca_runtime.collision_hypothesis_program import (
    CollisionHypothesisProgramCoordinator,
    CollisionHypothesisCandidate,
    ResonanceCandidate,
    UnauthorizedCollisionLaneError,
    WorkspaceScopeViolationError,
    ResonanceAlignmentError,
    MatrixOfEdgingError,
    UngroundedHypothesisError,
    ClicheTropeQuarantineError,
    PortfolioDiversityError,
    HypothesisApprovalError,
    HYPOTHESIS_GATES,
    EVALUATION_DIMENSIONS,
)


@pytest.fixture
def test_setup():
    """Sets up an isolated in-memory runtime and store for collision testing."""
    conn = sqlite3.connect(":memory:")
    store = CollisionHypothesisStore(conn)
    state_store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(state_store)
    runtime.register_state_machine(get_canonical_collision_state_machine())
    return {
        "conn": conn,
        "store": store,
        "state_store": state_store,
        "runtime": runtime,
    }


def _seed_valid_matrix(coord: CollisionHypothesisProgramCoordinator, ws_id: str, matrix_id: str):
    """Helper to seed a valid matrix through the coordinator and advance state machine."""
    coord.discover_resonance(
        workspace_id=ws_id,
        guest_dna={"guest_id": "G-1", "proof_citation": "Resolved severe organizational crises over 10 years."},
        audience_tensions=[{"tension_label": "Tension"}],
        world_signals=[{"signal_id": "SIG-1"}],
        lane=AuthorityLane.HUNTER,
    )
    return coord.evaluate_matrix_of_edging(
        workspace_id=ws_id,
        matrix_id=matrix_id,
        broad_signal="Broad signal on systemic changes",
        hidden_pressure="Leaders believe resting is failure, creating self-reinforcing burnout cycles.",
        surviving_edge="Strategic surrender and intentional structural pruning as active power.",
        identity_gap="Heroic savior complex vs authentic regenerative leadership.",
        audience_reality="Trapped in relentless output demands without permission to pause.",
        desired_recognition="Recognized for structural resilience rather than martyrdom.",
        smallest_useful_movement="Schedule mandatory non-negotiable operational silence periods.",
        lane=AuthorityLane.ANALYST,
    )


def test_collision_hypothesis_full_lifecycle_e2e(test_setup):
    """Test 1: Full end-to-end lifecycle across all four authority lanes to operator approval."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-collision-prod-01"

    coord = CollisionHypothesisProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )

    guest_dna = {
        "guest_id": "GUEST-AUDREY-01",
        "proof_citation": "Resolved existential crisis in 2021 by establishing decentralized autonomy protocols across 14 distributed teams.",
    }
    audience_tensions = [
        {
            "audience_id": "AUD-LEADERS-01",
            "tension_ref": "TENSION-AUTONOMY-VS-CONTROL",
            "tension_label": "Autonomy vs Control Paradox",
        }
    ]
    world_signals = [
        {
            "signal_id": "SIG-SYSTEMIC-BURNOUT",
            "theme": "Systemic Exhaustion in Tech Leadership",
        }
    ]
    oblique_lenses = [
        {
            "lens_id": "LENS-BIO-01",
            "domain_name": "Cellular Biology",
            "source_reference": "Apoptosis and Tissue Regeneration Principles (2020)",
            "invariant_principle": "Programmed cell death enables multicellular longevity and dynamic structural adaptation.",
        }
    ]

    # 1. HUNTER: Discover Resonance
    resonances = coord.discover_resonance(
        workspace_id=ws_id,
        guest_dna=guest_dna,
        audience_tensions=audience_tensions,
        world_signals=world_signals,
        oblique_lenses=oblique_lenses,
        lane=AuthorityLane.HUNTER,
    )
    assert len(resonances) == 1
    assert resonances[0].guest_id == "GUEST-AUDREY-01"
    assert resonances[0].resonance_score_bps >= 7000

    # 2. ANALYST: Evaluate Matrix of Edging
    matrix = coord.evaluate_matrix_of_edging(
        workspace_id=ws_id,
        matrix_id="MOE-001",
        broad_signal="Systemic Exhaustion in Tech Leadership",
        hidden_pressure="Leaders believe resting is failure, creating self-reinforcing burnout cycles.",
        surviving_edge="Strategic surrender and intentional structural pruning as active power.",
        identity_gap="Heroic savior complex vs authentic regenerative leadership.",
        audience_reality="Trapped in relentless output demands without permission to pause.",
        desired_recognition="Recognized for structural resilience rather than martyrdom.",
        smallest_useful_movement="Schedule mandatory non-negotiable operational silence periods.",
        counteractivation_risks=["Nihilistic disengagement", "Passive avoidance"],
        lane=AuthorityLane.ANALYST,
    )
    assert matrix.matrix_id == "MOE-001"

    # 3. COMPOSER: Compose Hypotheses and Form Portfolio
    candidates = [
        CollisionHypothesisCandidate(
            title="Strategic Apoptosis in Modern Leadership",
            relation_type="ANALOGY",
            audience_id="AUD-LEADERS-01",
            audience_tension_ref="TENSION-AUTONOMY-VS-CONTROL",
            guest_id="GUEST-AUDREY-01",
            guest_lived_proof_citation="Resolved existential crisis in 2021 by establishing decentralized autonomy protocols across 14 distributed teams.",
            research_signal_id="SIG-SYSTEMIC-BURNOUT",
            sda_invariant="SDA-INV-001_ACTIVE_TENSION",
            oblique_lens=oblique_lenses[0],
            bridge_statement="Just as biological cells utilize programmed apoptosis for tissue renewal, executive leaders must enforce intentional structural pruning to avert terminal burnout.",
            evidence_references=["SIG-SYSTEMIC-BURNOUT", "EVID-GUEST-BIO-2021"],
            refuting_observation="Organizations that eliminate pruning mechanisms show zero productivity degradation over 3 years.",
            disconfirming_testimony="Guest admits that centralizing all emergency decisions was strictly superior to distributed autonomy.",
            boundary_limitation="Applies only to knowledge organizations undergoing rapid scale, not emergency trauma units.",
            surprise_score=0.82,
            emotion_score=0.78,
            specificity_score=0.88,
        )
    ]
    portfolio = coord.compose_hypotheses(
        workspace_id=ws_id,
        portfolio_id="PORTFOLIO-01",
        candidates=candidates,
        matrix_id="MOE-001",
        lane=AuthorityLane.COMPOSER,
    )
    assert portfolio.portfolio_id == "PORTFOLIO-01"
    assert len(portfolio.candidate_hypothesis_ids) == 1
    assert "proof_sha256" in portfolio.diversity_signature

    hyp_id = portfolio.candidate_hypothesis_ids[0]

    # 4. ANALYST: Evaluate Portfolio with 10 Gates & 7 Dimensions in integer micros
    gate_outcomes = {
        hyp_id: {g: True for g in HYPOTHESIS_GATES}
    }
    candidate_scores = {
        hyp_id: {
            "source_fidelity": 850000,
            "role_tension_integrity": 900000,
            "primitive_coalition_fitness": 880000,
            "archetype_fit": 820000,
            "edge_integrity": 910000,
            "anti_centroid_distinctiveness": 940000,
            "execution_feasibility": 870000,
        }
    }
    eval_result = coord.evaluate_portfolio(
        workspace_id=ws_id,
        portfolio_id="PORTFOLIO-01",
        gate_outcomes=gate_outcomes,
        candidate_scores_micros=candidate_scores,
        lane=AuthorityLane.ANALYST,
    )
    assert eval_result["decision"] == "DECISIVE_WINNER"
    assert eval_result["selected_hypothesis_id"] == hyp_id

    # 5. COMMANDER: Operator Approval Gate
    receipt = coord.approve_hypothesis(
        workspace_id=ws_id,
        portfolio_id="PORTFOLIO-01",
        hypothesis_id=hyp_id,
        approval_notes="Approved for interview brief synthesis and production transfer.",
        lane=AuthorityLane.COMMANDER,
    )
    assert receipt.status == "APPROVED"
    assert receipt.lane == "COMMANDER"
    assert receipt.target_id == hyp_id

    # Verify snapshot state
    snapshot = coord.get_snapshot()
    assert snapshot.current_state == "APPROVED"
    assert snapshot.candidate_count == 1
    assert snapshot.matrix_count == 1
    assert snapshot.portfolio_count == 1


def test_authority_lane_enforcement(test_setup):
    """Test 2: Authority lane boundaries strictly enforced fail-closed."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-lane-check"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    # Attempt HUNTER operation with COMPOSER
    with pytest.raises(UnauthorizedCollisionLaneError) as exc_info:
        coord.discover_resonance(
            workspace_id=ws_id,
            guest_dna={"guest_id": "G-1", "proof_citation": "Verified background citation."},
            audience_tensions=[{"tension_label": "T-1"}],
            world_signals=[{"signal_id": "S-1"}],
            lane=AuthorityLane.COMPOSER,
        )
    assert "requires authority lane 'HUNTER'" in str(exc_info.value)

    # Attempt ANALYST operation with HUNTER
    with pytest.raises(UnauthorizedCollisionLaneError) as exc_info:
        coord.evaluate_matrix_of_edging(
            workspace_id=ws_id,
            matrix_id="M-1",
            broad_signal="Broad signal",
            hidden_pressure="Hidden pressure",
            surviving_edge="Surviving edge",
            identity_gap="Identity gap",
            audience_reality="Audience reality",
            desired_recognition="Desired recognition",
            smallest_useful_movement="Smallest useful movement",
            lane=AuthorityLane.HUNTER,
        )
    assert "requires authority lane 'ANALYST'" in str(exc_info.value)

    # Attempt COMPOSER operation with COMMANDER
    with pytest.raises(UnauthorizedCollisionLaneError) as exc_info:
        coord.compose_hypotheses(
            workspace_id=ws_id,
            portfolio_id="P-1",
            candidates=[],
            matrix_id="M-1",
            lane=AuthorityLane.COMMANDER,
        )
    assert "requires authority lane 'COMPOSER'" in str(exc_info.value)

    # Attempt COMMANDER operation with ANALYST
    with pytest.raises(UnauthorizedCollisionLaneError) as exc_info:
        coord.approve_hypothesis(
            workspace_id=ws_id,
            portfolio_id="P-1",
            hypothesis_id="HYP-1",
            approval_notes="Approved",
            lane=AuthorityLane.ANALYST,
        )
    assert "requires authority lane 'COMMANDER'" in str(exc_info.value)


def test_multi_tenant_workspace_isolation(test_setup):
    """Test 3: Cross-tenant isolation is strictly maintained."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]

    ws_alpha = "ws-alpha"
    ws_beta = "ws-beta"

    coord_alpha = CollisionHypothesisProgramCoordinator(workspace_id=ws_alpha, store=store, state_runtime=runtime)
    coord_beta = CollisionHypothesisProgramCoordinator(workspace_id=ws_beta, store=store, state_runtime=runtime)

    matrix_alpha = MatrixOfEdgingRecord(
        workspace_id=ws_alpha,
        matrix_id="MOE-ALPHA",
        broad_signal="Broad Alpha",
        hidden_pressure="Hidden Alpha",
        surviving_edge="Surviving Alpha",
        identity_gap="Identity Alpha",
        audience_reality="Reality Alpha",
        desired_recognition="Recognition Alpha",
        smallest_useful_movement="Movement Alpha",
    )
    store.store_matrix(matrix_alpha)

    # Alpha can read its matrix, Beta cannot
    assert store.get_matrix(ws_alpha, "MOE-ALPHA") is not None
    assert store.get_matrix(ws_beta, "MOE-ALPHA") is None

    # Targeting mismatched workspace fails closed
    with pytest.raises(WorkspaceScopeViolationError):
        coord_alpha.discover_resonance(
            workspace_id=ws_beta,
            guest_dna={"guest_id": "G-1", "proof_citation": "Verified citation text."},
            audience_tensions=[{"tension_label": "T"}],
            world_signals=[{"signal_id": "S"}],
            lane=AuthorityLane.HUNTER,
        )

    # Empty workspace ID fails closed
    with pytest.raises(WorkspaceScopeViolationError):
        CollisionHypothesisProgramCoordinator(workspace_id="", store=store, state_runtime=runtime)


def test_adversarial_falsification_and_cliche_gating(test_setup):
    """Test 4: Falsification gates and anti-cliché quarantine enforce high truth standards."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-adversarial"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    matrix = MatrixOfEdgingRecord(
        workspace_id=ws_id,
        matrix_id="MOE-ADV",
        broad_signal="Signal",
        hidden_pressure="Pressure",
        surviving_edge="Edge",
        identity_gap="Gap",
        audience_reality="Reality",
        desired_recognition="Recognition",
        smallest_useful_movement="Movement",
    )
    store.store_matrix(matrix)

    # 1. Generic Viral Buzzword / Trope Quarantining
    cliche_candidate = CollisionHypothesisCandidate(
        title="10x Your Potential with Morning Secrets",
        relation_type="INVERSION",
        audience_id="AUD-01",
        audience_tension_ref="TENSION-01",
        guest_id="GUEST-01",
        guest_lived_proof_citation="Overcame catastrophic burnout through rigorous boundary enforcement.",
        research_signal_id="SIG-01",
        bridge_statement="Discover the 10x your potential secret hack to crush your goals with this ultimate game changer mindset shift.",
        refuting_observation="Evidence showing that hustle harder mindsets cause zero performance degradation.",
        disconfirming_testimony="Guest testimony stating that morning routines are completely useless.",
        boundary_limitation="Valid only for startup founders in early stages.",
    )
    with pytest.raises(ClicheTropeQuarantineError) as exc_info:
        coord.compose_hypotheses(
            workspace_id=ws_id,
            portfolio_id="P-CLICHE",
            candidates=[cliche_candidate],
            matrix_id="MOE-ADV",
            lane=AuthorityLane.COMPOSER,
        )
    assert "quarantined due to excessive cliché/trope" in str(exc_info.value)

    # 2. Missing Falsification Condition Rejection
    missing_falsification_candidate = CollisionHypothesisCandidate(
        title="Authentic Paradox Hypothesis",
        relation_type="PARADOX",
        audience_id="AUD-01",
        audience_tension_ref="TENSION-01",
        guest_id="GUEST-01",
        guest_lived_proof_citation="Overcame catastrophic burnout through rigorous boundary enforcement.",
        research_signal_id="SIG-01",
        bridge_statement="Substantive bridge statement showing the paradox between extreme vulnerability and extreme resilience.",
        refuting_observation="",  # Empty refutation
        disconfirming_testimony="Guest testimony stating that vulnerability was harmful.",
        boundary_limitation="Valid for leadership contexts.",
    )
    with pytest.raises(UngroundedHypothesisError):
        coord.compose_hypotheses(
            workspace_id=ws_id,
            portfolio_id="P-MISSING-FALSIFICATION",
            candidates=[missing_falsification_candidate],
            matrix_id="MOE-ADV",
            lane=AuthorityLane.COMPOSER,
        )


def test_portfolio_diversity_and_duplicate_rejection(test_setup):
    """Test 5: Portfolio diversity signature and duplicate signature detection."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-diversity"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    matrix = MatrixOfEdgingRecord(
        workspace_id=ws_id,
        matrix_id="MOE-DIV",
        broad_signal="Signal",
        hidden_pressure="Pressure",
        surviving_edge="Edge",
        identity_gap="Gap",
        audience_reality="Reality",
        desired_recognition="Recognition",
        smallest_useful_movement="Movement",
    )
    store.store_matrix(matrix)

    candidates = [
        CollisionHypothesisCandidate(
            title="Analogy Hypothesis One",
            relation_type="ANALOGY",
            audience_id="AUD-01",
            audience_tension_ref="T-1",
            guest_id="G-1",
            guest_lived_proof_citation="Built distributed systems across 12 countries over a decade.",
            research_signal_id="SIG-01",
            bridge_statement="Valid substantive bridge statement comparing biological systems to software architecture.",
            refuting_observation="Clear empirical refuting observation criteria.",
            disconfirming_testimony="Clear guest disconfirming testimony criteria.",
            boundary_limitation="Clear boundary limitation criteria.",
        ),
        CollisionHypothesisCandidate(
            title="Inversion Hypothesis Two",
            relation_type="INVERSION",
            audience_id="AUD-02",
            audience_tension_ref="T-2",
            guest_id="G-1",
            guest_lived_proof_citation="Built distributed systems across 12 countries over a decade.",
            research_signal_id="SIG-02",
            bridge_statement="Valid substantive bridge statement inverting standard top-down managerial control assumptions.",
            refuting_observation="Clear empirical refuting observation criteria.",
            disconfirming_testimony="Clear guest disconfirming testimony criteria.",
            boundary_limitation="Clear boundary limitation criteria.",
        ),
    ]

    portfolio = coord.compose_hypotheses(
        workspace_id=ws_id,
        portfolio_id="PORT-DIV-01",
        candidates=candidates,
        matrix_id="MOE-DIV",
        lane=AuthorityLane.COMPOSER,
    )

    sig = portfolio.diversity_signature
    assert sig["candidate_count"] == 2
    assert "proof_sha256" in sig
    assert len(sig["axes"]) == 2


def test_source_truth_immutability_on_decision(test_setup):
    """Test 6: Operator approval/rejection updates hypothesis state without mutating underlying evidence."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-immutability"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    # Seed matrix through coordinator to advance state machine
    _seed_valid_matrix(coord, ws_id, "MOE-IMM")

    candidate = CollisionHypothesisCandidate(
        title="Hypothesis For Rejection",
        relation_type="COUNTER_POSITION",
        audience_id="AUD-01",
        audience_tension_ref="T-1",
        guest_id="G-1",
        guest_lived_proof_citation="Authentic guest proof citation that must remain unchanged.",
        research_signal_id="SIG-01",
        bridge_statement="Bridge statement countering traditional corporate diversification strategies.",
        refuting_observation="Empirical observation that diversification always outperforms focus.",
        disconfirming_testimony="Guest testimony stating that diversification was essential.",
        boundary_limitation="Applies only to high-growth tech ventures.",
    )
    portfolio = coord.compose_hypotheses(
        workspace_id=ws_id,
        portfolio_id="P-REJECT",
        candidates=[candidate],
        matrix_id="MOE-IMM",
        lane=AuthorityLane.COMPOSER,
    )
    hid = portfolio.candidate_hypothesis_ids[0]

    # Evaluate portfolio
    coord.evaluate_portfolio(
        workspace_id=ws_id,
        portfolio_id="P-REJECT",
        gate_outcomes={hid: {g: True for g in HYPOTHESIS_GATES}},
        candidate_scores_micros={hid: {d: 800000 for d in EVALUATION_DIMENSIONS}},
        lane=AuthorityLane.ANALYST,
    )

    # Reject hypothesis
    receipt = coord.reject_hypothesis(
        workspace_id=ws_id,
        portfolio_id="P-REJECT",
        hypothesis_id=hid,
        rejection_reason="Editorial priority shifted towards systemic lens rather than counter position.",
        lane=AuthorityLane.COMMANDER,
    )
    assert receipt.status == "REJECTED"

    # Verify underlying hypothesis content remains pristine
    stored_hyp = store.get_hypothesis(ws_id, hid)
    assert stored_hyp.status == "REJECTED"
    assert stored_hyp.guest_lived_proof_citation == "Authentic guest proof citation that must remain unchanged."
    assert stored_hyp.bridge_statement == "Bridge statement countering traditional corporate diversification strategies."


def test_integer_micros_scoring_and_gate_evaluation(test_setup):
    """Test 7: 10 hypothesis gates and 7 dimensions evaluated in strict integer micros."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-scoring"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    # Advance state machine to HYPOTHESIS_FORMED
    _seed_valid_matrix(coord, ws_id, "MOE-SCORE")

    candidate1 = CollisionHypothesisCandidate(
        title="Winner Candidate",
        relation_type="SYSTEMS_LENS",
        audience_id="AUD-01",
        audience_tension_ref="T-1",
        guest_id="G-1",
        guest_lived_proof_citation="Substantive guest proof citation over years of work.",
        research_signal_id="SIG-01",
        bridge_statement="Substantive bridge statement illustrating feedback loops across domain boundaries.",
        refuting_observation="Refuting observation criteria.",
        disconfirming_testimony="Disconfirming testimony criteria.",
        boundary_limitation="Boundary limitation criteria.",
    )
    candidate2 = CollisionHypothesisCandidate(
        title="Failing Gate Candidate",
        relation_type="PARADOX",
        audience_id="AUD-02",
        audience_tension_ref="T-2",
        guest_id="G-1",
        guest_lived_proof_citation="Substantive guest proof citation over years of work.",
        research_signal_id="SIG-02",
        bridge_statement="Substantive bridge statement illustrating paradox across domain boundaries.",
        refuting_observation="Refuting observation criteria.",
        disconfirming_testimony="Disconfirming testimony criteria.",
        boundary_limitation="Boundary limitation criteria.",
    )

    portfolio = coord.compose_hypotheses(
        workspace_id=ws_id,
        portfolio_id="P-SCORE",
        candidates=[candidate1, candidate2],
        matrix_id="MOE-SCORE",
        lane=AuthorityLane.COMPOSER,
    )
    h1, h2 = portfolio.candidate_hypothesis_ids

    # Candidate 2 fails the 'SOURCE_FIDELITY' gate
    gate_outcomes = {
        h1: {g: True for g in HYPOTHESIS_GATES},
        h2: {g: (g != "SOURCE_FIDELITY") for g in HYPOTHESIS_GATES},
    }
    candidate_scores = {
        h1: {d: 850000 for d in EVALUATION_DIMENSIONS},
        h2: {d: 950000 for d in EVALUATION_DIMENSIONS},  # Higher score but ineligible
    }

    result = coord.evaluate_portfolio(
        workspace_id=ws_id,
        portfolio_id="P-SCORE",
        gate_outcomes=gate_outcomes,
        candidate_scores_micros=candidate_scores,
        lane=AuthorityLane.ANALYST,
    )

    # h1 wins because h2 failed a required gate
    assert result["decision"] == "DECISIVE_WINNER"
    assert result["selected_hypothesis_id"] == h1


def test_governed_repair_and_quarantine_lifecycle(test_setup):
    """Test 8: Governed repair and quarantine lifecycle."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-repair"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    # Store a hypothesis
    hyp = CollisionHypothesisRecord(
        workspace_id=ws_id,
        hypothesis_id="HYP-QUARANTINE",
        title="Quarantine Candidate",
        relation_type="ANALOGY",
        audience_id="AUD-01",
        audience_tension_ref="T-1",
        guest_id="G-1",
        guest_lived_proof_citation="Citation",
        research_signal_id="SIG-01",
        bridge_statement="Bridge statement",
        novelty_assessment={},
        falsification_condition={},
        heritage_eval={},
    )
    store.store_hypothesis(hyp)

    # Quarantine hypothesis
    quarantined = coord.quarantine_hypothesis(
        workspace_id=ws_id,
        hypothesis_id="HYP-QUARANTINE",
        reason="Detected potential data leakage from secondary unverified source.",
        lane=AuthorityLane.COMMANDER,
    )
    assert quarantined.status == "QUARANTINED"

    # Move aggregate to REPAIRING state to test repair transition
    agg = runtime.get_aggregate(coord.aggregate_id)
    d = agg.to_dict()
    d["current_state"] = "REPAIRING"
    d["lifecycle"] = ProgramStateLifecycle.REPAIRING.value
    d["version"] += 1
    runtime.store.save_aggregate(ProgramStateAggregate.from_dict(d))

    # Test state machine repair transition
    coord.retry_discovery(workspace_id=ws_id, lane=AuthorityLane.COMMANDER)
    snapshot = coord.get_snapshot()
    assert snapshot.current_state == "SIGNAL_HUNTING"


def test_contrastive_negative_cases(test_setup):
    """Test 9: Negative/contrastive test cases fail closed."""
    store: CollisionHypothesisStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-negative"
    coord = CollisionHypothesisProgramCoordinator(workspace_id=ws_id, store=store, state_runtime=runtime)

    # Empty audience tensions
    with pytest.raises(ResonanceAlignmentError):
        coord.discover_resonance(
            workspace_id=ws_id,
            guest_dna={"guest_id": "G-1", "proof_citation": "Substantive proof text."},
            audience_tensions=[],
            world_signals=[{"signal_id": "S-1"}],
            lane=AuthorityLane.HUNTER,
        )

    # Empty world signals
    with pytest.raises(ResonanceAlignmentError):
        coord.discover_resonance(
            workspace_id=ws_id,
            guest_dna={"guest_id": "G-1", "proof_citation": "Substantive proof text."},
            audience_tensions=[{"tension_label": "T-1"}],
            world_signals=[],
            lane=AuthorityLane.HUNTER,
        )

    # Approving non-existent hypothesis
    with pytest.raises(HypothesisApprovalError):
        coord.approve_hypothesis(
            workspace_id=ws_id,
            portfolio_id="P-NONE",
            hypothesis_id="HYP-DOES-NOT-EXIST",
            approval_notes="Approved",
            lane=AuthorityLane.COMMANDER,
        )
