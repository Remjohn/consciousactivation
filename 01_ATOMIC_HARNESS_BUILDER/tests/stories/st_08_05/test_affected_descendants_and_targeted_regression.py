from __future__ import annotations

import hashlib

import pytest

from cmf_builder.evaluation.selective_repair import (
    ProtectedCasePolicyStatus,
    RerunRequirement,
    RerunRequirementKind,
    RerunRequirementStatus,
    SelectiveRepairError,
    canonical_json_bytes,
    compile_bounded_rerun_plan,
)
from tests.stories.st_08_04.test_layer_localization_and_graph import valid_graph
from tests.stories.st_08_05.test_accepted_diagnosis_and_repair_scope import (
    compile_candidate,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def requirements(graph, *, blocked_suite: str | None = None):
    direct_suite, descendant_suite = graph.targeted_regression_suite
    direct_status = (
        RerunRequirementStatus.BLOCKED
        if blocked_suite == direct_suite
        else RerunRequirementStatus.AVAILABLE
    )
    descendant_status = (
        RerunRequirementStatus.BLOCKED
        if blocked_suite == descendant_suite
        else RerunRequirementStatus.AVAILABLE
    )
    return (
        RerunRequirement(
            suite_id=direct_suite,
            target_identity=graph.responsible_phase_or_capability,
            kind=RerunRequirementKind.DIRECT_TEST,
            status=direct_status,
            blocked_reason=(
                "governed local fixture is unavailable"
                if direct_status is RerunRequirementStatus.BLOCKED
                else None
            ),
        ),
        RerunRequirement(
            suite_id=descendant_suite,
            target_identity=graph.invalidated_descendant_set[-1],
            kind=RerunRequirementKind.DESCENDANT_REGRESSION,
            status=descendant_status,
            blocked_reason=(
                "governed local fixture is unavailable"
                if descendant_status is RerunRequirementStatus.BLOCKED
                else None
            ),
        ),
    )


def compile_plan(
    *,
    graph=None,
    governed_requirements=None,
    protected_case_policy_status=ProtectedCasePolicyStatus.NOT_APPLICABLE,
    external_execution_requested: bool = False,
):
    governed_graph = graph or valid_graph()
    candidate = compile_candidate(graph=governed_graph)
    return compile_bounded_rerun_plan(
        candidate=candidate,
        graph=governed_graph,
        requirements=(
            governed_requirements
            if governed_requirements is not None
            else requirements(governed_graph)
        ),
        applicable_benchmark_refs=(digest("development-benchmark-v1"),),
        protected_case_policy_status=protected_case_policy_status,
        execution_order=governed_graph.targeted_regression_suite,
        stop_conditions=(
            "stop on the first required local regression failure",
            "stop while a required result remains blocked",
        ),
        result_receipt_requirements=(
            "suite identity and immutable result hash",
            "repair candidate and graph lineage",
        ),
        external_execution_requested=external_execution_requested,
    )


def test_affected_descendants_are_derived_exactly_from_the_st_08_04_graph() -> None:
    graph = valid_graph()
    plan = compile_plan(graph=graph)

    assert plan.repair_candidate_identity == compile_candidate(graph=graph).candidate_identity
    assert plan.graph_identity == graph.graph_identity
    assert plan.responsible_unit == graph.responsible_phase_or_capability
    assert plan.affected_descendants == graph.invalidated_descendant_set
    assert set(plan.affected_descendants).isdisjoint(
        graph.frozen_upstream_and_unaffected_state
    )

    included_children = {
        evidence.child_identity for evidence in plan.included_adjacency_evidence
    }
    assert included_children == set(graph.invalidated_descendant_set)
    assert {
        (
            evidence.parent_identity,
            evidence.child_identity,
            evidence.relation,
        )
        for evidence in plan.included_adjacency_evidence
    } == {
        (edge.parent_identity, edge.child_identity, edge.relation)
        for edge in graph.dependency_edges
        if edge.child_identity in graph.invalidated_descendant_set
    }


def test_unaffected_adjacent_and_independent_units_have_explicit_exclusion_evidence() -> None:
    graph = valid_graph()
    plan = compile_plan(graph=graph)

    excluded = {
        (evidence.parent_identity, evidence.child_identity): evidence.reason
        for evidence in plan.excluded_adjacency_evidence
    }
    independent_edges = {
        (edge.parent_identity, edge.child_identity)
        for edge in graph.dependency_edges
        if edge.child_identity not in graph.invalidated_descendant_set
    }

    assert set(excluded) == independent_edges
    assert all(reason.strip() for reason in excluded.values())
    assert not set(plan.affected_descendants).intersection(
        child for _, child in excluded
    )


def test_rerun_plan_covers_every_graph_required_suite_without_manual_guessing() -> None:
    graph = valid_graph()
    plan = compile_plan(graph=graph)

    assert tuple(item.suite_id for item in plan.requirements) == tuple(
        sorted(graph.targeted_regression_suite)
    )
    assert plan.execution_order == graph.targeted_regression_suite
    assert plan.applicable_benchmark_refs == (digest("development-benchmark-v1"),)
    assert plan.completion_status == "READY_FOR_LOCAL_RERUN"
    assert plan.blocked_requirements == ()
    assert plan.external_runtime_executed is False


def test_omitting_a_graph_required_regression_fails_closed() -> None:
    graph = valid_graph()

    with pytest.raises(SelectiveRepairError) as caught:
        compile_plan(
            graph=graph,
            governed_requirements=requirements(graph)[:1],
        )

    assert caught.value.code == "MISSING_REQUIRED_REGRESSION"


def test_blocked_required_results_remain_visible_and_prevent_completion() -> None:
    graph = valid_graph()
    blocked_suite = graph.targeted_regression_suite[-1]
    plan = compile_plan(
        graph=graph,
        governed_requirements=requirements(graph, blocked_suite=blocked_suite),
    )

    assert plan.completion_status == "BLOCKED_REQUIRED_RESULTS"
    assert tuple(item.suite_id for item in plan.blocked_requirements) == (
        blocked_suite,
    )
    assert plan.blocked_requirements[0].blocked_reason == (
        "governed local fixture is unavailable"
    )


def test_blocked_requirement_needs_a_typed_reason() -> None:
    graph = valid_graph()

    with pytest.raises(SelectiveRepairError) as caught:
        RerunRequirement(
            suite_id=graph.targeted_regression_suite[0],
            target_identity=graph.responsible_phase_or_capability,
            kind=RerunRequirementKind.DIRECT_TEST,
            status=RerunRequirementStatus.BLOCKED,
            blocked_reason=None,
        )

    assert caught.value.code == "MISSING_BLOCKED_REQUIREMENT_REASON"


def test_protected_cases_require_a_separately_authorized_policy() -> None:
    graph = valid_graph()
    protected = RerunRequirement(
        suite_id="tests/semantic/protected-case-regression",
        target_identity=graph.invalidated_descendant_set[-1],
        kind=RerunRequirementKind.PROTECTED_CASE,
        status=RerunRequirementStatus.AVAILABLE,
        protected_case_policy_ref=digest("protected-case-policy-v1"),
    )

    with pytest.raises(SelectiveRepairError) as caught:
        compile_plan(
            graph=graph,
            governed_requirements=requirements(graph) + (protected,),
            protected_case_policy_status=ProtectedCasePolicyStatus.NOT_AUTHORIZED,
        )
    assert caught.value.code == "PROTECTED_CASE_NOT_AUTHORIZED"

    authorized = compile_plan(
        graph=graph,
        governed_requirements=requirements(graph) + (protected,),
        protected_case_policy_status=ProtectedCasePolicyStatus.AUTHORIZED,
    )
    assert protected in authorized.requirements
    assert authorized.protected_case_policy_status is (
        ProtectedCasePolicyStatus.AUTHORIZED
    )


def test_protected_policy_does_not_fabricate_an_unavailable_protected_case() -> None:
    graph = valid_graph()
    protected = RerunRequirement(
        suite_id="tests/semantic/protected-case-regression",
        target_identity=graph.invalidated_descendant_set[-1],
        kind=RerunRequirementKind.PROTECTED_CASE,
        status=RerunRequirementStatus.BLOCKED,
        blocked_reason="protected evidence is unavailable in the offline branch",
        protected_case_policy_ref=digest("protected-case-policy-v1"),
    )
    plan = compile_plan(
        graph=graph,
        governed_requirements=requirements(graph) + (protected,),
        protected_case_policy_status=ProtectedCasePolicyStatus.AUTHORIZED,
    )

    assert plan.completion_status == "BLOCKED_REQUIRED_RESULTS"
    assert protected in plan.blocked_requirements
    assert plan.external_runtime_executed is False


def test_external_runtime_or_provider_execution_is_not_a_rerun_plan_operation() -> None:
    with pytest.raises(SelectiveRepairError) as caught:
        compile_plan(external_execution_requested=True)

    assert caught.value.code == "EXTERNAL_RUNTIME_PROHIBITED"


def test_selection_and_plan_identity_are_canonical_and_order_independent() -> None:
    graph = valid_graph()
    first_requirements = requirements(graph)
    first = compile_plan(graph=graph, governed_requirements=first_requirements)
    second = compile_plan(
        graph=graph,
        governed_requirements=tuple(reversed(first_requirements)),
    )

    assert first.plan_identity == second.plan_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    assert first.as_dict()["production_ready"] is False
    assert first.as_dict()["certified"] is False
