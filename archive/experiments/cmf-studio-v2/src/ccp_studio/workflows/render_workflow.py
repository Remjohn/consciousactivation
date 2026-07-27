"""Render workflow adapters for TS-CMF-039, TS-CMF-043, and TS-CMF-047."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.assembly import AssemblyPlan
from ccp_studio.contracts.deterministic_rendering import RenderOutput
from ccp_studio.contracts.sonic_timeline import SonicTimelineReceipt
from ccp_studio.services.assembly_planner import AssemblyPlanner
from ccp_studio.services.deterministic_rendering_service import DeterministicRenderService
from ccp_studio.services.sonic_timeline_service import SonicTimelineService


@dataclass
class RenderWorkflow:
    assembly_planner: AssemblyPlanner
    deterministic_render_service: DeterministicRenderService | None = None
    sonic_timeline_service: SonicTimelineService | None = None

    def stage12_compile_assembly_plan(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
        caption_cues: list[dict[str, Any]] | None = None,
        audio_components: list[dict[str, Any]] | None = None,
    ) -> AssemblyPlan:
        return self.assembly_planner.compile_assembly_plan(
            scene_spec_id=scene_spec_id,
            actor_id=actor_id,
            caption_cues=caption_cues,
            audio_components=audio_components,
        )

    def stage12_deterministic_render(
        self,
        *,
        render_contract_id: UUID,
        assembly_plan_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
    ) -> RenderOutput:
        if self.deterministic_render_service is None:
            raise RuntimeError("DeterministicRenderService is required for deterministic rendering.")
        return self.deterministic_render_service.stage12_deterministic_render(
            render_contract_id=render_contract_id,
            assembly_plan_id=assembly_plan_id,
            actor_id=actor_id,
            idempotency_key=idempotency_key,
        )

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
        voice_boost_report: Any | None = None,
        voice_bridge_manifest_id: UUID | None = None,
    ) -> SonicTimelineReceipt:
        if self.sonic_timeline_service is None:
            raise RuntimeError("SonicTimelineService is required for audio/caption/timeline assembly.")
        return self.sonic_timeline_service.stage12_audio_caption_timeline_assembly(
            render_output_id=render_output_id,
            audio_components=audio_components,
            caption_segments=caption_segments,
            duration_ms=duration_ms,
            actor_id=actor_id,
            platform_variant=platform_variant,
            style_constraints=style_constraints,
            timeline_segments=timeline_segments,
            ducking_rules=ducking_rules,
            voice_boost_report=voice_boost_report,
            voice_bridge_manifest_id=voice_bridge_manifest_id,
        )
