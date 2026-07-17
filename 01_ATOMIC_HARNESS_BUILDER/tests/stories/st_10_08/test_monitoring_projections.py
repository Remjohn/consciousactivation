import pytest

from cmf_builder.application.monitoring_projections import (
    MonitorFamily,
    MonitorRecord,
    MonitoringProjectionError,
    filter_monitors,
)


def monitor(family=MonitorFamily.WORKFLOW_MONITOR, **overrides):
    values = {
        "monitor_identity": f"monitor:{family.value}",
        "family": family,
        "subject_identity": "workflow:1",
        "status": "ACTIVE",
        "evidence_refs": ("receipt:queue",),
        "owner": "builder",
        "checkpoint_ref": "checkpoint:1",
    }
    values.update(overrides)
    return MonitorRecord(**values)


def test_monitor_families_filter_stale_partial_disconnected_and_redacted_states():
    records = (
        monitor(MonitorFamily.WORKFLOW_MONITOR),
        monitor(MonitorFamily.QUEUE_MONITOR, stale=True),
        monitor(MonitorFamily.CONTEXT_MONITOR, partial=True, redacted=True, selected_context=("ctx:required",), required_context=("ctx:required",), excluded_context=("ctx:optional",)),
        monitor(MonitorFamily.INCIDENT_MONITOR, disconnected=True),
    )

    assert [item.family for item in filter_monitors(records, stale=True)] == [MonitorFamily.QUEUE_MONITOR]
    assert filter_monitors(records, family=MonitorFamily.CONTEXT_MONITOR)[0].redacted is True


def test_incident_resource_and_context_failures_are_governed():
    with pytest.raises(MonitoringProjectionError) as root:
        monitor(MonitorFamily.INCIDENT_MONITOR, root_cause_ref="INFERRED")
    assert root.value.code == "ROOT_CAUSE_NOT_DIAGNOSED"

    with pytest.raises(MonitoringProjectionError) as cost:
        monitor(MonitorFamily.RESOURCE_AND_COST_MONITOR, cost="$5.00", simulated=False)
    assert cost.value.code == "REAL_CLOUD_COST_REQUIRES_REAL_EVIDENCE"

    simulated = monitor(MonitorFamily.RESOURCE_AND_COST_MONITOR, cost="$5.00", simulated=True)
    assert simulated.simulated is True

    with pytest.raises(MonitoringProjectionError) as context:
        monitor(MonitorFamily.CONTEXT_MONITOR, selected_context=("ctx:x",), excluded_context=("ctx:x",))
    assert context.value.code == "EXCLUDED_CONTEXT_SELECTED"
