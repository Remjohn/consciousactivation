"""Comprehensive Test Suite for CAE Mandate M68: State + Observability + Persistence Convergence.

Governed by:
- 04_STATE_OBSERVABILITY_CONVERGENCE/M68_state_observability_persistence_convergence.md
- docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/05_CLAIM_CEILING.md

Verifies:
- Gate 1: Durable Program Run Creation and Immediate Aggregate Verification in SQLite.
- Gate 2: Authoritative State Transitions & Monotonic Version/Receipt Progression.
- Gate 3: StateM State-Entry Context Refresh at State Boundaries.
- Gate 4 (Checked Transfer Rule): Failed Transitions Leave Aggregate Strictly in Source State.
- Gate 5: Unified Observability Projects Pure Operational Truth from Persistent Store.
- Gate 6: Process Restart & Re-Read from Persistent SQLite Database.
- Gate 7 (Countertest): Stale-Context Reuse Detected and Blocked.
- Gate 8 (Countertest): Cross-Tenant State and Replay Queries Fail Closed.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentCapabilityGrant,
    AgentDefinition,
    AgentInvocationCompiler,
    AgentInvocationRuntime,
    AgentLifecycleState,
    AgentModelPolicy,
    AgentOutputContract,
    AgentPromptReference,
    AgentRegistry,
    AuthorityLane,
    CapabilityProjection,
    CapabilityScope,
    ContextItem,
    ContextPrecedenceLayer,
    ExecutionMode,
    HierarchicalContextResolver,
    JITContextCapsule,
    JITContextCompiler,
    ObservabilityTenantIsolationError,
    ProgramAuthorityLaneViolationError,
    ProgramOperatorRuntimeService,
    ProgramRegistry,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateLocalContext,
    ProgramStateRuntimeError,
    ProgramStateTransition,
    ProgramTransitionBlockedError,
    ReadOnlyObservabilityViewer,
    SkillMaturity,
    SkillPackageRef,
    SqliteProgramStateStore,
    UnifiedFactoryCommandEngine,
    UniversalProgramStateRuntime,
    get_canonical_research_canonicalization_state_machine,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def temp_db_path():
    tmp_dir = tempfile.mkdtemp(prefix="m68_state_test_")
    db_file = os.path.join(tmp_dir, "m68_program_state.db")
    yield db_file
    try:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    except Exception:
        pass


@pytest.fixture
def persistent_sqlite_store(temp_db_path: str) -> SqliteProgramStateStore:
    return SqliteProgramStateStore(temp_db_path)


@pytest.fixture
def persistent_runtime(persistent_sqlite_store: SqliteProgramStateStore) -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime(store=persistent_sqlite_store)


@pytest.fixture
def persistent_operator(persistent_runtime: UniversalProgramStateRuntime) -> ProgramOperatorRuntimeService:
    return ProgramOperatorRuntimeService(runtime=persistent_runtime)


@pytest.fixture
def command_engine(persistent_operator: ProgramOperatorRuntimeService) -> UnifiedFactoryCommandEngine:
    return UnifiedFactoryCommandEngine(program_operator=persistent_operator)


# ===========================================================================
# Gate 1: Durable Program Run Creation and Immediate Aggregate Verification
# ===========================================================================

def test_m68_run_creation_persists_aggregate_in_sqlite(
    command_engine: UnifiedFactoryCommandEngine,
    persistent_sqlite_store: SqliteProgramStateStore,
) -> None:
    """Gate 1: Creating a program run persists a real aggregate in SQLite store."""
    res = command_engine.execute_command_text("run program research_canonicalization_program")
    assert res.success
    aggregate_id = res.data["aggregate_id"]

    # Verify directly from SQLite store
    stored_agg = persistent_sqlite_store.get_aggregate(aggregate_id)
    assert stored_agg is not None
    assert stored_agg.aggregate_id == aggregate_id
    assert stored_agg.program_id == "research_canonicalization_program"
    assert stored_agg.lifecycle == ProgramStateLifecycle.RUNNING
    assert stored_agg.version == 2  # v1 (init) -> v2 (running)
    assert len(stored_agg.state_hash) == 64
    assert stored_agg.last_receipt_id != ""


# ===========================================================================
# Gate 2: Authoritative State Transitions & Monotonic Version/Receipt Progression
# ===========================================================================

def test_m68_state_transitions_maintain_monotonic_version_and_receipt_lineage(
    persistent_runtime: UniversalProgramStateRuntime,
    persistent_operator: ProgramOperatorRuntimeService,
    persistent_sqlite_store: SqliteProgramStateStore,
) -> None:
    """Gate 2: Sequential transitions update state, increment versions monotonically, and log receipts in SQLite."""
    # 1. Run program
    agg = persistent_operator.run_program(
        program_id="research_canonicalization_program",
        workspace_id="test_ws_m68",
        actor_id="operator:commander",
    )
    agg_id = agg.aggregate_id
    assert agg.current_state == "INITIAL"
    assert agg.version == 2

    # 2. Transition: attach_sources (COMMANDER lane)
    res_1 = persistent_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="operator:commander",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "sources_verified"],
        state_updates={"sources": ["src_001", "src_002"]},
    )
    assert res_1.aggregate.current_state == "SOURCES_ATTACHED"
    assert res_1.aggregate.version == 3
    assert res_1.transition.from_state == "INITIAL"
    assert res_1.transition.to_state == "SOURCES_ATTACHED"
    assert res_1.transition.lane == AuthorityLane.COMMANDER
    assert res_1.transition.receipt_id != ""

    # 3. Transition: extract_candidates (HUNTER lane)
    res_2 = persistent_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="extract_candidates",
        actor_id="agent:hunter",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "sources_attached"],
        state_updates={"candidates": ["cand_101", "cand_102"]},
    )
    assert res_2.aggregate.current_state == "CANDIDATES_EXTRACTED"
    assert res_2.aggregate.version == 4
    assert res_2.transition.from_state == "SOURCES_ATTACHED"
    assert res_2.transition.to_state == "CANDIDATES_EXTRACTED"

    # 4. Verify transitions persisted in SQLite store
    transitions = persistent_sqlite_store.list_transitions(agg_id)
    assert len(transitions) == 2
    assert transitions[0].transition_name == "attach_sources"
    assert transitions[0].committed_version == 3
    assert transitions[1].transition_name == "extract_candidates"
    assert transitions[1].committed_version == 4


# ===========================================================================
# Gate 3: StateM State-Entry Context Refresh at State Boundaries
# ===========================================================================

def test_m68_statem_context_refresh_at_boundaries(
    persistent_runtime: UniversalProgramStateRuntime,
    persistent_operator: ProgramOperatorRuntimeService,
) -> None:
    """Gate 3: State-entry context is dynamically computed and bound to current state and hash."""
    agg = persistent_operator.run_program(
        program_id="research_canonicalization_program",
        workspace_id="test_ws_m68_ctx",
        actor_id="operator:commander",
    )
    agg_id = agg.aggregate_id

    # 1. Check local context at INITIAL state
    ctx_init = persistent_runtime.get_local_context(agg_id, active_lane=AuthorityLane.COMMANDER)
    assert isinstance(ctx_init, ProgramStateLocalContext)
    assert ctx_init.aggregate.current_state == "INITIAL"
    assert "attach_sources" in ctx_init.allowable_transitions
    assert "extract_candidates" not in ctx_init.allowable_transitions

    # 2. Advance to SOURCES_ATTACHED
    persistent_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="operator:commander",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "sources_verified"],
    )

    # 3. Check local context at SOURCES_ATTACHED state
    ctx_sources = persistent_runtime.get_local_context(agg_id, active_lane=AuthorityLane.HUNTER)
    assert ctx_sources.aggregate.current_state == "SOURCES_ATTACHED"
    assert "extract_candidates" in ctx_sources.allowable_transitions
    assert "attach_sources" not in ctx_sources.allowable_transitions
    assert ctx_sources.aggregate.state_hash != ctx_init.aggregate.state_hash


# ===========================================================================
# Gate 4: Checked Transfer Rule (Failed Transition Leaves Source State Unchanged)
# ===========================================================================

def test_m68_checked_transfer_failed_transition_retains_source_state(
    persistent_runtime: UniversalProgramStateRuntime,
    persistent_operator: ProgramOperatorRuntimeService,
    persistent_sqlite_store: SqliteProgramStateStore,
) -> None:
    """Gate 4: Failed transitions leave the aggregate strictly in its source state."""
    agg = persistent_operator.run_program(
        program_id="research_canonicalization_program",
        workspace_id="test_ws_m68_checked",
        actor_id="operator:commander",
    )
    agg_id = agg.aggregate_id

    # 1. Advance to SOURCES_ATTACHED
    persistent_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="operator:commander",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "sources_verified"],
    )

    agg_before = persistent_sqlite_store.get_aggregate(agg_id)
    assert agg_before is not None
    assert agg_before.current_state == "SOURCES_ATTACHED"
    assert agg_before.version == 3
    hash_before = agg_before.state_hash

    # 2. Attempt illegal transition: skipping directly to project_okf_bundle
    with pytest.raises(ProgramTransitionBlockedError) as exc_info:
        persistent_runtime.execute_transition(
            aggregate_id=agg_id,
            transition_name="project_okf_bundle",
            actor_id="agent:composer",
            actor_lane=AuthorityLane.COMPOSER,
            context_claims=["workspace_active", "canonical_nodes_resolved"],
        )
    assert "Contract requires source state 'CANONICALIZED'" in str(exc_info.value)

    # 3. Verify state aggregate in SQLite store is completely untouched
    agg_after = persistent_sqlite_store.get_aggregate(agg_id)
    assert agg_after is not None
    assert agg_after.current_state == "SOURCES_ATTACHED"
    assert agg_after.version == 3
    assert agg_after.state_hash == hash_before

    # 4. Verify no extra transition was logged
    transitions = persistent_sqlite_store.list_transitions(agg_id)
    assert len(transitions) == 1
    assert transitions[0].transition_name == "attach_sources"


# ===========================================================================
# Gate 5: Unified Observability Projects Pure Operational Truth
# ===========================================================================

def test_m68_unified_observability_projects_authoritative_sqlite_truth(
    command_engine: UnifiedFactoryCommandEngine,
    persistent_runtime: UniversalProgramStateRuntime,
    persistent_sqlite_store: SqliteProgramStateStore,
) -> None:
    """Gate 5: Factory command inspect and replay project directly from SQLite truth."""
    res_run = command_engine.execute_command_text("run program research_canonicalization_program")
    agg_id = res_run.data["aggregate_id"]

    # Execute transition
    persistent_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="operator:commander",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "sources_verified"],
    )

    # 1. Inspect run via factory command
    res_inspect = command_engine.execute_command_text(f"inspect run {agg_id}")
    assert res_inspect.success
    inspected_run = res_inspect.data["run"]
    assert inspected_run["aggregate_id"] == agg_id
    assert inspected_run["current_state"] == "SOURCES_ATTACHED"
    assert inspected_run["version"] == 3

    # 2. Replay run via factory command
    res_replay = command_engine.execute_command_text(f"replay run {agg_id}")
    assert res_replay.success
    replay_data = res_replay.data["replay"]
    assert len(replay_data["events"]) >= 1
    for event in replay_data["events"]:
        assert event["receipt_sha256"] != ""

    # 3. ReadOnlyObservabilityViewer rendering
    viewer = ReadOnlyObservabilityViewer(command_engine)
    dashboard = viewer.render_factory_floor()
    assert "CAE FACTORY FLOOR DASHBOARD" in dashboard
    assert "Active Runs:" in dashboard


# ===========================================================================
# Gate 6: Process Restart & Re-Read from Persistent SQLite Database
# ===========================================================================

def test_m68_process_restart_preserves_execution_and_replay(
    temp_db_path: str,
) -> None:
    """Gate 6: Entire runtime process restart preserves state aggregate and replay history."""
    # Process 1: Start run and execute transitions
    store_1 = SqliteProgramStateStore(temp_db_path)
    runtime_1 = UniversalProgramStateRuntime(store=store_1)
    operator_1 = ProgramOperatorRuntimeService(runtime=runtime_1)
    engine_1 = UnifiedFactoryCommandEngine(program_operator=operator_1)

    res_run = engine_1.execute_command_text("run program research_canonicalization_program")
    agg_id = res_run.data["aggregate_id"]

    runtime_1.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="operator:commander",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "sources_verified"],
    )

    # Simulate Process Restart: Tear down all Process 1 objects
    del engine_1
    del operator_1
    del runtime_1
    del store_1

    # Process 2: Re-instantiate completely fresh objects against same SQLite DB
    store_2 = SqliteProgramStateStore(temp_db_path)
    runtime_2 = UniversalProgramStateRuntime(store=store_2)
    operator_2 = ProgramOperatorRuntimeService(runtime=runtime_2)
    engine_2 = UnifiedFactoryCommandEngine(program_operator=operator_2)

    # 1. Re-read and inspect restored run
    res_inspect = engine_2.execute_command_text(f"inspect run {agg_id}")
    assert res_inspect.success
    assert res_inspect.data["run"]["current_state"] == "SOURCES_ATTACHED"
    assert res_inspect.data["run"]["version"] == 3

    # 2. Advance execution in Process 2
    res_trans = runtime_2.execute_transition(
        aggregate_id=agg_id,
        transition_name="extract_candidates",
        actor_id="agent:hunter",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "sources_attached"],
    )
    assert res_trans.aggregate.current_state == "CANDIDATES_EXTRACTED"
    assert res_trans.aggregate.version == 4

    # 3. Replay in Process 2
    res_replay = engine_2.execute_command_text(f"replay run {agg_id}")
    assert res_replay.success
    assert len(res_replay.data["replay"]["events"]) == 2  # attach_sources + extract_candidates


# ===========================================================================
# Gate 7 (Countertest): Stale-Context Reuse Detected and Blocked
# ===========================================================================

def test_m68_stale_context_reuse_countertest(
    persistent_runtime: UniversalProgramStateRuntime,
    persistent_operator: ProgramOperatorRuntimeService,
) -> None:
    """Countertest: Stale prior-state context cannot validate subsequent phase transitions."""
    agg = persistent_operator.run_program(
        program_id="research_canonicalization_program",
        workspace_id="test_ws_m68_stale",
        actor_id="operator:commander",
    )
    agg_id = agg.aggregate_id

    # 1. Capture context at INITIAL state
    ctx_init = persistent_runtime.get_local_context(agg_id, active_lane=AuthorityLane.COMMANDER)
    assert ctx_init.aggregate.current_state == "INITIAL"

    # 2. Advance state to SOURCES_ATTACHED
    persistent_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="operator:commander",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=["workspace_active", "sources_verified"],
    )

    # 3. Attempt to validate a transition using the stale INITIAL version
    with pytest.raises(ProgramStateRuntimeError) as exc_info:
        persistent_runtime.validate_transition(
            aggregate_id=agg_id,
            transition_name="extract_candidates",
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active", "sources_attached"],
            expected_version=ctx_init.aggregate.version,  # Stale version 2 vs actual version 3
        )
    assert exc_info.value.reason_code == "STALE_VERSION_CONFLICT"


# ===========================================================================
# Gate 8 (Countertest): Cross-Tenant State and Replay Queries Fail Closed
# ===========================================================================

def test_m68_cross_tenant_access_denial_countertest(
    persistent_runtime: UniversalProgramStateRuntime,
    persistent_operator: ProgramOperatorRuntimeService,
) -> None:
    """Countertest: Cross-tenant trace, inspect, and replay queries are rejected fail-closed."""
    engine = UnifiedFactoryCommandEngine(program_operator=persistent_operator)

    # Run program in tenant alpha
    agg_alpha = persistent_operator.run_program(
        program_id="research_canonicalization_program",
        workspace_id="tenant_alpha_ws",
        actor_id="operator:commander",
    )
    agg_id_alpha = agg_alpha.aggregate_id

    # Tenant Beta attempts to inspect Tenant Alpha's run
    with pytest.raises(ObservabilityTenantIsolationError) as exc_info:
        engine.execute_command_text(f"inspect run {agg_id_alpha}", tenant_id="tenant_beta")
    assert "tenant isolation violation" in str(exc_info.value).lower()

    # Tenant Beta attempts to replay Tenant Alpha's run
    with pytest.raises(ObservabilityTenantIsolationError) as exc_info2:
        engine.execute_command_text(f"replay run {agg_id_alpha}", tenant_id="tenant_beta")
    assert "tenant isolation violation" in str(exc_info2.value).lower()
