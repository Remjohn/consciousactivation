from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_guest_asset_pack_spec_generation import _package_fixture  # noqa: E402

from ccp_studio.contracts.brand_context import BrandContextAssetBundle, BrandContextStatus, BrandContextVersion  # noqa: E402
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.complete_editing_session import CompleteEditingSessionStatus  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.repositories.acting_library import InMemoryActingLibraryRepository  # noqa: E402
from ccp_studio.repositories.creative_library_items import InMemoryCreativeLibraryRepository  # noqa: E402
from ccp_studio.repositories.rig_manifests import InMemoryRigManifestRepository  # noqa: E402
from ccp_studio.services.brand_context_service import BrandContextService  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.complete_editing_session_service import (  # noqa: E402
    CompleteEditingSessionService,
    CompleteEditingSessionServiceError,
    register_complete_editing_session_command_handlers,
)
from ccp_studio.workflows.complete_editing_session import CompleteEditingSessionWorkflow  # noqa: E402


def _locked_brand_context_service(org_id, brand_id, actor_id, *, status=BrandContextStatus.locked):
    service = BrandContextService(
        InMemoryActingLibraryRepository(),
        InMemoryRigManifestRepository(),
        InMemoryCreativeLibraryRepository(),
    )
    version = BrandContextVersion(
        schema_version="cmf.brand_context_version.v1",
        brand_context_version_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=uuid4(),
        status=status,
        version_hash=f"brand-context-hash:{status.value}",
        asset_bundle=BrandContextAssetBundle(
            schema_version="cmf.brand_context_asset_bundle.v1",
            acting_library_version_id=uuid4(),
            rig_manifest_id=uuid4(),
            creative_library_receipt_ids=[uuid4()],
            evaluation_receipt_ids=[uuid4()],
        ),
        clearance_certificate_id=uuid4() if status == BrandContextStatus.locked else None,
        created_by_actor_id=actor_id,
        locked_by_actor_id=actor_id if status == BrandContextStatus.locked else None,
        created_at=utc_now(),
        updated_at=utc_now(),
        locked_at=utc_now() if status == BrandContextStatus.locked else None,
    )
    service.repository.put_version(version)
    return service, version


def _editing_fixture(route_count=2):
    package_service, routing, review, extraction, source_service, session_service, _commercial, org_id, brand_id, actor_id, session, route_receipts = _package_fixture(route_count=route_count)
    spec = package_service.generate_trial_guest_asset_pack_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in route_receipts],
        actor_id=actor_id,
    )
    approved = package_service.approve_asset_package_spec(asset_package_spec_id=spec.asset_package_spec_id, actor_id=actor_id)
    requests = package_service.prepare_editing_session_requests(
        asset_package_spec_id=approved.asset_package_spec_id,
        actor_id=actor_id,
    )
    brand_context, locked_context = _locked_brand_context_service(org_id, brand_id, actor_id)
    service = CompleteEditingSessionService(
        expression_review_service=review,
        routing_service=routing,
        brand_context_service=brand_context,
        asset_package_service=package_service,
    )
    return service, package_service, routing, review, org_id, brand_id, actor_id, session, route_receipts, requests, locked_context


def test_session_binds_source_route_package_item_locked_context_actor_brand_and_status():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, locked_context = _editing_fixture()

    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        source_expression_moment_id=requests[0].expression_moment_id,
        asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
        asset_package_item_id=requests[0].package_item_id,
        brand_context_version_id=locked_context.brand_context_version_id,
        actor_id=actor_id,
    )

    assert session.source_expression_moment_id == requests[0].expression_moment_id
    assert session.asset_route_receipt_id == route_receipts[0].asset_route_receipt_id
    assert session.asset_package_item_id == requests[0].package_item_id
    assert session.brand_context_version_id == locked_context.brand_context_version_id
    assert session.brand_context_version_hash == locked_context.version_hash
    assert session.created_by_user_id == actor_id
    assert session.brand_id == brand_id
    assert session.status == CompleteEditingSessionStatus.created


def test_missing_moment_approval_fails_and_writes_blocked_receipt():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, _requests, locked_context = _editing_fixture()

    with pytest.raises(Exception):
        service.create_session(
            organization_id=org_id,
            brand_id=brand_id,
            source_expression_moment_id=uuid4(),
            asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
            brand_context_version_id=locked_context.brand_context_version_id,
            actor_id=actor_id,
        )

    assert list(service.repository.receipts.values())[-1].decision_code == "EDITING_SESSION_CREATION_BLOCKED"


def test_unlocked_or_stale_brand_context_fails():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, _locked_context = _editing_fixture()
    draft_context_service, draft = _locked_brand_context_service(org_id, brand_id, actor_id, status=BrandContextStatus.draft)
    service.brand_context_service = draft_context_service

    with pytest.raises(Exception):
        service.create_session(
            organization_id=org_id,
            brand_id=brand_id,
            source_expression_moment_id=requests[0].expression_moment_id,
            asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
            brand_context_version_id=draft.brand_context_version_id,
            actor_id=actor_id,
        )

    assert list(service.repository.receipts.values())[-1].decision_code == "EDITING_SESSION_CREATION_BLOCKED"


def test_creation_writes_status_event_and_editing_session_receipt():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, locked_context = _editing_fixture()

    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        source_expression_moment_id=requests[0].expression_moment_id,
        asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
        brand_context_version_id=locked_context.brand_context_version_id,
        actor_id=actor_id,
    )

    assert any(event.complete_editing_session_id == session.complete_editing_session_id for event in service.repository.status_events.values())
    receipt = next(item for item in service.repository.receipts.values() if item.complete_editing_session_id == session.complete_editing_session_id)
    assert receipt.decision_code == "COMPLETE_EDITING_SESSION_CREATED"


def test_query_displays_source_route_brand_context_and_readiness():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, locked_context = _editing_fixture()
    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        source_expression_moment_id=requests[0].expression_moment_id,
        asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
        asset_package_item_id=requests[0].package_item_id,
        brand_context_version_id=locked_context.brand_context_version_id,
        actor_id=actor_id,
    )

    model = service.read_model(session.complete_editing_session_id)

    assert model.source_refs
    assert model.registry_refs
    assert model.brand_context_version_id == locked_context.brand_context_version_id
    assert model.production_readiness == "scene_spec_pending"


def test_workflow_stage9_creates_session_after_receipt_persistence():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, locked_context = _editing_fixture()
    workflow = CompleteEditingSessionWorkflow(service)

    session = workflow.stage9_create_session(
        organization_id=org_id,
        brand_id=brand_id,
        source_expression_moment_id=requests[0].expression_moment_id,
        asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
        asset_package_item_id=requests[0].package_item_id,
        brand_context_version_id=locked_context.brand_context_version_id,
        actor_id=actor_id,
    )

    assert session.complete_editing_session_id in service.repository.sessions
    assert any(event.next_status == CompleteEditingSessionStatus.scene_spec_pending for event in service.repository.status_events.values())


def test_complete_editing_session_command_bus_emits_receipt_event():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, locked_context = _editing_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_complete_editing_session_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="CreateCompleteEditingSessionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "source_expression_moment_id": str(requests[0].expression_moment_id),
            "asset_route_receipt_id": str(route_receipts[0].asset_route_receipt_id),
            "asset_package_item_id": str(requests[0].package_item_id),
            "brand_context_version_id": str(locked_context.brand_context_version_id),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["complete_editing_session_id"]
    assert bus.event_outbox.events[-1].event_type == "CreateCompleteEditingSessionCommand.succeeded"
