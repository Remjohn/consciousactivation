"""Audio, caption, timeline, and mix assembly service for TS-CMF-047."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.sonic_timeline import (
    AudioTimelineComponent,
    CaptionSegment,
    DuckingDecision,
    SonicAudioComponentRole,
    SonicAudioMixManifest,
    SonicCaptionManifest,
    SonicTimelineManifest,
    SonicTimelineReceipt,
    SonicTimelineReviewReadModel,
    SonicTimelineSegment,
    VoiceBridgePolicyValidation,
    new_sonic_timeline_receipt,
    sonic_timeline_hash,
)
from ccp_studio.contracts.voice import VoiceBoostEligibilityReport, VoiceEligibilityStatus
from ccp_studio.repositories.sonic_timeline import InMemorySonicTimelineRepository
from ccp_studio.services.command_bus import CommandBus


class SonicTimelineError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SonicTimelineService:
    repository: InMemorySonicTimelineRepository = field(default_factory=InMemorySonicTimelineRepository)

    def compile_audio_mix_manifest(
        self,
        *,
        render_output_id: UUID,
        components: list[dict[str, Any]],
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> SonicAudioMixManifest:
        parsed = [self._audio_component(item) for item in components]
        self._validate_audio_roles(parsed)
        manifest = SonicAudioMixManifest(
            schema_version="cmf.sonic_audio_mix_manifest.v1",
            audio_mix_manifest_id=uuid4(),
            render_output_id=render_output_id,
            components=parsed,
            mix_hash=sonic_timeline_hash([item.model_dump(mode="json") for item in parsed]),
            created_at=utc_now(),
        )
        return self.repository.put_audio_mix_manifest(manifest)

    def compile_caption_manifest(
        self,
        *,
        render_output_id: UUID,
        platform_variant: str,
        caption_segments: list[dict[str, Any]],
        style_constraints: dict[str, Any] | None,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> SonicCaptionManifest:
        constraints = style_constraints or {}
        parsed = [self._caption_segment(item, constraints) for item in caption_segments]
        text_source_refs = sorted({item.text_source_ref for item in parsed})
        manifest = SonicCaptionManifest(
            schema_version="cmf.sonic_caption_manifest.v1",
            caption_manifest_id=uuid4(),
            render_output_id=render_output_id,
            platform_variant=platform_variant,
            caption_segments=parsed,
            style_constraints=constraints,
            text_source_refs=text_source_refs,
            manifest_hash=sonic_timeline_hash(
                {
                    "platform_variant": platform_variant,
                    "segments": [item.model_dump(mode="json") for item in parsed],
                    "style_constraints": constraints,
                }
            ),
            created_at=utc_now(),
        )
        return self.repository.put_caption_manifest(manifest)

    def compile_timeline_manifest(
        self,
        *,
        render_output_id: UUID,
        duration_ms: int,
        segments: list[dict[str, Any]],
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> SonicTimelineManifest:
        parsed = [self._timeline_segment(item) for item in segments]
        for segment in parsed:
            if segment.end_ms > duration_ms:
                raise SonicTimelineError("TIMELINE_SEGMENT_OUT_OF_RANGE", "Timeline segment exceeds total duration.")
        manifest = SonicTimelineManifest(
            schema_version="cmf.sonic_timeline_manifest.v1",
            timeline_manifest_id=uuid4(),
            render_output_id=render_output_id,
            duration_ms=duration_ms,
            segments=parsed,
            timeline_hash=sonic_timeline_hash([item.model_dump(mode="json") for item in parsed] + [duration_ms]),
            created_at=utc_now(),
        )
        return self.repository.put_timeline_manifest(manifest)

    def evaluate_audio_ducking(
        self,
        *,
        audio_mix_manifest_id: UUID,
        ducking_rules: list[dict[str, Any]],
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> list[DuckingDecision]:
        manifest = self._audio(audio_mix_manifest_id)
        components = {item.component_id: item for item in manifest.components}
        decisions: list[DuckingDecision] = []
        for rule in ducking_rules:
            drivers = self._component_ids_from_rule(rule, components, "driver")
            ducked = self._component_ids_from_rule(rule, components, "ducked")
            missing = [item for item in [*drivers, *ducked] if item not in components]
            if missing:
                raise SonicTimelineError("DUCKING_COMPONENT_UNKNOWN", "Ducking rule references an unknown audio component.")
            if float(rule["gain_reduction_db"]) >= 0:
                raise SonicTimelineError("DUCKING_REDUCTION_REQUIRED", "Ducking gain reduction must be negative dB.")
            window = tuple(rule.get("affected_window_ms", self._overlap_window([components[item] for item in [*drivers, *ducked]])))
            decision_hash = sonic_timeline_hash(
                {
                    "audio_mix_manifest_id": audio_mix_manifest_id,
                    "ducking_rule_id": rule["ducking_rule_id"],
                    "drivers": drivers,
                    "ducked": ducked,
                    "window": window,
                    "gain_reduction_db": rule["gain_reduction_db"],
                }
            )
            decisions.append(
                self.repository.put_ducking_decision(
                    DuckingDecision(
                        schema_version="cmf.ducking_decision.v1",
                        ducking_decision_id=uuid4(),
                        audio_mix_manifest_id=audio_mix_manifest_id,
                        ducking_rule_id=rule["ducking_rule_id"],
                        driver_component_ids=drivers,
                        ducked_component_ids=ducked,
                        affected_window_ms=(int(window[0]), int(window[1])),
                        gain_reduction_db=float(rule["gain_reduction_db"]),
                        reason=rule.get("reason", "Protect source/interviewer voice intelligibility."),
                        decision_hash=decision_hash,
                        created_at=utc_now(),
                    )
                )
            )
        return decisions

    def validate_voice_bridge_policy(
        self,
        *,
        audio_mix_manifest_id: UUID,
        actor_id: UUID,
        voice_boost_report: VoiceBoostEligibilityReport | None = None,
        voice_bridge_manifest_id: UUID | None = None,
        command_id: UUID | None = None,
    ) -> VoiceBridgePolicyValidation:
        manifest = self._audio(audio_mix_manifest_id)
        synthetic_components = [
            item for item in manifest.components if item.role == SonicAudioComponentRole.synthetic_bridge
        ]
        if not synthetic_components:
            validation = VoiceBridgePolicyValidation(
                schema_version="cmf.voice_bridge_policy_validation.v1",
                voice_bridge_policy_validation_id=uuid4(),
                audio_mix_manifest_id=audio_mix_manifest_id,
                synthetic_component_ids=[],
                passed=True,
                evidence_refs=["no_synthetic_bridge_components"],
                created_at=utc_now(),
            )
            return self.repository.put_voice_policy_validation(validation)

        if voice_boost_report is None:
            validation = self._blocked_voice_validation(
                audio_mix_manifest_id=audio_mix_manifest_id,
                synthetic_component_ids=[item.component_id for item in synthetic_components],
                blocker_codes=["VOICE_BRIDGE_POLICY_REPORT_REQUIRED"],
            )
            raise SonicTimelineError("VOICE_BRIDGE_POLICY_REPORT_REQUIRED", "Synthetic bridge audio requires Voice-DNA Boost policy validation.")

        blocker_codes: list[str] = []
        if voice_boost_report.render_output_id != manifest.render_output_id:
            blocker_codes.append("VOICE_BRIDGE_RENDER_OUTPUT_MISMATCH")
        if voice_boost_report.status != VoiceEligibilityStatus.eligible:
            blocker_codes.extend(voice_boost_report.blocker_codes or ["VOICE_BOOST_NOT_ELIGIBLE"])
        if not voice_boost_report.visual_covering_provided:
            blocker_codes.append("VOICE_BRIDGE_VISUAL_COVERING_REQUIRED")
        if not voice_boost_report.claim_restriction_passed:
            blocker_codes.append("VOICE_BRIDGE_CLAIM_RESTRICTED")
        if voice_boost_report.requested_duration_seconds > voice_boost_report.max_duration_seconds:
            blocker_codes.append("VOICE_BRIDGE_DURATION_CAP_EXCEEDED")

        validation = VoiceBridgePolicyValidation(
            schema_version="cmf.voice_bridge_policy_validation.v1",
            voice_bridge_policy_validation_id=uuid4(),
            audio_mix_manifest_id=audio_mix_manifest_id,
            voice_boost_eligibility_report_id=voice_boost_report.voice_boost_eligibility_report_id,
            voice_bridge_manifest_id=voice_bridge_manifest_id,
            synthetic_component_ids=[item.component_id for item in synthetic_components],
            passed=not blocker_codes,
            blocker_codes=blocker_codes,
            max_duration_seconds=voice_boost_report.max_duration_seconds,
            requested_duration_seconds=voice_boost_report.requested_duration_seconds,
            visual_covering_ref=next((ref for ref in voice_boost_report.evidence_refs if "cover" in ref.lower()), None),
            evidence_refs=voice_boost_report.evidence_refs + [str(item) for item in voice_boost_report.evaluation_receipt_ids],
            created_at=utc_now(),
        )
        self.repository.put_voice_policy_validation(validation)
        if blocker_codes:
            raise SonicTimelineError("VOICE_BRIDGE_POLICY_BLOCKED", "Synthetic bridge audio failed Voice-DNA Boost policy validation.")
        return validation

    def write_sonic_timeline_receipt(
        self,
        *,
        render_output_id: UUID,
        audio_mix_manifest_id: UUID,
        caption_manifest_id: UUID,
        timeline_manifest_id: UUID,
        actor_id: UUID,
        ducking_decision_ids: list[UUID] | None = None,
        voice_bridge_policy_validation_id: UUID | None = None,
        command_id: UUID | None = None,
    ) -> SonicTimelineReceipt:
        audio = self._audio(audio_mix_manifest_id)
        captions = self._caption(caption_manifest_id)
        timeline = self._timeline(timeline_manifest_id)
        self._validate_same_render(render_output_id, audio, captions, timeline)
        self._validate_timing_against_timeline(audio, captions, timeline)
        final_mix = self._final_mix_component(audio)
        ducking_ids = ducking_decision_ids or self._ducking_ids_for_audio(audio.audio_mix_manifest_id)
        self._require_ducking_if_music_overlaps_voice(audio, ducking_ids)
        voice_validation_id = voice_bridge_policy_validation_id or self._voice_validation_id_for_audio(audio.audio_mix_manifest_id)
        self._require_voice_validation_for_synthetic(audio, voice_validation_id)
        receipt = new_sonic_timeline_receipt(
            render_output_id=render_output_id,
            audio_mix_manifest=audio,
            caption_manifest=captions,
            timeline_manifest=timeline,
            final_mix_ref=final_mix.source_ref,
            actor_id=actor_id,
            ducking_decision_ids=ducking_ids,
            voice_bridge_policy_validation_id=voice_validation_id,
            validation_summary="voice/caption/timing validation passed with role-separated audio and auditable final mix lineage.",
            evidence_refs=[
                audio.mix_hash,
                captions.manifest_hash,
                timeline.timeline_hash,
                *[str(item) for item in ducking_ids],
                *(["voice_bridge_policy_validated"] if voice_validation_id else []),
            ],
            command_id=command_id,
        )
        return self.repository.put_receipt(receipt)

    def stage12_audio_caption_timeline_assembly(
        self,
        *,
        render_output_id: UUID,
        audio_components: list[dict[str, Any]],
        caption_segments: list[dict[str, Any]],
        duration_ms: int,
        actor_id: UUID,
        platform_variant: str = "9:16",
        style_constraints: dict[str, Any] | None = None,
        timeline_segments: list[dict[str, Any]] | None = None,
        ducking_rules: list[dict[str, Any]] | None = None,
        voice_boost_report: VoiceBoostEligibilityReport | None = None,
        voice_bridge_manifest_id: UUID | None = None,
    ) -> SonicTimelineReceipt:
        audio = self.compile_audio_mix_manifest(
            render_output_id=render_output_id,
            components=audio_components,
            actor_id=actor_id,
        )
        captions = self.compile_caption_manifest(
            render_output_id=render_output_id,
            platform_variant=platform_variant,
            caption_segments=caption_segments,
            style_constraints=style_constraints,
            actor_id=actor_id,
        )
        timeline = self.compile_timeline_manifest(
            render_output_id=render_output_id,
            duration_ms=duration_ms,
            segments=timeline_segments or self._default_timeline_segments(audio, captions, duration_ms),
            actor_id=actor_id,
        )
        ducking = self.evaluate_audio_ducking(
            audio_mix_manifest_id=audio.audio_mix_manifest_id,
            ducking_rules=ducking_rules or self._default_ducking_rules(audio),
            actor_id=actor_id,
        )
        voice_validation = self.validate_voice_bridge_policy(
            audio_mix_manifest_id=audio.audio_mix_manifest_id,
            voice_boost_report=voice_boost_report,
            voice_bridge_manifest_id=voice_bridge_manifest_id,
            actor_id=actor_id,
        )
        return self.write_sonic_timeline_receipt(
            render_output_id=render_output_id,
            audio_mix_manifest_id=audio.audio_mix_manifest_id,
            caption_manifest_id=captions.caption_manifest_id,
            timeline_manifest_id=timeline.timeline_manifest_id,
            ducking_decision_ids=[item.ducking_decision_id for item in ducking],
            voice_bridge_policy_validation_id=voice_validation.voice_bridge_policy_validation_id,
            actor_id=actor_id,
        )

    def build_review_read_model(self, sonic_timeline_receipt_id: UUID) -> SonicTimelineReviewReadModel:
        receipt = self.repository.receipts.get(sonic_timeline_receipt_id)
        if receipt is None:
            raise SonicTimelineError("SONIC_TIMELINE_RECEIPT_REQUIRED", "Sonic timeline receipt is required.")
        audio = self._audio(receipt.audio_mix_manifest_id)
        captions = self._caption(receipt.caption_manifest_id)
        timeline = self._timeline(receipt.timeline_manifest_id)
        final_mix = self._final_mix_component(audio)
        return SonicTimelineReviewReadModel(
            schema_version="cmf.sonic_timeline_review_read_model.v1",
            sonic_timeline_receipt_id=receipt.sonic_timeline_receipt_id,
            render_output_id=receipt.render_output_id,
            audio_lineage=[
                {
                    "component_id": str(item.component_id),
                    "role": item.role.value,
                    "source_ref": item.source_ref,
                    "provider_receipt_id": str(item.provider_receipt_id) if item.provider_receipt_id else None,
                    "content_hash": item.content_hash,
                    "start_ms": item.start_ms,
                    "end_ms": item.end_ms,
                }
                for item in audio.components
            ],
            caption_lineage=[
                {
                    "caption_segment_id": str(item.caption_segment_id),
                    "text_source_ref": item.text_source_ref,
                    "start_ms": item.start_ms,
                    "end_ms": item.end_ms,
                    "style_tags": item.style_tags,
                }
                for item in captions.caption_segments
            ],
            timeline_lineage=[item.model_dump(mode="json") for item in timeline.segments],
            mix_lineage={
                "final_mix_ref": final_mix.source_ref,
                "ducking_decision_ids": [str(item) for item in receipt.ducking_decision_ids],
                "voice_bridge_policy_validation_id": str(receipt.voice_bridge_policy_validation_id)
                if receipt.voice_bridge_policy_validation_id
                else None,
            },
            manifest_hashes={
                "audio_mix_hash": receipt.audio_mix_hash,
                "caption_hash": receipt.caption_hash,
                "timeline_hash": receipt.timeline_hash,
            },
            validation_summary=receipt.validation_summary,
        )

    def _audio_component(self, payload: dict[str, Any]) -> AudioTimelineComponent:
        role = SonicAudioComponentRole(payload["role"])
        source_ref = payload["source_ref"]
        content_hash = payload.get("content_hash") or sonic_timeline_hash(
            {
                "role": role.value,
                "source_ref": source_ref,
                "source_artifact_id": payload.get("source_artifact_id"),
                "provider_receipt_id": payload.get("provider_receipt_id"),
                "start_ms": payload["start_ms"],
                "end_ms": payload["end_ms"],
                "gain_db": payload.get("gain_db"),
                "ducking_rule_id": payload.get("ducking_rule_id"),
            }
        )
        return AudioTimelineComponent(
            schema_version="cmf.audio_timeline_component.v1",
            component_id=self._uuid(payload.get("component_id")) or uuid4(),
            role=role,
            source_ref=source_ref,
            source_artifact_id=self._uuid(payload.get("source_artifact_id")),
            provider_receipt_id=self._uuid(payload.get("provider_receipt_id")),
            start_ms=int(payload["start_ms"]),
            end_ms=int(payload["end_ms"]),
            gain_db=payload.get("gain_db"),
            ducking_rule_id=payload.get("ducking_rule_id"),
            content_hash=content_hash,
        )

    def _caption_segment(self, payload: dict[str, Any], constraints: dict[str, Any]) -> CaptionSegment:
        max_chars = constraints.get("max_chars_per_segment")
        text = payload["text"]
        if max_chars is not None and len(text) > int(max_chars):
            raise SonicTimelineError("CAPTION_PLATFORM_LIMIT_EXCEEDED", "Caption text exceeds platform segment limit.")
        try:
            return CaptionSegment(
                schema_version="cmf.caption_segment.v1",
                caption_segment_id=self._uuid(payload.get("caption_segment_id")) or uuid4(),
                text=text,
                start_ms=int(payload["start_ms"]),
                end_ms=int(payload["end_ms"]),
                source_start_ms=int(payload.get("source_start_ms", payload["start_ms"])),
                source_end_ms=int(payload.get("source_end_ms", payload["end_ms"])),
                text_source_ref=payload["text_source_ref"],
                style_tags=list(payload.get("style_tags", [])),
            )
        except Exception as exc:
            raise SonicTimelineError("CAPTION_SOURCE_TIMING_CONFLICT", str(exc)) from exc

    def _timeline_segment(self, payload: dict[str, Any]) -> SonicTimelineSegment:
        return SonicTimelineSegment(
            schema_version="cmf.sonic_timeline_segment.v1",
            timeline_segment_id=self._uuid(payload.get("timeline_segment_id")) or uuid4(),
            track=payload["track"],
            source_ref=payload["source_ref"],
            component_refs=[self._uuid(item) or UUID(str(item)) for item in payload.get("component_refs", [])],
            start_ms=int(payload["start_ms"]),
            end_ms=int(payload["end_ms"]),
        )

    def _validate_audio_roles(self, components: list[AudioTimelineComponent]) -> None:
        if not any(item.role == SonicAudioComponentRole.final_mix for item in components):
            raise SonicTimelineError("FINAL_MIX_COMPONENT_REQUIRED", "Audio mix manifest must include a final mix component.")
        for item in components:
            if item.role == SonicAudioComponentRole.source_guest and item.source_ref.startswith(("synthetic_bridge:", "sfx:", "music:", "final_mix:")):
                raise SonicTimelineError("AUDIO_SOURCE_ROLE_CONFLICT", "Source guest audio cannot point at synthetic, SFX, music, or final mix refs.")
            if item.role == SonicAudioComponentRole.synthetic_bridge and not item.source_ref.startswith("synthetic_bridge:"):
                raise SonicTimelineError("SYNTHETIC_BRIDGE_REF_REQUIRED", "Synthetic bridge audio must use a synthetic_bridge source ref.")
            if item.role == SonicAudioComponentRole.final_mix and not item.source_ref.startswith(("final_mix:", "object://mixes/")):
                raise SonicTimelineError("FINAL_MIX_REF_REQUIRED", "Final mix audio must use a final_mix or object://mixes ref.")

    def _validate_same_render(
        self,
        render_output_id: UUID,
        audio: SonicAudioMixManifest,
        captions: SonicCaptionManifest,
        timeline: SonicTimelineManifest,
    ) -> None:
        ids = {audio.render_output_id, captions.render_output_id, timeline.render_output_id}
        if ids != {render_output_id}:
            raise SonicTimelineError("SONIC_TIMELINE_RENDER_MISMATCH", "Audio, captions, and timeline must belong to the same render output.")

    def _validate_timing_against_timeline(
        self,
        audio: SonicAudioMixManifest,
        captions: SonicCaptionManifest,
        timeline: SonicTimelineManifest,
    ) -> None:
        for item in audio.components:
            if item.end_ms > timeline.duration_ms:
                raise SonicTimelineError("AUDIO_COMPONENT_OUT_OF_RANGE", "Audio component exceeds timeline duration.")
        for segment in captions.caption_segments:
            if segment.end_ms > timeline.duration_ms:
                raise SonicTimelineError("CAPTION_TIMING_OUT_OF_RANGE", "Caption exceeds timeline duration.")

    def _require_ducking_if_music_overlaps_voice(self, audio: SonicAudioMixManifest, ducking_ids: list[UUID]) -> None:
        music = [item for item in audio.components if item.role == SonicAudioComponentRole.music]
        voice_roles = {
            SonicAudioComponentRole.source_guest,
            SonicAudioComponentRole.interviewer,
            SonicAudioComponentRole.restored_source,
            SonicAudioComponentRole.synthetic_bridge,
        }
        voices = [item for item in audio.components if item.role in voice_roles]
        needs_ducking = any(self._overlaps(music_item, voice_item) for music_item in music for voice_item in voices)
        if needs_ducking and not ducking_ids:
            raise SonicTimelineError("DUCKING_DECISION_REQUIRED", "Music or SFX overlap with voice requires recorded ducking decisions.")
        for decision_id in ducking_ids:
            decision = self.repository.ducking_decisions.get(decision_id)
            if decision is None or decision.audio_mix_manifest_id != audio.audio_mix_manifest_id:
                raise SonicTimelineError("DUCKING_DECISION_MISMATCH", "Ducking decision must belong to the audio mix manifest.")

    def _require_voice_validation_for_synthetic(self, audio: SonicAudioMixManifest, validation_id: UUID | None) -> None:
        synthetic = [item for item in audio.components if item.role == SonicAudioComponentRole.synthetic_bridge]
        if not synthetic:
            return
        if validation_id is None:
            raise SonicTimelineError("VOICE_BRIDGE_POLICY_VALIDATION_REQUIRED", "Synthetic bridge components require policy validation.")
        validation = self.repository.voice_policy_validations.get(validation_id)
        if validation is None or validation.audio_mix_manifest_id != audio.audio_mix_manifest_id:
            raise SonicTimelineError("VOICE_BRIDGE_POLICY_VALIDATION_MISMATCH", "Voice bridge validation must belong to the audio mix manifest.")
        if not validation.passed:
            raise SonicTimelineError("VOICE_BRIDGE_POLICY_BLOCKED", "Voice bridge policy validation did not pass.")

    def _default_timeline_segments(
        self,
        audio: SonicAudioMixManifest,
        captions: SonicCaptionManifest,
        duration_ms: int,
    ) -> list[dict[str, Any]]:
        caption_start = min(item.start_ms for item in captions.caption_segments)
        caption_end = max(item.end_ms for item in captions.caption_segments)
        return [
            {
                "track": "audio",
                "source_ref": f"audio_mix_manifest:{audio.audio_mix_manifest_id}",
                "component_refs": [item.component_id for item in audio.components],
                "start_ms": 0,
                "end_ms": duration_ms,
            },
            {
                "track": "caption",
                "source_ref": f"caption_manifest:{captions.caption_manifest_id}",
                "component_refs": [],
                "start_ms": caption_start,
                "end_ms": caption_end,
            },
        ]

    def _default_ducking_rules(self, audio: SonicAudioMixManifest) -> list[dict[str, Any]]:
        music = [item for item in audio.components if item.role == SonicAudioComponentRole.music]
        voice = [
            item
            for item in audio.components
            if item.role
            in {
                SonicAudioComponentRole.source_guest,
                SonicAudioComponentRole.interviewer,
                SonicAudioComponentRole.restored_source,
                SonicAudioComponentRole.synthetic_bridge,
            }
        ]
        if not music or not voice:
            return []
        return [
            {
                "ducking_rule_id": "legacy-audio-engine:voice-over-music-duck",
                "driver_component_ids": [item.component_id for item in voice],
                "ducked_component_ids": [item.component_id for item in music],
                "affected_window_ms": (min(item.start_ms for item in voice), max(item.end_ms for item in voice)),
                "gain_reduction_db": -9.0,
                "reason": "Legacy audio engine fixture protects source/interviewer intelligibility over music bed.",
            }
        ]

    def _component_ids_from_rule(
        self,
        rule: dict[str, Any],
        components: dict[UUID, AudioTimelineComponent],
        prefix: str,
    ) -> list[UUID]:
        explicit_key = f"{prefix}_component_ids"
        role_key = f"{prefix}_roles"
        if explicit_key in rule:
            return [self._uuid(item) or UUID(str(item)) for item in rule[explicit_key]]
        roles = {SonicAudioComponentRole(item) for item in rule.get(role_key, [])}
        return [component_id for component_id, component in components.items() if component.role in roles]

    @staticmethod
    def _overlap_window(components: list[AudioTimelineComponent]) -> tuple[int, int]:
        return min(item.start_ms for item in components), max(item.end_ms for item in components)

    @staticmethod
    def _overlaps(left: AudioTimelineComponent, right: AudioTimelineComponent) -> bool:
        return left.start_ms < right.end_ms and right.start_ms < left.end_ms

    def _final_mix_component(self, audio: SonicAudioMixManifest) -> AudioTimelineComponent:
        final_mix = next((item for item in audio.components if item.role == SonicAudioComponentRole.final_mix), None)
        if final_mix is None:
            raise SonicTimelineError("FINAL_MIX_COMPONENT_REQUIRED", "Final mix component is required.")
        return final_mix

    def _ducking_ids_for_audio(self, audio_mix_manifest_id: UUID) -> list[UUID]:
        return [
            item.ducking_decision_id
            for item in self.repository.ducking_decisions.values()
            if item.audio_mix_manifest_id == audio_mix_manifest_id
        ]

    def _voice_validation_id_for_audio(self, audio_mix_manifest_id: UUID) -> UUID | None:
        validation = next(
            (
                item
                for item in self.repository.voice_policy_validations.values()
                if item.audio_mix_manifest_id == audio_mix_manifest_id and item.passed
            ),
            None,
        )
        return validation.voice_bridge_policy_validation_id if validation else None

    def _blocked_voice_validation(
        self,
        *,
        audio_mix_manifest_id: UUID,
        synthetic_component_ids: list[UUID],
        blocker_codes: list[str],
    ) -> VoiceBridgePolicyValidation:
        return self.repository.put_voice_policy_validation(
            VoiceBridgePolicyValidation(
                schema_version="cmf.voice_bridge_policy_validation.v1",
                voice_bridge_policy_validation_id=uuid4(),
                audio_mix_manifest_id=audio_mix_manifest_id,
                synthetic_component_ids=synthetic_component_ids,
                passed=False,
                blocker_codes=blocker_codes,
                created_at=utc_now(),
            )
        )

    def _audio(self, audio_mix_manifest_id: UUID) -> SonicAudioMixManifest:
        manifest = self.repository.audio_mix_manifests.get(audio_mix_manifest_id)
        if manifest is None:
            raise SonicTimelineError("AUDIO_MIX_MANIFEST_REQUIRED", "Audio mix manifest is required.")
        return manifest

    def _caption(self, caption_manifest_id: UUID) -> SonicCaptionManifest:
        manifest = self.repository.caption_manifests.get(caption_manifest_id)
        if manifest is None:
            raise SonicTimelineError("CAPTION_MANIFEST_REQUIRED", "Caption manifest is required.")
        return manifest

    def _timeline(self, timeline_manifest_id: UUID) -> SonicTimelineManifest:
        manifest = self.repository.timeline_manifests.get(timeline_manifest_id)
        if manifest is None:
            raise SonicTimelineError("TIMELINE_MANIFEST_REQUIRED", "Timeline manifest is required.")
        return manifest

    @staticmethod
    def _uuid(value: Any) -> UUID | None:
        if value is None:
            return None
        if isinstance(value, UUID):
            return value
        return UUID(str(value))


@dataclass
class SonicTimelineCommandHandler:
    command_type: str
    service: SonicTimelineService
    aggregate_type: str = "sonic_timeline"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward", "reviewer"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CompileAudioMixManifestCommand":
            return self.service.compile_audio_mix_manifest(
                render_output_id=UUID(payload["render_output_id"]),
                components=payload["components"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "CompileCaptionManifestCommand":
            return self.service.compile_caption_manifest(
                render_output_id=UUID(payload["render_output_id"]),
                platform_variant=payload["platform_variant"],
                caption_segments=payload["caption_segments"],
                style_constraints=payload.get("style_constraints"),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "CompileTimelineManifestCommand":
            return self.service.compile_timeline_manifest(
                render_output_id=UUID(payload["render_output_id"]),
                duration_ms=int(payload["duration_ms"]),
                segments=payload["segments"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "EvaluateAudioDuckingCommand":
            return {
                "ducking_decisions": [
                    item.model_dump(mode="json")
                    for item in self.service.evaluate_audio_ducking(
                        audio_mix_manifest_id=UUID(payload["audio_mix_manifest_id"]),
                        ducking_rules=payload["ducking_rules"],
                        actor_id=envelope.actor.actor_id,
                        command_id=envelope.command_id,
                    )
                ]
            }
        if self.command_type == "ValidateVoiceBridgePolicyCommand":
            report = (
                VoiceBoostEligibilityReport.model_validate(payload["voice_boost_report"])
                if payload.get("voice_boost_report")
                else None
            )
            return self.service.validate_voice_bridge_policy(
                audio_mix_manifest_id=UUID(payload["audio_mix_manifest_id"]),
                voice_boost_report=report,
                voice_bridge_manifest_id=UUID(payload["voice_bridge_manifest_id"]) if payload.get("voice_bridge_manifest_id") else None,
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "WriteSonicTimelineReceiptCommand":
            return self.service.write_sonic_timeline_receipt(
                render_output_id=UUID(payload["render_output_id"]),
                audio_mix_manifest_id=UUID(payload["audio_mix_manifest_id"]),
                caption_manifest_id=UUID(payload["caption_manifest_id"]),
                timeline_manifest_id=UUID(payload["timeline_manifest_id"]),
                ducking_decision_ids=[UUID(item) for item in payload.get("ducking_decision_ids", [])],
                voice_bridge_policy_validation_id=UUID(payload["voice_bridge_policy_validation_id"]) if payload.get("voice_bridge_policy_validation_id") else None,
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise SonicTimelineError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = (
            payload.get("sonic_timeline_receipt_id")
            or payload.get("audio_mix_manifest_id")
            or payload.get("caption_manifest_id")
            or payload.get("timeline_manifest_id")
            or envelope.payload.get("render_output_id")
        )
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_sonic_timeline_command_handlers(bus: CommandBus, service: SonicTimelineService) -> None:
    for command_type in [
        "CompileAudioMixManifestCommand",
        "CompileCaptionManifestCommand",
        "CompileTimelineManifestCommand",
        "EvaluateAudioDuckingCommand",
        "ValidateVoiceBridgePolicyCommand",
        "WriteSonicTimelineReceiptCommand",
    ]:
        bus.register_handler(SonicTimelineCommandHandler(command_type=command_type, service=service))
