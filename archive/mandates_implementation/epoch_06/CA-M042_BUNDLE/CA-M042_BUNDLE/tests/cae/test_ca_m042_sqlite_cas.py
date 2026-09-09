"""Executable proof for CA-M042 / INV-CAS-001.

The tests exercise the canonical UniversalProgramStateRuntime against real
SQLite connections. The concurrency proof deliberately uses two independent
store instances and a test barrier; it does not use a process-local mutex as
the correctness mechanism.
"""

from __future__ import annotations

from pathlib import Path
from threading import Barrier, Thread
from typing import Any
from uuid import uuid4

import pytest

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    ProgramStateVersionConflictError,
    ProgramTransitionResult,
    SqliteProgramStateStore,
    UniversalProgramStateRuntime,
)


@pytest.fixture
def program_registry() -> ProgramRegistry:
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    return registry


def _new_runtime(db_path: Path, registry: ProgramRegistry) -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime(
        store=SqliteProgramStateStore(db_path),
        program_registry=registry,
    )


def _initialize_interview_runtime(
    db_path: Path,
    registry: ProgramRegistry,
) -> tuple[UniversalProgramStateRuntime, str]:
    runtime = _new_runtime(db_path, registry)
    aggregate = runtime.initialize_program_state(
        program_package=registry.get_program("interview_semantic_program"),
        workspace_id=str(uuid4()),
        actor_id="actor_hunter_01",
        context_claims=["workspace_active", "interview_brief_approved"],
        initial_data={"initial": True},
    )
    return runtime, aggregate.aggregate_id


def _start_elicitation(runtime: UniversalProgramStateRuntime, aggregate_id: str, actor_id: str, *, expected_version: int) -> ProgramTransitionResult:
    return runtime.execute_transition(
        aggregate_id=aggregate_id,
        transition_name="start_elicitation",
        actor_id=actor_id,
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "interview_brief_approved"],
        expected_version=expected_version,
        state_updates={"actor": actor_id},
    )


def test_ca_m042_positive_cas_advances_exactly_one_version(
    tmp_path: Path,
    program_registry: ProgramRegistry,
) -> None:
    runtime, aggregate_id = _initialize_interview_runtime(tmp_path / "ca_m042_positive.db", program_registry)

    result = _start_elicitation(runtime, aggregate_id, "actor_hunter_01", expected_version=1)

    persisted = runtime.get_aggregate(aggregate_id)
    assert result.aggregate.version == 2
    assert persisted.version == 2
    assert persisted.state_data["actor"] == "actor_hunter_01"
    assert len(runtime.store.list_transitions(aggregate_id)) == 1


def test_ca_m042_stale_version_is_rejected_without_partial_state_mutation(
    tmp_path: Path,
    program_registry: ProgramRegistry,
) -> None:
    db_path = tmp_path / "ca_m042_stale.db"
    runtime_a, aggregate_id = _initialize_interview_runtime(db_path, program_registry)
    runtime_b = _new_runtime(db_path, program_registry)

    _start_elicitation(runtime_a, aggregate_id, "winner", expected_version=1)

    with pytest.raises(ProgramStateVersionConflictError) as exc_info:
        _start_elicitation(runtime_b, aggregate_id, "stale-writer", expected_version=1)

    assert exc_info.value.expected_version == 1
    assert exc_info.value.actual_version == 2

    persisted = runtime_b.get_aggregate(aggregate_id)
    assert persisted.version == 2
    assert persisted.current_state == "QUESTIONING"
    assert persisted.state_data["actor"] == "winner"
    assert len(runtime_b.store.list_transitions(aggregate_id)) == 1


def test_ca_m042_two_real_sqlite_connections_have_one_winner_and_one_conflict(
    tmp_path: Path,
    program_registry: ProgramRegistry,
) -> None:
    db_path = tmp_path / "ca_m042_concurrency.db"
    runtime_seed, aggregate_id = _initialize_interview_runtime(db_path, program_registry)

    class BarrierSqliteProgramStateStore(SqliteProgramStateStore):
        def __init__(self, path: Path, barrier: Barrier) -> None:
            self._cas_barrier = barrier
            super().__init__(path)

        def save_aggregate(self, aggregate: Any, expected_version: int | None = None) -> None:
            if expected_version is not None:
                self._cas_barrier.wait(timeout=10)
            return super().save_aggregate(aggregate, expected_version=expected_version)

    barrier = Barrier(2)
    runtime_a = UniversalProgramStateRuntime(
        store=BarrierSqliteProgramStateStore(db_path, barrier),
        program_registry=program_registry,
    )
    runtime_b = UniversalProgramStateRuntime(
        store=BarrierSqliteProgramStateStore(db_path, barrier),
        program_registry=program_registry,
    )

    # Both workers read the same committed version before either reaches the CAS.
    assert runtime_a.get_aggregate(aggregate_id).version == 1
    assert runtime_b.get_aggregate(aggregate_id).version == 1

    outcomes: list[tuple[str, object]] = []

    def worker(runtime: UniversalProgramStateRuntime, actor_id: str) -> None:
        try:
            outcomes.append(("success", _start_elicitation(runtime, aggregate_id, actor_id, expected_version=1)))
        except ProgramStateVersionConflictError as error:
            outcomes.append(("conflict", error))

    thread_a = Thread(target=worker, args=(runtime_a, "worker_a"))
    thread_b = Thread(target=worker, args=(runtime_b, "worker_b"))
    thread_a.start()
    thread_b.start()
    thread_a.join(timeout=10)
    thread_b.join(timeout=10)

    assert not thread_a.is_alive()
    assert not thread_b.is_alive()
    assert sorted(kind for kind, _ in outcomes) == ["conflict", "success"]

    persisted = runtime_seed.get_aggregate(aggregate_id)
    assert persisted.version == 2
    assert persisted.state_data["actor"] in {"worker_a", "worker_b"}
    transitions = runtime_seed.store.list_transitions(aggregate_id)
    assert len(transitions) == 1
    assert transitions[0].expected_version == 1
    assert transitions[0].committed_version == 2


def test_ca_m042_stale_cas_does_not_emit_a_second_transition_or_receipt_claim(
    tmp_path: Path,
    program_registry: ProgramRegistry,
) -> None:
    db_path = tmp_path / "ca_m042_receipt_conflict.db"
    runtime_a, aggregate_id = _initialize_interview_runtime(db_path, program_registry)
    runtime_b = _new_runtime(db_path, program_registry)

    first = _start_elicitation(runtime_a, aggregate_id, "accepted", expected_version=1)

    with pytest.raises(ProgramStateVersionConflictError):
        _start_elicitation(runtime_b, aggregate_id, "rejected", expected_version=1)

    persisted = runtime_b.get_aggregate(aggregate_id)
    transitions = runtime_b.store.list_transitions(aggregate_id)
    assert persisted.last_receipt_id == first.receipt_id
    assert len(transitions) == 1
    assert transitions[0].receipt_id == first.receipt_id
    assert all(t.actor_id != "rejected" for t in transitions)
