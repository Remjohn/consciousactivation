from __future__ import annotations

from dataclasses import replace
import hashlib
import os
from pathlib import Path
import subprocess
import sys

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
    ScoringAction,
    ScoringAuthority,
    ScoringCommand,
    build_rejection_receipt,
    canonical_json_bytes,
    canonical_sha256,
    compute_issue_payload_sha256,
    invalidate_scoring_receipt,
    issue_independent_scoring_receipt,
    rollback_scoring_receipt,
    validate_repeat_receipt,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def authority(
    *actions: ScoringAction,
    authority_id: str = "od-am-001-st-08.03-development-authority",
) -> ScoringAuthority:
    return ScoringAuthority(
        authority_id=authority_id,
        authority_version="1.0.0-development",
        authority_sha256=digest(f"{authority_id}-bytes"),
        permitted_actions=actions or (
            ScoringAction.ISSUE,
            ScoringAction.INVALIDATE,
            ScoringAction.ROLLBACK,
        ),
    )


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


def scorecards() -> tuple[DimensionScorecard, ...]:
    return tuple(
        DimensionScorecard(
            dimension=dimension,
            status=DimensionStatus.PASSING,
            score_basis_points=7_500 + index,
            evidence_refs=(digest(f"dimension-evidence-{dimension}"),),
        )
        for index, dimension in enumerate(BASE_DIMENSIONS)
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


def gates() -> tuple[GateResult, ...]:
    return tuple(
        GateResult(
            gate_id=gate_id,
            status=GateStatus.PASSING,
            evidence_refs=(digest(f"gate-evidence-{gate_id}"),),
        )
        for gate_id in NON_COMPENSABLE_GATES
    )


def stability() -> RepeatedRunSummary:
    return RepeatedRunSummary(
        repetition_identities=(digest("repeat-41"), digest("repeat-42"), digest("repeat-43")),
        distributions=tuple(
            DimensionDistribution(
                dimension=dimension,
                scores_basis_points=(7_500 + index, 7_500 + index, 7_500 + index),
            )
            for index, dimension in enumerate(BASE_DIMENSIONS)
        ),
        dominant_failure_patterns=(),
    )


def issue_inputs(**changes: object) -> dict[str, object]:
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
        "scorecards": scorecards(),
        "mutations": (mutation(),),
        "gates": gates(),
        "stability_summary": stability(),
        "downstream_results": (),
        "observations": (
            "ST-08.03:IndependentDimensionsScored",
            "ST-08.03:NonCompensableGatesEvaluated",
        ),
        "protected_label_accessed": False,
        "composite_trend_basis_points": 7_503,
    }
    values.update(changes)
    return values


def command(
    inputs: dict[str, object],
    auth: ScoringAuthority,
    *,
    command_id: str = "issue-independent-scoring-v1",
    action: ScoringAction = ScoringAction.ISSUE,
    resource_id: str | None = None,
    payload_sha256: str | None = None,
    expected_authority_identity: str | None = None,
) -> ScoringCommand:
    if payload_sha256 is None:
        if action is ScoringAction.ISSUE:
            payload_sha256 = compute_issue_payload_sha256(**inputs)
        else:
            raise AssertionError("transition commands require an explicit payload hash")
    return ScoringCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id or str(inputs["evaluated_artifact_sha256"]),
        payload_sha256=payload_sha256,
        expected_authority_identity=expected_authority_identity or auth.authority_identity,
    )


def valid_receipt(
    *,
    inputs: dict[str, object] | None = None,
    auth: ScoringAuthority | None = None,
    issue_command: ScoringCommand | None = None,
) -> IndependentScoringReceipt:
    governed_inputs = inputs or issue_inputs()
    governed_authority = auth or authority()
    governed_command = issue_command or command(governed_inputs, governed_authority)
    return issue_independent_scoring_receipt(
        **governed_inputs,
        command=governed_command,
        authority=governed_authority,
    )


def transition_command(
    receipt: IndependentScoringReceipt,
    auth: ScoringAuthority,
    *,
    action: ScoringAction,
    payload: dict[str, object],
    command_id: str,
    resource_id: str | None = None,
    expected_authority_identity: str | None = None,
) -> ScoringCommand:
    return ScoringCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id or receipt.receipt_identity,
        payload_sha256=canonical_sha256(payload),
        expected_authority_identity=expected_authority_identity or auth.authority_identity,
    )


def test_issue_records_exact_attributable_command_and_authority() -> None:
    inputs = issue_inputs()
    auth = authority()
    cmd = command(inputs, auth)

    receipt = valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)

    assert receipt.command_identity == cmd.command_identity
    assert receipt.authority_identity == auth.authority_identity
    assert receipt.evaluated_artifact_sha256 == cmd.resource_id
    assert receipt.as_dict()["observations"] == [
        "ST-08.03:IndependentDimensionsScored",
        "ST-08.03:NonCompensableGatesEvaluated",
    ]


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"action": ScoringAction.ROLLBACK}, "COMMAND_ACTION_MISMATCH"),
        ({"resource_id": digest("wrong-resource")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        ({"expected_authority_identity": digest("other-authority")}, "AUTHORITY_IDENTITY_MISMATCH"),
    ),
)
def test_issue_fails_closed_on_command_or_authority_binding_drift(
    change: dict[str, object], expected_code: str
) -> None:
    inputs = issue_inputs()
    auth = authority()
    cmd = command(inputs, auth)
    cmd = replace(cmd, **change)
    issued: IndependentScoringReceipt | None = None

    with pytest.raises(IndependentScoringError) as caught:
        issued = valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)

    assert caught.value.code == expected_code
    assert issued is None


def test_issue_requires_an_authority_that_grants_the_issue_action() -> None:
    inputs = issue_inputs()
    auth = authority(ScoringAction.INVALIDATE)
    cmd = command(inputs, auth)

    with pytest.raises(IndependentScoringError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)

    assert caught.value.code == "UNAUTHORIZED_SCORING_ACTION"


def test_identical_repeat_is_idempotent_and_returns_the_original_receipt() -> None:
    inputs = issue_inputs()
    auth = authority()
    cmd = command(inputs, auth)
    existing = valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)
    candidate = valid_receipt(inputs=issue_inputs(), auth=authority(), issue_command=command(issue_inputs(), authority()))

    assert candidate.receipt_identity == existing.receipt_identity
    assert validate_repeat_receipt(existing, candidate) is existing


def test_conflicting_repeat_command_payload_fails_closed() -> None:
    inputs = issue_inputs()
    auth = authority()
    existing = valid_receipt(
        inputs=inputs,
        auth=auth,
        issue_command=command(inputs, auth),
    )
    conflicting_command = command(
        inputs,
        auth,
        command_id="same-resource-different-command",
    )
    candidate = valid_receipt(
        inputs=inputs,
        auth=auth,
        issue_command=conflicting_command,
    )

    with pytest.raises(IndependentScoringError) as caught:
        validate_repeat_receipt(existing, candidate)

    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_identical_inputs_are_byte_equal_in_a_fresh_python_process() -> None:
    repository = Path(__file__).resolve().parents[3]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(repository / "src"), str(repository), environment.get("PYTHONPATH", ""))
    )
    script = (
        "from tests.stories.st_08_03.test_lineage_determinism_and_rollback "
        "import valid_receipt; "
        "from cmf_builder.evaluation.independent_scoring import canonical_json_bytes; "
        "import sys; sys.stdout.buffer.write(canonical_json_bytes(valid_receipt().as_dict()))"
    )

    fresh_bytes = subprocess.check_output(
        [sys.executable, "-c", script],
        cwd=repository,
        env=environment,
    )

    assert fresh_bytes == canonical_json_bytes(valid_receipt().as_dict())


def test_changed_governed_lineage_produces_a_new_immutable_receipt_identity() -> None:
    original = valid_receipt()
    changed_inputs = issue_inputs(source_ir_sha256=digest("source-ir-v2"))
    auth = authority()
    changed = valid_receipt(
        inputs=changed_inputs,
        auth=auth,
        issue_command=command(changed_inputs, auth, command_id="issue-v2"),
    )

    assert changed.receipt_identity != original.receipt_identity
    assert changed.source_ir_sha256 != original.source_ir_sha256


def test_selective_invalidation_records_only_exact_changed_lineage() -> None:
    receipt = valid_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    changed = (receipt.source_ir_sha256, receipt.mutations[0].mutation_identity)
    sorted_changed = tuple(sorted(changed))
    auth = authority(ScoringAction.INVALIDATE)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.INVALIDATE,
        payload={"changed_identities": list(sorted_changed)},
        command_id="invalidate-affected-lineage-v1",
    )

    transition = invalidate_scoring_receipt(
        receipt,
        reversed(changed),
        command=cmd,
        authority=auth,
    )

    assert transition.action is ScoringAction.INVALIDATE
    assert transition.changed_identities == sorted_changed
    assert transition.prior_receipt_sha256 == receipt.receipt_identity
    assert transition.command_identity == cmd.command_identity
    assert transition.authority_identity == auth.authority_identity
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


def test_unrelated_invalidation_identity_fails_without_a_transition_receipt() -> None:
    receipt = valid_receipt()
    unrelated = digest("unrelated-descendant")
    auth = authority(ScoringAction.INVALIDATE)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.INVALIDATE,
        payload={"changed_identities": [unrelated]},
        command_id="invalidate-unrelated",
    )
    transition = None

    with pytest.raises(IndependentScoringError) as caught:
        transition = invalidate_scoring_receipt(
            receipt,
            (unrelated,),
            command=cmd,
            authority=auth,
        )

    assert caught.value.code == "UNRELATED_INVALIDATION_INPUT"
    assert caught.value.context == {"identities": (unrelated,)}
    assert transition is None


@pytest.mark.parametrize(
    ("command_change", "expected_code"),
    (
        ({"resource_id": digest("wrong-resource")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        ({"expected_authority_identity": digest("wrong-authority")}, "AUTHORITY_IDENTITY_MISMATCH"),
    ),
)
def test_invalidation_requires_exact_authority_resource_and_payload(
    command_change: dict[str, object], expected_code: str
) -> None:
    receipt = valid_receipt()
    changed = (receipt.source_ir_sha256,)
    auth = authority(ScoringAction.INVALIDATE)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.INVALIDATE,
        payload={"changed_identities": list(changed)},
        command_id="invalidate-boundary-test",
    )

    with pytest.raises(IndependentScoringError) as caught:
        invalidate_scoring_receipt(
            receipt,
            changed,
            command=replace(cmd, **command_change),
            authority=auth,
        )

    assert caught.value.code == expected_code


def test_invalidation_rejects_authority_without_invalidate_grant() -> None:
    receipt = valid_receipt()
    changed = (receipt.source_ir_sha256,)
    auth = authority(ScoringAction.ISSUE)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.INVALIDATE,
        payload={"changed_identities": list(changed)},
        command_id="invalidate-without-grant",
    )

    with pytest.raises(IndependentScoringError) as caught:
        invalidate_scoring_receipt(receipt, changed, command=cmd, authority=auth)

    assert caught.value.code == "UNAUTHORIZED_SCORING_ACTION"


def test_rollback_is_attributable_non_destructive_and_hash_bound() -> None:
    receipt = valid_receipt()
    original_identity = receipt.receipt_identity
    original_bytes = canonical_json_bytes(receipt.as_dict())
    target = digest("historical-scoring-receipt")
    auth = authority(ScoringAction.ROLLBACK)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.ROLLBACK,
        payload={"rollback_target_sha256": target},
        command_id="rollback-scoring-v1",
    )

    rollback = rollback_scoring_receipt(
        receipt,
        target,
        command=cmd,
        authority=auth,
    )

    assert rollback.action is ScoringAction.ROLLBACK
    assert rollback.prior_receipt_sha256 == original_identity
    assert rollback.rollback_target_sha256 == target
    assert rollback.changed_identities == ()
    assert rollback.command_identity == cmd.command_identity
    assert rollback.authority_identity == auth.authority_identity
    assert receipt.receipt_identity == original_identity
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


def test_identical_invalidation_and_rollback_commands_are_deterministic() -> None:
    receipt = valid_receipt()
    changed = (receipt.case_identity_sha256, receipt.provenance_sha256)
    sorted_changed = tuple(sorted(changed))
    invalidation_authority = authority(ScoringAction.INVALIDATE)
    invalidation_command = transition_command(
        receipt,
        invalidation_authority,
        action=ScoringAction.INVALIDATE,
        payload={"changed_identities": list(sorted_changed)},
        command_id="invalidate-deterministic",
    )
    first_invalidation = invalidate_scoring_receipt(
        receipt,
        changed,
        command=invalidation_command,
        authority=invalidation_authority,
    )
    second_invalidation = invalidate_scoring_receipt(
        receipt,
        changed,
        command=invalidation_command,
        authority=invalidation_authority,
    )
    target = digest("historical-target")
    rollback_authority = authority(ScoringAction.ROLLBACK)
    rollback_command = transition_command(
        receipt,
        rollback_authority,
        action=ScoringAction.ROLLBACK,
        payload={"rollback_target_sha256": target},
        command_id="rollback-deterministic",
    )
    first_rollback = rollback_scoring_receipt(
        receipt,
        target,
        command=rollback_command,
        authority=rollback_authority,
    )
    second_rollback = rollback_scoring_receipt(
        receipt,
        target,
        command=rollback_command,
        authority=rollback_authority,
    )

    assert first_invalidation.transition_identity == second_invalidation.transition_identity
    assert canonical_json_bytes(first_invalidation.as_dict()) == canonical_json_bytes(
        second_invalidation.as_dict()
    )
    assert first_rollback.transition_identity == second_rollback.transition_identity
    assert canonical_json_bytes(first_rollback.as_dict()) == canonical_json_bytes(
        second_rollback.as_dict()
    )


@pytest.mark.parametrize(
    ("action", "payload", "expected_code"),
    (
        (
            ScoringAction.ROLLBACK,
            {"rollback_target_sha256": digest("target")},
            "UNAUTHORIZED_SCORING_ACTION",
        ),
    ),
)
def test_rollback_requires_attributable_authority(
    action: ScoringAction, payload: dict[str, object], expected_code: str
) -> None:
    receipt = valid_receipt()
    target = str(payload["rollback_target_sha256"])
    auth = authority(ScoringAction.ISSUE)
    cmd = transition_command(
        receipt,
        auth,
        action=action,
        payload=payload,
        command_id="rollback-without-grant",
    )

    with pytest.raises(IndependentScoringError) as caught:
        rollback_scoring_receipt(receipt, target, command=cmd, authority=auth)

    assert caught.value.code == expected_code


def test_rollback_payload_conflict_fails_with_zero_partial_transition() -> None:
    receipt = valid_receipt()
    target = digest("historical-target")
    auth = authority(ScoringAction.ROLLBACK)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.ROLLBACK,
        payload={"rollback_target_sha256": digest("different-target")},
        command_id="rollback-payload-conflict",
    )
    transition = None

    with pytest.raises(IndependentScoringError) as caught:
        transition = rollback_scoring_receipt(
            receipt,
            target,
            command=cmd,
            authority=auth,
        )

    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"
    assert transition is None


def test_post_construction_lineage_tamper_blocks_transition_and_identity() -> None:
    receipt = valid_receipt()
    original_source = receipt.source_ir_sha256
    object.__setattr__(receipt, "source_ir_sha256", digest("forged-source-ir"))
    auth = authority(ScoringAction.INVALIDATE)
    cmd = ScoringCommand(
        command_id="invalidate-tampered-receipt",
        action=ScoringAction.INVALIDATE,
        resource_id=digest("untrusted-resource"),
        payload_sha256=canonical_sha256({"changed_identities": [original_source]}),
        expected_authority_identity=auth.authority_identity,
    )

    with pytest.raises(IndependentScoringError) as identity_error:
        _ = receipt.receipt_identity
    with pytest.raises(IndependentScoringError) as transition_error:
        invalidate_scoring_receipt(
            receipt,
            (original_source,),
            command=cmd,
            authority=auth,
        )

    assert identity_error.value.code == "MUTATED_GOVERNED_OBJECT"
    assert transition_error.value.code == "MUTATED_GOVERNED_OBJECT"


def test_nested_scorecard_tamper_blocks_parent_receipt_replay() -> None:
    receipt = valid_receipt()
    scorecard = receipt.scorecards[0]
    original_identity = receipt.receipt_identity
    object.__setattr__(scorecard, "score_basis_points", 9_999)

    with pytest.raises(IndependentScoringError) as caught:
        validate_repeat_receipt(receipt, receipt)

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert original_identity


def test_transition_receipt_tamper_is_detected() -> None:
    receipt = valid_receipt()
    target = digest("historical-target")
    auth = authority(ScoringAction.ROLLBACK)
    cmd = transition_command(
        receipt,
        auth,
        action=ScoringAction.ROLLBACK,
        payload={"rollback_target_sha256": target},
        command_id="rollback-before-tamper",
    )
    transition = rollback_scoring_receipt(receipt, target, command=cmd, authority=auth)
    object.__setattr__(transition, "rollback_target_sha256", digest("forged-target"))

    with pytest.raises(IndependentScoringError) as caught:
        transition.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert caught.value.context == {"field": "scoring_transition_receipt"}


def test_authority_rejection_receipt_is_deterministic_and_no_receipt_is_issued() -> None:
    inputs = issue_inputs()
    auth = authority(ScoringAction.INVALIDATE)
    cmd = command(inputs, auth)
    issued: IndependentScoringReceipt | None = None
    try:
        issued = valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)
    except IndependentScoringError as error:
        rejected_input = {"command": cmd, "authority": auth, "inputs": inputs}
        first = build_rejection_receipt(error, rejected_input=rejected_input)
        second = build_rejection_receipt(error, rejected_input=rejected_input)
    else:  # pragma: no cover - authority intentionally does not grant ISSUE
        raise AssertionError("expected authority rejection")

    assert issued is None
    assert first == second
    assert first["failure_code"] == "UNAUTHORIZED_SCORING_ACTION"
    assert first["outcome"] == "REJECTED_NO_SCORING_RECEIPT"
    assert first["production_ready"] is False
    assert first["certified"] is False
