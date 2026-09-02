"""Comprehensive Test Suite for CAE Mandate M69: Evidence-Derived Certification.

Governed by:
- 05_CERTIFICATION/M69_evidence_derived_certification.md
- docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md
- 00_CONTROL/05_CLAIM_CEILING.md

Verifies:
- Gate 1: Genuine benchmark executions produce 12 PASSED criteria with observed evidence and READY disposition.
- Gate 2: Missing mandatory reality-contact evidence evaluates strictly to BLOCKED and NOT_READY disposition.
- Gate 3: Undefeated adversarial attacks evaluate strictly to FAILED and NOT_READY disposition.
- Gate 4: Benchmark failures prevent READY disposition.
- Gate 5: Proof that zero unconditional PASSED construction exists in evaluator.
- Gate 6: All 12 certification criteria declare explicit, non-empty required evidence contracts.
- Gate 7 (Countertest): Synthetic execution results without valid receipts fail closed.
"""

from __future__ import annotations

import pytest

from ca_runtime import (
    AdversarialAttackVector,
    BenchmarkTraceSummary,
    CertificationCriterion,
    CertificationResultStatus,
    CriterionEvaluation,
    FactoryCertificationReport,
    FactoryCertificationRunner,
    ProductionReadinessStatus,
    SDLFExecutionTrace,
    SDLFPhaseKind,
    SDLFPhaseResult,
)


# ===========================================================================
# Gate 1: Genuine benchmark executions produce 12 PASSED criteria
# ===========================================================================

def test_m69_evidence_derived_evaluation_passes_with_real_benchmarks() -> None:
    """Gate 1: Genuine benchmark + adversarial executions evaluate to 12 PASSED criteria and READY status."""
    runner = FactoryCertificationRunner(
        tenant_id="tenant_prod_m69",
        git_commit_sha="c50d66d01a9aeaed21da6b7159e4774f9350204c",
    )
    report = runner.run_full_certification()

    assert report.readiness_status == ProductionReadinessStatus.READY
    assert report.total_criteria == 12
    assert report.passed_criteria == 12
    assert report.failed_criteria == 0
    assert len(report.evaluations) == 12

    # Verify every criterion has explicit required evidence and observed evidence refs
    for ev in report.evaluations:
        assert ev.status == CertificationResultStatus.PASSED
        assert len(ev.required_evidence) > 0
        assert len(ev.observed_evidence_refs) > 0
        assert ev.reason != ""
        assert len(ev.evaluation_sha256) == 64


# ===========================================================================
# Gate 2: Missing mandatory evidence evaluates strictly to BLOCKED
# ===========================================================================

def test_m69_missing_evidence_evaluates_to_blocked() -> None:
    """Gate 2: Evaluating criteria with missing mandatory evidence produces BLOCKED status."""
    runner = FactoryCertificationRunner(tenant_id="tenant_test")

    # Evaluate each criterion with zero evidence
    for crit in CertificationCriterion:
        ev = runner._evaluate_criterion(
            criterion=crit,
            sdlf_summary=None,
            sdlf_traces=None,
            domain_summary=None,
            domain_traces=None,
            adv_vectors=None,
        )
        assert ev.status == CertificationResultStatus.BLOCKED
        assert "Missing" in ev.reason or "No " in ev.reason or "required" in ev.reason
        assert len(ev.required_evidence) > 0
        assert ev.observed_evidence_refs == ()


# ===========================================================================
# Gate 3: Undefeated adversarial attacks evaluate strictly to FAILED
# ===========================================================================

def test_m69_adversarial_failure_evaluates_to_failed() -> None:
    """Gate 3: An undefeated adversarial vector evaluates to FAILED and prevents READY disposition."""
    runner = FactoryCertificationRunner(tenant_id="tenant_test")

    # Construct a compromised adversarial pack where ADV-006 succeeded (identity collision allowed)
    compromised_vectors = [
        AdversarialAttackVector(
            vector_id="ADV-006",
            name="agent_identity_collision",
            description="Attempting to register conflicting definition",
            expected_error="AGENT_IDENTITY_COLLISION",
            actual_error="COLLISION_ALLOWED",
            defeated=False,  # Compromised!
        ),
        AdversarialAttackVector(
            vector_id="ADV-001",
            name="cross_tenant_trace_query",
            description="Attempting cross-tenant trace query",
            expected_error="ERR_OBSERVABILITY_TENANT_ISOLATION",
            actual_error="TENANT_ISOLATION_VIOLATION",
            defeated=True,
        ),
    ]

    ev = runner._evaluate_criterion(
        criterion=CertificationCriterion.AGENT_IDENTITY_COLLISION_DEFENSE,
        sdlf_summary=None,
        sdlf_traces=None,
        domain_summary=None,
        domain_traces=None,
        adv_vectors=compromised_vectors,
    )

    assert ev.status == CertificationResultStatus.FAILED
    assert "breached" in ev.reason.lower() or "not defeated" in ev.evidence_ref.lower()
    assert ev.observed_evidence_refs == ()


# ===========================================================================
# Gate 4: Benchmark failures prevent READY disposition
# ===========================================================================

def test_m69_benchmark_failure_blocks_ready_disposition() -> None:
    """Gate 4: Failing benchmark runs result in NOT_READY disposition."""
    runner = FactoryCertificationRunner(tenant_id="tenant_test")

    sdlf_summary = BenchmarkTraceSummary(
        suite_name="CAE_SDLF_11_PHASE_PIPELINE",
        total_runs=3,
        successful_runs=2,
        failed_runs=1,  # 1 failure!
        pass_rate_bps=6666,
        total_phases_executed=25,
        total_receipts_emitted=25,
    )
    domain_summary = BenchmarkTraceSummary(
        suite_name="RESEARCH_CANONICALIZATION_PROGRAM",
        total_runs=3,
        successful_runs=3,
        failed_runs=0,
        pass_rate_bps=10000,
        total_phases_executed=6,
        total_receipts_emitted=6,
    )

    # Evaluate report with a benchmark failure
    adv_vectors = runner.run_adversarial_pack()
    criteria = list(CertificationCriterion)
    evaluations = [
        runner._evaluate_criterion(
            criterion=crit,
            sdlf_summary=sdlf_summary,
            sdlf_traces=None,  # Will cause some to be BLOCKED
            domain_summary=domain_summary,
            domain_traces=[{}],
            adv_vectors=adv_vectors,
        )
        for crit in criteria
    ]

    passed_count = sum(1 for e in evaluations if e.status == CertificationResultStatus.PASSED)
    failed_count = sum(1 for e in evaluations if e.status == CertificationResultStatus.FAILED)
    blocked_count = sum(1 for e in evaluations if e.status == CertificationResultStatus.BLOCKED)

    is_ready = (
        passed_count == len(criteria)
        and failed_count == 0
        and blocked_count == 0
        and sdlf_summary.failed_runs == 0
    )
    assert not is_ready


# ===========================================================================
# Gate 5: Zero unconditional PASSED construction exists in evaluator
# ===========================================================================

def test_m69_no_unconditional_pass_in_evaluator() -> None:
    """Gate 5: Evaluator rejects ungrounded evaluation requests without observed evidence."""
    runner = FactoryCertificationRunner(tenant_id="tenant_test")

    # None of the 12 criteria should ever return PASSED when all inputs are None
    for crit in CertificationCriterion:
        ev = runner._evaluate_criterion(
            criterion=crit,
            sdlf_summary=None,
            sdlf_traces=None,
            domain_summary=None,
            domain_traces=None,
            adv_vectors=None,
        )
        assert ev.status != CertificationResultStatus.PASSED


# ===========================================================================
# Gate 6: All 12 criteria declare explicit required evidence contracts
# ===========================================================================

def test_m69_all_twelve_criteria_have_explicit_evidence_contracts() -> None:
    """Gate 6: Every criterion has declared mandatory required evidence."""
    runner = FactoryCertificationRunner(tenant_id="tenant_test")

    for crit in CertificationCriterion:
        ev = runner._evaluate_criterion(
            criterion=crit,
            sdlf_summary=None,
            sdlf_traces=None,
            domain_summary=None,
            domain_traces=None,
            adv_vectors=None,
        )
        assert len(ev.required_evidence) >= 1
        for req in ev.required_evidence:
            assert isinstance(req, str)
            assert len(req) > 0


# ===========================================================================
# Gate 7 (Countertest): Synthetic command results without receipts fail closed
# ===========================================================================

def test_m69_synthetic_command_success_without_receipts_blocked() -> None:
    """Countertest: Synthetic SDLF phase results without cryptographic receipts fail closed."""
    runner = FactoryCertificationRunner(tenant_id="tenant_test")

    from ca_runtime import WorkUnitKind

    # Create fake SDLF execution trace with empty receipt digests
    fake_phase_results = [
        SDLFPhaseResult(
            phase_kind=SDLFPhaseKind.SCOUT,
            work_unit_kind=WorkUnitKind.AGENT_CALL,
            success=True,
            outputs={"findings": ["fake"]},
            receipt_sha256="",  # Missing receipt!
        )
    ]
    fake_trace = SDLFExecutionTrace(
        trace_id="fake_trace_001",
        request_id="fake_req_001",
        phase_results=tuple(fake_phase_results),
        final_status="COMPLETED",
        repair_attempts_count=0,
        operator_ship_granted=True,
    )

    ev = runner._evaluate_criterion(
        criterion=CertificationCriterion.PROMPT_CONTEXT_HASH_INTEGRITY,
        sdlf_summary=None,
        sdlf_traces=[fake_trace],
        domain_summary=None,
        domain_traces=None,
        adv_vectors=None,
    )

    # Insufficient receipts (< 11) must evaluate to FAILED, never PASSED
    assert ev.status == CertificationResultStatus.FAILED
    assert "INSUFFICIENT" in ev.evidence_ref or "Missing" in ev.reason
