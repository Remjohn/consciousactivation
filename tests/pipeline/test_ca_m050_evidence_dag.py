"""CA-M050 / INV-DAG-001 — Cryptographic Evidence DAG tests.

Positive and negative coverage for:
- multi-parent causal links with cryptographic parent-hash verification
- explicit PRUNED_REJECTION (rejected alternatives are not silently dropped)
- cycle rejection at construction time
- missing-parent rejection
- cross-tenant contamination rejection
- inferred-parent rejection (false-proof countercase)
- deterministic topological traversal
- serialize / reopen with parent-hash re-verification
- linking temporal moments, transcripts, tension matrices, synthesized media
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DAG_PATH = ROOT / "services" / "pipeline" / "src" / "cmf_pipeline" / "evidence" / "dag.py"


def _load_dag_module():
    """Load dag.py directly to avoid cmf_pipeline package __init__ side-effects
    (psycopg / ca_runtime) that are unrelated to INV-DAG-001.
    """
    spec = importlib.util.spec_from_file_location("cmf_pipeline_evidence_dag", DAG_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cmf_pipeline_evidence_dag"] = mod
    spec.loader.exec_module(mod)
    return mod


_dag = _load_dag_module()
EvidenceDAG = _dag.EvidenceDAG
EvidenceNodeKind = _dag.EvidenceNodeKind
EvidenceNodeStatus = _dag.EvidenceNodeStatus
CycleDetectedError = _dag.CycleDetectedError
MissingParentError = _dag.MissingParentError
ParentHashMismatchError = _dag.ParentHashMismatchError
CrossTenantError = _dag.CrossTenantError
InferredParentError = _dag.InferredParentError
NodeNotFoundError = _dag.NodeNotFoundError
DAGValidationError = _dag.DAGValidationError
PRUNED_REJECTION = _dag.PRUNED_REJECTION
content_hash = _dag.content_hash
make_node_id = _dag.make_node_id



WORKSPACE_A = "workspace-aaa-111"
WORKSPACE_B = "workspace-bbb-222"


def _moment_payload(label: str, offset_us: int = 0) -> dict:
    return {
        "label": label,
        "start_offset_us": offset_us,
        "end_offset_us": offset_us + 1_000_000,
        "source_media_sha256": "a" * 64,
    }


def _transcript_payload(text: str) -> dict:
    return {"text": text, "language": "en", "word_count": len(text.split())}


def _tension_payload(score: int) -> dict:
    return {"tension_score": score, "axes": ["urgency", "conflict"], "matrix_version": "1.0"}


def _media_payload(artifact_id: str) -> dict:
    return {"artifact_id": artifact_id, "codec": "h264", "duration_us": 5_000_000}


# ---------------------------------------------------------------------------
# Positive: construction, multi-parent, hashing, traversal
# ---------------------------------------------------------------------------


class TestEvidenceDAGConstruction:
    def test_add_nodes_of_all_kinds(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        m = dag.add_node(
            kind=EvidenceNodeKind.TEMPORAL_MOMENT,
            payload=_moment_payload("m1"),
            workspace_id=WORKSPACE_A,
        )
        t = dag.add_node(
            kind=EvidenceNodeKind.TRANSCRIPT,
            payload=_transcript_payload("hello world"),
            workspace_id=WORKSPACE_A,
        )
        x = dag.add_node(
            kind=EvidenceNodeKind.TENSION_MATRIX,
            payload=_tension_payload(7),
            workspace_id=WORKSPACE_A,
        )
        s = dag.add_node(
            kind=EvidenceNodeKind.SYNTHESIZED_MEDIA,
            payload=_media_payload("art-1"),
            workspace_id=WORKSPACE_A,
        )
        assert dag.node_count() == 4
        assert m.kind == EvidenceNodeKind.TEMPORAL_MOMENT
        assert t.content_hash == content_hash(_transcript_payload("hello world"))
        assert x.status == EvidenceNodeStatus.ACTIVE
        assert s.node_id.startswith("evidence-node:")

    def test_content_addressed_idempotent_add(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        payload = _moment_payload("same")
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=payload, workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=payload, workspace_id=WORKSPACE_A)
        assert a.node_id == b.node_id
        assert dag.node_count() == 1

    def test_multi_parent_links_with_hash_verification(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        root1 = dag.add_node(
            kind=EvidenceNodeKind.TEMPORAL_MOMENT,
            payload=_moment_payload("root1"),
            workspace_id=WORKSPACE_A,
        )
        root2 = dag.add_node(
            kind=EvidenceNodeKind.TRANSCRIPT,
            payload=_transcript_payload("src"),
            workspace_id=WORKSPACE_A,
        )
        child = dag.add_node(
            kind=EvidenceNodeKind.TENSION_MATRIX,
            payload=_tension_payload(3),
            workspace_id=WORKSPACE_A,
        )
        e1 = dag.link_parent(child_id=child.node_id, parent_id=root1.node_id, relation="DERIVES_FROM")
        e2 = dag.link_parent(child_id=child.node_id, parent_id=root2.node_id, relation="GROUNDED_IN")

        assert e1.parent_content_hash == root1.content_hash
        assert e2.parent_content_hash == root2.content_hash
        parents = dag.parents_of(child.node_id)
        assert set(parents) == {root1.node_id, root2.node_id}
        assert dag.edge_count() == 2

    def test_deterministic_topological_order(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("b"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TENSION_MATRIX, payload=_tension_payload(1), workspace_id=WORKSPACE_A)
        d = dag.add_node(kind=EvidenceNodeKind.SYNTHESIZED_MEDIA, payload=_media_payload("d"), workspace_id=WORKSPACE_A)

        dag.link_parent(child_id=c.node_id, parent_id=a.node_id)
        dag.link_parent(child_id=c.node_id, parent_id=b.node_id)
        dag.link_parent(child_id=d.node_id, parent_id=c.node_id)

        order = dag.topological_order()
        assert order.index(a.node_id) < order.index(c.node_id)
        assert order.index(b.node_id) < order.index(c.node_id)
        assert order.index(c.node_id) < order.index(d.node_id)
        # Determinism: same order on repeated calls
        assert dag.topological_order() == order

    def test_ancestors_and_descendants(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("b"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TENSION_MATRIX, payload=_tension_payload(2), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=b.node_id, parent_id=a.node_id)
        dag.link_parent(child_id=c.node_id, parent_id=b.node_id)

        assert dag.ancestors(c.node_id) == sorted([a.node_id, b.node_id])
        assert dag.descendants(a.node_id) == sorted([b.node_id, c.node_id])

    def test_verify_all_passes_on_valid_dag(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        p = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("p"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("c"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=c.node_id, parent_id=p.node_id)
        report = dag.verify_all(strict=True)
        assert report["ok"] is True
        assert report["acyclic"] is True
        assert report["parent_hash_ok"] is True
        assert report["workspace_ok"] is True
        assert report["no_inferred_parents"] is True


# ---------------------------------------------------------------------------
# Explicit pruning
# ---------------------------------------------------------------------------


class TestPruning:
    def test_prune_records_explicit_rejection(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        node = dag.add_node(
            kind=EvidenceNodeKind.TEMPORAL_MOMENT,
            payload=_moment_payload("to-prune"),
            workspace_id=WORKSPACE_A,
        )
        pruned = dag.prune(node.node_id, reason=PRUNED_REJECTION)
        assert pruned.status == EvidenceNodeStatus.PRUNED
        assert pruned.metadata.get("prune_reason") == PRUNED_REJECTION
        # Node still addressable
        assert dag.has_node(node.node_id)
        assert dag.get_node(node.node_id).status == EvidenceNodeStatus.PRUNED

    def test_prune_marks_incident_edges(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        p = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("p"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("c"), workspace_id=WORKSPACE_A)
        edge = dag.link_parent(child_id=c.node_id, parent_id=p.node_id)
        dag.prune(c.node_id)
        # Active edge count drops; total edges still present with PRUNED_REJECTION
        assert dag.edge_count(include_pruned=False) == 0
        assert dag.edge_count(include_pruned=True) == 1
        stored = dag._edges[edge.edge_id]
        assert stored.status == PRUNED_REJECTION

    def test_pruned_nodes_excluded_from_default_topo(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("b"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=b.node_id, parent_id=a.node_id)
        dag.prune(b.node_id)
        order = dag.topological_order()
        assert a.node_id in order
        assert b.node_id not in order
        order_all = dag.topological_order(include_pruned=True)
        assert b.node_id in order_all


# ---------------------------------------------------------------------------
# Negative: cycles, missing parents, hash mismatch, cross-tenant, inferred
# ---------------------------------------------------------------------------


class TestCycleRejection:
    def test_self_loop_rejected(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        n = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("n"), workspace_id=WORKSPACE_A)
        with pytest.raises(CycleDetectedError):
            dag.link_parent(child_id=n.node_id, parent_id=n.node_id)

    def test_simple_cycle_rejected(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("b"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=b.node_id, parent_id=a.node_id)
        with pytest.raises(CycleDetectedError):
            dag.link_parent(child_id=a.node_id, parent_id=b.node_id)

    def test_transitive_cycle_rejected(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("b"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TENSION_MATRIX, payload=_tension_payload(1), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=b.node_id, parent_id=a.node_id)
        dag.link_parent(child_id=c.node_id, parent_id=b.node_id)
        with pytest.raises(CycleDetectedError):
            dag.link_parent(child_id=a.node_id, parent_id=c.node_id)


class TestMissingParent:
    def test_link_to_unknown_parent_raises(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        child = dag.add_node(
            kind=EvidenceNodeKind.TEMPORAL_MOMENT,
            payload=_moment_payload("child"),
            workspace_id=WORKSPACE_A,
        )
        with pytest.raises(NodeNotFoundError):
            dag.link_parent(child_id=child.node_id, parent_id="evidence-node:does-not-exist")

    def test_get_missing_node_raises(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        with pytest.raises(NodeNotFoundError):
            dag.get_node("evidence-node:missing")


class TestCrossTenant:
    def test_node_from_other_workspace_rejected(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        with pytest.raises(CrossTenantError):
            dag.add_node(
                kind=EvidenceNodeKind.TRANSCRIPT,
                payload=_transcript_payload("b"),
                workspace_id=WORKSPACE_B,
            )

    def test_cross_tenant_link_rejected(self):
        # Build two isolated nodes then force a cross-tenant scenario by
        # constructing nodes in separate DAGs and attempting a manual edge
        # via low-level injection is not possible; instead verify that
        # a DAG bound to A refuses a node from B.
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        # Simulate a node that somehow has a different workspace by constructing
        # via from_dict path after the fact would also be caught on reopen.
        # Direct add already blocked; verify error message content.
        with pytest.raises(CrossTenantError) as exc_info:
            dag.add_node(
                kind=EvidenceNodeKind.SYNTHESIZED_MEDIA,
                payload=_media_payload("x"),
                workspace_id=WORKSPACE_B,
            )
        assert WORKSPACE_B in str(exc_info.value)


class TestInferredParentRejection:
    """False-proof countercase: neat chronological list / successful topo
    must not hide an inferred or cross-tenant parent.
    """

    def test_inferred_parent_rejected_at_link_time(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        p = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("p"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("c"), workspace_id=WORKSPACE_A)
        with pytest.raises(InferredParentError):
            dag.link_parent(
                child_id=c.node_id,
                parent_id=p.node_id,
                metadata={"inferred": True},
            )

    def test_false_proof_chronological_list_with_inferred_parent(self):
        """A report can show every node in neat chronological order and a
        topological sort can succeed, yet an inferred parent violates
        backward provenance.  The verifier must reject that case.
        """
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        # Legitimate nodes
        m1 = dag.add_node(
            kind=EvidenceNodeKind.TEMPORAL_MOMENT,
            payload=_moment_payload("m1", offset_us=0),
            workspace_id=WORKSPACE_A,
            created_at="2026-01-01T00:00:00Z",
        )
        m2 = dag.add_node(
            kind=EvidenceNodeKind.TEMPORAL_MOMENT,
            payload=_moment_payload("m2", offset_us=1_000_000),
            workspace_id=WORKSPACE_A,
            created_at="2026-01-01T00:00:01Z",
        )
        m3 = dag.add_node(
            kind=EvidenceNodeKind.TRANSCRIPT,
            payload=_transcript_payload("derived"),
            workspace_id=WORKSPACE_A,
            created_at="2026-01-01T00:00:02Z",
        )
        # Legitimate links
        dag.link_parent(child_id=m2.node_id, parent_id=m1.node_id)
        dag.link_parent(child_id=m3.node_id, parent_id=m2.node_id)

        # Chronological list looks neat
        chronological = sorted(
            [m1, m2, m3],
            key=lambda n: n.created_at or "",
        )
        assert [n.node_id for n in chronological] == [m1.node_id, m2.node_id, m3.node_id]

        # Topological sort succeeds
        order = dag.topological_order()
        assert len(order) == 3

        # Now inject an inferred-parent edge via serialization tampering
        # (simulates a false-proof report that looks organized).
        serialized = dag.to_dict()
        # Fabricate an edge that claims m3 → m1 with inferred=True
        fake_edge_id = "evidence-edge:fake-inferred"
        serialized["edges"][fake_edge_id] = {
            "edge_id": fake_edge_id,
            "child_id": m3.node_id,
            "parent_id": m1.node_id,
            "parent_content_hash": m1.content_hash,
            "relation": "DERIVES_FROM",
            "workspace_id": WORKSPACE_A,
            "status": "ACTIVE",
            "metadata": {"inferred": True},
        }

        # Reopen must reject inferred parent
        with pytest.raises(InferredParentError):
            EvidenceDAG.from_dict(serialized)

    def test_false_proof_cross_tenant_parent_hidden_by_sort(self):
        """Topological sort success must not hide a cross-tenant parent."""
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        a = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("a"), workspace_id=WORKSPACE_A)
        b = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("b"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=b.node_id, parent_id=a.node_id)

        # Topo succeeds
        assert len(dag.topological_order()) == 2

        # Tamper: change workspace on a node in serialization
        serialized = dag.to_dict()
        serialized["nodes"][a.node_id]["workspace_id"] = WORKSPACE_B

        with pytest.raises(CrossTenantError):
            EvidenceDAG.from_dict(serialized)


class TestParentHashIntegrity:
    def test_hash_mismatch_detected_on_reopen(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        p = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("p"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("c"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=c.node_id, parent_id=p.node_id)

        serialized = dag.to_dict()
        # Tamper parent content_hash on the node while leaving edge record intact
        serialized["nodes"][p.node_id]["content_hash"] = "0" * 64
        # Also update payload so content_hash field is inconsistent with payload
        # (the edge still holds the original hash)
        with pytest.raises(ParentHashMismatchError):
            EvidenceDAG.from_dict(serialized)

    def test_verify_parent_hashes_returns_failures(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        p = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("p"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("c"), workspace_id=WORKSPACE_A)
        edge = dag.link_parent(child_id=c.node_id, parent_id=p.node_id)
        # Manually corrupt the stored edge hash
        corrupted = type(edge)(
            edge_id=edge.edge_id,
            child_id=edge.child_id,
            parent_id=edge.parent_id,
            parent_content_hash="deadbeef" * 8,
            relation=edge.relation,
            workspace_id=edge.workspace_id,
            status=edge.status,
            metadata=edge.metadata,
        )
        dag._edges[edge.edge_id] = corrupted
        failures = dag.verify_parent_hashes()
        assert edge.edge_id in failures


# ---------------------------------------------------------------------------
# Serialization / reopen
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_round_trip_preserves_structure(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        m = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("m"), workspace_id=WORKSPACE_A)
        t = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("t"), workspace_id=WORKSPACE_A)
        x = dag.add_node(kind=EvidenceNodeKind.TENSION_MATRIX, payload=_tension_payload(5), workspace_id=WORKSPACE_A)
        s = dag.add_node(kind=EvidenceNodeKind.SYNTHESIZED_MEDIA, payload=_media_payload("s"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=t.node_id, parent_id=m.node_id)
        dag.link_parent(child_id=x.node_id, parent_id=t.node_id)
        dag.link_parent(child_id=x.node_id, parent_id=m.node_id)  # multi-parent
        dag.link_parent(child_id=s.node_id, parent_id=x.node_id)

        restored = EvidenceDAG.from_dict(dag.to_dict())
        assert restored.node_count() == 4
        assert restored.edge_count() == 4
        assert restored.workspace_id == WORKSPACE_A
        assert set(restored.parents_of(x.node_id)) == {t.node_id, m.node_id}
        report = restored.verify_all(strict=True)
        assert report["ok"] is True

    def test_evidence_refs_export(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        n = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("n"), workspace_id=WORKSPACE_A)
        refs = dag.evidence_refs()
        assert len(refs) == 1
        assert refs[0]["node_id"] == n.node_id
        assert refs[0]["content_hash"] == n.content_hash
        assert refs[0]["kind"] == "TEMPORAL_MOMENT"
        assert refs[0]["status"] == "ACTIVE"

    def test_missing_parent_on_reopen_raises(self):
        dag = EvidenceDAG(workspace_id=WORKSPACE_A)
        p = dag.add_node(kind=EvidenceNodeKind.TEMPORAL_MOMENT, payload=_moment_payload("p"), workspace_id=WORKSPACE_A)
        c = dag.add_node(kind=EvidenceNodeKind.TRANSCRIPT, payload=_transcript_payload("c"), workspace_id=WORKSPACE_A)
        dag.link_parent(child_id=c.node_id, parent_id=p.node_id)
        serialized = dag.to_dict()
        del serialized["nodes"][p.node_id]
        with pytest.raises(MissingParentError):
            EvidenceDAG.from_dict(serialized)


# ---------------------------------------------------------------------------
# make_node_id determinism
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_content_hash_stable(self):
        p = _moment_payload("x")
        assert content_hash(p) == content_hash(p)
        assert content_hash(p) != content_hash(_moment_payload("y"))

    def test_make_node_id_deterministic(self):
        digest = content_hash(_moment_payload("z"))
        a = make_node_id(EvidenceNodeKind.TEMPORAL_MOMENT, digest)
        b = make_node_id("TEMPORAL_MOMENT", digest)
        assert a == b
        assert a.startswith("evidence-node:")
