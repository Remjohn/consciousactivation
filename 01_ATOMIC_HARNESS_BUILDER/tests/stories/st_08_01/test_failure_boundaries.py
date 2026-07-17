from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.evaluation.fresh_context_controls import (
    CaseClass,
    DimensionScore,
    EvaluationArm,
    EvaluationLayer,
    FreshContextEvaluationError,
    FreshContextEvidence,
    LayerSuite,
    TrialPlan,
    build_rejection_evidence,
    evaluate_fresh_contexts,
    fresh_context_construction_receipt_sha256,
)
from tests.stories.st_08_01.test_fresh_context_evaluation import (
    APPROVAL_ACTOR,
    NOW,
    authority_for,
    digest,
    evaluate,
    plan,
    results,
)


def test_missing_control_or_repetition_fails_closed() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)

    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied[1:])

    assert caught.value.code == "INCOMPLETE_PAIRED_TRIALS"


def test_reused_context_fails_closed() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    with pytest.raises(FreshContextEvaluationError) as caught:
        replace(supplied[1], fresh_context=supplied[0].fresh_context)
    assert caught.value.code == "FRESH_CONTEXT_BINDING_MISMATCH"


def test_insufficient_repetitions_are_rejected() -> None:
    valid = plan()

    with pytest.raises(FreshContextEvaluationError) as caught:
        TrialPlan(
            plan_version=valid.plan_version,
            suites=valid.suites,
            repetition_count=2,
            evaluator_version=valid.evaluator_version,
            benchmark_version=valid.benchmark_version,
            authority_sha256=valid.authority_sha256,
            provenance_sha256=valid.provenance_sha256,
        )

    assert caught.value.code == "INSUFFICIENT_REPETITIONS"


def test_incomplete_case_class_coverage_is_rejected() -> None:
    valid = plan()
    last_suite = valid.suites[-1]
    replacement = LayerSuite(
        suite_version=last_suite.suite_version,
        layer=EvaluationLayer.END_TO_END_PHASE,
        cases=(replace(last_suite.cases[0], case_class=CaseClass.POSITIVE_APPLICATION),),
    )

    with pytest.raises(FreshContextEvaluationError) as caught:
        replace(valid, suites=valid.suites[:-1] + (replacement,))

    assert caught.value.code == "INCOMPLETE_CASE_CLASS_COVERAGE"


def test_case_ids_must_be_globally_unique_across_layers() -> None:
    valid = plan()
    duplicate = replace(
        valid.suites[1].cases[0],
        case_id=valid.suites[0].cases[0].case_id,
    )
    replacement = replace(valid.suites[1], cases=(duplicate,))

    with pytest.raises(FreshContextEvaluationError) as caught:
        replace(valid, suites=(valid.suites[0], replacement) + valid.suites[2:])

    assert caught.value.code == "DUPLICATE_CASE_ID_ACROSS_LAYERS"


def test_stale_case_and_dimension_drift_are_rejected() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    altered_case = digest("altered-case")
    original_context = supplied[0].fresh_context
    altered_context = replace(
        original_context,
        case_sha256=altered_case,
        construction_receipt_sha256=fresh_context_construction_receipt_sha256(
            case_sha256=altered_case,
            case_id=original_context.case_id,
            arm=original_context.arm,
            repeat_index=original_context.repeat_index,
            evaluator_version=original_context.evaluator_version,
            evaluator_identity=original_context.evaluator_identity,
            evaluator_input_sha256=original_context.evaluator_input_sha256,
            generator_history=(),
            mutable_cache_entries=(),
        ),
    )
    supplied[0] = replace(
        supplied[0],
        case_sha256=altered_case,
        fresh_context=altered_context,
    )
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "STALE_OR_ALTERED_CASE"

    supplied = results(trial_plan)
    supplied[0] = replace(
        supplied[0], dimension_scores=(supplied[0].dimension_scores[0],)
    )
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "RESULT_DIMENSION_DRIFT"


def test_generator_cannot_evaluate_or_solely_approve_own_output() -> None:
    trial_plan = plan()
    original = results(trial_plan)[0]

    with pytest.raises(FreshContextEvaluationError) as evaluator_error:
        replace(original, evaluator_identity=original.generator_identity)
    assert evaluator_error.value.code == "GENERATOR_CONTEXT_REUSED_BY_EVALUATOR"

    with pytest.raises(FreshContextEvaluationError) as authority_error:
        replace(original, approval_authority_identity=original.generator_identity)
    assert authority_error.value.code == "GENERATOR_IS_SOLE_APPROVER"


def test_boolean_values_cannot_masquerade_as_typed_integers() -> None:
    valid = plan()
    with pytest.raises(FreshContextEvaluationError) as repetitions:
        replace(valid, repetition_count=True)
    assert repetitions.value.code == "INVALID_REPETITION_COUNT"

    with pytest.raises(FreshContextEvaluationError) as score:
        DimensionScore("fidelity", True)
    assert score.value.code == "INVALID_DIMENSION_SCORE"

    with pytest.raises(FreshContextEvaluationError) as repeat:
        replace(results(valid)[0], repeat_index=True)
    assert repeat.value.code == "INVALID_REPEAT_INDEX"

    with pytest.raises(FreshContextEvaluationError) as expected_pass:
        replace(results(valid)[0], expected_behavior_passed=1)
    assert expected_pass.value.code == "INVALID_GOVERNED_TYPE"


def test_rejection_evidence_is_derived_from_exact_inputs_without_claiming_completion() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)[:-1]
    error = FreshContextEvaluationError("MISSING_CONTROL", "control is required")
    rejection = build_rejection_evidence(
        error,
        plan=trial_plan,
        results=supplied,
        approval_actor_id=APPROVAL_ACTOR,
    )
    repeated = build_rejection_evidence(
        error,
        plan=trial_plan,
        results=reversed(supplied),
        approval_actor_id=APPROVAL_ACTOR,
    )

    assert rejection.rejection_identity == repeated.rejection_identity
    assert rejection.observation.event_type == "ST-08.01:OfflineEvaluationRejected"
    assert rejection.observation.outcome == "REJECTED_NO_RECEIPT"
    assert rejection.observation.failure_code == "MISSING_CONTROL"
    assert rejection.as_dict()["production_ready"] is False


def test_fresh_context_requires_empty_history_cache_and_structural_claim_ceiling() -> None:
    original = results(plan())[0].fresh_context
    with pytest.raises(FreshContextEvaluationError) as history:
        replace(original, generator_history=("prior-message",))
    assert history.value.code == "NON_EMPTY_GENERATOR_HISTORY"
    with pytest.raises(FreshContextEvaluationError) as cache:
        replace(original, mutable_cache_entries=("cached-result",))
    assert cache.value.code == "NON_EMPTY_MUTABLE_CACHE"
    with pytest.raises(FreshContextEvaluationError) as isolation:
        replace(original, structural_isolation_only=False)
    assert isolation.value.code == "UNSUPPORTED_RUNTIME_ISOLATION_CLAIM"


def test_fresh_context_construction_receipt_rejects_arbitrary_hash_forgery() -> None:
    original = results(plan())[0].fresh_context
    with pytest.raises(FreshContextEvaluationError) as caught:
        replace(original, construction_receipt_sha256=digest("arbitrary-receipt"))
    assert caught.value.code == "FORGED_FRESH_CONTEXT_CONSTRUCTION_RECEIPT"


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("benchmark_version", "protected-benchmark-passed-v1"),
        ("evaluator_version", "certified-evaluator-v1"),
        ("plan_version", "production-ready-v1"),
    ),
)
def test_prohibited_maturity_and_certification_claims_are_rejected(field, value) -> None:
    valid = plan()
    with pytest.raises(FreshContextEvaluationError) as caught:
        replace(valid, **{field: value})
    assert caught.value.code == "PROHIBITED_MATURITY_OR_CERTIFICATION_CLAIM"


def test_strict_enum_types_reject_string_masquerades() -> None:
    trial_plan = plan()
    with pytest.raises(FreshContextEvaluationError) as case_layer:
        replace(trial_plan.cases[0], layer=EvaluationLayer.CANONICAL_SKILL.value)
    assert case_layer.value.code == "INVALID_GOVERNED_TYPE"
    with pytest.raises(FreshContextEvaluationError) as arm:
        replace(results(trial_plan)[0], arm=EvaluationArm.NO_GUIDANCE_CONTROL.value)
    assert arm.value.code == "INVALID_GOVERNED_TYPE"


@pytest.mark.parametrize(
    ("field_name", "mutated_value"),
    (("output_sha256", "not-a-sha256"), ("expected_behavior_passed", 1)),
)
def test_commit_boundary_rejects_object_setattr_trial_result_mutations(
    field_name, mutated_value
) -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    object.__setattr__(supplied[0], field_name, mutated_value)

    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


@pytest.mark.parametrize(
    ("field_name", "mutated_value"),
    (
        ("generator_history", ("generator-history",)),
        ("mutable_cache_entries", ("cached-output",)),
        ("structural_isolation_only", False),
    ),
)
def test_commit_boundary_rejects_object_setattr_fresh_context_mutations(
    field_name, mutated_value
) -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    object.__setattr__(supplied[0].fresh_context, field_name, mutated_value)

    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


@pytest.mark.parametrize("target", ("plan", "case", "suite", "score"))
def test_complete_commit_graph_rejects_nested_object_setattr_mutations(target) -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    authority = authority_for(trial_plan)
    if target == "plan":
        object.__setattr__(trial_plan, "repetition_count", True)
    elif target == "case":
        object.__setattr__(trial_plan.suites[0].cases[0], "layer", "canonical_skill")
    elif target == "suite":
        object.__setattr__(trial_plan.suites[0], "cases", list(trial_plan.suites[0].cases))
    else:
        object.__setattr__(supplied[0].dimension_scores[0], "score_basis_points", True)

    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate_fresh_contexts(
            plan=trial_plan,
            results=supplied,
            authority=authority,
            approval_actor_id=APPROVAL_ACTOR,
            now=NOW,
        )
    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_mutated_input_still_produces_deterministic_rejection_evidence_without_commit() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    object.__setattr__(supplied[0], "output_sha256", "not-a-sha256")
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)

    first = build_rejection_evidence(
        caught.value,
        plan=trial_plan,
        results=supplied,
        approval_actor_id=APPROVAL_ACTOR,
    )
    second = build_rejection_evidence(
        caught.value,
        plan=trial_plan,
        results=supplied,
        approval_actor_id=APPROVAL_ACTOR,
    )
    assert first.rejection_identity == second.rejection_identity
    assert first.as_dict()["result_status"] == "REJECTED_NO_EVALUATION_RECEIPT"
