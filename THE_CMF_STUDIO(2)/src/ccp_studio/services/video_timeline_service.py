from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    VideoFrameProfile,
    VideoLayerProgram,
    VideoLayerRole,
    VideoSceneBoundary,
    VideoSceneTimingPlan,
    VideoTimelineProgram,
    VideoTrackProgram,
    VideoTrackType,
)


class VideoTimelineService:
    def compile_scene_timing_plan(self, boundaries: list[VideoSceneBoundary]) -> VideoSceneTimingPlan:
        return VideoSceneTimingPlan(scene_boundaries=boundaries)

    def make_layer(
        self,
        *,
        layer_role: VideoLayerRole,
        start_ms: int,
        end_ms: int,
        frame_profile: VideoFrameProfile,
        source_ref: str | None = None,
        asset_ref: str | None = None,
        z_index: int = 1,
        composition_scene_ref: str | None = None,
    ) -> VideoLayerProgram:
        return VideoLayerProgram(
            layer_role=layer_role,
            source_ref=source_ref,
            asset_ref=asset_ref,
            start_ms=start_ms,
            end_ms=end_ms,
            z_index=z_index,
            frame_profile=frame_profile,
            composition_scene_ref=composition_scene_ref,
        )

    def make_track(self, track_type: VideoTrackType, layers: list[VideoLayerProgram]) -> VideoTrackProgram:
        return VideoTrackProgram(track_type=track_type, layers=layers)

    def compile_timeline_program(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        project_id: str,
        variant_id: str,
        frame_profile: VideoFrameProfile,
        duration_ms: int,
        source_asset_set_id: str,
        format_program_refs,
        composition_scene_refs,
        avatar_performance_plan_refs,
        tracks: list[VideoTrackProgram],
        scene_timing_plan: VideoSceneTimingPlan,
    ) -> VideoTimelineProgram:
        return VideoTimelineProgram(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            project_id=project_id,
            variant_id=variant_id,
            frame_profile=frame_profile,
            duration_ms=duration_ms,
            source_asset_set_id=source_asset_set_id,
            format_program_refs=format_program_refs,
            composition_scene_refs=composition_scene_refs,
            avatar_performance_plan_refs=avatar_performance_plan_refs,
            tracks=tracks,
            scene_timing_plan=scene_timing_plan,
        )
