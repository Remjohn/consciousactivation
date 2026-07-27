from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.evaluation.maturity_promotion import (
    CaseEvidence,
    CaseLayer,
    MaturityPromotionError,
    MaturityStatus,
    PromotionAction,
    promote_development_maturity,
)
from tests.stories.st_08_02.test_development_maturity_promotion import (
    authority,
    command,
    digest,
    evaluation_identity,
    protected_evidence,
)


def test_mismatched_evaluated_artifact_identity_fails_closed() -> None:
    candidate = evaluation_identity("candidate")
    evidence = protected_evidence(evaluation_identity("different"))

    with pytest.raises(MaturityPromotionError) as caught:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=command(candidate.identity),
            authority=authority(candidate.identity),
        )

    assert caught.value.code == "EVALUATED_ARTIFACT_IDENTITY_MISMATCH"


def test_hard_gate_failure_cannot_be_hidden_by_high_aggregate_score() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate, hard_gates_passed=False)

    with pytest.raises(MaturityPromotionError) as caught:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=command(candidate.identity),
            authority=authority(candidate.identity),
        )

    assert caught.value.code == "HARD_GATE_FAILURE"


def test_non_compensable_failures_block_promotion() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate, failures=("lost_immutable_lineage",))

    with pytest.raises(MaturityPromotionError) as caught:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=command(candidate.identity),
            authority=authority(candidate.identity),
        )

    assert caught.value.code == "NON_COMPENSABLE_FAILURE"


@pytest.mark.parametrize(
    "field",
    (
        "protected_label_bytes_in_receipt",
        "generator_access_to_expected_behavior",
        "synthetic_fixture_claimed_as_real_protected_evidence",
    ),
)
def test_protected_label_and_false_real_evidence_claims_fail_closed(field: str) -> None:
    kwargs = {
        "case_id": "protected-leak",
        "case_layer": CaseLayer.PROTECTED,
        "evidence_role": "protected_case_contract_fixture",
        "expected_behavior_authority_sha256": digest("authority"),
        "scoring_rule_sha256": digest("scoring"),
        "source_provenance_sha256": digest("provenance"),
        "custody_class": "protected_custody_reference_only",
        "custody_authority_sha256": digest("custody"),
        "case_assignment_receipt_sha256": digest("assignment"),
        "evaluator_isolation_receipt_sha256": digest("isolation"),
        "protected_label_reference_sha256": digest("label"),
        field: True,
    }
    with pytest.raises(MaturityPromotionError) as caught:
        CaseEvidence(**kwargs)

    assert caught.value.code in {
        "PROTECTED_LABEL_LEAKAGE",
        "PROTECTED_EXPECTED_BEHAVIOR_LEAKAGE",
        "SYNTHETIC_FIXTURE_FALSELY_CLAIMS_PROTECTED_EVIDENCE",
    }


def test_missing_protected_custody_references_fail_closed() -> None:
    with pytest.raises(MaturityPromotionError) as caught:
        CaseEvidence(
            case_id="protected-missing",
            case_layer=CaseLayer.PROTECTED,
            evidence_role="protected_case_contract_fixture",
            expected_behavior_authority_sha256=digest("authority"),
            scoring_rule_sha256=digest("scoring"),
            source_provenance_sha256=digest("provenance"),
            custody_class="protected_custody_reference_only",
        )

    assert caught.value.code == "MISSING_PROTECTED_CUSTODY_EVIDENCE"


@pytest.mark.parametrize(
    "status",
    (
        MaturityStatus.DRAFT,
        MaturityStatus.DEPRECATED,
        MaturityStatus.SUPERSEDED,
    ),
)
def test_invalid_promotion_statuses_are_rejected(status: MaturityStatus) -> None:
    candidate = evaluation_identity()
    with pytest.raises(MaturityPromotionError) as caught:
        command(
            candidate.identity,
            action=PromotionAction.PROMOTE,
            status=status,
        )

    assert caught.value.code == "INVALID_MATURITY_ACTION"


def test_prohibited_claim_words_are_rejected() -> None:
    with pytest.raises(MaturityPromotionError) as caught:
        evaluation_identity("production-ready")

    assert caught.value.code == "PROHIBITED_MATURITY_OR_CERTIFICATION_CLAIM"


def test_object_setattr_mutation_fails_deep_validation() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    object.__setattr__(evidence.cases[0], "custody_class", "mutated")

    with pytest.raises(MaturityPromotionError) as caught:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=command(candidate.identity),
            authority=authority(candidate.identity),
        )

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_unprotected_case_cannot_carry_protected_label_reference() -> None:
    public_case = protected_evidence().cases[0]
    with pytest.raises(MaturityPromotionError) as caught:
        replace(public_case, protected_label_reference_sha256=digest("label"))

    assert caught.value.code == "PROTECTED_LABEL_ON_UNPROTECTED_CASE"
