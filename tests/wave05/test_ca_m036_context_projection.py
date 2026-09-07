"""CA-M036 Acceptance Test Suite: Real State-Local Context Projection (INV-CTX-002).

Mandate: CA-M036 (Wave 05, Q36 / Spine Q03)
Invariant: INV-CTX-002 — input-scoped pruning + authority-lane masking + state_hash parity

Evidence classes required:
  EXECUTABLE positive path: node with restricted inputs receives only those fields,
      correctly masked, with matching state_hash.
  EXECUTABLE negative path: unauthorized-field request and hash-mismatch fail closed.
  Regression: existing get_local_context behaviour is unaffected.
  False-proof countercase: returning a subset of keys without lane/hash checks is not
      sufficient to satisfy INV-CTX-002.

All tests exercise the *real* state projection path in
  packages/ca_runtime/src/ca_runtime/program_state_runtime.py
and (for the pipeline-adapter variant) in
  services/pipeline/src/cmf_pipeline/adapters/jit_context_budget.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
from . import _support  # noqa: F401 — side-effect path registration

import hashlib
from typing import Any, Dict, List, Optional
from uuid import uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    # M036 new types / exceptions
    ContextProjectionError,
    ContextStateHashParityError,
    NodeDeclarationMissingError,
    PrunedContextSnapshot,
    _LANE_FIELD_ALLOW_LISTS,
    _compute_state_hash,
    _verify_state_hash_parity,
    # Existing runtime
    InMemoryProgramStateStore,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    UniversalProgramStateRuntime,
)
from cmf_pipeline.adapters.jit_context_budget import (
    ContextBudgetError,
    MissingNodeDeclarationError,
    StateHashParityError,
    compile_jit_context_snapshot,
    get_jit_context_snapshot,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_workspace_id() -> str:
    return str(uuid4())


def _make_runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime(store=InMemoryProgramStateStore())


def _make_aggregate(
    runtime: UniversalProgramStateRuntime,
    workspace_id: str,
    *,
    program_id: str = "research_source_ingestion_program",
    initial_data: Optional[Dict[str, Any]] = None,
) -> ProgramStateAggregate:
    return runtime.initialize_program_state(
        program_id=program_id,
        workspace_id=workspace_id,
        actor_id="usr_test",
        initial_data=initial_data or {},
    )


def _aggregate_with_state_data(
    runtime: UniversalProgramStateRuntime,
    workspace_id: str,
    data: Dict[str, Any],
    *,
    program_id: str = "research_source_ingestion_program",
) -> ProgramStateAggregate:
    """Helper: creates an aggregate pre-seeded with the given state_data."""
    agg = _make_aggregate(runtime, workspace_id, program_id=program_id, initial_data=data)
    return agg


# ---------------------------------------------------------------------------
# ============================================================
# GROUP 1: PrunedContextSnapshot via UniversalProgramStateRuntime
# ============================================================

class TestRuntimeGetPrunedLocalContext:
    """Tests for UniversalProgramStateRuntime.get_pruned_local_context (CA-M036)."""

    # ------------------------------------------------------------------
    # POSITIVE PATH: node receives only declared, lane-allowed fields
    # ------------------------------------------------------------------

    def test_positive_path_hunter_sees_declared_allowed_fields(self):
        """POSITIVE — HUNTER node with declared inputs receives only those fields, masked."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(
            rt, ws,
            {
                "hypothesis": "audience tension on identity",
                "corpus_refs": ["ref-A", "ref-B"],
                "approved_by": "operator-1",          # COMMANDER-only field
                "qa_scores": {"semantic": 90},       # ANALYST/COMMANDER field
                "script_draft": "INT. OFFICE — DAY",  # COMPOSER field
            },
        )

        snapshot = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="hunter_node_01",
            declared_inputs=["hypothesis", "corpus_refs", "approved_by"],
            active_lane=AuthorityLane.HUNTER,
        )

        # --- INV-CTX-002 positive assertions ---
        assert isinstance(snapshot, PrunedContextSnapshot)
        # Only declared keys that are in HUNTER allow-list survive
        assert "hypothesis" in snapshot.pruned_state_data
        assert "corpus_refs" in snapshot.pruned_state_data
        # approved_by is declared but NOT in HUNTER allow-list → masked
        assert "approved_by" not in snapshot.pruned_state_data
        assert "approved_by" in snapshot.masked_keys
        # Fields not declared at all are absent
        assert "qa_scores" not in snapshot.pruned_state_data
        assert "script_draft" not in snapshot.pruned_state_data
        # Envelope metadata
        assert snapshot.aggregate_id == agg.aggregate_id
        assert snapshot.active_lane == AuthorityLane.HUNTER
        assert snapshot.committed_state_hash == agg.state_hash
        # snapshot_hash must be non-empty and deterministic
        assert len(snapshot.snapshot_hash) == 64  # hex SHA-256

    def test_positive_path_analyst_sees_declared_analyst_fields(self):
        """POSITIVE — ANALYST node gets correct subset; COMMANDER fields masked."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(
            rt, ws,
            {
                "qa_scores": {"coherence": 85},
                "signals": ["sig-1"],
                "approved_by": "op-xyz",   # COMMANDER only
                "brief_content": "draft",  # COMPOSER only
            },
        )

        snapshot = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="analyst_node_02",
            declared_inputs=["qa_scores", "signals", "approved_by", "brief_content"],
            active_lane=AuthorityLane.ANALYST,
        )

        assert "qa_scores" in snapshot.pruned_state_data
        assert "signals" in snapshot.pruned_state_data
        assert "approved_by" not in snapshot.pruned_state_data   # masked
        assert "brief_content" not in snapshot.pruned_state_data # masked
        assert sorted(snapshot.masked_keys) == sorted(["approved_by", "brief_content"])

    def test_positive_path_commander_sees_governance_fields(self):
        """POSITIVE — COMMANDER node sees governance/approval fields; COMPOSER fields masked."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(
            rt, ws,
            {
                "approved_by": "operator-99",
                "operator_decision": "APPROVED",
                "script_draft": "confidential-script",  # COMPOSER only
                "corpus_refs": ["ref-Z"],               # HUNTER only
            },
        )

        snapshot = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="commander_gate_01",
            declared_inputs=["approved_by", "operator_decision", "script_draft", "corpus_refs"],
            active_lane=AuthorityLane.COMMANDER,
        )

        assert "approved_by" in snapshot.pruned_state_data
        assert "operator_decision" in snapshot.pruned_state_data
        # COMMANDER does not see COMPOSER or HUNTER exclusive fields
        assert "script_draft" not in snapshot.pruned_state_data
        assert "corpus_refs" not in snapshot.pruned_state_data

    def test_positive_path_snapshot_hash_is_deterministic(self):
        """POSITIVE — snapshot_hash must be deterministic for the same inputs."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(rt, ws, {"hypothesis": "test-hyp"})

        snap1 = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="node_X",
            declared_inputs=["hypothesis"],
            active_lane=AuthorityLane.HUNTER,
        )
        snap2 = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="node_X",
            declared_inputs=["hypothesis"],
            active_lane=AuthorityLane.HUNTER,
        )
        assert snap1.snapshot_hash == snap2.snapshot_hash

    def test_positive_path_snapshot_hash_differs_for_different_node_id(self):
        """POSITIVE — snapshot_hash must change if node_id changes (audit isolation)."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(rt, ws, {"hypothesis": "test-hyp"})

        snap1 = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="node_A",
            declared_inputs=["hypothesis"],
            active_lane=AuthorityLane.HUNTER,
        )
        snap2 = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="node_B",
            declared_inputs=["hypothesis"],
            active_lane=AuthorityLane.HUNTER,
        )
        assert snap1.snapshot_hash != snap2.snapshot_hash

    def test_positive_path_committed_state_hash_matches_aggregate(self):
        """POSITIVE — committed_state_hash in snapshot equals aggregate.state_hash."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(rt, ws, {"hypothesis": "h1"})

        snap = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="n1",
            declared_inputs=["hypothesis"],
            active_lane=AuthorityLane.HUNTER,
        )
        assert snap.committed_state_hash == agg.state_hash

    # ------------------------------------------------------------------
    # NEGATIVE PATH: fail-closed on missing declarations
    # ------------------------------------------------------------------

    def test_negative_path_empty_declared_inputs_raises(self):
        """NEGATIVE — empty declared_inputs raises NodeDeclarationMissingError (fail-closed)."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws)

        with pytest.raises(NodeDeclarationMissingError) as exc_info:
            rt.get_pruned_local_context(
                agg.aggregate_id,
                node_id="bad_node",
                declared_inputs=[],
                active_lane=AuthorityLane.HUNTER,
            )

        err = exc_info.value
        assert err.reason_code == "NODE_DECLARATION_MISSING"
        assert "bad_node" in str(err)

    def test_negative_path_none_declared_inputs_raises(self):
        """NEGATIVE — None declared_inputs raises NodeDeclarationMissingError."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws)

        with pytest.raises(NodeDeclarationMissingError):
            rt.get_pruned_local_context(
                agg.aggregate_id,
                node_id="no_decl_node",
                declared_inputs=None,
                active_lane=AuthorityLane.ANALYST,
            )

    def test_negative_path_state_hash_parity_failure_raises(self):
        """NEGATIVE — tampered aggregate.state_hash raises ContextStateHashParityError."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws, initial_data={"hypothesis": "original"})

        # Directly tamper with state_hash by writing a corrupted aggregate to the store
        corrupted = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=agg.state_data,
            version=agg.version,
            state_hash="deadbeef" * 8,   # deliberately wrong hash
            lifecycle=agg.lifecycle,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
        rt.store._aggregates[agg.aggregate_id] = corrupted

        with pytest.raises(ContextStateHashParityError) as exc_info:
            rt.get_pruned_local_context(
                agg.aggregate_id,
                node_id="parity_check_node",
                declared_inputs=["hypothesis"],
                active_lane=AuthorityLane.HUNTER,
            )
        err = exc_info.value
        assert err.reason_code == "CONTEXT_STATE_HASH_PARITY_FAILURE"
        assert "deadbeef" * 8 in str(err)

    def test_negative_path_unauthorized_field_not_leaked(self):
        """NEGATIVE — declaring a field the lane cannot see never leaks the value."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(
            rt, ws,
            {
                "script_draft": "SECRET COMPOSER DATA",  # COMPOSER only
                "hypothesis": "safe",
            },
        )

        # HUNTER requests a COMPOSER-only field
        snap = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="hunter_attempt",
            declared_inputs=["script_draft", "hypothesis"],
            active_lane=AuthorityLane.HUNTER,
        )

        # script_draft must never appear in pruned data
        assert "script_draft" not in snap.pruned_state_data
        assert snap.pruned_state_data.get("script_draft") is None
        # It should appear in masked_keys for audit
        assert "script_draft" in snap.masked_keys
        # The allowed field still comes through
        assert "hypothesis" in snap.pruned_state_data

    def test_negative_path_all_declared_keys_masked_yields_empty_data(self):
        """NEGATIVE — if all declared inputs are outside the lane, pruned_state_data is empty."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(
            rt, ws,
            {"script_draft": "RESTRICTED", "brief_content": "RESTRICTED TOO"},
        )

        # HUNTER requests COMPOSER-only fields
        snap = rt.get_pruned_local_context(
            agg.aggregate_id,
            node_id="hunter_restricted",
            declared_inputs=["script_draft", "brief_content"],
            active_lane=AuthorityLane.HUNTER,
        )

        assert snap.pruned_state_data == {}
        assert sorted(snap.masked_keys) == sorted(["script_draft", "brief_content"])

    # ------------------------------------------------------------------
    # Regression: existing get_local_context is unaffected
    # ------------------------------------------------------------------

    def test_regression_get_local_context_still_works(self):
        """REGRESSION — get_local_context continues to return ProgramStateLocalContext."""
        from ca_runtime.program_state_runtime import ProgramStateLocalContext
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws)

        ctx = rt.get_local_context(agg.aggregate_id, active_lane=AuthorityLane.HUNTER)
        assert isinstance(ctx, ProgramStateLocalContext)
        assert ctx.aggregate.aggregate_id == agg.aggregate_id
        # Full state_data is accessible via get_local_context (governance surface)
        assert ctx.aggregate.state_data is not None

    def test_regression_execute_transition_unaffected(self):
        """REGRESSION — executing transitions is unaffected by M036 changes."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws, initial_data={"source_origin": "https://example.com"})

        result = rt.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="admit_source",
            actor_id="usr_hunter",
            actor_lane=AuthorityLane.HUNTER,
            context_claims={"workspace_active", "source_origin_valid"},
        )
        assert result.aggregate.current_state == "SOURCE_ADMITTED"

    # ------------------------------------------------------------------
    # False-proof countercase
    # ------------------------------------------------------------------

    def test_false_proof_countercase_simple_key_filter_is_not_enough(self):
        """FALSE-PROOF — returning a subset of keys without lane/hash checks is insufficient.

        This test demonstrates that code which merely filters keys but skips
        state_hash parity and lane masking would NOT satisfy INV-CTX-002.
        The real implementation (get_pruned_local_context) must fail here if
        the hash is wrong, even though the key filtering alone would succeed.
        """
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws, initial_data={"hypothesis": "valid"})

        # Tamper with the aggregate state_hash
        corrupted = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=agg.state_data,   # Data unchanged — key filter would succeed
            version=agg.version,
            state_hash="0" * 64,          # Corrupted hash
            lifecycle=agg.lifecycle,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
        rt.store._aggregates[agg.aggregate_id] = corrupted

        # A naive implementation that only filters keys would succeed here.
        # Our implementation MUST raise because hash parity fails.
        with pytest.raises(ContextStateHashParityError):
            rt.get_pruned_local_context(
                agg.aggregate_id,
                node_id="n",
                declared_inputs=["hypothesis"],
                active_lane=AuthorityLane.HUNTER,
            )


# ---------------------------------------------------------------------------
# ============================================================
# GROUP 2: compile_jit_context_snapshot (pipeline adapter)
# ============================================================

class TestCompileJitContextSnapshot:
    """Tests for cmf_pipeline.adapters.jit_context_budget.compile_jit_context_snapshot."""

    def _make_clean_aggregate(self, state_data: Dict[str, Any]) -> ProgramStateAggregate:
        ws = _make_workspace_id()
        rt = _make_runtime()
        return _aggregate_with_state_data(rt, ws, state_data)

    # POSITIVE
    def test_positive_path_basic_compile(self):
        """POSITIVE — compile produces pruned snapshot with correct hash binding."""
        agg = self._make_clean_aggregate(
            {"hypothesis": "h1", "corpus_refs": ["r1"], "script_draft": "forbidden"}
        )
        snap = compile_jit_context_snapshot(
            aggregate=agg,
            node_id="adapter_node_01",
            declared_inputs=["hypothesis", "corpus_refs", "script_draft"],
            active_lane=AuthorityLane.HUNTER,
        )
        assert isinstance(snap, PrunedContextSnapshot)
        assert "hypothesis" in snap.pruned_state_data
        assert "corpus_refs" in snap.pruned_state_data
        assert "script_draft" not in snap.pruned_state_data
        assert snap.committed_state_hash == agg.state_hash
        assert len(snap.snapshot_hash) == 64

    def test_positive_path_composer_lane(self):
        """POSITIVE — COMPOSER lane sees only composer-allowed fields."""
        agg = self._make_clean_aggregate(
            {
                "brief_content": "intro paragraph",
                "script_draft": "line 1",
                "hypothesis": "background context",
            }
        )
        snap = compile_jit_context_snapshot(
            aggregate=agg,
            node_id="composer_node",
            declared_inputs=["brief_content", "script_draft", "hypothesis"],
            active_lane=AuthorityLane.COMPOSER,
        )
        assert "brief_content" in snap.pruned_state_data
        assert "script_draft" in snap.pruned_state_data
        # hypothesis is in ANALYST/HUNTER/COMMANDER but NOT in COMPOSER allow-list
        assert "hypothesis" not in snap.pruned_state_data
        assert "hypothesis" in snap.masked_keys

    # NEGATIVE
    def test_negative_path_empty_declared_inputs_raises(self):
        """NEGATIVE — empty declared_inputs raises MissingNodeDeclarationError."""
        agg = self._make_clean_aggregate({"hypothesis": "test"})
        with pytest.raises(MissingNodeDeclarationError) as exc_info:
            compile_jit_context_snapshot(
                aggregate=agg,
                node_id="empty_node",
                declared_inputs=[],
                active_lane=AuthorityLane.HUNTER,
            )
        assert exc_info.value.reason_code == "MISSING_NODE_DECLARATION"

    def test_negative_path_tampered_hash_raises(self):
        """NEGATIVE — tampered state_hash raises StateHashParityError (fail-closed)."""
        agg = self._make_clean_aggregate({"hypothesis": "legit"})
        # Build a tampered copy with wrong hash
        tampered = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=agg.state_data,
            version=agg.version,
            state_hash="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            lifecycle=agg.lifecycle,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
        with pytest.raises(StateHashParityError) as exc_info:
            compile_jit_context_snapshot(
                aggregate=tampered,
                node_id="tamper_check",
                declared_inputs=["hypothesis"],
                active_lane=AuthorityLane.HUNTER,
            )
        assert exc_info.value.reason_code == "STATE_HASH_PARITY_FAILURE"

    def test_negative_path_cross_lane_leakage_is_blocked(self):
        """NEGATIVE — ANALYST node cannot obtain COMMANDER-only field even if declared."""
        agg = self._make_clean_aggregate(
            {"approved_by": "op-9", "signals": ["s1"]}
        )
        snap = compile_jit_context_snapshot(
            aggregate=agg,
            node_id="analyst_cross",
            declared_inputs=["approved_by", "signals"],
            active_lane=AuthorityLane.ANALYST,
        )
        # signals is in ANALYST allow-list
        assert "signals" in snap.pruned_state_data
        # approved_by is COMMANDER-only
        assert "approved_by" not in snap.pruned_state_data
        assert "approved_by" in snap.masked_keys


# ---------------------------------------------------------------------------
# ============================================================
# GROUP 3: get_jit_context_snapshot (runtime-integrated pipeline helper)
# ============================================================

class TestGetJitContextSnapshot:
    """Tests for cmf_pipeline.adapters.jit_context_budget.get_jit_context_snapshot."""

    def test_positive_integration_with_runtime(self):
        """POSITIVE — get_jit_context_snapshot fetches from runtime and projects correctly."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _aggregate_with_state_data(
            rt, ws, {"hypothesis": "integration_test", "corpus_refs": ["cr-1"]}
        )

        snap = get_jit_context_snapshot(
            rt,
            aggregate_id=agg.aggregate_id,
            node_id="integration_node",
            declared_inputs=["hypothesis", "corpus_refs"],
            active_lane=AuthorityLane.HUNTER,
        )

        assert snap.aggregate_id == agg.aggregate_id
        assert "hypothesis" in snap.pruned_state_data
        assert "corpus_refs" in snap.pruned_state_data

    def test_negative_aggregate_not_found(self):
        """NEGATIVE — non-existent aggregate raises ProgramStateAggregateNotFoundError."""
        from ca_runtime.program_state_runtime import ProgramStateAggregateNotFoundError
        rt = _make_runtime()
        with pytest.raises(ProgramStateAggregateNotFoundError):
            get_jit_context_snapshot(
                rt,
                aggregate_id="prog-state:nonexistent",
                node_id="n",
                declared_inputs=["hypothesis"],
                active_lane=AuthorityLane.HUNTER,
            )


# ---------------------------------------------------------------------------
# ============================================================
# GROUP 4: _verify_state_hash_parity helper
# ============================================================

class TestVerifyStateHashParity:
    """Unit tests for the _verify_state_hash_parity helper."""

    def test_valid_hash_returns_hash(self):
        """Clean aggregate: returns the committed hash."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws, initial_data={"a": 1})
        result = _verify_state_hash_parity(agg)
        assert result == agg.state_hash

    def test_invalid_hash_raises(self):
        """Tampered hash: raises ContextStateHashParityError."""
        ws = _make_workspace_id()
        rt = _make_runtime()
        agg = _make_aggregate(rt, ws, initial_data={"a": 1})

        tampered = ProgramStateAggregate(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            cae_run_id=agg.cae_run_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            current_state=agg.current_state,
            state_data=agg.state_data,
            version=agg.version,
            state_hash="badhash" + "0" * 57,
            lifecycle=agg.lifecycle,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
        with pytest.raises(ContextStateHashParityError):
            _verify_state_hash_parity(tampered)


# ---------------------------------------------------------------------------
# ============================================================
# GROUP 5: Lane allow-list integrity (prevent regression of masking)
# ============================================================

class TestLaneAllowListIntegrity:
    """Structural tests to prevent inadvertent relaxation of masking rules."""

    def test_all_four_lanes_have_allow_lists(self):
        """All four authority lanes must have entries in _LANE_FIELD_ALLOW_LISTS."""
        for lane in AuthorityLane:
            assert lane in _LANE_FIELD_ALLOW_LISTS, (
                f"AuthorityLane.{lane.name} has no allow-list entry — "
                "this would cause all fields to be masked for that lane."
            )

    def test_no_lane_has_empty_allow_list(self):
        """Every lane must allow at least one field (node_id / declared_inputs)."""
        for lane, allow_set in _LANE_FIELD_ALLOW_LISTS.items():
            assert len(allow_set) > 0, (
                f"AuthorityLane.{lane.name} allow-list is empty — "
                "nodes of this lane could never receive any context."
            )

    def test_commander_does_not_see_composer_exclusive_script_draft(self):
        """Structural: script_draft must NOT be in COMMANDER allow-list."""
        assert "script_draft" not in _LANE_FIELD_ALLOW_LISTS[AuthorityLane.COMMANDER]

    def test_hunter_does_not_see_script_draft_or_brief_content(self):
        """Structural: HUNTER must not see COMPOSER-exclusive fields."""
        hunter_allow = _LANE_FIELD_ALLOW_LISTS[AuthorityLane.HUNTER]
        assert "script_draft" not in hunter_allow
        assert "brief_content" not in hunter_allow

    def test_all_lanes_allow_declared_inputs_and_repairs(self):
        """Structural: declared_inputs and repairs must be visible to all lanes."""
        for lane, allow_set in _LANE_FIELD_ALLOW_LISTS.items():
            assert "declared_inputs" in allow_set, (
                f"Lane {lane.name} cannot see declared_inputs — "
                "nodes would be unable to verify their own contract."
            )
            assert "repairs" in allow_set, (
                f"Lane {lane.name} cannot see repairs — "
                "repair audit trail would be invisible to this lane."
            )
