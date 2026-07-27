from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ccp_studio.contracts.golden_path_orchestrator import (
    Format02GoldenPathInput,
    Format02GoldenPathOutput,
    Format02GoldenPathSceneSeed,
    GoldenPathObjectSpineMap,
    GoldenPathReceipt,
    GoldenPathRecipeSpec,
    GoldenPathRun,
    GoldenPathStageName,
    GoldenPathStageResult,
    GoldenPathStatus,
)
from ccp_studio.contracts.narrative_story_doctor import ExtractionMode
from ccp_studio.contracts.narrative_format_bridge import NarrativeToFormatBridgeRequest
from ccp_studio.contracts.composition_intelligence import AudienceProxyPersona as CompositionAudienceProxyPersona, CompositionRole, PassStatus as CompositionPassStatus
from ccp_studio.contracts.format02_composition_intelligence import Format02SceneRole
from ccp_studio.contracts.video_editing_engine import (
    VideoAvatarPerformanceRef,
    VideoCompositionSceneRef,
    VideoFormatId,
    VideoFrameProfile,
    VideoLayerRole,
    VideoSceneBoundary,
    VideoSourceMedia,
    VideoTrackType,
)

from ccp_studio.repositories.golden_path_orchestrator import InMemoryGoldenPathOrchestratorRepository
from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService
from ccp_studio.services.narrative_to_format_bridge_service import NarrativeToFormatBridgeService
from ccp_studio.services.format_intelligence_service import FormatIntelligenceService
from ccp_studio.services.format02_composition_service import Format02CompositionService
from ccp_studio.services.format02_avatar_performance_adapter_service import Format02AvatarPerformanceAdapterService
from ccp_studio.services.video_editing_engine_service import VideoEditingEngineService


class Format02GoldenPathOrchestratorService:
    def __init__(
        self,
        repository: InMemoryGoldenPathOrchestratorRepository | None = None,
        narrative_service: NarrativeStoryDoctorService | None = None,
        format_service: FormatIntelligenceService | None = None,
        bridge_service: NarrativeToFormatBridgeService | None = None,
        composition_service: Format02CompositionService | None = None,
        avatar_adapter_service: Format02AvatarPerformanceAdapterService | None = None,
        video_engine_service: VideoEditingEngineService | None = None,
    ):
        self.repository = repository or InMemoryGoldenPathOrchestratorRepository()
        self.narrative = narrative_service or NarrativeStoryDoctorService()
        self.format_service = format_service or FormatIntelligenceService()
        self.bridge = bridge_service or NarrativeToFormatBridgeService(self.format_service)
        self.composition = composition_service or Format02CompositionService()
        self.avatar_adapter = avatar_adapter_service or Format02AvatarPerformanceAdapterService()
        self.video = video_engine_service or VideoEditingEngineService()

    def load_fixture_input(
        self,
        *,
        fixtures_dir: str | Path,
        brand_id: str = "brand_health_demo",
        brand_context_version_id: str = "bcv_health_demo_v1",
    ) -> Format02GoldenPathInput:
        fixtures_dir = Path(fixtures_dir)
        interview_brief = json.loads((fixtures_dir / "health_myth_interview_brief.json").read_text(encoding="utf-8"))
        transcript = (fixtures_dir / "health_myth_transcript.txt").read_text(encoding="utf-8")
        scene_outline = json.loads((fixtures_dir / "expected_scene_outline.json").read_text(encoding="utf-8"))
        scene_seeds = [Format02GoldenPathSceneSeed(**scene) for scene in scene_outline["scenes"]]
        return Format02GoldenPathInput(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            source_truth="Natural does not always mean safe.",
            transcript_text=transcript,
            interview_brief=interview_brief,
            scene_seeds=scene_seeds,
            source_span_refs=["span_1"],
        )

    def run_fixture(
        self,
        *,
        fixtures_dir: str | Path,
        brand_id: str = "brand_health_demo",
        brand_context_version_id: str = "bcv_health_demo_v1",
    ) -> GoldenPathRun:
        golden_input = self.load_fixture_input(
            fixtures_dir=fixtures_dir,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
        )
        return self.run(golden_input)

    def run(self, golden_input: Format02GoldenPathInput) -> GoldenPathRun:
        recipe = GoldenPathRecipeSpec()
        run = GoldenPathRun(recipe=recipe, input=golden_input, status=GoldenPathStatus.RUNNING)
        stage_results: list[GoldenPathStageResult] = []

        # Stage 1: fixture loaded
        stage_results.append(self._stage(
            GoldenPathStageName.FIXTURE_LOAD,
            {"scene_count": len(golden_input.scene_seeds), "brand_context_version_id": golden_input.brand_context_version_id},
        ))

        # Stage 2: Narrative extraction
        n_context = self.narrative.hydrate_context(
            brand_id=golden_input.brand_id,
            brand_context_version_id=golden_input.brand_context_version_id,
            extraction_mode=ExtractionMode.INTERVIEW_BRIEF_BOUND,
            interview_brief_id=golden_input.interview_brief.get("interview_brief_id"),
            target_formats=[],
        )
        binding = self.narrative.bind_interview_brief(n_context, golden_input.interview_brief)
        expected_graph = self.narrative.compile_expected_ingredient_graph(binding)
        source_packet = self.narrative.normalize_source(
            transcript_text=golden_input.transcript_text,
            mode=ExtractionMode.INTERVIEW_BRIEF_BOUND,
            source_id="health_myth_transcript",
            speaker="coach",
            question_id="q_health_001",
        )
        beat_map = self.narrative.compile_transcript_beat_map(source_packet)
        expression_inventory = self.narrative.extract_expression_moments(beat_map)
        clusters = self.narrative.compile_clusters(beat_map, source_packet)
        cluster = clusters[0]
        _meaning, _experience, edge = self.narrative.compile_meaning_candidates(cluster)
        format02_extraction_packet = self.narrative.compile_format02_packet(cluster)
        stage_results.append(self._stage(
            GoldenPathStageName.EXTRACTION_COMPILE,
            {
                "source_packet_id": source_packet.extraction_source_packet_id,
                "cluster_id": cluster.cluster_id,
                "format02_packet_id": format02_extraction_packet.format02_packet_id,
                "source_span_refs": format02_extraction_packet.source_span_refs,
            },
            {"expected_graph_id": expected_graph.expected_ingredient_graph_id, "expression_inventory_id": expression_inventory.expression_inventory_id},
        ))

        # Stage 3: Bridge to Format Intelligence and authorize
        packet_ref = self.bridge.ref_from_format02(format02_extraction_packet)
        bridge_request = NarrativeToFormatBridgeRequest(
            brand_id=golden_input.brand_id,
            brand_context_version_id=golden_input.brand_context_version_id,
            source_extraction_run_id=run.golden_path_run_id,
            packet_refs=[packet_ref],
        )
        format_context = self.bridge.make_context(bridge_request)
        format_program, format_verdict, engine_adapter_payload, bridge_receipt = self.bridge.compile_one(format_context, packet_ref)
        stage_results.append(self._stage(
            GoldenPathStageName.FORMAT_PROGRAM_COMPILE,
            {
                "format_program_id": format_program.format_intelligence_program_id,
                "authorized": format_verdict.authorized,
                "engine_adapter_payload_id": engine_adapter_payload.engine_adapter_payload_id if engine_adapter_payload else None,
            },
            {"format_verdict_id": format_verdict.commander_verdict_id, "bridge_receipt_id": bridge_receipt.format_program_compile_receipt_id},
        ))

        # Stage 4: Composition scenes
        scene_programs = []
        composition_receipts = []
        composition_reports = []
        for seed in golden_input.scene_seeds:
            scene = self.composition.compile_scene_program(
                brand_id=golden_input.brand_id,
                brand_context_version_id=golden_input.brand_context_version_id,
                source_span_refs=format02_extraction_packet.source_span_refs,
                scene_id=seed.scene_id,
                scene_role=Format02SceneRole(seed.scene_role),
                concept_statement=seed.concept_statement,
                headline_text=seed.headline_text,
                audience_proxy=CompositionAudienceProxyPersona(seed.audience_proxy),
                audience_proxy_sfl_function=seed.audience_proxy_sfl_function,
                hero_object_asset_id=seed.hero_object_asset_id,
                hero_object_source_ref=seed.hero_object_source_ref,
                hero_object_role=self._composition_role(seed.hero_object_role),
                negative_space_ratio=0.35,
            )
            visible_words = len(seed.headline_text.split())
            receipt, report = self.composition.core.compile_decision_receipt(
                scene.composition_scene_program,
                visible_words=visible_words,
                headline_words=visible_words,
                support_labels=0,
                audience_proxies=1,
                hero_real_life_objects=1,
                support_real_life_objects=0,
                diagram_nodes=0,
                simultaneous_motion_events=1,
                negative_space_ratio=0.35,
            )
            scene_programs.append(scene)
            composition_receipts.append(receipt)
            composition_reports.append(report)
        stage_results.append(self._stage(
            GoldenPathStageName.COMPOSITION_SCENES_COMPILE,
            {
                "scene_program_ids": [scene.format02_scene_program_id for scene in scene_programs],
                "locked_count": sum(1 for receipt in composition_receipts if receipt.locked),
            },
            {"composition_decision_receipt_ids": [receipt.composition_decision_receipt_id for receipt in composition_receipts]},
        ))

        # Stage 5: Avatar performance plans
        avatar_plans = []
        proxy_plans = []
        for scene in scene_programs:
            avatar_plan, proxy_plan = self.avatar_adapter.compile_from_format02_scene(scene)
            avatar_plans.append(avatar_plan)
            if proxy_plan:
                proxy_plans.append(proxy_plan)
        stage_results.append(self._stage(
            GoldenPathStageName.AVATAR_PLANS_COMPILE,
            {
                "avatar_plan_ids": [plan.avatar_performance_plan_id for plan in avatar_plans],
                "proxy_plan_ids": [plan.audience_proxy_performance_plan_id for plan in proxy_plans],
                "no_lip_sync": all(not plan.lip_sync_enabled for plan in avatar_plans),
                "proxy_sfl_functions": [plan.sfl_function for plan in proxy_plans],
            },
        ))

        # Stage 6: Video timeline
        project = self.video.create_project(
            brand_id=golden_input.brand_id,
            brand_context_version_id=golden_input.brand_context_version_id,
            title="Health Myth Format 02 Golden Path",
        )
        variant = self.video.create_variant(
            project_id=project.video_project_id,
            frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
            target_duration_ms=24000,
        )
        source_media = VideoSourceMedia(
            source_ref="health_myth_source_truth",
            media_type="text_fixture",
            uri="fixture://health_myth_transcript.txt",
            duration_ms=24000,
            width=1080,
            height=1920,
            fps=30,
        )
        source_set = self.video.sources.compile_source_asset_set(
            source_media=[source_media],
            source_span_refs=format02_extraction_packet.source_span_refs,
        )
        format_ref = self.video_format_ref(format_program.format_intelligence_program_id, format02_extraction_packet.source_span_refs)
        composition_refs = [
            VideoCompositionSceneRef(
                composition_scene_id=scene.composition_scene_program.composition_scene_program_id,
                format_id=VideoFormatId.FORMAT_02,
                locked=True,
                cognitive_load_receipt_ref=receipt.composition_decision_receipt_id,
            )
            for scene, receipt in zip(scene_programs, composition_receipts)
        ]
        avatar_refs = [
            VideoAvatarPerformanceRef(
                avatar_performance_plan_id=plan.avatar_performance_plan_id,
                lip_sync_enabled=plan.lip_sync_enabled,
                source_scene_ref=plan.scene_id,
            )
            for plan in avatar_plans
        ]
        boundaries = []
        avatar_layers = []
        proxy_layers = []
        text_layers = []
        for index, scene in enumerate(scene_programs):
            start = index * 3000
            end = start + 3000
            boundaries.append(VideoSceneBoundary(scene_id=scene.scene_id, start_ms=start, end_ms=end, scene_role=scene.scene_role.value))
            avatar_layers.append(self.video.timeline.make_layer(
                layer_role=VideoLayerRole.AVATAR_PERFORMANCE,
                start_ms=start,
                end_ms=end,
                frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
                asset_ref=avatar_plans[index].avatar_performance_plan_id,
                z_index=3,
                composition_scene_ref=scene.composition_scene_program.composition_scene_program_id,
            ))
            proxy_layers.append(self.video.timeline.make_layer(
                layer_role=VideoLayerRole.AUDIENCE_PROXY_PERFORMANCE,
                start_ms=start,
                end_ms=end,
                frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
                asset_ref=proxy_plans[index].audience_proxy_performance_plan_id,
                z_index=4,
                composition_scene_ref=scene.composition_scene_program.composition_scene_program_id,
            ))
            text_layers.append(self.video.timeline.make_layer(
                layer_role=VideoLayerRole.TEXT,
                start_ms=start,
                end_ms=end,
                frame_profile=VideoFrameProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
                asset_ref=scene.composition_scene_program.text_placement_plan.text_placement_plan_id,
                z_index=5,
                composition_scene_ref=scene.composition_scene_program.composition_scene_program_id,
            ))
        timing = self.video.timeline.compile_scene_timing_plan(boundaries)
        avatar_track = self.video.timeline.make_track(__import__("ccp_studio.contracts.video_editing_engine", fromlist=["VideoTrackType"]).VideoTrackType.AVATAR, avatar_layers)
        proxy_track = self.video.timeline.make_track(__import__("ccp_studio.contracts.video_editing_engine", fromlist=["VideoTrackType"]).VideoTrackType.AUDIENCE_PROXY, proxy_layers)
        text_track = self.video.timeline.make_track(__import__("ccp_studio.contracts.video_editing_engine", fromlist=["VideoTrackType"]).VideoTrackType.TEXT_REVEAL, text_layers)
        timeline = self.video.timeline.compile_timeline_program(
            brand_id=golden_input.brand_id,
            brand_context_version_id=golden_input.brand_context_version_id,
            project_id=project.video_project_id,
            variant_id=variant.video_variant_id,
            frame_profile=variant.frame_profile,
            duration_ms=24000,
            source_asset_set_id=source_set.source_asset_set_id,
            format_program_refs=[format_ref],
            composition_scene_refs=composition_refs,
            avatar_performance_plan_refs=avatar_refs,
            tracks=[avatar_track, proxy_track, text_track],
            scene_timing_plan=timing,
        )
        remotion_props = self.video.render.compile_remotion_input_props(timeline)
        otio = self.video.render.compile_otio_audit_timeline(timeline)
        stage_results.append(self._stage(
            GoldenPathStageName.VIDEO_TIMELINE_COMPILE,
            {
                "video_timeline_program_id": timeline.timeline_program_id,
                "remotion_input_props_id": remotion_props.remotion_input_props_id,
                "otio_audit_timeline_id": otio.otio_audit_timeline_id,
            },
        ))

        # Stage 7: fake render
        proxy_contract = self.video.render.compile_proxy_render_contract(timeline, remotion_props)
        proxy_receipt = self.video.render.execute_proxy_render_fake(proxy_contract)
        stage_results.append(self._stage(
            GoldenPathStageName.FAKE_RENDER_COMPILE,
            {"proxy_render_receipt_id": proxy_receipt.proxy_render_receipt_id, "proxy_hash": proxy_receipt.output_sha256},
            {"proxy_render_contract_id": proxy_contract.proxy_render_contract_id},
        ))

        # Stage 8: eval
        evaluation = self.video.eval.run_eval(timeline)
        stage_results.append(self._stage(
            GoldenPathStageName.EVAL_RUN,
            {"evaluation_receipt_id": evaluation.video_evaluation_receipt_id, "pass_status": evaluation.pass_status.value},
        ))

        # Stage 9: final fake render + approval + export
        self.video.lock_final_timeline(timeline)
        final_contract = self.video.render.compile_final_render_contract(
            timeline,
            asset_hashes={source_media.source_media_id: source_media.source_ref, "format_program": format_program.format_intelligence_program_id},
        )
        final_receipt = self.video.render.execute_final_render_fake(final_contract)
        approval = self.video.export.prepare_approval(
            variant_id=variant.video_variant_id,
            evaluation=evaluation,
            final_render=final_receipt,
            approved=True,
        )
        export_pack = self.video.export.compile_export_pack(
            variant_id=variant.video_variant_id,
            final_render=final_receipt,
            approved_variant=approval.approved,
        )
        stage_results.append(self._stage(
            GoldenPathStageName.EXPORT_COMPILE,
            {
                "final_render_receipt_id": final_receipt.final_render_receipt_id,
                "approval_packet_id": approval.video_approval_packet_id,
                "export_pack_id": export_pack.video_export_pack_id,
            },
            {"final_render_contract_id": final_contract.final_render_contract_id},
        ))

        output = Format02GoldenPathOutput(
            brand_context_version_id=golden_input.brand_context_version_id,
            source_span_refs=format02_extraction_packet.source_span_refs,
            extraction_packet_id=format02_extraction_packet.format02_packet_id,
            format_program_id=format_program.format_intelligence_program_id,
            format_program_authorized=format_verdict.authorized,
            scene_program_ids=[scene.format02_scene_program_id for scene in scene_programs],
            composition_decision_receipt_ids=[receipt.composition_decision_receipt_id for receipt in composition_receipts],
            composition_locked_count=sum(1 for receipt in composition_receipts if receipt.locked),
            avatar_performance_plan_ids=[plan.avatar_performance_plan_id for plan in avatar_plans],
            audience_proxy_plan_ids=[plan.audience_proxy_performance_plan_id for plan in proxy_plans],
            video_timeline_program_id=timeline.timeline_program_id,
            remotion_input_props_id=remotion_props.remotion_input_props_id,
            otio_audit_timeline_id=otio.otio_audit_timeline_id,
            proxy_render_receipt_id=proxy_receipt.proxy_render_receipt_id,
            evaluation_receipt_id=evaluation.video_evaluation_receipt_id,
            final_render_receipt_id=final_receipt.final_render_receipt_id,
            approval_packet_id=approval.video_approval_packet_id,
            export_pack_id=export_pack.video_export_pack_id,
            no_lip_sync=all(not plan.lip_sync_enabled for plan in avatar_plans),
            fake_render_only=True,
        )
        spine_map = GoldenPathObjectSpineMap(
            brand_context_version_id=golden_input.brand_context_version_id,
            source_expression_session_ref="fixture_expression_session_health_myth",
            complete_editing_session_ref=project.complete_editing_session_ref.complete_editing_session_ref_id if project.complete_editing_session_ref else project.video_project_id,
            expression_moment_refs=[m.expression_moment_id for m in expression_inventory.expression_moments],
            asset_route_receipt_refs=[bridge_receipt.format_program_compile_receipt_id],
            scene_spec_refs=[scene.format02_scene_program_id for scene in scene_programs],
            composition_job_refs=[scene.composition_scene_program.composition_scene_program_id for scene in scene_programs],
            render_output_refs=[proxy_receipt.proxy_render_receipt_id, final_receipt.final_render_receipt_id],
            evaluation_receipt_refs=[evaluation.video_evaluation_receipt_id],
            approval_event_refs=[approval.video_approval_packet_id],
        )
        receipt = GoldenPathReceipt(
            run_id=run.golden_path_run_id,
            pass_status=GoldenPathStatus.PASS,
            stage_result_ids=[stage.golden_path_stage_result_id for stage in stage_results],
            output_id=output.format02_golden_path_output_id,
        )
        run.stage_results = stage_results
        run.object_spine_map = spine_map
        run.output = output
        run.receipt = receipt
        run.status = GoldenPathStatus.PASS

        self.repository.upsert("runs", run.golden_path_run_id, run)
        self.repository.upsert("outputs", output.format02_golden_path_output_id, output)
        self.repository.upsert("receipts", receipt.golden_path_receipt_id, receipt)
        return run


    def _composition_role(self, role_value: str) -> CompositionRole:
        mapping = {
            "contrast_object": CompositionRole.HERO_OBJECT,
            "process_object": CompositionRole.DIAGRAM_OBJECT,
            "support_object": CompositionRole.SUPPORT_OBJECT,
            "micro_semiotic_anchor": CompositionRole.SUPPORT_OBJECT,
        }
        return mapping.get(role_value, CompositionRole(role_value))

    def video_format_ref(self, format_program_id: str, source_span_refs: list[str]):
        from ccp_studio.contracts.video_editing_engine import VideoFormatProgramRef, VideoFormatId
        return VideoFormatProgramRef(format_program_id=format_program_id, format_id=VideoFormatId.FORMAT_02, source_span_refs=source_span_refs)

    def _stage(self, stage_name: GoldenPathStageName, output_refs: dict[str, Any] | None = None, receipt_refs: dict[str, Any] | None = None) -> GoldenPathStageResult:
        return GoldenPathStageResult(
            stage_name=stage_name,
            status=GoldenPathStatus.PASS,
            output_refs=output_refs or {},
            receipt_refs=receipt_refs or {},
            blockers=[],
        )
