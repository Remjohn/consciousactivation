from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.independent_scoring import (
    BASE_DIMENSIONS,
    NON_COMPENSABLE_GATES,
    SUPPORTED_MUTATIONS,
    ControlledMutation,
    DevelopmentRubric,
    DimensionDistribution,
    DimensionScorecard,
    DimensionStatus,
    GateResult,
    GateStatus,
    IndependentScoringError,
    IndependentScoringReceipt,
    RepeatedRunSummary,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


_CHANGED_VARIABLE_BY_MUTATION = {
    "preserve_topic_change_grammar": "grammar",
    "preserve_grammar_change_topic": "topic",
    "remove_one_sequence_invariant": "sequence_invariants[1]",
    "swap_semantic_polarity": "semantic_polarity",
    "inject_irrelevant_style_evidence": "style_evidence",
}


def mutation(
    mutation_type: str = "preserve_topic_change_grammar",
    **changes: object,
) -> ControlledMutation:
    values: dict[str, object] = {
        "mutation_id": f"controlled-{mutation_type}-v1",
        "mutation_type": mutation_type,
        "base_case_sha256": digest("base-case-v1"),
        "mutated_input_sha256": digest(f"mutated-{mutation_type}-v1"),
        "changed_variables": (_CHANGED_VARIABLE_BY_MUTATION.get(mutation_type, "topic"),),
        "preserved_invariants": (
            "source_identity",
            "target_category",
            "profile_identity",
            "rubric_identity",
            "artifact_lineage",
        ),
        "expected_decision_sha256": digest(f"expected-decision-{mutation_type}-v1"),
        "source_lineage_sha256": digest("source-lineage-v1"),
    }
    values.update(changes)
    return ControlledMutation(**values)  # type: ignore[arg-type]


def scoring_receipt(controlled_mutation: ControlledMutation) -> IndependentScoringReceipt:
    rubric = DevelopmentRubric(
        rubric_id="OD-AM-001-ST-08.03-INDEPENDENT-DIMENSIONS-v1",
        rubric_version="1.0.0-development",
        scoring_policy_version="1.0.0-development",
        evaluator_contract_version="1.0.0-development",
        threshold_policy_reference="human-governed-threshold-policy-not-defined",
        scoring_policy_sha256=digest("development-scoring-policy-v1"),
        threshold_policy_reference_sha256=digest("human-threshold-policy-reference-v1"),
    )
    scorecards = tuple(
        DimensionScorecard(
            dimension=dimension,
            status=DimensionStatus.PASSING,
            score_basis_points=7_500,
            evidence_refs=(digest(f"dimension-evidence-{dimension}"),),
        )
        for dimension in BASE_DIMENSIONS
    )
    gates = tuple(
        GateResult(
            gate_id=gate_id,
            status=GateStatus.PASSING,
            evidence_refs=(digest(f"gate-evidence-{gate_id}"),),
        )
        for gate_id in NON_COMPENSABLE_GATES
    )
    stability = RepeatedRunSummary(
        repetition_identities=(digest("repeat-41"), digest("repeat-42"), digest("repeat-43")),
        distributions=tuple(
            DimensionDistribution(
                dimension=dimension,
                scores_basis_points=(7_500, 7_500, 7_500),
            )
            for dimension in BASE_DIMENSIONS
        ),
        dominant_failure_patterns=(),
    )
    return IndependentScoringReceipt(
        rubric=rubric,
        evaluated_artifact_sha256=digest("evaluated-artifact-v1"),
        builder_version="builder-development-v1",
        target_category="generic_not_applicable_category_branch",
        target_profile="repository-owned-controlled-mutation-fixture",
        source_ir_sha256=digest("source-ir-v1"),
        predecessor_maturity_receipt_sha256=digest("st-08.02-maturity-receipt-v1"),
        benchmark_portfolio_sha256=digest("development-case-portfolio-v1"),
        case_identity_sha256=digest("controlled-mutation-case-v1"),
        case_access_class="development",
        run_id="st-08.03-controlled-mutation-test-run",
        provenance_sha256=digest("controlled-mutation-provenance-v1"),
        command_identity=digest("authorized-scoring-command-v1"),
        authority_identity=digest("scoring-authority-v1"),
        scorecards=scorecards,
        mutations=(controlled_mutation,),
        gates=gates,
        stability_summary=stability,
        downstream_results=(),
        observations=("ST-08.03:controlled-mutation-evaluated",),
    )


@pytest.mark.parametrize("mutation_type", SUPPORTED_MUTATIONS)
def test_each_supported_mutation_preserves_one_variable_and_complete_lineage(
    mutation_type: str,
) -> None:
    controlled = mutation(mutation_type)
    payload = controlled.as_dict()

    assert controlled.base_case_sha256 != controlled.mutated_input_sha256
    assert controlled.changed_variables == (_CHANGED_VARIABLE_BY_MUTATION[mutation_type],)
    assert len(controlled.changed_variables) == 1
    assert controlled.preserved_invariants == (
        "source_identity",
        "target_category",
        "profile_identity",
        "rubric_identity",
        "artifact_lineage",
    )
    assert payload["expected_decision_sha256"] == digest(
        f"expected-decision-{mutation_type}-v1"
    )
    assert payload["source_lineage_sha256"] == digest("source-lineage-v1")
    assert payload["base_case_sha256"] != payload["mutated_input_sha256"]


def test_supported_mutation_registry_is_exactly_the_capsule_defined_set() -> None:
    assert SUPPORTED_MUTATIONS == (
        "preserve_topic_change_grammar",
        "preserve_grammar_change_topic",
        "remove_one_sequence_invariant",
        "swap_semantic_polarity",
        "inject_irrelevant_style_evidence",
    )


@pytest.mark.parametrize("changed_variables", [(), ("topic", "grammar"), ["topic"]])
def test_uncontrolled_or_non_immutable_changed_variable_collection_is_rejected(
    changed_variables: object,
) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        mutation(changed_variables=changed_variables)

    assert caught.value.code == "UNCONTROLLED_MUTATION"


def test_blank_changed_variable_is_rejected() -> None:
    with pytest.raises(IndependentScoringError) as caught:
        mutation(changed_variables=("  ",))

    assert caught.value.code == "MISSING_GOVERNED_FIELD"
    assert caught.value.context == {"field": "changed_variable"}


def test_unsupported_mutation_type_fails_closed() -> None:
    with pytest.raises(IndependentScoringError) as caught:
        mutation("change_everything_until_it_passes")

    assert caught.value.code == "UNSUPPORTED_MUTATION"


def test_equal_base_and_mutated_input_identity_is_not_an_actual_mutation() -> None:
    base_identity = digest("same-input")

    with pytest.raises(IndependentScoringError) as caught:
        mutation(
            base_case_sha256=base_identity,
            mutated_input_sha256=base_identity,
        )

    assert caught.value.code == "MISSING_ACTUAL_MUTATION"


@pytest.mark.parametrize(
    "field",
    [
        "base_case_sha256",
        "mutated_input_sha256",
        "expected_decision_sha256",
        "source_lineage_sha256",
    ],
)
def test_every_identity_and_lineage_reference_must_be_an_immutable_sha256(field: str) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        mutation(**{field: f"mutable-or-missing-{field}"})

    assert caught.value.code == "INVALID_IMMUTABLE_IDENTITY"
    assert caught.value.context == {"field": field}


@pytest.mark.parametrize("preserved_invariants", [(), [], ("source_identity", "")])
def test_preserved_invariants_are_required_immutable_and_non_blank(
    preserved_invariants: object,
) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        mutation(preserved_invariants=preserved_invariants)

    if preserved_invariants == ():
        assert caught.value.code == "MISSING_MUTATION_INVARIANTS"
    elif preserved_invariants == []:
        assert caught.value.code == "MISSING_MUTATION_INVARIANTS"
    else:
        assert caught.value.code == "MISSING_GOVERNED_FIELD"
        assert caught.value.context == {"field": "preserved_invariant"}


def test_identical_governed_mutations_have_deterministic_identity_and_bytes() -> None:
    first = mutation()
    second = mutation()

    assert first.mutation_identity == second.mutation_identity
    assert first.as_dict() == second.as_dict()


@pytest.mark.parametrize(
    ("field", "changed_value"),
    [
        ("mutation_id", "controlled-preserve-topic-change-grammar-v2"),
        ("mutation_type", "preserve_grammar_change_topic"),
        ("base_case_sha256", digest("base-case-v2")),
        ("mutated_input_sha256", digest("mutated-input-v2")),
        ("changed_variables", ("topic",)),
        ("preserved_invariants", ("source_identity", "rubric_identity")),
        ("expected_decision_sha256", digest("expected-decision-v2")),
        ("source_lineage_sha256", digest("source-lineage-v2")),
    ],
)
def test_each_governed_input_change_creates_a_new_mutation_identity(
    field: str,
    changed_value: object,
) -> None:
    original = mutation()
    changed = replace(original, **{field: changed_value})

    assert changed.mutation_identity != original.mutation_identity


@pytest.mark.parametrize(
    ("field", "mutated_value"),
    [
        ("mutated_input_sha256", digest("tampered-mutated-input")),
        ("changed_variables", ("topic", "grammar")),
        ("preserved_invariants", ("source_identity",)),
        ("expected_decision_sha256", digest("tampered-decision")),
        ("source_lineage_sha256", digest("tampered-source-lineage")),
    ],
)
def test_post_construction_mutation_of_nested_fields_is_detected(
    field: str,
    mutated_value: object,
) -> None:
    controlled = mutation()
    object.__setattr__(controlled, field, mutated_value)

    with pytest.raises(IndependentScoringError) as caught:
        controlled.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert caught.value.context == {"field": "controlled_mutation"}


def test_parent_receipt_detects_tampering_inside_nested_controlled_mutation() -> None:
    controlled = mutation()
    receipt = scoring_receipt(controlled)
    original_receipt_identity = receipt.receipt_identity
    object.__setattr__(controlled, "source_lineage_sha256", digest("forged-lineage"))

    with pytest.raises(IndependentScoringError) as caught:
        _ = receipt.receipt_identity

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"
    assert caught.value.context == {"field": "independent_scoring_receipt"}
    assert original_receipt_identity
