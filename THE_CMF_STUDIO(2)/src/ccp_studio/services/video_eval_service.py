from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    CaptionReadabilityReceipt,
    AudioQualityReceipt,
    MotionDoctrineReceipt,
    PassStatus,
    TimelineIntegrityReceipt,
    VideoEvaluationReceipt,
    VideoTimelineProgram,
)


class VideoEvalService:
    def run_eval(
        self,
        timeline: VideoTimelineProgram,
        *,
        timeline_integrity_pass: bool = True,
        caption_pass: bool = True,
        audio_pass: bool = True,
        motion_pass: bool = True,
    ) -> VideoEvaluationReceipt:
        timeline_receipt = TimelineIntegrityReceipt(
            pass_status=PassStatus.PASS if timeline_integrity_pass else PassStatus.FAIL,
            blockers=[] if timeline_integrity_pass else ["timeline_integrity_failure"],
        )
        caption = CaptionReadabilityReceipt(
            pass_status=PassStatus.PASS if caption_pass else PassStatus.FAIL,
            blockers=[] if caption_pass else ["caption_readability_failure"],
        )
        audio = AudioQualityReceipt(
            pass_status=PassStatus.PASS if audio_pass else PassStatus.FAIL,
            blockers=[] if audio_pass else ["audio_quality_failure"],
        )
        motion = MotionDoctrineReceipt(
            pass_status=PassStatus.PASS if motion_pass else PassStatus.FAIL,
            blockers=[] if motion_pass else ["motion_doctrine_failure"],
        )
        blockers = timeline_receipt.blockers + caption.blockers + audio.blockers + motion.blockers
        return VideoEvaluationReceipt(
            timeline_program_id=timeline.timeline_program_id,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            timeline_integrity=timeline_receipt,
            caption_readability=caption,
            audio_quality=audio,
            motion_doctrine=motion,
            blockers=blockers,
        )
