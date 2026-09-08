"""CA-M040 executable contract tests for fail-closed human gate suspension."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pytest

from uuid import uuid4

from ca_contracts import canonical_sha256
from ca_runtime.agent_invocation import AgentInvocation, AgentInvocationRuntime, GateSuspensionExecutionBlockedError
from ca_runtime.program_registry import ProgramManifest, ProgramPackage, ProgramStatus
from ca_runtime.program_state_runtime import (
    AuthorityLane,
    GateSuspensionSnapshot,
    InMemoryProgramStateStore,
    SqliteProgramStateStore,
    ProgramStateLifecycle,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
    get_canonical_collision_state_machine,
)


class _GateProgramRegistry:
    def __init__(self, gates: list[str]):
        manifest = ProgramManifest(
            id="collision_discovery_program",
            version="1.0.0",
            status=ProgramStatus.ACTIVE,
            purpose="CA-M040 focused gate fixture",
            lanes=[lane.value for lane in AuthorityLane],
            operator_gates=gates,
        )
        self.package = ProgramPackage(
            program_id=manifest.id,
            version=manifest.version,
            package_root=str(Path.cwd()),
            manifest=manifest,
            manifest_sha256="fixture",
            package_sha256="fixture",
        )

    def get_program(self, program_id: str):
        if program_id != self.package.program_id:
            raise KeyError(program_id)
        return self.package


def _runtime_and_running_aggregate(store=None) -> tuple[UniversalProgramStateRuntime, str]:
    registry = _GateProgramRegistry(["hypothesis_approval_gate"])
    runtime = UniversalProgramStateRuntime(
        store=store or InMemoryProgramStateStore(),
        program_registry=registry,
    )
    runtime.register_state_machine(get_canonical_collision_state_machine())
    aggregate = runtime.register_program_dispatch(
        program_package=registry.package,
        program_id=None,
        workspace_id="ws-m040",
        actor_id="test-commander",
        initial_data={
            "hypothesis": "test",
            "collision_hypotheses": [{"id": "h-1", "status": "EVALUATED"}],
            "qa_scores": {"quality": 99},
        },
    )
    runtime.acquire_execution_lease_and_trigger(
        aggregate_id=aggregate.aggregate_id,
        actor_id="test-commander",
        expected_lease_version=0,
        context_claims=[],
    )
    runtime.execute_transition(
        aggregate_id=aggregate.aggregate_id,
        transition_name="ingest_corpus",
        actor_id="hunter",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "guest_profile_verified"],
    )
    runtime.execute_transition(
        aggregate_id=aggregate.aggregate_id,
        transition_name="hunt_signals",
        actor_id="hunter",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active"],
    )
    runtime.execute_transition(
        aggregate_id=aggregate.aggregate_id,
        transition_name="form_hypothesis",
        actor_id="analyst",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
    )
    return runtime, aggregate.aggregate_id


def test_ca_m040_halts_at_declared_gate_and_persists_immutable_snapshot() -> None:
    runtime, aggregate_id = _runtime_and_running_aggregate()

    result = runtime.execute_transition(
        aggregate_id=aggregate_id,
        transition_name="evaluate_collision",
        actor_id="analyst",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        payload={
            "node_id": "evaluate_collision",
            "candidate_outputs": {"selected_hypothesis_id": "h-1"},
            "violations": [{"dimension": "policy", "observed": "operator approval required"}],
            "thresholds": {"quality": 90, "safety": 100, "policy": "human_required"},
        },
    )

    assert result.aggregate.lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL
    assert result.gate_suspension is not None
    snapshot = result.gate_suspension
    assert isinstance(snapshot, GateSuspensionSnapshot)
    assert snapshot.gate_id == "hypothesis_approval_gate"
    assert snapshot.required_lane == AuthorityLane.COMMANDER
    assert snapshot.state_version == result.aggregate.version - 1
    assert snapshot.state_hash
    assert snapshot.candidate_outputs == {"selected_hypothesis_id": "h-1"}
    assert snapshot.violations[0]["dimension"] == "policy"
    assert snapshot.snapshot_hash
    assert runtime.get_gate_suspension(aggregate_id) == snapshot

    lease = runtime.store.get_execution_lease(aggregate_id)
    assert lease is not None
    assert lease["status"] == "SUSPENDED"
    assert lease["holder_id"] is None

    dispatch = runtime.store.get_workflow_dispatch(aggregate_id)
    assert dispatch is not None
    assert dispatch["status"] == "SUSPENDED"

    alerts = result.aggregate.state_data["alerts"]
    assert alerts[-1]["event_type"] == "GateSuspensionEvent"
    assert alerts[-1]["invariant"] == "INV-GATE-001"


def test_ca_m040_blocks_downstream_transition_while_awaiting_approval() -> None:
    runtime, aggregate_id = _runtime_and_running_aggregate()
    runtime.execute_transition(
        aggregate_id=aggregate_id,
        transition_name="evaluate_collision",
        actor_id="analyst",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
    )

    suspended = runtime.get_aggregate(aggregate_id)
    assert suspended.lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL
    with pytest.raises(ProgramTransitionBlockedError) as exc_info:
        runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="ingest_corpus",
            actor_id="analyst-agent",
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
        )
    assert exc_info.value.reason_code == "TRANSITION_BLOCKED"
    assert exc_info.value.details["reason_code"] == "GATE_AWAITING_APPROVAL"
    assert runtime.get_aggregate(aggregate_id).lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL


def test_ca_m040_prevents_direct_lifecycle_bypass() -> None:
    runtime, aggregate_id = _runtime_and_running_aggregate()
    runtime.execute_transition(
        aggregate_id=aggregate_id,
        transition_name="evaluate_collision",
        actor_id="analyst",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
    )
    with pytest.raises(ProgramTransitionBlockedError) as exc_info:
        runtime.set_lifecycle(
            aggregate_id=aggregate_id,
            new_lifecycle=ProgramStateLifecycle.RUNNING,
            actor_id="rogue-worker",
        )
    assert exc_info.value.details["reason_code"] == "GATE_AWAITING_APPROVAL"


def test_ca_m040_agent_invocation_guard_blocks_before_inference() -> None:
    called = {"inference": False}
    invocation_kwargs = dict(
        invocation_id="inv_m040",
        workspace_id=uuid4(),
        run_id="run-m040",
        lane=AuthorityLane.ANALYST,
        agent_id="agent-m040",
        agent_version="1.0.0",
        state_id="EVALUATED",
        package_sha256="package",
        capsule_sha256="capsule",
        model_id="model",
        model_provider="test",
        temperature_bps=0,
        timeout_ms=1000,
        skills=(),
        tools=(),
        forbidden_actions=(),
        capabilities=(),
        output_contract=None,
        assembled_prompt="prompt",
        system_prompt="system",
        created_at="2026-01-01T00:00:00+00:00",
    )
    template = AgentInvocation(invocation_sha256="", **invocation_kwargs)
    invocation = AgentInvocation(
        invocation_sha256=canonical_sha256(template.canonical_dict()),
        **invocation_kwargs,
    )

    def guard(_invocation: Any) -> None:
        raise GateSuspensionExecutionBlockedError(
            aggregate_id="prog-state:ws-m040:collision_discovery_program:run-1",
            gate_id="hypothesis_approval_gate",
        )

    def inference(_invocation: Any) -> Dict[str, Any]:
        called["inference"] = True
        return {"response_text": "should not execute", "parsed_json": {"ok": True}}

    with pytest.raises(GateSuspensionExecutionBlockedError) as exc_info:
        AgentInvocationRuntime.execute(invocation, inference_fn=inference, execution_guard=guard)

    assert exc_info.value.reason_code == "GATE_AWAITING_APPROVAL"
    assert called["inference"] is False


def test_ca_m040_sqlite_persists_suspension_and_released_lease(tmp_path: Path) -> None:
    db_path = tmp_path / "m040.sqlite3"
    store = SqliteProgramStateStore(db_path)
    runtime, aggregate_id = _runtime_and_running_aggregate(store=store)

    result = runtime.execute_transition(
        aggregate_id=aggregate_id,
        transition_name="evaluate_collision",
        actor_id="analyst",
        actor_lane=AuthorityLane.ANALYST,
        context_claims=["workspace_active"],
        payload={"candidate_outputs": {"selected_hypothesis_id": "h-1"}},
    )

    reopened = UniversalProgramStateRuntime(
        store=SqliteProgramStateStore(db_path),
        program_registry=_GateProgramRegistry(["hypothesis_approval_gate"]),
    )
    reopened.register_state_machine(get_canonical_collision_state_machine())
    persisted = reopened.get_aggregate(aggregate_id)
    assert persisted.lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL
    assert reopened.get_gate_suspension(aggregate_id) == result.gate_suspension
    lease = reopened.store.get_execution_lease(aggregate_id)
    assert lease is not None
    assert lease["status"] == "SUSPENDED"
    assert lease["holder_id"] is None
    assert reopened.list_aggregates(lifecycle=ProgramStateLifecycle.RUNNING) == []


def test_ca_m040_non_gated_execution_remains_running() -> None:
    runtime = UniversalProgramStateRuntime(
        store=InMemoryProgramStateStore(),
        program_registry=_GateProgramRegistry([]),
    )
    runtime.register_state_machine(get_canonical_collision_state_machine())
    aggregate = runtime.register_program_dispatch(
        program_package=runtime.program_registry.package,
        program_id=None,
        workspace_id="ws-m040",
        actor_id="commander",
    )
    runtime.acquire_execution_lease_and_trigger(
        aggregate_id=aggregate.aggregate_id,
        actor_id="commander",
        expected_lease_version=0,
        context_claims=[],
    )
    result = runtime.execute_transition(
        aggregate_id=aggregate.aggregate_id,
        transition_name="ingest_corpus",
        actor_id="hunter",
        actor_lane=AuthorityLane.HUNTER,
        context_claims=["workspace_active", "guest_profile_verified"],
    )
    assert result.aggregate.lifecycle == ProgramStateLifecycle.RUNNING
    assert runtime.get_gate_suspension(aggregate.aggregate_id) is None
