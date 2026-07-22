from __future__ import annotations

import sys
from pathlib import Path
from uuid import UUID, uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_expression_moment_review_and_boundary_control import _review_fixture, _candidate  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.registry import RegistryEntry, RegistryFamily, RegistryStatus  # noqa: E402
from ccp_studio.contracts.routing import RouteDecision  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.migration_service import MigrationService  # noqa: E402
from ccp_studio.services.registry_service import RegistryService  # noqa: E402
from ccp_studio.services.routing_service import RoutingService, register_routing_command_handlers  # noqa: E402
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _entry(registry_type: str, *, name: str, status=RegistryStatus.active, extra: dict | None = None) -> RegistryEntry:
    return RegistryEntry(
        schema_version="cmf.registry_entry.v1",
        registry_entry_id=uuid4(),
        registry_family=RegistryFamily.archetype if registry_type != "cmf_render_mode" else RegistryFamily.creative_subsystem,
        migration_ledger_entry_id=uuid4(),
        source_hash=f"hash:{name}",
        payload={
            "name": name,
            "registry_type": registry_type,
            "route_constraints": ["must preserve source truth"],
            **(extra or {}),
        },
        fixture_set_ids=[uuid4()],
        evaluation_target_ids=[uuid4()],
        known_defects=[],
        reviewer_actor_id=uuid4(),
        status=status,
        created_at=utc_now(),
        updated_at=utc_now(),
    )


def _routing_fixture():
    review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, extraction_receipt = _review_fixture()
    candidate = _candidate((review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, extraction_receipt))
    approval = review.approve_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        reviewer_actor_id=actor_id,
        rationale="Approved for route testing.",
    )
    moment_id = approval.new_expression_moment_ids[0]
    registry_service = RegistryService(MigrationService().repository)
    for entry in [
        _entry("core_content_archetype", name="conceptual contrast"),
        _entry("asset_derivative", name="paper cut explainer", extra={"aliases": ["paper-cut explainer"]}),
        _entry("meme_mechanism", name="micro contradiction"),
        _entry("reaction_archetype", name="validation reaction"),
        _entry("cmf_render_mode", name="paper cut render"),
        _entry("asset_derivative", name="raw legacy prompt filename", status=RegistryStatus.draft, extra={"raw_prompt": "old monolith"}),
    ]:
        registry_service.repository.put_entry(entry)
    routing = RoutingService(review, registry_service)
    return routing, review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, moment_id


def test_routing_evaluates_only_active_migrated_registry_entries():
    routing, _review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()

    receipt = routing.route_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        requested_format="paper-cut explainer",
        actor_id=actor_id,
    )

    assert receipt.decision_code == "ASSET_ROUTE_ACCEPTED"
    assert receipt.accepted_route_ids
    assert all("raw legacy prompt filename" not in ref for ref in receipt.registry_entry_refs)
    assert len(receipt.registry_entry_refs) >= 3


def test_routing_receipt_includes_moment_route_registry_evidence_rationale_and_failures():
    routing, _review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()

    receipt = routing.route_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        actor_id=actor_id,
    )
    route = routing.repository.archetype_routes[receipt.accepted_route_ids[0]]

    assert receipt.expression_moment_id == moment_id
    assert route.archetype_route_id in receipt.accepted_route_ids
    assert receipt.registry_bundle_version.startswith("cmf-routing-bundle:")
    assert receipt.source_support_evidence
    assert receipt.route_rationale
    assert receipt.failure_alternatives


def test_source_insufficient_route_is_rejected_instead_of_fabricated():
    routing, review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()
    moment = review.repository.moments[moment_id]
    weak_receipt = review.supersede_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        reviewer_actor_id=actor_id,
        boundary=moment.boundary,
        source_quote="Okay.",
        rationale="Create weak source moment for route rejection.",
    )
    weak_moment_id = weak_receipt.new_expression_moment_ids[0]

    receipt = routing.route_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=weak_moment_id,
        actor_id=actor_id,
    )
    route = routing.repository.archetype_routes[receipt.rejected_route_ids[0]]

    assert receipt.decision_code == "ROUTE_REJECTED_SOURCE_UNSUPPORTED"
    assert route.decision == RouteDecision.rejected_source_unsupported
    assert not receipt.accepted_route_ids


def test_unsupported_newsletter_format_is_blocked_with_clear_receipt():
    routing, _review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()

    receipt = routing.route_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        requested_format="newsletter",
        actor_id=actor_id,
    )
    rejection = routing.repository.unsupported_format_rejections[receipt.unsupported_format_rejection_ids[0]]

    assert receipt.decision_code == "ROUTE_REJECTED_UNSUPPORTED_FORMAT"
    assert "Newsletters are not CMF deliverables" in receipt.route_rationale
    assert rejection.decision == RouteDecision.rejected_unsupported_format
    assert not receipt.accepted_route_ids


def test_route_lineage_remains_attached_for_package_planning():
    routing, _review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()

    receipt = routing.route_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        actor_id=actor_id,
    )

    assert receipt.package_planning_refs
    assert receipt.package_planning_refs[0].startswith("asset_package_spec_input:asset_route_receipt:")


def test_workflow_stage7_routes_expression_moments():
    routing, review, extraction, source_service, session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()
    workflow = CompleteExpressionSessionWorkflow(
        service=session_service,
        source_provenance_service=source_service,
        extraction_service=extraction,
        expression_review_service=review,
        routing_service=routing,
    )

    receipts = workflow.stage7_route_expression_moments(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_ids=[moment_id],
        actor_id=actor_id,
    )

    assert receipts[0].decision_code == "ASSET_ROUTE_ACCEPTED"


def test_routing_command_bus_emits_receipt_event():
    routing, _review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, moment_id = _routing_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_routing_command_handlers(bus, routing)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="RouteExpressionMomentCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"expression_moment_id": str(moment_id), "requested_format": "paper-cut explainer"},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "ASSET_ROUTE_ACCEPTED"
    assert bus.event_outbox.events[-1].event_type == "RouteExpressionMomentCommand.succeeded"
