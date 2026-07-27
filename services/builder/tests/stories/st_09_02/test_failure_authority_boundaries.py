from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.workflow.manual_shadow_routing import (
    SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL,
    DivergenceClass,
    ImmutableInputSnapshot,
    ManualShadowError,
    ProposedAutomatedOutput,
    ProposedOutputStatus,
    ReviewerDisposition,
    ReviewerDispositionStatus,
    ShadowAction,
    ShadowAuthority,
    ShadowAuthorityStatus,
    ShadowCommand,
    ShadowDisposition,
    ShadowReviewRequest,
    compile_manual_shadow_evaluation,
    compute_shadow_issue_payload_sha256,
    issue_manual_shadow_receipt,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def input_snapshot(**changes: object) -> ImmutableInputSnapshot:
    values: dict[str, object] = {
        "snapshot_id": "synthetic-shadow-input",
        "snapshot_version": "1.0.0-development",
        "snapshot_sha256": digest("synthetic-shadow-input-bytes"),
        "active": True,
        "superseded": False,
        "invalidated": False,
    }
    values.update(changes)
    return ImmutableInputSnapshot(**values)  # type: ignore[arg-type]


def proposed_output(
    *,
    status: ProposedOutputStatus = ProposedOutputStatus.PASS,
    sha256: str | None = None,
) -> ProposedAutomatedOutput:
    return ProposedAutomatedOutput(
        output_id="synthetic-proposed-automated-output",
        output_version="1.0.0-development",
        output_sha256=sha256 or digest("synthetic-proposed-output-bytes"),
        status=status,
        authority_identity=digest("bounded-proposal-authority"),
    )


def review_request(
    *,
    snapshot: ImmutableInputSnapshot | None = None,
    proposal: ProposedAutomatedOutput | None = None,
    fixture_classification: str = SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL,
) -> ShadowReviewRequest:
    return ShadowReviewRequest(
        request_id="synthetic-shadow-review-request",
        workflow_identity=digest("st-09.01-actor-explicit-workflow"),
        node_identity=digest("human-shadow-review-node"),
        input_snapshot=snapshot or input_snapshot(),
        proposed_output=proposal or proposed_output(),
        fixture_classification=fixture_classification,
        requested_reviewer_role="synthetic-fixture-reviewer-role",
        authority_requirement=digest("shadow-review-authority-requirement"),
    )


def reviewer(
    *,
    status: ReviewerDispositionStatus = ReviewerDispositionStatus.ACTIVE,
    response: str = "synthetic fixture response agrees with the proposed structure",
    reviewer_identity: str = "synthetic-shadow-fixture-reviewer",
    response_sha256: str | None = None,
) -> ReviewerDisposition:
    return ReviewerDisposition(
        reviewer_identity=reviewer_identity,
        response=response,
        response_sha256=response_sha256 or digest(response),
        status=status,
        authority_sha256=digest("synthetic-fixture-review-authority"),
        recorded_at="2026-07-17T00:00:00Z",
    )


def authority(
    *actions: ShadowAction,
    status: ShadowAuthorityStatus = ShadowAuthorityStatus.ACTIVE,
) -> ShadowAuthority:
    return ShadowAuthority(
        authority_id="od-am-001-st-09.02-development-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-09.02-authority-bytes"),
        permitted_actions=actions or (ShadowAction.ISSUE,),
        applicable_scope=("OD_AM_001_OFFLINE_DEVELOPMENT",),
        status=status,
    )


def command(
    *,
    action: ShadowAction,
    resource_id: str,
    payload_sha256: str,
    governed_authority: ShadowAuthority,
    command_id: str,
) -> ShadowCommand:
    return ShadowCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id,
        payload_sha256=payload_sha256,
        expected_authority_identity=governed_authority.authority_identity,
    )


def evaluation(
    *,
    request: ShadowReviewRequest | None = None,
    reviewer_disposition: ReviewerDisposition | None = None,
    divergence_class: DivergenceClass = DivergenceClass.EXACT_AGREEMENT,
    reviewer_present: bool = True,
):
    governed_request = request or review_request()
    governed_reviewer = (
        reviewer_disposition if reviewer_disposition is not None else reviewer()
    )
    return compile_manual_shadow_evaluation(
        review_request=governed_request,
        reviewer_disposition=governed_reviewer if reviewer_present else None,
        divergence_class=divergence_class,
        comparison_sha256=digest(
            f"comparison:{divergence_class.value}:{governed_request.request_identity}"
        ),
        comparison_summary=f"governed {divergence_class.value} development comparison",
        limitations=(
            "synthetic structural fixture only",
            "not attributable human approval",
            "manual shadow evidence gate remains open",
        ),
    )


def issue_receipt(*, candidate=None, governed_authority=None, governed_command=None):
    result = candidate or evaluation()
    auth = governed_authority or authority(ShadowAction.ISSUE)
    cmd = governed_command or command(
        action=ShadowAction.ISSUE,
        resource_id=result.evaluation_identity,
        payload_sha256=compute_shadow_issue_payload_sha256(result),
        governed_authority=auth,
        command_id="issue-synthetic-shadow-evaluation-v1",
    )
    return issue_manual_shadow_receipt(result, cmd, auth)


def test_six_dispositions_are_stable_and_detailed_failure_classes_remain_visible() -> None:
    assert tuple(item.value for item in ShadowDisposition) == (
        "PASS_EXACT_AGREEMENT",
        "PASS_ACCEPTABLE_BOUNDED_DIFFERENCE",
        "FAIL_SEMANTIC_DIVERGENCE",
        "FAIL_AUTHORITY_VIOLATION",
        "BLOCKED_REVIEWER_EVIDENCE",
        "BLOCKED_STALE_OR_FAILED_PROPOSAL",
    )
    assert {
        item.value for item in DivergenceClass
    } == {
        "EXACT_AGREEMENT",
        "ACCEPTABLE_BOUNDED_DIFFERENCE",
        "SEMANTIC_DIVERGENCE",
        "AUTHORITY_VIOLATION",
        "MISSING_REVIEWER",
        "WITHDRAWN_REVIEWER_DISPOSITION",
        "STALE_INPUT_SNAPSHOT",
        "FAILED_PROPOSED_OUTPUT",
    }


@pytest.mark.parametrize(
    ("divergence", "expected_disposition"),
    (
        (DivergenceClass.EXACT_AGREEMENT, ShadowDisposition.PASS_EXACT_AGREEMENT),
        (
            DivergenceClass.ACCEPTABLE_BOUNDED_DIFFERENCE,
            ShadowDisposition.PASS_ACCEPTABLE_BOUNDED_DIFFERENCE,
        ),
        (
            DivergenceClass.SEMANTIC_DIVERGENCE,
            ShadowDisposition.FAIL_SEMANTIC_DIVERGENCE,
        ),
        (
            DivergenceClass.AUTHORITY_VIOLATION,
            ShadowDisposition.FAIL_AUTHORITY_VIOLATION,
        ),
    ),
)
def test_comparison_maps_to_exact_governed_disposition(
    divergence: DivergenceClass,
    expected_disposition: ShadowDisposition,
) -> None:
    result = evaluation(divergence_class=divergence)
    assert result.divergence_class is divergence
    assert result.disposition is expected_disposition


def test_synthetic_fixture_is_never_serialized_as_human_approval_or_real_shadow() -> None:
    receipt = issue_receipt()
    payload = receipt.as_dict()

    assert payload["fixture_classification"] == (
        "SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL"
    )
    assert payload["human_approval_issued"] is False
    assert payload["real_manual_shadow_evidence"] is False
    assert payload["automation_promotion_available"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False
    assert "manual_shadow_evidence" in payload["open_evidence_gates"]


def test_fixture_cannot_be_reclassified_as_real_human_review() -> None:
    with pytest.raises(ManualShadowError) as caught:
        review_request(fixture_classification="REAL_HUMAN_APPROVAL")

    assert caught.value.code == "REAL_HUMAN_APPROVAL_NOT_PROVEN"


def test_missing_reviewer_is_typed_and_blocks_review_evidence() -> None:
    result = evaluation(
        reviewer_present=False,
        divergence_class=DivergenceClass.MISSING_REVIEWER,
    )
    assert result.divergence_class is DivergenceClass.MISSING_REVIEWER
    assert result.disposition is ShadowDisposition.BLOCKED_REVIEWER_EVIDENCE
    assert result.reviewer_disposition is None


def test_withdrawn_reviewer_disposition_is_inactive_and_cannot_promote() -> None:
    result = evaluation(
        reviewer_disposition=reviewer(status=ReviewerDispositionStatus.WITHDRAWN),
        divergence_class=DivergenceClass.WITHDRAWN_REVIEWER_DISPOSITION,
    )
    assert result.disposition is ShadowDisposition.BLOCKED_REVIEWER_EVIDENCE
    assert result.reviewer_disposition.status is ReviewerDispositionStatus.WITHDRAWN
    assert result.automation_promotion_available is False


@pytest.mark.parametrize(
    ("governed_request", "divergence"),
    (
        (
            review_request(snapshot=input_snapshot(superseded=True)),
            DivergenceClass.STALE_INPUT_SNAPSHOT,
        ),
        (
            review_request(
                proposal=proposed_output(status=ProposedOutputStatus.FAIL)
            ),
            DivergenceClass.FAILED_PROPOSED_OUTPUT,
        ),
    ),
)
def test_stale_input_or_failed_proposal_blocks_shadow_disposition(
    governed_request: ShadowReviewRequest,
    divergence: DivergenceClass,
) -> None:
    result = evaluation(request=governed_request, divergence_class=divergence)
    assert result.disposition is ShadowDisposition.BLOCKED_STALE_OR_FAILED_PROPOSAL
    assert result.automation_promotion_available is False


def test_stale_or_failed_state_cannot_be_mislabeled_as_agreement() -> None:
    invalid_requests = (
        review_request(snapshot=input_snapshot(invalidated=True)),
        review_request(proposal=proposed_output(status=ProposedOutputStatus.FAIL)),
    )
    for request in invalid_requests:
        with pytest.raises(ManualShadowError) as caught:
            evaluation(request=request, divergence_class=DivergenceClass.EXACT_AGREEMENT)
        assert caught.value.code == "DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE"


def test_missing_or_withdrawn_reviewer_cannot_be_mislabeled_as_human_agreement() -> None:
    with pytest.raises(ManualShadowError) as caught:
        evaluation(
            reviewer_present=False,
            divergence_class=DivergenceClass.EXACT_AGREEMENT,
        )
    assert caught.value.code == "DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE"

    with pytest.raises(ManualShadowError) as caught:
        evaluation(
            reviewer_disposition=reviewer(status=ReviewerDispositionStatus.WITHDRAWN),
            divergence_class=DivergenceClass.EXACT_AGREEMENT,
        )
    assert caught.value.code == "DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE"


@pytest.mark.parametrize(
    ("field", "expected_code"),
    (
        ("resource_id", "COMMAND_RESOURCE_MISMATCH"),
        ("payload_sha256", "COMMAND_PAYLOAD_MISMATCH"),
        ("expected_authority_identity", "AUTHORITY_IDENTITY_MISMATCH"),
    ),
)
def test_issue_command_is_exactly_bound_to_resource_payload_and_authority(
    field: str,
    expected_code: str,
) -> None:
    candidate = evaluation()
    auth = authority(ShadowAction.ISSUE)
    valid = command(
        action=ShadowAction.ISSUE,
        resource_id=candidate.evaluation_identity,
        payload_sha256=compute_shadow_issue_payload_sha256(candidate),
        governed_authority=auth,
        command_id="issue-authority-boundary",
    )
    invalid = replace(valid, **{field: digest(f"wrong-{field}")})

    with pytest.raises(ManualShadowError) as caught:
        issue_receipt(
            candidate=candidate,
            governed_authority=auth,
            governed_command=invalid,
        )
    assert caught.value.code == expected_code


def test_stale_authority_cannot_issue_a_shadow_receipt() -> None:
    stale = authority(
        ShadowAction.ISSUE,
        status=ShadowAuthorityStatus.SUPERSEDED,
    )
    with pytest.raises(ManualShadowError) as caught:
        issue_receipt(governed_authority=stale)
    assert caught.value.code == "INACTIVE_AUTHORITY"
