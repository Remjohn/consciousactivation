from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256

from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.evaluation.fresh_context_controls import (
    CaseClass,
    DimensionScore,
    EvaluationArm,
    EvaluationCase,
    EvaluationLayer,
    FreshContextEvidence,
    LayerSuite,
    TrialResult,
    canonical_json_bytes,
    compile_trial_plan,
    evaluate_fresh_contexts,
    fresh_context_construction_receipt_sha256,
    fresh_context_evaluator_input_sha256,
)


APPROVAL_ACTOR = "offline-independent-approval-policy"
NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def digest(label: str) -> str:
    return sha256(label.encode()).hexdigest()


def case(case_id: str, layer: EvaluationLayer, case_class: CaseClass) -> EvaluationCase:
    return EvaluationCase(
        case_id=case_id,
        layer=layer,
        case_class=case_class,
        governed_input_sha256=digest(f"input:{case_id}"),
        output_contract_sha256=digest(f"output:{case_id}"),
        budget_contract_sha256=digest(f"budget:{case_id}"),
        expected_behavior_sha256=digest(f"expected:{case_id}"),
        dimensions=("fidelity", "rule_application"),
        authority_sha256=digest(f"authority:{case_id}"),
        provenance_sha256=digest(f"provenance:{case_id}"),
    )


def plan():
    cases = (
        case("case-01", EvaluationLayer.CANONICAL_SKILL, CaseClass.POSITIVE_APPLICATION),
        case("case-02", EvaluationLayer.CANONICAL_SKILL, CaseClass.NEAR_MISS),
        case("case-03", EvaluationLayer.CANONICAL_SKILL, CaseClass.COUNTEREXAMPLE),
        case("case-04", EvaluationLayer.HARNESS_ADAPTATION, CaseClass.MISSING_EVIDENCE),
        case("case-05", EvaluationLayer.COMPOSITION_RECIPE, CaseClass.CONTRADICTION),
        case("case-06", EvaluationLayer.JIT_CAPSULE, CaseClass.TEMPTING_IRRELEVANT_CONTEXT),
        case("case-07", EvaluationLayer.END_TO_END_PHASE, CaseClass.RULE_VIOLATION_PRESSURE),
    )
    suites = tuple(
        LayerSuite(
            suite_version="1.0.0",
            layer=layer,
            cases=tuple(item for item in cases if item.layer is layer),
        )
        for layer in EvaluationLayer
    )
    return compile_trial_plan(
        plan_version="1.0.0",
        suites=suites,
        repetition_count=3,
        evaluator_version="offline-evaluator-v1",
        benchmark_version="repository-synthetic-v1",
        authority_sha256=digest("plan-authority"),
        provenance_sha256=digest("plan-provenance"),
    )


def results(trial_plan):
    output = []
    cases = {item.case_id: item for item in trial_plan.cases}
    for case_id, arm_value, repeat in trial_plan.expected_trial_keys:
        arm = EvaluationArm(arm_value)
        governed = arm is EvaluationArm.GOVERNED_CANDIDATE
        base = 8_000 if governed else 5_000
        evaluator_identity = f"evaluator:{case_id}:{arm.value}:{repeat}"
        evaluator_input_sha256 = fresh_context_evaluator_input_sha256(
            case=cases[case_id],
            arm=arm,
            repeat_index=repeat,
            evaluator_version=trial_plan.evaluator_version,
            evaluator_identity=evaluator_identity,
        )
        construction_receipt_sha256 = fresh_context_construction_receipt_sha256(
            case_sha256=cases[case_id].case_identity,
            case_id=case_id,
            arm=arm,
            repeat_index=repeat,
            evaluator_version=trial_plan.evaluator_version,
            evaluator_identity=evaluator_identity,
            evaluator_input_sha256=evaluator_input_sha256,
            generator_history=(),
            mutable_cache_entries=(),
        )
        context = FreshContextEvidence(
            case_sha256=cases[case_id].case_identity,
            case_id=case_id,
            arm=arm,
            repeat_index=repeat,
            evaluator_version=trial_plan.evaluator_version,
            evaluator_identity=evaluator_identity,
            evaluator_input_sha256=evaluator_input_sha256,
            generator_history=(),
            mutable_cache_entries=(),
            construction_receipt_sha256=construction_receipt_sha256,
        )
        output.append(
            TrialResult(
                plan_sha256=trial_plan.plan_identity,
                case_sha256=cases[case_id].case_identity,
                case_id=case_id,
                layer=cases[case_id].layer,
                arm=arm,
                repeat_index=repeat,
                fresh_context=context,
                output_sha256=digest(f"output:{case_id}:{arm.value}:{repeat}"),
                evaluator_version=trial_plan.evaluator_version,
                generator_identity=f"generator:{arm.value}",
                evaluator_identity=evaluator_identity,
                approval_authority_identity=APPROVAL_ACTOR,
                dimension_scores=(
                    DimensionScore("fidelity", base + repeat * 10),
                    DimensionScore("rule_application", base + repeat * 20),
                ),
                expected_behavior_passed=governed,
                result_provenance_sha256=digest(
                    f"result-provenance:{case_id}:{arm.value}:{repeat}"
                ),
            )
        )
    return output


def authority_for(trial_plan, *, actor_id: str = APPROVAL_ACTOR) -> AuthorityService:
    return AuthorityService(
        actors=(Actor(actor_id=actor_id, kind=ActorKind.HUMAN),),
        grants=(
            AuthorityGrant(
                actor_id=actor_id,
                actions=frozenset({Action.EVALUATE_FRESH_CONTEXTS}),
                resource_id=trial_plan.plan_identity,
                expires_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
            ),
        ),
    )


def evaluate(trial_plan, supplied):
    return evaluate_fresh_contexts(
        plan=trial_plan,
        results=supplied,
        authority=authority_for(trial_plan),
        approval_actor_id=APPROVAL_ACTOR,
        now=NOW,
    )


def test_compiles_all_layers_cases_arms_and_repetitions() -> None:
    trial_plan = plan()

    assert len(trial_plan.suites) == 5
    assert len(trial_plan.cases) == 7
    assert len(trial_plan.expected_trial_keys) == 42
    assert {item.case_class for item in trial_plan.cases} == set(CaseClass)


def test_evaluates_each_layer_independently_and_reports_only_deltas() -> None:
    trial_plan = plan()
    receipt = evaluate(trial_plan, results(trial_plan))

    assert [item.layer for item in receipt.layer_evaluations] == list(EvaluationLayer)
    assert all(item.status == "OFFLINE_DELTAS_COMPUTED_NO_INHERITED_LAYER_PASS" for item in receipt.layer_evaluations)
    assert all(
        comparison.candidate_minus_control_mean > 0
        for layer in receipt.layer_evaluations
        for comparison in layer.comparisons
    )
    assert all(
        comparison.control.trial_count == comparison.candidate.trial_count == 3
        for layer in receipt.layer_evaluations
        for comparison in layer.comparisons
    )
    payload = receipt.as_dict()
    assert payload["result_status"] == "OFFLINE_SYNTHETIC_STRUCTURAL_DELTAS_ONLY"
    assert payload["empirical_superiority_claimed"] is False
    assert payload["behavioral_improvement_proven"] is False
    assert payload["maturity_promoted"] is False
    assert payload["evidence_gate_closed"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False


def test_statistics_and_receipt_bytes_are_deterministic() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)

    first = evaluate(trial_plan, supplied)
    second = evaluate(trial_plan, reversed(supplied))

    assert first.receipt_identity == second.receipt_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    comparison = first.layer_evaluations[0].comparisons[0]
    assert comparison.control.mean_score.denominator != 0
    assert comparison.control.minimum_score <= comparison.control.mean_score
    assert comparison.control.variance >= 0
    assert comparison.control.failure_frequency == 1
    assert 0 <= comparison.control.confidence_estimate_basis_points <= 10_000


def test_success_observations_are_typed_and_attributable() -> None:
    trial_plan = plan()
    receipt = evaluate(trial_plan, results(trial_plan))

    assert [item.event_type for item in receipt.observations] == [
        "ST-08.01:OfflineTrialPlanValidated",
        "ST-08.01:OfflineEvaluationCompleted",
    ]
    assert receipt.observations[0].artifact_identity == trial_plan.plan_identity
    assert receipt.authority_sha256 == digest("plan-authority")
    assert receipt.provenance_sha256 == digest("plan-provenance")
