"""Projection repositories and deterministic Neo4j adapter for TS-CMF-058."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.projection import (
    ProjectedNode,
    ProjectedRelationship,
    ProjectionCheckpoint,
    ProjectionDomainEvent,
    ProjectionEvent,
    ProjectionHealth,
    ProjectionHealthStatus,
    ProjectionLagReport,
    ProjectionReceipt,
)
from ccp_studio.contracts.orchestration import utc_now


@dataclass
class InMemoryNeo4jAdapter:
    available: bool = True
    nodes: dict[str, ProjectedNode] = field(default_factory=dict)
    relationships: dict[UUID, ProjectedRelationship] = field(default_factory=dict)

    def write(self, nodes: list[ProjectedNode], relationships: list[ProjectedRelationship]) -> None:
        if not self.available:
            raise RuntimeError("Neo4j projection adapter unavailable")
        for node in nodes:
            self.nodes[node.node_ref] = node
        for relationship in relationships:
            self.relationships[relationship.relationship_id] = relationship

    def clear(self) -> None:
        self.nodes.clear()
        self.relationships.clear()


@dataclass
class InMemoryProjectionRepository:
    adapter: InMemoryNeo4jAdapter = field(default_factory=InMemoryNeo4jAdapter)
    checkpoints: dict[UUID, ProjectionCheckpoint] = field(default_factory=dict)
    projection_events: dict[UUID, ProjectionEvent] = field(default_factory=dict)
    receipts: dict[UUID, ProjectionReceipt] = field(default_factory=dict)
    lag_reports: dict[UUID, ProjectionLagReport] = field(default_factory=dict)
    domain_events: list[ProjectionDomainEvent] = field(default_factory=list)
    health: ProjectionHealth = field(
        default_factory=lambda: ProjectionHealth(
            schema_version="cmf.projection_health.v1",
            status=ProjectionHealthStatus.healthy,
            last_checkpoint_id=None,
            lag_event_count=0,
            conflict_count=0,
            message="Projection initialized.",
            checked_at=utc_now(),
        )
    )
    idempotency_index: dict[tuple[str, str], UUID] = field(default_factory=dict)

    def put_checkpoint(self, checkpoint: ProjectionCheckpoint) -> ProjectionCheckpoint:
        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
        self.health = self.health.model_copy(update={"last_checkpoint_id": checkpoint.checkpoint_id})
        return checkpoint

    def put_projection_event(self, event: ProjectionEvent) -> ProjectionEvent:
        self.projection_events[event.projection_event_id] = event
        return event

    def put_receipt(
        self,
        receipt: ProjectionReceipt,
        *,
        action: str | None = None,
        idempotency_key: str | None = None,
    ) -> ProjectionReceipt:
        self.receipts[receipt.projection_receipt_id] = receipt
        if action and idempotency_key:
            self.idempotency_index[(action, idempotency_key)] = receipt.projection_receipt_id
        return receipt

    def receipt_for_idempotency(self, action: str, idempotency_key: str) -> ProjectionReceipt | None:
        receipt_id = self.idempotency_index.get((action, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

    def put_lag_report(self, report: ProjectionLagReport) -> ProjectionLagReport:
        self.lag_reports[report.lag_report_id] = report
        return report

    def append_domain_event(self, event: ProjectionDomainEvent) -> ProjectionDomainEvent:
        self.domain_events.append(event)
        return event

    def set_health(self, health: ProjectionHealth) -> ProjectionHealth:
        self.health = health
        return health

    def reset_projection_state(self) -> None:
        self.adapter.clear()
        self.checkpoints.clear()
        self.projection_events.clear()
