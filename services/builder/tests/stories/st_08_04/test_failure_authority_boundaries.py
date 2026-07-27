from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.root_cause_diagnosis import (
    AuthorityStatus,
    DiagnosisAction,
    DiagnosisAuthority,
    DiagnosisCommand,
    RootCauseDiagnosisError,
    build_rejection_receipt,
    compute_issue_payload_sha256,
    issue_root_cause_diagnosis_receipt,
)
from tests.stories.st_08_04.test_layer_localization_and_graph import valid_graph
from tests.stories.st_08_04.test_typed_root_cause_diagnosis import localized_diagnosis


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def authority(
    *actions: DiagnosisAction,
    status: AuthorityStatus = AuthorityStatus.ACTIVE,
    authority_id: str = "od-am-001-st-08.04-development-authority",
) -> DiagnosisAuthority:
    return DiagnosisAuthority(
        authority_id=authority_id,
        authority_version="1.0.0-development",
        authority_sha256=digest(f"{authority_id}:governed-bytes"),
        permitted_actions=actions or (
            DiagnosisAction.ISSUE,
            DiagnosisAction.INVALIDATE,
        ),
        status=status,
    )


def issue_inputs(**changes: object) -> dict[str, object]:
    diagnosis = localized_diagnosis()
    active_graph = valid_graph(diagnosis)
    values: dict[str, object] = {
        "diagnosis": diagnosis,
        "graph": active_graph,
        "failure_subject_sha256": digest("failed-artifact"),
        "predecessor_scoring_receipt_sha256": digest("st-08.03-scoring-receipt"),
        "dependency_graph_sha256": digest("st-08.04-dependency-graph-v1"),
        "run_id": "st-08.04-development-run-v1",
        "provenance_sha256": digest("st-08.04-provenance-v1"),
        "observations": (
            "ST-08.04:RootCauseLocalized",
            "ST-08.04:RepairAndInvalidationGraphDeclared",
            "ST-08.04:OutcomeVerified",
        ),
    }
    values.update(changes)
    return values


def command(
    inputs: dict[str, object],
    auth: DiagnosisAuthority,
    *,
    command_id: str = "issue-root-cause-diagnosis-v1",
    action: DiagnosisAction = DiagnosisAction.ISSUE,
    resource_id: str | None = None,
    payload_sha256: str | None = None,
    expected_authority_identity: str | None = None,
) -> DiagnosisCommand:
    if payload_sha256 is None:
        if action is not DiagnosisAction.ISSUE:
            raise AssertionError("transition commands require an explicit payload hash")
        payload_sha256 = compute_issue_payload_sha256(**inputs)
    return DiagnosisCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id or inputs["diagnosis"].diagnosis_identity,  # type: ignore[union-attr]
        payload_sha256=payload_sha256,
        expected_authority_identity=expected_authority_identity or auth.authority_identity,
    )


def valid_receipt(*, inputs=None, auth=None, issue_command=None):
    governed_inputs = inputs or issue_inputs()
    governed_authority = auth or authority()
    governed_command = issue_command or command(governed_inputs, governed_authority)
    return issue_root_cause_diagnosis_receipt(
        **governed_inputs,
        command=governed_command,
        authority=governed_authority,
    )


def test_issue_binds_exact_authority_command_payload_resource_and_lineage() -> None:
    inputs = issue_inputs()
    auth = authority()
    cmd = command(inputs, auth)

    receipt = valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)

    assert receipt.command_identity == cmd.command_identity
    assert receipt.authority_identity == auth.authority_identity
    assert receipt.diagnosis.diagnosis_identity == cmd.resource_id
    assert receipt.failure_subject_sha256 == digest("failed-artifact")
    assert receipt.predecessor_scoring_receipt_sha256 == digest("st-08.03-scoring-receipt")
    assert receipt.graph is not None
    assert receipt.diagnosis.diagnosis_identity == receipt.graph.root_cause_diagnosis_ref
    assert receipt.as_dict()["observations"] == list(inputs["observations"])


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"action": DiagnosisAction.INVALIDATE}, "UNAUTHORIZED_ACTION"),
        ({"resource_id": digest("wrong-resource")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        (
            {"expected_authority_identity": digest("wrong-authority")},
            "AUTHORITY_IDENTITY_MISMATCH",
        ),
    ),
)
def test_issue_fails_closed_on_exact_binding_drift(change, expected_code) -> None:
    inputs = issue_inputs()
    auth = authority()
    cmd = replace(command(inputs, auth), **change)
    receipt = None

    with pytest.raises(RootCauseDiagnosisError) as caught:
        receipt = valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)

    assert caught.value.code == expected_code
    assert receipt is None


def test_missing_authority_evidence_fails_closed_without_receipt() -> None:
    inputs = issue_inputs()
    auth = authority()
    receipt = None

    with pytest.raises(RootCauseDiagnosisError) as caught:
        receipt = issue_root_cause_diagnosis_receipt(
            **inputs,
            command=command(inputs, auth),
            authority=None,  # type: ignore[arg-type]
        )

    assert caught.value.code == "INVALID_AUTHORITY_EVIDENCE"
    assert receipt is None


@pytest.mark.parametrize("status", (AuthorityStatus.SUPERSEDED, AuthorityStatus.INVALIDATED))
def test_stale_or_invalidated_authority_cannot_issue_new_diagnosis(status) -> None:
    inputs = issue_inputs()
    auth = authority(status=status)

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=command(inputs, auth))

    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_authority_must_explicitly_grant_issue_action() -> None:
    inputs = issue_inputs()
    auth = authority(DiagnosisAction.INVALIDATE)

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=command(inputs, auth))

    assert caught.value.code == "UNAUTHORIZED_ACTION"


def test_altered_predecessor_scoring_lineage_fails_closed() -> None:
    inputs = issue_inputs(predecessor_scoring_receipt_sha256=digest("altered-st-08.03-receipt"))
    auth = authority()

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=command(inputs, auth))

    assert caught.value.code == "PREDECESSOR_SCORING_LINEAGE_MISMATCH"


def test_graph_must_reference_the_exact_active_diagnosis() -> None:
    inputs = issue_inputs(diagnosis=localized_diagnosis(observed_symptom="different governed symptom"))
    auth = authority()

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=command(inputs, auth))

    assert caught.value.code == "DIAGNOSIS_GRAPH_MISMATCH"


@pytest.mark.parametrize(
    "prohibited_action",
    ("execute_repair", "execute_workflow", "execute_external_runtime"),
)
def test_repair_workflow_and_external_runtime_commands_are_rejected(prohibited_action) -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        DiagnosisCommand(
            command_id=f"prohibited-{prohibited_action}",
            action=prohibited_action,  # type: ignore[arg-type]
            resource_id=digest("failed-artifact"),
            payload_sha256=digest("payload"),
            expected_authority_identity=digest("authority"),
        )

    assert caught.value.code == "INVALID_COMMAND_ACTION"


def test_non_story_scoped_observation_is_rejected() -> None:
    inputs = issue_inputs(observations=("ST-08.03:WrongStory",))
    auth = authority()

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=command(inputs, auth))

    assert caught.value.code == "INVALID_OBSERVATION"


def test_deterministic_rejection_receipt_is_attributable_and_has_no_partial_success() -> None:
    inputs = issue_inputs()
    auth = authority()
    cmd = replace(command(inputs, auth), payload_sha256=digest("wrong-payload"))

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_receipt(inputs=inputs, auth=auth, issue_command=cmd)

    first = build_rejection_receipt(
        error=caught.value,
        command_id=cmd.command_id,
        payload_sha256=cmd.payload_sha256,
        authority_identity=auth.authority_identity,
    )
    second = build_rejection_receipt(
        error=caught.value,
        command_id=cmd.command_id,
        payload_sha256=cmd.payload_sha256,
        authority_identity=auth.authority_identity,
    )

    assert first.rejection_identity == second.rejection_identity
    assert first.as_dict() == second.as_dict()
    assert first.error_code == "COMMAND_PAYLOAD_MISMATCH"
    assert first.command_id == cmd.command_id
    assert first.payload_sha256 == cmd.payload_sha256
    assert first.authority_identity == auth.authority_identity
    assert first.partial_state_count == 0
