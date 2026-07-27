"""Command spine repositories.

The in-memory repositories are used by tests and local durable workflows. The
SQL migration in docs/migration/cmf_studio/001_command_spine.sql defines the
PostgreSQL persistence target for production deployments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope, CommandResult
from ccp_studio.contracts.events import DomainEventEnvelope
from ccp_studio.contracts.receipts import AuditReceipt


@dataclass
class InMemoryCommandLogRepository:
    records: dict[UUID, tuple[CommandEnvelope, CommandResult]] = field(default_factory=dict)

    def put(self, envelope: CommandEnvelope, result: CommandResult) -> None:
        self.records[envelope.command_id] = (envelope, result)

    def get(self, command_id: UUID) -> tuple[CommandEnvelope, CommandResult] | None:
        return self.records.get(command_id)


@dataclass
class InMemoryDomainEventOutbox:
    events: list[DomainEventEnvelope] = field(default_factory=list)

    def append(self, event: DomainEventEnvelope) -> None:
        self.events.append(event)


@dataclass
class InMemoryAuditReceiptRepository:
    receipts: list[AuditReceipt] = field(default_factory=list)
    writable: bool = True

    def append(self, receipt: AuditReceipt) -> None:
        if not self.writable:
            raise RuntimeError("audit receipt repository is not writable")
        self.receipts.append(receipt)

    def is_ready(self) -> bool:
        return self.writable


@dataclass
class InMemoryIdempotencyRepository:
    records: dict[tuple[UUID, UUID, str], CommandResult] = field(default_factory=dict)

    def get(self, organization_id: UUID, brand_id: UUID, idempotency_key: str) -> CommandResult | None:
        return self.records.get((organization_id, brand_id, idempotency_key))

    def put(
        self,
        organization_id: UUID,
        brand_id: UUID,
        idempotency_key: str,
        result: CommandResult,
    ) -> None:
        self.records[(organization_id, brand_id, idempotency_key)] = result


@dataclass
class InMemoryBrandRepository:
    scopes: set[tuple[UUID, UUID]] = field(default_factory=set)

    def add_scope(self, organization_id: UUID, brand_id: UUID) -> None:
        self.scopes.add((organization_id, brand_id))

    def contains_scope(self, organization_id: UUID, brand_id: UUID) -> bool:
        return (organization_id, brand_id) in self.scopes

