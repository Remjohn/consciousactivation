from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    FFmpegFinishPlan,
    FinalRenderContract,
    FinalRenderReceipt,
    OTIOAuditTimeline,
    ProxyRenderContract,
    ProxyRenderReceipt,
    RemotionInputProps,
    VideoTimelineProgram,
    stable_hash,
)


class VideoRenderContractService:
    def compile_otio_audit_timeline(self, timeline: VideoTimelineProgram) -> OTIOAuditTimeline:
        return OTIOAuditTimeline(
            timeline_program_id=timeline.timeline_program_id,
            tracks_summary=[track.track_type.value for track in timeline.tracks],
            external_media_refs=[layer.source_ref or layer.asset_ref or "" for track in timeline.tracks for layer in track.layers],
        )

    def compile_remotion_input_props(self, timeline: VideoTimelineProgram) -> RemotionInputProps:
        return RemotionInputProps(
            timeline_program_id=timeline.timeline_program_id,
            input_props={
                "timeline_program_id": timeline.timeline_program_id,
                "frame_profile": timeline.frame_profile.value,
                "duration_ms": timeline.duration_ms,
                "track_count": len(timeline.tracks),
            },
        )

    def compile_proxy_render_contract(self, timeline: VideoTimelineProgram, props: RemotionInputProps) -> ProxyRenderContract:
        return ProxyRenderContract(timeline_program_id=timeline.timeline_program_id, remotion_input_props_id=props.remotion_input_props_id)

    def execute_proxy_render_fake(self, contract: ProxyRenderContract) -> ProxyRenderReceipt:
        digest = stable_hash(contract.proxy_render_contract_id)
        return ProxyRenderReceipt(proxy_render_contract_id=contract.proxy_render_contract_id, output_uri=f"fake://proxy/{digest}.mp4", output_sha256=digest)

    def compile_final_render_contract(self, timeline: VideoTimelineProgram, asset_hashes: dict[str, str]) -> FinalRenderContract:
        return FinalRenderContract(timeline_program_id=timeline.timeline_program_id, timeline_locked=timeline.final_locked, asset_hashes=asset_hashes)

    def compile_ffmpeg_finish_plan(self, contract: FinalRenderContract) -> FFmpegFinishPlan:
        return FFmpegFinishPlan(final_render_contract_id=contract.final_render_contract_id)

    def execute_final_render_fake(self, contract: FinalRenderContract) -> FinalRenderReceipt:
        digest = stable_hash(contract.final_render_contract_id)
        return FinalRenderReceipt(final_render_contract_id=contract.final_render_contract_id, output_uri=f"fake://final/{digest}.mp4", output_sha256=digest)
