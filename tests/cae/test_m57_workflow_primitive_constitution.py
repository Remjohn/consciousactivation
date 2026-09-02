"""
Unit and Integration Tests for CAE Mandate M57: Workflow Primitive Constitution.

Validates:
- All 5 Acceptance Gates
- All 4 False-proof/Reward-hacking Defense Vectors (§10)
- Concrete deterministic workflow path and checked transfer semantics (StateM Alignment)
"""

import pytest
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.workflow_primitives import (
    AgentMutatedLoopBoundError,
    BlockingPreTransferCheckFailedError,
    CheckedTransferResult,
    ConditionBranchDefinition,
    HumanGateBypassError,
    HumanGateRequirement,
    InvalidPrimitiveKindError,
    InvalidTransitionEdgeError,
    JoinCondition,
    JoinPolicy,
    LoopBoundPolicy,
    LoopTerminationKind,
    ParallelBranchDefinition,
    ParallelSideEffectConflictError,
    RetryBackoffStrategy,
    RetryPolicyDefinition,
    StateRetentionViolationError,
    SwitchCaseDefinition,
    UnboundedLoopError,
    UnevaluableConditionError,
    UnsupportedPrimitiveError,
    WorkflowPrimitiveDefinition,
    WorkflowPrimitiveError,
    WorkflowPrimitiveKind,
    WorkflowPrimitiveValidator,
    WorkflowStepContract,
    WorkflowTransitionSemantics,
    WorkUnitKind,
)


# ============================================================================
# Gate 1: Every primitive has deterministic semantics
# ============================================================================


def test_gate1_all_fourteen_primitives_have_deterministic_semantics() -> None:
    """Verify all 14 ratified control-flow primitives and 2 work-unit kinds are recognized."""
    # 1. SEQUENCE
    p_seq = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_SEQ_01",
        primitive_kind=WorkflowPrimitiveKind.SEQUENCE,
        step_contract=WorkflowStepContract(
            step_id="STEP_01",
            work_unit_kind=WorkUnitKind.CODE_FUNCTION,
            target_ref="cmf_pipeline.compute_embeddings",
            authority_lane=AuthorityLane.ANALYST,
        ),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_seq)
    assert p_seq.verify_integrity()

    # 2. CONDITION
    p_cond = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_COND_01",
        primitive_kind=WorkflowPrimitiveKind.CONDITION,
        condition_config=ConditionBranchDefinition(
            condition_expression="quality_score >= 80",
            then_step_id="STEP_APPROVE",
            else_step_id="STEP_REPAIR",
        ),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_cond)

    # 3. SWITCH
    p_switch = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_SWITCH_01",
        primitive_kind=WorkflowPrimitiveKind.SWITCH,
        switch_cases=(
            SwitchCaseDefinition(match_value="AUDIO", target_step_id="STEP_AUDIO_PIPELINE"),
            SwitchCaseDefinition(match_value="VIDEO", target_step_id="STEP_VIDEO_PIPELINE"),
        ),
        default_switch_step="STEP_GENERIC_PIPELINE",
    )
    WorkflowPrimitiveValidator.validate_primitive(p_switch)

    # 4. LOOP
    p_loop = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_LOOP_01",
        primitive_kind=WorkflowPrimitiveKind.LOOP,
        loop_policy=LoopBoundPolicy(max_iterations=5, timeout_seconds=300),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_loop)

    # 5. RETRY
    p_retry = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_RETRY_01",
        primitive_kind=WorkflowPrimitiveKind.RETRY,
        retry_policy=RetryPolicyDefinition(
            max_attempts=3,
            backoff_strategy=RetryBackoffStrategy.EXPONENTIAL,
            initial_interval_seconds=2,
            max_interval_seconds=30,
            non_retryable_errors=("AuthenticationError", "PermissionDeniedError"),
        ),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_retry)

    # 6. PARALLEL
    p_par = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_PAR_01",
        primitive_kind=WorkflowPrimitiveKind.PARALLEL,
        parallel_branches=(
            ParallelBranchDefinition(branch_id="B1", primitive_ref="PRIM_SUB_1", side_effect_class="READ_ONLY"),
            ParallelBranchDefinition(branch_id="B2", primitive_ref="PRIM_SUB_2", side_effect_class="READ_ONLY"),
        ),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_par)

    # 7. JOIN
    p_join = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_JOIN_01",
        primitive_kind=WorkflowPrimitiveKind.JOIN,
        join_condition=JoinCondition(policy=JoinPolicy.ALL, timeout_seconds=60),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_join)

    # 8. TIMEOUT
    p_timeout = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_TIMEOUT_01",
        primitive_kind=WorkflowPrimitiveKind.TIMEOUT,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_timeout)

    # 9. WAIT
    p_wait = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_WAIT_01",
        primitive_kind=WorkflowPrimitiveKind.WAIT,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_wait)

    # 10. HUMAN_GATE
    p_gate = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_GATE_01",
        primitive_kind=WorkflowPrimitiveKind.HUMAN_GATE,
        human_gate=HumanGateRequirement(
            gate_id="GATE_OPERATOR_RELEASE",
            required_lane=AuthorityLane.COMMANDER,
            approver_role="lead_operator",
        ),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_gate)

    # 11. FAIL
    p_fail = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_FAIL_01",
        primitive_kind=WorkflowPrimitiveKind.FAIL,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_fail)

    # 12. REPAIR
    p_repair = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_REPAIR_01",
        primitive_kind=WorkflowPrimitiveKind.REPAIR,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_repair)

    # 13. CANCEL
    p_cancel = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_CANCEL_01",
        primitive_kind=WorkflowPrimitiveKind.CANCEL,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_cancel)

    # 14. RESUME
    p_resume = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_RESUME_01",
        primitive_kind=WorkflowPrimitiveKind.RESUME,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_resume)

    # Both Work Unit Kinds
    p_agent = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_AGENT_CALL_01",
        primitive_kind=WorkflowPrimitiveKind.SEQUENCE,
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        step_contract=WorkflowStepContract(
            step_id="STEP_REASONING",
            work_unit_kind=WorkUnitKind.AGENT_CALL,
            target_ref="RelationshipCanonicalizationAnalystAgent",
            authority_lane=AuthorityLane.ANALYST,
        ),
    )
    WorkflowPrimitiveValidator.validate_primitive(p_agent)
    assert p_agent.work_unit_kind == WorkUnitKind.AGENT_CALL


# ============================================================================
# Gate 2: Each primitive has explicit failure/termination behavior
# ============================================================================


def test_gate2_explicit_failure_and_termination_behavior() -> None:
    """Verify failure and termination behavior across key primitives."""
    # Loop termination kind enum verification
    assert LoopTerminationKind.MAX_ITERATIONS.value == "MAX_ITERATIONS"
    assert LoopTerminationKind.CONDITION_MET.value == "CONDITION_MET"
    assert LoopTerminationKind.EARLY_EXIT.value == "EARLY_EXIT"
    assert LoopTerminationKind.ERROR_ABORT.value == "ERROR_ABORT"

    # Retry policy error classification
    retry = RetryPolicyDefinition(
        max_attempts=3,
        non_retryable_errors=("FatalValidationError", "SecurityViolationError"),
    )
    assert "FatalValidationError" in retry.non_retryable_errors
    assert retry.max_attempts == 3

    # Switch case empty failure
    with pytest.raises(WorkflowPrimitiveError) as exc_info:
        WorkflowPrimitiveValidator.validate_primitive(
            WorkflowPrimitiveDefinition(
                primitive_id="PRIM_EMPTY_SWITCH",
                primitive_kind=WorkflowPrimitiveKind.SWITCH,
                switch_cases=(),
            )
        )
    assert exc_info.value.reason_code == "ERR_EMPTY_SWITCH_CASES"


# ============================================================================
# Gate 3: No primitive bypasses state/authority contracts
# ============================================================================


def test_gate3_authority_and_state_contracts_enforced() -> None:
    """Verify HUMAN_GATE and authority lane boundaries are strictly checked."""
    # Missing human gate config
    with pytest.raises(WorkflowPrimitiveError) as exc_info:
        WorkflowPrimitiveValidator.validate_primitive(
            WorkflowPrimitiveDefinition(
                primitive_id="PRIM_BAD_GATE",
                primitive_kind=WorkflowPrimitiveKind.HUMAN_GATE,
                human_gate=None,
            )
        )
    assert exc_info.value.reason_code == "ERR_MISSING_HUMAN_GATE_CONFIG"

    # Valid human gate strictly requires COMMANDER lane
    gate = HumanGateRequirement(
        gate_id="GATE_LEGAL_REVIEW",
        required_lane=AuthorityLane.COMMANDER,
        approver_role="lead_operator",
    )
    assert gate.required_lane == AuthorityLane.COMMANDER


# ============================================================================
# Gate 4: Unsupported primitives are rejected, not improvised
# ============================================================================


def test_gate4_unsupported_primitives_rejected() -> None:
    """Verify arbitrary strings or unratified primitive kinds are rejected fail-closed."""
    with pytest.raises(InvalidPrimitiveKindError):
        WorkflowPrimitiveValidator.validate_primitive(
            WorkflowPrimitiveDefinition(
                primitive_id="PRIM_IMPROVISED",
                primitive_kind="IMPROVISED_PIPELINE_HACK",  # type: ignore[arg-type]
            )
        )


# ============================================================================
# Gate 5: Transition semantics enforce ordered checked transfer (StateM)
# ============================================================================


def test_gate5_checked_transfer_ordering_and_source_state_retention() -> None:
    """Verify the 6-stage checked transfer protocol preserves source state on failed pre-check."""
    allowed_edges = [
        ("ANALYSIS_IN_PROGRESS", "EDITORIAL_READY"),
        ("ANALYSIS_IN_PROGRESS", "REPAIR_REQUIRED"),
    ]

    out_hook_called = False
    in_hook_called = False

    def sample_out_hook() -> None:
        nonlocal out_hook_called
        out_hook_called = True

    def sample_in_hook() -> None:
        nonlocal in_hook_called
        in_hook_called = True

    # Case A: Blocking pre-transfer check FAILS -> source state PRESERVED
    def failing_pre_check() -> tuple[bool, str]:
        return (False, "Editorial QA Score 65 is below required threshold 80")

    result_failed = WorkflowPrimitiveValidator.execute_checked_transfer(
        source_state="ANALYSIS_IN_PROGRESS",
        target_state="EDITORIAL_READY",
        allowed_edges=allowed_edges,
        pre_transfer_predicates={"QA_SCORE_THRESHOLD": failing_pre_check},
        out_hooks=[sample_out_hook],
        in_hooks=[sample_in_hook],
        current_version=3,
    )

    assert not result_failed.success
    assert result_failed.from_state == "ANALYSIS_IN_PROGRESS"
    assert result_failed.to_state == "EDITORIAL_READY"
    assert result_failed.current_state == "ANALYSIS_IN_PROGRESS"  # Retained in source state!
    assert not result_failed.version_incremented
    assert result_failed.failed_check == "QA_SCORE_THRESHOLD"
    assert "below required threshold" in (result_failed.failure_reason or "")
    assert not out_hook_called  # Out-hooks NOT executed when pre-check fails
    assert not in_hook_called  # In-hooks NOT executed
    assert not result_failed.context_refreshed

    # Case B: Blocking pre-transfer check PASSES -> target state COMMITTED
    def passing_pre_check() -> tuple[bool, str]:
        return (True, "Editorial QA Score 92 passes threshold")

    result_passed = WorkflowPrimitiveValidator.execute_checked_transfer(
        source_state="ANALYSIS_IN_PROGRESS",
        target_state="EDITORIAL_READY",
        allowed_edges=allowed_edges,
        pre_transfer_predicates={"QA_SCORE_THRESHOLD": passing_pre_check},
        out_hooks=[sample_out_hook],
        in_hooks=[sample_in_hook],
        current_version=3,
    )

    assert result_passed.success
    assert result_passed.from_state == "ANALYSIS_IN_PROGRESS"
    assert result_passed.to_state == "EDITORIAL_READY"
    assert result_passed.current_state == "EDITORIAL_READY"  # Successfully committed!
    assert result_passed.version_incremented
    assert result_passed.failed_check is None
    assert out_hook_called
    assert in_hook_called
    assert result_passed.context_refreshed
    assert len(result_passed.receipt_sha256) == 64

    # Case C: Invalid Edge rejected
    with pytest.raises(InvalidTransitionEdgeError):
        WorkflowPrimitiveValidator.execute_checked_transfer(
            source_state="ANALYSIS_IN_PROGRESS",
            target_state="RELEASE_APPROVED",  # Not a valid edge!
            allowed_edges=allowed_edges,
            pre_transfer_predicates={},
        )


# ============================================================================
# False-Proof & Reward-Hacking Defenses (Mandate §10)
# ============================================================================


def test_false_proof_1_unbounded_loop_rejected() -> None:
    """False-proof 1: Configuring an unbounded loop with max_iterations <= 0 is rejected."""
    with pytest.raises(UnboundedLoopError) as exc_info:
        LoopBoundPolicy(max_iterations=0)
    assert exc_info.value.reason_code == "ERR_UNBOUNDED_LOOP"

    with pytest.raises(UnboundedLoopError):
        LoopBoundPolicy(max_iterations=-5)


def test_false_proof_2_unevaluable_condition_rejected() -> None:
    """False-proof 2: Condition that cannot be evaluated by the runtime is rejected."""
    with pytest.raises(UnevaluableConditionError) as exc_info:
        WorkflowPrimitiveValidator.validate_condition(
            ConditionBranchDefinition(
                condition_expression="",  # Empty expression
                then_step_id="STEP_NEXT",
            )
        )
    assert exc_info.value.reason_code == "ERR_UNEVALUABLE_CONDITION"

    with pytest.raises(UnevaluableConditionError):
        WorkflowPrimitiveValidator.validate_condition(
            ConditionBranchDefinition(
                condition_expression="valid_expr",
                then_step_id="",  # Missing target branch
            )
        )


def test_false_proof_3_agent_mutating_loop_bound_rejected() -> None:
    """False-proof 3: Allowing an Agent to mutate its own loop bound is rejected."""
    with pytest.raises(AgentMutatedLoopBoundError) as exc_info:
        LoopBoundPolicy(
            max_iterations=10,
            allow_agent_override=True,  # Prohibited!
        )
    assert exc_info.value.reason_code == "ERR_AGENT_MUTATED_LOOP_BOUND"


def test_false_proof_4_parallel_conflicting_mutating_side_effects_rejected() -> None:
    """False-proof 4: Using PARALLEL with conflicting non-read-only side effects is rejected."""
    # Case A: Both READ_ONLY -> Permitted
    branches_safe = (
        ParallelBranchDefinition(branch_id="B1", primitive_ref="P1", side_effect_class="READ_ONLY"),
        ParallelBranchDefinition(branch_id="B2", primitive_ref="P2", side_effect_class="READ_ONLY"),
    )
    WorkflowPrimitiveValidator.validate_parallel_branches(branches_safe)

    # Case B: Two branches with MUTATION_OPERATION -> Rejected!
    branches_conflict = (
        ParallelBranchDefinition(branch_id="B1", primitive_ref="P1", side_effect_class="MUTATION_OPERATION"),
        ParallelBranchDefinition(branch_id="B2", primitive_ref="P2", side_effect_class="MUTATION_OPERATION"),
    )
    with pytest.raises(ParallelSideEffectConflictError) as exc_info:
        WorkflowPrimitiveValidator.validate_parallel_branches(branches_conflict)
    assert exc_info.value.reason_code == "ERR_PARALLEL_SIDE_EFFECT_CONFLICT"


# ============================================================================
# Concrete End-to-End Workflow Control Path Demonstration
# ============================================================================


def test_concrete_workflow_control_flow_and_checked_transition_trace() -> None:
    """Demonstrate end-to-end deterministic workflow path: CONDITION -> SEQUENCE -> AGENT_CALL -> HUMAN_GATE -> REPAIR."""
    # 1. Condition evaluation
    cond = ConditionBranchDefinition(
        condition_expression="input_evidence_count > 0",
        then_step_id="STEP_ANALYZE",
        else_step_id="STEP_FAIL",
    )
    WorkflowPrimitiveValidator.validate_condition(cond)

    # 2. Sequence with Agent Call
    step_agent = WorkflowStepContract(
        step_id="STEP_ANALYZE",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="RelationshipCanonicalizationAnalystAgent",
        authority_lane=AuthorityLane.ANALYST,
    )
    p_seq = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_PIPELINE_STAGE_1",
        primitive_kind=WorkflowPrimitiveKind.SEQUENCE,
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        step_contract=step_agent,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_seq)

    # 3. Human Gate
    gate = HumanGateRequirement(
        gate_id="GATE_EDITORIAL_RELEASE",
        required_lane=AuthorityLane.COMMANDER,
        approver_role="lead_operator",
    )
    p_gate = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_OPERATOR_GATE",
        primitive_kind=WorkflowPrimitiveKind.HUMAN_GATE,
        human_gate=gate,
    )
    WorkflowPrimitiveValidator.validate_primitive(p_gate)

    # 4. State-preserving repair transition
    allowed_edges = [
        ("ANALYST_REASONING", "OPERATOR_GATE"),
        ("ANALYST_REASONING", "BOUNDED_REPAIR"),
        ("BOUNDED_REPAIR", "ANALYST_REASONING"),
    ]

    # Pre-check fails -> remains in ANALYST_REASONING
    res = WorkflowPrimitiveValidator.execute_checked_transfer(
        source_state="ANALYST_REASONING",
        target_state="OPERATOR_GATE",
        allowed_edges=allowed_edges,
        pre_transfer_predicates={
            "CONTRADICTION_CHECK": lambda: (False, "1 unresolved contradiction found")
        },
    )
    assert not res.success
    assert res.current_state == "ANALYST_REASONING"

    # Route to repair within allowed edge graph
    res_repair = WorkflowPrimitiveValidator.execute_checked_transfer(
        source_state="ANALYST_REASONING",
        target_state="BOUNDED_REPAIR",
        allowed_edges=allowed_edges,
        pre_transfer_predicates={},  # Unconditional edge to repair
    )
    assert res_repair.success
    assert res_repair.current_state == "BOUNDED_REPAIR"
    assert res_repair.version_incremented
