from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.workspace_lifecycle import BrandScopedObject, WorkspaceStatus
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.workspace_service import (
    WorkspaceService,
    WorkspaceServiceError,
    register_workspace_command_handlers,
)


def _actor(role: str = "owner"):
    return ActorContext(
        actor_id=uuid4(),
        actor_type=ActorType.human,
        role_ids=[role],
    )


def _workspace_fixture():
    service = WorkspaceService()
    bus = create_in_memory_command_bus()
    register_workspace_command_handlers(bus, service)
    org_id = uuid4()
    brand_id = uuid4()
    actor = _actor("owner")
    envelope = new_command_envelope(
        command_type="CreateBrandWorkspaceCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "organization_name": "CMF Studio Test Org",
            "brand_display_name": "Signal Brand",
        },
    )
    result = bus.submit(envelope)
    assert result.status == CommandStatus.succeeded
    return service, bus, org_id, brand_id, actor


def test_create_brand_workspace_command_writes_foundation_records_and_receipts():
    service, bus, org_id, brand_id, _actor_context = _workspace_fixture()

    workspace = service.workspaces.get(org_id, brand_id)

    assert service.organizations.get(org_id) is not None
    assert workspace is not None
    assert workspace.status == WorkspaceStatus.active
    assert len(service.role_assignments.active_for_brand(org_id, brand_id)) == 1
    assert len(service.retention_policies.policies) == 1
    assert len(service.lifecycle_events.events) == 1
    assert len(service.workspace_receipts.receipts) == 1
    assert bus.brands.contains_scope(org_id, brand_id)
    assert len(bus.event_outbox.events) == 1
    assert len(bus.audit_receipts.receipts) == 1


def test_suspended_workspace_blocks_mutation_but_allows_audit_inspection():
    service, bus, org_id, brand_id, actor = _workspace_fixture()
    suspend = new_command_envelope(
        command_type="SuspendBrandWorkspaceCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
    )

    result = bus.submit(suspend)

    assert result.status == CommandStatus.succeeded
    with pytest.raises(WorkspaceServiceError) as exc:
        service.require_production_mutation_allowed(org_id, brand_id)
    assert exc.value.code == "WORKSPACE_SUSPENDED"

    snapshot = service.inspect_workspace(
        actor_id=actor.actor_id,
        role_ids=["auditor"],
        organization_id=org_id,
        brand_id=brand_id,
    )
    assert snapshot.status == WorkspaceStatus.suspended
    assert snapshot.open_blockers == ["workspace_suspended"]
    assert snapshot.production_health == "blocked"


def test_archived_workspace_restore_requires_owner_or_admin_and_writes_receipt():
    service, bus, org_id, brand_id, actor = _workspace_fixture()
    archive = new_command_envelope(
        command_type="ArchiveBrandWorkspaceCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
    )
    bus.submit(archive)

    operator_restore = new_command_envelope(
        command_type="RestoreBrandWorkspaceCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor("operator"),
    )
    rejected = bus.submit(operator_restore)

    assert rejected.status == CommandStatus.rejected
    assert any(item.code == "ROLE_PERMISSION_DENIED" for item in rejected.validation_results)

    owner_restore = new_command_envelope(
        command_type="RestoreBrandWorkspaceCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
    )
    restored = bus.submit(owner_restore)

    assert restored.status == CommandStatus.succeeded
    assert service.workspaces.get(org_id, brand_id).status == WorkspaceStatus.active
    assert len(service.workspace_receipts.receipts) >= 4


def test_active_brand_context_switch_binds_future_workspace_state():
    service, bus, org_id, brand_id, actor = _workspace_fixture()
    switch = new_command_envelope(
        command_type="SwitchActiveBrandContextCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=ActorContext(
            actor_id=actor.actor_id,
            actor_type=ActorType.human,
            role_ids=["operator"],
        ),
        payload={"source_surface": "telegram"},
    )

    result = bus.submit(switch)
    context = service.active_contexts.get(actor.actor_id)

    assert result.status == CommandStatus.succeeded
    assert context is not None
    assert context.brand_id == brand_id
    assert context.source_surface == "telegram"


def test_workspace_inspection_snapshot_contains_roles_entitlements_commands_and_receipts():
    service, bus, org_id, brand_id, actor = _workspace_fixture()
    inspect_command = new_command_envelope(
        command_type="InspectBrandWorkspaceCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=ActorContext(
            actor_id=actor.actor_id,
            actor_type=ActorType.human,
            role_ids=["auditor"],
        ),
    )

    result = bus.submit(inspect_command)
    snapshot = result.result_payload

    assert result.status == CommandStatus.succeeded
    assert snapshot["status"] == "active"
    assert snapshot["active_role_count"] == 1
    assert snapshot["entitlement_state"] == "pending-commercial-policy"
    assert snapshot["recent_command_ids"]
    assert snapshot["last_receipt_id"] is not None


def test_cross_brand_query_returns_no_foreign_object_metadata_without_permission():
    service, _bus, org_id, brand_a, actor = _workspace_fixture()
    brand_b = uuid4()
    service.create_organization_with_brand(
        actor_id=actor.actor_id,
        role_ids=["owner"],
        organization_id=org_id,
        organization_name="CMF Studio Test Org",
        brand_id=brand_b,
        brand_display_name="Hidden Brand",
    )
    foreign_object = BrandScopedObject(
        object_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_b,
        title="Hidden Provider Job",
        preview_uri="brands/hidden/preview.png",
    )
    service.brand_objects.put(foreign_object)

    hidden = service.query_brand_objects(
        organization_id=org_id,
        active_brand_id=brand_a,
        requested_brand_id=brand_b,
        permitted_brand_ids={brand_a},
    )
    visible = service.query_brand_objects(
        organization_id=org_id,
        active_brand_id=brand_a,
        requested_brand_id=brand_b,
        permitted_brand_ids={brand_a, brand_b},
    )

    assert hidden == []
    assert visible[0].object_id == foreign_object.object_id


def test_object_storage_path_guard_includes_brand_id_and_hash():
    brand_id = uuid4()

    path = WorkspaceService.brand_storage_path(
        brand_id,
        "sha256-source",
        "source-artifacts",
        "../master.wav",
    )

    assert path.startswith(f"brands/{brand_id}/sha256-source/")
    assert ".." not in path
