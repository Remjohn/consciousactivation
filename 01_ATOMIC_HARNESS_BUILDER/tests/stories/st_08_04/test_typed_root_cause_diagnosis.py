from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib

import pytest

from cmf_builder.evaluation.root_cause_diagnosis import (
    PRIMARY_FAILURE_CLASSES,
    UNKNOWN_FAILURE_CODE,
    DiagnosticLayer,
    DiagnosisStatus,
    FailureClassification,
    HypothesisTestResult,
    HypothesisTestStatus,
    PrimaryFailureClass,
    RootCauseDiagnosis,
    RootCauseDiagnosisError,
    canonical_json_bytes,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def classification(
    *,
    stable_code: str = "SEMANTIC_LINEAGE_FLATTENED",
    primary_class: PrimaryFailureClass | None = PrimaryFailureClass.CONTRACT,
    localization_layer: DiagnosticLayer | None = DiagnosticLayer.SEMANTIC,
    **changes: object,
) -> FailureClassification:
    values: dict[str, object] = {
        "failure_id": "failure-semantic-lineage-v1",
        "stable_code": stable_code,
        "primary_class": primary_class,
        "localization_layer": localization_layer,
        "contributing_factors": (
            "projection omitted rich-object lineage reference",
            "contract conformance check detected the omission",
        ),
    }
    values.update(changes)
    return FailureClassification(**values)  # type: ignore[arg-type]


def hypothesis_result(
    hypothesis_id: str,
    hypothesis: str,
    status: HypothesisTestStatus,
    *,
    rejection_reason: str | None = None,
    evidence_label: str | None = None,
) -> HypothesisTestResult:
    return HypothesisTestResult(
        hypothesis_id=hypothesis_id,
        hypothesis=hypothesis,
        test_description=f"reproduce and isolate {hypothesis_id}",
        status=status,
        evidence_refs=(digest(evidence_label or f"{hypothesis_id}:test-evidence"),),
        result_summary=f"governed result for {hypothesis_id}",
        rejection_reason=rejection_reason,
    )


SUPPORTED_HYPOTHESIS = "semantic projection dropped the rich lineage reference"
REJECTED_HYPOTHESIS = "source IR never contained the lineage reference"


def localized_diagnosis(**changes: object) -> RootCauseDiagnosis:
    tests = (
        hypothesis_result(
            "hypothesis-projection-flattening",
            SUPPORTED_HYPOTHESIS,
            HypothesisTestStatus.SUPPORTED,
        ),
        hypothesis_result(
            "hypothesis-source-omission",
            REJECTED_HYPOTHESIS,
            HypothesisTestStatus.REJECTED,
            rejection_reason="the immutable source IR contains the exact rich-object lineage",
        ),
    )
    values: dict[str, object] = {
        "diagnosis_id": "root-cause-diagnosis-semantic-lineage-v1",
        "diagnosis_version": "1.0.0-development",
        "classification": classification(),
        "observed_symptom": "the rendered projection lacks a rich-object lineage reference",
        "reproduction_or_evidence_refs": (
            digest("failed-artifact"),
            digest("reproduction-receipt"),
            digest("st-08.03-scoring-receipt"),
        ),
        "affected_boundary": "semantic projection boundary",
        "competing_hypotheses": tuple(item.hypothesis_id for item in tests),
        "hypothesis_tests_and_results": tests,
        "status": DiagnosisStatus.LOCALIZED,
        "selected_root_cause": SUPPORTED_HYPOTHESIS,
        "confidence_basis": (
            "the controlled reproduction preserves the source IR",
            "only the projection step removes the lineage reference",
            "the alternate source-omission hypothesis is contradicted by immutable bytes",
        ),
        "smallest_supported_responsible_layer": DiagnosticLayer.SEMANTIC,
        "responsible_owner": "Builder semantic projection owner",
        "responsible_authority_ref": digest("builder-semantic-projection-authority"),
        "unaffected_frozen_state": (
            digest("source-lock"),
            digest("ratified-boundary"),
            digest("source-ir"),
        ),
        "exact_lineage": (
            digest("st-08.03-scoring-receipt"),
            digest("failed-artifact"),
            digest("reproduction-receipt"),
        ),
        "escalation_route": None,
    }
    values.update(changes)
    return RootCauseDiagnosis(**values)  # type: ignore[arg-type]


def unresolved_diagnosis(**changes: object) -> RootCauseDiagnosis:
    tests = (
        hypothesis_result(
            "hypothesis-semantic-layer",
            "semantic projection lost lineage",
            HypothesisTestStatus.INCONCLUSIVE,
        ),
        hypothesis_result(
            "hypothesis-context-layer",
            "minimum context omitted lineage",
            HypothesisTestStatus.INCONCLUSIVE,
        ),
    )
    values: dict[str, object] = {
        "diagnosis_id": "root-cause-diagnosis-unresolved-v1",
        "diagnosis_version": "1.0.0-development",
        "classification": classification(
            stable_code=UNKNOWN_FAILURE_CODE,
            primary_class=None,
            localization_layer=None,
            contributing_factors=("current evidence cannot distinguish two layers",),
        ),
        "observed_symptom": "the output lineage is incomplete",
        "reproduction_or_evidence_refs": (
            digest("unresolved-failed-artifact"),
            digest("unresolved-reproduction"),
        ),
        "affected_boundary": "semantic and context boundary unresolved",
        "competing_hypotheses": tuple(item.hypothesis_id for item in tests),
        "hypothesis_tests_and_results": tests,
        "status": DiagnosisStatus.UNKNOWN_REQUIRES_TRIAGE,
        "selected_root_cause": None,
        "confidence_basis": (
            "the same symptom reproduces with both candidate inputs",
            "available evidence cannot isolate one responsible layer",
        ),
        "smallest_supported_responsible_layer": None,
        "responsible_owner": None,
        "responsible_authority_ref": None,
        "unaffected_frozen_state": (digest("unresolved-source-lock"),),
        "exact_lineage": (
            digest("unresolved-scoring-receipt"),
            digest("unresolved-failed-artifact"),
        ),
        "escalation_route": "BLOCKED_PENDING_TYPED_TRIAGE",
    }
    values.update(changes)
    return RootCauseDiagnosis(**values)  # type: ignore[arg-type]


def test_stable_primary_failure_taxonomy_is_exact_and_has_no_catch_all_bucket() -> None:
    assert PRIMARY_FAILURE_CLASSES == (
        "evidence",
        "visual_parse",
        "atomicity",
        "authority",
        "contract",
        "module",
        "skill",
        "capsule",
        "benchmark",
        "budget",
        "provider",
        "observability",
        "migration",
        "downstream_implementation",
    )
    assert tuple(item.value for item in PrimaryFailureClass) == PRIMARY_FAILURE_CLASSES
    assert UNKNOWN_FAILURE_CODE == "UNKNOWN_REQUIRES_TRIAGE"
    assert UNKNOWN_FAILURE_CODE not in PRIMARY_FAILURE_CLASSES


def test_localized_diagnosis_contains_every_capsule_required_typed_field() -> None:
    diagnosis = localized_diagnosis()
    payload = diagnosis.as_dict()

    assert set(
        (
            "diagnosis_id",
            "diagnosis_version",
            "failure_id_and_stable_code",
            "observed_symptom",
            "reproduction_or_evidence_refs",
            "affected_boundary",
            "competing_hypotheses",
            "hypothesis_tests_and_results",
            "selected_root_cause_or_unresolved_status",
            "confidence_basis",
            "smallest_supported_responsible_layer",
            "responsible_owner_and_authority_ref",
            "unaffected_frozen_state",
            "exact_lineage",
            "diagnosis_receipt_id",
        )
    ).issubset(payload)
    assert payload["failure_id_and_stable_code"] == diagnosis.classification.as_dict()
    assert payload["selected_root_cause_or_unresolved_status"] == {
        "status": "localized",
        "selected_root_cause": SUPPORTED_HYPOTHESIS,
        "escalation_route": None,
    }
    assert payload["smallest_supported_responsible_layer"] == "semantic"
    assert payload["diagnosis_receipt_id"] == diagnosis.diagnosis_receipt_id


def test_observed_symptom_cannot_be_accepted_as_the_root_cause() -> None:
    symptom = "the rendered projection lacks a rich-object lineage reference"

    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(selected_root_cause=symptom)

    assert caught.value.code == "SYMPTOM_IS_NOT_ROOT_CAUSE"


def test_selected_root_cause_must_be_exactly_one_supported_hypothesis() -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(selected_root_cause=REJECTED_HYPOTHESIS)
    assert caught.value.code == "UNSUPPORTED_ROOT_CAUSE_SELECTION"

    first = hypothesis_result("hypothesis-one", "first cause", HypothesisTestStatus.SUPPORTED)
    second = hypothesis_result("hypothesis-two", "second cause", HypothesisTestStatus.SUPPORTED)
    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(
            competing_hypotheses=(first.hypothesis_id, second.hypothesis_id),
            hypothesis_tests_and_results=(first, second),
            selected_root_cause=first.hypothesis,
        )
    assert caught.value.code == "MULTIPLE_SUPPORTED_ROOT_CAUSES"


def test_every_competing_hypothesis_retains_test_evidence_and_rejection_reason() -> None:
    diagnosis = localized_diagnosis()
    results = {item.hypothesis_id: item for item in diagnosis.hypothesis_tests_and_results}

    assert set(results) == set(diagnosis.competing_hypotheses)
    assert all(item.evidence_refs for item in results.values())
    assert results["hypothesis-source-omission"].status is HypothesisTestStatus.REJECTED
    assert results["hypothesis-source-omission"].rejection_reason

    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(
            competing_hypotheses=(
                "hypothesis-projection-flattening",
                "hypothesis-source-omission",
                "hypothesis-never-tested",
            )
        )
    assert caught.value.code == "MISSING_HYPOTHESIS_TEST_EVIDENCE"


def test_localized_diagnosis_requires_evidence_qualified_confidence() -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(confidence_basis=())

    assert caught.value.code == "MISSING_CONFIDENCE_BASIS"


def test_one_smallest_responsible_layer_must_match_the_classification() -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(smallest_supported_responsible_layer=None)
    assert caught.value.code == "MISSING_RESPONSIBLE_LAYER"

    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(smallest_supported_responsible_layer=DiagnosticLayer.CONTEXT)
    assert caught.value.code == "LAYER_LOCALIZATION_MISMATCH"


def test_unknown_failure_is_explicit_blocked_and_cannot_be_forced_known() -> None:
    diagnosis = unresolved_diagnosis()
    payload = diagnosis.as_dict()

    assert diagnosis.status is DiagnosisStatus.UNKNOWN_REQUIRES_TRIAGE
    assert diagnosis.classification.stable_code == UNKNOWN_FAILURE_CODE
    assert diagnosis.classification.primary_class is None
    assert diagnosis.smallest_supported_responsible_layer is None
    assert payload["selected_root_cause_or_unresolved_status"] == {
        "status": "unknown_requires_triage",
        "selected_root_cause": None,
        "escalation_route": "BLOCKED_PENDING_TYPED_TRIAGE",
    }
    assert payload["repair_route"] == "BLOCKED"

    with pytest.raises(RootCauseDiagnosisError) as caught:
        classification(
            stable_code=UNKNOWN_FAILURE_CODE,
            primary_class=PrimaryFailureClass.EVIDENCE,
            localization_layer=DiagnosticLayer.SOURCE_AND_EVIDENCE,
        )
    assert caught.value.code == "UNKNOWN_CLASSIFICATION_FORCED"


def test_unresolved_evidence_cannot_select_a_layer_owner_or_repair_route() -> None:
    override_cases = (
        {"selected_root_cause": "guess that context is responsible"},
        {"smallest_supported_responsible_layer": DiagnosticLayer.CONTEXT},
        {"responsible_owner": "context owner"},
        {"responsible_authority_ref": digest("guessed-authority")},
        {"escalation_route": None},
    )

    for overrides in override_cases:
        with pytest.raises(RootCauseDiagnosisError) as caught:
            unresolved_diagnosis(**overrides)
        assert caught.value.code in {
            "UNKNOWN_DIAGNOSIS_MUST_REMAIN_UNRESOLVED",
            "MISSING_TRIAGE_ESCALATION",
        }


def test_diagnosis_records_are_frozen_and_detect_post_construction_tampering() -> None:
    diagnosis = localized_diagnosis()
    with pytest.raises(FrozenInstanceError):
        diagnosis.observed_symptom = "silently rewritten symptom"  # type: ignore[misc]

    original_identity = diagnosis.diagnosis_identity
    object.__setattr__(diagnosis, "exact_lineage", (digest("forged-lineage"),))
    with pytest.raises(RootCauseDiagnosisError) as caught:
        diagnosis.as_dict()
    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert original_identity


def test_identical_governed_inputs_produce_byte_identical_diagnoses_and_receipts() -> None:
    first = localized_diagnosis()
    second = localized_diagnosis()

    assert first.diagnosis_identity == second.diagnosis_identity
    assert first.diagnosis_receipt_id == second.diagnosis_receipt_id
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())


@pytest.mark.parametrize(
    ("field", "changed_value"),
    (
        ("observed_symptom", "a different governed symptom"),
        ("affected_boundary", "a different governed boundary"),
        ("confidence_basis", ("different evidence-qualified confidence basis",)),
        ("exact_lineage", (digest("different-lineage"),)),
        ("responsible_authority_ref", digest("different-authority")),
    ),
)
def test_changed_governed_input_changes_diagnosis_and_receipt_identity(
    field: str,
    changed_value: object,
) -> None:
    original = localized_diagnosis()
    changed = replace(original, **{field: changed_value})

    assert changed.diagnosis_identity != original.diagnosis_identity
    assert changed.diagnosis_receipt_id != original.diagnosis_receipt_id


@pytest.mark.parametrize(
    "claim",
    (
        "repair_selected",
        "repair_executed",
        "evidence_gate_closed",
        "production_ready",
        "certified",
    ),
)
def test_diagnosis_cannot_execute_repair_or_claim_evidence_production_or_certification(
    claim: str,
) -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        localized_diagnosis(**{claim: True})

    if claim in {"repair_selected", "repair_executed"}:
        assert caught.value.code == "PROHIBITED_REPAIR_EXECUTION"
    else:
        assert caught.value.code == "PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM"


def test_serialized_diagnosis_preserves_the_development_only_claim_ceiling() -> None:
    payload = localized_diagnosis().as_dict()

    assert payload["repair_route"] == "DIAGNOSIS_ONLY_NO_EXECUTION"
    assert payload["repair_selected"] is False
    assert payload["repair_executed"] is False
    assert payload["evidence_gate_closed"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False

