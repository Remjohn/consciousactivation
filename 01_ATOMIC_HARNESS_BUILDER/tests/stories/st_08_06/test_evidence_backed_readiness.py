from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.development_readiness import (
    READINESS_DIMENSIONS,
    AuthorizationOutcome,
    DevelopmentReadinessError,
    DevelopmentReadinessReceipt,
    EvidenceReference,
    HardGateAssessment,
    HardGateStatus,
    MaturityState,
    ReadinessAuthority,
    ReadinessDimensionAssessment,
    ReadinessDimensionStatus,
    ReadinessSubject,
    canonical_json_bytes,
)


EXPECTED_DIMENSIONS = (
    "evidence_saturation",
    "atomicity",
    "constitutional_authority",
    "Harness_IR_consistency",
    "phases",
    "contexts",
    "contracts",
    "modules",
    "skill_maturity",
    "benchmark_results",
    "repair_coverage",
    "observability",
    "budgets",
    "target_specific_requirements",
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def evidence(
    label: str,
    *,
    evidence_class: str = "governed_development_receipt",
    subject_identity: str | None = None,
) -> EvidenceReference:
    return EvidenceReference(
        ref_id=f"evidence:{label}",
        version="1.0.0-development",
        sha256=digest(f"{label}:immutable-bytes"),
        evidence_class=evidence_class,
        subject_identity=subject_identity or digest(f"{label}:subject"),
    )


def subject() -> ReadinessSubject:
    return ReadinessSubject(
        subject_id="synthetic-text-normalization-development-definition",
        subject_version="1.0.0-development",
        subject_sha256=digest("synthetic-text-normalization-definition"),
        target_category="generic_non_activative",
        target_profile="synthetic_text_normalization_v1",
    )


def authority() -> ReadinessAuthority:
    return ReadinessAuthority(
        authority_id="od-am-001-st-08.06-development-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-08.06-authority-bytes"),
        applicable_scope=("OD_AM_001_OFFLINE_DEVELOPMENT",),
        signatory_refs=(digest("governed-campaign-authorization"),),
    )


def dimensions(
    *,
    status_by_dimension: dict[str, ReadinessDimensionStatus] | None = None,
) -> tuple[ReadinessDimensionAssessment, ...]:
    statuses = status_by_dimension or {}
    return tuple(
        ReadinessDimensionAssessment(
            dimension=dimension,
            status=statuses.get(dimension, ReadinessDimensionStatus.PASS),
            evidence_refs=(evidence(f"dimension:{dimension}"),),
            limitation=(
                "bounded repository-owned development evidence; no external or production claim"
            ),
            failure_context=(
                ""
                if statuses.get(dimension, ReadinessDimensionStatus.PASS)
                is ReadinessDimensionStatus.PASS
                else f"{dimension} remains unresolved for the requested scope"
            ),
            not_applicable_basis=None,
        )
        for dimension in READINESS_DIMENSIONS
    )


def hard_gates(
    *,
    status_by_gate: dict[str, HardGateStatus] | None = None,
) -> tuple[HardGateAssessment, ...]:
    statuses = status_by_gate or {}
    return tuple(
        HardGateAssessment(
            gate_id=gate_id,
            status=statuses.get(gate_id, HardGateStatus.PASS),
            evidence_refs=(evidence(f"hard-gate:{gate_id}"),),
            failure_context=(
                ""
                if statuses.get(gate_id, HardGateStatus.PASS) is HardGateStatus.PASS
                else f"{gate_id} failed and cannot be averaged or agent-waived"
            ),
        )
        for gate_id in ("HG-009", "HG-010")
    )


def readiness_receipt(
    *,
    supplied_dimensions: tuple[ReadinessDimensionAssessment, ...] | None = None,
    supplied_hard_gates: tuple[HardGateAssessment, ...] | None = None,
    maturity: MaturityState = MaturityState.DEVELOPMENT_VALIDATED,
    outcome: AuthorizationOutcome = (
        AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION
    ),
) -> DevelopmentReadinessReceipt:
    governed_subject = subject()
    return DevelopmentReadinessReceipt(
        subject=governed_subject,
        maturity=maturity,
        outcome=outcome,
        dimensions=supplied_dimensions or dimensions(),
        hard_gates=supplied_hard_gates or hard_gates(),
        exact_evidence_refs=(
            evidence("source-lock", subject_identity=governed_subject.subject_identity),
            evidence("harness-ir", subject_identity=governed_subject.subject_identity),
            evidence("category-profile"),
            evidence("phase-context-contract-module"),
            evidence("skill-maturity-and-necessity"),
            evidence("benchmark-rubric-evaluator-policy"),
            evidence("st-08.03-independent-scorecard"),
            evidence("st-08.04-diagnosis-and-repair-graph"),
            evidence("st-08.05-repair-and-targeted-regression"),
            evidence("compiler-builder-version"),
            evidence("observability-budget-target"),
        ),
        predecessor_receipts=(
            digest("st-08.03-implementation-receipt"),
            digest("st-08.04-implementation-receipt"),
            digest("st-08.05-implementation-receipt"),
        ),
        authority=authority(),
        applicable_scope=("OD_AM_001_OFFLINE_DEVELOPMENT",),
        excluded_scope=(
            "runtime_execution",
            "deployment",
            "production",
            "certification",
            "external_provider_validation",
            "real_human_reaction_validation",
        ),
        limitations=(
            "offline development evidence only",
            "BD-007 external-provider evidence remains open",
            "no attributable real-human reaction evidence exists",
        ),
        unresolved_gates=(
            "external_provider_validation",
            "human_reaction_validation",
            "production_readiness",
            "certification",
        ),
        invalidation_conditions=(
            "subject or predecessor hash changes",
            "authority or signatory scope changes",
            "dimension or hard-gate evidence changes",
        ),
        implementation_completion="IMPLEMENTED_DEVELOPMENT_PASS",
        evidence_closure="pending",
        runtime_authorization="not_authorized",
        deployment_authorization="not_authorized",
        external_provider_validation="pending",
        human_reaction_validation="pending",
        production_ready=False,
        certified=False,
    )


def test_capsule_readiness_dimensions_are_exact_complete_and_independently_visible() -> None:
    receipt = readiness_receipt()
    payload = receipt.as_dict()

    assert READINESS_DIMENSIONS == EXPECTED_DIMENSIONS
    assert tuple(item["dimension"] for item in payload["dimensions"]) == EXPECTED_DIMENSIONS
    assert len(receipt.dimensions) == 14
    assert len({item.assessment_identity for item in receipt.dimensions}) == 14
    assert all(item.evidence_refs for item in receipt.dimensions)
    assert all(item.limitation for item in receipt.dimensions)
    assert all("failure_context" in item for item in payload["dimensions"])


@pytest.mark.parametrize(
    "missing_dimension",
    ("evidence_saturation", "constitutional_authority", "benchmark_results", "budgets"),
)
def test_no_readiness_dimension_may_be_silently_omitted(missing_dimension: str) -> None:
    incomplete = tuple(
        item for item in dimensions() if item.dimension != missing_dimension
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(supplied_dimensions=incomplete)

    assert caught.value.code == "INCOMPLETE_READINESS_DIMENSION_COVERAGE"
    assert missing_dimension in caught.value.context["missing_dimensions"]


def test_dimension_evidence_is_versioned_hash_bound_and_subject_attributable() -> None:
    receipt = readiness_receipt()

    for assessment in receipt.dimensions:
        for reference in assessment.evidence_refs:
            assert reference.ref_id
            assert reference.version
            assert len(reference.sha256) == 64
            assert reference.evidence_class
            assert len(reference.subject_identity) == 64

    changed = replace(
        receipt.dimensions[0].evidence_refs[0],
        sha256=digest("changed-dimension-evidence"),
    )
    changed_dimension = replace(
        receipt.dimensions[0],
        evidence_refs=(changed,),
    )
    changed_receipt = readiness_receipt(
        supplied_dimensions=(changed_dimension, *receipt.dimensions[1:])
    )
    assert changed_receipt.receipt_identity != receipt.receipt_identity


@pytest.mark.parametrize(
    ("evidence_refs", "limitation", "expected_code"),
    (
        ((), "bounded evidence", "MISSING_DIMENSION_EVIDENCE"),
        ((evidence("atomicity"),), "", "MISSING_DIMENSION_LIMITATION"),
    ),
)
def test_document_presence_or_an_unqualified_status_cannot_pass_a_dimension(
    evidence_refs: tuple[EvidenceReference, ...],
    limitation: str,
    expected_code: str,
) -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        ReadinessDimensionAssessment(
            dimension="atomicity",
            status=ReadinessDimensionStatus.PASS,
            evidence_refs=evidence_refs,
            limitation=limitation,
            failure_context="",
            not_applicable_basis=None,
        )

    assert caught.value.code == expected_code


def test_not_applicable_requires_authoritative_target_profile_basis() -> None:
    with pytest.raises(DevelopmentReadinessError) as caught:
        ReadinessDimensionAssessment(
            dimension="target_specific_requirements",
            status=ReadinessDimensionStatus.NOT_APPLICABLE,
            evidence_refs=(evidence("target-applicability"),),
            limitation="generic non-Activative development branch",
            failure_context="",
            not_applicable_basis=None,
        )
    assert caught.value.code == "MISSING_NOT_APPLICABLE_AUTHORITY_BASIS"

    assessment = ReadinessDimensionAssessment(
        dimension="target_specific_requirements",
        status=ReadinessDimensionStatus.NOT_APPLICABLE,
        evidence_refs=(evidence("target-applicability"),),
        limitation="generic non-Activative development branch",
        failure_context="",
        not_applicable_basis=evidence(
            "generic-target-profile-applicability",
            evidence_class="authoritative_target_profile_basis",
        ),
    )
    assert assessment.status is ReadinessDimensionStatus.NOT_APPLICABLE
    assert assessment.not_applicable_basis is not None


@pytest.mark.parametrize(
    "requested_maturity",
    (
        "shadow_ready",
        "production_ready",
        "certified",
    ),
)
def test_od_am_001_maturity_cannot_exceed_development_validated(
    requested_maturity: str,
) -> None:
    with pytest.raises((DevelopmentReadinessError, ValueError)) as caught:
        readiness_receipt(maturity=requested_maturity)  # type: ignore[arg-type]

    if isinstance(caught.value, DevelopmentReadinessError):
        assert caught.value.code == "MATURITY_EXCEEDS_DEVELOPMENT_CEILING"


def test_development_validation_keeps_every_other_authorization_gate_independent() -> None:
    receipt = readiness_receipt()
    payload = receipt.as_dict()

    assert payload["implementation_completion"] == "IMPLEMENTED_DEVELOPMENT_PASS"
    assert payload["maturity"] == "development_validated"
    assert payload["evidence_closure"] == "pending"
    assert payload["runtime_authorization"] == "not_authorized"
    assert payload["deployment_authorization"] == "not_authorized"
    assert payload["external_provider_validation"] == "pending"
    assert payload["human_reaction_validation"] == "pending"
    assert payload["production_ready"] is False
    assert payload["certified"] is False
    assert set(payload["unresolved_gates"]) >= {
        "external_provider_validation",
        "human_reaction_validation",
        "production_readiness",
        "certification",
    }


@pytest.mark.parametrize(
    ("dimension", "expected_outcome"),
    (
        ("constitutional_authority", AuthorizationOutcome.BLOCKED_AUTHORITY),
        ("skill_maturity", AuthorizationOutcome.BLOCKED_SKILL_MATURITY),
        ("benchmark_results", AuthorizationOutcome.BLOCKED_BENCHMARK),
        ("evidence_saturation", AuthorizationOutcome.BLOCKED_EVIDENCE),
    ),
)
def test_failed_or_unresolved_mandatory_dimension_cannot_be_hidden_by_aggregate_passes(
    dimension: str,
    expected_outcome: AuthorizationOutcome,
) -> None:
    supplied = dimensions(
        status_by_dimension={dimension: ReadinessDimensionStatus.UNRESOLVED}
    )

    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(
            supplied_dimensions=supplied,
            outcome=AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION,
        )
    assert caught.value.code == "OUTCOME_CONTRADICTS_READINESS_EVIDENCE"
    assert caught.value.context["required_outcome"] == expected_outcome.value


@pytest.mark.parametrize(
    ("gate_id", "expected_outcome"),
    (
        ("HG-009", AuthorizationOutcome.BLOCKED_HARD_GATE),
        ("HG-010", AuthorizationOutcome.BLOCKED_ARCHITECTURE),
    ),
)
def test_non_waivable_hard_gate_failure_forces_a_blocking_outcome(
    gate_id: str,
    expected_outcome: AuthorizationOutcome,
) -> None:
    supplied = hard_gates(status_by_gate={gate_id: HardGateStatus.FAIL})

    with pytest.raises(DevelopmentReadinessError) as caught:
        readiness_receipt(
            supplied_hard_gates=supplied,
            outcome=AuthorizationOutcome.AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION,
        )
    assert caught.value.code == "OUTCOME_CONTRADICTS_HARD_GATE"
    assert caught.value.context["gate_id"] == gate_id
    assert caught.value.context["required_outcome"] == expected_outcome.value


def test_identical_governed_inputs_produce_byte_identical_receipts() -> None:
    first = readiness_receipt()
    second = readiness_receipt()

    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    assert first.receipt_identity == second.receipt_identity
    assert len(first.receipt_identity) == 64


def test_scope_authority_limitations_predecessors_and_invalidation_are_identity_bound() -> None:
    receipt = readiness_receipt()
    payload = receipt.as_dict()

    assert payload["subject"]["subject_identity"] == receipt.subject.subject_identity
    assert payload["authority"]["authority_identity"] == receipt.authority.authority_identity
    assert len(payload["predecessor_receipts"]) == 3
    assert payload["applicable_scope"] == ["OD_AM_001_OFFLINE_DEVELOPMENT"]
    assert "production" in payload["excluded_scope"]
    assert payload["limitations"]
    assert payload["invalidation_conditions"]

    changed = replace(
        receipt,
        limitations=(*receipt.limitations, "new governed limitation"),
    )
    assert changed.receipt_identity != receipt.receipt_identity

