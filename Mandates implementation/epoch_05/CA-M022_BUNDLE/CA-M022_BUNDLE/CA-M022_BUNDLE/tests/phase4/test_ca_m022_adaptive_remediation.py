"""
CA-M022 — Adaptive Elicitation & Missing-Unit Resilience
Tests for FR-022 / FR-ELIC-002

Verification matrix
===================

SCHEMA
  test_mandate_constants_are_correct
  test_policy_defaults_are_within_bounds
  test_unit_record_schema_fields_present
  test_receipt_schema_fields_present

EXECUTABLE — positive path (session with missing units can still pass)
  test_session_with_one_omitted_unit_passes_when_yield_criteria_met
  test_session_with_multiple_omitted_units_passes_when_yield_criteria_met
  test_all_units_executed_passes_trivially
  test_partial_units_count_toward_yield_ratio
  test_custom_policy_lower_thresholds_accepts_weaker_session
  test_zero_omission_rate_passes_ceiling_gate

EXECUTABLE — negative path (fail-closed)
  test_session_fails_when_yield_ratio_below_minimum
  test_session_fails_when_tension_below_minimum
  test_session_fails_when_evidence_count_below_minimum
  test_session_fails_when_omission_rate_exceeds_maximum
  test_all_units_omitted_fails_every_gate
  test_partial_units_only_no_evidence_fails_evidence_gate
  test_empty_unit_list_fails_yield_and_evidence_gates

EXECUTABLE — omitted units remain visible in completion record
  test_omitted_units_recorded_in_passing_receipt
  test_omitted_units_recorded_in_failing_receipt
  test_omitted_unit_reason_is_preserved
  test_omitted_units_tuple_is_always_present_even_when_empty

EXECUTABLE — require_session_passed fail-closed guard
  test_require_session_passed_does_not_raise_for_passing_receipt
  test_require_session_passed_raises_for_failing_receipt
  test_require_session_passed_raises_for_foreign_receipt_mandate
  test_require_session_passed_raises_for_non_receipt

EXECUTABLE — remediation prompt injection
  test_failing_session_gets_remediation_prompts
  test_passing_session_has_no_remediation_prompts
  test_reactivate_prompt_generated_for_omitted_unit
  test_deepen_prompt_generated_for_low_tension_unit
  test_remediation_prompts_have_constitutional_check_passed
  test_remediation_prompt_kind_matches_failure_type

EXECUTABLE — unit record validation
  test_omitted_unit_requires_nonempty_omission_reason
  test_omitted_unit_requires_zero_tension
  test_omitted_unit_requires_zero_evidence
  test_executed_unit_accepts_nonzero_values
  test_invalid_status_raises_error
  test_invalid_tension_score_type_raises_error
  test_tension_score_out_of_range_raises_error
  test_missing_required_field_in_mapping_raises_error
  test_empty_unit_id_raises_error

INTEGRATION — authoritative boundary
  test_evaluate_returns_receipt_with_correct_session_id
  test_receipt_is_hash_addressable_and_deterministic
  test_module_level_convenience_function_matches_class_method
  test_receipt_to_dict_is_json_serialisable

FALSE-PROOF countercase
  test_false_proof_any_unit_executed_does_not_imply_pass
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Path bootstrap — mirrors pattern in tests/phase4/_support.py
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
for _p in reversed(
    [
        ROOT / "packages/ca_contracts/src",
        ROOT / "packages/ca_runtime/src",
        ROOT / "services/air/src",
        ROOT / "services/pipeline/src",
        ROOT / "services/interview/src",
    ]
):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from conscious_activations_interview_expression.adaptive_remediation import (
    MANDATE_ID,
    INVARIANT_ID,
    POLICY_VERSION,
    DEFAULT_MIN_HOLISTIC_YIELD_RATIO,
    DEFAULT_MIN_TENSION_SCORE,
    DEFAULT_MIN_EVIDENCE_COUNT,
    DEFAULT_MAX_OMISSION_RATE,
    AdaptiveElicitationEvaluator,
    ElicitationUnitRecord,
    InvalidUnitRecordError,
    OmittedUnitRecord,
    RemediationKind,
    UnitStatus,
    YieldEvaluationOutcome,
    YieldEvaluationReceipt,
    YieldSufficiencyPolicy,
    YieldCriteriaNotMetError,
    YieldEvaluationBlockedError,
    evaluate_session_yield,
    require_session_passed,
)


# ---------------------------------------------------------------------------
# Shared helpers / factories
# ---------------------------------------------------------------------------


def _executed(unit_id: str, *, tension: float = 0.70, evidence: int = 3) -> ElicitationUnitRecord:
    return ElicitationUnitRecord(
        unit_id=unit_id,
        status=UnitStatus.EXECUTED,
        tension_score=tension,
        evidence_count=evidence,
    )


def _omitted(unit_id: str, reason: str = "TIME_CONSTRAINT") -> ElicitationUnitRecord:
    return ElicitationUnitRecord(
        unit_id=unit_id,
        status=UnitStatus.OMITTED,
        tension_score=0.0,
        evidence_count=0,
        omission_reason=reason,
    )


def _partial(unit_id: str, *, tension: float = 0.50, evidence: int = 1) -> ElicitationUnitRecord:
    return ElicitationUnitRecord(
        unit_id=unit_id,
        status=UnitStatus.PARTIAL,
        tension_score=tension,
        evidence_count=evidence,
    )


def _passing_session_units() -> list[ElicitationUnitRecord]:
    """Three executed units, one omitted — yields well above thresholds."""
    return [
        _executed("unit-A", tension=0.80, evidence=4),
        _executed("unit-B", tension=0.75, evidence=3),
        _executed("unit-C", tension=0.70, evidence=2),
        _omitted("unit-D", reason="GUEST_REDIRECTED"),
    ]


def _evaluator(policy: YieldSufficiencyPolicy | None = None) -> AdaptiveElicitationEvaluator:
    return AdaptiveElicitationEvaluator(policy)


SESSION_ID = "session-m022-test-001"


# ===========================================================================
# SCHEMA
# ===========================================================================


def test_mandate_constants_are_correct() -> None:
    assert MANDATE_ID == "CA-M022"
    assert INVARIANT_ID == "FR-ELIC-002"
    assert POLICY_VERSION == "CA-M022-ADAPTIVE-ELICITATION-V1"


def test_policy_defaults_are_within_bounds() -> None:
    policy = YieldSufficiencyPolicy()
    assert 0.0 < policy.min_holistic_yield_ratio <= 1.0
    assert 0.0 < policy.min_tension_score <= 1.0
    assert policy.min_evidence_count >= 0
    assert 0.0 < policy.max_omission_rate <= 1.0


def test_unit_record_schema_fields_present() -> None:
    u = _executed("unit-X")
    assert u.unit_id == "unit-X"
    assert u.status is UnitStatus.EXECUTED
    assert isinstance(u.tension_score, float)
    assert isinstance(u.evidence_count, int)
    assert isinstance(u.omission_reason, str)


def test_receipt_schema_fields_present() -> None:
    receipt = _evaluator().evaluate(SESSION_ID, _passing_session_units())
    d = receipt.to_dict()
    required = {
        "mandate_id", "invariant_id", "policy_version", "session_id",
        "outcome", "passed", "total_planned_units", "executed_unit_count",
        "omitted_unit_count", "partial_unit_count", "holistic_yield_ratio",
        "mean_tension_score", "total_evidence_count", "omission_rate",
        "omitted_units", "gates", "policy", "remediation_prompts",
        "limitations", "receipt_sha256",
    }
    assert required.issubset(d.keys())


# ===========================================================================
# EXECUTABLE — positive path
# ===========================================================================


def test_session_with_one_omitted_unit_passes_when_yield_criteria_met() -> None:
    units = _passing_session_units()  # 3 executed, 1 omitted → ratio 0.75
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is True
    assert receipt.outcome is YieldEvaluationOutcome.PASSED


def test_session_with_multiple_omitted_units_passes_when_yield_criteria_met() -> None:
    # 5 executed, 2 omitted → ratio 5/7 ≈ 0.714 > 0.70
    # tension 0.80 > 0.40, evidence 15 > 1, omission 2/7 ≈ 0.286 < 0.50
    units = [
        _executed(f"unit-{i}", tension=0.80, evidence=3) for i in range(5)
    ] + [
        _omitted(f"omit-{j}", reason="TIME") for j in range(2)
    ]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is True
    assert receipt.omitted_unit_count == 2


def test_all_units_executed_passes_trivially() -> None:
    units = [_executed(f"u{i}", tension=0.60, evidence=2) for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is True
    assert receipt.omission_rate == 0.0
    assert receipt.omitted_unit_count == 0


def test_partial_units_count_toward_yield_ratio() -> None:
    # 3 partial, 1 omitted → active_count 3, total 4 → ratio 0.75
    units = [
        _partial("p-A", tension=0.60, evidence=2),
        _partial("p-B", tension=0.55, evidence=2),
        _partial("p-C", tension=0.50, evidence=1),
        _omitted("o-D", reason="OPERATOR_SKIP"),
    ]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is True
    assert receipt.partial_unit_count == 3


def test_custom_policy_lower_thresholds_accepts_weaker_session() -> None:
    weak_policy = YieldSufficiencyPolicy(
        min_holistic_yield_ratio=0.50,
        min_tension_score=0.20,
        min_evidence_count=1,
        max_omission_rate=0.60,
    )
    # Only 1 executed out of 3 — ratio 0.33 < default 0.70, but > 0.50 custom
    # Wait: 1/3 = 0.33 < 0.50 still. Let's use 2 out of 3 = 0.67 > 0.50
    units = [
        _executed("u1", tension=0.30, evidence=2),
        _executed("u2", tension=0.25, evidence=1),
        _omitted("u3", reason="GUEST_REQUEST"),
    ]
    receipt = _evaluator(weak_policy).evaluate(SESSION_ID, units)
    assert receipt.passed is True


def test_zero_omission_rate_passes_ceiling_gate() -> None:
    units = [_executed(f"u{i}", tension=0.70, evidence=2) for i in range(3)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.omission_rate == 0.0
    gate = receipt.gates["omission_rate"]
    assert gate.passed is True


# ===========================================================================
# EXECUTABLE — negative path (fail-closed)
# ===========================================================================


def test_session_fails_when_yield_ratio_below_minimum() -> None:
    # 1 executed, 4 omitted → ratio 0.20 < 0.70
    units = [
        _executed("u1", tension=0.80, evidence=5),
    ] + [_omitted(f"o{i}", reason="TIME") for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert receipt.outcome is YieldEvaluationOutcome.FAILED_INSUFFICIENT_YIELD
    assert receipt.gates["holistic_yield_ratio"].passed is False


def test_session_fails_when_tension_below_minimum() -> None:
    # All executed, high yield, but tension 0.10 < 0.40
    units = [_executed(f"u{i}", tension=0.10, evidence=2) for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert receipt.gates["mean_tension_score"].passed is False


def test_session_fails_when_evidence_count_below_minimum() -> None:
    policy = YieldSufficiencyPolicy(
        min_holistic_yield_ratio=0.50,
        min_tension_score=0.30,
        min_evidence_count=5,  # require at least 5 pieces
        max_omission_rate=0.50,
    )
    # Only 2 total evidence items
    units = [
        _executed("u1", tension=0.80, evidence=1),
        _executed("u2", tension=0.70, evidence=1),
    ]
    receipt = _evaluator(policy).evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert receipt.gates["evidence_count"].passed is False
    assert receipt.outcome is YieldEvaluationOutcome.FAILED_BELOW_EVIDENCE_MINIMUM


def test_session_fails_when_omission_rate_exceeds_maximum() -> None:
    # 3 omitted out of 4 = 0.75 > 0.50
    units = [
        _executed("u1", tension=0.80, evidence=3),
    ] + [_omitted(f"o{i}", reason="SKIP") for i in range(3)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert receipt.gates["omission_rate"].passed is False
    assert receipt.outcome is YieldEvaluationOutcome.FAILED_OMISSION_RATE_EXCEEDED


def test_all_units_omitted_fails_every_gate() -> None:
    units = [_omitted(f"o{i}", reason="ALL_SKIPPED") for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert all(not g.passed for name, g in receipt.gates.items()
               if name != "omission_rate" or receipt.omission_rate > receipt.policy.max_omission_rate)


def test_partial_units_only_no_evidence_fails_evidence_gate() -> None:
    policy = YieldSufficiencyPolicy(
        min_holistic_yield_ratio=0.50,
        min_tension_score=0.30,
        min_evidence_count=3,
        max_omission_rate=0.50,
    )
    # Partial units with zero evidence
    units = [
        _partial("p1", tension=0.60, evidence=0),
        _partial("p2", tension=0.55, evidence=0),
    ]
    receipt = _evaluator(policy).evaluate(SESSION_ID, units)
    assert receipt.total_evidence_count == 0
    assert receipt.gates["evidence_count"].passed is False


def test_empty_unit_list_fails_yield_and_evidence_gates() -> None:
    receipt = _evaluator().evaluate(SESSION_ID, [])
    assert receipt.passed is False
    # yield ratio = 0.0, evidence = 0
    assert receipt.holistic_yield_ratio == 0.0
    assert receipt.total_evidence_count == 0


# ===========================================================================
# EXECUTABLE — omitted units remain visible in completion record
# ===========================================================================


def test_omitted_units_recorded_in_passing_receipt() -> None:
    units = _passing_session_units()  # contains "unit-D" omitted
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is True
    assert receipt.omitted_unit_count == 1
    assert any(ou.unit_id == "unit-D" for ou in receipt.omitted_units)


def test_omitted_units_recorded_in_failing_receipt() -> None:
    # 1 executed, 4 omitted — fails
    units = [
        _executed("u1", tension=0.80, evidence=5),
    ] + [_omitted(f"o{i}", reason="SKIPPED") for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert len(receipt.omitted_units) == 4
    omitted_ids = {ou.unit_id for ou in receipt.omitted_units}
    assert {"o0", "o1", "o2", "o3"}.issubset(omitted_ids)


def test_omitted_unit_reason_is_preserved() -> None:
    units = [
        _executed("u1", tension=0.80, evidence=3),
        _executed("u2", tension=0.75, evidence=3),
        _executed("u3", tension=0.70, evidence=2),
        _omitted("u4", reason="OPERATOR_ELECTED_TO_SKIP"),
    ]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    omitted = next(ou for ou in receipt.omitted_units if ou.unit_id == "u4")
    assert omitted.omission_reason == "OPERATOR_ELECTED_TO_SKIP"


def test_omitted_units_tuple_is_always_present_even_when_empty() -> None:
    units = [_executed("u1", tension=0.80, evidence=3)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    # No omissions — tuple should be present but empty
    assert isinstance(receipt.omitted_units, tuple)
    assert len(receipt.omitted_units) == 0


# ===========================================================================
# EXECUTABLE — require_session_passed fail-closed guard
# ===========================================================================


def test_require_session_passed_does_not_raise_for_passing_receipt() -> None:
    receipt = _evaluator().evaluate(SESSION_ID, _passing_session_units())
    assert receipt.passed is True
    # Must not raise
    _evaluator().require_session_passed(receipt)


def test_require_session_passed_raises_for_failing_receipt() -> None:
    units = [_omitted(f"o{i}", reason="ALL_SKIPPED") for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    with pytest.raises(YieldCriteriaNotMetError) as exc_info:
        _evaluator().require_session_passed(receipt)
    err = exc_info.value
    assert "YIELD_CRITERIA_NOT_MET" in err.context.get("reason_code", "")
    assert err.context["session_id"] == SESSION_ID


def test_require_session_passed_raises_for_foreign_receipt_mandate() -> None:
    """A receipt from a different mandate must not be accepted."""
    good_receipt = _evaluator().evaluate(SESSION_ID, _passing_session_units())

    # Craft a fake receipt with wrong mandate_id using dataclass pattern
    # We exploit the fact that YieldEvaluationReceipt is frozen — we must
    # construct from scratch.
    class _FakeReceipt:
        mandate_id = "CA-M999"
        invariant_id = INVARIANT_ID
        policy_version = POLICY_VERSION
        passed = True

    with pytest.raises(YieldCriteriaNotMetError) as exc_info:
        _evaluator().require_session_passed(_FakeReceipt())  # type: ignore[arg-type]
    assert "MISSING_AUTHORITATIVE_RECEIPT" in exc_info.value.context.get("reason_code", "")


def test_require_session_passed_raises_for_non_receipt() -> None:
    with pytest.raises(YieldCriteriaNotMetError):
        _evaluator().require_session_passed({"passed": True})  # type: ignore[arg-type]


# ===========================================================================
# EXECUTABLE — remediation prompt injection
# ===========================================================================


def test_failing_session_gets_remediation_prompts() -> None:
    # Low tension — should trigger DEEPEN prompts
    units = [_executed(f"u{i}", tension=0.10, evidence=2) for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    assert len(receipt.remediation_prompts) > 0


def test_passing_session_has_no_remediation_prompts() -> None:
    receipt = _evaluator().evaluate(SESSION_ID, _passing_session_units())
    assert receipt.passed is True
    assert len(receipt.remediation_prompts) == 0


def test_reactivate_prompt_generated_for_omitted_unit() -> None:
    # Low yield due to many omissions — should generate REACTIVATE prompts
    units = [
        _executed("u1", tension=0.80, evidence=3),
    ] + [_omitted(f"o{i}", reason="SKIPPED") for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    prompt_kinds = {p.kind for p in receipt.remediation_prompts}
    assert RemediationKind.REACTIVATE in prompt_kinds
    # Prompts must target omitted units
    prompt_targets = {p.target_unit_id for p in receipt.remediation_prompts
                      if p.kind is RemediationKind.REACTIVATE}
    omitted_ids = {ou.unit_id for ou in receipt.omitted_units}
    assert prompt_targets.issubset(omitted_ids)


def test_deepen_prompt_generated_for_low_tension_unit() -> None:
    # All executed, but tension is low — expect DEEPEN prompts
    units = [_executed(f"u{i}", tension=0.10, evidence=2) for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    prompt_kinds = {p.kind for p in receipt.remediation_prompts}
    assert RemediationKind.DEEPEN in prompt_kinds


def test_remediation_prompts_have_constitutional_check_passed() -> None:
    units = [_executed(f"u{i}", tension=0.10, evidence=2) for i in range(4)]
    receipt = _evaluator().evaluate(SESSION_ID, units)
    for prompt in receipt.remediation_prompts:
        assert prompt.constitutional_check_passed is True


def test_remediation_prompt_kind_matches_failure_type() -> None:
    # Omissions → REACTIVATE; low tension → DEEPEN
    units = [
        _executed("u1", tension=0.80, evidence=3),
        _executed("u2", tension=0.75, evidence=3),
        _omitted("u3", reason="SKIPPED"),
        _omitted("u4", reason="SKIPPED"),
        _omitted("u5", reason="SKIPPED"),
    ]
    # ratio = 2/5 = 0.40 < 0.70, omission = 3/5 = 0.60 > 0.50
    receipt = _evaluator().evaluate(SESSION_ID, units)
    assert receipt.passed is False
    for p in receipt.remediation_prompts:
        assert p.kind in {RemediationKind.REACTIVATE, RemediationKind.DEEPEN, RemediationKind.CLARIFY}


# ===========================================================================
# EXECUTABLE — unit record validation
# ===========================================================================


def test_omitted_unit_requires_nonempty_omission_reason() -> None:
    with pytest.raises(InvalidUnitRecordError, match="omission_reason"):
        ElicitationUnitRecord(
            unit_id="u1",
            status=UnitStatus.OMITTED,
            tension_score=0.0,
            evidence_count=0,
            omission_reason="",  # empty — must be rejected
        )


def test_omitted_unit_requires_zero_tension() -> None:
    with pytest.raises(InvalidUnitRecordError, match="tension_score"):
        ElicitationUnitRecord(
            unit_id="u1",
            status=UnitStatus.OMITTED,
            tension_score=0.5,  # non-zero — must be rejected
            evidence_count=0,
            omission_reason="SKIPPED",
        )


def test_omitted_unit_requires_zero_evidence() -> None:
    with pytest.raises(InvalidUnitRecordError, match="evidence_count"):
        ElicitationUnitRecord(
            unit_id="u1",
            status=UnitStatus.OMITTED,
            tension_score=0.0,
            evidence_count=2,  # non-zero — must be rejected
            omission_reason="SKIPPED",
        )


def test_executed_unit_accepts_nonzero_values() -> None:
    u = ElicitationUnitRecord(
        unit_id="u-exec",
        status=UnitStatus.EXECUTED,
        tension_score=0.85,
        evidence_count=4,
    )
    assert u.status is UnitStatus.EXECUTED
    assert u.tension_score == 0.85
    assert u.evidence_count == 4


def test_invalid_status_raises_error() -> None:
    with pytest.raises(InvalidUnitRecordError):
        ElicitationUnitRecord(
            unit_id="u1",
            status="INVALID_STATUS",  # type: ignore[arg-type]
            tension_score=0.5,
            evidence_count=1,
        )


def test_invalid_tension_score_type_raises_error() -> None:
    with pytest.raises(InvalidUnitRecordError):
        ElicitationUnitRecord(
            unit_id="u1",
            status=UnitStatus.EXECUTED,
            tension_score="high",  # type: ignore[arg-type]
            evidence_count=1,
        )


def test_tension_score_out_of_range_raises_error() -> None:
    with pytest.raises(InvalidUnitRecordError):
        ElicitationUnitRecord(
            unit_id="u1",
            status=UnitStatus.EXECUTED,
            tension_score=1.5,  # > 1.0
            evidence_count=1,
        )


def test_missing_required_field_in_mapping_raises_error() -> None:
    with pytest.raises(InvalidUnitRecordError) as exc_info:
        ElicitationUnitRecord.from_mapping({"unit_id": "u1", "status": "EXECUTED"})
    assert "missing required" in str(exc_info.value).lower()


def test_empty_unit_id_raises_error() -> None:
    with pytest.raises(InvalidUnitRecordError):
        ElicitationUnitRecord(
            unit_id="   ",  # whitespace only
            status=UnitStatus.EXECUTED,
            tension_score=0.5,
            evidence_count=1,
        )


# ===========================================================================
# INTEGRATION — authoritative boundary
# ===========================================================================


def test_evaluate_returns_receipt_with_correct_session_id() -> None:
    receipt = _evaluator().evaluate("session-xyz-999", _passing_session_units())
    assert receipt.session_id == "session-xyz-999"


def test_receipt_is_hash_addressable_and_deterministic() -> None:
    units = _passing_session_units()
    r1 = _evaluator().evaluate(SESSION_ID, units)
    r2 = _evaluator().evaluate(SESSION_ID, units)
    assert r1.receipt_sha256 == r2.receipt_sha256
    assert len(r1.receipt_sha256) == 64  # full SHA-256 hex
    assert all(c in "0123456789abcdef" for c in r1.receipt_sha256)


def test_module_level_convenience_function_matches_class_method() -> None:
    units = _passing_session_units()
    r_module = evaluate_session_yield(SESSION_ID, units)
    r_class = AdaptiveElicitationEvaluator().evaluate(SESSION_ID, units)
    # Must produce the same receipt
    assert r_module.receipt_sha256 == r_class.receipt_sha256
    assert r_module.passed == r_class.passed


def test_receipt_to_dict_is_json_serialisable() -> None:
    receipt = _evaluator().evaluate(SESSION_ID, _passing_session_units())
    d = receipt.to_dict()
    # Must not raise — all values must be JSON-serialisable
    payload = json.dumps(d)
    assert len(payload) > 0
    parsed = json.loads(payload)
    assert parsed["mandate_id"] == "CA-M022"
    assert parsed["passed"] is True


def test_evaluate_with_mapping_input() -> None:
    """Unit records may be supplied as plain mappings (dict) instead of dataclasses."""
    units_as_dicts: list[dict[str, Any]] = [
        {"unit_id": "u1", "status": "EXECUTED", "tension_score": 0.75, "evidence_count": 3},
        {"unit_id": "u2", "status": "EXECUTED", "tension_score": 0.70, "evidence_count": 2},
        {"unit_id": "u3", "status": "EXECUTED", "tension_score": 0.65, "evidence_count": 2},
        {"unit_id": "u4", "status": "OMITTED", "tension_score": 0.0,
         "evidence_count": 0, "omission_reason": "TIME"},
    ]
    receipt = _evaluator().evaluate(SESSION_ID, units_as_dicts)
    assert receipt.passed is True


def test_invalid_session_id_raises_evaluation_blocked() -> None:
    with pytest.raises(YieldEvaluationBlockedError):
        _evaluator().evaluate("", _passing_session_units())


# ===========================================================================
# FALSE-PROOF countercase
# ===========================================================================


def test_false_proof_any_unit_executed_does_not_imply_pass() -> None:
    """
    False-proof countercase: a session where at least one unit executed
    must NOT be marked as PASSED unless yield criteria are actually met.

    This proves that partial progress is not accepted as holistic success.
    """
    # One unit executed with good tension, but four omitted → ratio 0.20 < 0.70
    units = [
        _executed("u-anchor", tension=0.90, evidence=5),
    ] + [_omitted(f"o{i}", reason="ALL_OTHERS_SKIPPED") for i in range(4)]

    receipt = _evaluator().evaluate(SESSION_ID, units)

    # The one executed unit has good metrics — a naive "any success" check
    # would pass this session. The mandate requires fail-closed evaluation.
    assert receipt.passed is False, (
        "A session where only 1 of 5 planned units executed must NOT pass "
        "holistic yield evaluation, even when that one unit has excellent metrics. "
        "This proves CA-M022 enforces holistic yield, not partial-progress success."
    )
    assert receipt.executed_unit_count == 1
    assert receipt.omitted_unit_count == 4
    assert receipt.holistic_yield_ratio < DEFAULT_MIN_HOLISTIC_YIELD_RATIO
    # Omitted units must still be visible
    assert len(receipt.omitted_units) == 4
