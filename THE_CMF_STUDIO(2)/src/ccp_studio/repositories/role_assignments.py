"""Role assignment repositories for TS-CMF-005."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.roles import (
    MigrationApprovalReceipt,
    RoleAssignment,
    RoleAssignmentReceipt,
    RoleAssignmentStatus,
    RoleKey,
)


@dataclass
class InMemoryRolePolicyRepository:
    assignments: dict[UUID, RoleAssignment] = field(default_factory=dict)
    assignment_receipts: dict[UUID, RoleAssignmentReceipt] = field(default_factory=dict)
    migration_receipts: dict[UUID, MigrationApprovalReceipt] = field(default_factory=dict)

    def put_assignment(self, assignment: RoleAssignment) -> RoleAssignment:
        self.assignments[assignment.role_assignment_id] = assignment
        return assignment

    def get_assignment(self, role_assignment_id: UUID) -> RoleAssignment | None:
        return self.assignments.get(role_assignment_id)

    def assignments_for_actor(
        self,
        actor_id: UUID,
        organization_id: UUID,
        brand_id: UUID | None,
        *,
        statuses: set[RoleAssignmentStatus],
    ) -> list[RoleAssignment]:
        return [
            assignment
            for assignment in self.assignments.values()
            if assignment.actor_id == actor_id
            and assignment.organization_id == organization_id
            and assignment.status in statuses
            and (brand_id is None or assignment.brand_id == brand_id)
        ]

    def active_role_keys(self, actor_id: UUID, organization_id: UUID, brand_id: UUID | None) -> set[RoleKey]:
        return {
            assignment.role_key
            for assignment in self.assignments_for_actor(
                actor_id,
                organization_id,
                brand_id,
                statuses={RoleAssignmentStatus.active},
            )
        }

    def put_assignment_receipt(self, receipt: RoleAssignmentReceipt) -> RoleAssignmentReceipt:
        self.assignment_receipts[receipt.role_assignment_receipt_id] = receipt
        return receipt

    def put_migration_receipt(self, receipt: MigrationApprovalReceipt) -> MigrationApprovalReceipt:
        self.migration_receipts[receipt.migration_approval_receipt_id] = receipt
        return receipt
