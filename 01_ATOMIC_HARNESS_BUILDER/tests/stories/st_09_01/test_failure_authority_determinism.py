from __future__ import annotations

from dataclasses import replace
import hashlib
import os
from pathlib import Path
import subprocess
import sys

import pytest

from cmf_builder.workflow.actor_explicit_contracts import (
    ActorExplicitWorkflowIR,
    ActorKind,
    AuthorityStatus,
    WorkflowAction,
    WorkflowAuthority,
    WorkflowCommand,
    WorkflowContractError,
    WorkflowEdge,
    WorkflowNode,
    canonical_json_bytes,
    compile_actor_explicit_workflow,
    compute_workflow_compile_payload_sha256,
    compute_workflow_invalidation_payload_sha256,
    invalidate_workflow_ir,
    validate_repeat_workflow_ir,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def authority(*actions: WorkflowAction, status: AuthorityStatus = AuthorityStatus.ACTIVE) -> WorkflowAuthority:
    return WorkflowAuthority(
        authority_id="od-am-001-st-09.01-development-authority",
        authority_version="1.0.0-development",
        authority_sha256=digest("st-09.01-authority-bytes"),
        permitted_actions=actions or (WorkflowAction.COMPILE,),
        applicable_scope=("OD_AM_001_OFFLINE_DEVELOPMENT",),
        status=status,
    )


def node(
    node_id: str,
    actor_kind: ActorKind,
    *,
    owner: str | tuple[str, ...] | None = None,
    dependency_node_ids: tuple[str, ...] = (),
    declared_downstream_nodes: tuple[str, ...] = (),
    input_contract: str | None = None,
    output_contract: str | None = None,
    producer_output_validation_ref: str | None = None,
    human_decision_reissued: bool = False,
    external_execution_requested: bool = False,
) -> WorkflowNode:
    resolved_owner: str | tuple[str, ...]
    if owner is None and isinstance(actor_kind, ActorKind):
        resolved_owner = {
            ActorKind.HUMAN_NODE: "governed-human-reviewer",
            ActorKind.GOVERNED_AGENT_NODE: "bounded-builder-agent",
            ActorKind.DETERMINISTIC_CODE_NODE: "cmf-builder-code",
            ActorKind.EXTERNAL_BOUNDARY_NODE: "external-product-owner",
        }[actor_kind]
    else:
        resolved_owner = owner if owner is not None else "ambiguous-mixed-actor-owner"
    actor_label = actor_kind.value if isinstance(actor_kind, ActorKind) else str(actor_kind)
    return WorkflowNode(
        node_id=node_id,
        actor_kind=actor_kind,
        owner=resolved_owner,
        actor_rationale=f"{actor_label} owns only the declared {node_id} responsibility",
        input_contract=input_contract or f"contract:{node_id}:input:v1",
        output_contract=output_contract or f"contract:{node_id}:output:v1",
        authority_requirement=f"authority:{node_id}:v1",
        dependency_node_ids=dependency_node_ids,
        execution_preconditions=(f"{node_id}:governed-inputs-valid",),
        completion_condition=f"{node_id}:typed-output-valid",
        rejection_behavior=f"{node_id}:reject-without-downstream-advance",
        retry_eligible=False,
        checkpoint_behavior="declare_checkpoint_only_no_runtime_execution",
        cancellation_behavior="typed_cancellation_before_advancement",
        failure_owner=str(resolved_owner),
        declared_downstream_nodes=declared_downstream_nodes,
        producer_output_validation_ref=(
            producer_output_validation_ref
            or f"validator:{node_id}:typed-output:v1"
        ),
        human_decision_reissued=human_decision_reissued,
        external_execution_requested=external_execution_requested,
    )


def workflow_nodes() -> tuple[WorkflowNode, ...]:
    return (
        node(
            "validate-input",
            ActorKind.DETERMINISTIC_CODE_NODE,
            declared_downstream_nodes=("bounded-proposal",),
            output_contract="handoff:validated-input:v1",
        ),
        node(
            "bounded-proposal",
            ActorKind.GOVERNED_AGENT_NODE,
            dependency_node_ids=("validate-input",),
            declared_downstream_nodes=("human-decision",),
            input_contract="handoff:validated-input:v1",
            output_contract="handoff:bounded-proposal:v1",
        ),
        node(
            "human-decision",
            ActorKind.HUMAN_NODE,
            dependency_node_ids=("bounded-proposal",),
            declared_downstream_nodes=("external-handoff",),
            input_contract="handoff:bounded-proposal:v1",
            output_contract="handoff:human-decision:v1",
        ),
        node(
            "external-handoff",
            ActorKind.EXTERNAL_BOUNDARY_NODE,
            dependency_node_ids=("human-decision",),
            declared_downstream_nodes=(),
            input_contract="handoff:human-decision:v1",
        ),
    )


def workflow_edges() -> tuple[WorkflowEdge, ...]:
    return (
        WorkflowEdge(
            source_node_id="validate-input",
            target_node_id="bounded-proposal",
            payload_contract="handoff:validated-input:v1",
            condition="validated_input_available",
            validated_output_required=True,
        ),
        WorkflowEdge(
            source_node_id="bounded-proposal",
            target_node_id="human-decision",
            payload_contract="handoff:bounded-proposal:v1",
            condition="proposal_schema_and_semantics_valid",
            validated_output_required=True,
        ),
        WorkflowEdge(
            source_node_id="human-decision",
            target_node_id="external-handoff",
            payload_contract="handoff:human-decision:v1",
            condition="attributable_human_decision_valid",
            validated_output_required=True,
        ),
    )


def compile_inputs(
    *,
    nodes: tuple[WorkflowNode, ...] | None = None,
    edges: tuple[WorkflowEdge, ...] | None = None,
) -> dict[str, object]:
    return {
        "workflow_id": "actor-explicit-builder-development-workflow",
        "workflow_version": "1.0.0-development",
        "profile_ref": digest("actor-explicit-development-profile"),
        "nodes": nodes or workflow_nodes(),
        "edges": edges or workflow_edges(),
        "entry_node_ids": ("validate-input",),
        "terminal_node_ids": ("external-handoff",),
        "source_graph_hashes": (
            digest("lifecycle-graph"),
            digest("phase-graph"),
            digest("context-graph"),
            digest("authorization-graph"),
        ),
        "promotion_status": "development_only",
    }


def command(
    *,
    action: WorkflowAction,
    resource_id: str,
    payload_sha256: str,
    governed_authority: WorkflowAuthority,
    command_id: str,
) -> WorkflowCommand:
    return WorkflowCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id,
        payload_sha256=payload_sha256,
        expected_authority_identity=governed_authority.authority_identity,
    )


def compile_workflow(
    *,
    nodes: tuple[WorkflowNode, ...] | None = None,
    edges: tuple[WorkflowEdge, ...] | None = None,
    governed_authority: WorkflowAuthority | None = None,
    governed_command: WorkflowCommand | None = None,
) -> ActorExplicitWorkflowIR:
    inputs = compile_inputs(nodes=nodes, edges=edges)
    auth = governed_authority or authority(WorkflowAction.COMPILE)
    resource_id = digest(f"{inputs['workflow_id']}:{inputs['workflow_version']}:{inputs['profile_ref']}")
    cmd = governed_command or command(
        action=WorkflowAction.COMPILE,
        resource_id=resource_id,
        payload_sha256=compute_workflow_compile_payload_sha256(**inputs),
        governed_authority=auth,
        command_id="compile-actor-explicit-workflow-v1",
    )
    return compile_actor_explicit_workflow(
        **inputs,
        command=cmd,
        authority=auth,
    )


@pytest.mark.parametrize(
    ("invalid_node", "expected_code"),
    (
        (
            lambda: node("human-decision", ActorKind.HUMAN_NODE, owner=""),
            "MISSING_ACTOR_OWNER",
        ),
        (
            lambda: node(
                "human-decision",
                ActorKind.HUMAN_NODE,
                owner=("human-owner", "agent-owner"),
            ),
            "AMBIGUOUS_ACTOR_OWNERSHIP",
        ),
        (
            lambda: node(
                "mixed-actor",
                (ActorKind.HUMAN_NODE, ActorKind.GOVERNED_AGENT_NODE),  # type: ignore[arg-type]
            ),
            "AMBIGUOUS_ACTOR_OWNERSHIP",
        ),
    ),
)
def test_missing_anonymous_or_mixed_actor_ownership_fails_closed(
    invalid_node,
    expected_code: str,
) -> None:
    with pytest.raises(WorkflowContractError) as caught:
        invalid_node()

    assert caught.value.code == expected_code


def test_cyclic_workflow_is_rejected_before_ir_commit() -> None:
    nodes = (
        node(
            "first",
            ActorKind.DETERMINISTIC_CODE_NODE,
            dependency_node_ids=("second",),
            declared_downstream_nodes=("second",),
        ),
        node(
            "second",
            ActorKind.GOVERNED_AGENT_NODE,
            dependency_node_ids=("first",),
            declared_downstream_nodes=("first",),
        ),
    )
    edges = (
        WorkflowEdge("first", "second", "contract:first:output:v1", "first_valid", True),
        WorkflowEdge("second", "first", "contract:second:output:v1", "second_valid", True),
    )
    result = None

    with pytest.raises(WorkflowContractError) as caught:
        result = compile_workflow(nodes=nodes, edges=edges)

    assert caught.value.code == "CYCLIC_WORKFLOW"
    assert result is None


def test_undeclared_handoff_is_rejected_atomically() -> None:
    nodes = workflow_nodes()
    undeclared = WorkflowEdge(
        source_node_id="validate-input",
        target_node_id="human-decision",
        payload_contract="contract:validate-input:output:v1",
        condition="attempt_hidden_handoff",
        validated_output_required=True,
    )

    with pytest.raises(WorkflowContractError) as caught:
        compile_workflow(nodes=nodes, edges=(*workflow_edges(), undeclared))

    assert caught.value.code == "UNDECLARED_HANDOFF"


def test_invalid_node_output_cannot_be_declared_to_advance_downstream() -> None:
    edges = tuple(
        replace(edge, validated_output_required=False)
        if edge.source_node_id == "bounded-proposal"
        else edge
        for edge in workflow_edges()
    )

    with pytest.raises(WorkflowContractError) as caught:
        compile_workflow(edges=edges)

    assert caught.value.code == "UNVALIDATED_OUTPUT_ADVANCEMENT"


def test_historical_human_decision_cannot_be_replayed_as_new_authority() -> None:
    nodes = workflow_nodes()
    object.__setattr__(next(item for item in nodes if item.node_id == "human-decision"), "human_decision_reissued", True)

    with pytest.raises(WorkflowContractError) as caught:
        compile_workflow(nodes=nodes)

    assert caught.value.code == "HUMAN_DECISION_REPLAY_PROHIBITED"


def test_external_boundary_is_declarative_and_cannot_request_execution() -> None:
    nodes = workflow_nodes()
    object.__setattr__(next(item for item in nodes if item.node_id == "external-handoff"), "external_execution_requested", True)

    with pytest.raises(WorkflowContractError) as caught:
        compile_workflow(nodes=nodes)

    assert caught.value.code == "EXTERNAL_EXECUTION_PROHIBITED"


@pytest.mark.parametrize(
    ("changed_field", "expected_code"),
    (
        ("payload_sha256", "COMMAND_PAYLOAD_MISMATCH"),
        ("resource_id", "COMMAND_RESOURCE_MISMATCH"),
        ("expected_authority_identity", "AUTHORITY_IDENTITY_MISMATCH"),
    ),
)
def test_compile_command_is_exactly_bound_to_payload_resource_and_authority(
    changed_field: str,
    expected_code: str,
) -> None:
    inputs = compile_inputs()
    auth = authority(WorkflowAction.COMPILE)
    resource_id = digest(
        f"{inputs['workflow_id']}:{inputs['workflow_version']}:{inputs['profile_ref']}"
    )
    valid = command(
        action=WorkflowAction.COMPILE,
        resource_id=resource_id,
        payload_sha256=compute_workflow_compile_payload_sha256(**inputs),
        governed_authority=auth,
        command_id="compile-authority-boundary",
    )
    invalid = replace(valid, **{changed_field: digest(f"wrong-{changed_field}")})

    with pytest.raises(WorkflowContractError) as caught:
        compile_workflow(governed_authority=auth, governed_command=invalid)

    assert caught.value.code == expected_code


def test_stale_authority_cannot_compile_a_new_workflow() -> None:
    stale = authority(
        WorkflowAction.COMPILE,
        status=AuthorityStatus.SUPERSEDED,
    )

    with pytest.raises(WorkflowContractError) as caught:
        compile_workflow(governed_authority=stale)

    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_nested_node_tampering_is_detected_at_serialization_boundary() -> None:
    workflow = compile_workflow()
    object.__setattr__(workflow.nodes[0], "owner", "forged-owner")

    with pytest.raises(WorkflowContractError) as caught:
        workflow.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_identical_compilation_is_byte_deterministic_and_idempotent() -> None:
    first = compile_workflow()
    second = compile_workflow()

    assert first.workflow_identity == second.workflow_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    assert validate_repeat_workflow_ir(first, second) is first


def test_conflicting_repeat_cannot_reuse_the_original_compilation_identity() -> None:
    original = compile_workflow()
    changed_nodes = tuple(
        replace(item, retry_eligible=True)
        if item.node_id == "bounded-proposal"
        else item
        for item in workflow_nodes()
    )
    changed = compile_workflow(nodes=changed_nodes)

    with pytest.raises(WorkflowContractError) as caught:
        validate_repeat_workflow_ir(original, changed)

    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_fresh_process_reproduces_exact_workflow_bytes() -> None:
    repository = Path(__file__).resolve().parents[3]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(repository / "src"), str(repository), environment.get("PYTHONPATH", ""))
    )
    script = (
        "from tests.stories.st_09_01.test_failure_authority_determinism "
        "import compile_workflow; "
        "from cmf_builder.workflow.actor_explicit_contracts import canonical_json_bytes; "
        "import sys; sys.stdout.buffer.write(canonical_json_bytes(compile_workflow().as_dict()))"
    )

    fresh_bytes = subprocess.check_output(
        [sys.executable, "-c", script],
        cwd=repository,
        env=environment,
    )

    assert fresh_bytes == canonical_json_bytes(compile_workflow().as_dict())


def test_invalidation_is_exact_authorized_non_destructive_and_historical() -> None:
    workflow = compile_workflow()
    historical_bytes = canonical_json_bytes(workflow.as_dict())
    governed_authority = authority(WorkflowAction.INVALIDATE)
    scope = (workflow.workflow_identity,)
    governed_command = command(
        action=WorkflowAction.INVALIDATE,
        resource_id=workflow.workflow_identity,
        payload_sha256=compute_workflow_invalidation_payload_sha256(
            prior_workflow_identity=workflow.workflow_identity,
            affected_scope=scope,
        ),
        governed_authority=governed_authority,
        command_id="invalidate-actor-explicit-workflow-v1",
    )

    transition = invalidate_workflow_ir(
        workflow,
        affected_scope=scope,
        command=governed_command,
        authority=governed_authority,
    )

    assert transition.prior_workflow_identity == workflow.workflow_identity
    assert transition.affected_scope == scope
    assert transition.active_after is False
    assert transition.historical_workflow_preserved is True
    assert transition.reevaluation_requires_new_workflow is True
    assert canonical_json_bytes(workflow.as_dict()) == historical_bytes


def test_failed_invalidation_leaves_zero_partial_state_and_preserves_history() -> None:
    workflow = compile_workflow()
    historical_bytes = canonical_json_bytes(workflow.as_dict())
    governed_authority = authority(WorkflowAction.INVALIDATE)
    scope = (workflow.workflow_identity,)
    invalid_command = command(
        action=WorkflowAction.INVALIDATE,
        resource_id=workflow.workflow_identity,
        payload_sha256=digest("wrong-invalidation-payload"),
        governed_authority=governed_authority,
        command_id="invalid-invalidation-attempt",
    )
    transition = None

    with pytest.raises(WorkflowContractError) as caught:
        transition = invalidate_workflow_ir(
            workflow,
            affected_scope=scope,
            command=invalid_command,
            authority=governed_authority,
        )

    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"
    assert transition is None
    assert canonical_json_bytes(workflow.as_dict()) == historical_bytes


def test_adr_006_external_temporal_conformance_remains_explicitly_pending() -> None:
    payload = compile_workflow().as_dict()

    assert payload["adapter_kind"] == "deterministic_local_development_adapter"
    assert payload["external_engine"] is False
    assert payload["workflow_execution"] is False
    assert payload["agent_execution"] is False
    assert payload["temporal_conformance"] == "EXTERNAL_VALIDATION_PENDING"
    assert payload["full_ADR_006_satisfaction"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False
