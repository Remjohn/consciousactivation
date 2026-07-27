from __future__ import annotations

from dataclasses import replace
import hashlib
import socket
import subprocess

import pytest

from cmf_builder.workflow.actor_explicit_contracts import (
    ActorExplicitWorkflowIR,
    ActorKind,
    WorkflowAuthority,
    WorkflowEdge,
    WorkflowNode,
    compile_actor_explicit_workflow,
)
from cmf_builder.workflow.deterministic_local_adapter import (
    DeterministicLocalWorkflowAdapter,
    LocalAdapterError,
    RoutingRequest,
    WorkflowProfile,
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def node(
    node_id: str,
    actor_kind: ActorKind,
    *,
    dependencies: tuple[str, ...] = (),
    downstream: tuple[str, ...] = (),
    input_contract: str = "governed-text/v1",
    output_contract: str = "governed-text/v1",
) -> WorkflowNode:
    return WorkflowNode(
        node_id=node_id,
        actor_kind=actor_kind,
        owner=f"owner:{node_id}",
        input_contract=input_contract,
        output_contract=output_contract,
        authority_requirement=f"authority:{node_id}",
        dependency_node_ids=dependencies,
        execution_preconditions=("validated-input",),
        completion_condition="typed-output-valid",
        rejection_behavior="stop-with-typed-rejection",
        retry_eligible=False,
        checkpoint_behavior="checkpoint-after-validation",
        cancellation_behavior="cancel-before-downstream-advance",
        failure_owner=f"owner:{node_id}",
        declared_downstream_nodes=downstream,
        producer_output_validation_ref=f"validator:{node_id}:v1",
    )


def workflow(*, workflow_id: str = "local-actor-explicit-workflow") -> ActorExplicitWorkflowIR:
    source = node(
        "validate-input",
        ActorKind.DETERMINISTIC_CODE_NODE,
        downstream=("human-gate",),
    )
    gate = node(
        "human-gate",
        ActorKind.HUMAN_NODE,
        dependencies=("validate-input",),
    )
    return compile_actor_explicit_workflow(
        workflow_id=workflow_id,
        workflow_version="1.0.0-development",
        nodes=(gate, source),
        edges=(
            WorkflowEdge(
                source_node_id="validate-input",
                target_node_id="human-gate",
                payload_contract="governed-text/v1",
                condition="validated-output-present",
            ),
        ),
        authority=WorkflowAuthority(
            authority_id="od-am-001-st-09.01",
            version="1.0.0-development",
            sha256=digest("workflow-authority"),
            scope=("OFFLINE_DEVELOPMENT",),
        ),
        source_refs=(digest("active-workflow-graphs"),),
        predecessor_receipts=(digest("st-08.07-receipt"),),
    )


def profile(
    *,
    profile_id: str = "bounded-activative-review",
    profile_version: str = "1.0.0-development",
    registry_version: str = "registry-1.0.0-development",
    risk_states: tuple[str, ...] = ("bounded",),
) -> WorkflowProfile:
    return WorkflowProfile(
        profile_id=profile_id,
        profile_version=profile_version,
        profile_sha256=digest(
            f"{profile_id}:{profile_version}:{registry_version}:{risk_states}"
        ),
        registry_version=registry_version,
        request_classifications=("activative-structural-review",),
        target_profiles=("reply_dm",),
        risk_states=risk_states,
    )


def request(
    *,
    request_id: str = "request-001",
    registry_version: str = "registry-1.0.0-development",
    risk_state: str = "bounded",
) -> RoutingRequest:
    return RoutingRequest(
        request_id=request_id,
        request_classification="activative-structural-review",
        target_profile="reply_dm",
        risk_state=risk_state,
        registry_version=registry_version,
    )


def adapter() -> DeterministicLocalWorkflowAdapter:
    return DeterministicLocalWorkflowAdapter(
        adapter_id="deterministic-local-development-adapter",
        adapter_version="1.0.0-development",
    )


def test_adapter_exposes_only_the_five_execution_free_operations() -> None:
    local = adapter()

    assert local.allowed_operations == (
        "compile",
        "validate",
        "register_profile",
        "select_profile",
        "query_compiled_contract",
    )
    assert local.external_engine is False
    assert local.network_access is False
    assert local.workflow_execution is False
    assert local.agent_execution is False
    assert local.external_product_execution is False
    assert local.temporal_conformance == "EXTERNAL_VALIDATION_PENDING"
    assert not hasattr(local, "execute")
    assert not hasattr(local, "run_node")
    assert not hasattr(local, "resume")


def test_compile_validate_and_query_are_deterministic_and_execution_free() -> None:
    governed_workflow = workflow()
    first_adapter = adapter()
    second_adapter = adapter()

    assert first_adapter.validate(governed_workflow) is True
    first = first_adapter.compile(governed_workflow, "compile-command-001")
    second = second_adapter.compile(governed_workflow, "compile-command-001")

    assert first == second
    assert first.receipt_identity == second.receipt_identity
    assert first.workflow_identity == governed_workflow.workflow_identity
    assert first.canonical_workflow_sha256 == digest_bytes(
        governed_workflow.as_dict()
    )
    assert first.execution_performed is False
    assert first.as_dict()["execution_performed"] is False
    assert first_adapter.query_compiled_contract(first.workflow_identity) is governed_workflow


def digest_bytes(value: object) -> str:
    from cmf_builder.workflow.actor_explicit_contracts import canonical_json_bytes

    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def test_compile_does_not_access_network_or_start_an_external_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def prohibited(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("local adapter attempted prohibited external execution")

    monkeypatch.setattr(socket, "socket", prohibited)
    monkeypatch.setattr(subprocess, "run", prohibited)
    monkeypatch.setattr(subprocess, "Popen", prohibited)

    local = adapter()
    governed_workflow = workflow()
    receipt = local.compile(governed_workflow, "compile-without-runtime")

    assert receipt.execution_performed is False
    assert local.query_compiled_contract(receipt.workflow_identity) == governed_workflow


def test_identical_compile_command_is_payload_safe_and_idempotent() -> None:
    local = adapter()
    governed_workflow = workflow()

    first = local.compile(governed_workflow, "stable-compile-command")
    repeated = local.compile(governed_workflow, "stable-compile-command")

    assert repeated is first
    assert repeated.receipt_identity == first.receipt_identity


def test_conflicting_compile_command_rejects_without_registering_second_workflow() -> None:
    local = adapter()
    first_workflow = workflow()
    conflicting_workflow = workflow(workflow_id="different-workflow")
    local.compile(first_workflow, "one-command-id")

    with pytest.raises(LocalAdapterError) as conflict:
        local.compile(conflicting_workflow, "one-command-id")
    assert conflict.value.code == "CONFLICTING_COMMAND_PAYLOAD"

    with pytest.raises(LocalAdapterError) as absent:
        local.query_compiled_contract(conflicting_workflow.workflow_identity)
    assert absent.value.code == "UNKNOWN_COMPILED_WORKFLOW"


def test_versioned_profile_registration_is_deterministic_and_idempotent() -> None:
    first_adapter = adapter()
    second_adapter = adapter()
    governed_profile = profile()

    first = first_adapter.register_profile(governed_profile, "register-profile-001")
    repeated = first_adapter.register_profile(governed_profile, "register-profile-001")
    fresh = second_adapter.register_profile(governed_profile, "register-profile-001")

    assert repeated is first
    assert fresh == first
    assert first.receipt_identity == fresh.receipt_identity
    assert first.profile_identity == governed_profile.profile_identity
    assert first.registry_version == governed_profile.registry_version


def test_registered_profile_version_is_immutable() -> None:
    local = adapter()
    original = profile()
    local.register_profile(original, "register-original")
    changed = replace(
        original,
        profile_sha256=digest("mutated-profile-bytes"),
    )

    with pytest.raises(LocalAdapterError) as conflict:
        local.register_profile(changed, "register-mutated")
    assert conflict.value.code == "IMMUTABLE_PROFILE_CONFLICT"


def test_profile_promotion_above_development_only_is_prohibited() -> None:
    with pytest.raises(LocalAdapterError) as prohibited:
        replace(profile(), promotion_status="PRODUCTION")
    assert prohibited.value.code == "PRODUCTION_PROMOTION_PROHIBITED"


def test_profile_identity_changes_for_a_new_registry_or_profile_version() -> None:
    original = profile()
    new_profile_version = profile(profile_version="1.0.1-development")
    new_registry_version = profile(registry_version="registry-1.0.1-development")

    assert new_profile_version.profile_identity != original.profile_identity
    assert new_registry_version.profile_identity != original.profile_identity


def test_stable_routing_uses_all_four_governed_routing_inputs() -> None:
    first_adapter = adapter()
    second_adapter = adapter()
    governed_profile = profile()
    for local in (first_adapter, second_adapter):
        local.register_profile(governed_profile, "register-profile")

    first = first_adapter.select_profile(request())
    repeated = first_adapter.select_profile(request())
    fresh = second_adapter.select_profile(request())

    assert repeated == first
    assert fresh == first
    assert first.decision_identity == fresh.decision_identity
    assert first.profile_id == governed_profile.profile_id
    assert first.profile_identity == governed_profile.profile_identity
    assert first.registry_version == governed_profile.registry_version


@pytest.mark.parametrize(
    "routing_request",
    (
        request(registry_version="registry-stale"),
        request(risk_state="high-risk"),
        RoutingRequest(
            request_id="wrong-classification",
            request_classification="generic-task",
            target_profile="reply_dm",
            risk_state="bounded",
            registry_version="registry-1.0.0-development",
        ),
        RoutingRequest(
            request_id="wrong-target",
            request_classification="activative-structural-review",
            target_profile="public_comment",
            risk_state="bounded",
            registry_version="registry-1.0.0-development",
        ),
    ),
)
def test_route_requires_exact_classification_target_risk_and_registry_version(
    routing_request: RoutingRequest,
) -> None:
    local = adapter()
    local.register_profile(profile(), "register-profile")

    with pytest.raises(LocalAdapterError) as no_route:
        local.select_profile(routing_request)
    assert no_route.value.code == "NO_DETERMINISTIC_ROUTE"


def test_ambiguous_exact_route_emits_typed_nondeterminism() -> None:
    local = adapter()
    local.register_profile(profile(profile_id="profile-a"), "register-a")
    local.register_profile(profile(profile_id="profile-b"), "register-b")

    with pytest.raises(LocalAdapterError) as nondeterminism:
        local.select_profile(request())

    assert nondeterminism.value.code == "NONDETERMINISTIC_ROUTING"
    assert nondeterminism.value.context["candidate_profile_ids"] == (
        "profile-a",
        "profile-b",
    )


def test_unknown_compiled_contract_query_fails_closed() -> None:
    with pytest.raises(LocalAdapterError) as unknown:
        adapter().query_compiled_contract(digest("not-compiled"))
    assert unknown.value.code == "UNKNOWN_COMPILED_WORKFLOW"
