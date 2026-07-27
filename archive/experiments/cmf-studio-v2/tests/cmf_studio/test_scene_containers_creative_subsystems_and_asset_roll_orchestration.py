from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_revision_and_reconstruction_audit import _revision_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.scene_intelligence import AssetRollRole, BiologicalArcContainer  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.scene_intelligence_service import (  # noqa: E402
    SceneIntelligenceService,
    SceneIntelligenceServiceError,
    register_scene_intelligence_command_handlers,
)
from ccp_studio.workflows.complete_editing_session import CompleteEditingSessionWorkflow  # noqa: E402


def _scene_intelligence_fixture():
    _revision, planner, compiler, org_id, brand_id, actor_id, scene_spec, _plan = _revision_fixture()
    service = SceneIntelligenceService(
        compiler,
        composition_service=planner.composition_service,
        assembly_planner=planner,
    )
    return service, planner, compiler, org_id, brand_id, actor_id, scene_spec


def test_container_is_required_before_component_selection():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()

    with pytest.raises(SceneIntelligenceServiceError) as exc:
        service.select_scene_component(
            scene_container_plan_id=scene_spec.scene_spec_id,
            actor_id=actor_id,
            component_registry_ref="legacy-cmf:scene-component:first-frame-imprint",
            satisfied_constraints=["container:hook"],
            violated_constraints=[],
            selection_rationale="bad ordering",
        )

    assert exc.value.code == "SCENE_CONTAINER_REQUIRED"
    receipt = service.run_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    container = service.repository.container_plans[receipt.scene_container_plan_id]
    component = service.repository.component_selections[receipt.scene_component_selection_id]
    assert container.container == BiologicalArcContainer.hook
    assert component.scene_container_plan_id == container.scene_container_plan_id


def test_component_records_validity_and_constraints():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()

    receipt = service.run_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    component = service.repository.component_selections[receipt.scene_component_selection_id]
    assert component.valid_for_container is True
    assert "first_frame_readable" in component.satisfied_constraints
    assert not component.violated_constraints
    assert component.selection_rationale


def test_creative_subsystem_gates_are_recorded_as_registry_decisions():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()

    receipt = service.run_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    decisions = [service.repository.subsystem_decisions[item] for item in receipt.creative_subsystem_decision_ids]
    assert {item.subsystem_registry_ref for item in decisions} >= {
        "legacy-cmf:creative-subsystem:first-frame-imprint",
        "legacy-cmf:creative-subsystem:recognition-window",
    }
    assert all(item.decision == "approved" for item in decisions)


def test_asset_roll_plan_items_carry_function_and_source_license_state():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()

    receipt = service.run_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    plan = service.repository.asset_roll_plans[receipt.asset_roll_plan_id]
    assert {item.role for item in plan.items} == set(AssetRollRole)
    assert all(item.function and item.source_or_license_state and item.rationale for item in plan.items)
    assert next(item for item in plan.items if item.role == AssetRollRole.a_roll).source_or_license_state == "approved_source_expression"


def test_reconstruction_resolves_container_component_gates_asset_roll_sonic_plan_composition_and_manifests():
    service, planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()
    service.run_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    view = service.reconstruct_scene_intelligence(scene_spec.scene_spec_id)

    assert view.source_expression_moment_id == scene_spec.source_expression_moment_id
    assert view.asset_route_receipt_id == scene_spec.asset_route_receipt_id
    assert view.scene_container_plan_id in service.repository.container_plans
    assert view.scene_component_selection_id in service.repository.component_selections
    assert view.creative_subsystem_decision_ids
    assert view.asset_roll_plan_id in service.repository.asset_roll_plans
    assert view.composition_job_ids
    assert view.assembly_plan_ids
    assert planner.repository.assembly_plans[view.assembly_plan_ids[0]].audio_mix_manifest_id in view.sonic_plan_ids


def test_workflow_stage9_10_scene_intelligence_writes_receipt():
    service, _planner, compiler, _org_id, _brand_id, actor_id, scene_spec = _scene_intelligence_fixture()
    workflow = CompleteEditingSessionWorkflow(
        compiler.editing_session_service,
        scene_spec_compiler=compiler,
        scene_intelligence_service=service,
    )

    receipt = workflow.stage9_10_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    assert receipt.validation_passed is True
    assert receipt.decision_code == "SCENE_ORCHESTRATION_VALIDATED"


def test_scene_intelligence_command_bus_emits_receipt_event():
    service, _planner, _compiler, org_id, brand_id, actor_id, scene_spec = _scene_intelligence_fixture()
    service.run_scene_intelligence(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_scene_intelligence_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="ValidateSceneOrchestrationCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"scene_spec_id": str(scene_spec.scene_spec_id)},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["scene_intelligence_receipt_id"]
    assert bus.event_outbox.events[-1].event_type == "ValidateSceneOrchestrationCommand.succeeded"
