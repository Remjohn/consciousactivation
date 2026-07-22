from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_layer_manifests_animation_plans_edl_captions_and_sonic_plans import _assembly_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.revision_service import RevisionService, RevisionServiceError, register_revision_command_handlers  # noqa: E402
from ccp_studio.workflows.review_workflow import ReviewWorkflow  # noqa: E402


def _revision_fixture():
    planner, compiler, org_id, brand_id, actor_id, scene_spec = _assembly_fixture()
    plan = planner.compile_assembly_plan(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    editing_service = compiler.editing_session_service
    composition_service = planner.composition_service
    service = RevisionService(editing_service, compiler, composition_service, planner)
    return service, planner, compiler, org_id, brand_id, actor_id, scene_spec, plan


def _delta(field_path="caption_manifest.cues[0].text"):
    return {
        "field_path": field_path,
        "previous_value_hash": "sha256-before",
        "new_value_hash": "sha256-after",
        "reason": "caption should better preserve the guest's exact meaning",
    }


def test_revision_records_reason_deltas_prior_actor_lineage_provider_receipts_and_evaluation():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec, _plan = _revision_fixture()
    evaluation_receipt_id = uuid4()

    request = service.request_scene_revision(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        requested_by_user_id=actor_id,
        reason="caption repair after review",
        target_object_type="caption_manifest",
        target_object_id=scene_spec.scene_spec_id,
        deltas=[_delta()],
        prior_version_id=scene_spec.scene_spec_id,
        evaluation_receipt_ids=[evaluation_receipt_id],
    )

    receipt = next(item for item in service.repository.receipts.values() if item.revision_request_id == request.revision_request_id)
    assert request.reason == "caption repair after review"
    assert request.deltas[0].field_path == "caption_manifest.cues[0].text"
    assert request.prior_version_id == scene_spec.scene_spec_id
    assert request.requested_by_user_id == actor_id
    assert request.lineage_refs.source_expression_moment_id == scene_spec.source_expression_moment_id
    assert request.lineage_refs.provider_receipt_ids
    assert request.lineage_refs.evaluation_receipt_ids == [evaluation_receipt_id]
    assert receipt.decision_code == "REVISION_REQUESTED"


def test_reconstruction_audit_traces_multiple_revisions_to_source_route_brand_provider_manifest_and_human_decision():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec, plan = _revision_fixture()
    first = service.request_scene_revision(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        requested_by_user_id=actor_id,
        reason="caption repair",
        target_object_type="caption_manifest",
        target_object_id=plan.caption_manifest_id,
        deltas=[_delta()],
        prior_version_id=scene_spec.scene_spec_id,
    )
    first_version = next(item for item in service.repository.revision_versions.values() if item.revision_request_id == first.revision_request_id)
    second = service.request_scene_revision(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        requested_by_user_id=actor_id,
        reason="motion timing repair",
        target_object_type="animation_plan",
        target_object_id=plan.animation_plan_id,
        deltas=[_delta("animation_plan.layer_animations[0].end_frame")],
        prior_version_id=first_version.revision_version_id,
    )
    second_version = next(item for item in service.repository.revision_versions.values() if item.revision_request_id == second.revision_request_id)
    approval = service.approve_final_version(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        final_version_id=second_version.revision_version_id,
        approved_by_actor_id=actor_id,
        human_decision_ref="pwa_review:approved_after_second_revision",
    )

    audit = service.build_reconstruction_audit_view(complete_editing_session_id=scene_spec.complete_editing_session_id)

    assert audit.source_expression_moment_id == scene_spec.source_expression_moment_id
    assert audit.asset_route_receipt_id == scene_spec.asset_route_receipt_id
    assert audit.brand_context_version_id == scene_spec.brand_context_version_id
    assert second_version.revision_version_id in audit.scene_spec_versions
    assert audit.composition_job_ids
    assert audit.provider_job_ids
    assert plan.layer_manifest_id in audit.render_manifest_ids
    assert approval.final_approval_binding_id in audit.approval_event_ids


def test_lineage_dropping_revision_is_blocked():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec, _plan = _revision_fixture()

    with pytest.raises(RevisionServiceError) as exc:
        service.request_scene_revision(
            complete_editing_session_id=scene_spec.complete_editing_session_id,
            requested_by_user_id=actor_id,
            reason="bad rewrite",
            target_object_type="scene_spec",
            target_object_id=scene_spec.scene_spec_id,
            deltas=[_delta("source_expression_moment_id") | {"new_value_hash": "DROP"}],
            prior_version_id=scene_spec.scene_spec_id,
        )

    assert exc.value.code == "LINEAGE_DROPPING_REVISION_BLOCKED"
    assert list(service.repository.receipts.values())[-1].decision_code == "LINEAGE_DROPPING_REVISION_BLOCKED"


def test_final_approval_references_final_version_and_prior_chain():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec, plan = _revision_fixture()
    request = service.request_scene_revision(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        requested_by_user_id=actor_id,
        reason="caption repair",
        target_object_type="caption_manifest",
        target_object_id=plan.caption_manifest_id,
        deltas=[_delta()],
        prior_version_id=scene_spec.scene_spec_id,
    )
    version = next(item for item in service.repository.revision_versions.values() if item.revision_request_id == request.revision_request_id)

    approval = service.approve_final_version(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        final_version_id=version.revision_version_id,
        approved_by_actor_id=actor_id,
        human_decision_ref="operator_final_approval",
    )

    assert approval.final_version_id == version.revision_version_id
    assert scene_spec.scene_spec_id in approval.prior_version_ids
    assert approval.revision_chain_id in service.repository.revision_chains


def test_reconstruction_resolves_source_route_brand_composition_provider_manifests_and_approvals():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec, plan = _revision_fixture()
    request = service.request_scene_revision(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        requested_by_user_id=actor_id,
        reason="manifest repair",
        target_object_type="layer_manifest",
        target_object_id=plan.layer_manifest_id,
        deltas=[_delta("layer_manifest.layers[0].bbox")],
        prior_version_id=scene_spec.scene_spec_id,
    )
    version = next(item for item in service.repository.revision_versions.values() if item.revision_request_id == request.revision_request_id)
    service.approve_final_version(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        final_version_id=version.revision_version_id,
        approved_by_actor_id=actor_id,
        human_decision_ref="human:approved",
    )

    view = service.build_reconstruction_audit_view(complete_editing_session_id=scene_spec.complete_editing_session_id)

    assert view.source_expression_moment_id == scene_spec.source_expression_moment_id
    assert view.composition_job_ids
    assert view.provider_job_ids
    assert set(plan.manifest_hashes) == {
        "layer_manifest_hash",
        "animation_plan_hash",
        "edit_decision_list_hash",
        "timeline_manifest_hash",
        "caption_manifest_hash",
        "audio_mix_manifest_hash",
    }
    assert view.render_manifest_ids
    assert view.approval_event_ids


def test_review_workflow_stage13_records_revision_request():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, scene_spec, plan = _revision_fixture()
    workflow = ReviewWorkflow(service)

    request = workflow.stage13_revision_and_reconstruction(
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        actor_id=actor_id,
        reason="review requested caption repair",
        target_object_type="caption_manifest",
        target_object_id=plan.caption_manifest_id,
        deltas=[_delta()],
        prior_version_id=scene_spec.scene_spec_id,
    )

    assert request.revision_request_id in service.repository.revision_requests


def test_revision_command_bus_emits_receipt_event():
    service, _planner, _compiler, org_id, brand_id, actor_id, scene_spec, plan = _revision_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_revision_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="RequestSceneRevisionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "complete_editing_session_id": str(scene_spec.complete_editing_session_id),
            "reason": "caption repair",
            "target_object_type": "caption_manifest",
            "target_object_id": str(plan.caption_manifest_id),
            "deltas": [_delta()],
            "prior_version_id": str(scene_spec.scene_spec_id),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["revision_request_id"]
    assert bus.event_outbox.events[-1].event_type == "RequestSceneRevisionCommand.succeeded"
