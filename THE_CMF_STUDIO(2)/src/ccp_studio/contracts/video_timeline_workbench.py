from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

from ccp_studio.contracts.video_editing_engine import stable_hash


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str, seed: str | None = None) -> str:
    if seed:
        return f"{prefix}_{stable_hash(seed)[:12]}"
    return f"{prefix}_{stable_hash(_now_iso())[:12]}"


class TimelineTimeRange(BaseModel):
    start_frame: int = Field(ge=0)
    end_frame: int = Field(ge=0)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_frame <= self.start_frame:
            raise ValueError("TimelineTimeRange requires positive frame duration")
        if self.end_ms <= self.start_ms:
            raise ValueError("TimelineTimeRange requires positive millisecond duration")


class TimelineClipSegment(BaseModel):
    schema_version: Literal["cmf.timeline_clip_segment.v1"] = "cmf.timeline_clip_segment.v1"
    segment_id: str
    lane_id: str
    segment_type: str
    label: str
    time_range: TimelineTimeRange
    source_refs: list[str] = Field(default_factory=list)
    primitive_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    locked: bool = False
    note: str = ""


class TimelineTrackLane(BaseModel):
    schema_version: Literal["cmf.timeline_track_lane.v1"] = "cmf.timeline_track_lane.v1"
    lane_id: str
    display_name: str
    lane_kind: str
    editable: bool
    edit_policy_ref: str | None = None
    segments: list[TimelineClipSegment] = Field(default_factory=list)


class TimelineMarker(BaseModel):
    schema_version: Literal["cmf.timeline_marker.v1"] = "cmf.timeline_marker.v1"
    marker_id: str
    marker_type: str
    lane_id: str | None = None
    time_range: TimelineTimeRange
    severity: Literal["info", "warning", "hard_blocker"] = "info"
    label: str
    primitive_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    repair_command_type: str | None = None


class VideoTimelineWorkbenchProgramSummary(BaseModel):
    program_id: str
    timeline_program_id: str | None = None
    brand_id: str
    brand_context_version_id: str
    frame_profile: str
    format_program_refs: list[str] = Field(default_factory=list)
    source_span_refs: list[str] = Field(default_factory=list)


class VideoTimelineWorkbenchScene(BaseModel):
    scene_id: str
    scene_role: str
    time_range: TimelineTimeRange
    source_refs: list[str] = Field(default_factory=list)


class VideoTimelineWorkbenchLayer(BaseModel):
    layer_id: str
    layer_role: str
    time_range: TimelineTimeRange
    source_ref: str | None = None
    asset_ref: str | None = None
    composition_scene_ref: str | None = None


class VideoTimelineWorkbenchTrack(BaseModel):
    track_id: str
    track_type: str
    layers: list[VideoTimelineWorkbenchLayer] = Field(default_factory=list)


class VideoTimelineWorkbenchCaptionCue(BaseModel):
    caption_id: str
    text: str
    time_range: TimelineTimeRange
    source_refs: list[str] = Field(default_factory=list)


class VideoTimelineWorkbenchSoundCue(BaseModel):
    sound_cue_id: str
    cue_type: str
    time_range: TimelineTimeRange
    target_ref: str | None = None


class VideoTimelineWorkbenchRenderSummary(BaseModel):
    render_summary_id: str = Field(default_factory=lambda: _new_id("render_summary"))
    render_type: Literal["proxy", "final", "otio"]
    status: str
    output_uri: str | None = None
    output_sha256: str | None = None
    fake_render: bool = True
    provider_calls_executed: bool = False
    remotion_called: bool = False
    ffmpeg_called: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed:
            raise ValueError("Workbench render summaries cannot record provider execution in V1")
        if self.remotion_called or self.ffmpeg_called:
            raise ValueError("Workbench render summaries cannot record real Remotion or FFmpeg calls in V1")


class VideoTimelineWorkbenchEvalSummary(BaseModel):
    eval_summary_id: str = Field(default_factory=lambda: _new_id("eval_summary"))
    evaluation_receipt_id: str | None = None
    pass_status: str
    blockers: list[str] = Field(default_factory=list)


def _validate_preview_uri(value: str | None) -> str | None:
    if value is None:
        return value
    if "\n" in value or "\r" in value or "\x00" in value:
        raise ValueError("output preview URL contains unsafe characters")
    allowed_prefixes = ("fake://", "dry-run://", "proxy://")
    if not value.startswith(allowed_prefixes):
        raise ValueError("output preview URL must use a safe V1 preview scheme")
    return value


class VideoWorkbenchRenderJobState(BaseModel):
    program_id: str
    timeline_program_id: str
    render_job_id: str
    job_type: str
    job_status: str
    worker_id: str | None = None
    lease_id: str | None = None
    result_id: str | None = None
    output_uri: str | None = None
    output_sha256: str | None = None
    dry_run: bool = True
    fake_result: bool = True
    external_runtime_calls_executed: bool = False
    provider_calls_executed: bool = False
    created_at: str
    completed_at: str | None = None
    lifecycle_events: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.program_id:
            raise ValueError("VideoWorkbenchRenderJobState requires program_id")
        if not self.timeline_program_id:
            raise ValueError("VideoWorkbenchRenderJobState requires timeline_program_id")
        if self.provider_calls_executed:
            raise ValueError("Proxy render job state cannot record provider execution")
        if self.dry_run and self.external_runtime_calls_executed:
            raise ValueError("Dry-run proxy render job state cannot record external runtime execution")
        self.output_uri = _validate_preview_uri(self.output_uri)


class VideoWorkbenchRenderQAReadModel(BaseModel):
    render_qa_report_id: str
    pass_status: str
    blockers: list[str] = Field(default_factory=list)
    ffprobe_status: str
    frame_sampling_status: str
    audio_level_status: str
    duration_tolerance_status: str
    duration_ms: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: float = Field(gt=0)


class VideoWorkbenchProxyRenderResponse(BaseModel):
    receipt_id: str = Field(default_factory=lambda: _new_id("proxy_rerender"))
    program_id: str
    timeline_program_id: str
    runtime_mode: Literal["video-timeline-workbench"] = "video-timeline-workbench"
    status: Literal["ready", "queued", "completed"] = "completed"
    created_at: str = Field(default_factory=_now_iso)
    proxy_render_receipt_id: str
    proxy_render_contract_id: str
    output_uri: str
    output_sha256: str
    fake_render: bool = True
    provider_calls_executed: bool = False
    remotion_called: bool = False
    ffmpeg_called: bool = False
    render_job_state: VideoWorkbenchRenderJobState
    output_preview_url: str
    render_qa: VideoWorkbenchRenderQAReadModel
    source_mode: Literal["backend", "dry_run", "fake", "fixture"] = "dry_run"
    message: str = "Proxy render completed through Local Render Worker fake/dry-run path."

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed:
            raise ValueError("Proxy render response cannot record provider execution")
        if self.remotion_called or self.ffmpeg_called:
            raise ValueError("Proxy render response cannot record real Remotion or FFmpeg calls in V1")
        if self.timeline_program_id != self.render_job_state.timeline_program_id:
            raise ValueError("Proxy render response must preserve timeline_program_id")
        self.output_preview_url = _validate_preview_uri(self.output_preview_url) or self.output_preview_url


class VideoTimelineWorkbenchReadModel(BaseModel):
    schema_version: Literal["cmf.video_timeline_workbench_state.v1"] = "cmf.video_timeline_workbench_state.v1"
    workbench_id: str
    program_id: str
    timeline_program_id: str | None = None
    brand_id: str
    brand_context_version_id: str
    brand_workspace_id: str
    guest_id: str
    guest_name: str = "Backend Demo"
    asset_code: str
    format_slot: str
    format_meta: dict[str, str] = Field(default_factory=dict)
    frame_profile: str
    fps: int = Field(gt=0)
    duration_frames: int = Field(gt=0)
    duration_ms: int = Field(gt=0)
    object_version: str
    proxy_render_ref: str | None = None
    renderer_props_manifest_ref: str | None = None
    renderer_props_hash: str | None = None
    beat_map_ref: str
    otio_manifest_ref: str | None = None
    playback_proxy_status: str = "ready"
    contract_gate_status: str = "valid"
    built_at: str = Field(default_factory=_now_iso)
    source_mode: Literal["backend", "demo", "fixture"] = "backend"
    source_span_refs: list[str] = Field(default_factory=list)
    program_summary: VideoTimelineWorkbenchProgramSummary
    scenes: list[VideoTimelineWorkbenchScene] = Field(default_factory=list)
    tracks: list[VideoTimelineWorkbenchTrack] = Field(default_factory=list)
    lanes: list[TimelineTrackLane] = Field(default_factory=list)
    markers: list[TimelineMarker] = Field(default_factory=list)
    captions: list[VideoTimelineWorkbenchCaptionCue] = Field(default_factory=list)
    sound_cues: list[VideoTimelineWorkbenchSoundCue] = Field(default_factory=list)
    render_summaries: list[VideoTimelineWorkbenchRenderSummary] = Field(default_factory=list)
    eval_summaries: list[VideoTimelineWorkbenchEvalSummary] = Field(default_factory=list)
    last_render_job_state: VideoWorkbenchRenderJobState | None = None
    last_render_qa: VideoWorkbenchRenderQAReadModel | None = None
    output_preview_url: str | None = None
    selected_segment_id: str | None = None
    hard_blocker_codes: list[str] = Field(default_factory=list)
    next_valid_commands: list[str] = Field(default_factory=lambda: ["request_repair", "rerender_proxy", "export_otio"])

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.program_id:
            raise ValueError("VideoTimelineWorkbenchReadModel requires program_id")
        if self.timeline_program_id is None and self.source_mode == "backend":
            raise ValueError("Backend workbench read models require timeline_program_id")
        if not self.frame_profile:
            raise ValueError("VideoTimelineWorkbenchReadModel requires frame_profile")
        if not self.tracks:
            raise ValueError("VideoTimelineWorkbenchReadModel requires tracks")
        if not self.scenes:
            raise ValueError("VideoTimelineWorkbenchReadModel requires scenes")
        if not self.render_summaries:
            raise ValueError("VideoTimelineWorkbenchReadModel requires render summaries")
        if not self.eval_summaries:
            raise ValueError("VideoTimelineWorkbenchReadModel requires eval summaries")
        self.output_preview_url = _validate_preview_uri(self.output_preview_url)


class VideoTimelineEditProposal(BaseModel):
    schema_version: Literal["cmf.timeline_edit_draft.v1"] = "cmf.timeline_edit_draft.v1"
    draft_id: str | None = None
    program_id: str
    target_segment_id: str
    edit_type: str
    proposed_time_range: TimelineTimeRange | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    expected_object_version: str
    blocker_codes: list[str] = Field(default_factory=list)


class VideoTimelineEditProposalResult(VideoTimelineEditProposal):
    status: Literal["proposed"] = "proposed"
    proposed_at: str = Field(default_factory=_now_iso)
    typed_revision_command_id: str | None = None
    runtime_mode: Literal["video-timeline-workbench"] = "video-timeline-workbench"


class VideoTimelineEditSubmission(BaseModel):
    schema_version: Literal["cmf.timeline_edit_command.v1"] = "cmf.timeline_edit_command.v1"
    command_id: str
    draft_id: str
    program_id: str
    brand_workspace_id: str
    guest_id: str
    target_segment_id: str | None = None
    edit_type: str
    expected_object_version: str
    expected_renderer_props_hash: str | None = None
    expected_scope_ref: str
    payload: dict[str, Any] = Field(default_factory=dict)
    submitted_by_operator_id: str


class VideoTimelineEditReceipt(BaseModel):
    schema_version: Literal["cmf.video_timeline_workbench_receipt.v1"] = "cmf.video_timeline_workbench_receipt.v1"
    receipt_id: str = Field(default_factory=lambda: _new_id("timeline_receipt"))
    status: Literal["receipted", "proposed"] = "receipted"
    command_id: str | None = None
    command_type: str = "submit_timeline_edit"
    runtime_mode: Literal["video-timeline-workbench"] = "video-timeline-workbench"
    object_version: str
    created_at: str = Field(default_factory=_now_iso)
    payload: dict[str, Any] = Field(default_factory=dict)
    typed_revision_command_id: str | None = None
    revision_receipt_id: str | None = None
    applied: bool = False
    target_segment_id: str | None = None
    edit_type: str | None = None


class ProxyRenderRequest(BaseModel):
    output_profile: str = "proxy_720p"
    requested_by_operator_id: str | None = None


class ProxyRenderResponse(VideoWorkbenchProxyRenderResponse):
    pass


class OTIOExportRequest(BaseModel):
    export_profile: str = "audit_manifest"
    requested_by_operator_id: str | None = None


class OTIOExportResponse(BaseModel):
    receipt_id: str = Field(default_factory=lambda: _new_id("otio_export"))
    program_id: str
    runtime_mode: Literal["video-timeline-workbench"] = "video-timeline-workbench"
    status: Literal["coverage-ready"] = "coverage-ready"
    created_at: str = Field(default_factory=_now_iso)
    otio_audit_timeline_id: str
    timeline_program_id: str
    tracks_summary: list[str]
    external_media_refs: list[str]
    otio_manifest_ref: str
    file_written: bool = False
    provider_calls_executed: bool = False
    remotion_called: bool = False
    ffmpeg_called: bool = False
