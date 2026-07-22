"""Brand workspace repositories for TS-CMF-004."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.workspace_lifecycle import (
    ActiveBrandContext,
    BrandScopedObject,
    BrandWorkspace,
    RetentionPolicy,
    RoleAssignment,
    WorkspaceLifecycleEvent,
    WorkspaceReceipt,
)


@dataclass
class InMemoryBrandWorkspaceRepository:
    workspaces: dict[tuple[UUID, UUID], BrandWorkspace] = field(default_factory=dict)

    def put(self, workspace: BrandWorkspace) -> BrandWorkspace:
        self.workspaces[(workspace.organization_id, workspace.brand_id)] = workspace
        return workspace

    def get(self, organization_id: UUID, brand_id: UUID) -> BrandWorkspace | None:
        return self.workspaces.get((organization_id, brand_id))


@dataclass
class InMemoryRoleAssignmentRepository:
    assignments: dict[UUID, RoleAssignment] = field(default_factory=dict)

    def put(self, assignment: RoleAssignment) -> RoleAssignment:
        self.assignments[assignment.role_assignment_id] = assignment
        return assignment

    def active_for_brand(self, organization_id: UUID, brand_id: UUID) -> list[RoleAssignment]:
        return [
            assignment
            for assignment in self.assignments.values()
            if assignment.organization_id == organization_id
            and assignment.brand_id == brand_id
            and assignment.active
        ]

    def roles_for_actor(self, actor_id: UUID, organization_id: UUID, brand_id: UUID) -> list[str]:
        return [
            assignment.role
            for assignment in self.active_for_brand(organization_id, brand_id)
            if assignment.actor_id == actor_id
        ]


@dataclass
class InMemoryRetentionPolicyRepository:
    policies: dict[UUID, RetentionPolicy] = field(default_factory=dict)

    def put(self, policy: RetentionPolicy) -> RetentionPolicy:
        self.policies[policy.retention_policy_id] = policy
        return policy


@dataclass
class InMemoryActiveBrandContextRepository:
    contexts: dict[UUID, ActiveBrandContext] = field(default_factory=dict)

    def put(self, context: ActiveBrandContext) -> ActiveBrandContext:
        self.contexts[context.actor_id] = context
        return context

    def get(self, actor_id: UUID) -> ActiveBrandContext | None:
        return self.contexts.get(actor_id)


@dataclass
class InMemoryWorkspaceEventRepository:
    events: dict[UUID, WorkspaceLifecycleEvent] = field(default_factory=dict)

    def put(self, event: WorkspaceLifecycleEvent) -> WorkspaceLifecycleEvent:
        self.events[event.lifecycle_event_id] = event
        return event

    def recent_command_ids(self, organization_id: UUID, brand_id: UUID) -> list[UUID]:
        return [
            event.command_id
            for event in self.events.values()
            if event.organization_id == organization_id
            and event.brand_id == brand_id
            and event.command_id is not None
        ][-10:]


@dataclass
class InMemoryWorkspaceReceiptRepository:
    receipts: dict[UUID, WorkspaceReceipt] = field(default_factory=dict)

    def put(self, receipt: WorkspaceReceipt) -> WorkspaceReceipt:
        self.receipts[receipt.workspace_receipt_id] = receipt
        return receipt

    def latest_for_brand(self, organization_id: UUID, brand_id: UUID) -> WorkspaceReceipt | None:
        matching = [
            receipt
            for receipt in self.receipts.values()
            if receipt.organization_id == organization_id and receipt.brand_id == brand_id
        ]
        if not matching:
            return None
        return max(matching, key=lambda item: item.written_at)


@dataclass
class InMemoryBrandObjectRepository:
    objects: dict[UUID, BrandScopedObject] = field(default_factory=dict)

    def put(self, item: BrandScopedObject) -> BrandScopedObject:
        self.objects[item.object_id] = item
        return item

    def query_visible(
        self,
        *,
        organization_id: UUID,
        active_brand_id: UUID,
        requested_brand_id: UUID,
        permitted_brand_ids: set[UUID],
    ) -> list[BrandScopedObject]:
        if requested_brand_id != active_brand_id and requested_brand_id not in permitted_brand_ids:
            return []
        return [
            item
            for item in self.objects.values()
            if item.organization_id == organization_id and item.brand_id == requested_brand_id
        ]
