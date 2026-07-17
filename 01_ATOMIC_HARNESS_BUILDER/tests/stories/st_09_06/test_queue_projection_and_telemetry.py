import pytest

from cmf_builder.workflow.observability_recovery import (
    NodeTelemetry,
    ObservabilityRecoveryError,
    QueueEvent,
    QueueState,
    project_queue,
)


def event(seq, node, state, reason="ready"):
    return QueueEvent(f"event:{seq}", seq, "workflow:1", node, state, reason, (), "actor:builder", "authority:1", "checkpoint:1", ("artifact:1",))


def telemetry(**overrides):
    values = {
        "node_identity": "node:a",
        "actor_identity": "actor:builder",
        "contract_version": "contract:v1",
        "start_observation_ref": "obs:start",
        "end_observation_ref": "obs:end",
        "queue_wait_ms": 10,
        "execution_latency_ms": 20,
        "deterministic_compute_units": 3,
        "model_token_observation": "NOT_APPLICABLE: no provider call",
        "cost_observation": "NOT_APPLICABLE: no provider call",
        "tool_calls": (),
        "capability_grants": ("DEFAULT_DENY",),
        "attempts": 1,
        "retries": 0,
        "circuit_state": "closed",
        "cache_behavior": "not_used",
        "sandbox_policy_ref": "sandbox:policy",
        "artifact_refs": ("artifact:output",),
        "validation_refs": ("receipt:validation",),
        "human_interventions": (),
        "final_status": "passed",
        "failure_context": "",
    }
    values.update(overrides)
    return NodeTelemetry(**values)


def test_queue_projection_has_one_authoritative_state_per_node():
    projection = project_queue((event(0, "node:a", QueueState.QUEUED), event(1, "node:a", QueueState.PASSED, "validated")))

    assert projection.node_states == {"node:a": "passed"}
    assert projection.transition_reasons["node:a"] == "validated"
    assert projection.projection_identity


def test_queue_projection_rejects_out_of_order_duplicate_or_conflicting_stream():
    with pytest.raises(ObservabilityRecoveryError) as order:
        project_queue((event(1, "node:a", QueueState.QUEUED),))
    assert order.value.code == "OUT_OF_ORDER_EVENT_STREAM"

    with pytest.raises(ObservabilityRecoveryError) as duplicate:
        project_queue((event(0, "node:a", QueueState.QUEUED), event(0, "node:b", QueueState.QUEUED)))
    assert duplicate.value.code == "OUT_OF_ORDER_EVENT_STREAM"

    other_workflow = QueueEvent("event:1", 1, "workflow:2", "node:b", QueueState.QUEUED, "ready", (), "actor", "authority", "checkpoint", ())
    with pytest.raises(ObservabilityRecoveryError) as conflict:
        project_queue((event(0, "node:a", QueueState.QUEUED), other_workflow))
    assert conflict.value.code == "CONFLICTING_WORKFLOW_EVENTS"


def test_node_telemetry_requires_mandatory_observations_and_not_applicable_basis():
    obs = telemetry()
    assert obs.telemetry_identity
    assert obs.model_token_observation.startswith("NOT_APPLICABLE")

    with pytest.raises(ObservabilityRecoveryError) as missing:
        telemetry(model_token_observation="")
    assert missing.value.code == "MISSING_GOVERNED_FIELD"
