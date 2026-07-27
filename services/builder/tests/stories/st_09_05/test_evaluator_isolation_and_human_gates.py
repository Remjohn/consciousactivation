import pytest

from cmf_builder.workflow.candidate_routing import (
    CandidateRoutingError,
    EvaluatorView,
    HumanGateClass,
    HumanGatePlacement,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def view(**overrides):
    values = {
        "candidate_identity": "candidate:a",
        "canonical_output_sha256": digest("output"),
        "input_contract_hash": digest("input-contract"),
        "rubric_hash": digest("rubric"),
        "evidence_hashes": (digest("evidence"),),
        "source_lineage_refs": ("lineage:source",),
        "cost_latency_observations": ("cost:offline", "latency:simulated"),
    }
    values.update(overrides)
    return EvaluatorView(**values)


def test_evaluator_view_contains_only_minimum_allowed_context():
    isolated = view()

    assert isolated.view_identity
    assert isolated.generator_hidden_reasoning == ""
    assert isolated.protected_benchmark_labels == ()


def test_evaluator_view_rejects_generator_reasoning_preferences_labels_and_secrets():
    forbidden = [
        {"generator_hidden_reasoning": "do not show"},
        {"generator_preferred_answer": "candidate:a"},
        {"protected_benchmark_labels": ("gold",)},
        {"credential_values": ("secret-value",)},
    ]
    for kwargs in forbidden:
        with pytest.raises(CandidateRoutingError) as caught:
            view(**kwargs)
        assert caught.value.code == "EVALUATOR_FORBIDDEN_VIEW"


def test_human_gate_cannot_be_resolved_by_automation():
    gate = HumanGatePlacement("gate:release", HumanGateClass.RELEASE_OR_PROMOTION, "human:authorized-reviewer")
    assert gate.gate_identity

    with pytest.raises(CandidateRoutingError) as caught:
        HumanGatePlacement(
            "gate:constitutional",
            HumanGateClass.CONSTITUTIONAL_DECISION,
            "human:constitutional-authority",
            resolved_by_model_agent_or_policy=True,
        )
    assert caught.value.code == "HUMAN_GATE_AUTOMATION_PROHIBITED"
