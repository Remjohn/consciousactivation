from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.independent_scoring import (
    BASE_DIMENSIONS,
    NON_COMPENSABLE_GATES,
    ControlledMutation,
    DevelopmentRubric,
    DimensionDistribution,
    DimensionScorecard,
    DimensionStatus,
    GateResult,
    GateStatus,
    IndependentScoringError,
    IndependentScoringReceipt,
    RepeatedRunSummary,
    build_rejection_receipt,
    canonical_json_bytes,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def rubric() -> DevelopmentRubric:
    return DevelopmentRubric(
        rubric_id="OD-AM-001-ST-08.03-INDEPENDENT-DIMENSIONS-v1",
        rubric_version="1.0.0-development",
        scoring_policy_version="1.0.0-development",
        evaluator_contract_version="1.0.0-development",
        threshold_policy_reference="HUMAN_GOVERNED_NOT_DEFINED",
        scoring_policy_sha256=digest("development-scoring-policy-v1"),
        threshold_policy_reference_sha256=digest("human-threshold-policy-reference-v1"),
    )


def scorecards(score: int = 10_000) -> tuple[DimensionScorecard, ...]:
    return tuple(
        DimensionScorecard(
            dimension=dimension,
            status=DimensionStatus.PASSING,
            score_basis_points=score,
            evidence_refs=(digest(f"dimension-evidence-{dimension}"),),
        )
        for dimension in BASE_DIMENSIONS
    )


def mutation() -> ControlledMutation:
    return ControlledMutation(
        mutation_id="controlled-preserve-topic-change-grammar-v1",
        mutation_type="preserve_topic_change_grammar",
        base_case_sha256=digest("base-case-v1"),
        mutated_input_sha256=digest("mutated-case-v1"),
        changed_variables=("grammar",),
        preserved_invariants=(
            "topic",
            "source_identity",
            "target_category",
            "profile_identity",
            "rubric_identity",
        ),
        expected_decision_sha256=digest("expected-decision-v1"),
        source_lineage_sha256=digest("source-lineage-v1"),
    )


def gates(*, failing: str | None = None) -> tuple[GateResult, ...]:
    return tuple(
        GateResult(
            gate_id=gate_id,
            status=GateStatus.FAILING if gate_id == failing else GateStatus.PASSING,
            evidence_refs=(digest(f"gate-evidence-{gate_id}"),),
            failure_context=(
                f"{gate_id} rejected the bounded decision" if gate_id == failing else None
            ),
        )
        for gate_id in NON_COMPENSABLE_GATES
    )


def stability(score: int = 10_000) -> RepeatedRunSummary:
    return RepeatedRunSummary(
        repetition_identities=(digest("repeat-41"), digest("repeat-42"), digest("repeat-43")),
        distributions=tuple(
            DimensionDistribution(
                dimension=dimension,
                scores_basis_points=(score, score, score),
            )
            for dimension in BASE_DIMENSIONS
        ),
        dominant_failure_patterns=(),
    )


def receipt_values(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "rubric": rubric(),
        "evaluated_artifact_sha256": digest("evaluated-artifact-v1"),
        "builder_version": "builder-development-v1",
        "target_category": "generic_not_applicable_category_branch",
        "target_profile": "repository_owned_generic_control_v1",
        "source_ir_sha256": digest("source-ir-v1"),
        "predecessor_maturity_receipt_sha256": digest("st-08.02-maturity-receipt-v1"),
        "benchmark_portfolio_sha256": digest("development-portfolio-v1"),
        "case_identity_sha256": digest("development-case-v1"),
        "case_access_class": "development",
        "run_id": "st-08.03-development-run-v1",
        "provenance_sha256": digest("provenance-v1"),
        "command_identity": digest("issue-command-v1"),
        "authority_identity": digest("scoring-authority-v1"),
        "scorecards": scorecards(),
        "mutations": (mutation(),),
        "gates": gates(),
        "stability_summary": stability(),
        "downstream_results": (),
        "observations": (
            "ST-08.03:IndependentDimensionsScored",
            "ST-08.03:NonCompensableGatesEvaluated",
        ),
        "composite_trend_basis_points": 10_000,
    }
    values.update(changes)
    return values


@pytest.mark.parametrize("failed_gate", NON_COMPENSABLE_GATES)
def test_each_non_compensable_gate_dominates_perfect_scores_and_stability(
    failed_gate: str,
) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        IndependentScoringReceipt(
            **receipt_values(
                scorecards=scorecards(10_000),
                gates=gates(failing=failed_gate),
                stability_summary=stability(10_000),
                composite_trend_basis_points=10_000,
            )
        )

    assert caught.value.code == "NON_COMPENSABLE_GATE_FAILED"
    assert caught.value.context == {"failed": (failed_gate,)}


def test_hard_gate_registry_is_exactly_the_nine_capsule_gates() -> None:
    assert NON_COMPENSABLE_GATES == (
        "critical_unsupported_decision",
        "evidence_failure",
        "wrong_atomicity",
        "contract_contradiction",
        "silent_rewrite",
        "untested_required_skill",
        "benchmark_leakage",
        "false_readiness",
        "anti_goal_violation",
    )
    assert rubric().hard_gates == NON_COMPENSABLE_GATES


@pytest.mark.parametrize(
    "malformed_gates",
    (
        gates()[:-1],
        gates()[:-1] + (gates()[0],),
        tuple(reversed(gates())),
    ),
)
def test_missing_duplicate_or_reordered_hard_gates_fail_closed(
    malformed_gates: tuple[GateResult, ...],
) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        IndependentScoringReceipt(**receipt_values(gates=malformed_gates))

    assert caught.value.code == "INCOMPLETE_NON_COMPENSABLE_GATES"


def test_a_failed_gate_requires_attributable_failure_context() -> None:
    with pytest.raises(IndependentScoringError) as caught:
        GateResult(
            gate_id="evidence_failure",
            status=GateStatus.FAILING,
            evidence_refs=(digest("gate-evidence"),),
        )

    assert caught.value.code == "MISSING_GOVERNED_FIELD"
    assert caught.value.context == {"field": "failure_context"}


def test_protected_case_access_is_rejected_before_a_scoring_receipt_exists() -> None:
    created: IndependentScoringReceipt | None = None
    with pytest.raises(IndependentScoringError) as caught:
        created = IndependentScoringReceipt(
            **receipt_values(case_access_class="protected")
        )

    assert caught.value.code == "PROTECTED_OR_UNKNOWN_CASE_ACCESS"
    assert created is None


def test_protected_label_access_is_rejected_even_when_every_gate_and_score_passes() -> None:
    with pytest.raises(IndependentScoringError) as caught:
        IndependentScoringReceipt(
            **receipt_values(
                protected_label_accessed=True,
                scorecards=scorecards(10_000),
                gates=gates(),
                composite_trend_basis_points=10_000,
            )
        )

    assert caught.value.code == "PROTECTED_LABEL_ACCESS_PROHIBITED"


def test_benchmark_leakage_cannot_be_reclassified_as_a_high_scoring_pass() -> None:
    with pytest.raises(IndependentScoringError) as caught:
        IndependentScoringReceipt(
            **receipt_values(
                gates=gates(failing="benchmark_leakage"),
                composite_trend_basis_points=10_000,
            )
        )

    assert caught.value.code == "NON_COMPENSABLE_GATE_FAILED"
    assert caught.value.context["failed"] == ("benchmark_leakage",)


def test_gate_tampering_after_construction_is_detected_by_parent_receipt() -> None:
    receipt = IndependentScoringReceipt(**receipt_values())
    gate = receipt.gates[0]
    original_identity = receipt.receipt_identity
    object.__setattr__(gate, "status", GateStatus.FAILING)
    object.__setattr__(gate, "failure_context", "late hidden failure")

    with pytest.raises(IndependentScoringError) as caught:
        _ = receipt.receipt_identity

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert caught.value.context == {"field": "independent_scoring_receipt"}
    assert original_identity


def test_rejection_receipt_is_deterministic_and_records_zero_partial_scoring_state() -> None:
    rejected_input = receipt_values(gates=gates(failing="contract_contradiction"))
    created: IndependentScoringReceipt | None = None
    try:
        created = IndependentScoringReceipt(**rejected_input)
    except IndependentScoringError as error:
        first = build_rejection_receipt(error, rejected_input=rejected_input)
        second = build_rejection_receipt(error, rejected_input=rejected_input)
    else:  # pragma: no cover - the governed input must reject
        raise AssertionError("expected non-compensable gate rejection")

    assert created is None
    assert first == second
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert first["failure_code"] == "NON_COMPENSABLE_GATE_FAILED"
    assert first["outcome"] == "REJECTED_NO_SCORING_RECEIPT"
    assert first["production_threshold_defined"] is False
    assert first["production_ready"] is False
    assert first["certified"] is False


def test_changed_failed_gate_changes_deterministic_rejection_identity() -> None:
    def rejection(failed_gate: str) -> dict[str, object]:
        rejected_input = receipt_values(gates=gates(failing=failed_gate))
        try:
            IndependentScoringReceipt(**rejected_input)
        except IndependentScoringError as error:
            return build_rejection_receipt(error, rejected_input=rejected_input)
        raise AssertionError("expected rejection")

    first = rejection("wrong_atomicity")
    second = rejection("anti_goal_violation")

    assert first["rejection_identity"] != second["rejection_identity"]
    assert first["rejected_input_identity"] != second["rejected_input_identity"]


def test_gate_status_cannot_be_a_free_form_string() -> None:
    with pytest.raises(IndependentScoringError) as caught:
        GateResult(
            gate_id="critical_unsupported_decision",
            status="passing",  # type: ignore[arg-type]
            evidence_refs=(digest("gate-evidence"),),
        )

    assert caught.value.code == "INVALID_GOVERNED_TYPE"


def test_gate_evidence_identity_tamper_is_rejected() -> None:
    valid = GateResult(
        gate_id="critical_unsupported_decision",
        status=GateStatus.PASSING,
        evidence_refs=(digest("gate-evidence"),),
    )
    object.__setattr__(valid, "evidence_refs", ("mutable-label",))

    with pytest.raises(IndependentScoringError) as caught:
        valid.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert caught.value.context == {"field": "gate_result"}


def test_valid_receipt_keeps_gate_results_independent_and_composite_non_authoritative() -> None:
    receipt = IndependentScoringReceipt(**receipt_values())
    payload = receipt.as_dict()

    assert tuple(item["gate_id"] for item in payload["gates"]) == NON_COMPENSABLE_GATES
    assert all(item["status"] == "passing" for item in payload["gates"])
    assert payload["composite_trend_basis_points"] == 10_000
    assert payload["composite_trend_authoritative"] is False
    assert payload["evidence_gate_closed"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False
