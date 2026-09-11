"""
Unit and Integration Tests for CAE Mandate M61: CAE Software Development Life Cycle Factory.

Validates:
- All 5 Acceptance Gates
- All 3 False-proof/Reward-hacking Defense Vectors (§10)
- End-to-End Real SDLF Repository Execution Trace
- Bounded Repair Loop and Operator Gate Suspension
"""

from typing import List, Tuple
import pytest
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.sdlf_factory import (
    SDLFExecutionRequest,
    SDLFExecutionTrace,
    SDLFFactoryEngine,
    SDLFFactoryError,
    SDLFOperatorShipDeniedError,
    SDLFPhaseExecutionError,
    SDLFPhaseKind,
    SDLFPhaseResult,
    SDLFQualityGateFailedError,
    SDLFRepairExhaustedError,
    SDLFReviewRejectedError,
    SDLFSandboxViolationError,
    build_canonical_sdlf_workflow_ir,
    create_canonical_sdlf_step_contracts,
)
from ca_runtime.step_contracts import StepContractValidator
from ca_runtime.workflow_control_flow import OperatorGrantRecord
from ca_runtime.workflow_ir import WorkflowIRValidator
from ca_runtime.workflow_primitives import WorkUnitKind


# ============================================================================
# Gate 1 & Gate 5: Real SDLF Execution Trace End-to-End
# ============================================================================


def test_gate1_and_gate5_sdlf_end_to_end_execution_trace() -> None:
    """Verify that a complete SDLF request executes end-to-end through all 11 phases."""
    engine = SDLFFactoryEngine()

    request = SDLFExecutionRequest(
        request_id="SDLF_REQ_001",
        title="Add deterministic retry metrics to ca_runtime",
        description="Extend ca_runtime telemetry with retry counters",
        target_workspace="packages/ca_runtime",
        branch_name="feature/retry-metrics",
        authority_lane=AuthorityLane.COMMANDER,
        sandbox_allowed_paths=("packages/ca_runtime/", "docs/"),
    )

    grant = OperatorGrantRecord(
        grant_id="grant_ship_001",
        gate_id="SDLF_SHIP",
        approver_id="lead_operator_1",
        approver_role="lead_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="All quality checks passed, security audit clean",
        granted_at_utc="2026-09-02T05:55:00Z",
    )

    trace = engine.run(request, operator_ship_grant=grant)

    assert trace.final_status == "COMPLETED"
    assert trace.operator_ship_granted
    assert len(trace.phase_results) == 10  # 10 phases in happy path (no repair needed)
    assert len(trace.trace_sha256) == 64

    # Verify all phase kinds are in chronological order
    phase_order = [r.phase_kind for r in trace.phase_results]
    expected_order = [
        SDLFPhaseKind.INTAKE,
        SDLFPhaseKind.SCOUT,
        SDLFPhaseKind.PLAN,
        SDLFPhaseKind.BUILD,
        SDLFPhaseKind.QUALITY,
        SDLFPhaseKind.REVIEW,
        SDLFPhaseKind.DOCUMENT,
        SDLFPhaseKind.INTEGRATE,
        SDLFPhaseKind.SHIP,
        SDLFPhaseKind.OBSERVE,
    ]
    assert phase_order == expected_order


# ============================================================================
# Gate 2 & Gate 3: Deterministic Quality & Typed Agent Envelopes
# ============================================================================


def test_gate2_and_gate3_deterministic_quality_and_typed_agent_envelopes() -> None:
    """Verify that QUALITY phase executes deterministic code runner and agent phases produce typed envelopes."""
    engine = SDLFFactoryEngine()

    test_executed = False

    def custom_code_test_runner() -> Tuple[bool, List[str]]:
        nonlocal test_executed
        test_executed = True
        return True, []

    request = SDLFExecutionRequest(
        request_id="SDLF_REQ_002",
        title="Code Quality Verification",
        description="Verify deterministic code runner",
        target_workspace="packages/ca_runtime",
        branch_name="feature/quality-test",
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )

    grant = OperatorGrantRecord(
        grant_id="grant_ship_002",
        gate_id="SDLF_SHIP",
        approver_id="lead_operator_1",
        approver_role="lead_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="Approved",
        granted_at_utc="2026-09-02T05:55:00Z",
    )

    trace = engine.run(request, operator_ship_grant=grant, deterministic_test_runner=custom_code_test_runner)

    assert test_executed  # Proves deterministic code runner was invoked!

    # Verify typed agent results
    for r in trace.phase_results:
        assert isinstance(r.outputs, dict)
        assert len(r.receipt_sha256) == 64
        if r.phase_kind in {SDLFPhaseKind.SCOUT, SDLFPhaseKind.PLAN, SDLFPhaseKind.BUILD, SDLFPhaseKind.REVIEW, SDLFPhaseKind.DOCUMENT}:
            assert r.work_unit_kind == WorkUnitKind.AGENT_CALL
        else:
            assert r.work_unit_kind == WorkUnitKind.CODE_FUNCTION


# ============================================================================
# Gate 4: Review Rejection and Bounded Repair
# ============================================================================


def test_gate4_review_rejection_routes_to_bounded_repair() -> None:
    """Verify that failing code tests trigger Review rejection and bounded repair cycle."""
    engine = SDLFFactoryEngine()

    run_count = 0

    def failing_then_passing_runner() -> Tuple[bool, List[str]]:
        nonlocal run_count
        run_count += 1
        if run_count == 1:
            return False, ["AssertionError: expected 42, got 0"]
        return True, []

    request = SDLFExecutionRequest(
        request_id="SDLF_REQ_REPAIR",
        title="Repair Verification Request",
        description="Test repair cycle on test failure",
        target_workspace="packages/ca_runtime",
        branch_name="feature/repair-test",
        max_repair_retries=2,
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )

    grant = OperatorGrantRecord(
        grant_id="grant_ship_repair",
        gate_id="SDLF_SHIP",
        approver_id="lead_operator_1",
        approver_role="lead_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="Approved after repair",
        granted_at_utc="2026-09-02T05:55:00Z",
    )

    trace = engine.run(request, operator_ship_grant=grant, deterministic_test_runner=failing_then_passing_runner)

    assert trace.final_status == "REPAIRED_AND_COMPLETED"
    assert trace.repair_attempts_count == 1
    # Check that REPAIR phase is present in trace
    repair_phases = [r for r in trace.phase_results if r.phase_kind == SDLFPhaseKind.REPAIR]
    assert len(repair_phases) == 1
    assert repair_phases[0].outputs["repair_attempt"] == 1


# ============================================================================
# False-Proof & Reward-Hacking Defenses (§10)
# ============================================================================


def test_false_proof_1_quality_phase_cannot_claim_pass_when_code_tests_fail() -> None:
    """False-proof 1: QUALITY phase cannot use model narrative to pass when code tests fail."""
    engine = SDLFFactoryEngine()

    def constantly_failing_runner() -> Tuple[bool, List[str]]:
        return False, ["SyntaxError: invalid syntax in compiled module"]

    request = SDLFExecutionRequest(
        request_id="SDLF_REQ_FAIL_QUALITY",
        title="Defective Code Request",
        description="Failing tests",
        target_workspace="packages/ca_runtime",
        branch_name="feature/failing-tests",
        max_repair_retries=2,
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )

    with pytest.raises(SDLFRepairExhaustedError) as exc_info:
        engine.run(request, deterministic_test_runner=constantly_failing_runner)
    assert exc_info.value.reason_code == "ERR_SDLF_REPAIR_EXHAUSTED"


def test_false_proof_2_build_outside_sandbox_rejected() -> None:
    """False-proof 2: BUILD phase attempting to modify files outside sandbox is rejected."""
    engine = SDLFFactoryEngine()

    request = SDLFExecutionRequest(
        request_id="SDLF_REQ_SANDBOX_VIOLATION",
        title="Escape Sandbox Request",
        description="Testing sandbox constraint",
        target_workspace="packages/ca_runtime",
        branch_name="feature/escape-sandbox",
        sandbox_allowed_paths=("packages/ca_runtime/isolated_submodule/",),  # Narrow sandbox
    )

    with pytest.raises(SDLFSandboxViolationError) as exc_info:
        engine.run(request)
    assert exc_info.value.reason_code == "ERR_SDLF_SANDBOX_VIOLATION"


def test_false_proof_3_ship_without_commander_grant_suspends() -> None:
    """False-proof 3: SHIP phase without valid COMMANDER grant suspends execution."""
    engine = SDLFFactoryEngine()

    request = SDLFExecutionRequest(
        request_id="SDLF_REQ_UNAUTHORIZED_SHIP",
        title="Unauthorized Ship Request",
        description="Testing ship suspension",
        target_workspace="packages/ca_runtime",
        branch_name="feature/unauthorized-ship",
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )

    # Run without grant
    trace = engine.run(request, operator_ship_grant=None)
    assert trace.final_status == "SUSPENDED"
    assert not trace.operator_ship_granted

    # Run with unauthorized lane grant (e.g. ANALYST)
    analyst_grant = OperatorGrantRecord(
        grant_id="grant_analyst",
        gate_id="SDLF_SHIP",
        approver_id="analyst_1",
        approver_role="analyst",
        authority_lane=AuthorityLane.ANALYST,  # Illegal!
        decision="APPROVED",
        rationale="Bypassing commander",
        granted_at_utc="2026-09-02T05:55:00Z",
    )
    trace_lane = engine.run(request, operator_ship_grant=analyst_grant)
    assert trace_lane.final_status == "SUSPENDED"
    assert not trace_lane.operator_ship_granted


# ============================================================================
# SDLF Workflow IR & Step Contracts Validation
# ============================================================================


def test_canonical_sdlf_workflow_ir_and_step_contracts() -> None:
    """Verify canonical SDLF workflow IR compilation and all step contracts."""
    # 1. Validate Workflow IR
    ir = build_canonical_sdlf_workflow_ir()
    WorkflowIRValidator.validate_ir(ir)
    assert len(ir.nodes) == 10
    assert len(ir.edges) == 9

    # 2. Validate all 10 step contracts
    contracts = create_canonical_sdlf_step_contracts()
    assert len(contracts) == 10
    for c in contracts:
        StepContractValidator.validate_contract(c)
        assert c.verify_integrity()
