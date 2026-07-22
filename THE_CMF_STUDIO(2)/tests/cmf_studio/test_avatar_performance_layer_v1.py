import pytest

from ccp_studio.contracts.avatar_performance import (
    AudienceProxyPersona,
    Avatar64StateActingLibrary,
    AvatarFacePlate,
    AvatarFormatUse,
    AvatarHybridDesignSpec,
    AvatarPerformancePlan,
    AvatarPerformanceState,
    AvatarPropAttachmentSpec,
    AvatarRenderPayload,
    BodyPoseName,
    ExpressionPlateName,
    MockingRisk,
    MouthAnimationMode,
    PassStatus,
    RuntimeTarget,
)
from ccp_studio.contracts.format02_composition_intelligence import Format02SceneRole
from ccp_studio.services.audience_proxy_service import AudienceProxyService
from ccp_studio.services.avatar_body_rig_service import AvatarBodyRigService
from ccp_studio.services.avatar_clip_library_service import AvatarClipLibraryService
from ccp_studio.services.avatar_face_plate_service import AvatarFacePlateService
from ccp_studio.services.avatar_performance_eval_service import AvatarPerformanceEvalService
from ccp_studio.services.avatar_performance_service import AvatarPerformanceLayerService
from ccp_studio.services.avatar_prop_attachment_service import AvatarPropAttachmentService
from ccp_studio.services.avatar_render_payload_service import AvatarRenderPayloadService
from ccp_studio.services.format02_avatar_performance_adapter_service import Format02AvatarPerformanceAdapterService
from ccp_studio.services.format02_composition_service import Format02CompositionService


def test_hybrid_design_disables_lipsync():
    spec = AvatarHybridDesignSpec(avatar_id="coach_avatar_v1")
    assert not spec.lip_sync_enabled
    assert spec.mouth_animation == MouthAnimationMode.DISABLED


def test_hybrid_design_rejects_lipsync_enabled():
    with pytest.raises(Exception):
        AvatarHybridDesignSpec(avatar_id="coach_avatar_v1", lip_sync_enabled=True)


def test_face_plate_rejects_phoneme_or_viseme_keys():
    with pytest.raises(Exception):
        AvatarFacePlate(
            avatar_id="coach_avatar_v1",
            expression_name=ExpressionPlateName.GENTLE_SMILE,
            image_ref="face_smile",
            phoneme_key="A",
        )


def test_canonical_face_plate_set_has_8_expressions():
    face_set = AvatarFacePlateService().create_canonical_face_plate_set("coach_avatar_v1")
    assert len(face_set.plates) == 8
    assert {plate.expression_name for plate in face_set.plates} == set(ExpressionPlateName)


def test_body_rig_manifest_requires_canonical_bones_and_prop_sockets():
    layer_graph = AvatarBodyRigService().create_default_layer_graph("coach_avatar_v1")
    rig = AvatarBodyRigService().create_default_body_rig_manifest("coach_avatar_v1", layer_graph.avatar_layer_graph_id)
    assert rig.supports_prop_sockets
    assert {bone.bone_name for bone in rig.bones}.issuperset({"torso", "head_anchor", "left_hand", "right_hand"})


def test_pose_library_has_8_canonical_poses():
    pose_library = AvatarBodyRigService().create_canonical_pose_library("coach_avatar_v1")
    assert len(pose_library.poses) == 8
    assert {pose.pose_name for pose in pose_library.poses} == set(BodyPoseName)


def test_64_state_acting_library_compiles_8x8_states():
    library = AvatarClipLibraryService().create_64_state_acting_library("coach_avatar_v1")
    assert len(library.states) == 64
    assert len({(s.expression_name, s.body_pose_name) for s in library.states}) == 64


def test_64_state_library_rejects_incomplete_library():
    state = AvatarClipLibraryService().create_64_state_acting_library("coach_avatar_v1").states[0]
    with pytest.raises(Exception):
        Avatar64StateActingLibrary(avatar_id="coach_avatar_v1", states=[state])


def test_audience_proxy_personas_are_four():
    personas = AudienceProxyService().create_canonical_personas()
    assert {p.persona for p in personas} == set(AudienceProxyPersona)


def test_audience_proxy_rejects_high_mocking_risk():
    with pytest.raises(Exception):
        AudienceProxyService().create_proxy_state(
            persona=AudienceProxyPersona.CONFUSED_SEEKER,
            state_name="confused",
            primitive_function="clarity",
            sfl_function="open_question",
            mocking_risk=MockingRisk.HIGH,
        )


def test_performance_plan_rejects_lip_sync_enabled():
    state = AvatarPerformanceState(
        start_ms=0,
        end_ms=900,
        expression_name=ExpressionPlateName.CURIOUS_THINKING,
        body_pose_name=BodyPoseName.POINT_TO_CARD,
        primitive_function="clarity",
        sfl_function="focus_target",
    )
    with pytest.raises(Exception):
        AvatarPerformancePlan(
            avatar_id="coach_avatar_v1",
            format_use=AvatarFormatUse.FORMAT_02,
            scene_id="scene_1",
            performance_states=[state],
            lip_sync_enabled=True,
        )


def test_avatar_performance_service_compiles_no_lipsync_plan():
    plan = AvatarPerformanceLayerService().compile_performance_plan(
        avatar_id="coach_avatar_v1",
        scene_id="scene_1",
    )
    assert not plan.lip_sync_enabled
    assert plan.performance_states[0].sfl_function == "focus_target"


def test_prop_attachment_requires_socket_and_sfl():
    socket = AvatarPropAttachmentService().create_socket("right_hand", "right_hand")
    prop = AvatarPropAttachmentService().attach_prop(
        prop_ref="tea_cup_001",
        socket=socket,
        purpose="support object",
        sfl_function="closure_warmth",
    )
    assert prop.socket.socket_name == "right_hand"
    assert prop.sfl_function == "closure_warmth"


def test_uncanny_eval_fails_face_morphing_or_lipsync():
    receipt = AvatarPerformanceEvalService().evaluate_uncanny_risk(
        avatar_id="coach_avatar_v1",
        face_morphing_detected=True,
    )
    assert receipt.pass_status == PassStatus.FAIL
    assert "face_morphing_detected" in receipt.blockers


def test_render_payload_is_not_final_render():
    plan = AvatarPerformanceLayerService().compile_performance_plan(avatar_id="coach_avatar_v1", scene_id="scene_1")
    payload = AvatarRenderPayloadService().compile_render_payload(plan=plan)
    assert not payload.final_render
    assert not payload.provider_calls_executed
    assert not payload.render_executed


def test_render_payload_rejects_final_render_true():
    plan = AvatarPerformanceLayerService().compile_performance_plan(avatar_id="coach_avatar_v1", scene_id="scene_1")
    with pytest.raises(Exception):
        AvatarRenderPayload(
            avatar_performance_plan_id=plan.avatar_performance_plan_id,
            runtime_target=RuntimeTarget.REMOTION_LAYER,
            layer_refs=["layer_1"],
            performance_state_refs=[plan.performance_states[0].avatar_performance_state_id],
            final_render=True,
        )


def test_format02_scene_adapter_emits_avatar_and_proxy_performance_plan():
    scene = Format02CompositionService().compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="scene_1",
        scene_role=Format02SceneRole.MYTH_SETUP,
        concept_statement="Natural does not always mean safe.",
        headline_text="Natural ≠ always safe?",
    )
    avatar_plan, proxy_plan = Format02AvatarPerformanceAdapterService().compile_from_format02_scene(scene)
    assert avatar_plan.format_use == AvatarFormatUse.FORMAT_02
    assert not avatar_plan.lip_sync_enabled
    assert proxy_plan is not None
    assert proxy_plan.sfl_function == "relevant_open_question"


def test_evaluate_performance_plan_passes_valid_plan():
    plan = AvatarPerformanceLayerService().compile_performance_plan(avatar_id="coach_avatar_v1", scene_id="scene_1")
    receipt = AvatarPerformanceEvalService().evaluate_performance_plan(plan)
    assert receipt.pass_status == PassStatus.PASS
