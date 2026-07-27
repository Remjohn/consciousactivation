from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

import pytest

from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.evaluation.fresh_context_controls import (
    DimensionScore,
    EvaluationArm,
    FreshContextEvaluationError,
    build_rejection_evidence,
    canonical_json_bytes,
    evaluate_fresh_contexts,
    fresh_context_construction_receipt_sha256,
    validate_evaluation_receipt,
)
from tests.stories.st_08_01.test_fresh_context_evaluation import (
    APPROVAL_ACTOR,
    NOW,
    digest,
    evaluate,
    plan,
    results,
)


def test_each_arm_uses_the_same_case_contract_budget_and_dimensions() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    by_case = {}
    for result in supplied:
        by_case.setdefault(result.case_id, []).append(result)

    for case in trial_plan.cases:
        case_results = by_case[case.case_id]
        assert {item.arm for item in case_results} == set(EvaluationArm)
        assert {item.case_sha256 for item in case_results} == {case.case_identity}
        assert {
            tuple(score.dimension for score in item.dimension_scores)
            for item in case_results
        } == {case.dimensions}


def test_changed_governed_result_changes_receipt_identity() -> None:
    trial_plan = plan()
    original = results(trial_plan)
    changed = list(original)
    changed[0] = replace(
        changed[0],
        dimension_scores=(
            DimensionScore("fidelity", 4_000),
            DimensionScore("rule_application", 4_100),
        ),
        output_sha256=digest("changed-output"),
    )

    first = evaluate(trial_plan, original)
    second = evaluate(trial_plan, changed)

    assert first.receipt_identity != second.receipt_identity
    assert canonical_json_bytes(first.as_dict()) != canonical_json_bytes(second.as_dict())


def test_control_success_is_surfaced_without_skill_necessity_claim() -> None:
    trial_plan = plan()
    supplied = [replace(item, expected_behavior_passed=True) for item in results(trial_plan)]
    receipt = evaluate(trial_plan, supplied)

    assert all(
        comparison.control_target_failure_absent is True
        and comparison.skill_necessity_signal
        == "CONTROL_SUCCEEDS_NO_SKILL_NECESSITY_ATTRIBUTION"
        for layer in receipt.layer_evaluations
        for comparison in layer.comparisons
    )
    assert receipt.as_dict()["behavioral_improvement_proven"] is False


def test_evaluator_version_and_plan_authority_drift_fail_closed() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    original_context = supplied[0].fresh_context
    drifted_context = replace(
        original_context,
        evaluator_version="different-evaluator",
        construction_receipt_sha256=fresh_context_construction_receipt_sha256(
            case_sha256=original_context.case_sha256,
            case_id=original_context.case_id,
            arm=original_context.arm,
            repeat_index=original_context.repeat_index,
            evaluator_version="different-evaluator",
            evaluator_identity=original_context.evaluator_identity,
            evaluator_input_sha256=original_context.evaluator_input_sha256,
            generator_history=(),
            mutable_cache_entries=(),
        ),
    )
    supplied[0] = replace(
        supplied[0],
        evaluator_version="different-evaluator",
        fresh_context=drifted_context,
    )
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "EVALUATOR_VERSION_DRIFT"

    supplied = results(trial_plan)
    supplied[0] = replace(supplied[0], plan_sha256=digest("different-plan"))
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "STALE_OR_ALTERED_PLAN"


def test_receipt_preserves_authority_provenance_and_nonproduction_ceiling() -> None:
    trial_plan = plan()
    receipt = evaluate(trial_plan, results(trial_plan))
    payload = receipt.as_dict()

    assert payload["authority_sha256"] == trial_plan.authority_sha256
    assert payload["provenance_sha256"] == trial_plan.provenance_sha256
    assert payload["benchmark_version"] == "repository-synthetic-v1"
    assert payload["evaluator_version"] == "offline-evaluator-v1"
    assert payload["evidence_gate_closed"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False
    assert payload["fresh_context_claim"] == "STRUCTURAL_ISOLATION_ONLY_NOT_RUNTIME_PROOF"


def test_deny_by_default_authority_requires_exact_registered_actor_grant_and_resource() -> None:
    trial_plan = plan()
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate_fresh_contexts(
            plan=trial_plan,
            results=results(trial_plan),
            authority=AuthorityService(actors=(), grants=()),
            approval_actor_id=APPROVAL_ACTOR,
            now=NOW,
        )
    assert caught.value.code == "EVALUATION_AUTHORITY_DENIED"


def test_wildcard_only_authority_grant_is_rejected_at_evaluation_commit_boundary() -> None:
    trial_plan = plan()
    wildcard_only = AuthorityService(
        actors=(Actor(actor_id=APPROVAL_ACTOR, kind=ActorKind.HUMAN),),
        grants=(
            AuthorityGrant(
                actor_id=APPROVAL_ACTOR,
                actions=frozenset({Action.EVALUATE_FRESH_CONTEXTS}),
                resource_id="*",
                expires_at=datetime(2030, 1, 1, tzinfo=timezone.utc),
            ),
        ),
    )
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate_fresh_contexts(
            plan=trial_plan,
            results=results(trial_plan),
            authority=wildcard_only,
            approval_actor_id=APPROVAL_ACTOR,
            now=NOW,
        )
    assert caught.value.code == "EVALUATION_AUTHORITY_DENIED"


def test_forged_receipt_cannot_validate_against_governed_plan_and_results() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    receipt = evaluate(trial_plan, supplied)
    forged = replace(receipt, provenance_sha256=digest("forged-provenance"))

    with pytest.raises(FreshContextEvaluationError) as caught:
        validate_evaluation_receipt(
            receipt=forged,
            plan=trial_plan,
            results=supplied,
            approval_actor_id=APPROVAL_ACTOR,
        )
    assert caught.value.code == "FORGED_OR_DRIFTED_EVALUATION_RECEIPT"


def test_altered_evaluator_input_binding_is_rejected() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    original_context = supplied[0].fresh_context
    altered_input = digest("altered-evaluator-input")
    altered_context = replace(
        original_context,
        evaluator_input_sha256=altered_input,
        construction_receipt_sha256=fresh_context_construction_receipt_sha256(
            case_sha256=original_context.case_sha256,
            case_id=original_context.case_id,
            arm=original_context.arm,
            repeat_index=original_context.repeat_index,
            evaluator_version=original_context.evaluator_version,
            evaluator_identity=original_context.evaluator_identity,
            evaluator_input_sha256=altered_input,
            generator_history=(),
            mutable_cache_entries=(),
        ),
    )
    supplied[0] = replace(supplied[0], fresh_context=altered_context)
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "ALTERED_EVALUATOR_INPUT"


def test_rejection_observation_identity_and_exact_evidence_refs_cannot_be_forged() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)[:-1]
    rejection = build_rejection_evidence(
        FreshContextEvaluationError("INCOMPLETE_PAIRED_TRIALS", "missing result"),
        plan=trial_plan,
        results=supplied,
        approval_actor_id=APPROVAL_ACTOR,
    )
    with pytest.raises(FreshContextEvaluationError) as artifact_error:
        replace(
            rejection,
            observation=replace(
                rejection.observation,
                artifact_identity=digest("forged-rejected-input"),
            ),
        )
    assert artifact_error.value.code == "INVALID_REJECTION_EVIDENCE"

    with pytest.raises(FreshContextEvaluationError) as refs_error:
        replace(
            rejection,
            observation=replace(
                rejection.observation,
                evidence_refs=(
                    rejection.plan_identity,
                    rejection.results_identity,
                    digest("forged-authority"),
                ),
            ),
        )
    assert refs_error.value.code == "INVALID_REJECTION_EVIDENCE"


def test_receipt_observations_and_result_identity_collection_cannot_be_forged() -> None:
    trial_plan = plan()
    receipt = evaluate(trial_plan, results(trial_plan))

    with pytest.raises(FreshContextEvaluationError) as result_type_error:
        replace(receipt, result_identities=list(receipt.result_identities))
    assert result_type_error.value.code == "INVALID_GOVERNED_TYPE"

    with pytest.raises(FreshContextEvaluationError) as plan_observation_error:
        replace(
            receipt,
            observations=(
                replace(receipt.observations[0], artifact_identity=digest("forged-plan")),
                receipt.observations[1],
            ),
        )
    assert plan_observation_error.value.code == "FORGED_EVALUATION_RECEIPT"

    with pytest.raises(FreshContextEvaluationError) as completion_error:
        replace(
            receipt,
            observations=(
                receipt.observations[0],
                replace(
                    receipt.observations[1],
                    evidence_refs=(digest("forged-plan-ref"),),
                ),
            ),
        )
    assert completion_error.value.code == "FORGED_EVALUATION_RECEIPT"


def test_private_construction_anchor_blocks_public_self_reseal_bypass() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)
    score = supplied[0].dimension_scores[0]
    object.__setattr__(score, "score_basis_points", score.score_basis_points - 1)

    with pytest.raises(AttributeError):
        object.__setattr__(score, "_constructed_identity", canonical_json_bytes(score.as_dict()))
    with pytest.raises(AttributeError):
        object.__setattr__(supplied[0], "_constructed_identity", digest("self-resealed-parent"))
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate(trial_plan, supplied)
    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_authority_service_subclass_cannot_override_exact_commit_authority() -> None:
    class AllowAllAuthority(AuthorityService):
        def authorize_exact(self, **kwargs):
            return Actor(actor_id=APPROVAL_ACTOR, kind=ActorKind.HUMAN)

    trial_plan = plan()
    forged_authority = AllowAllAuthority(actors=(), grants=())
    with pytest.raises(FreshContextEvaluationError) as caught:
        evaluate_fresh_contexts(
            plan=trial_plan,
            results=results(trial_plan),
            authority=forged_authority,
            approval_actor_id=APPROVAL_ACTOR,
            now=NOW,
        )
    assert caught.value.code == "INVALID_AUTHORITY_SERVICE"


def test_object_setattr_forged_rejection_and_observation_fail_deep_validation() -> None:
    trial_plan = plan()
    supplied = results(trial_plan)[:-1]
    rejection = build_rejection_evidence(
        FreshContextEvaluationError("INCOMPLETE_PAIRED_TRIALS", "missing result"),
        plan=trial_plan,
        results=supplied,
        approval_actor_id=APPROVAL_ACTOR,
    )
    object.__setattr__(
        rejection.observation, "artifact_identity", digest("forged-observation-artifact")
    )
    with pytest.raises(FreshContextEvaluationError) as observation_error:
        rejection.as_dict()
    assert observation_error.value.code == "MUTATED_GOVERNED_OBJECT"

    rejection = build_rejection_evidence(
        FreshContextEvaluationError("INCOMPLETE_PAIRED_TRIALS", "missing result"),
        plan=trial_plan,
        results=supplied,
        approval_actor_id=APPROVAL_ACTOR,
    )
    object.__setattr__(rejection, "failure_code", "FORGED_FAILURE")
    object.__setattr__(rejection.observation, "failure_code", "FORGED_FAILURE")
    with pytest.raises(FreshContextEvaluationError) as rejection_error:
        _ = rejection.rejection_identity
    assert rejection_error.value.code == "MUTATED_GOVERNED_OBJECT"
