import pytest

from cmf_builder.workflow.checkpoint_isolation import (
    CheckpointIsolationError,
    ParallelPlan,
    ParallelWorkUnit,
)


def unit(unit_id, writes, deps=()):
    return ParallelWorkUnit(unit_id, deps, tuple(writes), f"authority:{unit_id}")


def plan(*units, **overrides):
    values = {
        "plan_id": "parallel-plan:1",
        "units": units or (unit("a", ("path/a",)), unit("b", ("path/b",))),
        "concurrency_limit": 2,
        "budget_limit": "offline-local-only",
        "cancellation_policy": "cancel-one-branch-preserve-independent-sibling",
        "merge_policy": "explicit-integrator-merge",
        "conflict_policy": "block-on-shared-write",
        "terminal_states": ("READY", "BLOCKED", "CANCELLED"),
    }
    values.update(overrides)
    return ParallelPlan(**values)


def test_parallel_plan_requires_independent_disjoint_work():
    compiled = plan()

    assert compiled.execution_performed is False
    assert compiled.plan_identity


def test_dependency_between_concurrent_units_blocks_parallel_eligibility():
    with pytest.raises(CheckpointIsolationError) as caught:
        plan(unit("a", ("path/a",), deps=("b",)), unit("b", ("path/b",)))
    assert caught.value.code == "DEPENDENCY_UNSAFE_PARALLELISM"


def test_shared_write_blocks_parallel_eligibility():
    with pytest.raises(CheckpointIsolationError) as caught:
        plan(unit("a", ("shared",)), unit("b", ("shared",)))
    assert caught.value.code == "SHARED_WRITE_PARALLELISM"


def test_parallel_plan_rejects_unbounded_or_executed_plan():
    with pytest.raises(CheckpointIsolationError) as unbounded:
        plan(concurrency_limit=0)
    assert unbounded.value.code == "UNBOUNDED_PARALLELISM"

    with pytest.raises(CheckpointIsolationError) as executed:
        plan(execution_performed=True)
    assert executed.value.code == "PARALLEL_EXECUTION_PROHIBITED"
