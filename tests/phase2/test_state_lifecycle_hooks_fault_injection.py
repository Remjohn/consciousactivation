"""Phase 2 Mandate M20: State Lifecycle, Hooks, Repair, and Fault Injection Tests.

Governed by:
- 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md
- 00_CONTROL/23_PHASE2_EVENT_TRACE_CONTRACT.md
- 00_CONTROL/24_PHASE2_FAULT_INJECTION_MATRIX.md
- 00_CONTROL/26_PHASE2_REPLAY_IDEMPOTENCY_CONTRACT.md
- 00_CONTROL/06_STATE_AND_HOOKS_MODEL.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
from uuid import UUID, uuid4
import pytest

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime import (
    AuthorityLane,
    AuthorityLaneMismatchError,
    BeforeTransferValidationError,
    CausalTraceEventType,
    CausalTraceLedger,
    CrossWorkspaceLeakError,
    DuplicateResumeBlockedError,
    EffectKind,
    FailureWindow,
    HookExecutionStatus,
    HookPhase,
    HookRejectionError,
    HookResult,
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    ReplaySafety,
    StateCheckpoint,
    StateEffectDeclaration,
    StateLifecycleCoordinator,
    StateLifecycleError,
    StateRepairRequiredError,
    TenantContext,
    UncertainEffectReconciliationError,
    UniversalProgramStateRuntime,
    apply_tenant_session,
    tenant_scope,
    get_canonical_collision_state_machine,
    get_canonical_interview_state_machine,
)


@pytest.fixture
def workspace_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def tenant_context(workspace_id: UUID) -> Any:
    ctx = TenantContext(
        workspace_id=workspace_id,
        actor_id="usr_tester_123",
        role="OPERATOR",
    )
    with tenant_scope(ctx):
        yield ctx


@pytest.fixture
def state_runtime() -> UniversalProgramStateRuntime:
    store = InMemoryProgramStateStore()
    runtime = UniversalProgramStateRuntime(store=store)
    return runtime


@pytest.fixture
def lifecycle_coordinator(state_runtime: UniversalProgramStateRuntime) -> StateLifecycleCoordinator:
    return StateLifecycleCoordinator(state_runtime=state_runtime)


class TestStateLifecycleNormalFlow:
    """Tests the canonical StateM execution lifecycle under normal conditions."""

    def test_complete_statem_lifecycle_execution(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        # 1. Initialize Interview Program state
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_interview_001",
            initial_data={"guest_name": "Jean Pierre", "brief_id": "brief_001"},
            context_claims=["workspace_active", "interview_brief_approved"],
        )
        assert agg.current_state == "INITIAL"
        assert agg.version == 1

        # 2. Register a custom out_hook and before_transfer check
        out_hook_called = []
        before_check_called = []

        def custom_out_hook(a: ProgramStateAggregate, updates: Dict[str, Any], lane: AuthorityLane) -> HookResult:
            out_hook_called.append(True)
            return HookResult(
                phase=HookPhase.OUT_HOOK,
                status=HookExecutionStatus.PASSED,
                check_name="validate_elicitation_payload",
                message="Payload valid",
            )

        def custom_before_transfer(a: ProgramStateAggregate, c: Any, updates: Dict[str, Any]) -> HookResult:
            before_check_called.append(True)
            if "source_id" not in updates:
                return HookResult(
                    phase=HookPhase.BEFORE_TRANSFER,
                    status=HookExecutionStatus.REJECTED,
                    check_name="require_source_id",
                    message="Missing source_id",
                )
            return HookResult(
                phase=HookPhase.BEFORE_TRANSFER,
                status=HookExecutionStatus.PASSED,
                check_name="require_source_id",
                message="source_id verified",
            )

        lifecycle_coordinator.register_out_hook(custom_out_hook)
        lifecycle_coordinator.register_before_transfer_check(custom_before_transfer)

        # 3. Execute State Phase: INITIAL -> QUESTIONING (start_elicitation)
        result = lifecycle_coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=lambda current_agg: {"source_id": "src_audio_456", "elicitation_started": True},
            context=tenant_context,
            context_claims=["workspace_active", "interview_brief_approved"],
            idempotency_key="idemp_start_001",
        )

        assert out_hook_called == [True]
        assert before_check_called == [True]
        assert result.aggregate.current_state == "QUESTIONING"
        assert result.aggregate.version == 2
        assert result.aggregate.state_data["source_id"] == "src_audio_456"
        assert result.receipt["receipt_type"] == "cae_execution_receipt"
        assert result.receipt["validator_results"]["transition_contract"] == "PASS"

        # 4. Check Causal Trace Chain
        traces = lifecycle_coordinator.trace_ledger.get_traces_for_aggregate(agg.aggregate_id)
        event_types = [t.event_type for t in traces]
        assert CausalTraceEventType.STATE_ENTERED in event_types
        assert CausalTraceEventType.OPERATION_STARTED in event_types
        assert CausalTraceEventType.TRANSFER_CHECKED in event_types
        assert CausalTraceEventType.TRANSFERRED in event_types
        assert CausalTraceEventType.COMPLETED in event_types

        # Verify cryptographic trace chaining
        for i in range(1, len(traces)):
            assert traces[i].previous_trace_sha256 == traces[i - 1].trace_sha256


class TestFaultInjectionMatrix:
    """Executes representative fault injection scenarios mandated by 24_PHASE2_FAULT_INJECTION_MATRIX.md."""

    def test_fault_stale_state_optimistic_concurrency_conflict(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Concurrent or out-of-order state modification attempts to advance state.
        
        Expected Outcome: BLOCK (raises ProgramStateVersionConflictError), state unchanged.
        """
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_stale_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )
        assert agg.version == 1

        # Modify state once to advance version to 2
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active", "interview_brief_approved"],
            expected_version=1,
            state_updates={"round": 1},
        )
        agg_v2 = state_runtime.get_aggregate(agg.aggregate_id)
        assert agg_v2.version == 2

        # Now attempt transition expecting version 1 (stale)
        with pytest.raises(ProgramStateVersionConflictError) as exc_info:
            state_runtime.execute_transition(
                aggregate_id=agg.aggregate_id,
                transition_name="record_turn",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                context_claims=["workspace_active"],
                expected_version=1,  # Stale!
            )
        assert exc_info.value.reason_code == "STALE_VERSION_CONFLICT"

    def test_fault_in_hook_rejection_halts_state_entry(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: In-hook invariant check fails (e.g. security claim missing).
        
        Expected Outcome: FAIL-CLOSED (raises HookRejectionError), trace logged as BLOCKED.
        """
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_inhook_fail_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        def rejecting_in_hook(a: ProgramStateAggregate, t: str, lane: AuthorityLane, ctx: TenantContext) -> HookResult:
            return HookResult(
                phase=HookPhase.IN_HOOK,
                status=HookExecutionStatus.REJECTED,
                check_name="media_pipeline_readiness",
                message="Media ingest endpoint is offline",
            )

        lifecycle_coordinator.register_in_hook(rejecting_in_hook)

        with pytest.raises(HookRejectionError) as exc_info:
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="start_elicitation",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {"data": "foo"},
                context=tenant_context,
                context_claims=["workspace_active", "interview_brief_approved"],
            )

        assert "media_pipeline_readiness" in str(exc_info.value)

        # Verify BLOCKED trace emitted
        traces = lifecycle_coordinator.trace_ledger.get_traces_for_aggregate(agg.aggregate_id)
        assert any(t.event_type == CausalTraceEventType.BLOCKED for t in traces)

    def test_fault_failed_before_transfer_check_blocks_and_routes_to_repair(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Before-transfer blocking check fails (falsification rule violated).
        
        Expected Outcome: BLOCK transition, followed by governed REPAIR under COMMANDER lane.
        """
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_before_fail_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        def strict_quality_check(a: ProgramStateAggregate, contract: Any, candidate: Dict[str, Any]) -> HookResult:
            if candidate.get("audio_quality_score", 0.0) < 0.8:
                return HookResult(
                    phase=HookPhase.BEFORE_TRANSFER,
                    status=HookExecutionStatus.REJECTED,
                    check_name="audio_quality_threshold",
                    message="Audio quality score 0.45 is below required threshold 0.80",
                )
            return HookResult(
                phase=HookPhase.BEFORE_TRANSFER,
                status=HookExecutionStatus.PASSED,
                check_name="audio_quality_threshold",
            )

        lifecycle_coordinator.register_before_transfer_check(strict_quality_check)

        # Attempt transition with poor audio quality
        with pytest.raises(BeforeTransferValidationError) as exc_info:
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="start_elicitation",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {"audio_quality_score": 0.45},
                context=tenant_context,
                context_claims=["workspace_active", "interview_brief_approved"],
            )

        assert exc_info.value.check_name == "audio_quality_threshold"

        # Verify state was NOT committed
        current_agg = state_runtime.get_aggregate(agg.aggregate_id)
        assert current_agg.current_state == "INITIAL"
        assert current_agg.version == 1

        # Operator/Commander executes governed repair routing
        repair_res = lifecycle_coordinator.route_to_repair(
            aggregate_id=agg.aggregate_id,
            fault_reason="Low audio quality detected in elicitation start",
            actor_id="usr_commander_99",
            actor_lane=AuthorityLane.COMMANDER,
        )

        assert repair_res.aggregate.current_state == "REPAIRING"
        assert repair_res.aggregate.lifecycle == ProgramStateLifecycle.REPAIRING
        assert repair_res.aggregate.state_data["repair_reason"] == "Low audio quality detected in elicitation start"
        assert repair_res.receipt["validator_results"]["repair_gate"] == "OPERATOR_AUTHORIZED"

    def test_fault_duplicate_resume_idempotent_replay(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Duplicate resume / retry after successful execution with same idempotency key.
        
        Expected Outcome: IDEMPOTENT_RESUME (returns existing receipt, zero duplicate mutations).
        """
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_idemp_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        work_counter = {"executions": 0}

        def counting_work(a: ProgramStateAggregate) -> Dict[str, Any]:
            work_counter["executions"] += 1
            return {"turn": 1, "payload": "interview_chunk_1"}

        # First execution
        res1 = lifecycle_coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=counting_work,
            context=tenant_context,
            context_claims=["workspace_active", "interview_brief_approved"],
            idempotency_key="idemp_key_turn_1",
        )
        assert work_counter["executions"] == 1
        assert res1.aggregate.version == 2

        # Second execution with identical idempotency key
        res2 = lifecycle_coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=counting_work,
            context=tenant_context,
            context_claims=["workspace_active", "interview_brief_approved"],
            idempotency_key="idemp_key_turn_1",
        )

        # Assert no duplicate mutation occurred
        assert work_counter["executions"] == 1
        assert res2.receipt_id == res1.receipt_id
        assert res2.aggregate.version == 2

    def test_fault_crash_before_effect_settlement_and_checkpoint_resume(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Crash simulated in POST_EFFECT_PRE_RECEIPT window. Checkpoint is preserved.
        
        Expected Outcome: Execution halts, checkpoint is stored, resume executes safely.
        """
        agg = state_runtime.initialize_program_state(
            program_id="collision_discovery_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_crash_sim_001",
            context_claims=["workspace_active", "guest_profile_verified"],
        )

        # Attempt state phase with crash simulation in POST_EFFECT_PRE_RECEIPT window
        with pytest.raises(StateLifecycleError) as exc_info:
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="ingest_corpus",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {"corpus_size_mb": 150},
                context=tenant_context,
                context_claims=["workspace_active", "guest_profile_verified"],
                idempotency_key="idemp_corpus_001",
                simulate_crash_window=FailureWindow.POST_EFFECT_PRE_RECEIPT,
            )

        assert "POST_EFFECT_PRE_RECEIPT" in str(exc_info.value)

        # Verify state aggregate remained at version 1 (uncommitted)
        current_agg = state_runtime.get_aggregate(agg.aggregate_id)
        assert current_agg.current_state == "INITIAL"
        assert current_agg.version == 1

        # Checkpoints exist in coordinator
        assert len(lifecycle_coordinator._checkpoints) == 1
        chkpt_id = list(lifecycle_coordinator._checkpoints.keys())[0]

        # Resume from checkpoint
        resume_res = lifecycle_coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="ingest_corpus",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=lambda a: {"corpus_size_mb": 150},
            context=tenant_context,
            context_claims=["workspace_active", "guest_profile_verified"],
            idempotency_key="idemp_corpus_001",
        )

        assert resume_res.aggregate.current_state == "CORPUS_LOADED"
        assert resume_res.aggregate.version == 2

    def test_fault_uncertain_external_effect_blocks_unsafe_resume(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Resuming from checkpoint with unsettled RECONCILIATION_REQUIRED external effect.
        
        Expected Outcome: FAIL-CLOSED (raises UncertainEffectReconciliationError).
        """
        agg = state_runtime.initialize_program_state(
            program_id="collision_discovery_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_reconcile_001",
            context_claims=["workspace_active", "guest_profile_verified"],
        )

        unsettled_effect = StateEffectDeclaration(
            effect_id="eff_remote_transcode_001",
            effect_kind=EffectKind.EXTERNAL_TOOL,
            replay_safety=ReplaySafety.RECONCILIATION_REQUIRED,
            idempotency_key="idemp_transcode_001",
            settlement_id="settle_pending_001",
            failure_window=FailureWindow.IN_EFFECT,
            settled=False,
        )

        # Attempt state phase with crash simulation and declared unsettled effect
        with pytest.raises(StateLifecycleError):
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="ingest_corpus",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {"corpus_size_mb": 200},
                context=tenant_context,
                context_claims=["workspace_active", "guest_profile_verified"],
                declared_effects=[unsettled_effect],
                simulate_crash_window=FailureWindow.POST_EFFECT_PRE_RECEIPT,
            )

        chkpt_id = list(lifecycle_coordinator._checkpoints.keys())[0]

        # Resuming without reconciliation must raise UncertainEffectReconciliationError
        with pytest.raises(UncertainEffectReconciliationError) as exc_info:
            lifecycle_coordinator.resume_from_checkpoint(
                checkpoint_id=chkpt_id,
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {"corpus_size_mb": 200},
                context=tenant_context,
            )

        assert exc_info.value.reason_code == "UNCERTAIN_EFFECT_RECONCILIATION_REQUIRED"

    def test_fault_authority_lane_violation_blocks_fail_closed(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Actor in HUNTER lane attempts to execute COMMANDER-only approval transition.
        
        Expected Outcome: FAIL-CLOSED (raises ProgramAuthorityLaneViolationError).
        """
        agg = state_runtime.initialize_program_state(
            program_id="collision_discovery_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_lane_viol_001",
            context_claims=["workspace_active", "guest_profile_verified"],
        )

        # Advance to EVALUATED state
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="ingest_corpus",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active", "guest_profile_verified"],
        )
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="hunt_signals",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active"],
        )
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="form_hypothesis",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
        )
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="evaluate_collision",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
        )

        # Hunter attempts operator_approve (which requires COMMANDER lane)
        with pytest.raises(ProgramAuthorityLaneViolationError) as exc_info:
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="operator_approve",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,  # Violating lane!
                work_fn=lambda a: {"approved": True},
                context=tenant_context,
                context_claims=["workspace_active", "operator_confirmed"],
            )

        assert exc_info.value.reason_code == "AUTHORITY_LANE_VIOLATION"

    def test_fault_cross_workspace_leak_attempt_blocks_fail_closed(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        workspace_id: UUID,
    ) -> None:
        """Fault: TenantContext with workspace B attempts to transition aggregate in workspace A.
        
        Expected Outcome: FAIL-CLOSED (raises CrossWorkspaceLeakError).
        """
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id="usr_alpha",
            cae_run_id="run_ws_leak_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        other_workspace_ctx = TenantContext(
            workspace_id=UUID("22222222-2222-2222-2222-222222222222"),
            actor_id="usr_attacker",
            role="OPERATOR",
        )

        with pytest.raises(CrossWorkspaceLeakError) as exc_info:
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="start_elicitation",
                actor_id="usr_attacker",
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {"leak": True},
                context=other_workspace_ctx,
                context_claims=["workspace_active", "interview_brief_approved"],
            )

        assert "CROSS_WORKSPACE_LEAK" in str(exc_info.value)

    def test_fault_terminal_state_transition_attempt_blocks(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Fault: Attempting transition out of a terminal state.
        
        Expected Outcome: BLOCK (raises ProgramTransitionBlockedError).
        """
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_term_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        # Transition all the way to terminal COMPLETED
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active", "interview_brief_approved"],
        )
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="record_turn",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active"],
        )
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="begin_transcription",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
        )
        state_runtime.execute_transition(
            aggregate_id=agg.aggregate_id,
            transition_name="complete_interview",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
        )

        final_agg = state_runtime.get_aggregate(agg.aggregate_id)
        assert final_agg.current_state == "COMPLETED"
        assert final_agg.lifecycle == ProgramStateLifecycle.COMPLETED

        # Attempting any transition on terminal state must raise ProgramTransitionBlockedError
        with pytest.raises(ProgramTransitionBlockedError) as exc_info:
            lifecycle_coordinator.execute_state_phase(
                aggregate_id=agg.aggregate_id,
                transition_name="start_elicitation",
                actor_id=tenant_context.actor_id,
                actor_lane=AuthorityLane.HUNTER,
                work_fn=lambda a: {},
                context=tenant_context,
                context_claims=["workspace_active"],
            )

        assert exc_info.value.reason_code == "TRANSITION_BLOCKED"
        assert "terminal" in str(exc_info.value).lower()

    def test_causal_trace_immutable_hash_chain_and_reconstruction(
        self,
        lifecycle_coordinator: StateLifecycleCoordinator,
        state_runtime: UniversalProgramStateRuntime,
        tenant_context: TenantContext,
        workspace_id: UUID,
    ) -> None:
        """Verifies full cryptographic trace chaining from STATE_ENTERED to COMPLETED."""
        agg = state_runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_trace_chain_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        lifecycle_coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=lambda a: {"elicitation": "active"},
            context=tenant_context,
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        traces = lifecycle_coordinator.trace_ledger.get_traces_for_aggregate(agg.aggregate_id)
        assert len(traces) == 5  # STATE_ENTERED, OPERATION_STARTED, TRANSFER_CHECKED, TRANSFERRED, COMPLETED

        # Verify trace hashing and link validation
        for i, trace in enumerate(traces):
            assert trace.trace_sha256 and len(trace.trace_sha256) == 64
            assert trace.payload_hash and len(trace.payload_hash) == 64
            if i > 0:
                assert trace.previous_trace_sha256 == traces[i - 1].trace_sha256
            else:
                assert trace.previous_trace_sha256 is None

    def test_sqlite_state_store_with_lifecycle_coordinator(
        self,
        tenant_context: TenantContext,
        workspace_id: UUID,
        tmp_path: Path,
    ) -> None:
        """Verifies StateLifecycleCoordinator integration with durable SqliteProgramStateStore."""
        from ca_runtime import SqliteProgramStateStore

        db_path = tmp_path / "lifecycle_test.db"
        store = SqliteProgramStateStore(db_path=db_path)
        runtime = UniversalProgramStateRuntime(store=store)
        coordinator = StateLifecycleCoordinator(state_runtime=runtime)

        agg = runtime.initialize_program_state(
            program_id="interview_semantic_program",
            workspace_id=workspace_id,
            actor_id=tenant_context.actor_id,
            cae_run_id="run_sqlite_001",
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        res = coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="start_elicitation",
            actor_id=tenant_context.actor_id,
            actor_lane=AuthorityLane.HUNTER,
            work_fn=lambda a: {"sqlite_verified": True},
            context=tenant_context,
            context_claims=["workspace_active", "interview_brief_approved"],
        )

        assert res.aggregate.current_state == "QUESTIONING"
        assert res.aggregate.version == 2

        # Reopen sqlite store in a fresh runtime instance
        store2 = SqliteProgramStateStore(db_path=db_path)
        runtime2 = UniversalProgramStateRuntime(store=store2)
        persisted_agg = runtime2.get_aggregate(agg.aggregate_id)

        assert persisted_agg.current_state == "QUESTIONING"
        assert persisted_agg.version == 2
        assert persisted_agg.state_data["sqlite_verified"] is True
