"""Role-based production permission service for TS-CMF-005."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.roles import (
    CommandPermission,
    MigrationApprovalReceipt,
    PermissionDecision,
    RoleAssignment,
    RoleAssignmentReceipt,
    RoleAssignmentStatus,
    RoleKey,
    new_permission_decision,
    new_role_assignment,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.role_assignments import InMemoryRolePolicyRepository
from ccp_studio.services.command_bus import CommandBus


DEFAULT_COMMAND_PERMISSIONS = [
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="workspace.lifecycle",
        command_type="AssignRoleCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="workspace.lifecycle",
        command_type="RevokeRoleCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="production.start",
        command_type="StartProductionCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.operator, RoleKey.production_steward],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="production.provider_job",
        command_type="SubmitProviderJobCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.operator, RoleKey.production_steward],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="production.render",
        command_type="QueueRenderCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.operator, RoleKey.production_steward],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="production.asset_package",
        command_type="GenerateAssetPackageSpecCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.operator, RoleKey.production_steward],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="production.publish_intent",
        command_type="PublishIntentCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.publishing_approver],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="service.workflow",
        command_type="RunServiceWorkflowCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.service_actor],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="publishing.approve",
        command_type="ApprovePublishingCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.publishing_approver],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="migration.approve",
        command_type="ApproveMigrationRegistryEntryCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.migration_steward],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="commercial.update",
        command_type="UpdateCommercialPolicyCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.commercial_administrator],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="commercial.entitlement.create",
        command_type="CreateCommercialEntitlementCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.commercial_administrator],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="commercial.entitlement.update",
        command_type="UpdateCommercialEntitlementCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.commercial_administrator],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="commercial.policy.evaluate",
        command_type="EvaluateCommercialPolicyCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.commercial_administrator, RoleKey.operator],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="commercial.usage.record",
        command_type="RecordUsageCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.commercial_administrator, RoleKey.service_actor],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="workspace.inspect",
        command_type="InspectRoleAssignmentsCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.operator, RoleKey.reviewer],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="review.submit",
        command_type="SubmitReviewCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.reviewer],
    ),
    CommandPermission(
        schema_version="cmf.command_permission.v1",
        permission_key="permission.evaluate",
        command_type="EvaluateCommandPermissionCommand",
        allowed_roles=[RoleKey.owner, RoleKey.admin, RoleKey.operator, RoleKey.reviewer],
    ),
]


class RolePolicyError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class RolePolicyService:
    repository: InMemoryRolePolicyRepository = field(default_factory=InMemoryRolePolicyRepository)
    permissions: dict[str, CommandPermission] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.permissions:
            self.permissions = {item.command_type: item for item in DEFAULT_COMMAND_PERMISSIONS}

    def bootstrap_owner(
        self,
        *,
        actor_id: UUID,
        organization_id: UUID,
        brand_id: UUID,
    ) -> RoleAssignment:
        assignment = new_role_assignment(
            actor_id=actor_id,
            organization_id=organization_id,
            brand_id=brand_id,
            role_key=RoleKey.owner,
            assigned_by_actor_id=actor_id,
        )
        self.repository.put_assignment(assignment)
        self._receipt(assignment=assignment, actor_id=actor_id, action="bootstrap_owner", decision="role_assigned")
        return assignment

    def assign_role(
        self,
        *,
        assigner_actor_id: UUID,
        target_actor_id: UUID,
        organization_id: UUID,
        brand_id: UUID,
        role_key: RoleKey,
    ) -> RoleAssignment:
        decision = self.evaluate(
            actor_id=assigner_actor_id,
            command_type="AssignRoleCommand",
            organization_id=organization_id,
            brand_id=brand_id,
            source_surface="internal",
        )
        if not decision.allowed:
            raise RolePolicyError(decision.decision_code, "Assigner lacks permission.")
        assignment = new_role_assignment(
            actor_id=target_actor_id,
            organization_id=organization_id,
            brand_id=brand_id,
            role_key=role_key,
            assigned_by_actor_id=assigner_actor_id,
        )
        self.repository.put_assignment(assignment)
        self._receipt(assignment=assignment, actor_id=assigner_actor_id, action="AssignRoleCommand", decision="role_assigned")
        return assignment

    def revoke_role(
        self,
        *,
        revoker_actor_id: UUID,
        role_assignment_id: UUID,
    ) -> RoleAssignment:
        assignment = self.repository.get_assignment(role_assignment_id)
        if assignment is None:
            raise RolePolicyError("ROLE_ASSIGNMENT_NOT_FOUND", "Role assignment not found.")
        decision = self.evaluate(
            actor_id=revoker_actor_id,
            command_type="RevokeRoleCommand",
            organization_id=assignment.organization_id,
            brand_id=assignment.brand_id,
            source_surface="internal",
        )
        if not decision.allowed:
            raise RolePolicyError(decision.decision_code, "Revoker lacks permission.")
        assignment.status = RoleAssignmentStatus.revoked
        assignment.revoked_at = utc_now()
        self.repository.put_assignment(assignment)
        self._receipt(assignment=assignment, actor_id=revoker_actor_id, action="RevokeRoleCommand", decision="role_revoked")
        return assignment

    def evaluate(
        self,
        *,
        actor_id: UUID,
        command_type: str,
        organization_id: UUID,
        brand_id: UUID | None,
        source_surface: str,
    ) -> PermissionDecision:
        permission = self.permissions.get(command_type)
        if permission is None:
            return new_permission_decision(
                actor_id=actor_id,
                command_type=command_type,
                organization_id=organization_id,
                brand_id=brand_id,
                allowed=False,
                decision_code="PERMISSION_DENIED",
            )
        if permission.allowed_surfaces and source_surface not in permission.allowed_surfaces:
            return new_permission_decision(
                actor_id=actor_id,
                command_type=command_type,
                organization_id=organization_id,
                brand_id=brand_id,
                allowed=False,
                decision_code="SURFACE_NOT_ALLOWED",
            )
        active = self.repository.assignments_for_actor(
            actor_id,
            organization_id,
            brand_id if permission.requires_brand_scope else None,
            statuses={RoleAssignmentStatus.active},
        )
        matching = [
            assignment
            for assignment in active
            if assignment.role_key in permission.allowed_roles
        ]
        if matching:
            return new_permission_decision(
                actor_id=actor_id,
                command_type=command_type,
                organization_id=organization_id,
                brand_id=brand_id,
                allowed=True,
                decision_code="PERMISSION_ALLOWED",
                matched_role_assignment_ids=[item.role_assignment_id for item in matching],
            )
        revoked = self.repository.assignments_for_actor(
            actor_id,
            organization_id,
            brand_id if permission.requires_brand_scope else None,
            statuses={RoleAssignmentStatus.revoked},
        )
        if any(item.role_key in permission.allowed_roles for item in revoked):
            return new_permission_decision(
                actor_id=actor_id,
                command_type=command_type,
                organization_id=organization_id,
                brand_id=brand_id,
                allowed=False,
                decision_code="ROLE_REVOKED",
            )
        return new_permission_decision(
            actor_id=actor_id,
            command_type=command_type,
            organization_id=organization_id,
            brand_id=brand_id,
            allowed=False,
            decision_code="PERMISSION_DENIED",
        )

    def approve_migration_registry_entry(
        self,
        *,
        reviewer_actor_id: UUID,
        organization_id: UUID,
        brand_id: UUID,
        source_hash: str,
        target_contract: str,
        fixture_target: str,
        eval_target: str,
    ) -> MigrationApprovalReceipt:
        for field_name, value in {
            "source_hash": source_hash,
            "target_contract": target_contract,
            "fixture_target": fixture_target,
            "eval_target": eval_target,
        }.items():
            if not value:
                raise RolePolicyError("MIGRATION_RECEIPT_INCOMPLETE", f"{field_name} is required.")
        decision = self.evaluate(
            actor_id=reviewer_actor_id,
            command_type="ApproveMigrationRegistryEntryCommand",
            organization_id=organization_id,
            brand_id=brand_id,
            source_surface="internal",
        )
        if not decision.allowed:
            raise RolePolicyError(decision.decision_code, "Migration approval denied.")
        receipt = MigrationApprovalReceipt(
            schema_version="cmf.migration_approval_receipt.v1",
            migration_approval_receipt_id=uuid4(),
            reviewer_actor_id=reviewer_actor_id,
            organization_id=organization_id,
            brand_id=brand_id,
            source_hash=source_hash,
            target_contract=target_contract,
            fixture_target=fixture_target,
            eval_target=eval_target,
            role_assignment_id=decision.matched_role_assignment_ids[0],
            written_at=utc_now(),
        )
        return self.repository.put_migration_receipt(receipt)

    def _receipt(
        self,
        *,
        assignment: RoleAssignment,
        actor_id: UUID,
        action: str,
        decision: str,
    ) -> RoleAssignmentReceipt:
        receipt = RoleAssignmentReceipt(
            schema_version="cmf.role_assignment_receipt.v1",
            role_assignment_receipt_id=uuid4(),
            role_assignment_id=assignment.role_assignment_id,
            organization_id=assignment.organization_id,
            brand_id=assignment.brand_id,
            actor_id=actor_id,
            action=action,
            decision=decision,
            written_at=utc_now(),
        )
        return self.repository.put_assignment_receipt(receipt)


@dataclass
class RoleCommandHandler:
    command_type: str
    role_policy: RolePolicyService
    aggregate_type: str = "role_assignment"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "AssignRoleCommand":
            assignment = self.role_policy.assign_role(
                assigner_actor_id=envelope.actor.actor_id,
                target_actor_id=UUID(payload["target_actor_id"]),
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                role_key=RoleKey(payload["role_key"]),
            )
            return assignment.model_dump(mode="json")
        if self.command_type == "RevokeRoleCommand":
            assignment = self.role_policy.revoke_role(
                revoker_actor_id=envelope.actor.actor_id,
                role_assignment_id=UUID(payload["role_assignment_id"]),
            )
            return assignment.model_dump(mode="json")
        if self.command_type == "InspectRoleAssignmentsCommand":
            assignments = [
                item.model_dump(mode="json")
                for item in self.role_policy.repository.assignments.values()
                if item.organization_id == envelope.organization_id
                and item.brand_id == envelope.brand_id
            ]
            return {"assignments": assignments}
        if self.command_type == "EvaluateCommandPermissionCommand":
            decision = self.role_policy.evaluate(
                actor_id=UUID(payload["target_actor_id"]),
                command_type=payload["command_type"],
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                source_surface=payload.get("source_surface", envelope.source_surface),
            )
            return decision.model_dump(mode="json")
        raise RolePolicyError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("role_assignment_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_role_command_handlers(bus: CommandBus, role_policy: RolePolicyService) -> None:
    bus.permission_policy = role_policy
    for command_type in [
        "AssignRoleCommand",
        "RevokeRoleCommand",
        "InspectRoleAssignmentsCommand",
        "EvaluateCommandPermissionCommand",
    ]:
        bus.register_handler(
            RoleCommandHandler(
                command_type=command_type,
                role_policy=role_policy,
            )
        )
