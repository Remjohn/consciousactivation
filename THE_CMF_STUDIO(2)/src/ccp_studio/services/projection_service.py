"""Neo4j relationship projection service for TS-CMF-058."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.events import DomainEventEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.projection import (
    GraphInsightActionDecision,
    ProjectedNode,
    ProjectedRelationship,
    ProjectionCheckpoint,
    ProjectionDomainEvent,
    ProjectionEvent,
    ProjectionHealth,
    ProjectionHealthStatus,
    ProjectionLagReport,
    ProjectionReceipt,
    new_projection_checkpoint,
    new_projection_receipt,
)
from ccp_studio.repositories.projection import InMemoryProjectionRepository
from ccp_studio.services.command_bus import CommandBus


PROJECTION_ROLES = {"owner", "admin", "operator", "production_steward"}
PROJECTION_VERSION = "neo4j_relationship_projection.v1"


class ProjectionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ProjectionService:
    repository: InMemoryProjectionRepository = field(default_factory=InMemoryProjectionRepository)

    def project_domain_event(
        self,
        *,
        domain_event: DomainEventEnvelope | dict[str, Any],
        event_outbox_offset: int,
        idempotency_key: str | None = None,
    ) -> ProjectionReceipt:
        if idempotency_key:
            prior = self.repository.receipt_for_idempotency("project", idempotency_key)
            if prior:
                return prior
        event = self._domain_event(domain_event)
        batch_id = uuid4()
        nodes, relationships = self._map_event(event, batch_id)
        try:
            self.repository.adapter.write(nodes, relationships)
        except RuntimeError:
            lag = self._lag_report(expected_event_count=event_outbox_offset + 1)
            receipt = self._receipt(
                checkpoint_id=self.repository.health.last_checkpoint_id,
                event_range_start=event_outbox_offset,
                event_range_end=event_outbox_offset,
                node_count=0,
                relationship_count=0,
                lag_event_count=lag.lag_event_count,
                conflict_count=self.repository.health.conflict_count,
                rebuild_result="projection_lag_recorded_canonical_workflow_continues",
                health_status=ProjectionHealthStatus.unavailable,
                action="project",
                idempotency_key=idempotency_key,
            )
            self._event("ProjectionLagRetryScheduled", None, None, {"source_event_id": str(event.event_id), "lag_event_count": lag.lag_event_count})
            return receipt
        projection_event = self.repository.put_projection_event(
            ProjectionEvent(
                schema_version="cmf.projection_event.v1",
                projection_event_id=uuid4(),
                source_event_id=event.event_id,
                event_outbox_offset=event_outbox_offset,
                projection_batch_id=batch_id,
                node_count=len(nodes),
                relationship_count=len(relationships),
                checkpoint_id=None,
                projected_at=utc_now(),
            )
        )
        checkpoint = self.create_projection_checkpoint(
            event_outbox_offset=event_outbox_offset,
            projected_event_count=len(self.repository.projection_events),
        )
        self.repository.put_projection_event(projection_event.model_copy(update={"checkpoint_id": checkpoint.checkpoint_id}))
        self._set_health(
            status=ProjectionHealthStatus.healthy,
            lag_event_count=0,
            conflict_count=self.repository.health.conflict_count,
            message="Projection event written.",
            checkpoint_id=checkpoint.checkpoint_id,
        )
        receipt = self._receipt(
            checkpoint_id=checkpoint.checkpoint_id,
            event_range_start=event_outbox_offset,
            event_range_end=event_outbox_offset,
            node_count=len(self.repository.adapter.nodes),
            relationship_count=len(self.repository.adapter.relationships),
            lag_event_count=0,
            conflict_count=self.repository.health.conflict_count,
            rebuild_result="domain_event_projected",
            health_status=ProjectionHealthStatus.healthy,
            action="project",
            idempotency_key=idempotency_key,
        )
        self._event("DomainEventProjected", checkpoint.checkpoint_id, projection_event.projection_event_id, {"source_event_id": str(event.event_id)})
        return receipt

    def project_outbox_events(self, events: list[DomainEventEnvelope], *, start_offset: int = 0) -> ProjectionReceipt:
        if not events:
            return self._receipt(
                checkpoint_id=self.repository.health.last_checkpoint_id,
                event_range_start=start_offset,
                event_range_end=start_offset,
                node_count=len(self.repository.adapter.nodes),
                relationship_count=len(self.repository.adapter.relationships),
                lag_event_count=0,
                conflict_count=self.repository.health.conflict_count,
                rebuild_result="no_events_to_project",
                health_status=self.repository.health.status,
            )
        latest: ProjectionReceipt | None = None
        for offset, event in enumerate(events, start=start_offset):
            latest = self.project_domain_event(domain_event=event, event_outbox_offset=offset)
        return latest

    def create_projection_checkpoint(self, *, event_outbox_offset: int, projected_event_count: int) -> ProjectionCheckpoint:
        checkpoint = self.repository.put_checkpoint(
            new_projection_checkpoint(
                event_outbox_offset=event_outbox_offset,
                projected_event_count=projected_event_count,
                projection_version=PROJECTION_VERSION,
            )
        )
        self._event("ProjectionCheckpointCreated", checkpoint.checkpoint_id, None, {"event_outbox_offset": event_outbox_offset})
        return checkpoint

    def rebuild_neo4j_projection(
        self,
        *,
        domain_events: list[DomainEventEnvelope | dict[str, Any]],
        from_checkpoint_id: UUID | None = None,
        idempotency_key: str | None = None,
    ) -> ProjectionReceipt:
        if idempotency_key:
            prior = self.repository.receipt_for_idempotency("rebuild", idempotency_key)
            if prior:
                return prior
        start_offset = 0
        if from_checkpoint_id is not None:
            checkpoint = self.repository.checkpoints.get(from_checkpoint_id)
            if checkpoint is None:
                raise ProjectionError("PROJECTION_CHECKPOINT_REQUIRED", "Checkpoint is required for rebuild.")
            start_offset = checkpoint.event_outbox_offset + 1
        events = [self._domain_event(event) for event in domain_events][start_offset:]
        self.repository.reset_projection_state()
        receipt = self.project_outbox_events(events, start_offset=start_offset)
        validation = self.validate_projection_counts(expected_event_count=len(events))
        receipt = self._receipt(
            checkpoint_id=self.repository.health.last_checkpoint_id,
            event_range_start=start_offset,
            event_range_end=start_offset + len(events) - 1 if events else start_offset,
            node_count=len(self.repository.adapter.nodes),
            relationship_count=len(self.repository.adapter.relationships),
            lag_event_count=validation.lag_event_count,
            conflict_count=validation.conflict_count,
            rebuild_result="neo4j_projection_rebuilt",
            health_status=validation.status,
            action="rebuild",
            idempotency_key=idempotency_key,
        )
        self._event("Neo4jProjectionRebuilt", receipt.checkpoint_id, None, {"event_count": len(events)})
        return receipt

    def validate_projection_counts(self, *, expected_event_count: int) -> ProjectionHealth:
        projected = len(self.repository.projection_events)
        lag = max(expected_event_count - projected, 0)
        conflict_count = 0
        if projected and (not self.repository.adapter.nodes or not self.repository.adapter.relationships):
            conflict_count += 1
        status = ProjectionHealthStatus.healthy
        message = "Projection counts validated."
        if conflict_count:
            status = ProjectionHealthStatus.unhealthy_rebuild_required
            message = "Projection count conflict requires rebuild."
        elif lag:
            status = ProjectionHealthStatus.lagging
            message = "Projection lag detected."
        health = self._set_health(
            status=status,
            lag_event_count=lag,
            conflict_count=conflict_count,
            message=message,
            checkpoint_id=self.repository.health.last_checkpoint_id,
        )
        self._event("ProjectionCountsValidated", health.last_checkpoint_id, None, {"expected_event_count": expected_event_count, "projected_event_count": projected})
        return health

    def mark_projection_unhealthy(self, *, reason: str, conflict_count: int = 1) -> ProjectionReceipt:
        health = self._set_health(
            status=ProjectionHealthStatus.unhealthy_rebuild_required,
            lag_event_count=self.repository.health.lag_event_count,
            conflict_count=conflict_count,
            message=reason,
            checkpoint_id=self.repository.health.last_checkpoint_id,
        )
        receipt = self._receipt(
            checkpoint_id=health.last_checkpoint_id,
            event_range_start=0,
            event_range_end=max((item.event_outbox_offset for item in self.repository.projection_events.values()), default=0),
            node_count=len(self.repository.adapter.nodes),
            relationship_count=len(self.repository.adapter.relationships),
            lag_event_count=health.lag_event_count,
            conflict_count=health.conflict_count,
            rebuild_result="projection_unhealthy_rebuild_required",
            health_status=health.status,
        )
        self._event("ProjectionMarkedUnhealthy", health.last_checkpoint_id, None, {"reason": reason, "conflict_count": conflict_count})
        return receipt

    def retry_projection_lag(self, *, domain_events: list[DomainEventEnvelope | dict[str, Any]]) -> ProjectionReceipt:
        start = (self.repository.health.last_checkpoint_id and self.repository.checkpoints[self.repository.health.last_checkpoint_id].event_outbox_offset + 1) or 0
        return self.project_outbox_events([self._domain_event(event) for event in domain_events][start:], start_offset=start)

    def graph_insight_action_boundary(
        self,
        *,
        graph_query_ref: str,
        requested_action: str,
        required_command_type: str,
        direct_graph_mutation_requested: bool,
    ) -> GraphInsightActionDecision:
        return GraphInsightActionDecision(
            schema_version="cmf.graph_insight_action_decision.v1",
            graph_query_ref=graph_query_ref,
            requested_action=requested_action,
            direct_graph_mutation_allowed=False,
            required_command_type=required_command_type,
            reason="Graph insights may inform operators, but production actions must use Command Bus and canonical state."
            if direct_graph_mutation_requested
            else "Command Bus boundary preserved.",
        )

    def stage14_rebuild_graph_projection(self, **kwargs: Any) -> ProjectionReceipt:
        return self.rebuild_neo4j_projection(**kwargs)

    def _map_event(self, event: DomainEventEnvelope, projection_batch_id: UUID) -> tuple[list[ProjectedNode], list[ProjectedRelationship]]:
        brand_ref = f"Brand:{event.brand_id}"
        aggregate_ref = f"{event.aggregate_type}:{event.aggregate_id}"
        event_ref = f"DomainEvent:{event.event_id}"
        nodes = [
            ProjectedNode(node_ref=brand_ref, node_type="Brand", source_event_id=event.event_id, properties={"brand_id": str(event.brand_id), "organization_id": str(event.organization_id)}),
            ProjectedNode(node_ref=aggregate_ref, node_type=event.aggregate_type, source_event_id=event.event_id, properties={"aggregate_id": str(event.aggregate_id), "event_type": event.event_type}),
            ProjectedNode(node_ref=event_ref, node_type="DomainEvent", source_event_id=event.event_id, properties={"event_type": event.event_type, "command_id": str(event.command_id)}),
        ]
        relationships = [
            ProjectedRelationship(
                relationship_id=uuid4(),
                from_node_ref=brand_ref,
                to_node_ref=aggregate_ref,
                relationship_type="OWNS_AGGREGATE",
                source_event_id=event.event_id,
                projection_batch_id=projection_batch_id,
            ),
            ProjectedRelationship(
                relationship_id=uuid4(),
                from_node_ref=event_ref,
                to_node_ref=aggregate_ref,
                relationship_type="PROJECTS",
                source_event_id=event.event_id,
                projection_batch_id=projection_batch_id,
            ),
        ]
        return nodes, relationships

    def _lag_report(self, *, expected_event_count: int) -> ProjectionLagReport:
        projected = len(self.repository.projection_events)
        lag = max(expected_event_count - projected, 0)
        report = self.repository.put_lag_report(
            ProjectionLagReport(
                schema_version="cmf.projection_lag_report.v1",
                lag_report_id=uuid4(),
                expected_event_count=expected_event_count,
                projected_event_count=projected,
                lag_event_count=lag,
                status=ProjectionHealthStatus.unavailable,
                created_at=utc_now(),
            )
        )
        self._set_health(
            status=ProjectionHealthStatus.unavailable,
            lag_event_count=lag,
            conflict_count=self.repository.health.conflict_count,
            message="Neo4j unavailable; canonical workflows continue.",
            checkpoint_id=self.repository.health.last_checkpoint_id,
        )
        return report

    def _receipt(
        self,
        *,
        checkpoint_id: UUID | None,
        event_range_start: int,
        event_range_end: int,
        node_count: int,
        relationship_count: int,
        lag_event_count: int,
        conflict_count: int,
        rebuild_result: str,
        health_status: ProjectionHealthStatus,
        action: str | None = None,
        idempotency_key: str | None = None,
    ) -> ProjectionReceipt:
        return self.repository.put_receipt(
            new_projection_receipt(
                checkpoint_id=checkpoint_id,
                event_range_start=event_range_start,
                event_range_end=event_range_end,
                node_count=node_count,
                relationship_count=relationship_count,
                lag_event_count=lag_event_count,
                conflict_count=conflict_count,
                rebuild_result=rebuild_result,
                health_status=health_status,
            ),
            action=action,
            idempotency_key=idempotency_key,
        )

    def _set_health(
        self,
        *,
        status: ProjectionHealthStatus,
        lag_event_count: int,
        conflict_count: int,
        message: str,
        checkpoint_id: UUID | None,
    ) -> ProjectionHealth:
        return self.repository.set_health(
            ProjectionHealth(
                schema_version="cmf.projection_health.v1",
                status=status,
                last_checkpoint_id=checkpoint_id,
                lag_event_count=lag_event_count,
                conflict_count=conflict_count,
                message=message,
                checked_at=utc_now(),
            )
        )

    @staticmethod
    def _domain_event(event: DomainEventEnvelope | dict[str, Any]) -> DomainEventEnvelope:
        if isinstance(event, DomainEventEnvelope):
            return event
        return DomainEventEnvelope(**event)

    def _event(
        self,
        event_type: str,
        checkpoint_id: UUID | None,
        projection_event_id: UUID | None,
        payload: dict[str, Any],
    ) -> ProjectionDomainEvent:
        return self.repository.append_domain_event(
            ProjectionDomainEvent(
                schema_version="cmf.projection_domain_event.v1",
                projection_domain_event_id=uuid4(),
                event_type=event_type,
                checkpoint_id=checkpoint_id,
                projection_event_id=projection_event_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class ProjectionCommandHandler:
    command_type: str
    service: ProjectionService
    aggregate_type: str = "projection"
    allowed_roles: set[str] = field(default_factory=lambda: PROJECTION_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "ProjectDomainEventCommand":
            return self.service.project_domain_event(
                domain_event=payload["domain_event"],
                event_outbox_offset=int(payload["event_outbox_offset"]),
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "CreateProjectionCheckpointCommand":
            return self.service.create_projection_checkpoint(
                event_outbox_offset=int(payload["event_outbox_offset"]),
                projected_event_count=int(payload["projected_event_count"]),
            ).model_dump(mode="json")
        if self.command_type == "RebuildNeo4jProjectionCommand":
            return self.service.rebuild_neo4j_projection(
                domain_events=payload.get("domain_events", []),
                from_checkpoint_id=UUID(payload["from_checkpoint_id"]) if payload.get("from_checkpoint_id") else None,
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "ValidateProjectionCountsCommand":
            return self.service.validate_projection_counts(
                expected_event_count=int(payload["expected_event_count"])
            ).model_dump(mode="json")
        if self.command_type == "MarkProjectionUnhealthyCommand":
            return self.service.mark_projection_unhealthy(
                reason=payload["reason"],
                conflict_count=int(payload.get("conflict_count", 1)),
            ).model_dump(mode="json")
        if self.command_type == "RetryProjectionLagCommand":
            return self.service.retry_projection_lag(domain_events=payload.get("domain_events", [])).model_dump(mode="json")
        raise ProjectionError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        if payload.get("checkpoint_id"):
            return UUID(payload["checkpoint_id"])
        return envelope.brand_id


def register_projection_command_handlers(bus: CommandBus, service: ProjectionService) -> None:
    for command_type in [
        "ProjectDomainEventCommand",
        "CreateProjectionCheckpointCommand",
        "RebuildNeo4jProjectionCommand",
        "ValidateProjectionCountsCommand",
        "MarkProjectionUnhealthyCommand",
        "RetryProjectionLagCommand",
    ]:
        bus.register_handler(ProjectionCommandHandler(command_type=command_type, service=service))
