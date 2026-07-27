import pytest

from ccp_studio.contracts.video_editing_engine import (
    CaptionCue,
    CaptionTrack,
    FaceSafeZoneReceipt,
    FinalRenderContract,
    Format02SceneRealizationPlan,
    Format03SceneRealizationPlan,
    Format04SceneRealizationPlan,
    MemeticCueLedger,
    MotionCueType,
    PassStatus,
    VideoAvatarPerformanceRef,
    VideoCompositionSceneRef,
    VideoEditingProject,
    VideoExportPack,
    VideoFormatId,
    VideoFormatProgramRef,
    VideoFrameProfile,
    VideoLayerProgram,
    VideoLayerRole,
    VideoMotionCue,
    VideoSceneBoundary,
    VideoSourceAssetSet,
    VideoSourceMedia,
    VideoTrackProgram,
    VideoTrackType,
)
from ccp_studio.contracts.format02_composition_intelligence import Format02SceneRole
from ccp_studio.services.format02_avatar_performance_adapter_service import Format02AvatarPerformanceAdapterService
from ccp_studio.services.format02_composition_service import Format02CompositionService
from ccp_studio.services.video_editing_engine_service import VideoEditingEngineService
from ccp_studio.services.video_eval_service import VideoEvalService
from ccp_studio.services.video_render_contract_service import VideoRenderContractService
from ccp_studio.services.video_scene_realization_service import VideoSceneRealizationService
from ccp_studio.services.video_timeline_service import VideoTimelineService
from ccp_studio.services.video_audio_service import VideoAudioService
from ccp_studio.services.video_revision_service import VideoRevisionService
from ccp_studio.services.video_export_service import VideoExportService


def _source_media():
    return VideoSourceMedia(source_ref="src_video_1", media_type="video", uri="file://source.mp4", duration_ms=60000, width=1920, height=1080, fps=30)


def _source_set():
    return VideoSourceAssetSet(source_media=[_source_media()], source_span_refs=["span_1"], asset_hashes={"a": "h"})


def _format_ref(format_id=VideoFormatId.FORMAT_02):
    return VideoFormatProgramRef(format_program_id="format_program_1", format_id=format_id, source_span_refs=["span_1"])


def _composition_ref(format_id=VideoFormatId.FORMAT_02, locked=True):
    return VideoCompositionSceneRef(composition_scene_id="composition_scene_1", format_id=format_id, locked=locked)


def _avatar_ref(lip_sync=False):
    return VideoAvatarPerformanceRef(avatar_performance_plan_id="avatar_plan_1", lip_sync_enabled=lip_sync)


def _basic_timeline(format_id=VideoFormatId.FORMAT_02):
    service = VideoTimelineService()
    layer = service.make_layer(
        layer_role=VideoLayerRole.AVATAR_PERFORMANCE if format_id == VideoFormatId.FORMAT_02 else VideoLayerRole.PRIMARY_SOURCE,
        start_ms=0,
        end_ms=5000,
        frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER if format_id == VideoFormatId.FORMAT_02 else VideoFrameProfile.NINE_SIXTEEN_FULL_VERTICAL,
        asset_ref="asset_1",
    )
    track = service.make_track(VideoTrackType.AVATAR if format_id == VideoFormatId.FORMAT_02 else VideoTrackType.A_ROLL, [layer])
    timing = service.compile_scene_timing_plan([VideoSceneBoundary(scene_id="scene_1", start_ms=0, end_ms=5000, scene_role="hook")])
    return service.compile_timeline_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        project_id="project_1",
        variant_id="variant_1",
        frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER if format_id == VideoFormatId.FORMAT_02 else VideoFrameProfile.NINE_SIXTEEN_FULL_VERTICAL,
        duration_ms=5000,
        source_asset_set_id="source_set_1",
        format_program_refs=[_format_ref(format_id)],
        composition_scene_refs=[_composition_ref(format_id)] if format_id == VideoFormatId.FORMAT_02 else [],
        avatar_performance_plan_refs=[_avatar_ref()] if format_id == VideoFormatId.FORMAT_02 else [],
        tracks=[track],
        scene_timing_plan=timing,
    )


def test_video_project_requires_brand_context_version():
    with pytest.raises(Exception):
        VideoEditingProject(brand_id="brand_1", brand_context_version_id="", title="Video")


def test_16_9_rejected_as_delivery():
    with pytest.raises(Exception):
        VideoLayerProgram(
            layer_role=VideoLayerRole.PRIMARY_SOURCE,
            start_ms=0,
            end_ms=1000,
            frame_profile="16:9_SOURCE_INTERVIEW",
        )


def test_source_asset_set_requires_source_refs():
    with pytest.raises(Exception):
        VideoSourceAssetSet(source_media=[_source_media()], source_span_refs=[])


def test_timeline_requires_format_program_refs():
    service = VideoTimelineService()
    layer = service.make_layer(layer_role=VideoLayerRole.PRIMARY_SOURCE, start_ms=0, end_ms=1000, frame_profile=VideoFrameProfile.NINE_SIXTEEN_FULL_VERTICAL)
    track = service.make_track(VideoTrackType.A_ROLL, [layer])
    timing = service.compile_scene_timing_plan([VideoSceneBoundary(scene_id="s", start_ms=0, end_ms=1000, scene_role="hook")])
    with pytest.raises(Exception):
        service.compile_timeline_program(
            brand_id="brand",
            brand_context_version_id="bcv",
            project_id="p",
            variant_id="v",
            frame_profile=VideoFrameProfile.NINE_SIXTEEN_FULL_VERTICAL,
            duration_ms=1000,
            source_asset_set_id="ss",
            format_program_refs=[],
            composition_scene_refs=[],
            avatar_performance_plan_refs=[],
            tracks=[track],
            scene_timing_plan=timing,
        )


def test_timeline_requires_composition_scene_refs_for_format02():
    service = VideoTimelineService()
    layer = service.make_layer(layer_role=VideoLayerRole.AVATAR_PERFORMANCE, start_ms=0, end_ms=1000, frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER)
    track = service.make_track(VideoTrackType.AVATAR, [layer])
    timing = service.compile_scene_timing_plan([VideoSceneBoundary(scene_id="s", start_ms=0, end_ms=1000, scene_role="explain")])
    with pytest.raises(Exception):
        service.compile_timeline_program(
            brand_id="brand",
            brand_context_version_id="bcv",
            project_id="p",
            variant_id="v",
            frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
            duration_ms=1000,
            source_asset_set_id="ss",
            format_program_refs=[_format_ref(VideoFormatId.FORMAT_02)],
            composition_scene_refs=[],
            avatar_performance_plan_refs=[_avatar_ref()],
            tracks=[track],
            scene_timing_plan=timing,
        )


def test_scene_boundaries_are_time_sorted():
    with pytest.raises(Exception):
        VideoTimelineService().compile_scene_timing_plan([
            VideoSceneBoundary(scene_id="s2", start_ms=1000, end_ms=2000, scene_role="b"),
            VideoSceneBoundary(scene_id="s1", start_ms=0, end_ms=900, scene_role="a"),
        ])


def test_track_layers_have_positive_duration():
    with pytest.raises(Exception):
        VideoLayerProgram(layer_role=VideoLayerRole.PRIMARY_SOURCE, start_ms=1000, end_ms=1000, frame_profile=VideoFrameProfile.NINE_SIXTEEN_FULL_VERTICAL)


def test_final_render_rejects_provider_calls():
    with pytest.raises(Exception):
        FinalRenderContract(timeline_program_id="timeline", timeline_locked=True, asset_hashes={"a": "hash"}, provider_calls_allowed=True)


def test_export_requires_approved_variant():
    with pytest.raises(Exception):
        VideoExportPack(variant_id="v", final_render_receipt_id="final", approved_variant=False, output_files=["file.mp4"])


def test_format01_requires_aroll_spine():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format01(aroll_story_spine_ref="", broll_story_functions=["contrast"])


def test_format01_broll_requires_story_function():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format01(aroll_story_spine_ref="spine", broll_story_functions=["pretty_filler"])


def test_format01_preserves_emotional_pause():
    plan = VideoSceneRealizationService().compile_format01(
        aroll_story_spine_ref="spine",
        broll_story_functions=["contrast"],
        emotional_pause_refs=["pause_1"],
    )
    assert plan.emotional_pause_refs == ["pause_1"]


def test_format02_requires_locked_composition_scene():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format02(
            composition_scene_refs=[_composition_ref(locked=False)],
            avatar_performance_refs=[_avatar_ref()],
        )


def test_format02_requires_avatar_performance_plan():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format02(
            composition_scene_refs=[_composition_ref()],
            avatar_performance_refs=[],
        )


def test_format02_rejects_lipsync_avatar_plan():
    with pytest.raises(Exception):
        _avatar_ref(lip_sync=True)


def test_format02_preserves_cognitive_load_budget():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format02(
            composition_scene_refs=[_composition_ref()],
            avatar_performance_refs=[_avatar_ref()],
            cognitive_load_budget_preserved=False,
        )


def test_format02_real_life_cutout_motion_rejects_morph():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format02(
            composition_scene_refs=[_composition_ref()],
            avatar_performance_refs=[_avatar_ref()],
            real_life_cutout_motion_policy=["slide_in", "morph"],
        )


def test_format03_requires_proof_surface():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format03(
            proof_or_quote_surface_ref="",
            stimulus_time_ms=1000,
            reaction_start_ms=1200,
            rough_notation_speech_timing_refs=["speech_1"],
        )


def test_format03_reaction_timing_after_stimulus():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format03(
            proof_or_quote_surface_ref="proof",
            stimulus_time_ms=1200,
            reaction_start_ms=1000,
            rough_notation_speech_timing_refs=["speech_1"],
        )


def test_format03_rough_notation_requires_speech_timing():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format03(
            proof_or_quote_surface_ref="proof",
            stimulus_time_ms=1000,
            reaction_start_ms=1200,
            rough_notation_speech_timing_refs=[],
        )


def test_format04_requires_debate_tension():
    with pytest.raises(Exception):
        VideoSceneRealizationService().compile_format04(
            debate_tension_ref="",
            reaction_ui_surface_ref="ui",
            zoom_motion_cues=[],
            cue_times_ms=[],
        )


def test_format04_memetic_cue_spacing_is_10s():
    with pytest.raises(Exception):
        MemeticCueLedger(format_id=VideoFormatId.FORMAT_04, cue_times_ms=[0, 5000])


def test_format04_zoom_events_require_argument_shift():
    with pytest.raises(Exception):
        VideoMotionCue(cue_type=MotionCueType.SNAP_ZOOM, start_ms=0, end_ms=500, reason="zoom")


def test_caption_track_blocks_face_collision():
    with pytest.raises(Exception):
        CaptionTrack(cues=[CaptionCue(text="Hello", start_ms=0, end_ms=1000)], collision_with_face=True)


def test_sound_cue_timeline_enforces_memetic_limit():
    with pytest.raises(Exception):
        VideoAudioService().compile_memetic_cue_ledger(format_id=VideoFormatId.FORMAT_01, cue_times_ms=[0, 10000])


def test_remotion_props_include_timeline_program_id():
    timeline = _basic_timeline(VideoFormatId.FORMAT_02)
    props = VideoRenderContractService().compile_remotion_input_props(timeline)
    assert props.input_props["timeline_program_id"] == timeline.timeline_program_id


def test_otio_audit_timeline_compiles():
    timeline = _basic_timeline(VideoFormatId.FORMAT_02)
    otio = VideoRenderContractService().compile_otio_audit_timeline(timeline)
    assert otio.timeline_program_id == timeline.timeline_program_id
    assert otio.tracks_summary


def test_fake_proxy_render_receipt_has_hash():
    timeline = _basic_timeline(VideoFormatId.FORMAT_02)
    renderer = VideoRenderContractService()
    props = renderer.compile_remotion_input_props(timeline)
    contract = renderer.compile_proxy_render_contract(timeline, props)
    receipt = renderer.execute_proxy_render_fake(contract)
    assert receipt.output_sha256
    assert receipt.fake_render


def test_video_eval_blocks_timeline_integrity_failure():
    timeline = _basic_timeline(VideoFormatId.FORMAT_02)
    receipt = VideoEvalService().run_eval(timeline, timeline_integrity_pass=False)
    assert receipt.pass_status == PassStatus.FAIL
    assert "timeline_integrity_failure" in receipt.blockers


def test_operator_revision_compiles_typed_command():
    service = VideoRevisionService()
    command = service.compile_revision_command(command_type="move_caption", target_ref="caption_1", reason="face collision")
    receipt = service.apply_revision_fake(command)
    assert receipt.applied


def test_full_fake_video_engine_path_format02():
    engine = VideoEditingEngineService()
    project = engine.create_project(brand_id="brand_1", brand_context_version_id="bcv_1", title="Format 02 Demo")
    variant = engine.create_variant(project_id=project.video_project_id, frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER, target_duration_ms=5000)
    source_set = engine.sources.compile_source_asset_set(source_media=[_source_media()], source_span_refs=["span_1"])
    format_ref = _format_ref(VideoFormatId.FORMAT_02)
    comp_ref = _composition_ref(VideoFormatId.FORMAT_02)
    avatar_ref = _avatar_ref()
    layer = engine.timeline.make_layer(layer_role=VideoLayerRole.AVATAR_PERFORMANCE, start_ms=0, end_ms=5000, frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER, asset_ref="avatar_asset")
    track = engine.timeline.make_track(VideoTrackType.AVATAR, [layer])
    timing = engine.timeline.compile_scene_timing_plan([VideoSceneBoundary(scene_id="scene_1", start_ms=0, end_ms=5000, scene_role="explain")])
    timeline = engine.timeline.compile_timeline_program(
        brand_id=project.brand_id,
        brand_context_version_id=project.brand_context_version_id,
        project_id=project.video_project_id,
        variant_id=variant.video_variant_id,
        frame_profile=variant.frame_profile,
        duration_ms=5000,
        source_asset_set_id=source_set.source_asset_set_id,
        format_program_refs=[format_ref],
        composition_scene_refs=[comp_ref],
        avatar_performance_plan_refs=[avatar_ref],
        tracks=[track],
        scene_timing_plan=timing,
    )
    props = engine.render.compile_remotion_input_props(timeline)
    proxy_contract = engine.render.compile_proxy_render_contract(timeline, props)
    proxy = engine.render.execute_proxy_render_fake(proxy_contract)
    evaluation = engine.eval.run_eval(timeline)
    assert evaluation.pass_status == PassStatus.PASS
    engine.lock_final_timeline(timeline)
    final_contract = engine.render.compile_final_render_contract(timeline, asset_hashes={"avatar_asset": "hash"})
    final = engine.render.execute_final_render_fake(final_contract)
    approval = engine.export.prepare_approval(variant_id=variant.video_variant_id, evaluation=evaluation, final_render=final, approved=True)
    export = engine.export.compile_export_pack(variant_id=variant.video_variant_id, final_render=final, approved_variant=approval.approved)
    assert proxy.output_sha256
    assert export.output_files


def test_format02_composition_and_avatar_plan_can_attach_to_video_timeline():
    scene = Format02CompositionService().compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="format02_scene_1",
        scene_role=Format02SceneRole.TRUTH_DEFINE,
        concept_statement="Healing takes time.",
        headline_text="Healing takes time.",
    )
    avatar_plan, proxy_plan = Format02AvatarPerformanceAdapterService().compile_from_format02_scene(scene)
    assert proxy_plan is not None
    assert not avatar_plan.lip_sync_enabled

    composition_program = scene.composition_scene_program
    assert composition_program is not None
    composition_ref = VideoCompositionSceneRef(
        composition_scene_id=composition_program.composition_scene_program_id,
        format_id=VideoFormatId.FORMAT_02,
        locked=True,
        cognitive_load_receipt_ref="cognitive_load_pass_1",
    )
    avatar_ref = VideoAvatarPerformanceRef(
        avatar_performance_plan_id=avatar_plan.avatar_performance_plan_id,
        lip_sync_enabled=avatar_plan.lip_sync_enabled,
        source_scene_ref=scene.scene_id,
    )

    source_set = VideoSourceAssetSet(source_media=[_source_media()], source_span_refs=["span_1"], asset_hashes={"avatar_asset": "hash"})
    timeline_service = VideoTimelineService()
    layer = timeline_service.make_layer(
        layer_role=VideoLayerRole.AVATAR_PERFORMANCE,
        start_ms=0,
        end_ms=4000,
        frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
        asset_ref=avatar_plan.avatar_id,
    )
    track = timeline_service.make_track(VideoTrackType.AVATAR, [layer])
    timing = timeline_service.compile_scene_timing_plan(
        [VideoSceneBoundary(scene_id=scene.scene_id, start_ms=0, end_ms=4000, scene_role=scene.scene_role.value)]
    )
    timeline = timeline_service.compile_timeline_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        project_id="video_project_1",
        variant_id="video_variant_1",
        frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
        duration_ms=4000,
        source_asset_set_id=source_set.source_asset_set_id,
        format_program_refs=[_format_ref(VideoFormatId.FORMAT_02)],
        composition_scene_refs=[composition_ref],
        avatar_performance_plan_refs=[avatar_ref],
        tracks=[track],
        scene_timing_plan=timing,
    )
    renderer = VideoRenderContractService()
    props = renderer.compile_remotion_input_props(timeline)
    proxy_contract = renderer.compile_proxy_render_contract(timeline, props)
    proxy_receipt = renderer.execute_proxy_render_fake(proxy_contract)

    assert timeline.composition_scene_refs[0].composition_scene_id == composition_program.composition_scene_program_id
    assert timeline.avatar_performance_plan_refs[0].avatar_performance_plan_id == avatar_plan.avatar_performance_plan_id
    assert proxy_receipt.fake_render
    assert proxy_receipt.output_sha256
