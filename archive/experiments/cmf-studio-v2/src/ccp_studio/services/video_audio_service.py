from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    AudioMixPlan,
    LoudnessFinishPlan,
    MemeticCueLedger,
    SoundCueEvent,
    SoundCueTimeline,
    VideoFormatId,
    VoicePresencePlan,
)


class VideoAudioService:
    def compile_voice_presence_plan(self) -> VoicePresencePlan:
        return VoicePresencePlan()

    def compile_memetic_cue_ledger(self, *, format_id: VideoFormatId, cue_times_ms: list[int]) -> MemeticCueLedger:
        return MemeticCueLedger(format_id=format_id, cue_times_ms=cue_times_ms)

    def compile_sound_cue_timeline(self, *, format_id: VideoFormatId, events: list[SoundCueEvent], cue_times_ms: list[int]) -> SoundCueTimeline:
        return SoundCueTimeline(format_id=format_id, events=events, memetic_cue_ledger=MemeticCueLedger(format_id=format_id, cue_times_ms=cue_times_ms))

    def compile_audio_mix_plan(self) -> AudioMixPlan:
        return AudioMixPlan(voice_presence_plan=self.compile_voice_presence_plan())

    def compile_loudness_finish_plan(self) -> LoudnessFinishPlan:
        return LoudnessFinishPlan()
