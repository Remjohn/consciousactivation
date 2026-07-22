from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    Format01SceneRealizationPlan,
    Format02SceneRealizationPlan,
    Format03SceneRealizationPlan,
    Format04SceneRealizationPlan,
    MemeticCueLedger,
    VideoAvatarPerformanceRef,
    VideoCompositionSceneRef,
    VideoFormatId,
    VideoMotionCue,
)


class VideoSceneRealizationService:
    def compile_format01(
        self,
        *,
        aroll_story_spine_ref: str,
        broll_story_functions: list[str],
        emotional_pause_refs: list[str] | None = None,
    ) -> Format01SceneRealizationPlan:
        return Format01SceneRealizationPlan(
            aroll_story_spine_ref=aroll_story_spine_ref,
            broll_story_functions=broll_story_functions,
            emotional_pause_refs=emotional_pause_refs or [],
        )

    def compile_format02(
        self,
        *,
        composition_scene_refs: list[VideoCompositionSceneRef],
        avatar_performance_refs: list[VideoAvatarPerformanceRef],
        cognitive_load_budget_preserved: bool = True,
        real_life_cutout_motion_policy: list[str] | None = None,
    ) -> Format02SceneRealizationPlan:
        return Format02SceneRealizationPlan(
            composition_scene_refs=composition_scene_refs,
            avatar_performance_refs=avatar_performance_refs,
            cognitive_load_budget_preserved=cognitive_load_budget_preserved,
            real_life_cutout_motion_policy=real_life_cutout_motion_policy or ["slide_in", "settle", "subtle_parallax"],
        )

    def compile_format03(
        self,
        *,
        proof_or_quote_surface_ref: str,
        stimulus_time_ms: int,
        reaction_start_ms: int,
        rough_notation_speech_timing_refs: list[str],
    ) -> Format03SceneRealizationPlan:
        return Format03SceneRealizationPlan(
            proof_or_quote_surface_ref=proof_or_quote_surface_ref,
            stimulus_time_ms=stimulus_time_ms,
            reaction_start_ms=reaction_start_ms,
            rough_notation_speech_timing_refs=rough_notation_speech_timing_refs,
        )

    def compile_format04(
        self,
        *,
        debate_tension_ref: str,
        reaction_ui_surface_ref: str,
        zoom_motion_cues: list[VideoMotionCue],
        cue_times_ms: list[int],
    ) -> Format04SceneRealizationPlan:
        return Format04SceneRealizationPlan(
            debate_tension_ref=debate_tension_ref,
            reaction_ui_surface_ref=reaction_ui_surface_ref,
            zoom_motion_cues=zoom_motion_cues,
            memetic_cue_ledger=MemeticCueLedger(format_id=VideoFormatId.FORMAT_04, cue_times_ms=cue_times_ms),
        )
