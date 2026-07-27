import pytest

from ccp_studio.contracts.render_qa import MotionPromiseLevel, ObservedMotionLevel, PassStatus
from ccp_studio.contracts.studio_pipeline_recipe_harness import (
    PipelineArtifactRole,
    PipelineStepReceipt,
    PipelineStepStatus,
)
from ccp_studio.services.pipeline_render_qa_bridge_service import PipelineRenderQABridgeService
from ccp_studio.services.render_qa_service import RenderQAService


def _failing_report():
    svc = RenderQAService()
    file_ref = "workspace://renders/final.mp4"
    profile = svc.promise_profile(
        delivery_id="delivery_final",
        expected_width=1080,
        expected_height=1920,
        expected_duration_ms=24000,
    )
    return svc.composite(
        file_ref=file_ref,
        ffprobe_validation=svc.ffprobe(
            file_ref=file_ref,
            playable=True,
            duration_ms=24000,
            width=1080,
            height=1920,
            fps=30,
            video_codec="h264",
            audio_codec="aac",
            expected_width=1080,
            expected_height=1920,
        ),
        frame_sampling=svc.frame_sampling(
            file_ref=file_ref,
            sampled_frame_count=1,
            expected_scene_count=8,
        ),
        audio_level_analysis=svc.audio(file_ref=file_ref, integrated_lufs=-14, true_peak_db=-1.5),
        caption_burn_check=svc.captions(
            file_ref=file_ref,
            captions_required=True,
            captions_detected=True,
            burned_caption_detected=True,
        ),
        visual_regression=svc.visual_regression(
            file_ref=file_ref,
            screenshot_refs=["s1"],
            baseline_refs=["b1"],
            observed_max_drift=0.02,
        ),
        motion_downgrade=svc.motion(
            file_ref=file_ref,
            promised_motion_level=MotionPromiseLevel.STANDARD,
            observed_motion_level=ObservedMotionLevel.STANDARD,
        ),
        delivery_promise=svc.delivery(
            file_ref=file_ref,
            promise_profile=profile,
            actual_width=1080,
            actual_height=1920,
            actual_duration_ms=24000,
            captions_pass=True,
            motion_pass=True,
            negative_space_ratio=0.35,
            identity_consistency=0.95,
            composition_quality=0.9,
            style_consistency=0.9,
            emotional_accuracy=0.85,
            platform_fit=0.88,
            hook_strength=0.82,
            shareability=0.75,
            routeability=0.9,
        ),
    )


def test_render_qa_report_maps_to_pipeline_qa_artifact_ref():
    report = _failing_report()
    bridge = PipelineRenderQABridgeService()
    artifact = bridge.report_artifact_ref(report, workspace_id="workspace_1", run_id="run_1")
    assert artifact.role == PipelineArtifactRole.QA_RECEIPT
    assert artifact.uri.startswith("render_qa://composite/")
    assert artifact.source_ref_ids == [report.file_ref]
    assert bridge.provider_calls_executed is False
    assert bridge.renderer_calls_executed is False
    assert bridge.local_worker_jobs_executed is False


def test_render_qa_failure_maps_to_pipeline_blocker_and_blocks_pass_receipt():
    report = _failing_report()
    blockers = PipelineRenderQABridgeService().blockers_from_report(report, step_id="render_qa")
    assert report.pass_status == PassStatus.FAIL
    assert blockers
    assert blockers[0].step_id == "render_qa"
    assert any(blocker.code == "insufficient_frame_samples" for blocker in blockers)
    with pytest.raises(ValueError):
        PipelineStepReceipt(
            pipeline_step_run_id="pipeline_step_run_qa",
            step_id="render_qa",
            status=PipelineStepStatus.BLOCKED,
            pass_status=PassStatus.PASS,
            blockers=blockers,
        )
