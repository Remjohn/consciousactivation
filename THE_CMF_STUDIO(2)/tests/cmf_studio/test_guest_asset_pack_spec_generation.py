from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_archetype_and_asset_derivative_routing import _routing_fixture  # noqa: E402

from ccp_studio.contracts.asset_package import PackageItemStatus, PackageItemType, TARGET_TRIAL_GUEST_PACK_COUNTS  # noqa: E402
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.commercial import PublicContentOffer  # noqa: E402
from ccp_studio.services.asset_package_service import AssetPackageService, register_asset_package_command_handlers  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.commercial_policy_service import CommercialPolicyService  # noqa: E402
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _package_fixture(route_count=13):
    routing, review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, moment_id = _routing_fixture()
    commercial = CommercialPolicyService()
    commercial.create_entitlement(
        organization_id=org_id,
        brand_id=brand_id,
        public_offer=PublicContentOffer.trial_guest_asset_pack,
    )
    route_receipts = [
        routing.route_expression_moment(
            organization_id=org_id,
            brand_id=brand_id,
            expression_moment_id=moment_id,
            actor_id=actor_id,
        )
        for _index in range(route_count)
    ]
    package_service = AssetPackageService(routing, commercial)
    return (
        package_service,
        routing,
        review,
        extraction,
        source_service,
        session_service,
        commercial,
        org_id,
        brand_id,
        actor_id,
        session,
        route_receipts,
    )


def _ready_items(spec):
    return [item for item in spec.items if item.production_readiness == PackageItemStatus.ready_for_editing_session]


def test_trial_pack_targets_standard_counts_when_source_supports_them():
    package_service, _routing, _review, _extraction, _source, _session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture()

    spec = package_service.generate_trial_guest_asset_pack_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in receipts],
        actor_id=actor_id,
    )
    ready_counts = {item_type: 0 for item_type in TARGET_TRIAL_GUEST_PACK_COUNTS}
    for item in _ready_items(spec):
        ready_counts[item.item_type] += 1

    assert ready_counts[PackageItemType.short_video] == 4
    assert ready_counts[PackageItemType.carousel] == 2
    assert ready_counts[PackageItemType.meme_visual] == 2
    assert ready_counts[PackageItemType.poll_visual] == 2
    assert ready_counts[PackageItemType.reaction_seed] == 3
    assert len(spec.reaction_seeds) == 3
    assert not spec.gaps


def test_unsupported_source_creates_gap_instead_of_fabricated_item():
    package_service, _routing, _review, _extraction, _source, _session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture(route_count=1)

    spec = package_service.generate_trial_guest_asset_pack_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in receipts],
        actor_id=actor_id,
    )

    assert len(_ready_items(spec)) == 1
    assert spec.gaps
    assert any(item.production_readiness == PackageItemStatus.source_gap for item in spec.items)
    assert all(item.expression_moment_id is None for item in spec.items if item.production_readiness == PackageItemStatus.source_gap)


def test_each_ready_package_item_maps_to_moment_route_registry_brand_context_evaluation_and_readiness():
    package_service, _routing, _review, _extraction, _source, _session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture(route_count=3)

    spec = package_service.generate_trial_guest_asset_pack_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in receipts],
        actor_id=actor_id,
    )

    for item in _ready_items(spec):
        assert item.expression_moment_id
        assert item.asset_route_receipt_id
        assert item.registry_refs
        assert item.brand_context_required is True
        assert item.evaluation_state == "route_receipt_passed_pending_render_eval"
        assert item.production_readiness == PackageItemStatus.ready_for_editing_session


def test_trial_pack_language_uses_29_week_only():
    package_service, _routing, _review, _extraction, _source, _session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture(route_count=1)

    spec = package_service.generate_trial_guest_asset_pack_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in receipts],
        actor_id=actor_id,
    )

    assert "$29/week" in spec.customer_facing_price_label
    assert "$99/month" not in spec.customer_facing_price_label
    assert "newsletter" not in spec.customer_facing_price_label.lower()


def test_approved_package_prepares_editing_session_requests_with_lineage():
    package_service, _routing, _review, _extraction, _source, _session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture(route_count=2)
    spec = package_service.generate_trial_guest_asset_pack_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in receipts],
        actor_id=actor_id,
    )
    approved = package_service.approve_asset_package_spec(
        asset_package_spec_id=spec.asset_package_spec_id,
        actor_id=actor_id,
    )

    requests = package_service.prepare_editing_session_requests(
        asset_package_spec_id=approved.asset_package_spec_id,
        actor_id=actor_id,
    )

    assert requests
    assert requests[0].expression_moment_id
    assert requests[0].asset_route_receipt_id
    assert requests[0].registry_refs
    assert requests[0].route_state == "ASSET_ROUTE_ACCEPTED"
    assert any(ref.startswith("asset_route_receipt:") for ref in requests[0].source_lineage_refs)


def test_workflow_stage8_generates_asset_package_spec():
    package_service, routing, review, extraction, source_service, session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture(route_count=2)
    workflow = CompleteExpressionSessionWorkflow(
        service=session_service,
        source_provenance_service=source_service,
        extraction_service=extraction,
        expression_review_service=review,
        routing_service=routing,
        asset_package_service=package_service,
    )

    spec = workflow.stage8_generate_asset_package_spec(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        asset_route_receipt_ids=[receipt.asset_route_receipt_id for receipt in receipts],
        actor_id=actor_id,
    )

    assert spec.package_spec_receipt_id in package_service.repository.receipts


def test_asset_package_command_bus_emits_package_spec_receipt_event():
    package_service, _routing, _review, _extraction, _source, _session_service, _commercial, org_id, brand_id, actor_id, session, receipts = _package_fixture(route_count=1)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_asset_package_command_handlers(bus, package_service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="GenerateTrialGuestAssetPackSpecCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "expression_session_id": str(session.expression_session_id),
            "asset_route_receipt_ids": [str(receipts[0].asset_route_receipt_id)],
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["package_spec_receipt_id"]
    assert bus.event_outbox.events[-1].event_type == "GenerateTrialGuestAssetPackSpecCommand.succeeded"
