"""
Executable evidence for CA-M004 / INV-CAUSAL-001:
Pipeline Stage Ordering & Causal Flow.

Positive: valid causal progression is admitted.
Negative: missing ancestors, wrong order, stale/mismatched identity,
invalid state, synthesized placeholders, and force/bypass attempts are blocked.
"""

from __future__ import annotations

import pytest

from cmf_pipeline.domain.enums import NodeState
from cmf_pipeline.domain.errors import PipelineLifecycleError, PipelineValidationError
from cmf_pipeline.workflow.admission.causal_admission import (
    AncestorBinding,
    CausalAdmissionDecision,
    CausalAdmissionError,
    CausalAdmissionService,
    CausalBlockReason,
    RequiredAncestor,
)
from cmf_pipeline.workflow.application.scheduler import DeterministicScheduler


def _binding(
    ancestor_id: str,
    *,
    state: str = NodeState.SUCCEEDED.value,
    digest: str = "digest-v1",
    revision: str = "1",
    identity: str | None = None,
    is_placeholder: bool = False,
) -> AncestorBinding:
    return AncestorBinding(
        ancestor_id=ancestor_id,
        identity=identity or f"id:{ancestor_id}",
        content_digest=digest,
        revision=revision,
        state=state,
        is_placeholder=is_placeholder,
    )


def _minimal_workflow(
    nodes: list[tuple[str, int]],
    edges: list[tuple[str, str]],
) -> dict:
    """nodes: list of (node_id, phase_order); edges: (source, target)."""
    node_ids = [n[0] for n in nodes]
    return {
        "nodes": [
            {
                "node_id": nid,
                "phase_order": phase,
                "side_effect_class": "NONE",
                "capability_id": f"cap-{nid}",
                "purpose": f"purpose-{nid}",
                "actor_kind": "DETERMINISTIC_MODULE",
                "role": "NOT_APPLICABLE_BY_RULE",
                "product_boundary": "ATOMIC_HARNESS_PIPELINE",
                "input_contracts": [],
                "output_contracts": [],
            }
            for nid, phase in nodes
        ],
        "edges": [
            {"source_node_id": s, "target_node_id": t} for s, t in edges
        ],
        "topological_order": node_ids,
        "evaluation_requirements": [],
    }


class TestCausalAdmissionService:
    def setup_method(self):
        self.svc = CausalAdmissionService()

    def test_positive_valid_progression_admitted(self):
        required = [
            RequiredAncestor("upstream_a", identity_digest="digest-a"),
            RequiredAncestor("upstream_b", identity_digest="digest-b"),
        ]
        bindings = {
            "upstream_a": _binding("upstream_a", digest="digest-a"),
            "upstream_b": _binding("upstream_b", digest="digest-b"),
        }
        states = {
            "upstream_a": NodeState.SUCCEEDED.value,
            "upstream_b": NodeState.SUCCEEDED.value,
            "downstream": NodeState.BLOCKED.value,
        }
        result = self.svc.evaluate(
            "downstream",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
            topological_order=["upstream_a", "upstream_b", "downstream"],
            phase_order=2,
            ancestor_phase_orders={"upstream_a": 0, "upstream_b": 1},
        )
        assert result.is_admitted
        assert result.decision == CausalAdmissionDecision.ADMITTED
        assert set(result.admitted_ancestors) == {"upstream_a", "upstream_b"}
        fact = result.to_runtime_fact()
        assert fact["admitted"] is True
        assert fact["blocks"] == []

    def test_negative_missing_ancestor(self):
        required = [RequiredAncestor("missing_upstream")]
        result = self.svc.evaluate(
            "downstream",
            required_ancestors=required,
            bindings={},
            node_states={"downstream": NodeState.BLOCKED.value},
        )
        assert not result.is_admitted
        assert any(b.reason == CausalBlockReason.MISSING_ANCESTOR for b in result.blocks)

    def test_negative_wrong_topological_order(self):
        required = [RequiredAncestor("later_node")]
        bindings = {"later_node": _binding("later_node")}
        states = {
            "later_node": NodeState.SUCCEEDED.value,
            "early_node": NodeState.BLOCKED.value,
        }
        result = self.svc.evaluate(
            "early_node",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
            topological_order=["early_node", "later_node"],  # later appears after early
        )
        assert not result.is_admitted
        assert any(b.reason == CausalBlockReason.WRONG_ORDER for b in result.blocks)

    def test_negative_wrong_phase_order(self):
        required = [RequiredAncestor("peer_or_later")]
        bindings = {"peer_or_later": _binding("peer_or_later")}
        states = {
            "peer_or_later": NodeState.SUCCEEDED.value,
            "node": NodeState.BLOCKED.value,
        }
        result = self.svc.evaluate(
            "node",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
            phase_order=1,
            ancestor_phase_orders={"peer_or_later": 1},  # same phase — not strictly before
        )
        assert not result.is_admitted
        assert any(b.reason == CausalBlockReason.WRONG_ORDER for b in result.blocks)

    def test_negative_stale_digest_mismatch(self):
        required = [RequiredAncestor("up", identity_digest="expected-digest")]
        bindings = {"up": _binding("up", digest="stale-digest")}
        states = {"up": NodeState.SUCCEEDED.value}
        result = self.svc.evaluate(
            "down",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
        )
        assert not result.is_admitted
        assert any(
            b.reason == CausalBlockReason.STALE_OR_MISMATCHED_IDENTITY for b in result.blocks
        )

    def test_negative_revision_mismatch(self):
        required = [RequiredAncestor("up", revision="rev-2")]
        bindings = {"up": _binding("up", revision="rev-1")}
        states = {"up": NodeState.SUCCEEDED.value}
        result = self.svc.evaluate(
            "down",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
        )
        assert not result.is_admitted
        assert any(
            b.reason == CausalBlockReason.STALE_OR_MISMATCHED_IDENTITY for b in result.blocks
        )

    def test_negative_invalid_prerequisite_state(self):
        required = [RequiredAncestor("up", required_state=NodeState.SUCCEEDED.value)]
        bindings = {"up": _binding("up", state=NodeState.FAILED.value)}
        states = {"up": NodeState.FAILED.value}
        result = self.svc.evaluate(
            "down",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
        )
        assert not result.is_admitted
        assert any(
            b.reason == CausalBlockReason.INVALID_PREREQUISITE_STATE for b in result.blocks
        )

    def test_negative_synthesized_placeholder(self):
        required = [RequiredAncestor("up")]
        bindings = {"up": _binding("up", is_placeholder=True)}
        states = {"up": NodeState.SUCCEEDED.value}
        result = self.svc.evaluate(
            "down",
            required_ancestors=required,
            bindings=bindings,
            node_states=states,
        )
        assert not result.is_admitted
        assert any(
            b.reason == CausalBlockReason.SYNTHESIZED_PLACEHOLDER for b in result.blocks
        )

    def test_negative_force_bypass_prohibited(self):
        result = self.svc.evaluate(
            "down",
            required_ancestors=[],
            bindings={},
            node_states={},
            force=True,
        )
        assert not result.is_admitted
        assert any(b.reason == CausalBlockReason.BYPASS_ATTEMPT for b in result.blocks)

    def test_require_admitted_raises(self):
        with pytest.raises(CausalAdmissionError) as excinfo:
            self.svc.require_admitted(
                "down",
                required_ancestors=[RequiredAncestor("missing")],
                bindings={},
                node_states={},
            )
        assert not excinfo.value.result.is_admitted

    def test_constructor_rejects_allow_force(self):
        with pytest.raises(PipelineValidationError):
            CausalAdmissionService(allow_force=True)

    def test_no_binding_when_state_present_but_no_identity(self):
        required = [RequiredAncestor("up")]
        # states has the node, but no binding provided
        result = self.svc.evaluate(
            "down",
            required_ancestors=required,
            bindings={},
            node_states={"up": NodeState.SUCCEEDED.value},
        )
        assert not result.is_admitted
        assert any(b.reason == CausalBlockReason.NO_BINDING for b in result.blocks)

    def test_bindings_from_artifacts_helper(self):
        states = {"a": NodeState.SUCCEEDED.value, "b": NodeState.READY.value}
        arts = {
            "a": {
                "identity": "id:a",
                "content_digest": "d-a",
                "revision": "1",
            },
            # b missing identity → omitted
        }
        bindings = self.svc.bindings_from_node_states_and_artifacts(states, arts)
        assert "a" in bindings
        assert "b" not in bindings
        assert bindings["a"].content_digest == "d-a"


class TestSchedulerCausalIntegration:
    def setup_method(self):
        self.scheduler = DeterministicScheduler()

    def test_ready_nodes_requires_succeeded_predecessors(self):
        wf = _minimal_workflow(
            [("a", 0), ("b", 1)],
            [("a", "b")],
        )
        states = {"a": NodeState.SUCCEEDED.value, "b": NodeState.BLOCKED.value}
        # Without bindings, causal integrity blocks even if state is SUCCEEDED
        ready = self.scheduler.ready_nodes(wf, states, enforce_causal=True)
        assert "b" not in ready  # no binding → not ready under causal enforcement

    def test_ready_nodes_with_valid_bindings_admits(self):
        wf = _minimal_workflow(
            [("a", 0), ("b", 1)],
            [("a", "b")],
        )
        states = {"a": NodeState.SUCCEEDED.value, "b": NodeState.BLOCKED.value}
        bindings = {"a": _binding("a")}
        ready = self.scheduler.ready_nodes(
            wf, states, ancestor_bindings=bindings, enforce_causal=True
        )
        assert "b" in ready

    def test_ready_nodes_blocks_wrong_order_via_causal(self):
        # edge a->b but topo puts b before a (invalid topo would be caught at register,
        # but phase_order check still applies)
        wf = _minimal_workflow(
            [("a", 2), ("b", 1)],  # b has lower phase but depends on a
            [("a", "b")],
        )
        states = {"a": NodeState.SUCCEEDED.value, "b": NodeState.BLOCKED.value}
        bindings = {"a": _binding("a")}
        ready = self.scheduler.ready_nodes(
            wf, states, ancestor_bindings=bindings, enforce_causal=True
        )
        assert "b" not in ready

    def test_admit_node_raises_on_missing(self):
        wf = _minimal_workflow(
            [("a", 0), ("b", 1)],
            [("a", "b")],
        )
        states = {"a": NodeState.BLOCKED.value, "b": NodeState.BLOCKED.value}
        with pytest.raises(CausalAdmissionError):
            self.scheduler.admit_node(wf, states, "b", ancestor_bindings={})

    def test_admit_node_succeeds_with_bindings(self):
        wf = _minimal_workflow(
            [("a", 0), ("b", 1)],
            [("a", "b")],
        )
        states = {"a": NodeState.SUCCEEDED.value, "b": NodeState.BLOCKED.value}
        bindings = {"a": _binding("a")}
        result = self.scheduler.admit_node(
            wf, states, "b", ancestor_bindings=bindings
        )
        assert result.is_admitted

    def test_force_on_admit_blocked(self):
        wf = _minimal_workflow([("a", 0)], [])
        states = {"a": NodeState.BLOCKED.value}
        with pytest.raises(CausalAdmissionError) as excinfo:
            self.scheduler.admit_node(wf, states, "a", force=True)
        assert any(
            b.reason == CausalBlockReason.BYPASS_ATTEMPT
            for b in excinfo.value.result.blocks
        )

    def test_enforce_causal_false_preserves_legacy_topology_only(self):
        """Regression: adjacent existing behavior (topology-only) still available when explicitly disabled."""
        wf = _minimal_workflow(
            [("a", 0), ("b", 1)],
            [("a", "b")],
        )
        states = {"a": NodeState.SUCCEEDED.value, "b": NodeState.BLOCKED.value}
        ready = self.scheduler.ready_nodes(wf, states, enforce_causal=False)
        assert "b" in ready  # legacy path without identity bindings


class TestRuntimeFactProjection:
    def test_blocked_fact_surface_for_ui(self):
        svc = CausalAdmissionService()
        result = svc.evaluate(
            "storyboard",
            required_ancestors=[RequiredAncestor("evidence_segments")],
            bindings={},
            node_states={},
        )
        fact = result.to_runtime_fact()
        assert fact["admitted"] is False
        assert fact["node_id"] == "storyboard"
        assert len(fact["blocks"]) >= 1
        assert fact["blocks"][0]["reason"] == CausalBlockReason.MISSING_ANCESTOR.value
