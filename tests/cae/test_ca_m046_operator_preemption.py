"""CA-M046 / INV-PREEMPT-001 proof suite.

Covers the complete bounded control chain:
operator authorization -> workspace binding -> CAS state commit -> durable
preemption receipt material -> cancellation signal -> real isolated worker
interruption.  Negative cases explicitly prove fail-closed behavior.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from ca_runtime.agent_host_runner import AgentHostRunner, HostRunnerConfig, ProviderSpec
from ca_runtime.operator_preemption import ExecutionCancellationToken, ExecutionCancelledError
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramStateLifecycle,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
    get_canonical_interview_state_machine,
)
from ca_runtime.tenancy import CrossWorkspaceLeakError, TenantContext, UnauthorizedOperatorAccessError


WS = UUID("11111111-1111-1111-1111-111111111111")
OTHER_WS = UUID("22222222-2222-2222-2222-222222222222")
OPERATOR_GRANT = UUID("33333333-3333-3333-3333-333333333333")


@pytest.fixture
def runtime() -> UniversalProgramStateRuntime:
    store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(store=store)
    runtime.register_state_machine(get_canonical_interview_state_machine())
    return runtime


@pytest.fixture
def operator_service(runtime: UniversalProgramStateRuntime) -> ProgramOperatorRuntimeService:
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    return ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)


def operator_context(actor_id: str = "operator-alice", workspace_id: UUID = WS) -> TenantContext:
    return TenantContext(
        workspace_id=workspace_id,
        actor_id=actor_id,
        role="OPERATOR",
        is_operator=True,
        operator_grant_id=OPERATOR_GRANT,
    )


def start_execution(service: ProgramOperatorRuntimeService, *, workspace_id: UUID = WS, actor_id: str = "operator-alice"):
    return service.run_program(
        program_id="interview_semantic_program",
        workspace_id=str(workspace_id),
        actor_id=actor_id,
        initial_data={"preserved": "checkpoint-value", "counter": 7},
    )


def test_successful_abort_commits_cancel_and_preserves_execution_state(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    original_state = dict(agg.state_data)
    context = operator_context()

    token = operator_service.execution_controls.bind(agg.aggregate_id)
    callback_called = threading.Event()
    token.add_callback("synthetic-worker", callback_called.set)

    updated = operator_service.abort_program(
        aggregate_id=agg.aggregate_id,
        actor_id="operator-alice",
        operator_context=context,
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
        reason="operator safety stop",
    )

    assert updated.lifecycle is ProgramStateLifecycle.CANCELLED
    assert updated.version == agg.version + 1
    assert updated.current_state == agg.current_state
    assert updated.state_data["preserved"] == original_state["preserved"]
    assert updated.state_data["counter"] == original_state["counter"]
    assert updated.last_receipt_id == updated.state_data["preemption"]["receipt_id"]
    assert updated.state_data["preemption"]["source_state"] == agg.lifecycle.value
    assert updated.state_data["preemption"]["target_state"] == "CANCELLED"
    assert updated.state_data["preemption"]["cancellation_observed"] is False
    assert callback_called.wait(0.5)
    assert token.is_cancelled


def test_stale_abort_cannot_preempt_or_change_state(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    token = operator_service.execution_controls.bind(agg.aggregate_id)

    with pytest.raises(ProgramStateVersionConflictError):
        operator_service.abort_program(
            aggregate_id=agg.aggregate_id,
            actor_id="operator-alice",
            operator_context=operator_context(),
            expected_version=agg.version + 1,
            expected_state_sha256=agg.state_hash,
        )

    current = operator_service.runtime.get_aggregate(agg.aggregate_id)
    assert current.lifecycle is agg.lifecycle
    assert current.version == agg.version
    assert not token.is_cancelled


def test_wrong_workspace_is_rejected_before_cancellation(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    token = operator_service.execution_controls.bind(agg.aggregate_id)

    with pytest.raises(CrossWorkspaceLeakError):
        operator_service.abort_program(
            aggregate_id=agg.aggregate_id,
            actor_id="operator-alice",
            operator_context=operator_context(workspace_id=OTHER_WS),
            expected_version=agg.version,
            expected_state_sha256=agg.state_hash,
        )

    current = operator_service.runtime.get_aggregate(agg.aggregate_id)
    assert current.lifecycle is agg.lifecycle
    assert not token.is_cancelled


def test_non_operator_is_rejected_fail_closed(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    token = operator_service.execution_controls.bind(agg.aggregate_id)
    context = TenantContext(workspace_id=WS, actor_id="member-bob", role="MEMBER")

    with pytest.raises(UnauthorizedOperatorAccessError):
        operator_service.abort_program(
            aggregate_id=agg.aggregate_id,
            actor_id="member-bob",
            operator_context=context,
            expected_version=agg.version,
            expected_state_sha256=agg.state_hash,
        )

    assert operator_service.runtime.get_aggregate(agg.aggregate_id).lifecycle is agg.lifecycle
    assert not token.is_cancelled


def test_actor_identity_mismatch_cannot_self_grant_control(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service, actor_id="operator-alice")
    token = operator_service.execution_controls.bind(agg.aggregate_id)

    with pytest.raises(ValueError, match="actor_id must match"):
        operator_service.abort_program(
            aggregate_id=agg.aggregate_id,
            actor_id="operator-forged",
            operator_context=operator_context("operator-alice"),
            expected_version=agg.version,
            expected_state_sha256=agg.state_hash,
        )

    assert not token.is_cancelled


def test_terminal_execution_is_not_rewritten(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    completed = operator_service.runtime.set_lifecycle(
        aggregate_id=agg.aggregate_id,
        new_lifecycle=ProgramStateLifecycle.COMPLETED,
        actor_id="runtime",
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )
    token = operator_service.execution_controls.bind(agg.aggregate_id)

    with pytest.raises(ProgramTransitionBlockedError):
        operator_service.abort_program(
            aggregate_id=agg.aggregate_id,
            actor_id="operator-alice",
            operator_context=operator_context(),
            expected_version=completed.version,
            expected_state_sha256=completed.state_hash,
        )

    current = operator_service.runtime.get_aggregate(agg.aggregate_id)
    assert current.lifecycle is ProgramStateLifecycle.COMPLETED
    assert not token.is_cancelled


def test_gate_suspended_execution_fails_closed(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    gate_suspended = operator_service.runtime.set_lifecycle(
        aggregate_id=agg.aggregate_id,
        new_lifecycle=ProgramStateLifecycle.AWAITING_APPROVAL,
        actor_id="runtime",
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )

    with pytest.raises(ProgramTransitionBlockedError):
        operator_service.abort_program(
            aggregate_id=agg.aggregate_id,
            actor_id="operator-alice",
            operator_context=operator_context(),
            expected_version=gate_suspended.version,
            expected_state_sha256=gate_suspended.state_hash,
        )

    assert operator_service.runtime.get_aggregate(agg.aggregate_id).lifecycle is ProgramStateLifecycle.AWAITING_APPROVAL


def test_cancellation_token_preempts_bound_callbacks_immediately():
    token = ExecutionCancellationToken("exec:test")
    notified = []
    token.add_callback("model-socket", lambda: notified.append("socket"))
    token.add_callback("tool-worker", lambda: notified.append("tool"))

    observation = token.cancel()

    assert token.is_cancelled
    assert set(notified) == {"socket", "tool"}
    assert observation.observed
    assert observation.latency_ms >= 0
    with pytest.raises(ExecutionCancelledError):
        token.raise_if_cancelled()


def _slow_provider(_request):
    time.sleep(10)
    return {"response": "should never return"}


def test_real_isolated_worker_is_interrupted_by_operator_token():
    token = ExecutionCancellationToken("exec:worker-proof")
    runner = AgentHostRunner(
        providers=(ProviderSpec(name="slow", invoke=_slow_provider),),
        config=HostRunnerConfig(wall_clock_timeout_ms=15_000),
    )
    invocation = {
        "agent_id": "agent-proof",
        "model_id": "slow-model",
        "prompt": "long-running operation",
        "system_prompt": "test",
        "tools": [],
        "messages": [],
    }

    holder: dict[str, object] = {}

    def run_worker() -> None:
        try:
            runner.run(invocation, cancellation_token=token)
        except BaseException as exc:
            holder["exc"] = exc

    thread = threading.Thread(target=run_worker, daemon=True)
    thread.start()
    time.sleep(0.20)
    started = time.monotonic()
    observation = token.cancel()
    thread.join(timeout=3.0)
    elapsed = time.monotonic() - started

    assert observation.observed
    assert not thread.is_alive(), "real isolated worker did not stop after cancellation"
    assert isinstance(holder.get("exc"), ExecutionCancelledError)
    assert elapsed < 3.0


def test_abort_receipt_is_cryptographically_self_consistent(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    updated = operator_service.abort_program(
        aggregate_id=agg.aggregate_id,
        actor_id="operator-alice",
        operator_context=operator_context(),
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )
    receipt = updated.state_data["preemption"]
    from ca_contracts import canonical_sha256

    without_digest = dict(receipt)
    without_digest.pop("receipt_sha256")
    assert receipt["receipt_sha256"] == canonical_sha256(without_digest)
    assert receipt["committed_version"] == updated.version
    assert receipt["aggregate_id"] == agg.aggregate_id


def test_pause_resume_state_semantics_remain_untouched(operator_service: ProgramOperatorRuntimeService):
    agg = start_execution(operator_service)
    paused = operator_service.pause_program(
        aggregate_id=agg.aggregate_id,
        actor_id="operator-alice",
        expected_version=agg.version,
        expected_state_sha256=agg.state_hash,
    )
    resumed = operator_service.resume_program(
        aggregate_id=paused.aggregate_id,
        actor_id="operator-alice",
        expected_version=paused.version,
        expected_state_sha256=paused.state_hash,
    )
    assert paused.lifecycle is ProgramStateLifecycle.PAUSED
    assert resumed.lifecycle is ProgramStateLifecycle.RUNNING

