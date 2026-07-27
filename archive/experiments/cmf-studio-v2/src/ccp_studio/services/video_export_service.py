from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import VideoApprovalPacket, VideoEvaluationReceipt, FinalRenderReceipt, VideoExportPack


class VideoExportService:
    def prepare_approval(self, *, variant_id: str, evaluation: VideoEvaluationReceipt, final_render: FinalRenderReceipt, approved: bool) -> VideoApprovalPacket:
        return VideoApprovalPacket(
            variant_id=variant_id,
            evaluation_receipt_id=evaluation.video_evaluation_receipt_id,
            final_render_receipt_id=final_render.final_render_receipt_id,
            approved=approved,
        )

    def compile_export_pack(self, *, variant_id: str, final_render: FinalRenderReceipt, approved_variant: bool) -> VideoExportPack:
        return VideoExportPack(
            variant_id=variant_id,
            final_render_receipt_id=final_render.final_render_receipt_id,
            approved_variant=approved_variant,
            output_files=[final_render.output_uri],
            platform_caption_seed="source-faithful caption seed",
        )
