from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    PassStatus,
    VideoFormatId,
    VideoFormatProgramRef,
    VideoFrameProfile,
    VideoLayerProgram,
    VideoLayerRole,
    VideoSceneBoundary,
    VideoSourceMedia,
    VideoTimelineProgram,
    VideoTrackProgram,
    VideoTrackType,
    stable_hash,
)
from ccp_studio.contracts.local_render_worker import RenderJobType
from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    CompleteEditingSessionRenderStateWrapper,
    MemeticSoundCueModerationReceipt,
    MotionCueName,
    MotionVocabularyPolicyReceipt,
    RemotionRenderJob,
    RenderLayerName,
    SevenLayerCompositionPayload,
    VideoFormatId as RenderAdapterVideoFormatId,
)
from ccp_studio.contracts.video_timeline_workbench import (
    OTIOExportRequest,
    OTIOExportResponse,
    ProxyRenderRequest,
    ProxyRenderResponse,
    TimelineClipSegment,
    TimelineMarker,
    TimelineTimeRange,
    TimelineTrackLane,
    VideoTimelineEditProposal,
    VideoTimelineEditProposalResult,
    VideoTimelineEditReceipt,
    VideoTimelineEditSubmission,
    VideoTimelineWorkbenchEvalSummary,
    VideoTimelineWorkbenchLayer,
    VideoTimelineWorkbenchProgramSummary,
    VideoTimelineWorkbenchReadModel,
    VideoTimelineWorkbenchRenderSummary,
    VideoTimelineWorkbenchScene,
    VideoTimelineWorkbenchTrack,
    VideoWorkbenchRenderJobState,
    VideoWorkbenchRenderQAReadModel,
)
from ccp_studio.services.audio_level_analysis_service import AudioLevelAnalysisService
from ccp_studio.services.duration_tolerance_service import DurationToleranceService
from ccp_studio.services.ffprobe_validation_service import FFprobeValidationService
from ccp_studio.services.frame_sampling_service import FrameSamplingService
from ccp_studio.services.local_render_worker_orchestrator_service import LocalRenderWorkerOrchestratorService
from ccp_studio.services.remotion_render_adapter_service import RemotionRenderAdapterService
from ccp_studio.services.render_qa_service import RenderQAService
from ccp_studio.services.video_editing_engine_service import VideoEditingEngineService
from ccp_studio.services.video_render_contract_service import VideoRenderContractService
from ccp_studio.services.video_revision_service import VideoRevisionService


FORMAT_SLOT_META = {
    "SV-CSC": {
        "name": "Cinematic Story Commentary",
        "role": "Make them feel the story.",
        "previewHeadline": "A-roll spine",
        "previewSubhead": "memory object pacing",
        "sceneNote": "Backend timeline generated from Format 01 realization boundaries.",
    },
    "SV-EDU": {
        "name": "Educational / Explainer",
        "role": "Make them understand the idea.",
        "previewHeadline": "MYTH 1",
        "previewSubhead": "Natural does not always mean safe.",
        "sceneNote": "Format 02 paper-cut explainer with avatar, proxy, and text tracks.",
    },
    "SV-FRB": {
        "name": "Challenger / Frame Breaker",
        "role": "Make them reconsider the frame.",
        "previewHeadline": "PROOF CHECK",
        "previewSubhead": "the claim meets the source",
        "sceneNote": "Format 03 proof surface and reaction timing tracks.",
    },
    "SV-RRC": {
        "name": "Reaction / Recognition Clip",
        "role": "Make them trust the human moment.",
        "previewHeadline": "SOURCE TRUTH",
        "previewSubhead": "recognition before reaction",
        "sceneNote": "Format 04 conscious reaction UI and source track timing.",
    },
}


class VideoTimelineWorkbenchService:
    def __init__(
        self,
        video_engine: VideoEditingEngineService | None = None,
        renderer: VideoRenderContractService | None = None,
        revision: VideoRevisionService | None = None,
    ):
        self.video = video_engine or VideoEditingEngineService()
        self.renderer = renderer or self.video.render
        self.revision = revision or self.video.revision
        self.local_render = LocalRenderWorkerOrchestratorService()
        self.remotion_adapter = RemotionRenderAdapterService()
        self.ffprobe = FFprobeValidationService()
        self.frame_sampling = FrameSamplingService()
        self.audio_levels = AudioLevelAnalysisService()
        self.duration_tolerance = DurationToleranceService()
        self.render_qa = RenderQAService()
        self._timelines_by_program_id: dict[str, VideoTimelineProgram] = {}
        self._read_models_by_program_id: dict[str, VideoTimelineWorkbenchReadModel] = {}
        self._render_states_by_job_id: dict[str, VideoWorkbenchRenderJobState] = {}

    def get_current_workbench(self, format: str | None = None) -> VideoTimelineWorkbenchReadModel:
        format_slot = self._normalize_format_slot(format)
        for read_model in self._read_models_by_program_id.values():
            if read_model.format_slot == format_slot:
                return read_model
        timeline = self.build_demo_format02_timeline(format_slot=format_slot)
        return self.build_from_timeline(timeline, source_mode="demo", format_slot=format_slot)

    def get_workbench(self, program_id: str) -> VideoTimelineWorkbenchReadModel:
        if program_id in self._read_models_by_program_id:
            return self._read_models_by_program_id[program_id]
        timeline = self._timelines_by_program_id[program_id]
        return self.build_from_timeline(timeline, source_mode="backend")

    def build_from_timeline(
        self,
        timeline: VideoTimelineProgram,
        source_mode: str = "backend",
        format_slot: str | None = None,
    ) -> VideoTimelineWorkbenchReadModel:
        format_slot = format_slot or self._format_slot_for_timeline(timeline)
        source_span_refs = self._source_span_refs(timeline)
        remotion_props = self.renderer.compile_remotion_input_props(timeline)
        proxy_contract = self.renderer.compile_proxy_render_contract(timeline, remotion_props)
        proxy_receipt = self.renderer.execute_proxy_render_fake(proxy_contract)
        otio = self.renderer.compile_otio_audit_timeline(timeline)
        evaluation = self.video.eval.run_eval(timeline)

        scene_segments, scenes = self._scene_segments(timeline)
        track_lanes = [self._lane_from_track(track, timeline) for track in timeline.tracks]
        lanes = [
            TimelineTrackLane(
                lane_id="scene",
                display_name="Scene boundaries",
                lane_kind="scene",
                editable=False,
                segments=scene_segments,
            ),
            *track_lanes,
            self._eval_lane(timeline, evaluation),
            self._approval_lane(timeline, otio),
        ]
        tracks = [self._track_summary(track, timeline) for track in timeline.tracks]
        markers = self._markers(timeline, evaluation)
        selected_segment_id = next((segment.segment_id for lane in lanes for segment in lane.segments), None)
        object_version = f"{timeline.timeline_program_id}.v1"
        render_summary = VideoTimelineWorkbenchRenderSummary(
            render_type="proxy",
            status="ready",
            output_uri=proxy_receipt.output_uri,
            output_sha256=proxy_receipt.output_sha256,
            fake_render=proxy_receipt.fake_render,
        )
        otio_summary = VideoTimelineWorkbenchRenderSummary(
            render_type="otio",
            status="coverage-ready",
            output_uri=f"otio://audit/{otio.otio_audit_timeline_id}",
            fake_render=True,
        )
        eval_summary = VideoTimelineWorkbenchEvalSummary(
            evaluation_receipt_id=evaluation.video_evaluation_receipt_id,
            pass_status=evaluation.pass_status.value,
            blockers=evaluation.blockers,
        )
        program_summary = VideoTimelineWorkbenchProgramSummary(
            program_id=timeline.timeline_program_id,
            timeline_program_id=timeline.timeline_program_id,
            brand_id=timeline.brand_id,
            brand_context_version_id=timeline.brand_context_version_id,
            frame_profile=timeline.frame_profile.value,
            format_program_refs=[ref.format_program_id for ref in timeline.format_program_refs],
            source_span_refs=source_span_refs,
        )
        read_model = VideoTimelineWorkbenchReadModel(
            workbench_id=f"wb_{timeline.timeline_program_id}",
            program_id=timeline.timeline_program_id,
            timeline_program_id=timeline.timeline_program_id,
            brand_id=timeline.brand_id,
            brand_context_version_id=timeline.brand_context_version_id,
            brand_workspace_id=timeline.brand_id,
            guest_id="health_myth_demo",
            guest_name="Health Myth Demo",
            asset_code=f"CMF-{format_slot}-{timeline.timeline_program_id}",
            format_slot=format_slot,
            format_meta=FORMAT_SLOT_META[format_slot],
            frame_profile=timeline.frame_profile.value,
            fps=timeline.fps,
            duration_frames=self._ms_to_frames(timeline.duration_ms, timeline.fps),
            duration_ms=timeline.duration_ms,
            object_version=object_version,
            proxy_render_ref=proxy_receipt.output_uri,
            output_preview_url=proxy_receipt.output_uri,
            renderer_props_manifest_ref=remotion_props.remotion_input_props_id,
            renderer_props_hash=stable_hash(remotion_props.remotion_input_props_id),
            beat_map_ref=f"beatmap://{timeline.source_asset_set_id}",
            otio_manifest_ref=f"otio://audit/{otio.otio_audit_timeline_id}",
            playback_proxy_status="ready",
            contract_gate_status="valid" if evaluation.pass_status == PassStatus.PASS else "stale_contract",
            source_mode=source_mode,  # type: ignore[arg-type]
            source_span_refs=source_span_refs,
            program_summary=program_summary,
            scenes=scenes,
            tracks=tracks,
            lanes=lanes,
            markers=markers,
            captions=[],
            sound_cues=[],
            render_summaries=[render_summary, otio_summary],
            eval_summaries=[eval_summary],
            selected_segment_id=selected_segment_id,
            hard_blocker_codes=evaluation.blockers,
        )
        self._timelines_by_program_id[timeline.timeline_program_id] = timeline
        self._read_models_by_program_id[timeline.timeline_program_id] = read_model
        return read_model

    def build_demo_format02_timeline(self, format_slot: str | None = None) -> VideoTimelineProgram:
        format_slot = self._normalize_format_slot(format_slot)
        format_id = self._format_id_for_slot(format_slot)
        frame_profile = self._frame_profile_for_slot(format_slot)
        duration_ms = 24000
        project = self.video.create_project(
            brand_id="brand_health_demo",
            brand_context_version_id="bcv_health_demo_v1",
            title=f"{format_slot} Timeline Workbench Demo",
        )
        variant = self.video.create_variant(
            project_id=project.video_project_id,
            frame_profile=frame_profile,
            target_duration_ms=duration_ms,
        )
        source_media = VideoSourceMedia(
            source_ref="source://health_myth/transcript",
            media_type="text_fixture",
            uri="fixture://golden_path/health_myth_transcript.txt",
            duration_ms=duration_ms,
            width=1080,
            height=1920,
            fps=30,
        )
        source_set = self.video.sources.compile_source_asset_set(
            source_media=[source_media],
            source_span_refs=["span_health_myth_1"],
        )
        format_ref = VideoFormatProgramRef(
            format_program_id=f"format_program_{format_slot.lower()}",
            format_id=format_id,
            source_span_refs=source_set.source_span_refs,
        )
        boundaries = [
            VideoSceneBoundary(scene_id="scene_define", start_ms=0, end_ms=6000, scene_role="truth_define"),
            VideoSceneBoundary(scene_id="scene_contrast", start_ms=6000, end_ms=12000, scene_role="myth_contrast"),
            VideoSceneBoundary(scene_id="scene_mechanism", start_ms=12000, end_ms=18000, scene_role="mechanism"),
            VideoSceneBoundary(scene_id="scene_takeaway", start_ms=18000, end_ms=24000, scene_role="takeaway"),
        ]
        timing = self.video.timeline.compile_scene_timing_plan(boundaries)
        tracks = self._demo_tracks(format_slot, frame_profile, boundaries)
        composition_refs = []
        avatar_refs = []
        if format_id == VideoFormatId.FORMAT_02:
            from ccp_studio.contracts.video_editing_engine import VideoAvatarPerformanceRef, VideoCompositionSceneRef

            composition_refs = [
                VideoCompositionSceneRef(
                    composition_scene_id=f"composition_{boundary.scene_id}",
                    format_id=format_id,
                    locked=True,
                    cognitive_load_receipt_ref=f"cognitive_load_{boundary.scene_id}",
                )
                for boundary in boundaries
            ]
            avatar_refs = [
                VideoAvatarPerformanceRef(
                    avatar_performance_plan_id=f"avatar_plan_{boundary.scene_id}",
                    lip_sync_enabled=False,
                    source_scene_ref=boundary.scene_id,
                )
                for boundary in boundaries
            ]
        timeline = self.video.timeline.compile_timeline_program(
            brand_id=project.brand_id,
            brand_context_version_id=project.brand_context_version_id,
            project_id=project.video_project_id,
            variant_id=variant.video_variant_id,
            frame_profile=variant.frame_profile,
            duration_ms=duration_ms,
            source_asset_set_id=source_set.source_asset_set_id,
            format_program_refs=[format_ref],
            composition_scene_refs=composition_refs,
            avatar_performance_plan_refs=avatar_refs,
            tracks=tracks,
            scene_timing_plan=timing,
        )
        self.video.repository.upsert("source_asset_sets", source_set.source_asset_set_id, source_set)
        self.video.repository.upsert("timeline_programs", timeline.timeline_program_id, timeline)
        self._timelines_by_program_id[timeline.timeline_program_id] = timeline
        return timeline

    def propose_timeline_edit(self, program_id: str, request: VideoTimelineEditProposal) -> VideoTimelineEditProposalResult:
        if isinstance(request, dict):
            request = VideoTimelineEditProposal(**request)
        self._require_timeline(program_id)
        command = self.revision.compile_revision_command(
            command_type=request.edit_type,
            target_ref=request.target_segment_id,
            reason="timeline workbench proposal",
            payload=request.payload,
        )
        proposal_payload = self._dump_model(request)
        proposal_payload["draft_id"] = request.draft_id or f"draft_{command.operator_video_revision_command_id}"
        return VideoTimelineEditProposalResult(
            **proposal_payload,
            typed_revision_command_id=command.operator_video_revision_command_id,
        )

    def submit_timeline_edit(self, program_id: str, request: VideoTimelineEditSubmission) -> VideoTimelineEditReceipt:
        if isinstance(request, dict):
            request = VideoTimelineEditSubmission(**request)
        timeline = self._require_timeline(program_id)
        command = self.revision.compile_revision_command(
            command_type=request.edit_type,
            target_ref=request.target_segment_id or program_id,
            reason="timeline workbench submission",
            payload=request.payload,
        )
        revision_receipt = self.revision.apply_revision_fake(command)
        read_model = self._read_models_by_program_id.get(program_id) or self.build_from_timeline(timeline)
        object_version = f"{read_model.object_version}+draft"
        return VideoTimelineEditReceipt(
            receipt_id=revision_receipt.operator_video_revision_receipt_id,
            command_id=request.command_id,
            object_version=object_version,
            payload=request.payload,
            typed_revision_command_id=command.operator_video_revision_command_id,
            revision_receipt_id=revision_receipt.operator_video_revision_receipt_id,
            applied=revision_receipt.applied,
            target_segment_id=request.target_segment_id,
            edit_type=request.edit_type,
        )

    def create_proxy_render(self, program_id: str, request: ProxyRenderRequest | None = None) -> ProxyRenderResponse:
        timeline = self._require_timeline(program_id)
        props = self.renderer.compile_remotion_input_props(timeline)
        contract = self.renderer.compile_proxy_render_contract(timeline, props)
        receipt = self.renderer.execute_proxy_render_fake(contract)
        worker = self.local_render.workers.register_worker(
            worker_id="video_workbench_fake_worker",
            machine_id="video_workbench_local_machine",
            display_name="Video Workbench Fake Worker",
        )
        queue = self.local_render.queue.create_queue(queue_name="video_workbench_proxy_render")
        job = self.local_render.queue.create_job(
            job_type=RenderJobType.PROXY_VIDEO_RENDER,
            job_name=f"Proxy render for {program_id}",
            payload={
                "program_id": program_id,
                "timeline_program_id": timeline.timeline_program_id,
                "proxy_render_contract_id": contract.proxy_render_contract_id,
                "remotion_input_props_id": props.remotion_input_props_id,
                "output_profile": (request or ProxyRenderRequest()).output_profile,
            },
            requested_by=(request.requested_by_operator_id if request else None) or "video_timeline_workbench",
        )
        queue = self.local_render.queue.enqueue(queue, job)
        lease = self.local_render.leases.lease_job(job=queue.queued_jobs[0], worker=worker)
        self.local_render.heartbeats.record_heartbeat(worker=worker, active_job_ids=[job.render_job_id])
        worker_result = self.local_render.results.complete_fake_result(job=job, worker=worker, lease=lease)

        remotion_job = self._compile_dry_run_remotion_job(timeline=timeline, props_ref=props.remotion_input_props_id)
        remotion_result = self.remotion_adapter.execute_dry_run(remotion_job)
        output_uri = remotion_result.output_uri or worker_result.output_uri or receipt.output_uri
        output_sha256 = remotion_result.output_sha256 or worker_result.output_sha256 or receipt.output_sha256
        render_qa = self._compile_synthetic_render_qa(timeline=timeline, file_ref=output_uri)
        render_qa_read_model = self._qa_read_model(render_qa, timeline=timeline)
        render_job_state = VideoWorkbenchRenderJobState(
            program_id=program_id,
            timeline_program_id=timeline.timeline_program_id,
            render_job_id=job.render_job_id,
            job_type=job.job_type.value,
            job_status=job.status.value,
            worker_id=worker.worker_id,
            lease_id=lease.render_job_lease_id,
            result_id=worker_result.render_job_result_id,
            output_uri=output_uri,
            output_sha256=output_sha256,
            dry_run=True,
            fake_result=worker_result.fake_result,
            external_runtime_calls_executed=False,
            provider_calls_executed=False,
            created_at=job.created_at,
            completed_at=worker_result.completed_at,
            lifecycle_events=["created", "queued", "leased", "heartbeat", "completed"],
        )
        self._render_states_by_job_id[render_job_state.render_job_id] = render_job_state
        self._update_read_model_after_proxy_render(
            program_id=program_id,
            output_uri=output_uri,
            output_sha256=output_sha256,
            render_job_state=render_job_state,
            render_qa=render_qa_read_model,
        )
        return ProxyRenderResponse(
            program_id=program_id,
            timeline_program_id=timeline.timeline_program_id,
            proxy_render_receipt_id=receipt.proxy_render_receipt_id,
            proxy_render_contract_id=contract.proxy_render_contract_id,
            output_uri=output_uri,
            output_sha256=output_sha256,
            fake_render=receipt.fake_render,
            render_job_state=render_job_state,
            output_preview_url=output_uri,
            render_qa=render_qa_read_model,
            source_mode="dry_run",
        )

    def get_render_job_state(self, program_id: str, render_job_id: str) -> VideoWorkbenchRenderJobState:
        state = self._render_states_by_job_id[render_job_id]
        if state.program_id != program_id:
            raise KeyError(f"Render job {render_job_id} does not belong to program {program_id}")
        return state

    def export_otio(self, program_id: str, request: OTIOExportRequest | None = None) -> OTIOExportResponse:
        timeline = self._require_timeline(program_id)
        otio = self.renderer.compile_otio_audit_timeline(timeline)
        return OTIOExportResponse(
            program_id=program_id,
            otio_audit_timeline_id=otio.otio_audit_timeline_id,
            timeline_program_id=otio.timeline_program_id,
            tracks_summary=otio.tracks_summary,
            external_media_refs=otio.external_media_refs,
            otio_manifest_ref=f"otio://audit/{otio.otio_audit_timeline_id}",
        )

    def _require_timeline(self, program_id: str) -> VideoTimelineProgram:
        if program_id not in self._timelines_by_program_id:
            raise KeyError(f"Unknown video timeline program: {program_id}")
        return self._timelines_by_program_id[program_id]

    def _compile_dry_run_remotion_job(self, *, timeline: VideoTimelineProgram, props_ref: str) -> RemotionRenderJob:
        return RemotionRenderJob(
            timeline_program_id=timeline.timeline_program_id,
            composition_id=f"{self._format_slot_for_timeline(timeline)}ProxyComposition",
            entry_point="remotion/index.ts",
            output_path=f"client_workspaces/{timeline.brand_id}/runs/{timeline.timeline_program_id}/renders/proxy.mp4",
            input_props_ref=props_ref,
            complete_editing_session_state=CompleteEditingSessionRenderStateWrapper(
                complete_editing_session_ref=f"ces_{timeline.project_id}",
                brand_context_version_id=timeline.brand_context_version_id,
                research_snapshot_refs=[f"research_snapshot_{timeline.source_asset_set_id}"],
                asset_manifest_refs=[timeline.source_asset_set_id],
                scene_spec_refs=[boundary.scene_id for boundary in timeline.scene_timing_plan.scene_boundaries],
                composition_job_refs=[
                    ref.composition_scene_id for ref in timeline.composition_scene_refs
                ] or [f"composition_job_{timeline.timeline_program_id}"],
                provider_job_receipt_refs=[],
                evaluation_receipt_refs=[f"video_eval_{timeline.timeline_program_id}"],
            ),
            seven_layer_payload=SevenLayerCompositionPayload(
                layer_refs={
                    RenderLayerName.BACKGROUND: [f"background_{timeline.timeline_program_id}"],
                    RenderLayerName.PROOF_OBJECT: [f"proof_{timeline.timeline_program_id}"],
                    RenderLayerName.REAL_LIFE_CUTOUT: [f"cutout_{timeline.timeline_program_id}"],
                    RenderLayerName.AVATAR: [f"avatar_{timeline.timeline_program_id}"],
                    RenderLayerName.TEXT: [f"text_{timeline.timeline_program_id}"],
                    RenderLayerName.ANNOTATION: [f"annotation_{timeline.timeline_program_id}"],
                    RenderLayerName.FOREGROUND_FX: [f"foreground_fx_{timeline.timeline_program_id}"],
                }
            ),
            motion_vocabulary_receipt=MotionVocabularyPolicyReceipt(
                requested_motion_cues=[MotionCueName.PAPER_SLIDE_IN, MotionCueName.TEXT_REVEAL]
            ),
            memetic_sound_receipt=MemeticSoundCueModerationReceipt(
                format_id=self._render_adapter_format_id(timeline),
                cue_times_ms=self._synthetic_memetic_cues(timeline),
            ),
            duration_in_frames=self._ms_to_frames(timeline.duration_ms, timeline.fps),
        )

    def _compile_synthetic_render_qa(self, *, timeline: VideoTimelineProgram, file_ref: str):
        ffprobe = self.ffprobe.validate_from_metadata(
            file_ref=file_ref,
            metadata={
                "duration_ms": timeline.duration_ms,
                "width": 1080,
                "height": 1920,
                "fps": timeline.fps,
                "video_codec": "h264",
                "audio_codec": "aac",
            },
        )
        frame_count = max(1, len(timeline.scene_timing_plan.scene_boundaries))
        frames = self.frame_sampling.compile_receipt(
            file_ref=file_ref,
            sampled_frame_count=frame_count,
            expected_scene_count=frame_count,
        )
        audio = self.audio_levels.compile_receipt(
            file_ref=file_ref,
            integrated_lufs=-14,
            true_peak_db=-1.5,
        )
        duration = self.duration_tolerance.compile_receipt(
            expected_duration_ms=timeline.duration_ms,
            actual_duration_ms=timeline.duration_ms,
        )
        return self.render_qa.compile_report(
            file_ref=file_ref,
            ffprobe_validation=ffprobe,
            frame_sampling=frames,
            audio_level_analysis=audio,
            duration_tolerance=duration,
        )

    def _qa_read_model(self, report, *, timeline: VideoTimelineProgram) -> VideoWorkbenchRenderQAReadModel:
        return VideoWorkbenchRenderQAReadModel(
            render_qa_report_id=report.render_qa_report_id,
            pass_status=report.pass_status.value,
            blockers=report.blockers,
            ffprobe_status=report.ffprobe_validation.pass_status.value,
            frame_sampling_status=report.frame_sampling.pass_status.value,
            audio_level_status=report.audio_level_analysis.pass_status.value,
            duration_tolerance_status=report.duration_tolerance.pass_status.value,
            duration_ms=timeline.duration_ms,
            width=1080,
            height=1920,
            fps=timeline.fps,
        )

    def _update_read_model_after_proxy_render(
        self,
        *,
        program_id: str,
        output_uri: str,
        output_sha256: str,
        render_job_state: VideoWorkbenchRenderJobState,
        render_qa: VideoWorkbenchRenderQAReadModel,
    ) -> None:
        read_model = self._read_models_by_program_id.get(program_id)
        if not read_model:
            return
        read_model.playback_proxy_status = render_job_state.job_status
        read_model.proxy_render_ref = output_uri
        read_model.output_preview_url = output_uri
        read_model.last_render_job_state = render_job_state
        read_model.last_render_qa = render_qa
        read_model.render_summaries = [
            summary for summary in read_model.render_summaries if summary.render_type != "proxy"
        ]
        read_model.render_summaries.insert(
            0,
            VideoTimelineWorkbenchRenderSummary(
                render_type="proxy",
                status=render_job_state.job_status,
                output_uri=output_uri,
                output_sha256=output_sha256,
                fake_render=True,
            ),
        )

    def _render_adapter_format_id(self, timeline: VideoTimelineProgram) -> RenderAdapterVideoFormatId:
        format_id = timeline.format_program_refs[0].format_id if timeline.format_program_refs else VideoFormatId.FORMAT_02
        return {
            VideoFormatId.FORMAT_01: RenderAdapterVideoFormatId.FORMAT_01,
            VideoFormatId.FORMAT_02: RenderAdapterVideoFormatId.FORMAT_02,
            VideoFormatId.FORMAT_03: RenderAdapterVideoFormatId.FORMAT_03,
            VideoFormatId.FORMAT_04: RenderAdapterVideoFormatId.FORMAT_04,
        }[format_id]

    def _synthetic_memetic_cues(self, timeline: VideoTimelineProgram) -> list[int]:
        format_id = self._render_adapter_format_id(timeline)
        if format_id == RenderAdapterVideoFormatId.FORMAT_04:
            return [0, min(timeline.duration_ms, 10000)]
        return [0, min(timeline.duration_ms, 30000)] if timeline.duration_ms >= 30000 else [0]

    def _demo_tracks(
        self,
        format_slot: str,
        frame_profile: VideoFrameProfile,
        boundaries: list[VideoSceneBoundary],
    ) -> list[VideoTrackProgram]:
        def layers(role: VideoLayerRole, asset_prefix: str, *, z_index: int, source: bool = False) -> list[VideoLayerProgram]:
            return [
                self.video.timeline.make_layer(
                    layer_role=role,
                    start_ms=boundary.start_ms,
                    end_ms=boundary.end_ms,
                    frame_profile=frame_profile,
                    source_ref=f"source://health_myth/{boundary.scene_id}" if source else None,
                    asset_ref=None if source else f"{asset_prefix}_{boundary.scene_id}",
                    z_index=z_index,
                    composition_scene_ref=f"composition_{boundary.scene_id}",
                )
                for boundary in boundaries
            ]

        if format_slot == "SV-EDU":
            return [
                self.video.timeline.make_track(VideoTrackType.AVATAR, layers(VideoLayerRole.AVATAR_PERFORMANCE, "avatar", z_index=3)),
                self.video.timeline.make_track(VideoTrackType.AUDIENCE_PROXY, layers(VideoLayerRole.AUDIENCE_PROXY_PERFORMANCE, "proxy", z_index=4)),
                self.video.timeline.make_track(VideoTrackType.TEXT_REVEAL, layers(VideoLayerRole.TEXT, "text_placement", z_index=5)),
            ]
        if format_slot == "SV-FRB":
            return [
                self.video.timeline.make_track(VideoTrackType.PROOF_OBJECT, layers(VideoLayerRole.PROOF_SURFACE, "proof", z_index=3)),
                self.video.timeline.make_track(VideoTrackType.REACTION_UI, layers(VideoLayerRole.REACTION_SURFACE, "reaction_ui", z_index=4)),
                self.video.timeline.make_track(VideoTrackType.CAPTION, layers(VideoLayerRole.CAPTION, "caption", z_index=5)),
            ]
        if format_slot == "SV-CSC":
            return [
                self.video.timeline.make_track(VideoTrackType.A_ROLL, layers(VideoLayerRole.PRIMARY_SOURCE, "source", z_index=1, source=True)),
                self.video.timeline.make_track(VideoTrackType.MEMORY_OBJECT, layers(VideoLayerRole.SUPPORTING_BROLL, "memory", z_index=2)),
                self.video.timeline.make_track(VideoTrackType.CAPTION, layers(VideoLayerRole.CAPTION, "caption", z_index=3)),
            ]
        return [
            self.video.timeline.make_track(VideoTrackType.SOURCE_VIDEO, layers(VideoLayerRole.PRIMARY_SOURCE, "source", z_index=1, source=True)),
            self.video.timeline.make_track(VideoTrackType.REACTION_UI, layers(VideoLayerRole.REACTION_SURFACE, "reaction_ui", z_index=3)),
            self.video.timeline.make_track(VideoTrackType.CAPTION, layers(VideoLayerRole.CAPTION, "caption", z_index=4)),
        ]

    def _scene_segments(self, timeline: VideoTimelineProgram) -> tuple[list[TimelineClipSegment], list[VideoTimelineWorkbenchScene]]:
        segments: list[TimelineClipSegment] = []
        scenes: list[VideoTimelineWorkbenchScene] = []
        for boundary in timeline.scene_timing_plan.scene_boundaries:
            time_range = self._range(boundary.start_ms, boundary.end_ms, timeline.fps)
            segments.append(TimelineClipSegment(
                segment_id=f"seg_{boundary.scene_id}",
                lane_id="scene",
                segment_type="scene",
                label=boundary.scene_role.replace("_", " ").title(),
                time_range=time_range,
                source_refs=self._source_span_refs(timeline),
                primitive_refs=["prim.source_truth.specificity", "prim.delivery_shape.sequence", "prim.format_material_expression.timeline"],
                locked=True,
            ))
            scenes.append(VideoTimelineWorkbenchScene(
                scene_id=boundary.scene_id,
                scene_role=boundary.scene_role,
                time_range=time_range,
                source_refs=self._source_span_refs(timeline),
            ))
        return segments, scenes

    def _lane_from_track(self, track: VideoTrackProgram, timeline: VideoTimelineProgram) -> TimelineTrackLane:
        lane_id = track.track_type.value
        return TimelineTrackLane(
            lane_id=lane_id,
            display_name=self._display_name(lane_id),
            lane_kind=self._lane_kind(track.track_type),
            editable=track.track_type not in {VideoTrackType.SOURCE_VIDEO, VideoTrackType.SOURCE_AUDIO, VideoTrackType.A_ROLL},
            segments=[self._segment_from_layer(layer, lane_id, timeline) for layer in track.layers],
        )

    def _segment_from_layer(self, layer: VideoLayerProgram, lane_id: str, timeline: VideoTimelineProgram) -> TimelineClipSegment:
        label = self._display_name(layer.asset_ref or layer.source_ref or layer.layer_role.value)
        return TimelineClipSegment(
            segment_id=layer.layer_id,
            lane_id=lane_id,
            segment_type=self._segment_type(layer.layer_role, lane_id),
            label=label,
            time_range=self._range(layer.start_ms, layer.end_ms, timeline.fps),
            source_refs=[ref for ref in [layer.source_ref, layer.asset_ref, layer.composition_scene_ref] if ref],
            primitive_refs=self._primitive_refs(layer.layer_role),
            receipt_refs=[ref for ref in [layer.composition_scene_ref] if ref],
            locked=lane_id in {"source_video", "source_audio", "a_roll"},
        )

    def _track_summary(self, track: VideoTrackProgram, timeline: VideoTimelineProgram) -> VideoTimelineWorkbenchTrack:
        return VideoTimelineWorkbenchTrack(
            track_id=track.track_id,
            track_type=track.track_type.value,
            layers=[
                VideoTimelineWorkbenchLayer(
                    layer_id=layer.layer_id,
                    layer_role=layer.layer_role.value,
                    time_range=self._range(layer.start_ms, layer.end_ms, timeline.fps),
                    source_ref=layer.source_ref,
                    asset_ref=layer.asset_ref,
                    composition_scene_ref=layer.composition_scene_ref,
                )
                for layer in track.layers
            ],
        )

    def _eval_lane(self, timeline: VideoTimelineProgram, evaluation) -> TimelineTrackLane:
        severity = "hard_blocker" if evaluation.blockers else "info"
        label = "Eval blockers present" if evaluation.blockers else "Video eval pass"
        return TimelineTrackLane(
            lane_id="eval",
            display_name="Eval and blocker markers",
            lane_kind="eval",
            editable=False,
            segments=[
                TimelineClipSegment(
                    segment_id=f"seg_eval_{timeline.timeline_program_id}",
                    lane_id="eval",
                    segment_type="eval_marker",
                    label=label,
                    time_range=self._range(0, max(1000, min(timeline.duration_ms, 6000)), timeline.fps),
                    primitive_refs=["prim.receipt_chain.coverage", "prim.operator_review.trace", "prim.timeline_integrity.pass"],
                    receipt_refs=[evaluation.video_evaluation_receipt_id],
                    blocker_codes=evaluation.blockers if severity == "hard_blocker" else [],
                    locked=True,
                )
            ],
        )

    def _approval_lane(self, timeline: VideoTimelineProgram, otio) -> TimelineTrackLane:
        return TimelineTrackLane(
            lane_id="approval",
            display_name="Approval and OTIO markers",
            lane_kind="approval",
            editable=False,
            segments=[
                TimelineClipSegment(
                    segment_id=f"seg_otio_{otio.otio_audit_timeline_id}",
                    lane_id="approval",
                    segment_type="approval_marker",
                    label="OTIO audit coverage",
                    time_range=self._range(0, timeline.duration_ms, timeline.fps),
                    primitive_refs=["prim.verifiable_artifact.otio", "prim.receipt_chain.coverage", "prim.operator_approval.trace"],
                    receipt_refs=[otio.otio_audit_timeline_id],
                    locked=True,
                )
            ],
        )

    def _markers(self, timeline: VideoTimelineProgram, evaluation) -> list[TimelineMarker]:
        marker_range = self._range(0, max(1000, min(timeline.duration_ms, 6000)), timeline.fps)
        if evaluation.blockers:
            return [
                TimelineMarker(
                    marker_id=f"marker_{blocker}",
                    marker_type="eval_blocker",
                    lane_id="eval",
                    time_range=marker_range,
                    severity="hard_blocker",
                    label=blocker,
                    primitive_refs=["prim.timeline_integrity.pass"],
                    receipt_refs=[evaluation.video_evaluation_receipt_id],
                    repair_command_type="request_repair",
                )
                for blocker in evaluation.blockers
            ]
        return [
            TimelineMarker(
                marker_id=f"marker_eval_pass_{timeline.timeline_program_id}",
                marker_type="primitive_pass",
                lane_id="eval",
                time_range=marker_range,
                severity="info",
                label="Video timeline integrity pass",
                primitive_refs=["prim.timeline_integrity.pass", "prim.mobile_readability.pass"],
                receipt_refs=[evaluation.video_evaluation_receipt_id],
            )
        ]

    def _range(self, start_ms: int, end_ms: int, fps: int) -> TimelineTimeRange:
        return TimelineTimeRange(
            start_frame=self._ms_to_frames(start_ms, fps),
            end_frame=self._ms_to_frames(end_ms, fps),
            start_ms=start_ms,
            end_ms=end_ms,
        )

    def _ms_to_frames(self, value_ms: int, fps: int) -> int:
        return int(round((value_ms / 1000) * fps))

    def _source_span_refs(self, timeline: VideoTimelineProgram) -> list[str]:
        refs: list[str] = []
        for ref in timeline.format_program_refs:
            refs.extend(ref.source_span_refs)
        return list(dict.fromkeys(refs))

    def _format_slot_for_timeline(self, timeline: VideoTimelineProgram) -> str:
        format_id = timeline.format_program_refs[0].format_id if timeline.format_program_refs else VideoFormatId.FORMAT_02
        return {
            VideoFormatId.FORMAT_01: "SV-CSC",
            VideoFormatId.FORMAT_02: "SV-EDU",
            VideoFormatId.FORMAT_03: "SV-FRB",
            VideoFormatId.FORMAT_04: "SV-RRC",
        }[format_id]

    def _format_id_for_slot(self, format_slot: str) -> VideoFormatId:
        return {
            "SV-CSC": VideoFormatId.FORMAT_01,
            "SV-EDU": VideoFormatId.FORMAT_02,
            "SV-FRB": VideoFormatId.FORMAT_03,
            "SV-RRC": VideoFormatId.FORMAT_04,
        }[format_slot]

    def _frame_profile_for_slot(self, format_slot: str) -> VideoFrameProfile:
        return {
            "SV-CSC": VideoFrameProfile.NINE_SIXTEEN_FULL_VERTICAL,
            "SV-EDU": VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
            "SV-FRB": VideoFrameProfile.NINE_SIXTEEN_SPLIT_REACTION,
            "SV-RRC": VideoFrameProfile.NINE_SIXTEEN_CONSCIOUS_REACTION,
        }[format_slot]

    def _normalize_format_slot(self, format_slot: str | None) -> str:
        if format_slot in FORMAT_SLOT_META:
            return format_slot
        return "SV-RRC"

    def _lane_kind(self, track_type: VideoTrackType) -> str:
        if track_type in {VideoTrackType.SOURCE_VIDEO, VideoTrackType.A_ROLL, VideoTrackType.BROLL}:
            return "video"
        if track_type in {VideoTrackType.CAPTION, VideoTrackType.TEXT_REVEAL}:
            return "caption"
        if track_type in {VideoTrackType.SOURCE_AUDIO, VideoTrackType.SOUND_CUE, VideoTrackType.MUSIC, VideoTrackType.ROOM_TONE}:
            return "audio"
        if track_type in {VideoTrackType.AVATAR, VideoTrackType.AUDIENCE_PROXY, VideoTrackType.ROUGH_NOTATION}:
            return "animation"
        if track_type == VideoTrackType.REACTION_UI:
            return "ui"
        if track_type == VideoTrackType.REAL_LIFE_CUTOUT:
            return "subject"
        return "asset"

    def _segment_type(self, layer_role: VideoLayerRole, lane_id: str) -> str:
        if layer_role == VideoLayerRole.AVATAR_PERFORMANCE:
            return "avatar"
        if layer_role == VideoLayerRole.AUDIENCE_PROXY_PERFORMANCE:
            return "subject_cutout"
        if layer_role == VideoLayerRole.CAPTION:
            return "caption"
        if layer_role == VideoLayerRole.TEXT:
            return "caption"
        if layer_role == VideoLayerRole.REACTION_SURFACE:
            return "reaction_ui"
        if layer_role == VideoLayerRole.PROOF_SURFACE:
            return "generated_insert"
        if layer_role == VideoLayerRole.PRIMARY_SOURCE:
            return "source_clip"
        if "audio" in lane_id or "music" in lane_id:
            return "audio"
        return "generated_insert"

    def _primitive_refs(self, layer_role: VideoLayerRole) -> list[str]:
        mapping = {
            VideoLayerRole.AVATAR_PERFORMANCE: ["prim.delivery_shape.teacher_presence", "prim.character_rig.expression", "prim.source_truth.bound"],
            VideoLayerRole.AUDIENCE_PROXY_PERFORMANCE: ["prim.viewer_state.mirror", "prim.sfl.recognition", "prim.dignity.non_mocking"],
            VideoLayerRole.TEXT: ["prim.source_truth.exact_phrase", "prim.mobile_readability.text", "prim.format_material_expression.paper"],
            VideoLayerRole.CAPTION: ["prim.source_truth.exact_phrase", "prim.mobile_readability.caption", "prim.delivery_shape.clarity"],
            VideoLayerRole.REACTION_SURFACE: ["prim.commentability.choice", "prim.viewer_state.recognition", "prim.delivery_shape.participation"],
            VideoLayerRole.PROOF_SURFACE: ["prim.source_truth.evidence", "prim.frame_breaker.proof", "prim.delivery_shape.punch"],
            VideoLayerRole.PRIMARY_SOURCE: ["prim.source_truth.specificity", "prim.voice_dna.presence", "prim.human_dignity.non_extract"],
        }
        return mapping.get(layer_role, ["prim.receipt_chain.coverage", "prim.timeline.integrity", "prim.operator_review.trace"])

    def _display_name(self, value: str) -> str:
        return value.replace("://", " ").replace("_", " ").replace("-", " ").title()

    def _dump_model(self, model):
        return model.model_dump() if hasattr(model, "model_dump") else model.dict()
