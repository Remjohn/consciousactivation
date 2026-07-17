import pytest

from cmf_builder.workflow.candidate_routing import (
    CandidateRoutingError,
    ComputeRoutePolicy,
    ComputeRouteRequest,
    route_compute,
)


def request(**overrides):
    values = {
        "node_responsibility": "compile_candidate",
        "actor_kind": "GOVERNED_AGENT_NODE",
        "task_complexity": 4,
        "ambiguity": 3,
        "risk": 5,
        "expected_value": 8,
        "prior_evidence_refs": ("evidence:development",),
        "latency_budget": "latency:bounded",
        "cost_budget": "cost:offline-simulated",
    }
    values.update(overrides)
    return ComputeRouteRequest(**values)


def policy(**overrides):
    values = {
        "policy_id": "risk-aware-routing",
        "registered_model_tiers": ("tier:small", "tier:medium", "tier:large"),
        "registered_evaluator_strengths": ("eval:light", "eval:strong"),
        "allowed_tool_grants": ("DEFAULT_DENY",),
        "max_candidate_count": 4,
        "human_gate_threshold": 5,
    }
    values.update(overrides)
    return ComputeRoutePolicy(**values)


def test_compute_route_is_deterministic_provider_neutral_and_budget_bounded():
    first = route_compute(request(), policy())
    second = route_compute(request(), policy())

    assert first.decision_identity == second.decision_identity
    assert first.provider_or_model_selected is False
    assert first.tool_grants == ("DEFAULT_DENY",)
    assert first.compute_budget == "cost:offline-simulated"
    assert first.required_human_gate_refs == ("gate:risk-or-budget",)


def test_missing_route_evidence_or_unbounded_fanout_fails_closed():
    with pytest.raises(CandidateRoutingError) as evidence:
        route_compute(request(prior_evidence_refs=()), policy())
    assert evidence.value.code == "MISSING_GOVERNED_FIELD"

    with pytest.raises(CandidateRoutingError) as fanout:
        policy(max_candidate_count=0)
    assert fanout.value.code == "UNBOUNDED_ROUTE_FAN_OUT"
