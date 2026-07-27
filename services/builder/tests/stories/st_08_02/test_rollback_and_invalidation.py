from __future__ import annotations

import pytest

from cmf_builder.evaluation.maturity_promotion import (
    MaturityPromotionError,
    MaturityStatus,
    PromotionAction,
    invalidate_maturity_receipt,
    promote_development_maturity,
    transition_maturity_receipt,
)
from tests.stories.st_08_02.test_development_maturity_promotion import (
    authority,
    command,
    digest,
    evaluation_identity,
    protected_evidence,
)


def promoted_receipt():
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    receipt = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )
    return candidate, evidence, receipt


def test_changed_governed_input_invalidates_affected_descendants_only() -> None:
    _, _, receipt = promoted_receipt()
    changed = (digest("changed-rubric"), digest("changed-evaluator"))
    invalidation = invalidate_maturity_receipt(
        receipt=receipt,
        changed_identities=reversed(changed),
        command=command(
            receipt.receipt_identity,
            action=PromotionAction.INVALIDATE,
            status=MaturityStatus.TESTED,
            command_id="invalidate-001",
        ),
        authority=authority(receipt.receipt_identity, PromotionAction.INVALIDATE),
    )

    assert invalidation.prior_status == MaturityStatus.DEVELOPMENT_VALIDATED
    assert invalidation.maturity_status == MaturityStatus.SUPERSEDED
    assert invalidation.invalidates_descendants == tuple(sorted(changed))
    assert invalidation.as_dict()["production_ready"] is False
    assert invalidation.as_dict()["certified"] is False


def test_invalidation_requires_exact_active_receipt_resource() -> None:
    _, _, receipt = promoted_receipt()
    with pytest.raises(MaturityPromotionError) as caught:
        invalidate_maturity_receipt(
            receipt=receipt,
            changed_identities=(digest("changed"),),
            command=command(
                digest("wrong-resource"),
                action=PromotionAction.INVALIDATE,
                status=MaturityStatus.TESTED,
                command_id="invalidate-wrong",
            ),
            authority=authority(digest("wrong-resource"), PromotionAction.INVALIDATE),
        )

    assert caught.value.code == "COMMAND_RESOURCE_MISMATCH"


def test_deprecation_preserves_historical_receipt_without_production_claim() -> None:
    _, _, receipt = promoted_receipt()
    deprecated = transition_maturity_receipt(
        receipt=receipt,
        command=command(
            receipt.receipt_identity,
            action=PromotionAction.DEPRECATE,
            status=MaturityStatus.DEPRECATED,
            command_id="deprecate-001",
        ),
        authority=authority(receipt.receipt_identity, PromotionAction.DEPRECATE),
    )

    assert deprecated.maturity_status == MaturityStatus.DEPRECATED
    assert deprecated.prior_status == MaturityStatus.DEVELOPMENT_VALIDATED
    assert deprecated.evaluation_identity == receipt.evaluation_identity
    assert deprecated.as_dict()["real_protected_evidence_closed"] is False


def test_supersession_requires_replacement_receipt_and_records_it() -> None:
    _, _, receipt = promoted_receipt()
    replacement = digest("replacement-receipt")

    superseded = transition_maturity_receipt(
        receipt=receipt,
        command=command(
            receipt.receipt_identity,
            action=PromotionAction.SUPERSEDE,
            status=MaturityStatus.SUPERSEDED,
            command_id="supersede-001",
            replacement=replacement,
        ),
        authority=authority(receipt.receipt_identity, PromotionAction.SUPERSEDE),
    )

    assert superseded.maturity_status == MaturityStatus.SUPERSEDED
    assert superseded.invalidates_descendants == (replacement,)

    with pytest.raises(MaturityPromotionError) as caught:
        transition_maturity_receipt(
            receipt=receipt,
            command=command(
                receipt.receipt_identity,
                action=PromotionAction.SUPERSEDE,
                status=MaturityStatus.SUPERSEDED,
                command_id="supersede-missing",
            ),
            authority=authority(receipt.receipt_identity, PromotionAction.SUPERSEDE),
        )
    assert caught.value.code == "MISSING_REPLACEMENT_RECEIPT"


def test_rollback_returns_to_tested_without_mutating_original_receipt() -> None:
    _, _, receipt = promoted_receipt()
    rollback = transition_maturity_receipt(
        receipt=receipt,
        command=command(
            receipt.receipt_identity,
            action=PromotionAction.ROLLBACK,
            status=MaturityStatus.TESTED,
            command_id="rollback-001",
        ),
        authority=authority(receipt.receipt_identity, PromotionAction.ROLLBACK),
    )

    assert rollback.maturity_status == MaturityStatus.TESTED
    assert rollback.prior_status == MaturityStatus.DEVELOPMENT_VALIDATED
    assert receipt.maturity_status == MaturityStatus.DEVELOPMENT_VALIDATED
    assert rollback.receipt_identity != receipt.receipt_identity


def test_atomic_failure_leaves_no_partial_state_or_receipt() -> None:
    _, _, receipt = promoted_receipt()
    with pytest.raises(MaturityPromotionError) as caught:
        transition_maturity_receipt(
            receipt=receipt,
            command=command(
                receipt.receipt_identity,
                action=PromotionAction.INVALIDATE,
                status=MaturityStatus.TESTED,
                command_id="bad-transition",
            ),
            authority=authority(receipt.receipt_identity, PromotionAction.INVALIDATE),
        )

    assert caught.value.code == "INVALID_MATURITY_ACTION"
    assert receipt.maturity_status == MaturityStatus.DEVELOPMENT_VALIDATED
