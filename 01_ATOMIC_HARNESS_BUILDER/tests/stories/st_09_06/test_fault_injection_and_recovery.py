import pytest

from cmf_builder.workflow.observability_recovery import (
    FaultClass,
    FaultFixture,
    ObservabilityRecoveryError,
    QueueState,
    inject_fault_and_recover,
)


def fixture(fault_class=FaultClass.TIMEOUT, **overrides):
    values = {
        "fixture_id": "fault:timeout",
        "fault_class": fault_class,
        "injected_observation_ref": "injected:timeout",
        "affected_node": "node:a",
        "expected_state": QueueState.RETRYING,
        "repair_or_escalation_route": "route:retry",
    }
    values.update(overrides)
    return FaultFixture(**values)


def test_injected_fault_reaches_contained_recovery_state():
    receipt = inject_fault_and_recover(fixture(), ("node:unaffected",))

    assert receipt.contained_state == "retrying"
    assert receipt.repair_or_escalation_route == "route:retry"
    assert receipt.unaffected_branches_preserved == ("node:unaffected",)
    assert receipt.partial_state_created is False


def test_provider_unavailable_is_fixture_not_real_provider_outage_evidence():
    receipt = inject_fault_and_recover(
        fixture(FaultClass.PROVIDER_UNAVAILABLE, expected_state=QueueState.WAITING_HUMAN, repair_or_escalation_route="route:human-provider-gate"),
        ("node:independent",),
    )
    assert receipt.resume_eligible is False
    assert receipt.rollback_eligible is True


def test_external_fault_execution_is_prohibited():
    with pytest.raises(ObservabilityRecoveryError) as caught:
        fixture(external_fault_executed=True)
    assert caught.value.code == "EXTERNAL_FAULT_EXECUTION_PROHIBITED"
