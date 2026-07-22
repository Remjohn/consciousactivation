from ccp_studio.contracts.render_qa import MotionPromiseLevel, ObservedMotionLevel, PassStatus
from ccp_studio.services.render_qa_service import RenderQAService


def _passing():
    svc = RenderQAService()
    file_ref = "workspace://render/final.mp4"
    profile = svc.promise_profile(delivery_id="d1", expected_width=1080, expected_height=1920, expected_duration_ms=24000)
    return {
        "file_ref": file_ref,
        "ffprobe_validation": svc.ffprobe(file_ref=file_ref, playable=True, duration_ms=24000, width=1080, height=1920, fps=30, video_codec="h264", audio_codec="aac", expected_width=1080, expected_height=1920),
        "frame_sampling": svc.frame_sampling(file_ref=file_ref, sampled_frame_count=8, expected_scene_count=8),
        "audio_level_analysis": svc.audio(file_ref=file_ref, integrated_lufs=-14, true_peak_db=-1.5),
        "caption_burn_check": svc.captions(file_ref=file_ref, captions_required=True, captions_detected=True, burned_caption_detected=True),
        "visual_regression": svc.visual_regression(file_ref=file_ref, screenshot_refs=["s1"], baseline_refs=["b1"], observed_max_drift=0.03),
        "character_qa": svc.character(file_ref=file_ref, character_id="coach", identity_consistency_score=.95, face_plate_consistency_score=.94, body_layer_consistency_score=.93, style_consistency_score=.92),
        "motion_downgrade": svc.motion(file_ref=file_ref, promised_motion_level=MotionPromiseLevel.STANDARD, observed_motion_level=ObservedMotionLevel.STANDARD),
        "delivery_promise": svc.delivery(file_ref=file_ref, promise_profile=profile, actual_width=1080, actual_height=1920, actual_duration_ms=24100, captions_pass=True, motion_pass=True, negative_space_ratio=.35, identity_consistency=.95, composition_quality=.9, style_consistency=.9, emotional_accuracy=.85, platform_fit=.88, hook_strength=.82, shareability=.75, routeability=.9),
        "rendered_asset_evaluation": svc.evaluation(file_ref=file_ref, identity_consistency=.95, composition_quality=.9, style_consistency=.9, emotional_accuracy=.85, platform_fit=.88, negative_space_compliance=.9, hook_strength=.82, shareability=.75, routeability=.9),
    }


def test_composite_report_passes_all_receipts():
    report = RenderQAService().composite(**_passing())
    assert report.pass_status == PassStatus.PASS
    assert not report.blockers


def test_ffprobe_blocks_unplayable_and_dimension_mismatch():
    r = RenderQAService().ffprobe(file_ref="x.mp4", playable=False, duration_ms=1000, width=720, height=1280, fps=30, video_codec="h264", expected_width=1080, expected_height=1920)
    assert r.pass_status == PassStatus.FAIL
    assert {"not_playable", "width_mismatch", "height_mismatch"}.issubset({b.code for b in r.blockers})


def test_frame_sampling_blocks_black_and_insufficient_frames():
    r = RenderQAService().frame_sampling(file_ref="x.mp4", sampled_frame_count=1, expected_scene_count=8, black_frame_count=1)
    assert r.pass_status == PassStatus.FAIL
    assert "insufficient_frame_samples" in {b.code for b in r.blockers}
    assert "black_frames_detected" in {b.code for b in r.blockers}


def test_audio_blocks_loudness_peak_and_clipping():
    r = RenderQAService().audio(file_ref="x.mp4", integrated_lufs=-24, true_peak_db=0.5, clipping_detected=True)
    assert r.pass_status == PassStatus.FAIL
    assert "integrated_lufs_out_of_tolerance" in {b.code for b in r.blockers}
    assert "true_peak_exceeds_limit" in {b.code for b in r.blockers}
    assert "audio_clipping_detected" in {b.code for b in r.blockers}


def test_caption_burn_blocks_missing_required_captions():
    r = RenderQAService().captions(file_ref="x.mp4", captions_required=True, captions_detected=False)
    assert r.pass_status == PassStatus.FAIL
    assert "captions_required_but_missing" in {b.code for b in r.blockers}


def test_visual_regression_blocks_drift():
    r = RenderQAService().visual_regression(file_ref="x.mp4", screenshot_refs=["s"], baseline_refs=["b"], observed_max_drift=.25)
    assert r.pass_status == PassStatus.FAIL
    assert "visual_drift_exceeds_threshold" in {b.code for b in r.blockers}


def test_character_qa_blocks_identity_drift():
    r = RenderQAService().character(file_ref="x.mp4", character_id="coach", identity_consistency_score=.5, face_plate_consistency_score=.95, body_layer_consistency_score=.95, style_consistency_score=.95)
    assert r.pass_status == PassStatus.FAIL
    assert "identity_consistency_failed" in {b.code for b in r.blockers}


def test_motion_downgrade_blocks_static_output_when_motion_promised():
    r = RenderQAService().motion(file_ref="x.mp4", promised_motion_level=MotionPromiseLevel.STANDARD, observed_motion_level=ObservedMotionLevel.STATIC)
    assert r.pass_status == PassStatus.FAIL
    assert "motion_missing" in {b.code for b in r.blockers}


def test_operator_approved_motion_downgrade_warns_not_passes():
    r = RenderQAService().motion(file_ref="x.mp4", promised_motion_level=MotionPromiseLevel.STANDARD, observed_motion_level=ObservedMotionLevel.SUBTLE, operator_downgrade_approved=True)
    assert r.pass_status == PassStatus.WARN
    assert "motion_downgrade_operator_approved" in {b.code for b in r.blockers}


def test_delivery_promise_blocks_v9_metrics_and_delivery_mismatch():
    svc = RenderQAService()
    profile = svc.promise_profile(delivery_id="d1", expected_width=1080, expected_height=1920, expected_duration_ms=24000)
    r = svc.delivery(file_ref="x.mp4", promise_profile=profile, actual_width=720, actual_height=1280, actual_duration_ms=26000, captions_pass=False, motion_pass=False, negative_space_ratio=.1, identity_consistency=.5, composition_quality=.5, style_consistency=.5, emotional_accuracy=.5, platform_fit=.5, hook_strength=.5, shareability=.5, routeability=.5)
    assert r.pass_status == PassStatus.FAIL
    codes = {b.code for b in r.blockers}
    assert "delivery_dimensions_mismatch" in codes
    assert "delivery_duration_out_of_tolerance" in codes
    assert "routeability_below_minimum" in codes


def test_composite_report_fails_with_blocking_receipt():
    parts = _passing()
    parts["frame_sampling"] = RenderQAService().frame_sampling(file_ref=parts["file_ref"], sampled_frame_count=1, expected_scene_count=8)
    report = RenderQAService().composite(**parts)
    assert report.pass_status == PassStatus.FAIL
    assert "insufficient_frame_samples" in {b.code for b in report.blockers}
