from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_complete_editing_session_creation_from_approved_source import _editing_fixture  # noqa: E402

from ccp_studio.contracts.brand_context_gate import SelectedBrandAssetRef  # noqa: E402
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.scene_spec import CreativeStateStage  # noqa: E402
from ccp_studio.services.brand_context_gate_service import BrandContextGateService  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.scene_spec_compiler import (  # noqa: E402
    SceneSpecCompiler,
    SceneSpecCompilerError,
    register_scene_spec_command_handlers,
)
from ccp_studio.workflows.complete_editing_session import CompleteEditingSessionWorkflow  # noqa: E402


def _platform_variants():
    return [
        {
            "platform": "instagram_reels",
            "aspect_ratio": "9:16",
            "duration_seconds": 45,
            "captions_required": True,
            "caption_plan": "burned_in_captions_from_transcript_alignment",
            "negative_space_required": True,
            "text_space": "upper_third_reserved_for_caption_and_title",
            "safe_zone": "center_safe_9x16",
        },
        {
            "platform": "linkedin_feed",
            "aspect_ratio": "4:5",
            "duration_seconds": 45,
            "captions_required": True,
            "caption_plan": "open_caption_track_with_two_line_limit",
            "negative_space_required": True,
            "text_space": "left_margin_reserved_for_pull_quote",
            "safe_zone": "center_safe_4x5",
        },
    ]


def _revision_policy():
    return {
        "max_revision_cycles": 2,
        "requires_human_review": True,
        "allowed_change_scope": ["caption_timing", "asset_substitution_within_locked_context", "layout_spacing"],
        "rollback_strategy": "supersede_scene_spec_and_invalidate_downstream_jobs",
    }


def _scene_fixture():
    service, _package, _routing, _review, org_id, brand_id, actor_id, _session, route_receipts, requests, locked_context = _editing_fixture()
    editing_session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        source_expression_moment_id=requests[0].expression_moment_id,
        asset_route_receipt_id=route_receipts[0].asset_route_receipt_id,
        asset_package_item_id=requests[0].package_item_id,
        brand_context_version_id=locked_context.brand_context_version_id,
        actor_id=actor_id,
    )
    gate = BrandContextGateService(service.brand_context_service)
    compiler = SceneSpecCompiler(gate, editing_session_service=service)
    selected_assets = [
        SelectedBrandAssetRef(
            schema_version="cmf.selected_brand_asset_ref.v1",
            asset_type="acting_library_version",
            asset_id=locked_context.asset_bundle.acting_library_version_id,
            asset_hash="sha256-acting-library",
            brand_context_version_id=locked_context.brand_context_version_id,
        ),
        SelectedBrandAssetRef(
            schema_version="cmf.selected_brand_asset_ref.v1",
            asset_type="rig_manifest",
            asset_id=locked_context.asset_bundle.rig_manifest_id,
            asset_hash="sha256-rig-manifest",
            brand_context_version_id=locked_context.brand_context_version_id,
        ),
    ]
    return compiler, service, org_id, brand_id, actor_id, editing_session, selected_assets


def _compile(compiler, actor_id, editing_session, selected_assets):
    return compiler.compile_scene_spec(
        complete_editing_session_id=editing_session.complete_editing_session_id,
        actor_id=actor_id,
        selected_asset_refs=selected_assets,
        platform_variants=_platform_variants(),
        revision_policy=_revision_policy(),
    )


def test_scene_spec_compilation_emits_state_render_contract_assets_variants_evals_policy_and_receipt():
    compiler, _service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()

    scene_spec = _compile(compiler, actor_id, editing_session, selected_assets)

    creative_state = next(item for item in compiler.repository.creative_states.values() if item.scene_spec_id == scene_spec.scene_spec_id)
    render_contract = next(item for item in compiler.repository.render_contracts.values() if item.scene_spec_id == scene_spec.scene_spec_id)
    receipt = next(item for item in compiler.repository.receipts.values() if item.scene_spec_id == scene_spec.scene_spec_id and item.decision_code == "SCENE_SPEC_COMPILED")
    assert scene_spec.complete_editing_session_id == editing_session.complete_editing_session_id
    assert creative_state.stage == CreativeStateStage.render_contract_ready
    assert render_contract.revision_policy_id == scene_spec.revision_policy_id
    assert len(scene_spec.asset_selection_ids) == 2
    assert len(scene_spec.platform_variant_ids) == 2
    assert len(scene_spec.evaluation_requirement_ids) >= 2
    assert receipt.render_contract_id == render_contract.render_contract_id


def test_unapproved_brand_asset_fails_validation_and_writes_blocked_receipt():
    compiler, _service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()
    selected_assets[0] = selected_assets[0].model_copy(update={"asset_id": uuid4(), "asset_hash": "sha256-outside"})

    with pytest.raises(SceneSpecCompilerError) as exc:
        _compile(compiler, actor_id, editing_session, selected_assets)

    assert exc.value.code == "BRAND_ASSET_NOT_IN_CONTEXT"
    assert list(compiler.repository.receipts.values())[-1].decision_code == "SCENE_SPEC_COMPILATION_BLOCKED"


def test_platform_variant_caption_and_negative_space_constraints_are_explicit():
    compiler, _service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()

    scene_spec = _compile(compiler, actor_id, editing_session, selected_assets)

    variants = [compiler.repository.platform_variants[item] for item in scene_spec.platform_variant_ids]
    assert all(item.caption_plan for item in variants if item.captions_required)
    assert all(item.text_space for item in variants if item.negative_space_required)
    contract = next(item for item in compiler.repository.render_contracts.values() if item.scene_spec_id == scene_spec.scene_spec_id)
    assert contract.renderer_props["platform_variants"][0]["caption_plan"] == "burned_in_captions_from_transcript_alignment"


def test_missing_revision_policy_blocks_provider_queue_before_render_contract():
    compiler, _service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()

    with pytest.raises(SceneSpecCompilerError) as exc:
        compiler.compile_scene_spec(
            complete_editing_session_id=editing_session.complete_editing_session_id,
            actor_id=actor_id,
            selected_asset_refs=selected_assets,
            platform_variants=_platform_variants(),
            revision_policy=None,
        )

    assert exc.value.code == "REVISION_POLICY_REQUIRED"
    assert not compiler.repository.render_contracts
    assert list(compiler.repository.receipts.values())[-1].decision_code == "SCENE_SPEC_COMPILATION_BLOCKED"


def test_scene_spec_receipt_references_source_route_brand_context_and_input_hashes():
    compiler, _service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()

    scene_spec = _compile(compiler, actor_id, editing_session, selected_assets)

    receipt = next(item for item in compiler.repository.receipts.values() if item.scene_spec_id == scene_spec.scene_spec_id and item.decision_code == "SCENE_SPEC_COMPILED")
    assert receipt.source_expression_moment_id == editing_session.source_expression_moment_id
    assert receipt.asset_route_receipt_id == editing_session.asset_route_receipt_id
    assert receipt.brand_context_version_id == editing_session.brand_context_version_id
    assert receipt.brand_context_version_hash == editing_session.brand_context_version_hash
    assert receipt.input_hash == scene_spec.input_hash
    assert receipt.selected_asset_hashes == ["sha256-acting-library", "sha256-rig-manifest"]


def test_workflow_stage9_compile_scene_spec_links_complete_editing_session():
    compiler, service, _org_id, _brand_id, actor_id, editing_session, selected_assets = _scene_fixture()
    workflow = CompleteEditingSessionWorkflow(service, scene_spec_compiler=compiler)

    scene_spec = workflow.stage9_compile_scene_spec(
        complete_editing_session_id=editing_session.complete_editing_session_id,
        actor_id=actor_id,
        selected_asset_refs=selected_assets,
        platform_variants=_platform_variants(),
        revision_policy=_revision_policy(),
    )

    assert scene_spec.scene_spec_id in compiler.repository.scene_specs
    assert service.repository.sessions[editing_session.complete_editing_session_id].production_readiness == "render_contract_ready"


def test_scene_spec_command_bus_emits_receipt_event():
    compiler, _service, org_id, brand_id, actor_id, editing_session, selected_assets = _scene_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_scene_spec_command_handlers(bus, compiler)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="CompileSceneSpecCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "complete_editing_session_id": str(editing_session.complete_editing_session_id),
            "selected_asset_refs": [item.model_dump(mode="json") for item in selected_assets],
            "platform_variants": _platform_variants(),
            "revision_policy": _revision_policy(),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["scene_spec_id"]
    assert bus.event_outbox.events[-1].event_type == "CompileSceneSpecCommand.succeeded"
