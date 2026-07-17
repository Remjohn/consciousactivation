import pytest

from cmf_builder.workflow.workflow_outcomes import (
    AntiMonolithViolation,
    DimensionOutcome,
    OutcomeDimension,
    OutcomeStatus,
    WorkflowOutcomeError,
    WorkflowOutcomeVector,
    WorkflowStructureDeclaration,
    analyze_anti_monolith_structure,
)


def dim(dimension, status=OutcomeStatus.PASS_, *, simulated=False, notes="evidence-backed"):
    return DimensionOutcome(
        dimension=dimension,
        status=status,
        evidence_refs=(f"evidence:{dimension.value}",) if status is not OutcomeStatus.NOT_APPLICABLE else (),
        authority_ref="authority:od-am-002",
        notes=notes,
        simulated=simulated,
    )


def all_dimensions(**overrides):
    items = []
    for dimension in OutcomeDimension:
        items.append(overrides.get(dimension, dim(dimension, simulated=dimension is OutcomeDimension.SIMULATED_RESOURCE_USAGE)))
    return tuple(items)


def vector(**overrides):
    values = {
        "workflow_identity": "workflow:category-native",
        "workflow_profile_identity": "profile:dev",
        "node_identities": ("node:human", "node:agent", "node:code", "node:external-boundary"),
        "dimensions": all_dimensions(),
        "aggregate_status": "dimensioned_development_observation",
        "provider_validation": "pending",
    }
    values.update(overrides)
    return WorkflowOutcomeVector(**values)


def test_workflow_outcome_keeps_all_dimensions_independent():
    outcome = vector()

    assert outcome.outcome_identity
    assert len(outcome.dimensions) == 15
    assert {item.dimension for item in outcome.dimensions} == set(OutcomeDimension)
    assert outcome.as_dict()["provider_validation"] == "pending"


def test_missing_or_duplicate_dimensions_fail_closed():
    with pytest.raises(WorkflowOutcomeError) as missing:
        vector(dimensions=tuple(item for item in all_dimensions() if item.dimension is not OutcomeDimension.AUTHORITY))
    assert missing.value.code == "INCOMPLETE_OUTCOME_DIMENSIONS"

    duplicate = all_dimensions() + (dim(OutcomeDimension.AUTHORITY),)
    with pytest.raises(WorkflowOutcomeError) as dup:
        vector(dimensions=duplicate)
    assert dup.value.code == "DUPLICATE_OUTCOME_DIMENSION"


def test_aggregate_pass_provider_validation_and_production_claims_are_rejected():
    with pytest.raises(WorkflowOutcomeError) as aggregate:
        vector(aggregate_status="PASS")
    assert aggregate.value.code == "AGGREGATE_STATUS_HIDES_OPEN_GATES"

    with pytest.raises(WorkflowOutcomeError) as provider:
        vector(provider_validation="validated")
    assert provider.value.code == "PROVIDER_VALIDATION_REQUIRES_PROVIDER_EVIDENCE"

    with pytest.raises(WorkflowOutcomeError) as production:
        vector(production_ready=True)
    assert production.value.code == "FALSE_PRODUCTION_OR_CERTIFICATION_CLAIM"


def test_simulated_resource_usage_must_be_labeled_simulated():
    with pytest.raises(WorkflowOutcomeError) as exc:
        dim(OutcomeDimension.SIMULATED_RESOURCE_USAGE, simulated=False)

    assert exc.value.code == "RESOURCE_USAGE_MUST_BE_SIMULATED"


def test_not_applicable_requires_explicit_basis():
    with pytest.raises(WorkflowOutcomeError) as exc:
        dim(OutcomeDimension.EXTERNAL_BOUNDARY, status=OutcomeStatus.NOT_APPLICABLE, notes="not used")

    assert exc.value.code == "NOT_APPLICABLE_BASIS_REQUIRED"


def test_anti_monolith_analysis_flags_hidden_and_unbounded_designs():
    declaration = WorkflowStructureDeclaration(
        workflow_identity="workflow:bad",
        actor_roles=("HUMAN+AGENT",),
        typed_intermediate_states=False,
        human_decisions_visible=False,
        external_nodes_visible=False,
        checkpoint_refs=(),
        failure_handlers_by_node=False,
        retry_policy="unbounded",
        context_policy="load_everything",
        node_contract_refs=(),
        trace_refs=(),
    )

    violations = analyze_anti_monolith_structure(declaration)

    assert AntiMonolithViolation.INCOMPATIBLE_ACTOR_ROLES in violations
    assert AntiMonolithViolation.HIDDEN_HUMAN_DECISIONS in violations
    assert AntiMonolithViolation.HIDDEN_EXTERNAL_EXECUTION in violations
    assert AntiMonolithViolation.ORCHESTRATION_BLOB_BYPASSES_NODE_CONTRACTS in violations
    assert AntiMonolithViolation.UNTRACEABLE_OUTCOMES in violations


def test_traceable_graph_structure_has_no_anti_monolith_violations():
    declaration = WorkflowStructureDeclaration(
        workflow_identity="workflow:good",
        actor_roles=("HUMAN_NODE", "GOVERNED_AGENT_NODE", "DETERMINISTIC_CODE_NODE", "EXTERNAL_BOUNDARY_NODE"),
        typed_intermediate_states=True,
        human_decisions_visible=True,
        external_nodes_visible=True,
        checkpoint_refs=("checkpoint:1",),
        failure_handlers_by_node=True,
        retry_policy="bounded",
        context_policy="minimum_complete_context",
        node_contract_refs=("contract:node:1",),
        trace_refs=("trace:1",),
    )

    assert analyze_anti_monolith_structure(declaration) == ()
