import pytest

from cmf_builder.workflow.node_validation import (
    CheckStatus,
    NodeOutputSnapshot,
    NodeValidationAction,
    NodeValidationAuthority,
    NodeValidationCommand,
    NodeValidationError,
    NodeValidationPolicy,
    OutputDecision,
    OutputState,
    ValidationCheck,
    compute_node_validation_payload_sha256,
    validate_node_output,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def snapshot(**overrides):
    values = {
        "workflow_identity": digest("workflow"),
        "workflow_version": "1.0.0-development",
        "node_identity": "node:validate:1",
        "node_version": "1.0.0",
        "input_sha256": digest("input"),
        "output_sha256": digest("output"),
        "output_contract": "contract:node-output:v1",
    }
    values.update(overrides)
    return NodeOutputSnapshot(**values)


def policy(**overrides):
    values = {
        "policy_id": "node-output-validation-policy",
        "policy_version": "1.0.0-development",
        "required_check_kinds": (
            "deterministic_validator",
            "semantic_evaluator",
            "authority",
            "contract",
            "completion",
            "hard_gate",
        ),
        "semantic_evaluator_required": True,
        "allow_not_applicable_semantic_evaluator": False,
        "hard_gate_ids": ("HG-012", "HG-013"),
        "completion_criteria": ("all_declared_checks_pass",),
    }
    values.update(overrides)
    return NodeValidationPolicy(**values)


def checks(*, semantic_status=CheckStatus.PASS, failed_kind=None):
    result = []
    for kind in policy().required_check_kinds:
        status = CheckStatus.FAIL if kind == failed_kind else CheckStatus.PASS
        if kind == "semantic_evaluator":
            status = semantic_status
        result.append(
            ValidationCheck(
                check_id=f"check:{kind}",
                check_kind=kind,
                status=status,
                evidence_sha256=digest(kind),
                authority_ref=digest(f"authority:{kind}"),
                not_applicable_basis="offline semantic evaluator evidence pending"
                if status is CheckStatus.NOT_APPLICABLE
                else "",
            )
        )
    return tuple(result)


def authority(*actions):
    return NodeValidationAuthority(
        "node-validation-authority",
        "1.0.0",
        digest("authority"),
        actions or (NodeValidationAction.VALIDATE,),
        ("*",),
    )


def command(snap, pol, validation_checks, auth):
    return NodeValidationCommand(
        "validate-node-output",
        NodeValidationAction.VALIDATE,
        snap.snapshot_identity,
        compute_node_validation_payload_sha256(snap, pol, validation_checks, ("ST-09.02",)),
        auth.authority_identity,
    )


def validate(snap=None, pol=None, validation_checks=None, auth=None):
    snap = snap or snapshot()
    pol = pol or policy()
    validation_checks = validation_checks or checks()
    auth = auth or authority()
    return validate_node_output(
        snapshot=snap,
        policy=pol,
        checks=validation_checks,
        authority=auth,
        command=command(snap, pol, validation_checks, auth),
        predecessor_receipts=("ST-09.02",),
    )


def test_validated_output_releases_only_after_every_declared_check_passes():
    receipt = validate()

    assert receipt.decision is OutputDecision.RELEASE_VALIDATED
    assert receipt.release_state is OutputState.RELEASED_VALIDATED
    assert receipt.downstream_scheduling_eligible is True
    assert receipt.as_dict()["production_ready"] is False
    assert receipt.as_dict()["certified"] is False


def test_missing_declared_check_keeps_output_quarantined_and_blocks_downstream():
    validation_checks = tuple(check for check in checks() if check.check_kind != "contract")
    receipt = validate(validation_checks=validation_checks)

    assert receipt.decision is OutputDecision.BLOCK_VALIDATION_FAILED
    assert receipt.downstream_scheduling_eligible is False
    assert receipt.failure_code == "MISSING_DECLARED_CHECK"
    assert receipt.release_state is OutputState.BLOCKED_VALIDATION_FAILED


def test_failed_check_creates_typed_blocker_without_releasing_output():
    receipt = validate(validation_checks=checks(failed_kind="hard_gate"))

    assert receipt.decision is OutputDecision.BLOCK_VALIDATION_FAILED
    assert receipt.failure_code == "VALIDATION_CHECK_FAILED"
    assert receipt.downstream_scheduling_eligible is False


def test_semantic_not_applicable_requires_authorized_policy_basis():
    receipt = validate(validation_checks=checks(semantic_status=CheckStatus.NOT_APPLICABLE))

    assert receipt.failure_code == "SEMANTIC_EVALUATOR_REQUIRED"

    relaxed_policy = policy(
        semantic_evaluator_required=True,
        allow_not_applicable_semantic_evaluator=True,
    )
    released = validate(pol=relaxed_policy, validation_checks=checks(semantic_status=CheckStatus.NOT_APPLICABLE))
    assert released.decision is OutputDecision.RELEASE_VALIDATED


def test_unquarantined_or_invalidated_output_cannot_advance():
    with pytest.raises(NodeValidationError) as released:
        validate(snap=snapshot(state=OutputState.RELEASED_VALIDATED))
    assert released.value.code == "UNQUARANTINED_OUTPUT_RELEASE_PROHIBITED"

    with pytest.raises(NodeValidationError) as invalidated:
        validate(snap=snapshot(active=False, invalidated=True))
    assert invalidated.value.code == "INVALIDATED_OUTPUT"
