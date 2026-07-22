from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    CompleteEditingSessionRef,
    VideoEditingProject,
    VideoEditingVariant,
    VideoFrameProfile,
    VideoProjectStatus,
)
from ccp_studio.repositories.video_editing_engine import InMemoryVideoEditingEngineRepository
from ccp_studio.services.video_source_asset_service import VideoSourceAssetService
from ccp_studio.services.video_media_probe_service import VideoMediaProbeService
from ccp_studio.services.video_scene_realization_service import VideoSceneRealizationService
from ccp_studio.services.video_timeline_service import VideoTimelineService
from ccp_studio.services.video_render_contract_service import VideoRenderContractService
from ccp_studio.services.video_eval_service import VideoEvalService
from ccp_studio.services.video_revision_service import VideoRevisionService
from ccp_studio.services.video_export_service import VideoExportService


class VideoEditingEngineService:
    def __init__(self, repository: InMemoryVideoEditingEngineRepository | None = None):
        self.repository = repository or InMemoryVideoEditingEngineRepository()
        self.sources = VideoSourceAssetService()
        self.probe = VideoMediaProbeService()
        self.realization = VideoSceneRealizationService()
        self.timeline = VideoTimelineService()
        self.render = VideoRenderContractService()
        self.eval = VideoEvalService()
        self.revision = VideoRevisionService()
        self.export = VideoExportService()

    def create_project(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        title: str,
        complete_editing_session_ref: CompleteEditingSessionRef | None = None,
    ) -> VideoEditingProject:
        project = VideoEditingProject(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            title=title,
            complete_editing_session_ref=complete_editing_session_ref,
        )
        return self.repository.upsert("projects", project.video_project_id, project)

    def create_variant(
        self,
        *,
        project_id: str,
        frame_profile: VideoFrameProfile,
        target_duration_ms: int,
    ) -> VideoEditingVariant:
        variant = VideoEditingVariant(project_id=project_id, frame_profile=frame_profile, target_duration_ms=target_duration_ms)
        return self.repository.upsert("variants", variant.video_variant_id, variant)

    def lock_final_timeline(self, timeline):
        timeline.final_locked = True
        timeline.status = VideoProjectStatus.FINAL_TIMELINE_LOCKED
        return self.repository.upsert("timeline_programs", timeline.timeline_program_id, timeline)
