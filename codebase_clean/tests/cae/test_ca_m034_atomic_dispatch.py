"""Executable evidence for CA-M034: deterministic two-phase atomic lease dispatch."""

from __future__ import annotations

import concurrent.futures
from pathlib import Path
import tempfile

import pytest

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramLeaseConflictError,
    ProgramStateLifecycle,
    SqliteProgramStateStore,
    UniversalProgramStateRuntime,
)


def _registry() -> ProgramRegistry:
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    return registry


def test_ca_m034_positive_path_is_two_phase_and_workflow_triggered() -> None:
    registry = _registry()
    store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(store=store, program_registry=registry)

    phase1 = runtime.register_program_dispatch(
        program_package=registry.get_program("interview_semantic_program"),
        program_id="interview_semantic_program",
        workspace_id="ws-m034",
        actor_id="commander-1",
        initial_data={"guest_id": "guest-1"},
    )
    assert phase1.version == 0
    assert phase1.lifecycle is ProgramStateLifecycle.INITIALIZED
    assert store.get_execution_lease(phase1.aggregate_id)["status"] == "LEASE_ENQUEUED"

    running = runtime.acquire_execution_lease_and_trigger(
        aggregate_id=phase1.aggregate_id,
        actor_id="commander-1",
        context_claims=["workspace_active", "interview_brief_approved"],
    )
    assert running.version == 1
    assert running.lifecycle is ProgramStateLifecycle.RUNNING

    lease = store.get_execution_lease(running.aggregate_id)
    assert lease is not None
    assert lease["lease_version"] == 1
    assert lease["status"] == "LEASE_ACQUIRED"
    assert lease["holder_id"] == "commander-1"

    dispatch = store.get_workflow_dispatch(running.aggregate_id)
    assert dispatch is not None
    assert dispatch["status"] == "ENQUEUED"
    assert dispatch["trigger_operation"] == "cae.program.dispatch@1.0.0"
    assert dispatch["context_state_hash"] == phase1.state_hash


def test_ca_m034_stale_claim_fails_closed_without_running_state() -> None:
    registry = _registry()
    store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(store=store, program_registry=registry)

    phase1 = runtime.register_program_dispatch(
        program_package=registry.get_program("interview_semantic_program"),
        program_id="interview_semantic_program",
        workspace_id="ws-m034-stale",
        actor_id="commander-1",
    )

    with pytest.raises(ProgramLeaseConflictError):
        runtime.acquire_execution_lease_and_trigger(
            aggregate_id=phase1.aggregate_id,
            actor_id="commander-1",
            expected_lease_version=1,
        )

    after = store.get_aggregate(phase1.aggregate_id)
    lease = store.get_execution_lease(phase1.aggregate_id)
    assert after is not None
    assert after.version == 0
    assert after.lifecycle is ProgramStateLifecycle.INITIALIZED
    assert lease["status"] == "LEASE_ENQUEUED"
    assert lease["lease_version"] == 0
    assert store.get_workflow_dispatch(phase1.aggregate_id) is None


def test_ca_m034_false_proof_in_memory_lease_marker_does_not_claim_authority() -> None:
    registry = _registry()
    store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(store=store, program_registry=registry)

    phase1 = runtime.register_program_dispatch(
        program_package=registry.get_program("interview_semantic_program"),
        program_id="interview_semantic_program",
        workspace_id="ws-m034-false-proof",
        actor_id="commander-1",
        initial_data={"lease_version": 1, "lease_status": "LEASE_ACQUIRED"},
    )

    # Countercase: state_data that merely says a lease exists must not satisfy the durable lease CAS.
    with pytest.raises(ProgramLeaseConflictError):
        runtime.acquire_execution_lease_and_trigger(
            aggregate_id=phase1.aggregate_id,
            actor_id="commander-1",
        )

    after = store.get_aggregate(phase1.aggregate_id)
    assert after.lifecycle is ProgramStateLifecycle.INITIALIZED
    assert after.version == 0
    assert store.get_workflow_dispatch(phase1.aggregate_id) is None


def test_ca_m034_sqlite_concurrent_claim_has_exactly_one_winner() -> None:
    registry = _registry()
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "ca_m034.db")
        bootstrap = UniversalProgramStateRuntime(
            store=SqliteProgramStateStore(db_path),
            program_registry=registry,
        )
        phase1 = bootstrap.register_program_dispatch(
            program_package=registry.get_program("interview_semantic_program"),
            program_id="interview_semantic_program",
            workspace_id="ws-m034-concurrent",
            actor_id="commander-bootstrap",
        )

        def claim(actor_id: str):
            local_runtime = UniversalProgramStateRuntime(
                store=SqliteProgramStateStore(db_path),
                program_registry=registry,
            )
            try:
                return local_runtime.acquire_execution_lease_and_trigger(
                    aggregate_id=phase1.aggregate_id,
                    actor_id=actor_id,
                )
            except ProgramLeaseConflictError:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            first, second = pool.map(claim, ["worker-a", "worker-b"])

        winners = [value for value in (first, second) if value is not None]
        assert len(winners) == 1
        assert winners[0].lifecycle is ProgramStateLifecycle.RUNNING
        assert winners[0].version == 1

        check = UniversalProgramStateRuntime(
            store=SqliteProgramStateStore(db_path),
            program_registry=registry,
        )
        stored = check.get_aggregate(phase1.aggregate_id)
        lease = check.store.get_execution_lease(phase1.aggregate_id)
        dispatch = check.store.get_workflow_dispatch(phase1.aggregate_id)
        assert stored.lifecycle is ProgramStateLifecycle.RUNNING
        assert stored.version == 1
        assert lease["status"] == "LEASE_ACQUIRED"
        assert lease["lease_version"] == 1
        assert dispatch["status"] == "ENQUEUED"
        assert dispatch["context_state_hash"] in (phase1.state_hash, stored.state_hash)


def test_ca_m034_sqlite_operator_boundary_persists_phase_one_and_phase_two() -> None:
    registry = _registry()
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "ca_m034_operator.db")
        runtime = UniversalProgramStateRuntime(
            store=SqliteProgramStateStore(db_path),
            program_registry=registry,
        )
        service = ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)

        aggregate = service.run_program(
            program_id="interview_semantic_program",
            workspace_id="ws-m034-operator",
            actor_id="commander-1",
        )

        restored = UniversalProgramStateRuntime(
            store=SqliteProgramStateStore(db_path),
            program_registry=registry,
        )
        stored = restored.get_aggregate(aggregate.aggregate_id)
        lease = restored.store.get_execution_lease(aggregate.aggregate_id)
        dispatch = restored.store.get_workflow_dispatch(aggregate.aggregate_id)

        assert stored.lifecycle is ProgramStateLifecycle.RUNNING
        assert stored.version == 1
        assert lease["status"] == "LEASE_ACQUIRED"
        assert lease["lease_version"] == 1
        assert dispatch["status"] == "ENQUEUED"


def test_ca_m034_operator_boundary_requires_commander_and_returns_running() -> None:
    registry = _registry()
    runtime = UniversalProgramStateRuntime(
        store=InMemoryProgramStateStore(),
        program_registry=registry,
    )
    service = ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)

    with pytest.raises(ProgramAuthorityLaneViolationError):
        service.run_program(
            program_id="interview_semantic_program",
            workspace_id="ws-m034-auth",
            actor_lane=AuthorityLane.HUNTER,
        )

    aggregate = service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-m034-auth",
        actor_id="commander-1",
    )
    assert aggregate.lifecycle is ProgramStateLifecycle.RUNNING
    assert aggregate.version == 1
    lease = runtime.store.get_execution_lease(aggregate.aggregate_id)
    assert lease["status"] == "LEASE_ACQUIRED"

