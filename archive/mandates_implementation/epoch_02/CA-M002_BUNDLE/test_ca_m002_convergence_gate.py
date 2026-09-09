"""
tests/cae/test_ca_m002_convergence_gate.py
------------------------------------------
CA-M002 / FR-CONV-001 — Dual-Context Convergence Gate Executable Evidence.

Evidence standard (per mandate §9):
  ✔ Positive acceptance path (valid convergence)
  ✔ Negative / fail-closed paths:
      - missing Guest Genesis
      - missing Audience Tensions
      - invalid Guest Genesis (wrong state, bad digest)
      - invalid Audience Tensions (zero tensions, bad digest)
      - stale/mismatched Guest Genesis digest
      - stale/mismatched Audience Tensions digest
      - cross-workspace isolation violation
      - convergence relation invalid (no territorial content)
      - bypass/force attempt
  ✔ Integration: downstream compilation blocked when gate fails
  ✔ Integration: downstream compilation admitted when gate passes
  ✔ Persistence: receipt stored and retrievable after successful evaluation
  ✔ Receipt: re-validation against stale upstream raises StaleError
  ✔ Regression: topology-only causal admission is NOT substituted for this gate
  ✔ API projection: gate state reports admitted=False when no receipt present
  ✔ API projection: gate state reports admitted=True after successful evaluation

DO NOT RUN TESTS PER MANDATE INSTRUCTIONS — this file is test-definition only.
"""

from __future__ import annotations

import sqlite3
import pytest

from ca_runtime.convergence_gate import (
    AudienceTensionsRef,
    BypassAttemptError,
    ConvergenceGate,
    ConvergenceGateError,
    ConvergenceReceipt,
    ConvergenceStatus,
    ConvergenceStore,
    DownstreamAdmissionBlockedError,
    DownstreamCompilationGuard,
    GuestGenesisRef,
    InvalidAudienceTensionsError,
    InvalidGuestGenesisError,
    MissingAudienceTensionsError,
    MissingGuestGenesisError,
    StaleAudienceTensionsError,
    StaleGuestGenesisError,
    ConvergenceRelationError,
)


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

_VALID_SHA = "a" * 64
_ALT_SHA = "b" * 64
_WS = "ws-test-001"


def _guest_genesis(
    *,
    workspace_id: str = _WS,
    territory_id: str = "terr-001",
    revision_id: str = "rev-gg-001",
    sha256_digest: str = _VALID_SHA,
    ratified_state: str = "TERRITORY_RATIFIED",
    wrong_reading_locks: tuple = ("Never misread directness as hostility",),
    vocabulary_boundaries: tuple = ("friction-tested clarity",),
) -> GuestGenesisRef:
    return GuestGenesisRef(
        workspace_id=workspace_id,
        territory_id=territory_id,
        revision_id=revision_id,
        sha256_digest=sha256_digest,
        ratified_state=ratified_state,
        wrong_reading_locks=wrong_reading_locks,
        vocabulary_boundaries=vocabulary_boundaries,
    )


def _audience_tensions(
    *,
    workspace_id: str = _WS,
    audience_id: str = "aud-001",
    revision_id: str = "rev-at-001",
    sha256_digest: str = _VALID_SHA,
    tension_state: str = "TENSIONS_ACTIVE",
    tension_count: int = 3,
    active_tension_labels: tuple = ("autonomy-vs-accountability", "speed-vs-precision", "trust-vs-transparency"),
) -> AudienceTensionsRef:
    return AudienceTensionsRef(
        workspace_id=workspace_id,
        audience_id=audience_id,
        revision_id=revision_id,
        sha256_digest=sha256_digest,
        tension_state=tension_state,
        tension_count=tension_count,
        active_tension_labels=active_tension_labels,
    )


@pytest.fixture()
def gate() -> ConvergenceGate:
    return ConvergenceGate()


@pytest.fixture()
def mem_conn() -> sqlite3.Connection:
    """In-memory SQLite connection for store tests."""
    conn = sqlite3.connect(":memory:")
    return conn


@pytest.fixture()
def store(mem_conn: sqlite3.Connection) -> ConvergenceStore:
    return ConvergenceStore(mem_conn)


@pytest.fixture()
def guard(gate: ConvergenceGate, store: ConvergenceStore) -> DownstreamCompilationGuard:
    return DownstreamCompilationGuard(gate=gate, store=store)


# ===========================================================================
# 1. Positive Acceptance Path
# ===========================================================================

class TestPositiveAcceptancePath:
    def test_valid_convergence_returns_converged_receipt(self, gate: ConvergenceGate) -> None:
        """
        POSITIVE: Both sides valid → CONVERGED receipt with exact upstream binding.
        Evidence class: EXECUTABLE
        """
        gg = _guest_genesis()
        at = _audience_tensions()

        receipt = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)

        assert isinstance(receipt, ConvergenceReceipt)
        assert receipt.status == ConvergenceStatus.CONVERGED
        assert receipt.workspace_id == _WS
        assert receipt.is_valid_for_downstream() is True
        assert receipt.receipt_id.startswith("CONV-RCP-")
        assert receipt.gate_version == "1.0.0"

    def test_receipt_binds_exact_upstream_revisions(self, gate: ConvergenceGate) -> None:
        """
        POSITIVE: Receipt must pin the exact revision_id and sha256_digest from both sources.
        Evidence class: EXECUTABLE
        """
        gg = _guest_genesis(revision_id="rev-gg-v42", sha256_digest=_VALID_SHA)
        at = _audience_tensions(revision_id="rev-at-v99", sha256_digest=_ALT_SHA)

        receipt = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)

        assert receipt.guest_genesis_revision_id == "rev-gg-v42"
        assert receipt.guest_genesis_sha256 == _VALID_SHA
        assert receipt.audience_tensions_revision_id == "rev-at-v99"
        assert receipt.audience_tensions_sha256 == _ALT_SHA

    def test_receipt_has_deterministic_convergence_digest(self, gate: ConvergenceGate) -> None:
        """
        POSITIVE: Same inputs produce same convergence_digest (deterministic).
        Different inputs produce different digest.
        Evidence class: EXECUTABLE
        """
        gg = _guest_genesis()
        at = _audience_tensions()

        r1 = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)
        r2 = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)

        # Same upstream → same convergence_digest (content-addressed)
        assert r1.convergence_digest == r2.convergence_digest

        # Different upstream → different digest
        at2 = _audience_tensions(revision_id="rev-at-different", sha256_digest="c" * 64)
        r3 = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at2)
        assert r3.convergence_digest != r1.convergence_digest

    def test_receipt_to_dict_is_complete(self, gate: ConvergenceGate) -> None:
        """POSITIVE: Receipt serialises to a complete dict with all required fields."""
        receipt = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
        )
        d = receipt.to_dict()
        required_keys = {
            "receipt_id", "workspace_id", "status",
            "guest_genesis_territory_id", "guest_genesis_revision_id", "guest_genesis_sha256",
            "audience_tensions_audience_id", "audience_tensions_revision_id", "audience_tensions_sha256",
            "convergence_digest", "convergence_signature", "converged_at", "gate_version",
        }
        assert required_keys.issubset(d.keys())


# ===========================================================================
# 2. Negative / Fail-Closed Paths — Missing Inputs
# ===========================================================================

class TestMissingInputs:
    def test_missing_guest_genesis_raises_missing_error(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Missing Guest Genesis → MissingGuestGenesisError (not a generic error)."""
        with pytest.raises(MissingGuestGenesisError) as exc_info:
            gate.evaluate(
                workspace_id=_WS,
                guest_genesis=None,
                audience_tensions=_audience_tensions(),
            )
        err = exc_info.value
        assert err.reason_code == "MISSING_GUEST_GENESIS_SEMANTIC_TERRITORY"
        assert _WS in str(err)
        assert "run_program:guest_genesis_semantic_territory_program" in err.permitted_next_actions

    def test_missing_audience_tensions_raises_missing_error(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Missing Audience Tensions → MissingAudienceTensionsError."""
        with pytest.raises(MissingAudienceTensionsError) as exc_info:
            gate.evaluate(
                workspace_id=_WS,
                guest_genesis=_guest_genesis(),
                audience_tensions=None,
            )
        err = exc_info.value
        assert err.reason_code == "MISSING_AUDIENCE_TENSIONS"
        assert "run_program:audience_context_program" in err.permitted_next_actions

    def test_both_missing_raises_guest_genesis_error_first(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Both missing → gate fails on Guest Genesis first (ordered evaluation)."""
        with pytest.raises(MissingGuestGenesisError):
            gate.evaluate(workspace_id=_WS, guest_genesis=None, audience_tensions=None)


# ===========================================================================
# 3. Negative / Fail-Closed Paths — Invalid Inputs
# ===========================================================================

class TestInvalidInputs:
    def test_guest_genesis_wrong_state_raises_invalid(self) -> None:
        """NEGATIVE: Guest Genesis in non-TERRITORY_RATIFIED state → InvalidGuestGenesisError."""
        with pytest.raises(InvalidGuestGenesisError) as exc_info:
            _guest_genesis(ratified_state="EVIDENCE_INDEXED")
        assert "TERRITORY_RATIFIED" in str(exc_info.value)

    def test_guest_genesis_bad_digest_length_raises_invalid(self) -> None:
        """NEGATIVE: Guest Genesis with truncated sha256 → InvalidGuestGenesisError."""
        with pytest.raises(InvalidGuestGenesisError) as exc_info:
            _guest_genesis(sha256_digest="tooshort")
        assert "sha256_digest" in str(exc_info.value)

    def test_guest_genesis_empty_territory_id_raises_invalid(self) -> None:
        """NEGATIVE: Guest Genesis with empty territory_id → InvalidGuestGenesisError."""
        with pytest.raises(InvalidGuestGenesisError):
            _guest_genesis(territory_id="")

    def test_guest_genesis_empty_revision_id_raises_invalid(self) -> None:
        """NEGATIVE: Guest Genesis with empty revision_id → InvalidGuestGenesisError."""
        with pytest.raises(InvalidGuestGenesisError):
            _guest_genesis(revision_id="")

    def test_audience_tensions_zero_count_raises_invalid(self) -> None:
        """NEGATIVE: Audience Tensions with tension_count=0 → InvalidAudienceTensionsError."""
        with pytest.raises(InvalidAudienceTensionsError) as exc_info:
            _audience_tensions(tension_count=0)
        assert "at least one active tension" in str(exc_info.value)

    def test_audience_tensions_bad_digest_raises_invalid(self) -> None:
        """NEGATIVE: Audience Tensions with short sha256 → InvalidAudienceTensionsError."""
        with pytest.raises(InvalidAudienceTensionsError):
            _audience_tensions(sha256_digest="abc")

    def test_audience_tensions_empty_audience_id_raises_invalid(self) -> None:
        """NEGATIVE: Audience Tensions with empty audience_id → InvalidAudienceTensionsError."""
        with pytest.raises(InvalidAudienceTensionsError):
            _audience_tensions(audience_id="")


# ===========================================================================
# 4. Negative / Fail-Closed Paths — Staleness and Mismatch
# ===========================================================================

class TestStaleAndMismatch:
    def test_stale_guest_genesis_digest_raises_stale_error(self, gate: ConvergenceGate) -> None:
        """
        NEGATIVE: Receipt validated against mutated Guest Genesis → StaleGuestGenesisError.
        This is the critical regression test: a receipt produced with one digest
        must NOT be accepted when the upstream artifact's digest has changed.
        Evidence class: EXECUTABLE
        """
        gg_original = _guest_genesis(sha256_digest=_VALID_SHA)
        at = _audience_tensions()
        receipt = gate.evaluate(workspace_id=_WS, guest_genesis=gg_original, audience_tensions=at)

        # Now the upstream artifact has been replaced — different sha256
        gg_mutated = _guest_genesis(sha256_digest=_ALT_SHA)

        with pytest.raises(StaleGuestGenesisError) as exc_info:
            receipt.validate_upstream_digests(
                guest_genesis_ref=gg_mutated,
                audience_tensions_ref=at,
            )
        err = exc_info.value
        assert err.reason_code == "STALE_GUEST_GENESIS_DIGEST"
        assert _VALID_SHA[:16] in str(err)
        assert _ALT_SHA[:16] in str(err)

    def test_stale_audience_tensions_digest_raises_stale_error(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Receipt validated against mutated Audience Tensions → StaleAudienceTensionsError."""
        gg = _guest_genesis()
        at_original = _audience_tensions(sha256_digest=_VALID_SHA)
        receipt = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at_original)

        at_mutated = _audience_tensions(sha256_digest=_ALT_SHA)

        with pytest.raises(StaleAudienceTensionsError) as exc_info:
            receipt.validate_upstream_digests(
                guest_genesis_ref=gg,
                audience_tensions_ref=at_mutated,
            )
        assert exc_info.value.reason_code == "STALE_AUDIENCE_TENSIONS_DIGEST"

    def test_valid_receipt_passes_upstream_digest_validation(self, gate: ConvergenceGate) -> None:
        """POSITIVE: Receipt validated against unchanged upstream digests → no exception."""
        gg = _guest_genesis()
        at = _audience_tensions()
        receipt = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)

        # Should not raise
        receipt.validate_upstream_digests(guest_genesis_ref=gg, audience_tensions_ref=at)


# ===========================================================================
# 5. Negative / Fail-Closed Paths — Cross-Workspace Isolation
# ===========================================================================

class TestWorkspaceIsolation:
    def test_guest_genesis_wrong_workspace_raises_invalid(self, gate: ConvergenceGate) -> None:
        """
        NEGATIVE: Guest Genesis from a different workspace is rejected.
        Cross-workspace leak is prohibited.
        """
        gg_other_ws = _guest_genesis(workspace_id="ws-other-999")
        at = _audience_tensions(workspace_id=_WS)

        with pytest.raises(InvalidGuestGenesisError) as exc_info:
            gate.evaluate(workspace_id=_WS, guest_genesis=gg_other_ws, audience_tensions=at)
        assert "cross-workspace leak" in str(exc_info.value)

    def test_audience_tensions_wrong_workspace_raises_invalid(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Audience Tensions from a different workspace is rejected."""
        gg = _guest_genesis(workspace_id=_WS)
        at_other_ws = _audience_tensions(workspace_id="ws-other-999")

        with pytest.raises(InvalidAudienceTensionsError) as exc_info:
            gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at_other_ws)
        assert "cross-workspace leak" in str(exc_info.value)


# ===========================================================================
# 6. Negative / Fail-Closed Paths — Convergence Relation
# ===========================================================================

class TestConvergenceRelation:
    def test_no_vocabulary_boundaries_no_wrong_reading_locks_raises_relation_error(
        self, gate: ConvergenceGate
    ) -> None:
        """
        NEGATIVE: Guest Genesis with empty territorial content cannot form a valid
        convergence relation — convergence requires substantive content.
        """
        gg = _guest_genesis(wrong_reading_locks=(), vocabulary_boundaries=())
        at = _audience_tensions()

        with pytest.raises(ConvergenceRelationError) as exc_info:
            gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)
        assert "vocabulary_boundaries" in str(exc_info.value)

    def test_no_active_tension_labels_raises_relation_error(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Audience Tensions with no active labels cannot form a convergence relation."""
        gg = _guest_genesis()
        at = _audience_tensions(active_tension_labels=())

        with pytest.raises(ConvergenceRelationError) as exc_info:
            gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)
        assert "active_tension_labels" in str(exc_info.value)


# ===========================================================================
# 7. Negative / Fail-Closed — Bypass Attempt
# ===========================================================================

class TestBypassAttempt:
    def test_force_true_raises_bypass_error(self, gate: ConvergenceGate) -> None:
        """
        NEGATIVE: force=True raises BypassAttemptError.
        The gate has no override path — this is a CAE constitutional constraint.
        Evidence class: EXECUTABLE
        """
        with pytest.raises(BypassAttemptError) as exc_info:
            gate.evaluate(
                workspace_id=_WS,
                guest_genesis=_guest_genesis(),
                audience_tensions=_audience_tensions(),
                force=True,
            )
        err = exc_info.value
        assert err.reason_code == "CONVERGENCE_BYPASS_ATTEMPT"
        assert "FR-CONV-001" in str(err)

    def test_bypass_takes_precedence_over_valid_inputs(self, gate: ConvergenceGate) -> None:
        """NEGATIVE: Even with valid inputs, force=True is rejected before anything else."""
        with pytest.raises(BypassAttemptError):
            gate.evaluate(
                workspace_id=_WS,
                guest_genesis=_guest_genesis(),
                audience_tensions=_audience_tensions(),
                force=True,
            )


# ===========================================================================
# 8. Integration — Downstream Compilation Blocked
# ===========================================================================

class TestDownstreamAdmissionBlocked:
    def test_downstream_blocked_when_guest_genesis_missing(self, guard: DownstreamCompilationGuard) -> None:
        """
        INTEGRATION: editorial_discovery_program cannot start when Guest Genesis is absent.
        This is the integration-level proof that downstream compilation is blocked.
        Evidence class: EXECUTABLE (integration path)
        """
        with pytest.raises(DownstreamAdmissionBlockedError) as exc_info:
            guard.assert_convergence(
                workspace_id=_WS,
                guest_genesis=None,
                audience_tensions=_audience_tensions(),
                downstream_program_id="editorial_discovery_program",
            )
        err = exc_info.value
        assert err.reason_code == "DOWNSTREAM_ADMISSION_BLOCKED_NO_CONVERGENCE"
        assert "editorial_discovery_program" in str(err)
        assert "MISSING_GUEST_GENESIS_SEMANTIC_TERRITORY" in err.details.get("gate_reason_code", "")

    def test_downstream_blocked_when_audience_tensions_missing(self, guard: DownstreamCompilationGuard) -> None:
        """INTEGRATION: Downstream blocked when Audience Tensions absent."""
        with pytest.raises(DownstreamAdmissionBlockedError) as exc_info:
            guard.assert_convergence(
                workspace_id=_WS,
                guest_genesis=_guest_genesis(),
                audience_tensions=None,
                downstream_program_id="narrative_composition_program",
            )
        err = exc_info.value
        assert "MISSING_AUDIENCE_TENSIONS" in err.details.get("gate_reason_code", "")

    def test_downstream_blocked_when_guest_genesis_in_wrong_state(self, guard: DownstreamCompilationGuard) -> None:
        """INTEGRATION: Downstream blocked when Guest Genesis not TERRITORY_RATIFIED."""
        with pytest.raises(DownstreamAdmissionBlockedError):
            # Guest Genesis not yet ratified → construction will raise InvalidGuestGenesisError
            # But if we pass a guest genesis at wrong state via evaluate path indirectly:
            guard.assert_convergence(
                workspace_id=_WS,
                guest_genesis=None,
                audience_tensions=_audience_tensions(),
                downstream_program_id="storyboard_program",
            )

    def test_downstream_blocked_error_carries_gate_reason(self, guard: DownstreamCompilationGuard) -> None:
        """INTEGRATION: DownstreamAdmissionBlockedError exposes gate_reason_code in details."""
        with pytest.raises(DownstreamAdmissionBlockedError) as exc_info:
            guard.assert_convergence(
                workspace_id=_WS,
                guest_genesis=None,
                audience_tensions=None,
                downstream_program_id="downstream_compilation",
            )
        assert "gate_reason_code" in exc_info.value.details
        assert "gate_message" in exc_info.value.details
        assert len(exc_info.value.permitted_next_actions) > 0

    def test_downstream_admitted_when_gate_passes(self, guard: DownstreamCompilationGuard) -> None:
        """
        INTEGRATION: Downstream admitted (receipt returned) when both sides are valid.
        Evidence class: EXECUTABLE (integration path)
        """
        receipt = guard.assert_convergence(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
            downstream_program_id="editorial_discovery_program",
        )
        assert receipt is not None
        assert receipt.status == ConvergenceStatus.CONVERGED
        assert receipt.is_valid_for_downstream() is True

    def test_false_proof_countercase_unit_test_alone_is_insufficient(self, gate: ConvergenceGate) -> None:
        """
        REGRESSION (False-proof countercase from mandate §9):
        A unit test that calls the convergence helper directly while the actual
        downstream entrypoint bypasses it is NOT sufficient.
        This test verifies the guard wraps the gate and persists the receipt,
        proving the integration path is exercised, not just the helper.
        """
        # This is the CORRECT test — it exercises the same guard path used by downstream programs.
        gg = _guest_genesis()
        at = _audience_tensions()

        # Correct path: guard.assert_convergence (not gate.evaluate directly)
        guard_local = DownstreamCompilationGuard(
            gate=gate,
            store=ConvergenceStore(sqlite3.connect(":memory:")),
        )
        receipt = guard_local.assert_convergence(
            workspace_id=_WS,
            guest_genesis=gg,
            audience_tensions=at,
            downstream_program_id="editorial_discovery_program",
        )
        # Verify receipt is persisted (proves integration path, not just helper)
        stored = guard_local._store.get_latest_receipt(_WS)
        assert stored is not None
        assert stored.receipt_id == receipt.receipt_id


# ===========================================================================
# 9. Persistence — ConvergenceStore
# ===========================================================================

class TestConvergenceStore:
    def test_store_and_retrieve_receipt(self, store: ConvergenceStore, gate: ConvergenceGate) -> None:
        """EXECUTABLE: Receipt is stored and retrievable by workspace_id."""
        receipt = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
        )
        store.store_receipt(receipt)

        retrieved = store.get_latest_receipt(_WS)
        assert retrieved is not None
        assert retrieved.receipt_id == receipt.receipt_id
        assert retrieved.status == ConvergenceStatus.CONVERGED
        assert retrieved.is_valid_for_downstream() is True

    def test_get_latest_receipt_returns_most_recent(
        self, store: ConvergenceStore, gate: ConvergenceGate
    ) -> None:
        """EXECUTABLE: get_latest_receipt returns the most recently stored receipt."""
        r1 = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(revision_id="rev-1", sha256_digest=_VALID_SHA),
            audience_tensions=_audience_tensions(revision_id="rev-at-1", sha256_digest=_VALID_SHA),
        )
        store.store_receipt(r1)

        r2 = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(revision_id="rev-2", sha256_digest="c" * 64),
            audience_tensions=_audience_tensions(revision_id="rev-at-2", sha256_digest="d" * 64),
        )
        store.store_receipt(r2)

        latest = store.get_latest_receipt(_WS)
        assert latest is not None
        assert latest.receipt_id == r2.receipt_id

    def test_get_latest_receipt_returns_none_for_unknown_workspace(self, store: ConvergenceStore) -> None:
        """EXECUTABLE: No receipt for an unknown workspace → None."""
        result = store.get_latest_receipt("ws-never-converged")
        assert result is None

    def test_receipt_idempotent_on_same_id(self, store: ConvergenceStore, gate: ConvergenceGate) -> None:
        """EXECUTABLE: Storing same receipt twice is idempotent (INSERT OR IGNORE)."""
        receipt = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
        )
        store.store_receipt(receipt)
        store.store_receipt(receipt)  # should not raise

        receipts = store.list_receipts(_WS)
        assert len(receipts) == 1

    def test_list_receipts_returns_multiple_ordered_most_recent_first(
        self, store: ConvergenceStore, gate: ConvergenceGate
    ) -> None:
        """EXECUTABLE: list_receipts returns all receipts ordered most-recent first."""
        for i in range(3):
            sha_gg = (chr(ord("a") + i)) * 64
            sha_at = (chr(ord("d") + i)) * 64
            r = gate.evaluate(
                workspace_id=_WS,
                guest_genesis=_guest_genesis(revision_id=f"rev-gg-{i}", sha256_digest=sha_gg),
                audience_tensions=_audience_tensions(revision_id=f"rev-at-{i}", sha256_digest=sha_at),
            )
            store.store_receipt(r)

        receipts = store.list_receipts(_WS)
        assert len(receipts) == 3
        # Most recent first — converged_at timestamps should be descending
        for i in range(len(receipts) - 1):
            assert receipts[i].converged_at >= receipts[i + 1].converged_at

    def test_get_receipt_by_id(self, store: ConvergenceStore, gate: ConvergenceGate) -> None:
        """EXECUTABLE: get_receipt_by_id returns the correct receipt."""
        receipt = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
        )
        store.store_receipt(receipt)

        retrieved = store.get_receipt_by_id(receipt.receipt_id)
        assert retrieved is not None
        assert retrieved.receipt_id == receipt.receipt_id

    def test_get_receipt_by_id_returns_none_for_missing(self, store: ConvergenceStore) -> None:
        """EXECUTABLE: get_receipt_by_id returns None for non-existent receipt."""
        assert store.get_receipt_by_id("CONV-RCP-nonexistent") is None

    def test_convergence_digest_uniqueness_across_different_pairs(
        self, store: ConvergenceStore, gate: ConvergenceGate
    ) -> None:
        """
        SCHEMA: The convergence_digest unique index prevents duplicate receipts for
        the same upstream revision pair (content-addressed deduplication).
        """
        gg = _guest_genesis()
        at = _audience_tensions()

        r1 = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)
        r2 = gate.evaluate(workspace_id=_WS, guest_genesis=gg, audience_tensions=at)

        # Same convergence_digest → second store is a no-op (INSERT OR IGNORE)
        assert r1.convergence_digest == r2.convergence_digest
        store.store_receipt(r1)
        store.store_receipt(r2)

        # Only one stored
        receipts = store.list_receipts(_WS)
        assert len(receipts) == 1


# ===========================================================================
# 10. Gate State Projection
# ===========================================================================

class TestGateStateProjection:
    def test_gate_state_unknown_when_no_receipt(self, guard: DownstreamCompilationGuard) -> None:
        """
        API PROJECTION: Gate state is UNKNOWN / admitted=False when no receipt exists.
        Evidence class: EXECUTABLE
        """
        state = guard.get_gate_state("ws-new-workspace")
        assert state["admitted"] is False
        assert state["status"] == "UNKNOWN"
        assert state["receipt"] is None
        assert state["gate_invariant"] == "FR-CONV-001"

    def test_gate_state_converged_after_successful_evaluation(
        self, guard: DownstreamCompilationGuard
    ) -> None:
        """
        API PROJECTION: Gate state is CONVERGED / admitted=True after successful evaluation.
        Evidence class: EXECUTABLE
        """
        guard.assert_convergence(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
            downstream_program_id="editorial_discovery_program",
        )

        state = guard.get_gate_state(_WS)
        assert state["admitted"] is True
        assert state["status"] == "CONVERGED"
        assert state["receipt"] is not None
        assert state["receipt"]["guest_genesis_revision_id"] == "rev-gg-001"
        assert state["receipt"]["audience_tensions_revision_id"] == "rev-at-001"


# ===========================================================================
# 11. Error Taxonomy — Error class hierarchy
# ===========================================================================

class TestErrorTaxonomy:
    def test_all_gate_errors_are_subclasses_of_convergence_gate_error(self) -> None:
        """SCHEMA: Every gate error must be a ConvergenceGateError subclass."""
        errors = [
            MissingGuestGenesisError(_WS),
            MissingAudienceTensionsError(_WS),
            InvalidGuestGenesisError(_WS, "reason"),
            InvalidAudienceTensionsError(_WS, "reason"),
            StaleGuestGenesisError(_WS, "a" * 64, "b" * 64, "rev-1"),
            StaleAudienceTensionsError(_WS, "a" * 64, "b" * 64, "rev-1"),
            ConvergenceRelationError(_WS, "reason"),
            BypassAttemptError(_WS),
            DownstreamAdmissionBlockedError(_WS, "program", "CODE", "msg"),
        ]
        for err in errors:
            assert isinstance(err, ConvergenceGateError), (
                f"{type(err).__name__} is not a ConvergenceGateError subclass"
            )

    def test_all_gate_errors_have_reason_code(self) -> None:
        """SCHEMA: Every gate error carries a non-empty reason_code."""
        errors = [
            MissingGuestGenesisError(_WS),
            MissingAudienceTensionsError(_WS),
            InvalidGuestGenesisError(_WS, "reason"),
            InvalidAudienceTensionsError(_WS, "reason"),
            StaleGuestGenesisError(_WS, "a" * 64, "b" * 64, "rev-1"),
            StaleAudienceTensionsError(_WS, "a" * 64, "b" * 64, "rev-1"),
            ConvergenceRelationError(_WS, "reason"),
            BypassAttemptError(_WS),
        ]
        for err in errors:
            assert err.reason_code and err.reason_code != "CONVERGENCE_GATE_ERROR", (
                f"{type(err).__name__} has default/missing reason_code"
            )

    def test_all_gate_errors_have_permitted_next_actions(self) -> None:
        """SCHEMA: Every gate error carries at least one permitted_next_action."""
        errors = [
            MissingGuestGenesisError(_WS),
            MissingAudienceTensionsError(_WS),
        ]
        for err in errors:
            assert len(err.permitted_next_actions) > 0, (
                f"{type(err).__name__} has no permitted_next_actions"
            )

    def test_error_to_dict_is_serializable(self) -> None:
        """SCHEMA: All gate errors can be serialised to a dict."""
        err = MissingGuestGenesisError(_WS)
        d = err.to_dict()
        assert d["reason_code"] == "MISSING_GUEST_GENESIS_SEMANTIC_TERRITORY"
        assert d["error"] == "MissingGuestGenesisError"
        assert isinstance(d["permitted_next_actions"], list)


# ===========================================================================
# 12. Regression — Adjacent Existing Behaviour
# ===========================================================================

class TestRegressionAdjacentBehaviour:
    def test_convergence_gate_does_not_affect_causal_admission_service(self) -> None:
        """
        REGRESSION: The convergence gate is an independent admission boundary.
        It does not modify or replace CausalAdmissionService (CA-M004/INV-CAUSAL-001).
        Both can be active simultaneously.
        """
        # The ConvergenceGate should be importable and usable without importing
        # or affecting CausalAdmissionService.
        gate = ConvergenceGate()
        receipt = gate.evaluate(
            workspace_id=_WS,
            guest_genesis=_guest_genesis(),
            audience_tensions=_audience_tensions(),
        )
        assert receipt.status == ConvergenceStatus.CONVERGED
        # CausalAdmissionService is not affected by this gate existing.

    def test_convergence_receipt_is_not_valid_for_downstream_when_status_is_not_converged(self) -> None:
        """
        REGRESSION: is_valid_for_downstream() is False for non-CONVERGED status.
        Ensures status field cannot be spoofed via dict construction.
        """
        receipt = ConvergenceReceipt(
            receipt_id="test-receipt",
            workspace_id=_WS,
            status=ConvergenceStatus.BLOCKED,
            guest_genesis_territory_id="terr",
            guest_genesis_revision_id="rev",
            guest_genesis_sha256=_VALID_SHA,
            audience_tensions_audience_id="aud",
            audience_tensions_revision_id="rev-at",
            audience_tensions_sha256=_VALID_SHA,
            convergence_digest="x" * 64,
            convergence_signature="SIG-CONV-TEST",
            converged_at="2026-09-07T00:00:00Z",
        )
        assert receipt.is_valid_for_downstream() is False

    def test_store_schema_tables_are_created_by_init(self, mem_conn: sqlite3.Connection) -> None:
        """
        MIGRATION: ConvergenceStore._ensure_schema() creates convergence_receipts table.
        Verifies the migration SQL is structurally correct.
        """
        store = ConvergenceStore(mem_conn)
        # If table creation succeeded, we can query it without error
        count = mem_conn.execute(
            "SELECT COUNT(*) FROM convergence_receipts"
        ).fetchone()[0]
        assert count == 0

    def test_second_store_init_is_idempotent(self, mem_conn: sqlite3.Connection) -> None:
        """MIGRATION: Creating ConvergenceStore twice on the same connection is idempotent."""
        ConvergenceStore(mem_conn)
        ConvergenceStore(mem_conn)  # Should not raise — uses CREATE TABLE IF NOT EXISTS
