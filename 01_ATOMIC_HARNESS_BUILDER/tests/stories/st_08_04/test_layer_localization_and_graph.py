from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.root_cause_diagnosis import (
    DiagnosticLayer,
    DiagnosisStatus,
    DependencyEdge,
    FailureClassification,
    HypothesisTestResult,
    HypothesisTestStatus,
    PrimaryFailureClass,
    RepairAndInvalidationGraph,
    RepairField,
    RootCauseDiagnosis,
    RootCauseDiagnosisError,
    canonical_json_bytes,
    compile_repair_and_invalidation_graph,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def localized_diagnosis(
    layer: DiagnosticLayer = DiagnosticLayer.SEMANTIC,
    **changes: object,
) -> RootCauseDiagnosis:
    supported = HypothesisTestResult(
        hypothesis_id=f"hypothesis-{layer.value}-cause",
        hypothesis=f"the defect originates in the {layer.value} layer",
        test_description=f"isolate the {layer.value} layer with governed inputs",
        status=HypothesisTestStatus.SUPPORTED,
        evidence_refs=(digest(f"{layer.value}:supported-evidence"),),
        result_summary=f"only the {layer.value} layer reproduces the defect",
        rejection_reason=None,
    )
    rejected = HypothesisTestResult(
        hypothesis_id=f"hypothesis-{layer.value}-alternate",
        hypothesis=f"an adjacent layer caused the {layer.value} symptom",
        test_description="hold the selected layer fixed and test the adjacent-layer hypothesis",
        status=HypothesisTestStatus.REJECTED,
        evidence_refs=(digest(f"{layer.value}:rejected-evidence"),),
        result_summary="the adjacent layer preserves the governed invariant",
        rejection_reason="immutable comparison bytes contradict the alternate hypothesis",
    )
    values: dict[str, object] = {
        "diagnosis_id": f"root-cause-{layer.value}-v1",
        "diagnosis_version": "1.0.0-development",
        "classification": FailureClassification(
            failure_id=f"failure-{layer.value}-v1",
            stable_code=f"{layer.value.upper()}_GOVERNED_FAILURE",
            primary_class=PrimaryFailureClass.CONTRACT,
            localization_layer=layer,
            contributing_factors=(f"governed {layer.value} invariant failed",),
        ),
        "observed_symptom": f"the output violates a {layer.value} invariant",
        "reproduction_or_evidence_refs": (
            digest(f"{layer.value}:failed-artifact"),
            digest(f"{layer.value}:reproduction"),
        ),
        "affected_boundary": f"{layer.value} responsibility boundary",
        "competing_hypotheses": (supported.hypothesis_id, rejected.hypothesis_id),
        "hypothesis_tests_and_results": (supported, rejected),
        "status": DiagnosisStatus.LOCALIZED,
        "selected_root_cause": supported.hypothesis,
        "confidence_basis": (
            "controlled reproduction isolates one layer",
            "the competing hypothesis is contradicted by immutable evidence",
        ),
        "smallest_supported_responsible_layer": layer,
        "responsible_owner": f"Builder {layer.value} owner",
        "responsible_authority_ref": digest(f"{layer.value}:authority"),
        "unaffected_frozen_state": (
            digest(f"{layer.value}:source-lock"),
            digest(f"{layer.value}:upstream-truth"),
            digest(f"{layer.value}:unaffected-sibling"),
        ),
        "exact_lineage": (
            digest(f"{layer.value}:st-08.03-receipt"),
            digest(f"{layer.value}:failed-artifact"),
            digest(f"{layer.value}:reproduction"),
        ),
        "escalation_route": None,
    }
    values.update(changes)
    return RootCauseDiagnosis(**values)  # type: ignore[arg-type]


def unresolved_diagnosis() -> RootCauseDiagnosis:
    semantic = HypothesisTestResult(
        hypothesis_id="hypothesis-semantic",
        hypothesis="semantic projection lost lineage",
        test_description="isolate the semantic projection",
        status=HypothesisTestStatus.INCONCLUSIVE,
        evidence_refs=(digest("semantic-inconclusive"),),
        result_summary="semantic and context causes remain observationally equivalent",
        rejection_reason=None,
    )
    context = HypothesisTestResult(
        hypothesis_id="hypothesis-context",
        hypothesis="minimum context omitted lineage",
        test_description="isolate the minimum-context package",
        status=HypothesisTestStatus.INCONCLUSIVE,
        evidence_refs=(digest("context-inconclusive"),),
        result_summary="semantic and context causes remain observationally equivalent",
        rejection_reason=None,
    )
    return RootCauseDiagnosis(
        diagnosis_id="root-cause-unresolved-v1",
        diagnosis_version="1.0.0-development",
        classification=FailureClassification(
            failure_id="failure-unresolved-v1",
            stable_code="UNKNOWN_REQUIRES_TRIAGE",
            primary_class=None,
            localization_layer=None,
            contributing_factors=("evidence does not isolate one layer",),
        ),
        observed_symptom="lineage is incomplete",
        reproduction_or_evidence_refs=(digest("unresolved-reproduction"),),
        affected_boundary="semantic or context boundary",
        competing_hypotheses=(semantic.hypothesis_id, context.hypothesis_id),
        hypothesis_tests_and_results=(semantic, context),
        status=DiagnosisStatus.UNKNOWN_REQUIRES_TRIAGE,
        selected_root_cause=None,
        confidence_basis=("current evidence leaves two competing causes",),
        smallest_supported_responsible_layer=None,
        responsible_owner=None,
        responsible_authority_ref=None,
        unaffected_frozen_state=(digest("unresolved-source-lock"),),
        exact_lineage=(digest("unresolved-st-08.03-receipt"),),
        escalation_route="BLOCKED_PENDING_TYPED_TRIAGE",
    )


def graph_inputs(
    diagnosis: RootCauseDiagnosis | None = None,
    **changes: object,
) -> dict[str, object]:
    governed_diagnosis = diagnosis or localized_diagnosis()
    layer = governed_diagnosis.smallest_supported_responsible_layer or DiagnosticLayer.SEMANTIC
    responsible_unit = f"builder.{layer.value}.responsible-unit"
    direct_projection = digest(f"{layer.value}:direct-projection")
    direct_validation = digest(f"{layer.value}:direct-validation")
    packaged_descendant = digest(f"{layer.value}:packaged-descendant")
    unrelated_root = digest(f"{layer.value}:unrelated-root")
    unrelated_child = digest(f"{layer.value}:unrelated-child")
    values: dict[str, object] = {
        "diagnosis": governed_diagnosis,
        "responsible_phase_or_capability": responsible_unit,
        "permitted_repair_fields": (
            RepairField(
                layer=layer,
                field_name=f"{layer.value}_governed_projection",
            ),
        ),
        "frozen_upstream_and_unaffected_state": governed_diagnosis.unaffected_frozen_state,
        "dependency_edges": (
            DependencyEdge(
                parent_identity=responsible_unit,
                child_identity=direct_projection,
                relation="directly_compiled_projection",
            ),
            DependencyEdge(
                parent_identity=responsible_unit,
                child_identity=direct_validation,
                relation="direct_validation_receipt",
            ),
            DependencyEdge(
                parent_identity=direct_projection,
                child_identity=packaged_descendant,
                relation="packaged_from_projection",
            ),
            DependencyEdge(
                parent_identity=unrelated_root,
                child_identity=unrelated_child,
                relation="independent_branch",
            ),
        ),
        "invalidated_descendant_set": tuple(
            sorted((direct_projection, direct_validation, packaged_descendant))
        ),
        "targeted_regression_suite": (
            f"tests/{layer.value}/direct_projection_contract",
            f"tests/{layer.value}/descendant_package_regression",
        ),
        "escalation_conditions": (
            "responsible layer becomes ambiguous",
            "repair would alter ratified constitutional meaning",
        ),
        "required_repair_authority": digest(f"{layer.value}:repair-authority"),
        "rollback_requirements": (
            "preserve the prior immutable active artifact",
            "commit no partial repair or invalidation state",
        ),
    }
    values.update(changes)
    return values


def valid_graph(
    diagnosis: RootCauseDiagnosis | None = None,
    **changes: object,
) -> RepairAndInvalidationGraph:
    return compile_repair_and_invalidation_graph(**graph_inputs(diagnosis, **changes))  # type: ignore[arg-type]


def test_diagnostic_layer_vocabulary_is_exact_and_complete() -> None:
    assert tuple(item.value for item in DiagnosticLayer) == (
        "source_and_evidence",
        "authority",
        "semantic",
        "category",
        "skill",
        "context",
        "workflow",
        "external_boundary",
    )


@pytest.mark.parametrize("layer", tuple(DiagnosticLayer))
def test_each_diagnostic_layer_can_localize_one_smallest_supported_repair_scope(
    layer: DiagnosticLayer,
) -> None:
    diagnosis = localized_diagnosis(layer)
    graph = valid_graph(diagnosis)

    assert diagnosis.smallest_supported_responsible_layer is layer
    assert diagnosis.classification.localization_layer is layer
    assert graph.responsible_layer is layer
    assert graph.root_cause_diagnosis_ref == diagnosis.diagnosis_identity
    assert {field.layer for field in graph.permitted_repair_fields} == {layer}
    assert graph.responsible_phase_or_capability == f"builder.{layer.value}.responsible-unit"


def test_graph_requires_explicit_competing_hypothesis_resolution_not_symptom_routing() -> None:
    diagnosis = localized_diagnosis()
    graph = valid_graph(diagnosis)

    assert len(diagnosis.competing_hypotheses) == 2
    assert {item.status for item in diagnosis.hypothesis_tests_and_results} == {
        HypothesisTestStatus.SUPPORTED,
        HypothesisTestStatus.REJECTED,
    }
    assert graph.root_cause_diagnosis_ref == diagnosis.diagnosis_identity
    assert diagnosis.selected_root_cause != diagnosis.observed_symptom

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_graph(unresolved_diagnosis())
    assert caught.value.code == "UNRESOLVED_DIAGNOSIS_CANNOT_AUTHORIZE_GRAPH"


def test_repair_fields_are_typed_and_limited_to_the_responsible_layer() -> None:
    diagnosis = localized_diagnosis(DiagnosticLayer.SEMANTIC)
    graph = valid_graph(diagnosis)

    assert graph.permitted_repair_fields == (
        RepairField(
            layer=DiagnosticLayer.SEMANTIC,
            field_name="semantic_governed_projection",
        ),
    )

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_graph(
            diagnosis,
            permitted_repair_fields=(
                RepairField(
                    layer=DiagnosticLayer.CONTEXT,
                    field_name="minimum_complete_context",
                ),
            ),
        )
    assert caught.value.code == "CROSS_LAYER_REPAIR_FIELD"


def test_graph_invalidates_exactly_the_demonstrated_transitive_descendants() -> None:
    graph = valid_graph()
    inputs = graph_inputs()
    responsible = str(inputs["responsible_phase_or_capability"])
    edges = inputs["dependency_edges"]
    assert isinstance(edges, tuple)

    directly_dependent = {
        edge.child_identity
        for edge in edges
        if isinstance(edge, DependencyEdge) and edge.parent_identity == responsible
    }
    transitively_dependent = {
        edge.child_identity
        for edge in edges
        if isinstance(edge, DependencyEdge) and edge.parent_identity in directly_dependent
    }
    expected = tuple(sorted(directly_dependent | transitively_dependent))

    assert graph.invalidated_descendant_set == expected
    assert digest("semantic:unrelated-child") not in graph.invalidated_descendant_set


@pytest.mark.parametrize(
    "invalidated",
    (
        (digest("semantic:direct-projection"),),
        (
            digest("semantic:direct-projection"),
            digest("semantic:direct-validation"),
            digest("semantic:packaged-descendant"),
            digest("semantic:unrelated-child"),
        ),
    ),
)
def test_underbroad_or_overbroad_invalidation_is_rejected(invalidated: tuple[str, ...]) -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_graph(invalidated_descendant_set=invalidated)

    assert caught.value.code == "INVALIDATION_SCOPE_MISMATCH"


def test_frozen_upstream_and_unaffected_state_cannot_be_invalidated_or_rewritten() -> None:
    diagnosis = localized_diagnosis()
    original_diagnosis_bytes = canonical_json_bytes(diagnosis.as_dict())
    graph = valid_graph(diagnosis)

    assert graph.frozen_upstream_and_unaffected_state == diagnosis.unaffected_frozen_state
    assert not set(graph.frozen_upstream_and_unaffected_state).intersection(
        graph.invalidated_descendant_set
    )
    assert canonical_json_bytes(diagnosis.as_dict()) == original_diagnosis_bytes

    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_graph(
            diagnosis,
            invalidated_descendant_set=tuple(
                sorted((*graph.invalidated_descendant_set, diagnosis.unaffected_frozen_state[0]))
            ),
        )
    assert caught.value.code in {
        "FROZEN_STATE_INVALIDATED",
        "INVALIDATION_SCOPE_MISMATCH",
    }


def test_graph_declares_regression_escalation_authority_and_rollback_without_execution() -> None:
    graph = valid_graph()
    payload = graph.as_dict()

    assert graph.targeted_regression_suite == (
        "tests/semantic/descendant_package_regression",
        "tests/semantic/direct_projection_contract",
    )
    assert graph.escalation_conditions
    assert graph.required_repair_authority == digest("semantic:repair-authority")
    assert graph.rollback_requirements == (
        "commit no partial repair or invalidation state",
        "preserve the prior immutable active artifact",
    )
    assert payload["repair_executed"] is False
    assert payload["artifact_mutated"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False


@pytest.mark.parametrize(
    ("overrides", "expected_code"),
    (
        ({"targeted_regression_suite": ()}, "MISSING_TARGETED_REGRESSION_SUITE"),
        ({"escalation_conditions": ()}, "MISSING_ESCALATION_CONDITIONS"),
        ({"required_repair_authority": ""}, "MISSING_REPAIR_AUTHORITY"),
        ({"rollback_requirements": ()}, "MISSING_ROLLBACK_REQUIREMENTS"),
    ),
)
def test_required_graph_control_declarations_fail_closed(
    overrides: dict[str, object],
    expected_code: str,
) -> None:
    with pytest.raises(RootCauseDiagnosisError) as caught:
        valid_graph(**overrides)
    assert caught.value.code == expected_code


def test_graph_identity_and_serialization_are_deterministic_and_canonically_ordered() -> None:
    first = valid_graph()
    second_inputs = graph_inputs()
    second_inputs["dependency_edges"] = tuple(reversed(second_inputs["dependency_edges"]))  # type: ignore[arg-type]
    second_inputs["invalidated_descendant_set"] = tuple(
        reversed(second_inputs["invalidated_descendant_set"])  # type: ignore[arg-type]
    )
    second_inputs["targeted_regression_suite"] = tuple(
        reversed(second_inputs["targeted_regression_suite"])  # type: ignore[arg-type]
    )
    second = compile_repair_and_invalidation_graph(**second_inputs)  # type: ignore[arg-type]

    assert first.graph_identity == second.graph_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())


def test_changed_governed_dependency_graph_produces_a_new_immutable_graph_identity() -> None:
    original = valid_graph()
    inputs = graph_inputs()
    edges = inputs["dependency_edges"]
    assert isinstance(edges, tuple)
    changed_child = digest("semantic:new-demonstrated-descendant")
    inputs["dependency_edges"] = (
        *edges,
        DependencyEdge(
            parent_identity="builder.semantic.responsible-unit",
            child_identity=changed_child,
            relation="new_governed_dependency",
        ),
    )
    inputs["invalidated_descendant_set"] = tuple(
        sorted((*inputs["invalidated_descendant_set"], changed_child))  # type: ignore[arg-type]
    )

    changed = compile_repair_and_invalidation_graph(**inputs)  # type: ignore[arg-type]

    assert changed.graph_identity != original.graph_identity
    assert original.invalidated_descendant_set == tuple(
        sorted(
            (
                digest("semantic:direct-projection"),
                digest("semantic:direct-validation"),
                digest("semantic:packaged-descendant"),
            )
        )
    )


@pytest.mark.parametrize(
    "claim",
    ("repair_executed", "artifact_mutated", "production_ready", "certified"),
)
def test_graph_declaration_cannot_execute_repair_or_claim_production_state(claim: str) -> None:
    graph = valid_graph()

    with pytest.raises(RootCauseDiagnosisError) as caught:
        replace(graph, **{claim: True})

    assert caught.value.code in {
        "PROHIBITED_REPAIR_EXECUTION",
        "PROHIBITED_ARTIFACT_MUTATION",
        "PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM",
    }
