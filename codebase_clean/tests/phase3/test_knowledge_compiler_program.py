"""
Phase 3 Mandate M30 Acceptance Test Suite:
Canonical Knowledge Compiler + Supabase Projection Program Coordinator.

Governed by:
- 03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M30_canonical_knowledge_compiler_supabase_projection.md
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, List
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.knowledge_compiler_program import (
    CompiledKnowledgeProjection,
    CompiledSearchIndex,
    CrossWorkspaceProjectionError,
    InvalidKnowledgeNodeError,
    KnowledgeCompilationReceipt,
    KnowledgeCompilerProgramCoordinator,
    KnowledgeCompilerProgramError,
    KnowledgeCompilerSnapshot,
    ProjectionCompilationError,
    ProvenanceLineageBrokenError,
    UnauthorizedKnowledgeCompilerLaneError,
)
from ca_runtime.knowledge_projection_store import (
    KnowledgeProjectionStore,
    ScoredKnowledgeMatch,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    UniversalProgramStateRuntime,
    get_canonical_knowledge_compiler_state_machine,
)
from ca_runtime.research_canonicalization_program import (
    CanonicalKnowledgeNode,
    CanonicalRelationship,
    CanonicalRelationshipType,
)
from ca_runtime.tenancy import CrossWorkspaceLeakError, TenantContext, tenant_scope


# ----------------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------------

@pytest.fixture
def workspace_a_id() -> str:
    return str(uuid4())


@pytest.fixture
def workspace_b_id() -> str:
    return str(uuid4())


@pytest.fixture
def tenant_a_ctx(workspace_a_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(workspace_a_id),
        actor_id="usr_lead_commander_a",
        role="MEMBER",
    )


@pytest.fixture
def tenant_b_ctx(workspace_b_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(workspace_b_id),
        actor_id="usr_lead_commander_b",
        role="MEMBER",
    )


@pytest.fixture
def runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def store() -> KnowledgeProjectionStore:
    return KnowledgeProjectionStore(":memory:")


@pytest.fixture
def coordinator(
    runtime: UniversalProgramStateRuntime,
    store: KnowledgeProjectionStore,
) -> KnowledgeCompilerProgramCoordinator:
    return KnowledgeCompilerProgramCoordinator(runtime=runtime, store=store)


@pytest.fixture
def sample_canonical_nodes() -> List[CanonicalKnowledgeNode]:
    s1_text = "Artificial General Intelligence refers to autonomous systems that can accomplish intellectual tasks."
    s1_hash = hashlib.sha256(s1_text.encode("utf-8")).hexdigest()
    s2_text = "Narrow AI systems are specialized algorithms designed for specific bounded tasks."
    s2_hash = hashlib.sha256(s2_text.encode("utf-8")).hexdigest()

    node1 = CanonicalKnowledgeNode(
        node_id="kn_agi_001",
        canonical_label="Artificial General Intelligence",
        category="concept",
        aliases=["AGI", "Strong AI", "Human-Level AI"],
        definition="Hypothetical machine intelligence possessing broad human-level intellectual capabilities across diverse domains.",
        lifecycle_status="active",
        authority_class="derived_validated_knowledge",
        source_record_refs=["src_rec_001"],
        source_evidence_hashes=[s1_hash],
        lineage_sha256=hashlib.sha256(f"kn_agi_001:{s1_hash}".encode("utf-8")).hexdigest(),
        version=1,
        typed_edges={"DISTINCT": ["kn_narrow_ai_002"]},
    )

    node2 = CanonicalKnowledgeNode(
        node_id="kn_narrow_ai_002",
        canonical_label="Narrow AI",
        category="concept",
        aliases=["Weak AI", "Specialized AI"],
        definition="Artificial intelligence systems specialized in performing single bounded tasks.",
        lifecycle_status="active",
        authority_class="derived_validated_knowledge",
        source_record_refs=["src_rec_002"],
        source_evidence_hashes=[s2_hash],
        lineage_sha256=hashlib.sha256(f"kn_narrow_ai_002:{s2_hash}".encode("utf-8")).hexdigest(),
        version=1,
        typed_edges={"DISTINCT": ["kn_agi_001"]},
    )

    node3 = CanonicalKnowledgeNode(
        node_id="kn_neural_scaling_003",
        canonical_label="Neural Scaling Laws",
        category="framework",
        aliases=["Scaling Hypothesis", "Kaplan Laws"],
        definition="Empirical power-law relationships between compute, dataset size, parameters, and loss in transformer architectures.",
        lifecycle_status="active",
        authority_class="derived_validated_knowledge",
        source_record_refs=["src_rec_001", "src_rec_002"],
        source_evidence_hashes=[s1_hash, s2_hash],
        lineage_sha256=hashlib.sha256(f"kn_neural_scaling_003:{s1_hash}:{s2_hash}".encode("utf-8")).hexdigest(),
        version=1,
        typed_edges={"RELATED": ["kn_agi_001"]},
    )

    return [node1, node2, node3]


# ----------------------------------------------------------------------------
# Test Cases
# ----------------------------------------------------------------------------

def test_knowledge_compiler_full_lifecycle(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Tests end-to-end multi-lane compilation from canonical nodes to projected database tables."""
    with tenant_scope(tenant_a_ctx):
        # 1. Initialize session
        snap0 = coordinator.initialize_session(workspace_a_id)
        assert snap0.current_state == "INITIAL"
        assert snap0.nodes_count == 0

        # 2. Ingest Nodes (HUNTER lane)
        snap1 = coordinator.ingest_nodes(
            workspace_a_id,
            sample_canonical_nodes,
            caller_lane=AuthorityLane.HUNTER,
        )
        assert snap1.current_state == "KNOWLEDGE_INGESTED"
        assert snap1.nodes_count == 3

        # 3. Compile Projections (COMPOSER lane)
        snap2 = coordinator.compile_projections(
            workspace_a_id,
            caller_lane=AuthorityLane.COMPOSER,
        )
        assert snap2.current_state == "PROJECTIONS_COMPILED"
        assert snap2.projections_count == 3

        # 4. Build Search Index (ANALYST lane)
        snap3 = coordinator.build_search_index(
            workspace_a_id,
            caller_lane=AuthorityLane.ANALYST,
        )
        assert snap3.current_state == "SEARCH_INDEX_BUILT"
        assert snap3.indices_count == 3

        # 5. Project to Database (COMMANDER lane)
        receipt = coordinator.project_to_database(
            workspace_a_id,
            caller_lane=AuthorityLane.COMMANDER,
        )
        assert isinstance(receipt, KnowledgeCompilationReceipt)
        assert receipt.nodes_count == 3
        assert receipt.projections_count == 3
        assert receipt.edges_count == 3
        assert len(receipt.receipt_sha256) == 64

        snap4 = coordinator.get_snapshot(workspace_a_id)
        assert snap4.current_state == "SUPABASE_PROJECTED"
        assert snap4.receipt_count == 1

        # Verify persisted store contents
        nodes = coordinator.query_structured_nodes(workspace_a_id)
        assert len(nodes) == 3
        projections = coordinator.store.list_projections(workspace_a_id)
        assert len(projections) == 3


def test_authority_lane_enforcement(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies that executing operations on unauthorized authority lanes is strictly blocked."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)

        # Ingestion must be HUNTER lane
        with pytest.raises(UnauthorizedKnowledgeCompilerLaneError):
            coordinator.ingest_nodes(
                workspace_a_id,
                sample_canonical_nodes,
                caller_lane=AuthorityLane.COMPOSER,
            )
        with pytest.raises(UnauthorizedKnowledgeCompilerLaneError):
            coordinator.ingest_nodes(
                workspace_a_id,
                sample_canonical_nodes,
                caller_lane=AuthorityLane.COMMANDER,
            )

        # Correctly ingest
        coordinator.ingest_nodes(
            workspace_a_id,
            sample_canonical_nodes,
            caller_lane=AuthorityLane.HUNTER,
        )

        # Projections compilation must be COMPOSER lane
        with pytest.raises(UnauthorizedKnowledgeCompilerLaneError):
            coordinator.compile_projections(
                workspace_a_id,
                caller_lane=AuthorityLane.HUNTER,
            )
        with pytest.raises(UnauthorizedKnowledgeCompilerLaneError):
            coordinator.compile_projections(
                workspace_a_id,
                caller_lane=AuthorityLane.ANALYST,
            )

        # Correctly compile projections
        coordinator.compile_projections(
            workspace_a_id,
            caller_lane=AuthorityLane.COMPOSER,
        )

        # Search index must be ANALYST lane
        with pytest.raises(UnauthorizedKnowledgeCompilerLaneError):
            coordinator.build_search_index(
                workspace_a_id,
                caller_lane=AuthorityLane.COMPOSER,
            )

        # Correctly build search index
        coordinator.build_search_index(
            workspace_a_id,
            caller_lane=AuthorityLane.ANALYST,
        )

        # Database projection must be COMMANDER lane
        with pytest.raises(UnauthorizedKnowledgeCompilerLaneError):
            coordinator.project_to_database(
                workspace_a_id,
                caller_lane=AuthorityLane.ANALYST,
            )


def test_idempotent_rebuild_preserves_identity_and_lineage(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies that rebuilding projections produces identical hashes and preserves source identity."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        rcpt1 = coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

        # Record baseline hashes
        p1 = coordinator.store.get_projection_by_node(workspace_a_id, "kn_agi_001")
        assert p1 is not None
        p1_sha = p1["content_sha256"]
        p1_lineage = p1["object_ref"]["sha256"]

        # Rebuild projections idempotently
        rcpt2 = coordinator.rebuild_projections(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)
        assert rcpt2.rebuild_count == 1

        p1_rebuilt = coordinator.store.get_projection_by_node(workspace_a_id, "kn_agi_001")
        assert p1_rebuilt is not None
        assert p1_rebuilt["content_sha256"] == p1_sha
        assert p1_rebuilt["object_ref"]["sha256"] == p1_lineage
        assert p1_rebuilt["object_ref"]["object_id"] == "kn_agi_001"
        assert p1_rebuilt["rebuild_count"] == 1


def test_provenance_survival_through_projection(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies that source provenance refs and hashes survive projection into database tables."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

        # Inspect provenance link tables in store
        prov_agi = coordinator.store.get_provenance_for_node(workspace_a_id, "kn_agi_001")
        assert len(prov_agi) == 1
        assert prov_agi[0]["source_id"] == "src_rec_001"
        assert prov_agi[0]["source_sha256"] == sample_canonical_nodes[0].source_evidence_hashes[0]

        prov_scaling = coordinator.store.get_provenance_for_node(workspace_a_id, "kn_neural_scaling_003")
        assert len(prov_scaling) == 2
        assert {p["source_id"] for p in prov_scaling} == {"src_rec_001", "src_rec_002"}


def test_broken_provenance_rejected(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
) -> None:
    """Verifies that nodes without cryptographic lineage or source references are rejected fail-closed."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)

        corrupt_node = {
            "node_id": "kn_corrupt_999",
            "canonical_label": "Corrupt Node",
            "category": "concept",
            "definition": "A node with no provenance lineage.",
            "source_record_refs": [],
            "source_evidence_hashes": {},
            "lineage_sha256": "",
        }

        with pytest.raises(ProvenanceLineageBrokenError):
            coordinator.ingest_nodes(
                workspace_a_id,
                [corrupt_node],
                caller_lane=AuthorityLane.HUNTER,
            )


def test_structured_sql_retrieval(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies structured SQL filtering by category, lifecycle status, and relationship edges."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

        # Filter by category
        concepts = coordinator.query_structured_nodes(workspace_a_id, category="concept")
        assert len(concepts) == 2
        frameworks = coordinator.query_structured_nodes(workspace_a_id, category="framework")
        assert len(frameworks) == 1
        assert frameworks[0]["canonical_label"] == "Neural Scaling Laws"

        # Query edges
        edges = coordinator.store.get_edges_for_node(workspace_a_id, "kn_agi_001")
        assert len(edges) >= 2
        connected_neighbors = {e["target_node_id"] if e["source_node_id"] == "kn_agi_001" else e["source_node_id"] for e in edges}
        assert "kn_narrow_ai_002" in connected_neighbors
        assert "kn_neural_scaling_003" in connected_neighbors


def test_lexical_and_tag_search_with_integer_scoring(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies lexical search scoring in integer basis points (micros)."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

        # 1. Exact title match
        results_exact = coordinator.search_knowledge(workspace_a_id, "Artificial General Intelligence")
        assert len(results_exact) > 0
        top = results_exact[0]
        assert top.node_id == "kn_agi_001"
        assert top.exact_score_micros >= 400_000
        assert isinstance(top.total_score_micros, int)

        # 2. Token overlap search
        results_token = coordinator.search_knowledge(workspace_a_id, "scaling transformer loss")
        assert len(results_token) > 0
        assert results_token[0].node_id == "kn_neural_scaling_003"
        assert results_token[0].lexical_score_micros > 0

        # 3. Tag search boost
        results_tag = coordinator.search_knowledge(
            workspace_a_id,
            "intelligence",
            tags=["strong ai"],
        )
        assert len(results_tag) > 0
        assert results_tag[0].node_id == "kn_agi_001"
        assert results_tag[0].tag_score_micros > 0


def test_dense_adapter_candidate_hook(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies that pluggable dense ranking operates only on candidate nodes filtered by authority."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

        received_candidate_ids: List[str] = []

        def mock_dense_adapter(candidate_ids: List[str], query: str) -> Dict[str, int]:
            received_candidate_ids.extend(candidate_ids)
            # Give high dense score to kn_neural_scaling_003
            return {"kn_neural_scaling_003": 85_000}

        results = coordinator.search_knowledge(
            workspace_a_id,
            "neural compute empirical",
            dense_adapter_cb=mock_dense_adapter,
        )

        assert set(received_candidate_ids) == {"kn_agi_001", "kn_narrow_ai_002", "kn_neural_scaling_003"}
        assert len(results) > 0
        top = results[0]
        assert top.node_id == "kn_neural_scaling_003"
        assert top.dense_score_micros == 85_000


def test_multi_tenant_workspace_isolation(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    workspace_b_id: str,
    tenant_a_ctx: TenantContext,
    tenant_b_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies strict multi-tenant boundary isolation across projections and queries."""
    # Populate Workspace A
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

    # In Workspace B, query should return 0 nodes and 0 projections
    with tenant_scope(tenant_b_ctx):
        coordinator.initialize_session(workspace_b_id)
        nodes_b = coordinator.query_structured_nodes(workspace_b_id)
        assert len(nodes_b) == 0

        search_b = coordinator.search_knowledge(workspace_b_id, "Artificial General Intelligence")
        assert len(search_b) == 0

        projections_b = coordinator.store.list_projections(workspace_b_id)
        assert len(projections_b) == 0


def test_node_retraction_synchronization(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies that node retraction propagates to projection lifecycle and active queries."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)
        coordinator.compile_projections(workspace_a_id, caller_lane=AuthorityLane.COMPOSER)
        coordinator.build_search_index(workspace_a_id, caller_lane=AuthorityLane.ANALYST)
        coordinator.project_to_database(workspace_a_id, caller_lane=AuthorityLane.COMMANDER)

        # Retract kn_narrow_ai_002
        rcpt = coordinator.sync_retraction(
            workspace_a_id,
            "kn_narrow_ai_002",
            reason="Superseded by specialized sub-architecture framework",
            caller_lane=AuthorityLane.COMMANDER,
        )
        assert rcpt.rebuild_count >= 1

        # Query ACTIVE projections: kn_narrow_ai_002 is omitted
        active_search = coordinator.search_knowledge(
            workspace_a_id,
            "Narrow AI",
            lifecycle_state="ACTIVE",
        )
        active_node_ids = {m.node_id for m in active_search}
        assert "kn_narrow_ai_002" not in active_node_ids

        # Query RETRACTED projections: kn_narrow_ai_002 is found
        retracted_search = coordinator.search_knowledge(
            workspace_a_id,
            "Narrow AI",
            lifecycle_state="RETRACTED",
        )
        retracted_node_ids = {m.node_id for m in retracted_search}
        assert "kn_narrow_ai_002" in retracted_node_ids


def test_repair_and_quarantine_lifecycle(
    coordinator: KnowledgeCompilerProgramCoordinator,
    workspace_a_id: str,
    tenant_a_ctx: TenantContext,
    sample_canonical_nodes: List[CanonicalKnowledgeNode],
) -> None:
    """Verifies state recovery transitions through REPAIRING and QUARANTINED states."""
    with tenant_scope(tenant_a_ctx):
        coordinator.initialize_session(workspace_a_id)
        coordinator.ingest_nodes(workspace_a_id, sample_canonical_nodes, caller_lane=AuthorityLane.HUNTER)

        # Trigger recovery to REPAIRING
        snap_rep = coordinator.recover_to_repairing(
            workspace_a_id,
            reason="Simulated projection schema corruption",
            caller_lane=AuthorityLane.COMMANDER,
        )
        assert snap_rep.current_state == "REPAIRING"

        # Repair back to KNOWLEDGE_INGESTED
        snap_restored = coordinator.repair_compiler_state(
            workspace_a_id,
            caller_lane=AuthorityLane.COMMANDER,
        )
        assert snap_restored.current_state == "KNOWLEDGE_INGESTED"

        # Quarantine on unresolvable violation
        snap_quar = coordinator.quarantine_compiler_state(
            workspace_a_id,
            reason="Unresolvable contradictory axiom failure",
            caller_lane=AuthorityLane.COMMANDER,
        )
        assert snap_quar.current_state == "QUARANTINED"
