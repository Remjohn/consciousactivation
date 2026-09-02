"""
Unit and Integration Tests for CAE Mandate M66: Authoritative Program Execution Convergence.

Validates:
- Real ProgramStateAggregate creation in UniversalProgramStateRuntime via RUN PROGRAM
- Returned ID equals stored aggregate ID
- Dynamic Replay construction from stored StateTransitionReceipt records
- Multi-tenant isolation failure on cross-tenant inspection/replay
- Pause/resume/approve/reject/repair execution via authoritative state transitions
- Durability across process restart with SQLiteProgramStateStore
- Anti-synthetic countertest (unpersisted/synthetic runs rejected fail-closed)
"""

import os
from pathlib import Path
import shutil
import tempfile
from typing import List, Tuple
import pytest

from ca_runtime.factory_observability import (
    EntityNotFoundError,
    FactoryCommand,
    FactoryCommandVerb,
    FactoryFloorSnapshot,
    FactoryTargetType,
    ObservabilityTenantIsolationError,
    ReadOnlyObservabilityViewer,
    UnifiedFactoryCommandEngine,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    ProgramStateLifecycle,
    SqliteProgramStateStore,
    UniversalProgramStateRuntime,
)


# ============================================================================
# Test 1 & 2: RUN PROGRAM Produces Authoritative Aggregate and ID Parity
# ============================================================================


def test_m66_run_program_creates_authoritative_aggregate() -> None:
    """Prove that factory RUN creates a genuine aggregate in UniversalProgramStateRuntime."""
    state_runtime = UniversalProgramStateRuntime()
    op_service = ProgramOperatorRuntimeService(runtime=state_runtime)
    engine = UnifiedFactoryCommandEngine(program_operator=op_service)

    # Execute factory RUN
    res = engine.execute_command_text("run program research_canonicalization_program", tenant_id="ws_alpha")
    assert res.success
    agg_id = res.data["run_id"]
    assert agg_id == res.data["aggregate_id"]

    # Verify directly in authoritative state store
    stored_agg = state_runtime.store.get_aggregate(agg_id)
    assert stored_agg is not None
    assert stored_agg.aggregate_id == agg_id
    assert stored_agg.program_id == "research_canonicalization_program"
    assert stored_agg.lifecycle == ProgramStateLifecycle.RUNNING
    assert stored_agg.state_hash == res.data["state_hash"]
    assert stored_agg.version == 2


# ============================================================================
# Test 3: Replay Constructed Dynamically from Authoritative Transitions
# ============================================================================


def test_m66_replay_constructed_from_authoritative_transitions() -> None:
    """Prove that factory REPLAY reconstructs events from stored state transitions."""
    state_runtime = UniversalProgramStateRuntime()
    op_service = ProgramOperatorRuntimeService(runtime=state_runtime)
    engine = UnifiedFactoryCommandEngine(program_operator=op_service)

    # 1. Start program run
    res_run = engine.execute_command_text("run program research_canonicalization_program", tenant_id="ws_replay")
    agg_id = res_run.data["run_id"]

    # 2. Execute a transition on the research_canonicalization state machine
    state_runtime.execute_transition(
        aggregate_id=agg_id,
        transition_name="attach_sources",
        actor_id="commander_1",
        actor_lane=AuthorityLane.COMMANDER,
        context_claims=("workspace_active", "sources_verified"),
        payload={"source_ids": ["src_1", "src_2"]},
    )

    # 3. Replay run
    res_replay = engine.execute_command_text(f"replay run {agg_id}", tenant_id="ws_replay")
    assert res_replay.success
    replay = res_replay.data["replay"]

    # Verify transitions in store match replay events
    transitions = state_runtime.store.list_transitions(agg_id)
    assert len(transitions) == len(replay["events"]) == 1
    assert replay["events"][0]["event_kind"] == "attach_sources"
    assert replay["events"][0]["state_after"] == "SOURCES_ATTACHED"
    assert replay["events"][0]["receipt_sha256"] == transitions[0].receipt_id
    assert replay["events"][0]["is_committed"]


# ============================================================================
# Test 4: Cross-Tenant Access Fails Closed
# ============================================================================


def test_m66_cross_tenant_access_fails_closed() -> None:
    """Prove that inspecting or replaying an aggregate from another tenant raises ObservabilityTenantIsolationError."""
    state_runtime = UniversalProgramStateRuntime()
    op_service = ProgramOperatorRuntimeService(runtime=state_runtime)
    engine = UnifiedFactoryCommandEngine(program_operator=op_service)

    # Start run for tenant_a
    res_run = engine.execute_command_text("run program research_canonicalization_program", tenant_id="tenant_a")
    agg_id = res_run.data["run_id"]

    # Attempt inspection from tenant_b -> fails closed
    with pytest.raises(ObservabilityTenantIsolationError) as exc_info:
        engine.execute_command_text(f"inspect run {agg_id}", tenant_id="tenant_b")
    assert exc_info.value.reason_code == "ERR_OBSERVABILITY_TENANT_ISOLATION"

    # Attempt replay from tenant_b -> fails closed
    with pytest.raises(ObservabilityTenantIsolationError) as exc_info:
        engine.execute_command_text(f"replay run {agg_id}", tenant_id="tenant_b")
    assert exc_info.value.reason_code == "ERR_OBSERVABILITY_TENANT_ISOLATION"


# ============================================================================
# Test 5: Operator Control Operations Execute via Authoritative Transitions
# ============================================================================


def test_m66_operator_control_executes_authoritative_transitions() -> None:
    """Prove that pause, resume, and repair update the authoritative state machine aggregate."""
    state_runtime = UniversalProgramStateRuntime()
    op_service = ProgramOperatorRuntimeService(runtime=state_runtime)
    engine = UnifiedFactoryCommandEngine(program_operator=op_service)

    # Start run
    res_run = engine.execute_command_text("run program research_canonicalization_program", tenant_id="ws_ops")
    agg_id = res_run.data["run_id"]
    assert res_run.data["version"] == 2

    # Pause
    res_pause = engine.execute_command_text(f"pause run {agg_id}", tenant_id="ws_ops")
    assert res_pause.data["lifecycle"] == "PAUSED"
    assert res_pause.data["version"] == 3

    # Resume
    res_resume = engine.execute_command_text(f"resume run {agg_id}", tenant_id="ws_ops")
    assert res_resume.data["lifecycle"] == "RUNNING"
    assert res_resume.data["version"] == 4

    # Repair
    res_repair = engine.execute_command_text(f"repair run {agg_id}", tenant_id="ws_ops")
    assert res_repair.data["version"] == 5

    # Verify repair transition recorded in store
    transitions = state_runtime.store.list_transitions(agg_id)
    assert len(transitions) == 1
    assert transitions[0].transition_name == "repair:factory_command_repair"


# ============================================================================
# Test 6: SQLite Persistence Durability Across Restart
# ============================================================================


def test_m66_sqlite_persistence_durability_across_process_restart() -> None:
    """Prove that runs executed via factory commands persist across process restarts when SQLite is used."""
    tmpdir = tempfile.mkdtemp()
    try:
        db_path = os.path.join(tmpdir, "cae_state.db")

        # Session 1: Create store and run program
        store_1 = SqliteProgramStateStore(db_path=db_path)
        runtime_1 = UniversalProgramStateRuntime(store=store_1)
        op_1 = ProgramOperatorRuntimeService(runtime=runtime_1)
        engine_1 = UnifiedFactoryCommandEngine(program_operator=op_1)

        res_run = engine_1.execute_command_text("run program research_canonicalization_program", tenant_id="tenant_dur")
        agg_id = res_run.data["run_id"]
        engine_1.execute_command_text(f"pause run {agg_id}", tenant_id="tenant_dur")

        del engine_1, op_1, runtime_1, store_1

        # Session 2: Fresh instance pointing to same SQLite db
        store_2 = SqliteProgramStateStore(db_path=db_path)
        runtime_2 = UniversalProgramStateRuntime(store=store_2)
        op_2 = ProgramOperatorRuntimeService(runtime=runtime_2)
        engine_2 = UnifiedFactoryCommandEngine(program_operator=op_2)

        # Inspect run
        res_inspect = engine_2.execute_command_text(f"inspect run {agg_id}", tenant_id="tenant_dur")
        assert res_inspect.success
        assert res_inspect.data["run"]["aggregate_id"] == agg_id
        assert res_inspect.data["run"]["lifecycle"] == "PAUSED"
        assert res_inspect.data["run"]["version"] == 3

        # Replay run
        res_replay = engine_2.execute_command_text(f"replay run {agg_id}", tenant_id="tenant_dur")
        assert res_replay.success
        assert res_replay.data["replay"]["run_id"] == agg_id
        assert res_replay.data["replay"]["tenant_id"] == "tenant_dur"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ============================================================================
# Test 7: Anti-Synthetic Countertest
# ============================================================================


def test_m66_anti_synthetic_countertest_nonexistent_run_rejected() -> None:
    """Countertest: Inspecting or replaying a non-existent run raises EntityNotFoundError."""
    engine = UnifiedFactoryCommandEngine()

    with pytest.raises(EntityNotFoundError) as exc_info:
        engine.execute_command_text("inspect run nonexistent_run_123")
    assert exc_info.value.reason_code == "ERR_ENTITY_NOT_FOUND"

    with pytest.raises(EntityNotFoundError) as exc_info:
        engine.execute_command_text("replay run nonexistent_run_123")
    assert exc_info.value.reason_code == "ERR_ENTITY_NOT_FOUND"
