"""
test_knowledge_cluster_signal_program.py
----------------------------------------
Comprehensive acceptance and contrastive test suite for CAE Phase 3 Mandate M31:
Knowledge Clusters + Research Signals + Context Projection.

Verifies:
1. Full end-to-end lifecycle (Knowledge Nodes -> Clusters -> Signals -> Context Projections -> Commit).
2. Strict 4 Authority Lane enforcement (HUNTER, ANALYST, COMPOSER, COMMANDER).
3. Temporal signal separation from canonical knowledge truth.
4. Triple-gated integer basis points / micros scoring against Guest DNA & Audience Tensions.
5. Signal retraction and cascade propagation to active opportunities.
6. Multi-tenant workspace isolation.
7. Idempotent rebuilds preserving entity identity and lineage.
8. Governed repair and quarantine state machine transitions.
9. Contrastive negative and edge case validations.
"""

import sys
from pathlib import Path

# Add ca_runtime src to sys.path
sys.path.insert(0, str(Path(__file__).parents[2] / "packages" / "ca_runtime" / "src"))

import pytest
from datetime import datetime, timezone
from ca_runtime.program_state_runtime import AuthorityLane, UniversalProgramStateRuntime
from ca_runtime.research_canonicalization_program import (
    CanonicalKnowledgeNode,
    CanonicalRelationshipType,
)
from ca_runtime.knowledge_cluster_signal_store import (
    ContextProjectionRecord,
    KnowledgeClusterRecord,
    KnowledgeClusterSignalStore,
    ProvenanceEntry,
    ResearchSignalRecord,
    SourceMultiplicityInfo,
)
from ca_runtime.knowledge_cluster_signal_program import (
    ClusterFormationError,
    ClusterSignalReceipt,
    ContextProjectionError,
    InvalidLineageError,
    KnowledgeClusterSignalProgramCoordinator,
    KnowledgeClusterSignalProgramError,
    SignalCommitError,
    SignalDetectionError,
    UnauthorizedSignalLaneError,
    WorkspaceScopeViolationError,
)


@pytest.fixture
def store() -> KnowledgeClusterSignalStore:
    return KnowledgeClusterSignalStore()


@pytest.fixture
def state_runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def sample_canonical_nodes() -> list[CanonicalKnowledgeNode]:
    s1_hash = "a" * 64
    s2_hash = "b" * 64
    s3_hash = "c" * 64

    return [
        CanonicalKnowledgeNode(
            node_id="kn_universal_geometry_001",
            canonical_label="Universal Multimodal Latent Geometry",
            category="concept",
            aliases=["multimodal", "geometry", "latents", "representation"],
            definition="Unified representation manifold across vision and language models.",
            source_record_refs=["src_arxiv_2501_9999"],
            source_evidence_hashes=[s1_hash],
            lineage_sha256="1" * 64,
            version=1,
            lifecycle_status="active",
            authority_class="derived_validated_knowledge",
        ),
        CanonicalKnowledgeNode(
            node_id="kn_platonic_representation_002",
            canonical_label="Platonic Representation Hypothesis",
            category="concept",
            aliases=["representation", "platonic", "convergence", "multimodal"],
            definition="Hypothesis that neural networks converge toward a shared statistical model of reality.",
            source_record_refs=["src_arxiv_2501_8888"],
            source_evidence_hashes=[s2_hash],
            lineage_sha256="2" * 64,
            version=1,
            lifecycle_status="active",
            authority_class="derived_validated_knowledge",
        ),
        CanonicalKnowledgeNode(
            node_id="kn_deepmind_gemini_003",
            canonical_label="Google DeepMind Gemini Architecture",
            category="entity",
            aliases=["deepmind", "gemini", "frontier_ai"],
            definition="Frontier multimodal AI system natively trained on audio, vision, and code.",
            source_record_refs=["src_deepmind_gemini_techreport"],
            source_evidence_hashes=[s3_hash],
            lineage_sha256="3" * 64,
            version=1,
            lifecycle_status="active",
            authority_class="derived_validated_knowledge",
        ),
    ]



@pytest.fixture
def sample_raw_observations() -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "signal_id": "SIG-geometry-trend-001",
            "topic": "Rising Consensus on Platonic Latent Spaces in LMMs",
            "entities": ["Cornell", "Google DeepMind", "Platonic Representation"],
            "temporal_window_start_utc": now,
            "temporal_window_end_utc": now,
            "velocity_micros": 850000,
            "acceleration_micros": 600000,
            "novelty_micros": 900000,
            "divergence_micros": 250000,
            "confidence_micros": 950000,
            "evidence_excerpt": "Cross-engine search reveals a sharp spike in discussion regarding universal representation convergence.",
            "source_multiplicity": {
                "raw_mention_count": 5,
                "unique_root_domain_count": 4,
                "independent_source_count": 4,
                "syndication_ratio_bps": 2000,
            },
            "primary_provenance": {
                "origin_url": "https://arxiv.org/abs/2501.9999",
                "root_domain": "arxiv.org",
                "platform": "searxng",
                "observed_at_utc": now,
                "content_hash_sha256": "sha256_verbatim_geometry_snippet_001",
                "author_outlet": "Cornell Researchers",
                "is_syndicated_copy": False,
            },
            "corroborating_provenance": [
                {
                    "origin_url": "https://news.ycombinator.com/item?id=4001",
                    "root_domain": "ycombinator.com",
                    "platform": "hn",
                    "observed_at_utc": now,
                    "content_hash_sha256": "sha256_hn_commentary_001",
                    "is_syndicated_copy": False,
                }
            ],
            "metadata": {"search_mode": "searxng_cross_engine"},
        }
    ]


# ---------------------------------------------------------------------------
# Test 1: Full Lifecycle (Nodes -> Clusters -> Signals -> Projections -> Commit)
# ---------------------------------------------------------------------------

def test_knowledge_cluster_signal_full_lifecycle(
    store: KnowledgeClusterSignalStore,
    state_runtime: UniversalProgramStateRuntime,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    ws_id = "ws_test_m31_lifecycle"
    coord = KnowledgeClusterSignalProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=state_runtime,
    )

    # 1. HUNTER forms clusters
    clusters = coord.form_clusters(
        nodes=sample_canonical_nodes,
        lane=AuthorityLane.HUNTER,
        actor_id="agent_hunter",
    )
    assert len(clusters) == 2  # 'concept' and 'entity'
    concept_cluster = next(c for c in clusters if c.metadata["category"] == "concept")
    assert concept_cluster.coherence_score_micros >= 700000
    assert len(concept_cluster.member_node_ids) == 2
    assert coord.get_snapshot().state == "CLUSTERS_FORMED"

    # 2. ANALYST detects research signals
    signals = coord.detect_signals(
        raw_observations=sample_raw_observations,
        cluster_id=concept_cluster.cluster_id,
        lane=AuthorityLane.ANALYST,
        actor_id="agent_analyst",
    )
    assert len(signals) == 1
    sig = signals[0]
    assert sig.signal_id == "SIG-geometry-trend-001"
    assert sig.velocity_micros == 850000
    assert coord.get_snapshot().state == "SIGNALS_DETECTED"

    # 3. COMPOSER projects context onto Guest DNA & Audience Tensions
    identity_dna = {
        "identity_role": "AI Research Pioneer",
        "stance": "Unified representations are the substrate of machine intuition",
        "trigger_vectors": ["EXP-TRG-001", "EXP-TRG-004"],
    }
    projections = coord.project_context(
        signals=signals,
        guest_id="gst_audrey_001",
        identity_dna=identity_dna,
        audience_state_id="aud_engineers_001",
        audience_tensions=["TNS-002_model_fragmentation"],
        lane=AuthorityLane.COMPOSER,
        actor_id="agent_composer",
    )
    assert len(projections) == 1
    proj = projections[0]
    assert proj.guest_id == "gst_audrey_001"
    assert proj.activation_potential_micros > 0
    assert proj.distribution_potential_micros > 0
    assert proj.evidence_confidence_micros == 950000
    assert proj.composite_opportunity_score_micros > 0
    assert proj.hypothesis_readiness is True
    assert coord.get_snapshot().state == "CONTEXT_PROJECTED"

    # 4. COMMANDER commits projections to database store
    receipt = coord.commit_context_projections(
        lane=AuthorityLane.COMMANDER,
        actor_id="operator_commander",
    )
    assert receipt.receipt_id.startswith("rcpt_cs_")
    assert receipt.cluster_count == 2
    assert receipt.signal_count == 1
    assert receipt.projection_count == 1
    assert coord.get_snapshot().state == "SIGNALS_COMMITTED"

    # 5. Verify database store queries
    saved_cluster = store.get_cluster(ws_id, concept_cluster.cluster_id)
    assert saved_cluster is not None
    assert saved_cluster.cluster_label == concept_cluster.cluster_label

    saved_signal = store.get_signal(ws_id, sig.signal_id)
    assert saved_signal is not None
    assert saved_signal.topic == sig.topic

    saved_proj = store.get_context_projection(ws_id, proj.projection_id)
    assert saved_proj is not None
    assert saved_proj.composite_opportunity_score_micros == proj.composite_opportunity_score_micros

    top_opportunities = store.list_top_content_opportunities(ws_id, "gst_audrey_001", limit=5)
    assert len(top_opportunities) == 1
    assert top_opportunities[0].projection_id == proj.projection_id


# ---------------------------------------------------------------------------
# Test 2: Strict Authority Lane Enforcement
# ---------------------------------------------------------------------------

def test_authority_lane_enforcement(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    coord = KnowledgeClusterSignalProgramCoordinator(
        workspace_id="ws_test_lane_enforcement",
        store=store,
    )

    # 1. Non-HUNTER cannot form clusters
    with pytest.raises(UnauthorizedSignalLaneError):
        coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.COMPOSER)

    # Valid HUNTER call
    clusters = coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)

    # 2. Non-ANALYST cannot detect signals
    with pytest.raises(UnauthorizedSignalLaneError):
        coord.detect_signals(sample_raw_observations, clusters[0].cluster_id, lane=AuthorityLane.HUNTER)

    # Valid ANALYST call
    signals = coord.detect_signals(sample_raw_observations, clusters[0].cluster_id, lane=AuthorityLane.ANALYST)

    # 3. Non-COMPOSER cannot project context
    with pytest.raises(UnauthorizedSignalLaneError):
        coord.project_context(
            signals=signals,
            guest_id="gst_001",
            identity_dna={},
            audience_state_id="aud_001",
            audience_tensions=[],
            lane=AuthorityLane.COMMANDER,
        )

    # Valid COMPOSER call
    coord.project_context(
        signals=signals,
        guest_id="gst_001",
        identity_dna={"trigger_vectors": ["EXP-TRG-001"]},
        audience_state_id="aud_001",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )

    # 4. Non-COMMANDER cannot commit context projections
    with pytest.raises(UnauthorizedSignalLaneError):
        coord.commit_context_projections(lane=AuthorityLane.ANALYST)

    # Valid COMMANDER call
    receipt = coord.commit_context_projections(lane=AuthorityLane.COMMANDER)
    assert receipt.authority_lane == AuthorityLane.COMMANDER


# ---------------------------------------------------------------------------
# Test 3: Temporal Signal Separation from Canonical Truth
# ---------------------------------------------------------------------------

def test_temporal_signal_separation_from_canonical_truth(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    ws_id = "ws_test_temporal_separation"
    coord = KnowledgeClusterSignalProgramCoordinator(workspace_id=ws_id, store=store)

    clusters = coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)
    signals = coord.detect_signals(sample_raw_observations, clusters[0].cluster_id, lane=AuthorityLane.ANALYST)
    coord.project_context(
        signals=signals,
        guest_id="gst_001",
        identity_dna={"trigger_vectors": ["EXP-TRG-001"]},
        audience_state_id="aud_001",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )
    coord.commit_context_projections(lane=AuthorityLane.COMMANDER)

    # Verify signals are queryable as temporal signals
    db_signals = store.list_signals(ws_id, status="ACTIVE")
    assert len(db_signals) == 1
    assert db_signals[0].velocity_micros == 850000

    # Ensure no signal is miscategorized as a canonical knowledge cluster
    db_clusters = store.list_clusters(ws_id)
    assert all(not c.cluster_id.startswith("SIG-") for c in db_clusters)


# ---------------------------------------------------------------------------
# Test 4: Guest and Audience Context Projection Scoring
# ---------------------------------------------------------------------------

def test_guest_and_audience_context_projection_scoring(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    coord = KnowledgeClusterSignalProgramCoordinator(
        workspace_id="ws_test_scoring",
        store=store,
    )
    clusters = coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)
    signals = coord.detect_signals(sample_raw_observations, clusters[0].cluster_id, lane=AuthorityLane.ANALYST)

    identity_dna = {
        "identity_role": "Pioneer",
        "trigger_vectors": ["EXP-TRG-001", "EXP-TRG-002"],
    }
    projections = coord.project_context(
        signals=signals,
        guest_id="gst_001",
        identity_dna=identity_dna,
        audience_state_id="aud_001",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )

    proj = projections[0]
    assert 0 <= proj.activation_potential_micros <= 1000000
    assert 0 <= proj.distribution_potential_micros <= 1000000
    assert 0 <= proj.evidence_confidence_micros <= 1000000
    assert 0 <= proj.composite_opportunity_score_micros <= 1000000

    # Test formula: (A * D * E) / 10^12
    expected_composite = (
        proj.activation_potential_micros
        * proj.distribution_potential_micros
        * proj.evidence_confidence_micros
    ) // (1000000 * 1000000)
    assert proj.composite_opportunity_score_micros == expected_composite


# ---------------------------------------------------------------------------
# Test 5: Signal Retraction and Cascade Propagation
# ---------------------------------------------------------------------------

def test_signal_retraction_and_supersession(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    ws_id = "ws_test_retraction"
    coord = KnowledgeClusterSignalProgramCoordinator(workspace_id=ws_id, store=store)

    clusters = coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)
    signals = coord.detect_signals(sample_raw_observations, clusters[0].cluster_id, lane=AuthorityLane.ANALYST)
    coord.project_context(
        signals=signals,
        guest_id="gst_001",
        identity_dna={"trigger_vectors": ["EXP-TRG-001"]},
        audience_state_id="aud_001",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )
    coord.commit_context_projections(lane=AuthorityLane.COMMANDER)

    # Verify active before retraction
    assert len(store.list_signals(ws_id, status="ACTIVE")) == 1
    assert len(store.list_top_content_opportunities(ws_id, "gst_001")) == 1

    # COMMANDER retracts signal
    sig_id = signals[0].signal_id
    success = coord.retract_signal(sig_id, lane=AuthorityLane.COMMANDER)
    assert success is True

    # Active queries must now omit retracted signal
    assert len(store.list_signals(ws_id, status="ACTIVE")) == 0
    assert len(store.list_signals(ws_id, status="RETRACTED")) == 1

    # Top opportunities must cascade omit projections tied to retracted signals
    assert len(store.list_top_content_opportunities(ws_id, "gst_001")) == 0


# ---------------------------------------------------------------------------
# Test 6: Multi-Tenant Workspace Isolation
# ---------------------------------------------------------------------------

def test_multi_tenant_workspace_isolation(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    ws_a = "ws_tenant_alpha"
    ws_b = "ws_tenant_beta"

    coord_a = KnowledgeClusterSignalProgramCoordinator(workspace_id=ws_a, store=store)
    clusters_a = coord_a.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)
    signals_a = coord_a.detect_signals(sample_raw_observations, clusters_a[0].cluster_id, lane=AuthorityLane.ANALYST)
    coord_a.project_context(
        signals=signals_a,
        guest_id="gst_alpha",
        identity_dna={"trigger_vectors": ["EXP-TRG-001"]},
        audience_state_id="aud_alpha",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )
    coord_a.commit_context_projections(lane=AuthorityLane.COMMANDER)

    # Workspace B queries must return empty sets
    assert len(store.list_clusters(ws_b)) == 0
    assert len(store.list_signals(ws_b)) == 0
    assert len(store.list_context_projections(ws_b)) == 0
    assert store.get_cluster(ws_b, clusters_a[0].cluster_id) is None
    assert store.get_signal(ws_b, signals_a[0].signal_id) is None


# ---------------------------------------------------------------------------
# Test 7: Idempotent Rebuild Preserves Identity and Lineage
# ---------------------------------------------------------------------------

def test_idempotent_rebuild_preserves_cluster_identity(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
    sample_raw_observations: list[dict],
):
    ws_id = "ws_test_idempotency"
    coord = KnowledgeClusterSignalProgramCoordinator(workspace_id=ws_id, store=store)

    clusters_1 = coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)
    signals_1 = coord.detect_signals(sample_raw_observations, clusters_1[0].cluster_id, lane=AuthorityLane.ANALYST)
    projs_1 = coord.project_context(
        signals=signals_1,
        guest_id="gst_001",
        identity_dna={"trigger_vectors": ["EXP-TRG-001"]},
        audience_state_id="aud_001",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )
    coord.commit_context_projections(lane=AuthorityLane.COMMANDER)

    # Rebuild projections
    projs_2 = coord.rebuild_context_projections(
        guest_id="gst_001",
        identity_dna={"trigger_vectors": ["EXP-TRG-001"]},
        audience_state_id="aud_001",
        audience_tensions=["TNS-001"],
        lane=AuthorityLane.COMPOSER,
    )

    assert len(projs_2) == len(projs_1)
    assert projs_2[0].projection_id == projs_1[0].projection_id
    assert projs_2[0].composite_opportunity_score_micros == projs_1[0].composite_opportunity_score_micros


# ---------------------------------------------------------------------------
# Test 8: Governed Repair and Quarantine Lifecycle
# ---------------------------------------------------------------------------

def test_governed_repair_and_quarantine_lifecycle(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
):
    coord = KnowledgeClusterSignalProgramCoordinator(
        workspace_id="ws_test_repair",
        store=store,
    )
    coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)

    # 1. Recover to REPAIRING
    coord.recover_to_repairing("Simulated signal corruption", lane=AuthorityLane.COMMANDER)
    assert coord.get_snapshot().state == "REPAIRING"

    # 2. Repair back to CLUSTERS_FORMED
    coord.repair_signals(lane=AuthorityLane.COMMANDER)
    assert coord.get_snapshot().state == "CLUSTERS_FORMED"

    # 3. Quarantine on unrecoverable violation
    coord.quarantine_program("Irreparable tenant leak", lane=AuthorityLane.COMMANDER)
    assert coord.get_snapshot().state == "QUARANTINED"


# ---------------------------------------------------------------------------
# Test 9: Contrastive Negative and Validation Errors
# ---------------------------------------------------------------------------

def test_contrastive_negative_cases(
    store: KnowledgeClusterSignalStore,
    sample_canonical_nodes: list[CanonicalKnowledgeNode],
):
    coord = KnowledgeClusterSignalProgramCoordinator(
        workspace_id="ws_test_negative",
        store=store,
    )

    # 1. Empty nodes list
    with pytest.raises(ClusterFormationError):
        coord.form_clusters([], lane=AuthorityLane.HUNTER)

    # 2. Node missing source evidence hashes (model validation fails or coordinator checks)
    with pytest.raises(Exception):
        CanonicalKnowledgeNode(
            node_id="kn_broken",
            canonical_label="Broken Node",
            category="concept",
            definition="Node missing lineage",
            source_record_refs=["src_001"],
            source_evidence_hashes=[],  # EMPTY
            lineage_sha256="4" * 64,
        )


    # 3. Raw observation missing provenance
    clusters = coord.form_clusters(sample_canonical_nodes, lane=AuthorityLane.HUNTER)
    invalid_obs = [
        {
            "topic": "No Provenance Signal",
            "evidence_excerpt": "Valid snippet length exceeding 10 characters.",
            "source_multiplicity": {
                "raw_mention_count": 1,
                "unique_root_domain_count": 1,
                "independent_source_count": 1,
            },
            # missing primary_provenance
        }
    ]
    with pytest.raises(SignalDetectionError):
        coord.detect_signals(invalid_obs, clusters[0].cluster_id, lane=AuthorityLane.ANALYST)

    # 4. Out-of-bounds metric value
    out_of_bounds_obs = [
        {
            "topic": "Invalid Metric Signal",
            "evidence_excerpt": "Valid snippet length exceeding 10 characters.",
            "velocity_micros": 2000000,  # > 1_000_000
            "primary_provenance": {
                "origin_url": "https://example.com",
                "root_domain": "example.com",
                "platform": "news",
                "observed_at_utc": datetime.now(timezone.utc).isoformat(),
                "content_hash_sha256": "sha256_mock",
            },
            "source_multiplicity": {
                "raw_mention_count": 1,
                "unique_root_domain_count": 1,
                "independent_source_count": 1,
            },
        }
    ]
    with pytest.raises(SignalDetectionError):
        coord.detect_signals(out_of_bounds_obs, clusters[0].cluster_id, lane=AuthorityLane.ANALYST)
