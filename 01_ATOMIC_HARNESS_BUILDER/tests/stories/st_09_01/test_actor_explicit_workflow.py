from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.workflow.actor_explicit_contracts import (
    ActorExplicitWorkflowIR,
    ActorKind,
    WorkflowAction,
    WorkflowAuthority,
    WorkflowCommand,
    WorkflowContractError,
    WorkflowEdge,
    WorkflowNode,
    compile_actor_explicit_workflow,
    compute_workflow_compile_payload_sha256,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def authority() -> WorkflowAuthority:
    return WorkflowAuthority(
        authority_id="od-am-001-st-09.01-workflow-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-09.01-authority-bytes"),
        permitted_actions=(WorkflowAction.COMPILE, WorkflowAction.INVALIDATE),
        applicable_scope=("ACTOR_EXPLICIT_LOCAL_COMPILATION",),
    )


def node(
    node_id: str,
    actor_kind: ActorKind,
    *,
    owner: str,
    input_contract: str,
    output_contract: str,
    dependencies: tuple[str, ...] = (),
    downstream: tuple[str, ...] = (),
    **overrides: object,
) -> WorkflowNode:
    values: dict[str, object] = {
        "node_id": node_id,
        "actor_kind": actor_kind,
        "owner": owner,
        "actor_rationale": f"explicit responsibility and authority boundary for {node_id}",
        "input_contract": input_contract,
        "output_contract": output_contract,
        "authority_requirement": f"authority:{node_id}",
        "dependency_node_ids": dependencies,
        "execution_preconditions": (f"precondition:{node_id}",),
        "completion_condition": f"completion:{node_id}",
        "rejection_behavior": f"reject-and-stop:{node_id}",
        "retry_eligible": actor_kind is not ActorKind.HUMAN_NODE,
        "checkpoint_behavior": "DECLARE_IMMUTABLE_CHECKPOINT_NO_EXECUTION",
        "cancellation_behavior": "CANCEL_BEFORE_ADVANCEMENT_AND_PRESERVE_HISTORY",
        "failure_owner": owner,
        "declared_downstream_nodes": downstream,
        "producer_output_validation_ref": f"validation:{node_id}",
        "human_decision_reissued": False,
        "external_execution_requested": False,
    }
    values.update(overrides)
    return WorkflowNode(**values)


def workflow_parts() -> tuple[tuple[WorkflowNode, ...], tuple[WorkflowEdge, ...]]:
    nodes = (
        node(
            "human-ratification",
            ActorKind.HUMAN_NODE,
            owner="governed-human-reviewer",
            input_contract="task-request/v1",
            output_contract="attributable-human-decision/v1",
            downstream=("agent-proposal",),
            retry_eligible=False,
        ),
        node(
            "agent-proposal",
            ActorKind.GOVERNED_AGENT_NODE,
            owner="bounded-builder-agent",
            input_contract="attributable-human-decision/v1",
            output_contract="governed-proposal/v1",
            dependencies=("human-ratification",),
            downstream=("deterministic-validation",),
        ),
        node(
            "deterministic-validation",
            ActorKind.DETERMINISTIC_CODE_NODE,
            owner="builder-owned-validator",
            input_contract="governed-proposal/v1",
            output_contract="validated-builder-result/v1",
            dependencies=("agent-proposal",),
            downstream=("external-boundary",),
        ),
        node(
            "external-boundary",
            ActorKind.EXTERNAL_BOUNDARY_NODE,
            owner="external-product-owner",
            input_contract="validated-builder-result/v1",
            output_contract="external-result-reference/v1",
            dependencies=("deterministic-validation",),
        ),
    )
    edges = (
        WorkflowEdge(
            source_node_id="human-ratification",
            target_node_id="agent-proposal",
            payload_contract="attributable-human-decision/v1",
            condition="human decision is attributable and authority-valid",
        ),
        WorkflowEdge(
            source_node_id="agent-proposal",
            target_node_id="deterministic-validation",
            payload_contract="governed-proposal/v1",
            condition="proposal is complete and within bounded authority",
        ),
        WorkflowEdge(
            source_node_id="deterministic-validation",
            target_node_id="external-boundary",
            payload_contract="validated-builder-result/v1",
            condition="producer output validation receipt is PASS",
        ),
    )
    return nodes, edges


def compile_workflow(
    *,
    nodes: tuple[WorkflowNode, ...] | None = None,
    edges: tuple[WorkflowEdge, ...] | None = None,
) -> ActorExplicitWorkflowIR:
    default_nodes, default_edges = workflow_parts()
    selected_nodes = default_nodes if nodes is None else nodes
    selected_edges = default_edges if edges is None else edges
    workflow_id = "synthetic-actor-explicit-workflow"
    workflow_version = "1.0.0-development"
    profile_ref = digest("synthetic-actor-explicit-profile")
    entry_node_ids = tuple(
        item.node_id for item in selected_nodes if not item.dependency_node_ids
    )
    terminal_node_ids = tuple(
        item.node_id for item in selected_nodes if not item.declared_downstream_nodes
    )
    source_graph_hashes = (
        digest("approved-phase-graph"),
        digest("minimum-complete-context"),
    )
    governed_authority = authority()
    payload_sha256 = compute_workflow_compile_payload_sha256(
        workflow_id=workflow_id,
        workflow_version=workflow_version,
        profile_ref=profile_ref,
        nodes=selected_nodes,
        edges=selected_edges,
        entry_node_ids=entry_node_ids,
        terminal_node_ids=terminal_node_ids,
        source_graph_hashes=source_graph_hashes,
        promotion_status="development_only",
    )
    command = WorkflowCommand(
        command_id="compile-synthetic-actor-explicit-workflow",
        action=WorkflowAction.COMPILE,
        resource_id=digest(f"{workflow_id}:{workflow_version}:{profile_ref}"),
        payload_sha256=payload_sha256,
        expected_authority_identity=governed_authority.authority_identity,
    )
    return compile_actor_explicit_workflow(
        workflow_id=workflow_id,
        workflow_version=workflow_version,
        profile_ref=profile_ref,
        nodes=selected_nodes,
        edges=selected_edges,
        entry_node_ids=entry_node_ids,
        terminal_node_ids=terminal_node_ids,
        source_graph_hashes=source_graph_hashes,
        promotion_status="development_only",
        command=command,
        authority=governed_authority,
    )


def test_workflow_compilation_preserves_all_four_explicit_actor_kinds() -> None:
    workflow = compile_workflow()

    by_id = {item.node_id: item for item in workflow.nodes}
    assert by_id["human-ratification"].actor_kind is ActorKind.HUMAN_NODE
    assert by_id["agent-proposal"].actor_kind is ActorKind.GOVERNED_AGENT_NODE
    assert by_id["deterministic-validation"].actor_kind is ActorKind.DETERMINISTIC_CODE_NODE
    assert by_id["external-boundary"].actor_kind is ActorKind.EXTERNAL_BOUNDARY_NODE
    assert len({item.owner for item in workflow.nodes}) == 4
    assert workflow.external_engine is False
    assert workflow.temporal_conformance == "EXTERNAL_VALIDATION_PENDING"
    assert workflow.production_ready is False
    assert workflow.certified is False


def test_every_node_exposes_owned_contracts_conditions_stops_and_resume_policy() -> None:
    workflow = compile_workflow()

    for item in workflow.nodes:
        assert item.owner
        assert item.actor_rationale
        assert item.input_contract
        assert item.output_contract
        assert item.authority_requirement
        assert item.execution_preconditions
        assert item.completion_condition
        assert item.rejection_behavior.startswith("reject-and-stop:")
        assert item.checkpoint_behavior == "DECLARE_IMMUTABLE_CHECKPOINT_NO_EXECUTION"
        assert item.cancellation_behavior == "CANCEL_BEFORE_ADVANCEMENT_AND_PRESERVE_HISTORY"
        assert item.failure_owner == item.owner
        assert item.producer_output_validation_ref

    human = next(item for item in workflow.nodes if item.actor_kind is ActorKind.HUMAN_NODE)
    assert human.owner == "governed-human-reviewer"
    assert human.retry_eligible is False
    assert human.human_decision_reissued is False


def test_edges_are_traceable_declared_and_contract_typed() -> None:
    workflow = compile_workflow()
    nodes = {item.node_id: item for item in workflow.nodes}

    for edge in workflow.edges:
        source = nodes[edge.source_node_id]
        target = nodes[edge.target_node_id]
        assert edge.target_node_id in source.declared_downstream_nodes
        assert edge.source_node_id in target.dependency_node_ids
        assert edge.payload_contract == source.output_contract == target.input_contract
        assert edge.condition
        assert edge.validated_output_required is True


def test_identical_graphs_are_byte_stable_regardless_of_input_order() -> None:
    nodes, edges = workflow_parts()
    first = compile_workflow(nodes=nodes, edges=edges)
    reordered = compile_workflow(nodes=tuple(reversed(nodes)), edges=tuple(reversed(edges)))

    assert first.workflow_identity == reordered.workflow_identity
    assert first.as_dict() == reordered.as_dict()


@pytest.mark.parametrize("owner", ("", "human|agent", "human,agent", "human;agent"))
def test_anonymous_or_mixed_primary_ownership_fails_closed(owner: str) -> None:
    nodes, edges = workflow_parts()

    with pytest.raises(WorkflowContractError) as exc_info:
        replace(nodes[0], owner=owner)

    assert exc_info.value.code in {"MISSING_ACTOR_OWNER", "AMBIGUOUS_ACTOR_OWNERSHIP"}


def test_monolithic_or_duplicate_node_workflow_is_rejected() -> None:
    nodes, _ = workflow_parts()

    with pytest.raises(WorkflowContractError) as exc_info:
        compile_workflow(nodes=(nodes[0],), edges=())
    assert exc_info.value.code == "MONOLITHIC_WORKFLOW_PROHIBITED"

    with pytest.raises(WorkflowContractError) as exc_info:
        compile_workflow(nodes=(nodes[0], nodes[0]), edges=())
    assert exc_info.value.code == "DUPLICATE_WORKFLOW_NODE"


def test_hidden_external_execution_is_rejected_at_the_contract_boundary() -> None:
    nodes, edges = workflow_parts()

    with pytest.raises(WorkflowContractError) as exc_info:
        hidden_execution = replace(nodes[-1], external_execution_requested=True)
        compile_workflow(nodes=(*nodes[:-1], hidden_execution), edges=edges)
    assert exc_info.value.code == "EXTERNAL_EXECUTION_PROHIBITED"


def test_historical_human_decision_cannot_be_replayed_as_new_authority() -> None:
    nodes, edges = workflow_parts()

    with pytest.raises(WorkflowContractError) as exc_info:
        replayed_decision = replace(nodes[0], human_decision_reissued=True)
        compile_workflow(nodes=(replayed_decision, *nodes[1:]), edges=edges)
    assert exc_info.value.code == "HUMAN_DECISION_REPLAY_PROHIBITED"


def test_invalid_or_unvalidated_node_output_cannot_advance() -> None:
    nodes, edges = workflow_parts()
    unvalidated = replace(edges[1], validated_output_required=False)

    with pytest.raises(WorkflowContractError) as exc_info:
        compile_workflow(nodes=nodes, edges=(edges[0], unvalidated, edges[2]))
    assert exc_info.value.code == "UNVALIDATED_OUTPUT_ADVANCEMENT"


def test_undeclared_or_incompatible_handoff_fails_closed() -> None:
    nodes, edges = workflow_parts()
    undeclared = replace(edges[1], target_node_id="external-boundary")
    with pytest.raises(WorkflowContractError) as exc_info:
        compile_workflow(nodes=nodes, edges=(edges[0], undeclared, edges[2]))
    assert exc_info.value.code == "UNDECLARED_HANDOFF"

    incompatible = replace(edges[1], payload_contract="unrelated-contract/v1")
    with pytest.raises(WorkflowContractError) as exc_info:
        compile_workflow(nodes=nodes, edges=(edges[0], incompatible, edges[2]))
    assert exc_info.value.code == "INCOMPATIBLE_HANDOFF_CONTRACT"


def test_cyclic_workflow_is_rejected() -> None:
    first = node(
        "first",
        ActorKind.DETERMINISTIC_CODE_NODE,
        owner="first-owner",
        input_contract="cycle/v1",
        output_contract="cycle/v1",
        dependencies=("second",),
        downstream=("second",),
    )
    second = node(
        "second",
        ActorKind.GOVERNED_AGENT_NODE,
        owner="second-owner",
        input_contract="cycle/v1",
        output_contract="cycle/v1",
        dependencies=("first",),
        downstream=("first",),
    )
    edges = (
        WorkflowEdge("first", "second", "cycle/v1", "first-to-second"),
        WorkflowEdge("second", "first", "cycle/v1", "second-to-first"),
    )

    with pytest.raises(WorkflowContractError) as exc_info:
        compile_workflow(nodes=(first, second), edges=edges)
    assert exc_info.value.code == "CYCLIC_WORKFLOW"
