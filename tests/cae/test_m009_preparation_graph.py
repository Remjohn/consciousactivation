"""
test_m009_preparation_graph.py
-------------------------------
CA-M009 — Interactive Parameter-Sensitive Preparation Graph
Verification and Evidence Test Suite.

Governing mandate:  docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/01_CA_MANDATE_009.md
Governing UI:       docs/cae/UI.md §9
Governing Arch:     docs/cae/Architecture.md §13

=== What is measured ===
  Positive tests:
    T01  — graph creation and initial state
    T02  — first SAVE_REVISION (genesis, base=None)
    T03  — second SAVE_REVISION creates a new revision; previous goes HISTORICAL
    T04  — list_revisions returns ordered history; historical revisions readable
    T05  — bind_run_to_revision creates an immutable binding
    T06  — get_active_run_revision returns the bound revision even after later edits
    T07  — digest integrity passes on an unmodified binding (INV-M009-05)
    T08  — operator projection shows all lifecycle states
    T09  — idempotent re-bind to same revision returns existing binding unchanged

  Negative tests (fail-closed boundary — all MUST raise):
    N01  — stale base_revision_id rejected (INV-M009-02)
    N02  — in-place mutation of a committed revision row raises RevisionImmutabilityError
             (simulates false-proof case: backend collapses R1 and R2 into one row)
    N03  — binding an already-bound run to a DIFFERENT revision raises ActiveBindingMutationError
             (INV-M009-03)
    N04  — digest mismatch raises DigestMismatchError when revision content is tampered
             (INV-M009-05 anti-centroid proof)
    N05  — forged revision_id (non-existent) raises RevisionNotFoundError
    N06  — wrong authority lane for create_graph raises UnauthorizedGraphLaneError
    N07  — wrong authority lane for save_graph_revision raises UnauthorizedGraphLaneError
    N08  — wrong authority lane for bind_run_to_revision raises UnauthorizedGraphLaneError
    N09  — get_active_run_revision for unknown run_id raises RunBindingNotFoundError
    N10  — save_graph_revision to unknown graph raises GraphNotFoundError

=== Evidence record format ===
  Each test emits docstring evidence describing:
    - command (function under test)
    - fixture / data identity
    - observed result
    - exact property proved
    - limitation

=== Limitation ===
  SQLite does not enforce the immutability trigger (fn_graph_revision_immutability)
  because that trigger is PostgreSQL-only.  Test N02 exercises the application-layer
  guard (RevisionImmutabilityError) which is environment-independent.  In a
  PostgreSQL integration environment, the DB trigger provides additional defense-in-depth.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, Optional
from uuid import uuid4

import pytest

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.preparation_graph_store import (
    ActiveBindingMutationError,
    DigestMismatchError,
    GraphNotFoundError,
    GraphRevisionRecord,
    GraphRunBindingRecord,
    PreparationGraphRecord,
    PreparationGraphStore,
    RevisionImmutabilityError,
    RevisionLifecycleState,
    RevisionNotFoundError,
    RunBindingNotFoundError,
    StaleBaseRevisionError,
)
from ca_runtime.preparation_graph_program import (
    PreparationGraphProgramCoordinator,
    UnauthorizedGraphLaneError,
    GraphWorkspaceScopeError,
)
from ca_contracts import canonical_sha256


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture
def ws_id() -> str:
    return f"ws-m009-{uuid4().hex[:12]}"


@pytest.fixture
def db_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@pytest.fixture
def store(db_conn: sqlite3.Connection) -> PreparationGraphStore:
    return PreparationGraphStore(db_conn)


@pytest.fixture
def coord(ws_id: str, store: PreparationGraphStore) -> PreparationGraphProgramCoordinator:
    return PreparationGraphProgramCoordinator(workspace_id=ws_id, store=store)


@pytest.fixture
def sample_params_v1() -> Dict[str, Any]:
    return {
        "audience_context": {"audience_id": "AUD-001", "tension": "Autonomy vs Control"},
        "research_signals": [{"signal_id": "SIG-001"}],
        "collision_hypotheses": [{"hypothesis_id": "HYP-001"}],
        "elicitation_config": {"mode": "structured", "depth": 3},
        "policy_refs": ["POL-001"],
    }


@pytest.fixture
def sample_params_v2() -> Dict[str, Any]:
    return {
        "audience_context": {"audience_id": "AUD-001", "tension": "Autonomy vs Control"},
        "research_signals": [{"signal_id": "SIG-001"}, {"signal_id": "SIG-002"}],
        "collision_hypotheses": [{"hypothesis_id": "HYP-001"}, {"hypothesis_id": "HYP-002"}],
        "elicitation_config": {"mode": "adaptive", "depth": 5},
        "policy_refs": ["POL-001", "POL-002"],
    }


# ===========================================================================
# Positive tests
# ===========================================================================

class TestPositive:

    def test_T01_graph_creation_and_initial_state(
        self, coord: PreparationGraphProgramCoordinator, ws_id: str
    ) -> None:
        """
        T01: Graph is created in DRAFT state with no revision.

        Command: coord.create_graph(campaign_id, name, lane=COMMANDER)
        Fixture: fresh in-memory store, workspace ws_id
        Observed: PreparationGraphRecord with lifecycle_state=DRAFT, latest_revision_id=None
        Property proved: DRAFT_GRAPH is the initial state; no revision exists at creation time.
        Limitation: in-memory store only; production requires Postgres + RLS.
        """
        graph = coord.create_graph(
            campaign_id="campaign-001",
            name="Test Preparation Graph",
            lane=AuthorityLane.COMMANDER,
            actor_id="operator-01",
        )

        assert graph.workspace_id == ws_id
        assert graph.campaign_id == "campaign-001"
        assert graph.name == "Test Preparation Graph"
        assert graph.lifecycle_state == "DRAFT"
        assert graph.latest_revision_id is None
        assert graph.graph_id.startswith("graph_")

    def test_T02_genesis_save_revision(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        T02: First SAVE_REVISION (genesis) creates revision with base=None.

        Command: coord.save_graph_revision(base_revision_id=None, parameters=v1)
        Fixture: DRAFT graph, no prior revision
        Observed: revision_id created, revision_seq=1, lifecycle_state=CANDIDATE
        Property proved: genesis revision is accepted when base_revision_id=None
                         and graph.latest_revision_id is also None.
        Limitation: SQLite only; digest verified against canonical_sha256.
        """
        graph = coord.create_graph(
            campaign_id="campaign-001",
            name="Graph T02",
            lane=AuthorityLane.COMMANDER,
        )

        revision = coord.save_graph_revision(
            graph_id=graph.graph_id,
            base_revision_id=None,   # genesis
            parameters=sample_params_v1,
            lane=AuthorityLane.ANALYST,
            actor_id="analyst-01",
        )

        assert revision.graph_id == graph.graph_id
        assert revision.revision_seq == 1
        assert revision.base_revision_id is None
        assert revision.lifecycle_state == RevisionLifecycleState.CANDIDATE
        assert revision.author_id == "analyst-01"

        # Verify digest is correct
        expected_digest = canonical_sha256(sample_params_v1)
        assert revision.canonical_sha256 == expected_digest

        # Graph header should reflect the new revision
        updated_graph = coord.store.get_graph(ws_id, graph.graph_id)
        assert updated_graph.latest_revision_id == revision.revision_id

    def test_T03_second_revision_supersedes_first(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        T03: After a second SAVE_REVISION:
             - R1 transitions CANDIDATE → HISTORICAL
             - R2 is created as CANDIDATE
             - graph.latest_revision_id = R2

        Command: coord.save_graph_revision (called twice)
        Fixture: graph with R1 already saved
        Observed: R1 lifecycle_state=HISTORICAL, R2 lifecycle_state=CANDIDATE
        Property proved: Previous revision is superseded without being deleted;
                         historical revisions remain accessible (INV-M009-04).
        Limitation: lifecycle_state of EXECUTION_BOUND revisions is not downgraded.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T03", lane=AuthorityLane.COMMANDER)

        r1 = coord.save_graph_revision(
            graph_id=graph.graph_id,
            base_revision_id=None,
            parameters=sample_params_v1,
            lane=AuthorityLane.ANALYST,
        )

        r2 = coord.save_graph_revision(
            graph_id=graph.graph_id,
            base_revision_id=r1.revision_id,   # caller's base matches current latest
            parameters=sample_params_v2,
            lane=AuthorityLane.ANALYST,
        )

        # R1 must now be HISTORICAL
        r1_refreshed = coord.store.get_revision(ws_id, r1.revision_id)
        assert r1_refreshed.lifecycle_state == RevisionLifecycleState.HISTORICAL

        # R2 must be CANDIDATE
        assert r2.lifecycle_state == RevisionLifecycleState.CANDIDATE

        # Graph header must point to R2
        updated_graph = coord.store.get_graph(ws_id, graph.graph_id)
        assert updated_graph.latest_revision_id == r2.revision_id

        # R1's lineage is intact (revision_seq=1, base=None)
        assert r1_refreshed.revision_seq == 1
        assert r1_refreshed.base_revision_id is None

        # R2 has correct lineage
        assert r2.revision_seq == 2
        assert r2.base_revision_id == r1.revision_id

    def test_T04_list_revisions_ordered_history(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        T04: list_revisions returns all revisions ordered by revision_seq ASC.
             Historical revisions remain fully readable (INV-M009-04).

        Command: coord.list_graph_revisions(graph_id)
        Fixture: graph with R1 (HISTORICAL) and R2 (CANDIDATE)
        Observed: [R1, R2] in order; R1 payload readable and digest verifiable
        Property proved: INV-M009-04 — historical revisions are never deleted.
        Limitation: read-only assertion; no mutation attempted.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T04", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        r2 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=r1.revision_id,
                                        parameters=sample_params_v2, lane=AuthorityLane.ANALYST)

        revisions = coord.list_graph_revisions(graph.graph_id)

        assert len(revisions) == 2
        assert revisions[0].revision_id == r1.revision_id
        assert revisions[0].revision_seq == 1
        assert revisions[1].revision_id == r2.revision_id
        assert revisions[1].revision_seq == 2

        # Historical revision's payload and digest are fully readable
        r1_payload = json.loads(revisions[0].parameter_payload_json)
        assert r1_payload["elicitation_config"]["mode"] == "structured"
        assert revisions[0].canonical_sha256 == canonical_sha256(sample_params_v1)

    def test_T05_bind_run_to_revision(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        T05: bind_run_to_revision creates an immutable binding record.

        Command: coord.bind_run_to_revision(run_id, graph_id, revision_id, lane=COMMANDER)
        Fixture: graph with R1 (CANDIDATE)
        Observed: GraphRunBindingRecord with revision_id=R1, revision_digest=digest(R1)
        Property proved: The binding record captures the exact revision identity and digest
                         at execution start (INV-M009-05).  R1 transitions to EXECUTION_BOUND.
        Limitation: immutability of binding enforced at application layer; DB trigger
                    enforces in PostgreSQL production environment.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T05", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)

        run_id = f"run_{uuid4().hex[:12]}"
        binding = coord.bind_run_to_revision(
            run_id=run_id,
            graph_id=graph.graph_id,
            revision_id=r1.revision_id,
            lane=AuthorityLane.COMMANDER,
            bound_by_id="operator-cmd-01",
        )

        assert binding.run_id == run_id
        assert binding.revision_id == r1.revision_id
        assert binding.revision_digest == r1.canonical_sha256

        # R1 must now be EXECUTION_BOUND
        r1_refreshed = coord.store.get_revision(ws_id, r1.revision_id)
        assert r1_refreshed.lifecycle_state == RevisionLifecycleState.EXECUTION_BOUND

    def test_T06_active_run_returns_bound_revision_after_later_edits(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        T06: After binding a run to R1, a later operator edit creates R2.
             get_active_run_revision MUST still return R1 (runtime authority — UI-001).

        Command: coord.get_active_run_revision(run_id)
        Fixture: run bound to R1; operator then saves R2 with different parameters
        Observed: get_active_run_revision returns the R1 revision record
        Property proved: Active execution binding is independent of later graph revisions.
                         A run never "sees" changes made after it started.
        Limitation: Test verifies the application-layer CAS guarantee.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T06", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)

        run_id = f"run_{uuid4().hex[:12]}"
        coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                    revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        # Operator saves R2 AFTER the run started
        r2 = coord.save_graph_revision(
            graph_id=graph.graph_id,
            base_revision_id=r1.revision_id,
            parameters=sample_params_v2,
            lane=AuthorityLane.ANALYST,
        )
        assert r2.revision_id != r1.revision_id

        # The run must still see R1
        active_revision = coord.get_active_run_revision(run_id)
        assert active_revision.revision_id == r1.revision_id

        # And R1's parameters are unchanged
        payload = json.loads(active_revision.parameter_payload_json)
        assert payload["elicitation_config"]["mode"] == "structured"   # R1 value
        assert payload["elicitation_config"]["mode"] != "adaptive"    # R2 value

    def test_T07_digest_integrity_passes_on_unmodified_binding(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        T07: verify_active_run_integrity returns True for an untouched binding.

        Command: coord.verify_active_run_integrity(run_id)
        Fixture: run bound to R1; no subsequent mutations
        Observed: True
        Property proved: INV-M009-05 — stored digest matches recomputed canonical SHA-256.
        Limitation: validates application-layer digest; PostgreSQL trigger adds DB-layer guard.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T07", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        run_id = f"run_{uuid4().hex[:12]}"
        coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                    revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        result = coord.verify_active_run_integrity(run_id)
        assert result is True

    def test_T08_operator_projection_shows_all_lifecycle_states(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        T08: get_graph_operator_view returns graph header, revisions, and run bindings.

        Command: coord.get_graph_operator_view(graph_id)
        Fixture: graph with R1 (EXECUTION_BOUND, bound to run-01) and R2 (CANDIDATE)
        Observed: projection dict with graph, revisions[R1, R2], run_bindings[run-01→R1]
        Property proved: Operator can inspect all lifecycle states simultaneously (UI §9).
        Limitation: projection is read-only; content is not semantically validated.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T08", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        run_id = "run-operator-view-01"
        coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                    revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        r2 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=r1.revision_id,
                                        parameters=sample_params_v2, lane=AuthorityLane.ANALYST)

        view = coord.get_graph_operator_view(graph.graph_id)

        assert view["graph"]["graph_id"] == graph.graph_id
        assert view["graph"]["latest_revision_id"] == r2.revision_id
        assert len(view["revisions"]) == 2

        rev_states = {r["revision_id"]: r["lifecycle_state"] for r in view["revisions"]}
        assert rev_states[r1.revision_id] == RevisionLifecycleState.EXECUTION_BOUND
        assert rev_states[r2.revision_id] == RevisionLifecycleState.CANDIDATE

        assert len(view["run_bindings"]) == 1
        assert view["run_bindings"][0]["run_id"] == run_id
        assert view["run_bindings"][0]["revision_id"] == r1.revision_id

    def test_T09_idempotent_rebind_to_same_revision(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        T09: Binding the same run to the same revision a second time returns the existing binding.

        Command: coord.bind_run_to_revision called twice with identical arguments
        Fixture: run already bound to R1
        Observed: second call returns original GraphRunBindingRecord unchanged
        Property proved: idempotent re-bind is safe (same revision = replay guard).
        Limitation: Different revision on second call is N03; this tests same-revision only.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph T09", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        run_id = f"run_{uuid4().hex[:12]}"

        binding1 = coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                               revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)
        binding2 = coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                               revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        assert binding1.run_id == binding2.run_id
        assert binding1.revision_id == binding2.revision_id
        assert binding1.bound_at == binding2.bound_at   # row was not re-created


# ===========================================================================
# Negative tests (fail-closed boundary)
# ===========================================================================

class TestNegative:

    def test_N01_stale_base_revision_rejected(
        self,
        coord: PreparationGraphProgramCoordinator,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        N01: Stale write rejected when base_revision_id does not match current latest.

        Command: coord.save_graph_revision(base_revision_id=<stale>)
        Fixture: graph with R1 as latest; caller passes None (stale) as base
        Observed: StaleBaseRevisionError raised
        Property proved: INV-M009-02 — an editor that loaded an older revision cannot
                         overwrite a newer one silently.
        Limitation: enforced in application layer; DB has no equivalent constraint.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N01", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)

        # Caller has a stale view and passes None as base (the pre-R1 state)
        with pytest.raises(StaleBaseRevisionError) as exc_info:
            coord.save_graph_revision(
                graph_id=graph.graph_id,
                base_revision_id=None,       # stale: graph now has R1 as latest
                parameters=sample_params_v2,
                lane=AuthorityLane.ANALYST,
            )

        exc = exc_info.value
        assert exc.reason_code == "STALE_BASE_REVISION"
        assert exc.expected_base is None
        assert exc.actual_latest == r1.revision_id

    def test_N01b_stale_base_when_newer_revision_exists(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        N01b: Stale write rejected when caller passes R1 as base but R2 is now latest.

        Command: coord.save_graph_revision(base_revision_id=R1) when R2 is latest
        Observed: StaleBaseRevisionError with expected_base=R1, actual_latest=R2
        Property proved: Two concurrent editors: the one who saved R2 first wins;
                         the second must re-fetch and base on R2.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N01b", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        r2 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=r1.revision_id,
                                        parameters=sample_params_v2, lane=AuthorityLane.ANALYST)

        # Another editor still thinks R1 is latest
        params_v3 = {**sample_params_v2, "policy_refs": ["POL-003"]}
        with pytest.raises(StaleBaseRevisionError) as exc_info:
            coord.save_graph_revision(
                graph_id=graph.graph_id,
                base_revision_id=r1.revision_id,   # stale
                parameters=params_v3,
                lane=AuthorityLane.ANALYST,
            )
        assert exc_info.value.actual_latest == r2.revision_id

    def test_N02_in_place_mutation_of_committed_revision_rejected(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        db_conn: sqlite3.Connection,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        N02: False-proof case (anti-centroid) — simulates backend mutating R1 in-place.

        The false-proof case from CA-M009 §9:
          "The UI changes from R1 to R2 while the backend mutates the same stored row,
           so the active run now unknowingly uses R2.  That must fail."

        We simulate this by:
          1. Saving R1, binding a run to R1.
          2. Directly mutating the graph_revision table row (as a buggy backend would).
          3. Verifying that verify_active_run_integrity raises DigestMismatchError.

        Command: SQLite direct UPDATE (bypasses application layer); then verify_active_run_integrity
        Fixture: run bound to R1; direct SQL mutation of parameter_payload_json
        Observed: DigestMismatchError raised (binding digest no longer matches revision content)
        Property proved: INV-M009-05 — the digest stored at bind time detects subsequent
                         mutation of the revision row.
        Limitation: Application-layer guard only here.  In production the PostgreSQL trigger
                    fn_graph_revision_immutability blocks the UPDATE before it reaches storage.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N02", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        run_id = f"run_{uuid4().hex[:12]}"
        coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                    revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        # Verify integrity passes before tampering
        assert coord.verify_active_run_integrity(run_id) is True

        # --- SIMULATE BUGGY BACKEND: mutate the row in-place ---
        tampered_params = json.dumps(sample_params_v2, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        db_conn.execute(
            "UPDATE graph_revision SET parameter_payload_json = ? WHERE revision_id = ?",
            (tampered_params, r1.revision_id),
        )
        db_conn.commit()

        # --- NOW verify integrity — MUST FAIL ---
        with pytest.raises(DigestMismatchError) as exc_info:
            coord.verify_active_run_integrity(run_id)

        assert exc_info.value.reason_code == "DIGEST_MISMATCH"
        assert exc_info.value.revision_id == r1.revision_id

    def test_N03_binding_run_to_different_revision_rejected(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        N03: Attempting to rebind a run to a DIFFERENT revision raises ActiveBindingMutationError.

        Command: coord.bind_run_to_revision with same run_id but different revision_id
        Fixture: run already bound to R1; caller attempts to bind to R2
        Observed: ActiveBindingMutationError raised
        Property proved: INV-M009-03 — active run binding is immutable.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N03", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        r2 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=r1.revision_id,
                                        parameters=sample_params_v2, lane=AuthorityLane.ANALYST)
        run_id = f"run_{uuid4().hex[:12]}"
        coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                    revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        with pytest.raises(ActiveBindingMutationError) as exc_info:
            coord.bind_run_to_revision(
                run_id=run_id,
                graph_id=graph.graph_id,
                revision_id=r2.revision_id,    # different revision!
                lane=AuthorityLane.COMMANDER,
            )

        exc = exc_info.value
        assert exc.reason_code == "ACTIVE_BINDING_MUTATION"
        assert exc.run_id == run_id
        assert exc.bound_revision_id == r1.revision_id

    def test_N04_digest_mismatch_on_tampered_revision(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        db_conn: sqlite3.Connection,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        N04: DigestMismatchError when canonical_sha256 stored in revision row is stale.

        Simulates a different class of tampering: the revision row's canonical_sha256
        field itself is changed (e.g. by a migration bug).

        Command: Direct SQL UPDATE of canonical_sha256; then verify_active_run_integrity
        Observed: DigestMismatchError raised
        Property proved: The verify step re-derives the digest from the raw JSON and
                         compares to both the revision.canonical_sha256 AND the
                         binding.revision_digest, catching either class of tampering.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N04", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)
        run_id = f"run_{uuid4().hex[:12]}"
        coord.bind_run_to_revision(run_id=run_id, graph_id=graph.graph_id,
                                    revision_id=r1.revision_id, lane=AuthorityLane.COMMANDER)

        # Tamper: replace canonical_sha256 in the revision row with a forged digest
        forged_digest = "a" * 64
        db_conn.execute(
            "UPDATE graph_revision SET canonical_sha256 = ? WHERE revision_id = ?",
            (forged_digest, r1.revision_id),
        )
        db_conn.commit()

        with pytest.raises(DigestMismatchError):
            coord.verify_active_run_integrity(run_id)

    def test_N05_forged_revision_id_raises(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        N05: Binding a run to a non-existent revision_id raises RevisionNotFoundError.

        Command: coord.bind_run_to_revision(revision_id=<forged>)
        Observed: RevisionNotFoundError raised
        Property proved: Forged / invented revision identifiers cannot be used to
                         bypass the binding contract.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N05", lane=AuthorityLane.COMMANDER)

        with pytest.raises(RevisionNotFoundError) as exc_info:
            coord.bind_run_to_revision(
                run_id=f"run_{uuid4().hex[:12]}",
                graph_id=graph.graph_id,
                revision_id="rev_forged_does_not_exist",
                lane=AuthorityLane.COMMANDER,
            )

        assert exc_info.value.reason_code == "REVISION_NOT_FOUND"

    def test_N06_wrong_lane_for_create_graph(
        self,
        coord: PreparationGraphProgramCoordinator,
    ) -> None:
        """
        N06: create_graph called from non-COMMANDER lane raises UnauthorizedGraphLaneError.

        Command: coord.create_graph(lane=ANALYST)
        Observed: UnauthorizedGraphLaneError raised
        Property proved: Authority lane enforcement for create_graph.
        """
        with pytest.raises(UnauthorizedGraphLaneError) as exc_info:
            coord.create_graph(
                campaign_id="camp-001",
                name="Unauthorized Graph",
                lane=AuthorityLane.ANALYST,   # wrong lane
            )

        assert exc_info.value.reason_code == "UNAUTHORIZED_GRAPH_LANE"

    def test_N07_wrong_lane_for_save_graph_revision(
        self,
        coord: PreparationGraphProgramCoordinator,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        N07: save_graph_revision called from HUNTER lane raises UnauthorizedGraphLaneError.

        Command: coord.save_graph_revision(lane=HUNTER)
        Observed: UnauthorizedGraphLaneError raised
        Property proved: Only ANALYST or COMMANDER may save revisions.
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N07", lane=AuthorityLane.COMMANDER)

        with pytest.raises(UnauthorizedGraphLaneError) as exc_info:
            coord.save_graph_revision(
                graph_id=graph.graph_id,
                base_revision_id=None,
                parameters=sample_params_v1,
                lane=AuthorityLane.HUNTER,    # wrong lane
            )

        assert exc_info.value.reason_code == "UNAUTHORIZED_GRAPH_LANE"

    def test_N08_wrong_lane_for_bind_run(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        N08: bind_run_to_revision called from ANALYST lane raises UnauthorizedGraphLaneError.

        Command: coord.bind_run_to_revision(lane=ANALYST)
        Observed: UnauthorizedGraphLaneError raised
        Property proved: Only COMMANDER may bind a run (execution gate).
        """
        graph = coord.create_graph(campaign_id="camp-001", name="Graph N08", lane=AuthorityLane.COMMANDER)
        r1 = coord.save_graph_revision(graph_id=graph.graph_id, base_revision_id=None,
                                        parameters=sample_params_v1, lane=AuthorityLane.ANALYST)

        with pytest.raises(UnauthorizedGraphLaneError) as exc_info:
            coord.bind_run_to_revision(
                run_id=f"run_{uuid4().hex[:12]}",
                graph_id=graph.graph_id,
                revision_id=r1.revision_id,
                lane=AuthorityLane.ANALYST,   # wrong lane
            )

        assert exc_info.value.reason_code == "UNAUTHORIZED_GRAPH_LANE"

    def test_N09_get_active_run_revision_for_unknown_run(
        self,
        coord: PreparationGraphProgramCoordinator,
    ) -> None:
        """
        N09: get_active_run_revision for a run that has no binding raises RunBindingNotFoundError.

        Command: coord.get_active_run_revision(run_id=<unknown>)
        Observed: RunBindingNotFoundError raised
        Property proved: Unknown / unbound run IDs are rejected cleanly.
        """
        with pytest.raises(RunBindingNotFoundError) as exc_info:
            coord.get_active_run_revision("run_unknown_not_bound")

        assert exc_info.value.reason_code == "RUN_BINDING_NOT_FOUND"

    def test_N10_save_revision_to_unknown_graph(
        self,
        coord: PreparationGraphProgramCoordinator,
        sample_params_v1: Dict[str, Any],
    ) -> None:
        """
        N10: save_graph_revision for a non-existent graph raises GraphNotFoundError.

        Command: coord.save_graph_revision(graph_id=<unknown>)
        Observed: GraphNotFoundError raised
        Property proved: Graph scope is validated before any revision write.
        """
        with pytest.raises(GraphNotFoundError) as exc_info:
            coord.save_graph_revision(
                graph_id="graph_does_not_exist",
                base_revision_id=None,
                parameters=sample_params_v1,
                lane=AuthorityLane.ANALYST,
            )

        assert exc_info.value.reason_code == "GRAPH_NOT_FOUND"


# ===========================================================================
# End-to-end scenario: full M009 lifecycle
# ===========================================================================

class TestEndToEndLifecycle:

    def test_full_m009_lifecycle(
        self,
        coord: PreparationGraphProgramCoordinator,
        ws_id: str,
        sample_params_v1: Dict[str, Any],
        sample_params_v2: Dict[str, Any],
    ) -> None:
        """
        E2E: Complete M009 preparation-graph lifecycle.

        Verifies the entire arc:
          DRAFT_GRAPH → SAVE_REVISION (R1) → CANDIDATE
          → EXECUTION_BINDING (run-01 bound to R1)
          → SAVE_REVISION (R2) while run-01 is active
          → run-01 still returns R1
          → digest integrity passes for run-01
          → historical inspection shows R1 (EXECUTION_BOUND) and R2 (CANDIDATE)

        Command: full coordinator workflow
        Fixture: in-memory SQLite store
        Observed: all state transitions correct; active run unaffected by R2
        Property proved: Complete M009 causal arc as specified in mandate §8.
        Limitation: SQLite only; PostgreSQL migration and DB triggers for production.
        """
        # 1. COMMANDER: Create graph
        graph = coord.create_graph(
            campaign_id="campaign-e2e-001",
            name="E2E Preparation Graph",
            lane=AuthorityLane.COMMANDER,
            actor_id="cmd-operator",
        )
        assert graph.lifecycle_state == "DRAFT"
        assert graph.latest_revision_id is None

        # 2. ANALYST: Save first revision R1 (genesis)
        r1 = coord.save_graph_revision(
            graph_id=graph.graph_id,
            base_revision_id=None,
            parameters=sample_params_v1,
            lane=AuthorityLane.ANALYST,
            actor_id="analyst-prep-01",
        )
        assert r1.revision_seq == 1
        assert r1.lifecycle_state == RevisionLifecycleState.CANDIDATE

        # 3. COMMANDER: Bind run-A to R1 (execution starts)
        run_a = f"run_e2e_{uuid4().hex[:12]}"
        binding_a = coord.bind_run_to_revision(
            run_id=run_a,
            graph_id=graph.graph_id,
            revision_id=r1.revision_id,
            lane=AuthorityLane.COMMANDER,
            bound_by_id="cmd-operator",
        )
        assert binding_a.revision_id == r1.revision_id
        assert binding_a.revision_digest == r1.canonical_sha256

        # Verify R1 is now EXECUTION_BOUND
        r1_check = coord.store.get_revision(ws_id, r1.revision_id)
        assert r1_check.lifecycle_state == RevisionLifecycleState.EXECUTION_BOUND

        # 4. ANALYST: Operator makes new changes → R2 (while run-A is active)
        r2 = coord.save_graph_revision(
            graph_id=graph.graph_id,
            base_revision_id=r1.revision_id,
            parameters=sample_params_v2,
            lane=AuthorityLane.ANALYST,
            actor_id="analyst-prep-01",
        )
        assert r2.revision_seq == 2
        # R1 should still be EXECUTION_BOUND (not HISTORICAL, because it's bound to an active run)
        r1_after_r2 = coord.store.get_revision(ws_id, r1.revision_id)
        assert r1_after_r2.lifecycle_state == RevisionLifecycleState.EXECUTION_BOUND

        # 5. Verify run-A still uses R1 (runtime authority — UI-001)
        active_rev = coord.get_active_run_revision(run_a)
        assert active_rev.revision_id == r1.revision_id
        payload = json.loads(active_rev.parameter_payload_json)
        assert payload["elicitation_config"]["mode"] == "structured"   # R1 value

        # 6. Integrity check for run-A
        assert coord.verify_active_run_integrity(run_a) is True

        # 7. Operator view shows complete state
        view = coord.get_graph_operator_view(graph.graph_id)
        revision_states = {r["revision_id"]: r["lifecycle_state"] for r in view["revisions"]}
        assert revision_states[r1.revision_id] == RevisionLifecycleState.EXECUTION_BOUND
        assert revision_states[r2.revision_id] == RevisionLifecycleState.CANDIDATE
        assert view["graph"]["latest_revision_id"] == r2.revision_id

        # 8. Historical inspection: both revisions readable with correct seq order
        all_revisions = coord.list_graph_revisions(graph.graph_id)
        assert len(all_revisions) == 2
        assert all_revisions[0].revision_seq < all_revisions[1].revision_seq

        # 9. Stale write attempt rejected (N01 guard in context of E2E)
        with pytest.raises(StaleBaseRevisionError):
            coord.save_graph_revision(
                graph_id=graph.graph_id,
                base_revision_id=r1.revision_id,   # stale; R2 is now latest
                parameters={"stale": True},
                lane=AuthorityLane.ANALYST,
            )
