from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.selective_repair import (
    EscalationTrigger,
    LocalRerunResult,
    LocalRerunStatus,
    RepairAction,
    RepairAuthority,
    RepairAuthorityStatus,
    RepairCommand,
    SelectiveRepairError,
    build_repair_rejection_receipt,
    compute_commit_payload_sha256,
    compute_escalation_payload_sha256,
    issue_repair_commit_receipt,
    issue_repair_escalation_receipt,
)
from tests.stories.st_08_05.test_accepted_diagnosis_and_repair_scope import (
    authority,
    compile_candidate,
    command,
    digest,
)
from tests.stories.st_08_05.test_affected_descendants_and_targeted_regression import (
    compile_plan,
)


def lifecycle_authority(
    *actions: RepairAction,
    status: RepairAuthorityStatus = RepairAuthorityStatus.ACTIVE,
) -> RepairAuthority:
    return RepairAuthority(
        authority_id="od-am-001-st-08.05-lifecycle-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-08.05-lifecycle-authority-bytes"),
        permitted_actions=actions
        or (
            RepairAction.COMMIT_CANDIDATE,
            RepairAction.ESCALATE,
        ),
        status=status,
    )


def local_results(plan, *, status_by_suite: dict[str, LocalRerunStatus] | None = None):
    statuses = status_by_suite or {}
    return tuple(
        LocalRerunResult(
            suite_id=requirement.suite_id,
            status=statuses.get(requirement.suite_id, LocalRerunStatus.PASS),
            result_sha256=digest(
                f"{requirement.suite_id}:{statuses.get(requirement.suite_id, LocalRerunStatus.PASS).value}"
            ),
        )
        for requirement in plan.requirements
    )


def commit_inputs(*, candidate=None, plan=None, results=None):
    governed_candidate = candidate or compile_candidate()
    governed_plan = plan or compile_plan()
    assert governed_plan.repair_candidate_identity == governed_candidate.candidate_identity
    return {
        "candidate": governed_candidate,
        "plan": governed_plan,
        "results": results if results is not None else local_results(governed_plan),
        "observations": (
            "ST-08.05:TargetedRegressionsVerified",
            "ST-08.05:OutcomeVerified",
        ),
    }


def commit_receipt(*, inputs=None, governed_authority=None, governed_command=None):
    values = inputs or commit_inputs()
    auth = governed_authority or lifecycle_authority(RepairAction.COMMIT_CANDIDATE)
    cmd = governed_command or command(
        action=RepairAction.COMMIT_CANDIDATE,
        resource_id=values["candidate"].candidate_identity,
        payload_sha256=compute_commit_payload_sha256(**values),
        governed_authority=auth,
        command_id="commit-selective-repair-candidate-v1",
    )
    return issue_repair_commit_receipt(
        **values,
        command=cmd,
        authority=auth,
    )


def escalation_inputs(*, trigger=EscalationTrigger.CONSTITUTIONAL_DECISION_CHANGE):
    candidate = compile_candidate()
    return {
        "candidate": candidate,
        "trigger": trigger,
        "affected_authority_sha256": digest("affected-constitutional-authority-v1"),
        "required_decision": "governed human decision is required before another repair",
        "options": (
            "preserve the current immutable version",
            "authorize a new governed amendment and candidate version",
        ),
        "evidence_refs": (
            candidate.accepted_diagnosis_identity,
            digest("repeat-failure-evidence-v1"),
        ),
    }


def escalation_receipt(*, inputs=None, governed_authority=None, governed_command=None):
    values = inputs or escalation_inputs()
    auth = governed_authority or lifecycle_authority(RepairAction.ESCALATE)
    cmd = governed_command or command(
        action=RepairAction.ESCALATE,
        resource_id=values["candidate"].candidate_identity,
        payload_sha256=compute_escalation_payload_sha256(**values),
        governed_authority=auth,
        command_id="escalate-selective-repair-v1",
    )
    return issue_repair_escalation_receipt(
        **values,
        command=cmd,
        authority=auth,
    )


def test_candidate_commits_only_after_every_required_local_regression_passes() -> None:
    receipt = commit_receipt()

    assert receipt.status == "COMMITTED_DEVELOPMENT_CANDIDATE"
    assert receipt.active is True
    assert tuple(result.status for result in receipt.local_results) == tuple(
        LocalRerunStatus.PASS for _ in receipt.local_results
    )
    assert receipt.required_suite_coverage_complete is True
    assert receipt.external_runtime_executed is False
    assert receipt.production_ready is False
    assert receipt.certified is False


def test_missing_required_regression_result_fails_atomically() -> None:
    plan = compile_plan()
    inputs = commit_inputs(plan=plan, results=local_results(plan)[:-1])
    auth = lifecycle_authority(RepairAction.COMMIT_CANDIDATE)
    receipt = None

    with pytest.raises(SelectiveRepairError) as caught:
        receipt = commit_receipt(inputs=inputs, governed_authority=auth)

    assert caught.value.code == "MISSING_REQUIRED_RERUN_RESULT"
    assert receipt is None


@pytest.mark.parametrize(
    ("result_status", "expected_code"),
    (
        (LocalRerunStatus.FAIL, "REQUIRED_REGRESSION_FAILED"),
        (LocalRerunStatus.BLOCKED, "REQUIRED_REGRESSION_BLOCKED"),
    ),
)
def test_failed_or_blocked_required_result_prevents_commit(result_status, expected_code) -> None:
    plan = compile_plan()
    blocked_suite = plan.requirements[-1].suite_id
    inputs = commit_inputs(
        plan=plan,
        results=local_results(plan, status_by_suite={blocked_suite: result_status}),
    )

    with pytest.raises(SelectiveRepairError) as caught:
        commit_receipt(inputs=inputs)

    assert caught.value.code == expected_code


def test_commit_rejects_extra_unplanned_regression_result() -> None:
    plan = compile_plan()
    extra = LocalRerunResult(
        suite_id="tests/unrelated/whole-run-regeneration",
        status=LocalRerunStatus.PASS,
        result_sha256=digest("unrelated-suite-result"),
    )
    inputs = commit_inputs(plan=plan, results=local_results(plan) + (extra,))

    with pytest.raises(SelectiveRepairError) as caught:
        commit_receipt(inputs=inputs)

    assert caught.value.code == "UNPLANNED_RERUN_RESULT"


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"resource_id": digest("wrong-candidate")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        (
            {"expected_authority_identity": digest("wrong-authority")},
            "AUTHORITY_IDENTITY_MISMATCH",
        ),
    ),
)
def test_commit_requires_exact_command_payload_resource_and_authority(change, expected_code) -> None:
    inputs = commit_inputs()
    auth = lifecycle_authority(RepairAction.COMMIT_CANDIDATE)
    cmd = command(
        action=RepairAction.COMMIT_CANDIDATE,
        resource_id=inputs["candidate"].candidate_identity,
        payload_sha256=compute_commit_payload_sha256(**inputs),
        governed_authority=auth,
        command_id="commit-boundary-test",
    )

    with pytest.raises(SelectiveRepairError) as caught:
        commit_receipt(
            inputs=inputs,
            governed_authority=auth,
            governed_command=replace(cmd, **change),
        )

    assert caught.value.code == expected_code


@pytest.mark.parametrize(
    "status", (RepairAuthorityStatus.SUPERSEDED, RepairAuthorityStatus.INVALIDATED)
)
def test_stale_or_invalidated_authority_cannot_commit(status) -> None:
    with pytest.raises(SelectiveRepairError) as caught:
        commit_receipt(
            governed_authority=lifecycle_authority(
                RepairAction.COMMIT_CANDIDATE,
                status=status,
            )
        )

    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_authority_must_explicitly_grant_candidate_commit() -> None:
    inputs = commit_inputs()
    auth = lifecycle_authority(RepairAction.ESCALATE)
    cmd = command(
        action=RepairAction.COMMIT_CANDIDATE,
        resource_id=inputs["candidate"].candidate_identity,
        payload_sha256=compute_commit_payload_sha256(**inputs),
        governed_authority=auth,
        command_id="unauthorized-commit",
    )

    with pytest.raises(SelectiveRepairError) as caught:
        commit_receipt(
            inputs=inputs,
            governed_authority=auth,
            governed_command=cmd,
        )

    assert caught.value.code == "UNAUTHORIZED_ACTION"


@pytest.mark.parametrize("trigger", tuple(EscalationTrigger))
def test_every_capsule_governed_escalation_trigger_freezes_automated_repair(trigger) -> None:
    receipt = escalation_receipt(inputs=escalation_inputs(trigger=trigger))

    assert receipt.trigger is trigger
    assert receipt.automation_frozen is True
    assert receipt.required_decision.strip()
    assert receipt.options
    assert receipt.evidence_refs
    assert receipt.production_ready is False
    assert receipt.certified is False


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    (
        ("required_decision", "", "MISSING_REQUIRED_DECISION"),
        ("options", (), "MISSING_ESCALATION_OPTIONS"),
        ("evidence_refs", (), "MISSING_ESCALATION_EVIDENCE"),
    ),
)
def test_escalation_cannot_be_suppressed_or_emitted_without_decision_evidence(
    field, value, expected_code
) -> None:
    inputs = escalation_inputs()
    inputs[field] = value

    with pytest.raises(SelectiveRepairError) as caught:
        escalation_receipt(inputs=inputs)

    assert caught.value.code == expected_code


def test_escalation_requires_explicit_authority_grant() -> None:
    inputs = escalation_inputs()
    auth = lifecycle_authority(RepairAction.COMMIT_CANDIDATE)
    cmd = command(
        action=RepairAction.ESCALATE,
        resource_id=inputs["candidate"].candidate_identity,
        payload_sha256=compute_escalation_payload_sha256(**inputs),
        governed_authority=auth,
        command_id="unauthorized-escalation",
    )

    with pytest.raises(SelectiveRepairError) as caught:
        escalation_receipt(
            inputs=inputs,
            governed_authority=auth,
            governed_command=cmd,
        )

    assert caught.value.code == "UNAUTHORIZED_ACTION"


@pytest.mark.parametrize(
    "prohibited_action",
    (
        "execute_external_runtime",
        "publish_production_candidate",
        "certify_candidate",
        "repair_external_product",
    ),
)
def test_external_runtime_product_repair_production_and_certification_actions_are_unrepresentable(
    prohibited_action,
) -> None:
    with pytest.raises(SelectiveRepairError) as caught:
        RepairCommand(
            command_id=prohibited_action,
            action=prohibited_action,  # type: ignore[arg-type]
            resource_id=digest("candidate"),
            payload_sha256=digest("payload"),
            expected_authority_identity=digest("authority"),
        )

    assert caught.value.code == "INVALID_COMMAND_ACTION"


def test_atomic_commit_failure_can_emit_only_a_zero_state_rejection_receipt() -> None:
    inputs = commit_inputs()
    auth = lifecycle_authority(RepairAction.COMMIT_CANDIDATE)
    cmd = command(
        action=RepairAction.COMMIT_CANDIDATE,
        resource_id=inputs["candidate"].candidate_identity,
        payload_sha256=digest("conflicting-payload"),
        governed_authority=auth,
        command_id="atomic-commit-failure",
    )
    receipt = None

    with pytest.raises(SelectiveRepairError) as caught:
        receipt = commit_receipt(
            inputs=inputs,
            governed_authority=auth,
            governed_command=cmd,
        )

    rejection = build_repair_rejection_receipt(
        error=caught.value,
        command_id=cmd.command_id,
        payload_sha256=cmd.payload_sha256,
        authority_identity=auth.authority_identity,
    )
    assert receipt is None
    assert rejection.error_code == "COMMAND_PAYLOAD_MISMATCH"
    assert rejection.partial_state_count == 0

