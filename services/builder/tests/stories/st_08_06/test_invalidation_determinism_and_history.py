from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

from cmf_builder.evaluation.development_readiness import (
    AuthorityStatus,
    DevelopmentReadinessError,
    ReadinessAction,
    ReadinessCommand,
    canonical_json_bytes,
    compute_readiness_transition_payload_sha256,
    invalidate_readiness_receipt,
    revoke_readiness_receipt,
    validate_repeat_readiness_receipt,
)
from tests.stories.st_08_06.test_false_readiness_and_authority_boundaries import (
    digest,
    issue_receipt,
    lifecycle_authority,
    readiness_receipt,
)


def transition_command(
    receipt,
    authority,
    *,
    action: ReadinessAction = ReadinessAction.INVALIDATE,
    command_id: str = "invalidate-development-readiness-v1",
    affected_scope: tuple[str, ...] = ("OD_AM_001_OFFLINE_DEVELOPMENT",),
    resource_id: str | None = None,
    payload_sha256: str | None = None,
    expected_authority_identity: str | None = None,
) -> ReadinessCommand:
    return ReadinessCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id or receipt.receipt_identity,
        payload_sha256=payload_sha256
        or compute_readiness_transition_payload_sha256(
            prior_receipt_identity=receipt.receipt_identity,
            action=action,
            affected_scope=affected_scope,
        ),
        expected_authority_identity=(
            expected_authority_identity or authority.authority_identity
        ),
    )


def test_identical_issue_is_payload_safe_and_returns_original_receipt() -> None:
    existing = issue_receipt()
    repeated = issue_receipt()

    assert existing.receipt_identity == repeated.receipt_identity
    assert validate_repeat_readiness_receipt(existing, repeated) is existing


def test_conflicting_repeat_command_fails_closed() -> None:
    existing = issue_receipt()
    changed = readiness_receipt(
        limitations=(
            "BD-007 provider execution remains open",
            "changed governed limitation",
        )
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        validate_repeat_readiness_receipt(existing, changed)

    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_issue_is_byte_identical_in_a_fresh_python_process() -> None:
    repository = Path(__file__).resolve().parents[3]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(repository / "src"), str(repository), environment.get("PYTHONPATH", ""))
    )
    script = (
        "from tests.stories.st_08_06.test_false_readiness_and_authority_boundaries "
        "import issue_receipt; "
        "from cmf_builder.evaluation.development_readiness import canonical_json_bytes; "
        "import sys; sys.stdout.buffer.write(canonical_json_bytes(issue_receipt().as_dict()))"
    )

    fresh_bytes = subprocess.check_output(
        [sys.executable, "-c", script],
        cwd=repository,
        env=environment,
    )

    assert fresh_bytes == canonical_json_bytes(issue_receipt().as_dict())


def test_changed_governed_evidence_changes_immutable_receipt_identity() -> None:
    original = issue_receipt()
    changed = issue_receipt(
        receipt=readiness_receipt(
            invalidation_conditions=(
                "source_lock_or_Harness_IR_changes",
                "changed_governed_evidence_invalidates",
            )
        )
    )

    assert changed.receipt_identity != original.receipt_identity
    assert canonical_json_bytes(changed.as_dict()) != canonical_json_bytes(
        original.as_dict()
    )


def test_nested_evidence_tampering_is_detected_at_serialization_boundary() -> None:
    receipt = issue_receipt()
    nested = receipt.dimensions[0].evidence_refs[0]
    object.__setattr__(nested, "sha256", digest("forged-evidence"))

    with pytest.raises(DevelopmentReadinessError) as caught:
        receipt.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_invalidation_preserves_historical_bytes_and_emits_exact_scope() -> None:
    receipt = issue_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    authority = lifecycle_authority(ReadinessAction.INVALIDATE)
    affected_scope = ("OD_AM_001_OFFLINE_DEVELOPMENT",)
    command = transition_command(
        receipt,
        authority,
        affected_scope=affected_scope,
    )

    transition = invalidate_readiness_receipt(
        receipt,
        command,
        authority,
        affected_scope,
    )

    assert transition.action is ReadinessAction.INVALIDATE
    assert transition.prior_receipt_identity == receipt.receipt_identity
    assert transition.affected_scope == affected_scope
    assert transition.active_after is False
    assert transition.historical_receipt_preserved is True
    assert transition.reevaluation_requires_new_receipt is True
    assert transition.command_identity == command.command_identity
    assert transition.authority_identity == authority.authority_identity
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


def test_revocation_is_distinct_from_invalidation_and_preserves_history() -> None:
    receipt = issue_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    authority = lifecycle_authority(ReadinessAction.REVOKE)
    affected_scope = ("OD_AM_001_OFFLINE_DEVELOPMENT",)
    command = transition_command(
        receipt,
        authority,
        action=ReadinessAction.REVOKE,
        command_id="revoke-development-readiness-v1",
        affected_scope=affected_scope,
    )

    transition = revoke_readiness_receipt(
        receipt,
        command,
        authority,
        affected_scope,
    )

    assert transition.action is ReadinessAction.REVOKE
    assert transition.prior_receipt_identity == receipt.receipt_identity
    assert transition.affected_scope == affected_scope
    assert transition.active_after is False
    assert transition.historical_receipt_preserved is True
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


def test_identical_invalidation_commands_are_byte_deterministic() -> None:
    first_receipt = issue_receipt()
    second_receipt = issue_receipt()
    first_authority = lifecycle_authority(ReadinessAction.INVALIDATE)
    second_authority = lifecycle_authority(ReadinessAction.INVALIDATE)
    scope = ("OD_AM_001_OFFLINE_DEVELOPMENT",)

    first = invalidate_readiness_receipt(
        first_receipt,
        transition_command(first_receipt, first_authority, affected_scope=scope),
        first_authority,
        scope,
    )
    second = invalidate_readiness_receipt(
        second_receipt,
        transition_command(second_receipt, second_authority, affected_scope=scope),
        second_authority,
        scope,
    )

    assert first.transition_identity == second.transition_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"resource_id": digest("wrong-receipt")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        (
            {"expected_authority_identity": digest("wrong-authority")},
            "AUTHORITY_IDENTITY_MISMATCH",
        ),
    ),
)
@pytest.mark.parametrize("action", (ReadinessAction.INVALIDATE, ReadinessAction.REVOKE))
def test_transition_requires_exact_resource_payload_and_authority(
    action: ReadinessAction,
    change: dict[str, object],
    expected_code: str,
) -> None:
    receipt = issue_receipt()
    authority = lifecycle_authority(action)
    scope = ("OD_AM_001_OFFLINE_DEVELOPMENT",)
    command = replace(
        transition_command(
            receipt,
            authority,
            action=action,
            command_id=f"{action.value.lower()}-boundary-test",
            affected_scope=scope,
        ),
        **change,
    )
    operation = (
        invalidate_readiness_receipt
        if action is ReadinessAction.INVALIDATE
        else revoke_readiness_receipt
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        operation(receipt, command, authority, scope)

    assert caught.value.code == expected_code


def test_stale_authority_cannot_invalidate_active_receipt() -> None:
    receipt = issue_receipt()
    authority = lifecycle_authority(
        ReadinessAction.INVALIDATE,
        status=AuthorityStatus.SUPERSEDED,
    )
    scope = ("OD_AM_001_OFFLINE_DEVELOPMENT",)

    with pytest.raises(DevelopmentReadinessError) as caught:
        invalidate_readiness_receipt(
            receipt,
            transition_command(receipt, authority, affected_scope=scope),
            authority,
            scope,
        )

    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_conflicting_transition_fails_atomically_without_mutating_history() -> None:
    receipt = issue_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    authority = lifecycle_authority(ReadinessAction.INVALIDATE)
    scope = ("OD_AM_001_OFFLINE_DEVELOPMENT",)
    transition = None

    with pytest.raises(DevelopmentReadinessError) as caught:
        transition = invalidate_readiness_receipt(
            receipt,
            transition_command(
                receipt,
                authority,
                affected_scope=scope,
                payload_sha256=digest("wrong-payload"),
            ),
            authority,
            scope,
        )

    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"
    assert transition is None
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes
