from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    Avatar64StateActingLibrary,
    AvatarActingState,
    AvatarFormatUse,
    AvatarGestureClip,
    AvatarGestureClipLibrary,
    BodyPoseName,
    EdgeBand,
    ExpressionPlateName,
    GestureClipType,
)


class AvatarClipLibraryService:
    def create_canonical_gesture_clip_library(self, avatar_id: str) -> AvatarGestureClipLibrary:
        clip_by_pose = {
            GestureClipType.RAISE_FINGER: BodyPoseName.POINT_UP,
            GestureClipType.OPEN_PALM_REVEAL: BodyPoseName.OPEN_PALM_REVEAL,
            GestureClipType.POINT_TO_CARD: BodyPoseName.POINT_TO_CARD,
            GestureClipType.THINKING_TILT: BodyPoseName.THINKING_CHIN,
            GestureClipType.SOFT_SHRUG: BodyPoseName.SOFT_SHRUG,
            GestureClipType.HOLD_MUG: BodyPoseName.HOLD_CUP,
            GestureClipType.STAMP_TRUTH: BodyPoseName.STOP_HAND,
            GestureClipType.PRESENT_DIAGRAM: BodyPoseName.PRESENT_DIAGRAM,
        }
        clips = [
            AvatarGestureClip(
                clip_type=clip_type,
                body_pose_name=pose,
                primitive_function="clarity",
                sfl_function=self._sfl_for_clip(clip_type),
            )
            for clip_type, pose in clip_by_pose.items()
        ]
        return AvatarGestureClipLibrary(avatar_id=avatar_id, clips=clips)

    def create_64_state_acting_library(self, avatar_id: str) -> Avatar64StateActingLibrary:
        states = []
        for expression in ExpressionPlateName:
            for pose in BodyPoseName:
                states.append(
                    AvatarActingState(
                        expression_name=expression,
                        body_pose_name=pose,
                        primitive_function=self._primitive_for_expression(expression),
                        sfl_function=self._sfl_for_pose(pose),
                        best_formats=[AvatarFormatUse.FORMAT_02, AvatarFormatUse.CAROUSEL],
                        edge_band=EdgeBand.CLEAR_CONTRAST if expression in {ExpressionPlateName.SKEPTICAL_BROW, ExpressionPlateName.SERIOUS_TRUTH} else EdgeBand.GENTLE_RECOGNITION,
                    )
                )
        return Avatar64StateActingLibrary(avatar_id=avatar_id, states=states)

    def _sfl_for_clip(self, clip: GestureClipType) -> str:
        mapping = {
            GestureClipType.RAISE_FINGER: "perceptual_entry",
            GestureClipType.OPEN_PALM_REVEAL: "truthful_payoff",
            GestureClipType.POINT_TO_CARD: "focus_target",
            GestureClipType.THINKING_TILT: "active_prediction",
            GestureClipType.SOFT_SHRUG: "nuance_preservation",
            GestureClipType.HOLD_MUG: "closure_warmth",
            GestureClipType.STAMP_TRUTH: "truth_landing",
            GestureClipType.PRESENT_DIAGRAM: "process_confidence",
        }
        return mapping[clip]

    def _primitive_for_expression(self, expression: ExpressionPlateName) -> str:
        mapping = {
            ExpressionPlateName.NEUTRAL_WARM: "presence",
            ExpressionPlateName.GENTLE_SMILE: "warmth",
            ExpressionPlateName.SKEPTICAL_BROW: "discernment",
            ExpressionPlateName.CURIOUS_THINKING: "curiosity",
            ExpressionPlateName.SERIOUS_TRUTH: "integrity",
            ExpressionPlateName.PLAYFUL_WARNING: "edge_softening",
            ExpressionPlateName.COMPASSIONATE_CONCERN: "recognition",
            ExpressionPlateName.ENCOURAGING_CLOSE: "support",
        }
        return mapping[expression]

    def _sfl_for_pose(self, pose: BodyPoseName) -> str:
        mapping = {
            BodyPoseName.POINT_UP: "perceptual_entry",
            BodyPoseName.POINT_TO_CARD: "focus_target",
            BodyPoseName.OPEN_PALM_REVEAL: "truthful_payoff",
            BodyPoseName.THINKING_CHIN: "active_prediction",
            BodyPoseName.STOP_HAND: "myth_interruption",
            BodyPoseName.SOFT_SHRUG: "nuance_preservation",
            BodyPoseName.HOLD_CUP: "closure_warmth",
            BodyPoseName.PRESENT_DIAGRAM: "process_confidence",
        }
        return mapping[pose]
