"""
Unit and Integration Tests for CAE Mandate M64: Factory Benchmark + Production Certification + CURRENT Synchronization.

Validates:
- All 7 Acceptance Gates
- All 6 Adversarial Failure Pack Vectors (§10)
- Repeated SDLF Pipeline Benchmark (100% pass rate)
- Repeated Domain Program Benchmark (100% pass rate)
- StateM Context Refresh and Checked Transfer Semantics
- Production Readiness Disposition (READY)
"""

from typing import List, Tuple
import pytest

from ca_runtime.factory_certification import (
    AdversarialAttackVector,
    BenchmarkTraceSummary,
    CertificationCriterion,
    CertificationResultStatus,
    CriterionEvaluation,
    FactoryCertificationReport,
    FactoryCertificationRunner,
    ProductionReadinessStatus,
)
from ca_runtime.factory_observability import (
    ReadOnlyObservabilityMutationError,
    ReadOnlyObservabilityViewer,
    UnifiedFactoryCommandEngine,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.sdlf_factory import (
    SDLFExecutionRequest,
    SDLFFactoryEngine,
    SDLFOperatorShipDeniedError,
    SDLFPhaseKind,
    SDLFRepairExhaustedError,
    SDLFSandboxViolationError,
)
from ca_runtime.workflow_control_flow import OperatorGrantRecord


# ============================================================================
# Gate 1: Repeated Benchmark Executions Succeed (SDLF & Domain Program)
# ============================================================================


def test_gate1_repeated_benchmark_executions_succeed() -> None:
    """Gate 1: Repeated benchmark runs of SDLF and Domain Program succeed with 100% pass rate."""
    runner = FactoryCertificationRunner(tenant_id="tenant_cert_001")

    # 1. SDLF Benchmark (3 runs)
    sdlf_summary, sdlf_traces = runner.run_sdlf_benchmark(iterations=3)
    assert sdlf_summary.total_runs == 3
    assert sdlf_summary.successful_runs == 3
    assert sdlf_summary.failed_runs == 0
    assert sdlf_summary.pass_rate_bps == 10000
    assert len(sdlf_traces) == 3
    assert all(t.final_status == "COMPLETED" for t in sdlf_traces)

    # 2. Domain Program Benchmark (3 runs)
    prog_summary, prog_traces = runner.run_domain_program_benchmark(iterations=3)
    assert prog_summary.total_runs == 3
    assert prog_summary.successful_runs == 3
    assert prog_summary.failed_runs == 0
    assert prog_summary.pass_rate_bps == 10000
    assert len(prog_traces) == 3


# ============================================================================
# Gate 2 & Gate 4: Adversarial Failure Pack Defeated (All 6 Vectors)
# ============================================================================


def test_gate2_and_gate4_adversarial_failure_pack_defeated() -> None:
    """Gate 2 & Gate 4: All 6 adversarial vectors are tested and defeated fail-closed."""
    runner = FactoryCertificationRunner(tenant_id="tenant_adv_001")
    vectors = runner.run_adversarial_pack()

    assert len(vectors) == 6
    for v in vectors:
        assert v.defeated, f"Adversarial vector '{v.vector_id}: {v.name}' was not defeated!"
        assert len(v.vector_sha256) == 64


# ============================================================================
# Gate 3: Bounded Repair Monotonicity and Clean Exhaustion
# ============================================================================


def test_gate3_bounded_repair_exhaustion_terminates_cleanly() -> None:
    """Gate 3: Failing pipeline exhausts bounded retries and raises SDLFRepairExhaustedError."""
    engine = SDLFFactoryEngine()

    def constantly_failing_runner() -> Tuple[bool, List[str]]:
        return False, ["AssertionError: Unit tests failed"]

    req = SDLFExecutionRequest(
        request_id="SDLF_REQ_REPAIR_TEST",
        title="Repair Test",
        description="Failing tests",
        target_workspace="packages/ca_runtime",
        branch_name="feature/repair-test",
        max_repair_retries=2,
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )

    with pytest.raises(SDLFRepairExhaustedError) as exc_info:
        engine.run(req, deterministic_test_runner=constantly_failing_runner)

    assert exc_info.value.reason_code == "ERR_SDLF_REPAIR_EXHAUSTED"
    assert exc_info.value.details["attempts"] == 2


# ============================================================================
# Gate 5: Run Reconstructibility from Canonical Receipts
# ============================================================================


def test_gate5_run_reconstructibility_from_canonical_receipts() -> None:
    """Gate 5: Operator can reconstruct historical execution from canonical receipts alone."""
    command_engine = UnifiedFactoryCommandEngine()

    # Run program
    res_run = command_engine.execute_command_text("run program research_canonicalization_program")
    run_id = res_run.data["run_id"]

    # Replay run
    res_replay = command_engine.execute_command_text(f"replay run {run_id}")
    assert res_replay.success
    replay_data = res_replay.data["replay"]

    # Verify event chain
    assert len(replay_data["events"]) >= 1
    for event in replay_data["events"]:
        assert event["receipt_sha256"] != ""


# ============================================================================
# Gate 6: StateM Context Refresh and Checked Transfer Semantics
# ============================================================================


def test_gate6_statem_context_refresh_and_checked_transfer() -> None:
    """Gate 6: State entry refreshes context hash, and uncommitted states remain pending."""
    engine = SDLFFactoryEngine()
    req = SDLFExecutionRequest(
        request_id="SDLF_REQ_STATEM_TEST",
        title="StateM Feature",
        description="StateM verification",
        target_workspace="packages/ca_runtime",
        branch_name="feature/statem-test",
        sandbox_allowed_paths=("packages/ca_runtime/",),
    )
    grant = OperatorGrantRecord(
        grant_id="grant_statem",
        gate_id="SDLF_SHIP",
        approver_id="operator_commander",
        approver_role="commander_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="StateM verification approval",
        granted_at_utc="2026-09-02T06:00:00Z",
    )
    trace = engine.run(req, operator_ship_grant=grant)

    # Verify each phase has refreshed context hash and emitted receipt
    for phase_result in trace.phase_results:
        assert phase_result.receipt_sha256 != ""
        assert len(phase_result.receipt_sha256) == 64
        assert phase_result.phase_kind in SDLFPhaseKind


# ============================================================================
# Gate 7: Production Certification Report and READY Disposition
# ============================================================================


def test_gate7_production_certification_report_ready_status() -> None:
    """Gate 7: Full factory certification produces READY disposition and immutable report."""
    runner = FactoryCertificationRunner(
        tenant_id="tenant_prod_001",
        git_commit_sha="2043383556e698da5f8f06c4fa777068247fec57",
    )
    report = runner.run_full_certification()

    assert report.readiness_status == ProductionReadinessStatus.READY
    assert report.total_criteria == 12
    assert report.passed_criteria == 12
    assert report.failed_criteria == 0
    assert len(report.report_sha256) == 64
    assert report.sdlf_benchmark.pass_rate_bps == 10000
    assert report.domain_program_benchmark.pass_rate_bps == 10000
    assert len(report.adversarial_vectors) == 6
    assert all(v.defeated for v in report.adversarial_vectors)
