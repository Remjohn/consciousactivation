from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.development_readiness import (
    AuthorizationAuthority,
    AuthorizationAxis,
    AuthorizationAxisStatus,
    AuthorizationCommand,
    AuthorizationOutcome,
    DevelopmentReadinessError,
    PrototypeAuthorizationTerms,
    canonical_json_bytes,
    compute_authorization_payload_sha256,
    issue_development_authorization_receipt,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


SUBJECT_IDENTITY = digest("synthetic-text-normalization-definition-v1")
PREDECESSOR_RECEIPTS = (
    digest("st-08.03-implementation-receipt"),
    digest("st-08.04-implementation-receipt"),
    digest("st-08.05-implementation-receipt"),
)
ALLOWED_SCOPE = (
    "OD_AM_001_OFFLINE_DEVELOPMENT",
    "BUILDER_OWNED_DEVELOPMENT_FIXTURES",
)
PROHIBITED_SCOPE = (
    "RUNTIME_EXECUTION",
    "DEPLOYMENT",
    "PRODUCTION",
    "CERTIFICATION",
    "EXTERNAL_PROVIDER_VALIDATION",
    "REAL_HUMAN_REACTION_VALIDATION",
)
LIMITATIONS = (
    "BD-007 provider evidence remains open",
    "real attributable human-reaction evidence is absent",
    "implementation completion is not evidence closure",
)
EXPIRY_CONDITIONS = (
    "any predecessor receipt is invalidated",
    "the governed subject identity changes",
    "the bounded OD-AM-001 authority is withdrawn",
)


def authorization_axes() -> tuple[AuthorizationAxis, ...]:
    return (
        AuthorizationAxis(
            axis_id="implementation",
            status=AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS,
            evidence_refs=(PREDECESSOR_RECEIPTS[-1],),
            limitation="bounded offline implementation only",
        ),
        AuthorizationAxis(
            axis_id="evidence",
            status=AuthorizationAxisStatus.PENDING,
            evidence_refs=(digest("open-evidence-register"),),
            limitation="external evidence gate remains open",
        ),
        AuthorizationAxis(
            axis_id="runtime",
            status=AuthorizationAxisStatus.NOT_AUTHORIZED,
            evidence_refs=(digest("runtime-prohibition"),),
            limitation="no workflow or external runtime execution",
        ),
        AuthorizationAxis(
            axis_id="deployment",
            status=AuthorizationAxisStatus.NOT_AUTHORIZED,
            evidence_refs=(digest("deployment-prohibition"),),
            limitation="no deployment authority",
        ),
        AuthorizationAxis(
            axis_id="production",
            status=AuthorizationAxisStatus.FALSE,
            evidence_refs=(digest("production-readiness-open-gate"),),
            limitation="production readiness is false",
        ),
        AuthorizationAxis(
            axis_id="certification",
            status=AuthorizationAxisStatus.FALSE,
            evidence_refs=(digest("certification-open-gate"),),
            limitation="certification is false",
        ),
        AuthorizationAxis(
            axis_id="provider_validation",
            status=AuthorizationAxisStatus.PENDING,
            evidence_refs=(digest("bd-007-open"),),
            limitation="no provider execution occurred",
        ),
        AuthorizationAxis(
            axis_id="human_reaction_validation",
            status=AuthorizationAxisStatus.PENDING,
            evidence_refs=(digest("hd-006-open"),),
            limitation="no attributable real human-reaction evidence exists",
        ),
    )


def prototype_terms() -> PrototypeAuthorizationTerms:
    return PrototypeAuthorizationTerms(
        empirical_question="Can bounded deterministic Builder behavior be inspected offline?",
        allowed_implementation_scope=ALLOWED_SCOPE,
        permitted_artifacts=("development fixtures", "immutable development receipts"),
        provisional_decisions=("development-only module boundary",),
        required_evidence_return=("provider evidence", "attributable human evidence"),
        disposal_or_migration_policy="invalidate fixtures before any governed migration",
        budget_and_stop_conditions=("no external spend", "stop on authority drift"),
        promotion_conditions=("new evidence-closure receipt", "new production authority"),
        expiry_or_completion_condition="expires when OD-AM-001 is withdrawn or superseded",
        prohibited_claims=("production_ready", "certified", "provider_validated"),
    )


def authority(
    *,
    permitted_outcomes: tuple[AuthorizationOutcome, ...] = (
        AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION,
        AuthorizationOutcome.AUTHORIZED_FOR_PROTOTYPE_ONLY,
    ),
    allowed_scope: tuple[str, ...] = ALLOWED_SCOPE,
) -> AuthorizationAuthority:
    return AuthorizationAuthority(
        authority_id="od-am-001-standing-implementation-authority",
        authority_version="1",
        authority_sha256=digest("od-am-001-authority-bytes"),
        authorized_subject_identity=SUBJECT_IDENTITY,
        permitted_outcomes=permitted_outcomes,
        allowed_scope=allowed_scope,
        invalidation_conditions=EXPIRY_CONDITIONS,
    )


def issue_payload(
    *,
    axes: tuple[AuthorizationAxis, ...] | None = None,
    outcome: AuthorizationOutcome = (
        AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION
    ),
    allowed_scope: tuple[str, ...] = ALLOWED_SCOPE,
    maturity_state: str = "development_validated",
    terms: PrototypeAuthorizationTerms | None = None,
) -> str:
    return compute_authorization_payload_sha256(
        subject_identity=SUBJECT_IDENTITY,
        outcome=outcome,
        maturity_state=maturity_state,
        authorization_axes=axes or authorization_axes(),
        allowed_scope=allowed_scope,
        prohibited_scope=PROHIBITED_SCOPE,
        limitations=LIMITATIONS,
        expiry_or_completion_conditions=EXPIRY_CONDITIONS,
        predecessor_receipts=PREDECESSOR_RECEIPTS,
        prototype_terms=terms or prototype_terms(),
    )


def command(
    governed_authority: AuthorizationAuthority,
    *,
    axes: tuple[AuthorizationAxis, ...] | None = None,
    outcome: AuthorizationOutcome = (
        AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION
    ),
    allowed_scope: tuple[str, ...] = ALLOWED_SCOPE,
    maturity_state: str = "development_validated",
    terms: PrototypeAuthorizationTerms | None = None,
) -> AuthorizationCommand:
    return AuthorizationCommand(
        command_id="issue-st-08-06-development-authorization-v1",
        subject_identity=SUBJECT_IDENTITY,
        outcome=outcome,
        payload_sha256=issue_payload(
            axes=axes,
            outcome=outcome,
            allowed_scope=allowed_scope,
            maturity_state=maturity_state,
            terms=terms,
        ),
        expected_authority_identity=governed_authority.authority_identity,
    )


def issue_receipt(
    *,
    axes: tuple[AuthorizationAxis, ...] | None = None,
    outcome: AuthorizationOutcome = (
        AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION
    ),
    allowed_scope: tuple[str, ...] = ALLOWED_SCOPE,
    maturity_state: str = "development_validated",
    terms: PrototypeAuthorizationTerms | None = None,
    governed_authority: AuthorizationAuthority | None = None,
):
    axes = axes or authorization_axes()
    terms = terms or prototype_terms()
    governed_authority = governed_authority or authority(allowed_scope=allowed_scope)
    return issue_development_authorization_receipt(
        subject_identity=SUBJECT_IDENTITY,
        outcome=outcome,
        maturity_state=maturity_state,
        authorization_axes=axes,
        allowed_scope=allowed_scope,
        prohibited_scope=PROHIBITED_SCOPE,
        limitations=LIMITATIONS,
        expiry_or_completion_conditions=EXPIRY_CONDITIONS,
        predecessor_receipts=PREDECESSOR_RECEIPTS,
        prototype_terms=terms,
        command=command(
            governed_authority,
            axes=axes,
            outcome=outcome,
            allowed_scope=allowed_scope,
            maturity_state=maturity_state,
            terms=terms,
        ),
        authority=governed_authority,
    )


def test_bounded_development_authorization_receipt_names_exact_scope_and_authority() -> None:
    receipt = issue_receipt()

    assert receipt.subject_identity == SUBJECT_IDENTITY
    assert receipt.outcome is (
        AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION
    )
    assert receipt.maturity_state == "development_validated"
    assert receipt.allowed_scope == ALLOWED_SCOPE
    assert receipt.prohibited_scope == PROHIBITED_SCOPE
    assert receipt.limitations == LIMITATIONS
    assert receipt.expiry_or_completion_conditions == EXPIRY_CONDITIONS
    assert receipt.predecessor_receipts == PREDECESSOR_RECEIPTS
    assert receipt.authority_identity == authority().authority_identity
    assert len(receipt.receipt_identity) == 64


def test_all_authorization_axes_remain_independent_and_visible() -> None:
    receipt = issue_receipt()
    statuses = {axis.axis_id: axis.status for axis in receipt.authorization_axes}

    assert statuses == {
        "implementation": AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS,
        "evidence": AuthorizationAxisStatus.PENDING,
        "runtime": AuthorizationAxisStatus.NOT_AUTHORIZED,
        "deployment": AuthorizationAxisStatus.NOT_AUTHORIZED,
        "production": AuthorizationAxisStatus.FALSE,
        "certification": AuthorizationAxisStatus.FALSE,
        "provider_validation": AuthorizationAxisStatus.PENDING,
        "human_reaction_validation": AuthorizationAxisStatus.PENDING,
    }


def test_serialized_receipt_does_not_hide_open_gates_behind_aggregate_status() -> None:
    serialized = issue_receipt().as_dict()
    axes = {axis["axis_id"]: axis for axis in serialized["authorization_axes"]}

    assert set(axes) == {
        "implementation",
        "evidence",
        "runtime",
        "deployment",
        "production",
        "certification",
        "provider_validation",
        "human_reaction_validation",
    }
    assert all(axis["evidence_refs"] for axis in axes.values())
    assert all(axis["limitation"] for axis in axes.values())
    assert "overall_status" not in serialized
    assert "aggregate_readiness" not in serialized
    assert serialized["production_ready"] is False
    assert serialized["certified"] is False
    assert serialized["evidence_gate_closed"] is False


def test_prototype_only_receipt_preserves_every_required_governed_term() -> None:
    receipt = issue_receipt(outcome=AuthorizationOutcome.AUTHORIZED_FOR_PROTOTYPE_ONLY)
    terms = receipt.prototype_terms.as_dict()

    assert set(terms) == {
        "empirical_question",
        "allowed_implementation_scope",
        "permitted_artifacts",
        "provisional_decisions",
        "required_evidence_return",
        "disposal_or_migration_policy",
        "budget_and_stop_conditions",
        "promotion_conditions",
        "expiry_or_completion_condition",
        "prohibited_claims",
    }
    assert terms["required_evidence_return"]
    assert terms["promotion_conditions"]
    assert "production_ready" in terms["prohibited_claims"]


@pytest.mark.parametrize(
    "axis_id",
    (
        "implementation",
        "evidence",
        "runtime",
        "deployment",
        "production",
        "certification",
        "provider_validation",
        "human_reaction_validation",
    ),
)
def test_missing_independent_axis_fails_closed(axis_id: str) -> None:
    incomplete = tuple(axis for axis in authorization_axes() if axis.axis_id != axis_id)

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(axes=incomplete)

    assert caught.value.code == "MISSING_AUTHORIZATION_AXIS"


def test_duplicate_axis_cannot_hide_a_missing_or_conflicting_gate() -> None:
    axes = authorization_axes()

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(axes=axes + (axes[0],))

    assert caught.value.code == "DUPLICATE_AUTHORIZATION_AXIS"


@pytest.mark.parametrize(
    ("axis_id", "forged_status", "expected_code"),
    (
        ("production", AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS, "PRODUCTION_AUTHORIZATION_PROHIBITED"),
        ("certification", AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS, "CERTIFICATION_AUTHORIZATION_PROHIBITED"),
        ("provider_validation", AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS, "PROVIDER_VALIDATION_WITHOUT_EXECUTION"),
        ("human_reaction_validation", AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS, "HUMAN_REACTION_VALIDATION_WITHOUT_EVIDENCE"),
    ),
)
def test_development_completion_cannot_promote_unproven_authorization_axes(
    axis_id: str,
    forged_status: AuthorizationAxisStatus,
    expected_code: str,
) -> None:
    axes = tuple(
        replace(axis, status=forged_status) if axis.axis_id == axis_id else axis
        for axis in authorization_axes()
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(axes=axes)

    assert caught.value.code == expected_code


@pytest.mark.parametrize("maturity", ("shadow_ready", "production_ready", "certified"))
def test_od_am_001_cannot_issue_maturity_above_development_validated(maturity: str) -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(maturity_state=maturity)

    assert caught.value.code == "MATURITY_EXCEEDS_OD_AM_001_MAXIMUM"


def test_authorization_cannot_expand_beyond_issuing_authority_scope() -> None:
    narrower = authority(allowed_scope=(ALLOWED_SCOPE[0],))

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(governed_authority=narrower)

    assert caught.value.code == "AUTHORIZATION_SCOPE_EXCEEDS_AUTHORITY"


def test_outcome_must_be_explicitly_permitted_by_authority() -> None:
    prototype_only_authority = authority(
        permitted_outcomes=(AuthorizationOutcome.AUTHORIZED_FOR_PROTOTYPE_ONLY,)
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(governed_authority=prototype_only_authority)

    assert caught.value.code == "AUTHORIZATION_OUTCOME_NOT_PERMITTED"


def test_exact_command_payload_binding_is_required() -> None:
    governed_authority = authority()
    governed_command = replace(
        command(governed_authority),
        payload_sha256=digest("forged-aggregate-payload"),
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_development_authorization_receipt(
            subject_identity=SUBJECT_IDENTITY,
            outcome=AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION,
            maturity_state="development_validated",
            authorization_axes=authorization_axes(),
            allowed_scope=ALLOWED_SCOPE,
            prohibited_scope=PROHIBITED_SCOPE,
            limitations=LIMITATIONS,
            expiry_or_completion_conditions=EXPIRY_CONDITIONS,
            predecessor_receipts=PREDECESSOR_RECEIPTS,
            prototype_terms=prototype_terms(),
            command=governed_command,
            authority=governed_authority,
        )

    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"


def test_identical_governed_receipts_have_identical_bytes_and_identity() -> None:
    first = issue_receipt()
    second = issue_receipt()

    assert first.receipt_identity == second.receipt_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())

