from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.events import new_domain_event  # noqa: E402
from ccp_studio.contracts.projection import ProjectionHealthStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.projection_service import ProjectionService, register_projection_command_handlers  # noqa: E402
from ccp_studio.workflows.projection_rebuild import ProjectionRebuildWorkflow  # noqa: E402


def _event(org_id=None, brand_id=None, aggregate_type="memory_event", aggregate_id=None, event_type="MemoryAdmissionApproved"):
    org_id = org_id or uuid4()
    brand_id = brand_id or uuid4()
    return new_domain_event(
        event_type=event_type,
        organization_id=org_id,
        brand_id=brand_id,
        command_id=uuid4(),
        correlation_id=uuid4(),
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id or uuid4(),
        payload={"source": "canonical_event_outbox"},
    )


def test_domain_events_update_projected_nodes_relationships_and_checkpoint():
    service = ProjectionService()
    event = _event()

    receipt = service.project_domain_event(domain_event=event, event_outbox_offset=0)

    assert receipt.health_status == ProjectionHealthStatus.healthy
    assert receipt.node_count == 3
    assert receipt.relationship_count == 2
    assert f"Brand:{event.brand_id}" in service.repository.adapter.nodes
    assert any(rel.source_event_id == event.event_id for rel in service.repository.adapter.relationships.values())
    assert receipt.checkpoint_id in service.repository.checkpoints
    assert service.repository.domain_events[-1].event_type == "DomainEventProjected"


def test_neo4j_outage_records_lag_without_blocking_canonical_command_bus():
    bus = create_in_memory_command_bus()
    org_id = uuid4()
    brand_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["operator"])
    canonical = bus.submit(
        new_command_envelope(
            command_type="SubmitCommand",
            organization_id=org_id,
            brand_id=brand_id,
            actor=actor,
            payload={"aggregate_id": str(uuid4())},
        )
    )
    service = ProjectionService()
    service.repository.adapter.available = False

    receipt = service.project_domain_event(domain_event=bus.event_outbox.events[-1], event_outbox_offset=0)

    assert canonical.status == CommandStatus.succeeded
    assert receipt.health_status == ProjectionHealthStatus.unavailable
    assert receipt.lag_event_count == 1
    assert service.repository.health.status == ProjectionHealthStatus.unavailable
    assert service.repository.lag_reports


def test_rebuild_from_canonical_events_reconstructs_graph_and_validates_counts():
    service = ProjectionService()
    org_id = uuid4()
    brand_id = uuid4()
    events = [_event(org_id, brand_id, aggregate_type="approval_event"), _event(org_id, brand_id, aggregate_type="publishing_intent")]

    receipt = service.rebuild_neo4j_projection(domain_events=events, idempotency_key="projection:rebuild:one")
    health = service.validate_projection_counts(expected_event_count=2)

    assert receipt.rebuild_result == "neo4j_projection_rebuilt"
    assert receipt.health_status == ProjectionHealthStatus.healthy
    assert len(service.repository.projection_events) == 2
    assert health.status == ProjectionHealthStatus.healthy
    assert len(service.repository.adapter.relationships) == 4


def test_graph_insight_cannot_mutate_production_state_directly():
    service = ProjectionService()

    decision = service.graph_insight_action_boundary(
        graph_query_ref="neo4j://query/route-memory-hotspot",
        requested_action="approve_asset_from_graph",
        required_command_type="ApproveAssetCommand",
        direct_graph_mutation_requested=True,
    )

    assert decision.direct_graph_mutation_allowed is False
    assert decision.required_command_type == "ApproveAssetCommand"
    assert "Command Bus" in decision.reason


def test_projection_conflict_marks_unhealthy_and_requires_rebuild():
    service = ProjectionService()
    event = _event()
    service.project_domain_event(domain_event=event, event_outbox_offset=0)
    service.repository.adapter.clear()

    health = service.validate_projection_counts(expected_event_count=1)
    receipt = service.mark_projection_unhealthy(reason="Projected nodes diverged from canonical event count.", conflict_count=2)

    assert health.status == ProjectionHealthStatus.unhealthy_rebuild_required
    assert receipt.health_status == ProjectionHealthStatus.unhealthy_rebuild_required
    assert receipt.conflict_count == 2
    assert service.repository.domain_events[-1].event_type == "ProjectionMarkedUnhealthy"


def test_projection_rebuild_workflow_stage14_routes_to_service():
    service = ProjectionService()
    workflow = ProjectionRebuildWorkflow(service)
    events = [_event(), _event()]

    receipt = workflow.stage14_rebuild_graph_projection(
        domain_events=events,
        idempotency_key="projection:workflow:rebuild",
    )

    assert receipt.rebuild_result == "neo4j_projection_rebuilt"
    assert receipt.node_count >= 3
    assert receipt.checkpoint_id in service.repository.checkpoints


def test_projection_command_bus_is_idempotent_and_emits_projection_receipt():
    service = ProjectionService()
    bus = create_in_memory_command_bus()
    org_id = uuid4()
    brand_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    register_projection_command_handlers(bus, service)
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["operator"])
    event = _event(org_id, brand_id)
    envelope = new_command_envelope(
        command_type="ProjectDomainEventCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="projection:command:project",
        payload={"domain_event": event.model_dump(mode="json"), "event_outbox_offset": 0},
    )

    first = bus.submit(envelope)
    second = bus.submit(envelope)

    assert first.status == CommandStatus.succeeded
    assert second.status == CommandStatus.replayed
    assert first.result_payload["projection_receipt_id"] == second.result_payload["projection_receipt_id"]
    assert len(service.repository.receipts) == 1
