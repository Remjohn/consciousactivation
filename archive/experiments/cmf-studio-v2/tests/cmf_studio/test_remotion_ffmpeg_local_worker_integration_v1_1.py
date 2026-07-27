from ccp_studio.contracts.local_render_worker import RenderJobType
from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    CompleteEditingSessionRenderStateWrapper,
    FFmpegFinishJob,
    MemeticSoundCueModerationReceipt,
    MotionCueName,
    MotionVocabularyPolicyReceipt,
    RemotionRenderJob,
    RenderLayerName,
    SevenLayerCompositionPayload,
    VideoFormatId,
)
from ccp_studio.services.ffmpeg_finish_adapter_service import FFmpegFinishAdapterService
from ccp_studio.services.local_render_worker_service import LocalRenderWorkerService
from ccp_studio.services.remotion_ffmpeg_render_orchestrator_service import RemotionFFmpegRenderOrchestratorService
from ccp_studio.services.remotion_render_adapter_service import RemotionRenderAdapterService
from ccp_studio.services.render_job_lease_service import RenderJobLeaseService
from ccp_studio.services.render_job_queue_service import RenderJobQueueService
from ccp_studio.services.render_job_result_service import RenderJobResultService


def _wrapper() -> CompleteEditingSessionRenderStateWrapper:
    return CompleteEditingSessionRenderStateWrapper(
        complete_editing_session_ref="ces_local_worker",
        brand_context_version_id="bcv_local_worker",
        research_snapshot_refs=["research_snapshot_local_worker"],
        asset_manifest_refs=["asset_manifest_local_worker"],
        scene_spec_refs=["scene_spec_local_worker"],
        composition_job_refs=["composition_job_local_worker"],
        provider_job_receipt_refs=["provider_receipt_local_worker"],
        evaluation_receipt_refs=["eval_receipt_local_worker"],
    )


def _seven_layers() -> SevenLayerCompositionPayload:
    return SevenLayerCompositionPayload(
        layer_refs={
            RenderLayerName.BACKGROUND: ["background_layer"],
            RenderLayerName.PROOF_OBJECT: ["proof_layer"],
            RenderLayerName.REAL_LIFE_CUTOUT: ["cutout_layer"],
            RenderLayerName.AVATAR: ["avatar_layer"],
            RenderLayerName.TEXT: ["text_layer"],
            RenderLayerName.ANNOTATION: ["annotation_layer"],
            RenderLayerName.FOREGROUND_FX: ["fx_layer"],
        }
    )


def test_remotion_ffmpeg_dry_run_pipeline_can_coexist_with_fake_local_worker():
    worker = LocalRenderWorkerService().register_worker(
        worker_id="worker_remotion_dry_run",
        machine_id="machine_remotion_dry_run",
        display_name="Dry Run Worker",
    )
    queue_service = RenderJobQueueService()
    job = queue_service.create_job(
        job_type=RenderJobType.PROXY_VIDEO_RENDER,
        job_name="Dry-run Remotion proxy render",
        payload={"timeline_program_id": "timeline_remotion_dry_run"},
    )
    queue = queue_service.enqueue(queue_service.create_queue(), job)
    lease = RenderJobLeaseService().lease_job(job=queue.queued_jobs[0], worker=worker)
    worker_result = RenderJobResultService().complete_fake_result(job=job, worker=worker, lease=lease)

    remotion_job = RemotionRenderJob(
        timeline_program_id="timeline_remotion_dry_run",
        composition_id="Format02SceneComposition",
        entry_point="remotion/index.ts",
        output_path="client_workspaces/demo/runs/run_1/renders/proxy.mp4",
        input_props_ref="client_workspaces/demo/runs/run_1/timeline/props.json",
        complete_editing_session_state=_wrapper(),
        seven_layer_payload=_seven_layers(),
        motion_vocabulary_receipt=MotionVocabularyPolicyReceipt(
            requested_motion_cues=[MotionCueName.PAPER_SLIDE_IN]
        ),
        memetic_sound_receipt=MemeticSoundCueModerationReceipt(
            format_id=VideoFormatId.FORMAT_02,
            cue_times_ms=[0, 31000],
        ),
        duration_in_frames=720,
    )
    ffmpeg_job = FFmpegFinishJob(
        input_path="client_workspaces/demo/runs/run_1/renders/proxy.mp4",
        output_path="client_workspaces/demo/runs/run_1/exports/final.mp4",
    )

    result = RemotionFFmpegRenderOrchestratorService(
        remotion_service=RemotionRenderAdapterService(),
        ffmpeg_service=FFmpegFinishAdapterService(),
    ).execute_dry_run_pipeline(remotion_job=remotion_job, ffmpeg_job=ffmpeg_job)

    assert worker_result.output_uri.startswith("fake://local-render-worker/proxy_video_render/")
    assert result["remotion_result"].output_uri.startswith("dry-run://")
    assert result["ffmpeg_result"].output_uri.startswith("dry-run://")
    assert result["remotion_result"].external_runtime_calls_executed is False
    assert result["ffmpeg_result"].external_runtime_calls_executed is False
