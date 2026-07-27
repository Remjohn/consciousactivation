from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_complete_editing_session_creation_from_approved_source import _editing_fixture  # noqa: E402
from test_scenespec_creative_state_and_render_contract_compilation import (  # noqa: E402
    _platform_variants,
    _revision_policy,
    _scene_fixture,
)

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.reaction_editing_service import (  # noqa: E402
    ReactionEditingTemplateService,
    register_reaction_editing_template_command_handlers,
)


def test_reaction_editing_template_registry_keeps_legacy_app_families_as_editing_grammars():
    _service, _package, routing, _review, org_id, brand_id, actor_id, _session, route_receipts, _requests, _context = _editing_fixture()
    reaction_service = ReactionEditingTemplateService(routing)

    templates = {template.template_code.value: template for template in reaction_service.list_templates()}

    assert {"VRS-SPLIT", "TRK-TIER", "RNK-BLIND", "RNK-PROPOSAL", "ELM-BRACKET", "MIR-QUIZ", "AUTH-LADDER"}.issubset(templates)
    assert templates["VRS-SPLIT"].source_app_refs == ["apps/react-debate"]
    assert templates["TRK-TIER"].motion_grammar.composition_id == "reaction-tier-list"
    assert "SV-RRC" in templates["RNK-BLIND"].valid_content_format_codes


def test_approved_expression_route_can_select_goal_style_tier_template():
    _service, _package, routing, _review, org_id, brand_id, actor_id, _session, route_receipts, _requests, _context = _editing_fixture()
    reaction_service = ReactionEditingTemplateService(routing)

    receipt = reaction_service.plan_template_route(
        organization_id=org_id,
        brand_id=brand_id,
        asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
        actor_id=actor_id,
        requested_template_code="TRK-TIER",
        content_format_code="SV-RRC",
    )

    route = reaction_service.repository.routes[receipt.reaction_template_route_id]
    assert receipt.decision_code == "REACTION_TEMPLATE_ROUTE_ACCEPTED"
    assert receipt.template_code == "TRK-TIER"
    assert route.live_clip_slot_specs[0].slot_key == "rank_items"
    assert route.scene_spec_requirement_patch["renderer_route"] == "remotion_reaction_template"
    assert route.scene_spec_requirement_patch["composition_id"] == "reaction-tier-list"


def test_scene_spec_preserves_reaction_template_route_for_renderer_props():
    compiler, editing_service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()
    reaction_service = ReactionEditingTemplateService(editing_service.routing_service)
    template_receipt = reaction_service.plan_template_route(
        organization_id=editing_session.organization_id,
        brand_id=editing_session.brand_id,
        asset_route_receipt_id=editing_session.asset_route_receipt_id,
        actor_id=actor_id,
        requested_template_code="VRS-SPLIT",
        content_format_code="SV-RRC",
    )

    scene_spec = compiler.compile_scene_spec(
        complete_editing_session_id=editing_session.complete_editing_session_id,
        actor_id=actor_id,
        selected_asset_refs=selected_assets,
        platform_variants=_platform_variants(),
        revision_policy=_revision_policy(),
        renderer_route=template_receipt.scene_spec_requirement_patch["renderer_route"],
        composition_requirements=template_receipt.scene_spec_requirement_patch,
        reaction_template_route_id=template_receipt.reaction_template_route_id,
        reaction_template_code=template_receipt.template_code,
    )
    render_contract = next(item for item in compiler.repository.render_contracts.values() if item.scene_spec_id == scene_spec.scene_spec_id)
    receipt = next(item for item in compiler.repository.receipts.values() if item.scene_spec_id == scene_spec.scene_spec_id and item.decision_code == "SCENE_SPEC_COMPILED")

    assert scene_spec.reaction_template_code == "VRS-SPLIT"
    assert render_contract.reaction_template_code == "VRS-SPLIT"
    assert render_contract.renderer_props["reaction_template_code"] == "VRS-SPLIT"
    assert receipt.reaction_template_route_id == template_receipt.reaction_template_route_id


def test_reaction_template_route_command_bus_emits_receipt_event():
    _service, _package, routing, _review, org_id, brand_id, actor_id, _session, route_receipts, _requests, _context = _editing_fixture()
    reaction_service = ReactionEditingTemplateService(routing)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_reaction_editing_template_command_handlers(bus, reaction_service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="PlanReactionTemplateRouteCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "asset_route_receipt_id": str(route_receipts[0].asset_route_receipt_id),
            "requested_template_code": "VRS-SPLIT",
            "content_format_code": "VPL-VRS",
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "REACTION_TEMPLATE_ROUTE_ACCEPTED"
    assert bus.event_outbox.events[-1].event_type == "PlanReactionTemplateRouteCommand.succeeded"
