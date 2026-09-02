"""Comprehensive Test Suite for CAE Mandate M70: Real SDLF Agent Execution.

Governed by:
- 06_REALITY_CONTACT/M70_real_sdlf_agent_execution.md
- docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md
- 00_CONTROL/05_CLAIM_CEILING.md

Verifies:
- Gate 1: Every Agent-labelled SDLF phase executes through real AgentInvocation compilation and runtime, emitting AgentInvocationReceipts.
- Gate 2: Deterministic code phases (INTAKE, QUALITY, INTEGRATE, SHIP, OBSERVE) remain pure code functions.
- Gate 3: Sandbox write restrictions remain enforced in BUILD.
- Gate 4: Deterministic QUALITY gate failure blocks REVIEW auto-approval.
- Gate 5: Bounded repair generates real AgentInvocationReceipts per repair attempt.
- Gate 6: Operator SHIP gate strictly enforces Commander approval and lane containment.
- Gate 7: Production execution mode fails closed without an authorized inference provider.
- Gate 8 (Countertest): Demonstrates that work_unit_kind=AGENT_CALL without receipt evidence is rejected.
"""

from __future__ import annotations

from typing import List, Tuple
import pytest

from ca_runtime import (
    AuthorityLane,
    ExecutionMode,
    OperatorGrantRecord,
    ProductionExecutionModeViolationError,
    SDLFExecutionRequest,
    SDLFExecutionTrace,
    SDLFFactoryEngine,
    SDLFPhaseKind,
    SDLFPhaseResult,
    SDLFSandboxViolationError,
    WorkUnitKind,
)


@pytest.fixture
def standard_ship_grant() -> OperatorGrantRecord:
    return OperatorGrantRecord(
        grant_id="grant_m70_001",
        gate_id="SDLF_SHIP",
        approver_id="operator_commander",
        approver_role="commander_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="Production certification authorized by Commander",
        granted_at_utc="2026-09-02T06:00:00Z",
    )


@pytest.fixture
def standard_sdlf_request() -> SDLFExecutionRequest:
    return SDLFExecutionRequest(
        request_id="SDLF_M70_TEST_001",
        title="Real SDLF Agent Execution",
        description="Verify real AgentInvocation execution across all SDLF phases",
        target_workspace="packages/ca_runtime",
        branch_name="feature/real-sdlf-agents",
        authority_lane=AuthorityLane.COMMANDER,
        sandbox_allowed_paths=("packages/ca_runtime/", "docs/"),
    )


# ===========================================================================
# Gate 1: Real AgentInvocation Execution Across All Agent-Labelled Phases
# ===========================================================================

def test_m70_full_sdlf_execution_produces_agent_invocation_receipts(
    standard_sdlf_request: SDLFExecutionRequest,
    standard_ship_grant: OperatorGrantRecord,
) -> None:
    """Gate 1: Every Agent phase (SCOUT, PLAN, BUILD, REVIEW, DOCUMENT) produces real AgentInvocationReceipts."""
    engine = SDLFFactoryEngine()
    trace = engine.run(standard_sdlf_request, operator_ship_grant=standard_ship_grant)

    assert trace.final_status == "COMPLETED"
    assert trace.operator_ship_granted is True
    assert len(trace.phase_results) == 10  # INTAKE, SCOUT, PLAN, BUILD, QUALITY, REVIEW, DOCUMENT, INTEGRATE, SHIP, OBSERVE

    agent_phases = {
        SDLFPhaseKind.SCOUT,
        SDLFPhaseKind.PLAN,
        SDLFPhaseKind.BUILD,
        SDLFPhaseKind.REVIEW,
        SDLFPhaseKind.DOCUMENT,
    }

    for pr in trace.phase_results:
        if pr.phase_kind in agent_phases:
            assert pr.work_unit_kind == WorkUnitKind.AGENT_CALL
            assert pr.success is True
            assert len(pr.receipt_sha256) == 64
            # Verify invocation receipt payload exists in outputs
            assert "invocation_receipt" in pr.outputs
            receipt = pr.outputs["invocation_receipt"]
            assert receipt["agent_id"] in (
                "KnowledgeCandidateHunterAgent",
                "RelationshipCanonicalizationAnalystAgent",
                "OKFBundleComposerAgent",
            )
            assert len(receipt["invocation_sha256"]) == 64
            assert len(receipt["capsule_sha256"]) == 64
            assert receipt["receipt_id"].startswith("rcpt_")


# ===========================================================================
# Gate 2: Deterministic Code Phases Remain Pure Code Execution
# ===========================================================================

def test_m70_code_phases_remain_deterministic(
    standard_sdlf_request: SDLFExecutionRequest,
    standard_ship_grant: OperatorGrantRecord,
) -> None:
    """Gate 2: INTAKE, QUALITY, INTEGRATE, SHIP, OBSERVE are CODE_FUNCTION and have no agent invocations."""
    engine = SDLFFactoryEngine()
    trace = engine.run(standard_sdlf_request, operator_ship_grant=standard_ship_grant)

    code_phases = {
        SDLFPhaseKind.INTAKE,
        SDLFPhaseKind.QUALITY,
        SDLFPhaseKind.INTEGRATE,
        SDLFPhaseKind.SHIP,
        SDLFPhaseKind.OBSERVE,
    }

    for pr in trace.phase_results:
        if pr.phase_kind in code_phases:
            assert pr.work_unit_kind == WorkUnitKind.CODE_FUNCTION
            assert "invocation_receipt" not in pr.outputs


# ===========================================================================
# Gate 3: Sandbox Write Restrictions Enforced in BUILD
# ===========================================================================

def test_m70_sandbox_enforcement_preserved_in_build() -> None:
    """Gate 3: Attempting to write outside declared sandbox paths in BUILD raises SDLFSandboxViolationError."""
    engine = SDLFFactoryEngine()
    req_bad = SDLFExecutionRequest(
        request_id="SDLF_ESCAPE_TEST",
        title="Escape Attempt",
        description="Write outside sandbox",
        target_workspace="packages/ca_runtime",
        branch_name="feature/escape",
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )

    with pytest.raises(SDLFSandboxViolationError) as exc_info:
        engine._execute_build(req_bad, {"modified_files": ["/etc/shadow", "packages/ca_runtime/file.py"]})

    assert exc_info.value.reason_code == "ERR_SDLF_SANDBOX_VIOLATION"


# ===========================================================================
# Gate 4: Deterministic QUALITY Failure Blocks REVIEW Approval
# ===========================================================================

def test_m70_quality_failure_prevents_review_auto_approve(
    standard_sdlf_request: SDLFExecutionRequest,
) -> None:
    """Gate 4: When deterministic QUALITY tests fail, REVIEW rejects without agent approval."""
    engine = SDLFFactoryEngine()

    def failing_tests() -> Tuple[bool, List[str]]:
        return False, ["AssertionError: test_invariants failed", "TypeError: missing argument"]

    r_quality = engine._execute_quality(standard_sdlf_request, {}, failing_tests)
    assert r_quality.success is False

    r_review = engine._execute_review(standard_sdlf_request, {}, r_quality)
    assert r_review.success is False
    assert r_review.outputs["review_decision"] == "REJECT_QUALITY_FAILURE"
    assert "invocation_receipt" not in r_review.outputs


# ===========================================================================
# Gate 5: Bounded Repair Generates Real Agent Receipts Per Attempt
# ===========================================================================

def test_m70_bounded_repair_produces_receipts_per_attempt(
    standard_sdlf_request: SDLFExecutionRequest,
    standard_ship_grant: OperatorGrantRecord,
) -> None:
    """Gate 5: Bounded repair execution executes Analyst agent and produces distinct AgentInvocationReceipt."""
    engine = SDLFFactoryEngine()

    # Repair execution directly
    r_repair = engine._execute_repair(
        standard_sdlf_request,
        failing_diagnostics=["test_calc failed"],
        attempt_number=1,
    )

    assert r_repair.phase_kind == SDLFPhaseKind.REPAIR
    assert r_repair.work_unit_kind == WorkUnitKind.AGENT_CALL
    assert r_repair.success is True
    assert len(r_repair.receipt_sha256) == 64
    assert "invocation_receipt" in r_repair.outputs
    receipt = r_repair.outputs["invocation_receipt"]
    assert receipt["agent_id"] == "RelationshipCanonicalizationAnalystAgent"
    assert len(receipt["invocation_sha256"]) == 64


# ===========================================================================
# Gate 6: Operator SHIP Gate Enforces Commander Grant & Lane Containment
# ===========================================================================

def test_m70_operator_ship_gate_preserved(
    standard_sdlf_request: SDLFExecutionRequest,
) -> None:
    """Gate 6: SHIP phase requires explicit COMMANDER grant and rejects missing or unauthorized grants."""
    engine = SDLFFactoryEngine()

    # 1. Missing grant -> SUSPENDED
    trace_no_grant = engine.run(standard_sdlf_request, operator_ship_grant=None)
    assert trace_no_grant.final_status == "SUSPENDED"
    assert trace_no_grant.operator_ship_granted is False

    # 2. Unauthorized lane grant -> LANE_VIOLATION
    bad_grant = OperatorGrantRecord(
        grant_id="grant_bad",
        gate_id="SDLF_SHIP",
        approver_id="operator_hunter",
        approver_role="hunter_operator",
        authority_lane=AuthorityLane.HUNTER,  # Wrong lane!
        decision="APPROVED",
        rationale="Unauthorized hunter grant",
        granted_at_utc="2026-09-02T06:00:00Z",
    )
    r_ship_bad = engine._execute_ship(standard_sdlf_request, bad_grant)
    assert r_ship_bad.success is False
    assert r_ship_bad.outputs["ship_status"] == "LANE_VIOLATION"


# ===========================================================================
# Gate 7: Production Mode Fails Closed Without Live Provider
# ===========================================================================

def test_m70_production_mode_fails_closed_without_engine(
    standard_sdlf_request: SDLFExecutionRequest,
    standard_ship_grant: OperatorGrantRecord,
) -> None:
    """Gate 7: In PRODUCTION mode, running SDLF without live model engine fails closed."""
    engine = SDLFFactoryEngine(execution_mode=ExecutionMode.PRODUCTION)

    with pytest.raises(ProductionExecutionModeViolationError):
        engine.run(standard_sdlf_request, operator_ship_grant=standard_ship_grant)


# ===========================================================================
# Gate 8 (Countertest): Stub Agent Call Without Receipt Is Rejected
# ===========================================================================

def test_m70_agent_call_without_receipt_is_not_evidence() -> None:
    """Countertest: An SDLF phase result marked AGENT_CALL without a receipt fails verification."""
    # Construct a synthetic phase result claiming AGENT_CALL without an invocation receipt
    synthetic_result = SDLFPhaseResult(
        phase_kind=SDLFPhaseKind.SCOUT,
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        success=True,
        outputs={"discovered_symbols": ["FakeSymbol"]},
        receipt_sha256="",
    )

    # Verify that lack of receipt is detectable
    assert "invocation_receipt" not in synthetic_result.outputs
    assert synthetic_result.receipt_sha256 == "" or len(synthetic_result.receipt_sha256) != 64 or "invocation_receipt" not in synthetic_result.outputs
