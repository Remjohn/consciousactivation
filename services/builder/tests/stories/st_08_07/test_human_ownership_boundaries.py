from __future__ import annotations

from dataclasses import replace
import pytest

from cmf_builder.evaluation.structural_conversational_evaluation import (
    ApplicabilityState,
    EvaluationDecision,
    EvaluationError,
    HumanOwnedArtifactApplicability,
    evaluate_structural_conversation,
)
from tests.stories.st_08_07.test_wrong_reading_rejection import (
    digest,
    dimensions,
    dominant_lock,
    human_owned_artifacts,
    subject,
)


def evaluate(*, governed_subject=None, artifacts=None):
    return evaluate_structural_conversation(
        subject=governed_subject or subject(),
        locks=(dominant_lock(),),
        dimensions=dimensions(),
        human_owned_artifacts=human_owned_artifacts() if artifacts is None else artifacts,
        predecessor_receipts=(digest("st-08.06-implementation-receipt"),),
    )


def test_human_owned_artifacts_are_explicitly_applicable_but_not_issued() -> None:
    receipt = evaluate()
    by_kind = {item.artifact_kind: item for item in receipt.human_owned_artifacts}
    assert set(by_kind) == {"ReactionReceipt", "ExpressionMoment", "IdentityDNAAmendmentApproval"}
    assert all(item.state is ApplicabilityState.STRUCTURALLY_APPLICABLE_HUMAN_EVIDENCE_NOT_PROVIDED for item in by_kind.values())
    payload = receipt.as_dict()
    assert "actual_human_reaction" not in payload
    assert "issued_reaction_receipt" not in payload
    assert "real_expression_moment" not in payload


@pytest.mark.parametrize("false_owner", (
    "AGENT_OUTPUT_IS_HUMAN_REACTION",
    "REACTION_RECEIPT_ISSUED_BY_BUILDER",
    "EXPRESSION_MOMENT_DECLARED_REAL",
    "ACTIVATIVE_CALL_ACCEPTED_WITHOUT_HUMAN_RESPONSE",
))
def test_agent_or_builder_cannot_claim_human_response_authority(false_owner: str) -> None:
    with pytest.raises(EvaluationError) as caught:
        evaluate(governed_subject=subject(response_ownership=false_owner))
    assert caught.value.code == "HUMAN_RESPONSE_OWNERSHIP_VIOLATION"


def test_all_human_owned_applicability_states_are_required() -> None:
    with pytest.raises(EvaluationError) as missing:
        evaluate(artifacts=human_owned_artifacts()[:-1])
    assert missing.value.code == "INCOMPLETE_HUMAN_OWNED_ARTIFACT_APPLICABILITY"
    with pytest.raises(EvaluationError) as duplicate:
        evaluate(artifacts=(*human_owned_artifacts(), human_owned_artifacts()[0]))
    assert duplicate.value.code == "INCOMPLETE_HUMAN_OWNED_ARTIFACT_APPLICABILITY"


def test_not_applicable_requires_a_real_justification() -> None:
    with pytest.raises(EvaluationError) as caught:
        HumanOwnedArtifactApplicability("ReactionReceipt", ApplicabilityState.NOT_APPLICABLE_WITH_JUSTIFICATION, "")
    assert caught.value.code == "MISSING_GOVERNED_FIELD"


@pytest.mark.parametrize(("field", "value"), (("production_ready", True), ("certified", True)))
def test_structural_branch_cannot_claim_production_or_certification(field: str, value: bool) -> None:
    with pytest.raises(EvaluationError) as caught:
        subject(**{field: value})
    assert caught.value.code == "PRODUCTION_OR_CERTIFICATION_PROHIBITED"


def test_proposed_reaction_receipt_reading_is_rejected_not_issued() -> None:
    lock = replace(dominant_lock(), prohibited_reading="This proposed Reaction Receipt has been issued.")
    receipt = evaluate_structural_conversation(
        subject=subject(proposed_reading="This proposed Reaction Receipt has been issued."),
        locks=(lock,), dimensions=dimensions(), human_owned_artifacts=human_owned_artifacts(),
        predecessor_receipts=(digest("st-08.06-implementation-receipt"),),
    )
    assert receipt.decision is EvaluationDecision.FAIL_WRONG_READING_LOCK
    assert receipt.active is False

