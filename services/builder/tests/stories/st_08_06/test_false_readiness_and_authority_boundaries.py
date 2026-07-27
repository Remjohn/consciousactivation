from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.development_readiness import (
    READINESS_DIMENSIONS,
    AuthorityStatus,
    AuthorizationOutcome,
    DevelopmentReadinessError,
    DevelopmentReadinessReceipt,
    EvidenceReference,
    HardGateAssessment,
    HardGateStatus,
    MaturityState,
    ReadinessAction,
    ReadinessAuthority,
    ReadinessCommand,
    ReadinessDimensionAssessment,
    ReadinessDimensionStatus,
    ReadinessLifecycleAuthority,
    ReadinessSubject,
    build_readiness_rejection_receipt,
    compute_readiness_issue_payload_sha256,
    issue_development_readiness_receipt,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def evidence(
    label: str,
    *,
    evidence_class: str = "governed_development_result",
) -> EvidenceReference:
    return EvidenceReference(
        ref_id=f"evidence:{label}",
        version="1.0.0-development",
        sha256=digest(label),
        evidence_class=evidence_class,
        subject_identity=digest(f"subject:{label}"),
    )


def dimensions(
    *,
    evidence_class: str = "governed_development_result",
) -> tuple[ReadinessDimensionAssessment, ...]:
    return tuple(
        ReadinessDimensionAssessment(
            dimension=dimension,
            status=ReadinessDimensionStatus.PASS,
            evidence_refs=(evidence(f"dimension:{dimension}", evidence_class=evidence_class),),
            limitation="development-only evidence; external evidence gates remain open",
            failure_context="",
            not_applicable_basis=None,
        )
        for dimension in READINESS_DIMENSIONS
    )


def readiness_authority(
    *,
    applicable_scope: tuple[str, ...] = ("OD_AM_001_OFFLINE_DEVELOPMENT",),
    signatory_refs: tuple[str, ...] = (digest("OD-AM-001:standing-human-authority"),),
) -> ReadinessAuthority:
    return ReadinessAuthority(
        authority_id="od-am-001-st-08.06-development-readiness-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-08.06-readiness-authority"),
        applicable_scope=applicable_scope,
        signatory_refs=signatory_refs,
    )


def lifecycle_authority(
    *actions: ReadinessAction,
    status: AuthorityStatus = AuthorityStatus.ACTIVE,
) -> ReadinessLifecycleAuthority:
    return ReadinessLifecycleAuthority(
        authority_id="od-am-001-st-08.06-lifecycle-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-08.06-lifecycle-authority"),
        permitted_actions=actions or (ReadinessAction.ISSUE,),
        status=status,
    )


def readiness_receipt(**changes: object) -> DevelopmentReadinessReceipt:
    exact_refs = dimensions()
    values: dict[str, object] = {
        "subject": ReadinessSubject(
            subject_id="synthetic_text_normalization_v1",
            subject_version="1.0.0-development",
            subject_sha256=digest("synthetic_text_normalization_v1"),
            target_category="CATEGORY_NEUTRAL_SYNTHETIC",
            target_profile="synthetic_text_normalization_v1",
        ),
        "maturity": MaturityState.DEVELOPMENT_VALIDATED,
        "outcome": AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION,
        "dimensions": exact_refs,
        "hard_gates": (
            HardGateAssessment(
                gate_id="HG-009",
                status=HardGateStatus.PASS,
                evidence_refs=(evidence("HG-009:false-readiness-negative-tests"),),
                failure_context="",
            ),
            HardGateAssessment(
                gate_id="HG-010",
                status=HardGateStatus.PASS,
                evidence_refs=(evidence("HG-010:binding-anti-goal-negative-tests"),),
                failure_context="",
            ),
        ),
        "exact_evidence_refs": tuple(
            assessment.evidence_refs[0] for assessment in exact_refs
        )
        + (
            evidence("st-08.03-scorecard-receipt"),
            evidence("st-08.04-diagnosis-receipt"),
            evidence("st-08.05-repair-receipt"),
        ),
        "predecessor_receipts": (
            digest("st-08.03-implementation-receipt"),
            digest("st-08.04-implementation-receipt"),
            digest("st-08.05-implementation-receipt"),
        ),
        "authority": readiness_authority(),
        "applicable_scope": ("OD_AM_001_OFFLINE_DEVELOPMENT",),
        "excluded_scope": (
            "PRODUCTION",
            "CERTIFICATION",
            "EXTERNAL_PROVIDER_VALIDATION",
            "REAL_HUMAN_REACTION_VALIDATION",
        ),
        "limitations": (
            "BD-007 provider execution remains open",
            "no attributable real-human reaction evidence exists",
        ),
        "unresolved_gates": (
            "external_provider_validation",
            "human_reaction_validation",
            "production_readiness",
            "certification",
        ),
        "invalidation_conditions": (
            "source_lock_or_Harness_IR_changes",
            "governed_evidence_or_authority_changes",
        ),
        "implementation_completion": "IMPLEMENTED_DEVELOPMENT_PASS",
        "evidence_closure": "pending",
        "runtime_authorization": "not_authorized",
        "deployment_authorization": "not_authorized",
        "external_provider_validation": "pending",
        "human_reaction_validation": "pending",
        "production_ready": False,
        "certified": False,
    }
    values.update(changes)
    return DevelopmentReadinessReceipt(**values)


def issue_receipt(
    *,
    receipt: DevelopmentReadinessReceipt | None = None,
    authority: ReadinessLifecycleAuthority | None = None,
    command: ReadinessCommand | None = None,
) -> DevelopmentReadinessReceipt:
    candidate = receipt or readiness_receipt()
    governed_authority = authority or lifecycle_authority(ReadinessAction.ISSUE)
    governed_command = command or ReadinessCommand(
        command_id="issue-development-readiness-v1",
        action=ReadinessAction.ISSUE,
        resource_id=candidate.receipt_identity,
        payload_sha256=compute_readiness_issue_payload_sha256(candidate),
        expected_authority_identity=governed_authority.authority_identity,
    )
    return issue_development_readiness_receipt(
        candidate,
        governed_command,
        governed_authority,
    )


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"production_ready": True}, "PRODUCTION_AUTHORIZATION_PROHIBITED"),
        ({"certified": True}, "CERTIFICATION_PROHIBITED"),
        ({"evidence_closure": "closed"}, "EVIDENCE_CLOSURE_NOT_PROVEN"),
        ({"runtime_authorization": "authorized"}, "RUNTIME_AUTHORIZATION_PROHIBITED"),
        ({"deployment_authorization": "authorized"}, "DEPLOYMENT_AUTHORIZATION_PROHIBITED"),
    ),
)
def test_development_completion_cannot_imply_higher_authorization(
    change: dict[str, object], expected_code: str
) -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(**change)

    assert caught.value.code == expected_code


def test_provider_validation_requires_real_provider_execution_evidence() -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(external_provider_validation="validated")

    assert caught.value.code == "PROVIDER_VALIDATION_WITHOUT_EXECUTION"


def test_human_reaction_validation_requires_attributable_human_evidence() -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(human_reaction_validation="validated")

    assert caught.value.code == "HUMAN_REACTION_VALIDATION_WITHOUT_EVIDENCE"


def test_document_or_schema_presence_cannot_pass_readiness_dimensions() -> None:
    document_dimensions = dimensions(evidence_class="document_or_schema_presence")

    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(
            dimensions=document_dimensions,
            exact_evidence_refs=tuple(item.evidence_refs[0] for item in document_dimensions),
        )

    assert caught.value.code == "DOCUMENT_PRESENCE_IS_NOT_READINESS"


def test_required_signatory_and_exact_authority_scope_are_mandatory() -> None:
    with pytest.raises(DevelopmentReadinessError) as missing_signatory:
        readiness_receipt(authority=readiness_authority(signatory_refs=()))
    assert missing_signatory.value.code == "MISSING_SIGNATORY_AUTHORITY"

    with pytest.raises(DevelopmentReadinessError) as wrong_scope:
        readiness_receipt(
            authority=readiness_authority(applicable_scope=("UNRELATED_SCOPE",))
        )
    assert wrong_scope.value.code == "AUTHORITY_SCOPE_MISMATCH"


@pytest.mark.parametrize(
    "status", (AuthorityStatus.SUPERSEDED, AuthorityStatus.INVALIDATED)
)
def test_stale_or_invalidated_lifecycle_authority_cannot_issue(status: AuthorityStatus) -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(authority=lifecycle_authority(ReadinessAction.ISSUE, status=status))

    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_lifecycle_authority_must_explicitly_grant_issue() -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(authority=lifecycle_authority(ReadinessAction.INVALIDATE))

    assert caught.value.code == "UNAUTHORIZED_ACTION"


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"resource_id": digest("wrong-resource")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        (
            {"expected_authority_identity": digest("wrong-authority")},
            "AUTHORITY_IDENTITY_MISMATCH",
        ),
    ),
)
def test_issue_requires_exact_command_resource_payload_and_authority(
    change: dict[str, object], expected_code: str
) -> None:
    candidate = readiness_receipt()
    auth = lifecycle_authority(ReadinessAction.ISSUE)
    command = ReadinessCommand(
        command_id="issue-boundary-test",
        action=ReadinessAction.ISSUE,
        resource_id=candidate.receipt_identity,
        payload_sha256=compute_readiness_issue_payload_sha256(candidate),
        expected_authority_identity=auth.authority_identity,
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        issue_receipt(receipt=candidate, authority=auth, command=replace(command, **change))

    assert caught.value.code == expected_code


def test_atomic_failure_emits_only_deterministic_zero_state_rejection() -> None:
    candidate = readiness_receipt()
    auth = lifecycle_authority(ReadinessAction.ISSUE)
    command = ReadinessCommand(
        command_id="atomic-readiness-failure",
        action=ReadinessAction.ISSUE,
        resource_id=candidate.receipt_identity,
        payload_sha256=digest("conflicting-payload"),
        expected_authority_identity=auth.authority_identity,
    )
    issued = None

    with pytest.raises(DevelopmentReadinessError) as caught:
        issued = issue_receipt(receipt=candidate, authority=auth, command=command)

    rejection = build_readiness_rejection_receipt(
        error=caught.value,
        command_id=command.command_id,
        payload_sha256=command.payload_sha256,
        authority_identity=auth.authority_identity,
    )
    repeated = build_readiness_rejection_receipt(
        error=caught.value,
        command_id=command.command_id,
        payload_sha256=command.payload_sha256,
        authority_identity=auth.authority_identity,
    )

    assert issued is None
    assert rejection.error_code == "COMMAND_PAYLOAD_MISMATCH"
    assert rejection.partial_state_count == 0
    assert rejection.as_dict() == repeated.as_dict()
    assert rejection.rejection_identity == repeated.rejection_identity
