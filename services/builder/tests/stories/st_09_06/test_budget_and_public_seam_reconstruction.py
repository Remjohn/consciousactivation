import pytest

from cmf_builder.workflow.observability_recovery import (
    BudgetLimits,
    NodeTelemetry,
    ObservabilityRecoveryError,
    PublicSeamReceipt,
    QueueEvent,
    QueueState,
    project_queue,
    validate_budget,
)


def telemetry(latency=20, compute=3):
    return NodeTelemetry(
        "node:a",
        "actor:builder",
        "contract:v1",
        "obs:start",
        "obs:end",
        10,
        latency,
        compute,
        "NOT_APPLICABLE: no provider",
        "NOT_APPLICABLE: no provider",
        (),
        ("DEFAULT_DENY",),
        1,
        0,
        "closed",
        "not_used",
        "sandbox:policy",
        ("artifact",),
        ("validation",),
        (),
        "passed",
        "",
    )


def limits():
    return BudgetLimits(100, 200, 50, 100, 10, 20, 10, "gate:budget-human")


def test_budget_overflow_blocks_and_opens_authorized_gate():
    ok = validate_budget(telemetry(), limits(), observed_tokens=100, observed_cost_units=10)
    assert ok.within_budget is True
    assert ok.human_gate_ref == ""

    blocked = validate_budget(telemetry(latency=150), limits(), observed_tokens=250, observed_cost_units=25)
    assert blocked.within_budget is False
    assert "hard_token_limit" in blocked.blocked_reason
    assert blocked.human_gate_ref == "gate:budget-human"


def test_public_seam_reconstructs_from_public_contract_only():
    projection = project_queue((QueueEvent("event:0", 0, "workflow:1", "node:a", QueueState.PASSED, "done", (), "actor", "authority", "checkpoint", ()),))
    obs = telemetry()
    budget = validate_budget(obs, limits(), observed_tokens=100, observed_cost_units=10)

    receipt = PublicSeamReceipt(projection.projection_identity, (obs.telemetry_identity,), (budget.receipt_identity,), ("route:1",), ("checkpoint:1",))
    assert receipt.public_contract_only is True
    assert receipt.receipt_identity

    with pytest.raises(ObservabilityRecoveryError) as private:
        PublicSeamReceipt(projection.projection_identity, (obs.telemetry_identity,), (), (), (), private_state_used=True)
    assert private.value.code == "PRIVATE_STATE_AS_PUBLIC_SEAM_EVIDENCE"
