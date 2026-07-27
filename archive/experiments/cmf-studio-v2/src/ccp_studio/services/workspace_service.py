"""Organization and brand workspace lifecycle service for TS-CMF-004."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.workspace_lifecycle import (
    ActiveBrandContext,
    BrandScopedObject,
    BrandWorkspace,
    RetentionPolicy,
    RoleAssignment,
    WorkspaceInspectionSnapshot,
    WorkspaceReceipt,
    WorkspaceStatus,
    new_brand_workspace,
    new_organization,
    new_workspace_lifecycle_event,
)
from ccp_studio.domain.policies.workspace_lifecycle_policy import (
    WorkspaceLifecyclePolicy,
    WorkspacePolicyError,
)
from ccp_studio.repositories.brand_workspaces import (
    InMemoryActiveBrandContextRepository,
    InMemoryBrandObjectRepository,
    InMemoryBrandWorkspaceRepository,
    InMemoryRetentionPolicyRepository,
    InMemoryRoleAssignmentRepository,
    InMemoryWorkspaceEventRepository,
    InMemoryWorkspaceReceiptRepository,
)
from ccp_studio.repositories.command_log import InMemoryBrandRepository
from ccp_studio.repositories.organizations import InMemoryOrganizationRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.contracts.orchestration import utc_now


class WorkspaceServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class WorkspaceCreateResult:
    organization_id: UUID
    brand_id: UUID
    retention_policy_id: UUID
    role_assignment_id: UUID
    lifecycle_event_id: UUID
    workspace_receipt_id: UUID


@dataclass
class WorkspaceService:
    organizations: InMemoryOrganizationRepository = field(default_factory=InMemoryOrganizationRepository)
    workspaces: InMemoryBrandWorkspaceRepository = field(default_factory=InMemoryBrandWorkspaceRepository)
    role_assignments: InMemoryRoleAssignmentRepository = field(default_factory=InMemoryRoleAssignmentRepository)
    retention_policies: InMemoryRetentionPolicyRepository = field(default_factory=InMemoryRetentionPolicyRepository)
    active_contexts: InMemoryActiveBrandContextRepository = field(default_factory=InMemoryActiveBrandContextRepository)
    lifecycle_events: InMemoryWorkspaceEventRepository = field(default_factory=InMemoryWorkspaceEventRepository)
    workspace_receipts: InMemoryWorkspaceReceiptRepository = field(default_factory=InMemoryWorkspaceReceiptRepository)
    brand_objects: InMemoryBrandObjectRepository = field(default_factory=InMemoryBrandObjectRepository)
    policy: WorkspaceLifecyclePolicy = field(default_factory=WorkspaceLifecyclePolicy)

    def create_organization_with_brand(
        self,
        *,
        actor_id: UUID,
        role_ids: list[str],
        organization_id: UUID,
        organization_name: str,
        brand_id: UUID,
        brand_display_name: str,
        command_id: UUID | None = None,
    ) -> WorkspaceCreateResult:
        self.policy.require_owner_or_admin(role_ids)
        retention_policy = RetentionPolicy(
            schema_version="cmf.retention_policy.v1",
            retention_policy_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            policy_name="default",
            retention_days=365,
            created_at=utc_now(),
        )
        organization = new_organization(
            organization_id=organization_id,
            name=organization_name,
        )
        workspace = new_brand_workspace(
            organization_id=organization_id,
            brand_id=brand_id,
            display_name=brand_display_name,
            default_retention_policy_id=retention_policy.retention_policy_id,
        )
        assignment = RoleAssignment(
            schema_version="cmf.role_assignment.v1",
            role_assignment_id=uuid4(),
            actor_id=actor_id,
            organization_id=organization_id,
            brand_id=brand_id,
            role="owner",
            active=True,
            created_at=utc_now(),
        )
        event = new_workspace_lifecycle_event(
            organization_id=organization_id,
            brand_id=brand_id,
            event_type="BrandWorkspaceCreated",
            actor_id=actor_id,
            command_id=command_id,
        )
        receipt = self._workspace_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            action="CreateBrandWorkspaceCommand",
            status=WorkspaceStatus.active,
            decision="workspace_created",
            lifecycle_event_id=event.lifecycle_event_id,
            command_id=command_id,
            evidence_refs=[
                f"organization:{organization_id}",
                f"brand_workspace:{brand_id}",
                f"role_assignment:{assignment.role_assignment_id}",
                f"retention_policy:{retention_policy.retention_policy_id}",
            ],
        )
        self.organizations.put(organization)
        self.retention_policies.put(retention_policy)
        self.workspaces.put(workspace)
        self.role_assignments.put(assignment)
        self.lifecycle_events.put(event)
        self.workspace_receipts.put(receipt)
        return WorkspaceCreateResult(
            organization_id=organization_id,
            brand_id=brand_id,
            retention_policy_id=retention_policy.retention_policy_id,
            role_assignment_id=assignment.role_assignment_id,
            lifecycle_event_id=event.lifecycle_event_id,
            workspace_receipt_id=receipt.workspace_receipt_id,
        )

    def transition_workspace(
        self,
        *,
        actor_id: UUID,
        role_ids: list[str],
        organization_id: UUID,
        brand_id: UUID,
        target_status: WorkspaceStatus,
        action: str,
        command_id: UUID | None = None,
    ) -> WorkspaceReceipt:
        self.policy.require_owner_or_admin(role_ids)
        workspace = self._require_workspace(organization_id, brand_id)
        self.policy.validate_transition(workspace.status, target_status)
        workspace.status = target_status
        workspace.updated_at = utc_now()
        event_type = {
            WorkspaceStatus.suspended: "BrandWorkspaceSuspended",
            WorkspaceStatus.archived: "BrandWorkspaceArchived",
            WorkspaceStatus.restoring: "BrandWorkspaceRestoreStarted",
            WorkspaceStatus.active: "BrandWorkspaceRestored",
        }[target_status]
        event = new_workspace_lifecycle_event(
            organization_id=organization_id,
            brand_id=brand_id,
            event_type=event_type,
            actor_id=actor_id,
            command_id=command_id,
        )
        receipt = self._workspace_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            action=action,
            status=target_status,
            decision=event_type,
            lifecycle_event_id=event.lifecycle_event_id,
            command_id=command_id,
            evidence_refs=[f"workspace_status:{target_status.value}"],
        )
        self.workspaces.put(workspace)
        self.lifecycle_events.put(event)
        return self.workspace_receipts.put(receipt)

    def restore_archived_workspace(
        self,
        *,
        actor_id: UUID,
        role_ids: list[str],
        organization_id: UUID,
        brand_id: UUID,
        command_id: UUID | None = None,
    ) -> WorkspaceReceipt:
        start = self.transition_workspace(
            actor_id=actor_id,
            role_ids=role_ids,
            organization_id=organization_id,
            brand_id=brand_id,
            target_status=WorkspaceStatus.restoring,
            action="RestoreBrandWorkspaceCommand",
            command_id=command_id,
        )
        self.transition_workspace(
            actor_id=actor_id,
            role_ids=role_ids,
            organization_id=organization_id,
            brand_id=brand_id,
            target_status=WorkspaceStatus.active,
            action="RestoreBrandWorkspaceCommand",
            command_id=command_id,
        )
        return start

    def switch_active_brand_context(
        self,
        *,
        actor_id: UUID,
        role_ids: list[str],
        organization_id: UUID,
        brand_id: UUID,
        source_surface: str,
        command_id: UUID | None = None,
    ) -> ActiveBrandContext:
        self.policy.require_read_access(role_ids)
        workspace = self._require_workspace(organization_id, brand_id)
        self.policy.require_mutation_allowed(workspace.status)
        context = ActiveBrandContext(
            schema_version="cmf.active_brand_context.v1",
            actor_id=actor_id,
            organization_id=organization_id,
            brand_id=brand_id,
            selected_at=utc_now(),
            source_surface=source_surface,
        )
        event = new_workspace_lifecycle_event(
            organization_id=organization_id,
            brand_id=brand_id,
            event_type="ActiveBrandContextSwitched",
            actor_id=actor_id,
            command_id=command_id,
        )
        self.active_contexts.put(context)
        self.lifecycle_events.put(event)
        return context

    def inspect_workspace(
        self,
        *,
        actor_id: UUID,
        role_ids: list[str],
        organization_id: UUID,
        brand_id: UUID,
    ) -> WorkspaceInspectionSnapshot:
        self.policy.require_read_access(role_ids)
        workspace = self._require_workspace(organization_id, brand_id)
        last_receipt = self.workspace_receipts.latest_for_brand(organization_id, brand_id)
        blockers: list[str] = []
        if workspace.status == WorkspaceStatus.suspended:
            blockers.append("workspace_suspended")
        if workspace.status == WorkspaceStatus.archived:
            blockers.append("workspace_archived")
        return WorkspaceInspectionSnapshot(
            schema_version="cmf.workspace_inspection_snapshot.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            status=workspace.status,
            active_role_count=len(self.role_assignments.active_for_brand(organization_id, brand_id)),
            entitlement_state="pending-commercial-policy",
            recent_command_ids=self.lifecycle_events.recent_command_ids(organization_id, brand_id),
            open_blockers=blockers,
            production_health="blocked" if blockers else "ready",
            last_receipt_id=last_receipt.workspace_receipt_id if last_receipt else None,
        )

    def require_production_mutation_allowed(self, organization_id: UUID, brand_id: UUID) -> None:
        workspace = self._require_workspace(organization_id, brand_id)
        try:
            self.policy.require_mutation_allowed(workspace.status)
        except WorkspacePolicyError as exc:
            raise WorkspaceServiceError(exc.code, exc.message) from exc

    def query_brand_objects(
        self,
        *,
        organization_id: UUID,
        active_brand_id: UUID,
        requested_brand_id: UUID,
        permitted_brand_ids: set[UUID] | None = None,
    ) -> list[BrandScopedObject]:
        return self.brand_objects.query_visible(
            organization_id=organization_id,
            active_brand_id=active_brand_id,
            requested_brand_id=requested_brand_id,
            permitted_brand_ids=permitted_brand_ids or {active_brand_id},
        )

    @staticmethod
    def brand_storage_path(brand_id: UUID, content_hash: str, *parts: str) -> str:
        safe_parts = "/".join(part.strip("/").replace("..", "") for part in parts if part)
        return f"brands/{brand_id}/{content_hash}/{safe_parts}".rstrip("/")

    def _workspace_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        action: str,
        status: WorkspaceStatus,
        decision: str,
        lifecycle_event_id: UUID | None,
        command_id: UUID | None,
        evidence_refs: list[str],
    ) -> WorkspaceReceipt:
        return WorkspaceReceipt(
            schema_version="cmf.workspace_receipt.v1",
            workspace_receipt_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            action=action,
            status=status,
            decision=decision,
            lifecycle_event_id=lifecycle_event_id,
            command_id=command_id,
            evidence_refs=evidence_refs,
            written_at=utc_now(),
        )

    def _require_workspace(self, organization_id: UUID, brand_id: UUID) -> BrandWorkspace:
        workspace = self.workspaces.get(organization_id, brand_id)
        if workspace is None:
            raise WorkspaceServiceError("NOT_FOUND", "Workspace not found.")
        return workspace


@dataclass
class WorkspaceCommandHandler:
    command_type: str
    workspace_service: WorkspaceService
    brand_scope_registry: InMemoryBrandRepository
    aggregate_type: str = "brand_workspace"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        role_ids = envelope.actor.role_ids
        if self.command_type == "CreateBrandWorkspaceCommand":
            result = self.workspace_service.create_organization_with_brand(
                actor_id=envelope.actor.actor_id,
                role_ids=role_ids,
                organization_id=envelope.organization_id,
                organization_name=payload["organization_name"],
                brand_id=envelope.brand_id,
                brand_display_name=payload["brand_display_name"],
                command_id=envelope.command_id,
            )
            self.brand_scope_registry.add_scope(envelope.organization_id, envelope.brand_id)
            return result.__dict__
        if self.command_type == "SuspendBrandWorkspaceCommand":
            receipt = self.workspace_service.transition_workspace(
                actor_id=envelope.actor.actor_id,
                role_ids=role_ids,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                target_status=WorkspaceStatus.suspended,
                action=self.command_type,
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "ArchiveBrandWorkspaceCommand":
            receipt = self.workspace_service.transition_workspace(
                actor_id=envelope.actor.actor_id,
                role_ids=role_ids,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                target_status=WorkspaceStatus.archived,
                action=self.command_type,
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "RestoreBrandWorkspaceCommand":
            receipt = self.workspace_service.restore_archived_workspace(
                actor_id=envelope.actor.actor_id,
                role_ids=role_ids,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                command_id=envelope.command_id,
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "SwitchActiveBrandContextCommand":
            context = self.workspace_service.switch_active_brand_context(
                actor_id=envelope.actor.actor_id,
                role_ids=role_ids,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                source_surface=payload.get("source_surface", envelope.source_surface),
                command_id=envelope.command_id,
            )
            return context.model_dump(mode="json")
        if self.command_type == "InspectBrandWorkspaceCommand":
            snapshot = self.workspace_service.inspect_workspace(
                actor_id=envelope.actor.actor_id,
                role_ids=role_ids,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
            )
            return snapshot.model_dump(mode="json")
        raise WorkspaceServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("brand_id") or payload.get("brand_id".upper())
        if isinstance(raw, UUID):
            return raw
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_workspace_command_handlers(bus: CommandBus, service: WorkspaceService) -> None:
    bus.register_handler(
        WorkspaceCommandHandler(
            command_type="CreateBrandWorkspaceCommand",
            workspace_service=service,
            brand_scope_registry=bus.brands,
            requires_existing_brand_scope=False,
        )
    )
    for command_type in [
        "SuspendBrandWorkspaceCommand",
        "ArchiveBrandWorkspaceCommand",
        "RestoreBrandWorkspaceCommand",
    ]:
        bus.register_handler(
            WorkspaceCommandHandler(
                command_type=command_type,
                workspace_service=service,
                brand_scope_registry=bus.brands,
            )
        )
    bus.register_handler(
        WorkspaceCommandHandler(
            command_type="SwitchActiveBrandContextCommand",
            workspace_service=service,
            brand_scope_registry=bus.brands,
            allowed_roles={"owner", "admin", "operator"},
        )
    )
    bus.register_handler(
        WorkspaceCommandHandler(
            command_type="InspectBrandWorkspaceCommand",
            workspace_service=service,
            brand_scope_registry=bus.brands,
            allowed_roles={"owner", "admin", "operator", "auditor"},
        )
    )
