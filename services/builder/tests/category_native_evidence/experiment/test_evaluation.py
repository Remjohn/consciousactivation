from __future__ import annotations

import pytest

from cmf_builder.category_evidence.experiment_contracts import EvidenceGateError, ExperimentArm
from cmf_builder.category_evidence.experiment_evaluation import (
    Applicability,
    DIMENSIONS,
    DimensionScore,
    NONCOMPENSABLE_FAILURES,
    Scorecard,
    rubric_identity,
    validate_paired_scorecards,
)


H = "a" * 64


def scores(
    category: int,
    locks: int,
    *,
    not_applicable: tuple[str, ...] = (),
) -> tuple[DimensionScore, ...]:
    result = []
    for dimension in DIMENSIONS:
        if dimension in not_applicable:
            result.append(
                DimensionScore(
                    dimension,
                    Applicability.NOT_APPLICABLE,
                    None,
                    "explicitly outside the generic non-Activative control",
                    (),
                )
            )
            continue
        score = category if dimension == "category_native_syntax" else locks if dimension == "wrong_reading_resistance" else 3
        result.append(DimensionScore(dimension, Applicability.APPLICABLE, score, "governed evidence", (H,)))
    return tuple(result)


def card(arm: ExperimentArm, *, category: int, locks: int, failures=()) -> Scorecard:
    return Scorecard("1.0.0", H, "CASE-1", arm, H, 1, H, scores(category, locks), tuple(failures))


def test_rubric_has_exact_required_dimensions_and_fail_closed_failures() -> None:
    assert len(DIMENSIONS) == 17
    assert "non_invention_of_human_truth" in DIMENSIONS
    assert "non_admitted_corpus_evidence_used" in NONCOMPENSABLE_FAILURES
    assert len(rubric_identity()) == 64


def test_missing_dimension_is_rejected() -> None:
    with pytest.raises(EvidenceGateError, match="coverage is incomplete"):
        Scorecard("1.0.0", H, "CASE-1", ExperimentArm.NATIVE, H, 1, H, scores(4, 4)[:-1], ())


def test_not_applicable_is_explicit_and_cannot_hide_a_score() -> None:
    with pytest.raises(EvidenceGateError, match="cannot carry"):
        DimensionScore("spatial_structure", Applicability.NOT_APPLICABLE, 4, "not spatial", ())
    valid = DimensionScore("spatial_structure", Applicability.NOT_APPLICABLE, None, "generic text control", ())
    assert valid.score is None


def test_native_advantage_is_pairwise_and_noncompensable() -> None:
    native = card(ExperimentArm.NATIVE, category=4, locks=4)
    flattened = card(ExperimentArm.FLATTENED, category=2, locks=2)
    assert validate_paired_scorecards(native, flattened) == "DEVELOPMENT_ADVANTAGE_OBSERVED_FOR_REPEAT"
    compromised = card(
        ExperimentArm.NATIVE,
        category=4,
        locks=4,
        failures=("human_truth_invented",),
    )
    assert validate_paired_scorecards(compromised, flattened) == "NATIVE_NONCOMPENSABLE_FAILURE"


def test_high_average_does_not_compensate_for_missing_advantage() -> None:
    native = card(ExperimentArm.NATIVE, category=4, locks=3)
    flattened = card(ExperimentArm.FLATTENED, category=4, locks=3)
    assert validate_paired_scorecards(native, flattened) == "NO_GOVERNED_DEVELOPMENT_ADVANTAGE_FOR_REPEAT"


def test_scorecard_identity_is_deterministic() -> None:
    assert card(ExperimentArm.NATIVE, category=4, locks=4).scorecard_identity == card(
        ExperimentArm.NATIVE, category=4, locks=4
    ).scorecard_identity


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("case_identity", "not-a-hash"),
        ("provider_configuration_sha256", "B" * 64),
        ("output_sha256", ""),
    ),
)
def test_scorecard_rejects_unhashable_immutable_identities(field: str, value: str) -> None:
    values = {
        "scorecard_version": "1.0.0",
        "case_identity": H,
        "case_id": "CASE-1",
        "arm": ExperimentArm.NATIVE,
        "provider_configuration_sha256": H,
        "repeat_index": 1,
        "output_sha256": H,
        "scores": scores(4, 4),
        "noncompensable_failures": (),
    }
    values[field] = value
    with pytest.raises(EvidenceGateError, match=field):
        Scorecard(**values)


@pytest.mark.parametrize(("field", "value"), (("scorecard_version", ""), ("case_id", "")))
def test_scorecard_rejects_missing_version_or_case(field: str, value: str) -> None:
    values = {
        "scorecard_version": "1.0.0",
        "case_identity": H,
        "case_id": "CASE-1",
        "arm": ExperimentArm.NATIVE,
        "provider_configuration_sha256": H,
        "repeat_index": 1,
        "output_sha256": H,
        "scores": scores(4, 4),
        "noncompensable_failures": (),
    }
    values[field] = value
    with pytest.raises(EvidenceGateError, match=field):
        Scorecard(**values)


def test_dimension_evidence_must_be_a_lowercase_sha256() -> None:
    with pytest.raises(EvidenceGateError, match="evidence_sha256s"):
        DimensionScore(
            "category_native_syntax",
            Applicability.APPLICABLE,
            4,
            "governed evidence",
            ("not-a-digest",),
        )


def test_governed_generic_control_makes_no_category_native_advantage_claim() -> None:
    excluded = ("category_native_syntax", "wrong_reading_resistance")
    native = Scorecard(
        "1.0.0",
        H,
        "GENERIC-CONTROL",
        ExperimentArm.NATIVE,
        H,
        1,
        H,
        scores(0, 0, not_applicable=excluded),
        (),
    )
    flattened = Scorecard(
        "1.0.0",
        H,
        "GENERIC-CONTROL",
        ExperimentArm.FLATTENED,
        H,
        1,
        H,
        scores(0, 0, not_applicable=excluded),
        (),
    )
    assert (
        validate_paired_scorecards(native, flattened)
        == "GOVERNED_NON_ACTIVATIVE_CONTROL_NO_ADVANTAGE_CLAIM"
    )


def test_mixed_comparison_applicability_fails_closed() -> None:
    native = card(ExperimentArm.NATIVE, category=4, locks=4)
    flattened = Scorecard(
        "1.0.0",
        H,
        "CASE-1",
        ExperimentArm.FLATTENED,
        H,
        1,
        H,
        scores(0, 0, not_applicable=("category_native_syntax", "wrong_reading_resistance")),
        (),
    )
    with pytest.raises(EvidenceGateError, match="identical applicability"):
        validate_paired_scorecards(native, flattened)


def test_flattened_control_noncompensable_failure_is_not_tolerated() -> None:
    native = card(ExperimentArm.NATIVE, category=4, locks=4)
    flattened = card(
        ExperimentArm.FLATTENED,
        category=2,
        locks=2,
        failures=("non_admitted_corpus_evidence_used",),
    )
    assert (
        validate_paired_scorecards(native, flattened)
        == "FLATTENED_CONTROL_NONCOMPENSABLE_FAILURE"
    )
