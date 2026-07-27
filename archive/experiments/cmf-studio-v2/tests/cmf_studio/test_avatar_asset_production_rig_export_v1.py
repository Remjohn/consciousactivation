import pytest

from ccp_studio.contracts.avatar_asset_production import (
    ActionClipName,
    AvatarActionClipSpec,
    AvatarActionTimeline,
    AvatarCharacterQAReport,
    AvatarCharacterSpec,
    AvatarFacePlateAsset,
    AvatarFacePlateApprovalSet,
    AvatarPSDLayerRequirement,
    AvatarRigContinuityReceipt,
    AvatarRigExportManifest,
    AvatarRemotionLayerPayload,
    CanonicalBodyLayerName,
    DragonBonesExportManifest,
    ExpressionPlateName,
    MouthAnimationMode,
    PassStatus,
    RuntimeExportTarget,
    SpineExportManifest,
    StretchyStudioImportManifest,
)
from ccp_studio.services.avatar_asset_production_service import AvatarAssetProductionService
from ccp_studio.services.avatar_character_qa_service import AvatarCharacterQAService
from ccp_studio.services.avatar_face_plate_approval_service import AvatarFacePlateApprovalService
from ccp_studio.services.avatar_paper_body_layer_service import AvatarPaperBodyLayerService
from ccp_studio.services.avatar_psd_layer_service import AvatarPSDLayerService
from ccp_studio.services.avatar_rig_continuity_service import AvatarRigContinuityService
from ccp_studio.services.avatar_rig_export_service import AvatarRigExportService
from ccp_studio.services.avatar_action_timeline_service import AvatarActionTimelineService
from ccp_studio.services.dragonbones_export_manifest_service import DragonBonesExportManifestService
from ccp_studio.services.spine_export_manifest_service import SpineExportManifestService
from ccp_studio.services.stretchy_studio_manifest_service import StretchyStudioManifestService
from ccp_studio.services.avatar_remotion_layer_payload_service import AvatarRemotionLayerPayloadService


def test_character_spec_rejects_lipsync():
    with pytest.raises(Exception):
        AvatarCharacterSpec(
            avatar_id="coach_avatar_v1",
            brand_id="brand",
            brand_context_version_id="bcv",
            character_name="Coach",
            identity_anchor_refs=["face"],
            lip_sync_enabled=True,
        )


def test_character_spec_requires_identity_anchors():
    with pytest.raises(Exception):
        AvatarCharacterSpec(
            avatar_id="coach_avatar_v1",
            brand_id="brand",
            brand_context_version_id="bcv",
            character_name="Coach",
            identity_anchor_refs=[],
        )


def test_psd_layer_requirement_rejects_path_traversal():
    with pytest.raises(Exception):
        AvatarPSDLayerRequirement(
            layer_name="torso",
            canonical_layer=CanonicalBodyLayerName.TORSO,
            source_path="../escape.png",
            z_index=1,
        )


def test_psd_layer_service_compiles_canonical_layers():
    layers = AvatarPSDLayerService().compile_canonical_layer_requirements()
    assert {layer.canonical_layer for layer in layers} == set(CanonicalBodyLayerName)


def test_face_plate_asset_rejects_phoneme_and_viseme():
    with pytest.raises(Exception):
        AvatarFacePlateAsset(
            expression_name=ExpressionPlateName.GENTLE_SMILE,
            asset_ref="assets/avatar/face/smile.png",
            approved=True,
            phoneme_key="A",
        )


def test_face_plate_approval_set_requires_8_approved_expressions():
    face_set = AvatarFacePlateApprovalService().compile_approved_face_plate_set(
        avatar_id="coach_avatar_v1",
        approved_by="operator",
    )
    assert len(face_set.face_plates) == 8
    assert {plate.expression_name for plate in face_set.face_plates} == set(ExpressionPlateName)


def test_face_plate_approval_set_rejects_unapproved_plate():
    plates = [
        AvatarFacePlateAsset(
            expression_name=expression,
            asset_ref=f"assets/avatar/face/{expression.value}.png",
            approved=(expression != ExpressionPlateName.NEUTRAL_WARM),
        )
        for expression in ExpressionPlateName
    ]
    with pytest.raises(Exception):
        AvatarFacePlateApprovalSet(avatar_id="coach_avatar_v1", face_plates=plates, approved_by="operator")


def test_body_layer_set_requires_canonical_layers():
    body_set = AvatarPaperBodyLayerService().compile_body_layer_set(avatar_id="coach_avatar_v1")
    assert {layer.canonical_layer for layer in body_set.layers} == set(CanonicalBodyLayerName)


def test_asset_production_plan_requires_all_psd_layers():
    spec = AvatarAssetProductionService().create_character_spec(
        avatar_id="coach_avatar_v1",
        brand_id="brand",
        brand_context_version_id="bcv",
    )
    plan = AvatarAssetProductionService().compile_production_plan(spec)
    assert len(plan.psd_layer_requirements) == len(CanonicalBodyLayerName)


def test_action_timeline_rejects_lipsync_clip():
    with pytest.raises(Exception):
        AvatarActionClipSpec(
            clip_name=ActionClipName.RAISE_FINGER,
            start_ms=0,
            end_ms=900,
            primitive_function="clarity",
            sfl_function="entry",
            lip_sync_enabled=True,
        )


def test_action_timeline_service_compiles_canonical_clips():
    timeline = AvatarActionTimelineService().compile_canonical_action_timeline("coach_avatar_v1")
    assert len(timeline.clips) == len(ActionClipName)
    assert not timeline.lip_sync_enabled


def test_stretchy_manifest_requires_layers_bones_mesh_and_sockets():
    with pytest.raises(Exception):
        StretchyStudioImportManifest(
            avatar_id="coach_avatar_v1",
            source_psd_ref="assets/avatar/coach.psd",
            layer_requirements=[],
            skeleton_hints=[],
            mesh_candidates=[],
            prop_sockets=[],
        )


def test_stretchy_manifest_service_compiles_import_manifest():
    layers = AvatarPSDLayerService().compile_canonical_layer_requirements()
    timeline = AvatarActionTimelineService().compile_canonical_action_timeline("coach_avatar_v1")
    manifest = StretchyStudioManifestService().compile_import_manifest(
        avatar_id="coach_avatar_v1",
        source_psd_ref="assets/avatar/coach.psd",
        layer_requirements=layers,
        action_timeline_ref=timeline.avatar_action_timeline_id,
    )
    assert manifest.layer_requirements
    assert manifest.skeleton_hints
    assert manifest.mesh_candidates
    assert manifest.prop_sockets


def test_spine_export_requires_license_confirmation():
    with pytest.raises(Exception):
        SpineExportManifest(
            avatar_id="coach_avatar_v1",
            source_stretchy_manifest_id="stretchy_1",
            output_json_ref="assets/avatar/spine/coach.json",
            license_confirmed=False,
        )


def test_spine_export_service_compiles_with_license_confirmation():
    manifest = SpineExportManifestService().compile_export_manifest(
        avatar_id="coach_avatar_v1",
        source_stretchy_manifest_id="stretchy_1",
        output_json_ref="assets/avatar/spine/coach.json",
        license_confirmed=True,
    )
    assert manifest.license_confirmed


def test_dragonbones_export_requires_js_runtime_compatibility():
    with pytest.raises(Exception):
        DragonBonesExportManifest(
            avatar_id="coach_avatar_v1",
            source_stretchy_manifest_id="stretchy_1",
            output_json_ref="assets/avatar/dragonbones/coach.json",
            js_runtime_compatible=False,
        )


def test_dragonbones_export_service_compiles_manifest():
    manifest = DragonBonesExportManifestService().compile_export_manifest(
        avatar_id="coach_avatar_v1",
        source_stretchy_manifest_id="stretchy_1",
        output_json_ref="assets/avatar/dragonbones/coach.json",
    )
    assert manifest.js_runtime_compatible


def test_rig_export_manifest_requires_target_specific_ids():
    with pytest.raises(Exception):
        AvatarRigExportManifest(
            avatar_id="coach_avatar_v1",
            stretchy_studio_import_manifest_id="stretchy_1",
            export_targets=[RuntimeExportTarget.SPINE],
        )


def test_rig_export_service_compiles_export_manifest():
    manifest = AvatarRigExportService().compile_rig_export_manifest(
        avatar_id="coach_avatar_v1",
        stretchy_studio_import_manifest_id="stretchy_1",
        spine_export_manifest_id="spine_1",
    )
    assert RuntimeExportTarget.SPINE in manifest.export_targets
    assert RuntimeExportTarget.REMOTION in manifest.export_targets


def test_remotion_payload_is_not_final_render():
    payload = AvatarRemotionLayerPayloadService().compile_payload(
        avatar_id="coach_avatar_v1",
        layer_refs=["layer_head", "layer_torso"],
        action_timeline_ref="timeline_1",
        rig_export_manifest_ref="rig_export_1",
    )
    assert not payload.final_render
    assert not payload.renderer_calls_executed


def test_remotion_payload_rejects_renderer_execution():
    with pytest.raises(Exception):
        AvatarRemotionLayerPayload(
            avatar_id="coach_avatar_v1",
            layer_refs=["layer_head"],
            action_timeline_ref="timeline_1",
            rig_export_manifest_ref="rig_1",
            renderer_calls_executed=True,
        )


def test_character_qa_fails_missing_requirements():
    report = AvatarCharacterQAService().run_qa(
        avatar_id="coach_avatar_v1",
        face_plate_count=7,
        body_layer_count=5,
        required_bones_present=False,
        prop_sockets_present=False,
        no_lipsync_policy_pass=False,
        path_safety_pass=True,
        export_manifests_valid=True,
    )
    assert report.pass_status == PassStatus.FAIL
    assert "face_plate_count_not_8" in report.blockers
    assert "no_lipsync_policy_failed" in report.blockers


def test_character_qa_passes_complete_stack():
    report = AvatarCharacterQAService().run_qa(
        avatar_id="coach_avatar_v1",
        face_plate_count=8,
        body_layer_count=len(CanonicalBodyLayerName),
        required_bones_present=True,
        prop_sockets_present=True,
        no_lipsync_policy_pass=True,
        path_safety_pass=True,
        export_manifests_valid=True,
    )
    assert report.pass_status == PassStatus.PASS
    assert not report.blockers


def test_rig_continuity_fails_identity_drift():
    receipt = AvatarRigContinuityService().evaluate(
        avatar_id="coach_avatar_v1",
        identity_anchors_preserved=False,
    )
    assert receipt.pass_status == PassStatus.FAIL
    assert "identity_anchors_drift" in receipt.blockers


def test_asset_production_service_compiles_default_stack():
    service = AvatarAssetProductionService()
    spec = service.create_character_spec(
        avatar_id="coach_avatar_v1",
        brand_id="brand",
        brand_context_version_id="bcv",
    )
    stack = service.compile_default_asset_stack(spec, approved_by="operator")
    assert stack["production_plan"]
    assert len(stack["face_plate_approval_set"].face_plates) == 8
    assert len(stack["body_layer_set"].layers) == len(CanonicalBodyLayerName)
    assert stack["stretchy_studio_import_manifest"].skeleton_hints
