from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import (
    ActionClipName,
    AvatarActionClipSpec,
    AvatarActionTimeline,
)


class AvatarActionTimelineService:
    def compile_canonical_action_timeline(self, avatar_id: str) -> AvatarActionTimeline:
        clips = []
        start = 0
        for clip_name in ActionClipName:
            end = start + 900
            clips.append(
                AvatarActionClipSpec(
                    clip_name=clip_name,
                    start_ms=start,
                    end_ms=end,
                    primitive_function="clarity",
                    sfl_function=self._sfl_for_clip(clip_name),
                )
            )
            start = end
        return AvatarActionTimeline(avatar_id=avatar_id, clips=clips, total_duration_ms=start)

    def _sfl_for_clip(self, clip_name: ActionClipName) -> str:
        mapping = {
            ActionClipName.RAISE_FINGER: "perceptual_entry",
            ActionClipName.OPEN_PALM_REVEAL: "truthful_payoff",
            ActionClipName.POINT_TO_CARD: "focus_target",
            ActionClipName.THINKING_TILT: "active_prediction",
            ActionClipName.SOFT_SHRUG: "nuance_preservation",
            ActionClipName.HOLD_MUG: "closure_warmth",
            ActionClipName.STAMP_TRUTH: "truth_landing",
            ActionClipName.PRESENT_DIAGRAM: "process_confidence",
        }
        return mapping[clip_name]
