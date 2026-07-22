"""Deterministic assembly planner for TS-CMF-039."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.assembly import (
    AnimationPlan,
    AssemblyPlan,
    AssemblyPlanReceipt,
    AudioComponentRole,
    AudioMixComponent,
    AudioMixManifest,
    CaptionCue,
    CaptionManifest,
    EditDecision,
    EditDecisionList,
    LayerEntry,
    LayerManifest,
    TimelineManifest,
    TimelineSegment,
    assembly_hash,
    new_assembly_plan_receipt,
)
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.scene_spec import SceneSpec
from ccp_studio.repositories.assembly import InMemoryAssemblyRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.composition_service import CompositionService
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


class AssemblyPlannerError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class AssemblyPlanner:
    scene_spec_compiler: SceneSpecCompiler
    composition_service: CompositionService | None = None
    repository: InMemoryAssemblyRepository = field(default_factory=InMemoryAssemblyRepository)

    def compile_assembly_plan(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
        caption_cues: list[dict[str, Any]] | None = None,
        audio_components: list[dict[str, Any]] | None = None,
        command_id: UUID | None = None,
    ) -> AssemblyPlan:
        scene_spec = self._scene_spec(scene_spec_id)
        session = self._session(scene_spec)
        render_contract = self.scene_spec_compiler.render_contract_for_scene(scene_spec_id)
        try:
            layer_manifest = self.repository.put_layer_manifest(self._layer_manifest(scene_spec))
            animation_plan = self.repository.put_animation_plan(self._animation_plan(scene_spec, layer_manifest))
            edl = self.repository.put_edit_decision_list(self._edit_decision_list(scene_spec, layer_manifest))
            timeline = self.repository.put_timeline_manifest(self._timeline_manifest(scene_spec, layer_manifest))
            captions = self.repository.put_caption_manifest(self._caption_manifest(scene_spec, caption_cues))
            self._validate_caption_timing(captions, scene_spec.duration_seconds)
            audio = self.repository.put_audio_mix_manifest(self._audio_mix_manifest(scene_spec, audio_components))
            self._validate_audio_components(audio)
            manifest_hashes = {
                "layer_manifest_hash": layer_manifest.manifest_hash,
                "animation_plan_hash": animation_plan.plan_hash,
                "edit_decision_list_hash": edl.edl_hash,
                "timeline_manifest_hash": timeline.timeline_hash,
                "caption_manifest_hash": captions.caption_hash,
                "audio_mix_manifest_hash": audio.mix_hash,
            }
            selected_asset_ids = [
                layer.brand_context_asset_id
                for layer in layer_manifest.layers
                if layer.brand_context_asset_id is not None
            ]
            plan = self.repository.put_assembly_plan(
                AssemblyPlan(
                    schema_version="cmf.assembly_plan.v1",
                    assembly_plan_id=uuid4(),
                    scene_spec_id=scene_spec.scene_spec_id,
                    complete_editing_session_id=scene_spec.complete_editing_session_id,
                    layer_manifest_id=layer_manifest.layer_manifest_id,
                    animation_plan_id=animation_plan.animation_plan_id,
                    edit_decision_list_id=edl.edit_decision_list_id,
                    timeline_manifest_id=timeline.timeline_manifest_id,
                    caption_manifest_id=captions.caption_manifest_id,
                    audio_mix_manifest_id=audio.audio_mix_manifest_id,
                    renderer_route=render_contract.renderer_route,
                    manifest_hashes=manifest_hashes,
                    selected_asset_ids=selected_asset_ids,
                    valid_for_render=True,
                    created_at=utc_now(),
                )
            )
            self.repository.put_receipt(
                new_assembly_plan_receipt(
                    organization_id=session.organization_id,
                    brand_id=session.brand_id,
                    actor_id=actor_id,
                    complete_editing_session_id=scene_spec.complete_editing_session_id,
                    scene_spec_id=scene_spec.scene_spec_id,
                    assembly_plan_id=plan.assembly_plan_id,
                    layer_manifest_id=layer_manifest.layer_manifest_id,
                    animation_plan_id=animation_plan.animation_plan_id,
                    edit_decision_list_id=edl.edit_decision_list_id,
                    timeline_manifest_id=timeline.timeline_manifest_id,
                    caption_manifest_id=captions.caption_manifest_id,
                    audio_mix_manifest_id=audio.audio_mix_manifest_id,
                    manifest_hashes=manifest_hashes,
                    selected_asset_ids=selected_asset_ids,
                    brand_context_version_id=scene_spec.brand_context_version_id,
                    brand_context_version_hash=scene_spec.brand_context_version_hash,
                    timing_validation_passed=True,
                    caption_validation_passed=True,
                    sonic_validation_passed=True,
                    renderer_route=render_contract.renderer_route,
                    decision_code="ASSEMBLY_PLAN_VALIDATED",
                    evidence_refs=[
                        f"scene_spec:{scene_spec.scene_spec_id}",
                        f"render_contract:{render_contract.render_contract_id}",
                        *manifest_hashes.values(),
                    ],
                    command_id=command_id,
                )
            )
            return plan
        except Exception as exc:
            code = getattr(exc, "code", "ASSEMBLY_PLAN_INVALID")
            self._blocked_receipt(scene_spec, actor_id, code, command_id)
            if isinstance(exc, AssemblyPlannerError):
                raise
            raise AssemblyPlannerError(code, str(exc)) from exc

    def validate_assembly_plan(self, assembly_plan_id: UUID) -> AssemblyPlan:
        plan = self.repository.assembly_plans.get(assembly_plan_id)
        if plan is None:
            raise AssemblyPlannerError("ASSEMBLY_PLAN_REQUIRED", "Assembly plan is required.")
        if not plan.valid_for_render or not plan.manifest_hashes:
            raise AssemblyPlannerError("ASSEMBLY_PLAN_INVALID", "Assembly plan is not valid for render.")
        return plan

    def block_render_without_assembly_plan(self, *, scene_spec_id: UUID, actor_id: UUID, command_id: UUID | None = None) -> AssemblyPlanReceipt:
        existing = next((item for item in self.repository.assembly_plans.values() if item.scene_spec_id == scene_spec_id), None)
        if existing is not None and existing.valid_for_render:
            raise AssemblyPlannerError("ASSEMBLY_PLAN_ALREADY_PRESENT", "Render is not blocked because assembly plan is present.")
        scene_spec = self._scene_spec(scene_spec_id)
        return self._blocked_receipt(scene_spec, actor_id, "ASSEMBLY_PLAN_REQUIRED", command_id)

    def _layer_manifest(self, scene_spec: SceneSpec) -> LayerManifest:
        width, height = self._canvas(scene_spec.aspect_ratio)
        layers: list[LayerEntry] = []
        for index, selection_id in enumerate(scene_spec.asset_selection_ids, start=1):
            selection = self.scene_spec_compiler.repository.asset_selections[selection_id]
            self._validate_brand_asset(scene_spec, selection.asset_id)
            layers.append(
                LayerEntry(
                    schema_version="cmf.layer_entry.v1",
                    layer_id=uuid4(),
                    semantic_type=selection.asset_type,
                    file_uri=f"brand://{selection.asset_ref}",
                    asset_hash=selection.asset_hash,
                    z_index=index,
                    bbox=(0, 0, width, height),
                    anchor_point=(0.5, 0.5),
                    motion_affordances=["subtle_parallax", "paper_cut_hold"],
                    brand_context_asset_id=selection.asset_id,
                    source_ref=selection.source_ref or selection.asset_ref,
                )
            )
        plate = self._composition_plate(scene_spec.scene_spec_id)
        if plate is not None:
            layers.append(
                LayerEntry(
                    schema_version="cmf.layer_entry.v1",
                    layer_id=uuid4(),
                    semantic_type="composition_plate",
                    file_uri=plate.plate_uri,
                    asset_hash=plate.plate_hash,
                    z_index=0,
                    bbox=(0, 0, width, height),
                    anchor_point=(0.5, 0.5),
                    motion_affordances=["background_reference_only"],
                    brand_context_asset_id=None,
                    source_ref=f"composition_plate:{plate.composition_plate_id}",
                )
            )
        manifest_id = uuid4()
        manifest_hash = assembly_hash({"scene_spec_id": scene_spec.scene_spec_id, "layers": [item.model_dump(mode="json") for item in layers]})
        return LayerManifest(
            schema_version="cmf.layer_manifest.v1",
            layer_manifest_id=manifest_id,
            scene_spec_id=scene_spec.scene_spec_id,
            canvas_width=width,
            canvas_height=height,
            aspect_ratio=scene_spec.aspect_ratio,
            layers=layers,
            manifest_hash=manifest_hash,
        )

    def _animation_plan(self, scene_spec: SceneSpec, layer_manifest: LayerManifest) -> AnimationPlan:
        fps = 30
        duration_frames = int(scene_spec.duration_seconds * fps)
        animations = [
            {
                "layer_id": str(layer.layer_id),
                "motion": "micro_parallax" if layer.semantic_type != "composition_plate" else "locked_background_reference",
                "start_frame": 0,
                "end_frame": duration_frames,
            }
            for layer in layer_manifest.layers
        ]
        return AnimationPlan(
            schema_version="cmf.animation_plan.v1",
            animation_plan_id=uuid4(),
            layer_manifest_id=layer_manifest.layer_manifest_id,
            fps=fps,
            duration_frames=duration_frames,
            motion_style="restrained_paper_cut_motion",
            layer_animations=animations,
            plan_hash=assembly_hash({"layer_manifest_hash": layer_manifest.manifest_hash, "animations": animations}),
        )

    def _edit_decision_list(self, scene_spec: SceneSpec, layer_manifest: LayerManifest) -> EditDecisionList:
        decisions = [
            EditDecision(
                schema_version="cmf.edit_decision.v1",
                edit_decision_id=uuid4(),
                source_ref=layer.source_ref,
                track=f"v{index}",
                start_seconds=0,
                end_seconds=scene_spec.duration_seconds,
                operation="place_layer",
            )
            for index, layer in enumerate(layer_manifest.layers, start=1)
        ]
        return EditDecisionList(
            schema_version="cmf.edit_decision_list.v1",
            edit_decision_list_id=uuid4(),
            scene_spec_id=scene_spec.scene_spec_id,
            decisions=decisions,
            edl_hash=assembly_hash([item.model_dump(mode="json") for item in decisions]),
        )

    def _timeline_manifest(self, scene_spec: SceneSpec, layer_manifest: LayerManifest) -> TimelineManifest:
        segments = [
            TimelineSegment(
                schema_version="cmf.timeline_segment.v1",
                segment_id=uuid4(),
                track="visual",
                source_ref=f"layer_manifest:{layer_manifest.layer_manifest_id}",
                start_seconds=0,
                end_seconds=scene_spec.duration_seconds,
            ),
            TimelineSegment(
                schema_version="cmf.timeline_segment.v1",
                segment_id=uuid4(),
                track="caption",
                source_ref=f"source_expression_moment:{scene_spec.source_expression_moment_id}",
                start_seconds=0.5,
                end_seconds=max(0.6, scene_spec.duration_seconds - 0.5),
            ),
        ]
        return TimelineManifest(
            schema_version="cmf.timeline_manifest.v1",
            timeline_manifest_id=uuid4(),
            scene_spec_id=scene_spec.scene_spec_id,
            duration_seconds=scene_spec.duration_seconds,
            segments=segments,
            timeline_hash=assembly_hash([item.model_dump(mode="json") for item in segments]),
        )

    def _caption_manifest(self, scene_spec: SceneSpec, requests: list[dict[str, Any]] | None) -> CaptionManifest:
        requests = requests or [
            {
                "text": "Source-backed expression caption",
                "start_seconds": 0.5,
                "end_seconds": min(scene_spec.duration_seconds, 4.5),
                "source_start_seconds": 0.0,
                "source_end_seconds": min(scene_spec.duration_seconds, 5.0),
                "source_ref": f"source_expression_moment:{scene_spec.source_expression_moment_id}",
            }
        ]
        cues = [
            CaptionCue(
                schema_version="cmf.caption_cue.v1",
                caption_cue_id=uuid4(),
                text=item["text"],
                start_seconds=float(item["start_seconds"]),
                end_seconds=float(item["end_seconds"]),
                source_start_seconds=float(item.get("source_start_seconds", item["start_seconds"])),
                source_end_seconds=float(item.get("source_end_seconds", item["end_seconds"])),
                source_ref=item["source_ref"],
            )
            for item in requests
        ]
        text_space = scene_spec.subject.text_space or "caption_safe_negative_space"
        return CaptionManifest(
            schema_version="cmf.caption_manifest.v1",
            caption_manifest_id=uuid4(),
            scene_spec_id=scene_spec.scene_spec_id,
            cues=cues,
            negative_space_rule=text_space,
            caption_hash=assembly_hash([item.model_dump(mode="json") for item in cues] + [text_space]),
        )

    def _audio_mix_manifest(self, scene_spec: SceneSpec, requests: list[dict[str, Any]] | None) -> AudioMixManifest:
        requests = requests or [
            {
                "role": AudioComponentRole.source_voice.value,
                "source_ref": f"source_expression_moment:{scene_spec.source_expression_moment_id}",
                "start_seconds": 0,
                "end_seconds": min(scene_spec.duration_seconds, 8.0),
            },
            {
                "role": AudioComponentRole.sfx.value,
                "source_ref": "brand_context:sfx:paper_cut_soft_riser",
                "start_seconds": 0,
                "end_seconds": min(scene_spec.duration_seconds, 2.0),
            },
        ]
        components = [
            AudioMixComponent(
                schema_version="cmf.audio_mix_component.v1",
                audio_mix_component_id=uuid4(),
                role=AudioComponentRole(item["role"]),
                source_ref=item["source_ref"],
                start_seconds=float(item["start_seconds"]),
                end_seconds=float(item["end_seconds"]),
                provider_receipt_id=UUID(item["provider_receipt_id"]) if item.get("provider_receipt_id") else None,
            )
            for item in requests
        ]
        return AudioMixManifest(
            schema_version="cmf.assembly_audio_mix_manifest.v1",
            audio_mix_manifest_id=uuid4(),
            scene_spec_id=scene_spec.scene_spec_id,
            components=components,
            mix_hash=assembly_hash([item.model_dump(mode="json") for item in components]),
        )

    def _validate_caption_timing(self, manifest: CaptionManifest, duration_seconds: float) -> None:
        for cue in manifest.cues:
            if cue.end_seconds > duration_seconds:
                raise AssemblyPlannerError("CAPTION_TIMING_OUT_OF_RANGE", "Caption exceeds timeline duration.")
            if cue.start_seconds < cue.source_start_seconds or cue.end_seconds > cue.source_end_seconds:
                raise AssemblyPlannerError("CAPTION_SOURCE_TIMING_CONFLICT", "Caption timing conflicts with source phrase timing.")

    def _validate_audio_components(self, manifest: AudioMixManifest) -> None:
        for component in manifest.components:
            if component.role == AudioComponentRole.source_voice and component.source_ref.startswith(("synthetic_bridge:", "sfx:", "music:")):
                raise AssemblyPlannerError("AUDIO_SOURCE_ROLE_CONFLICT", "Synthetic, SFX, or music audio cannot be mixed as source voice.")
            if component.role == AudioComponentRole.synthetic_bridge_voice and not component.source_ref.startswith("synthetic_bridge:"):
                raise AssemblyPlannerError("SYNTHETIC_BRIDGE_REF_REQUIRED", "Synthetic bridge audio must use a synthetic_bridge source ref.")

    def _validate_brand_asset(self, scene_spec: SceneSpec, asset_id: UUID) -> None:
        session = self._session(scene_spec)
        try:
            self.scene_spec_compiler.gate_service.brand_context_service.assert_asset_in_locked_context(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                brand_context_version_id=scene_spec.brand_context_version_id,
                asset_id=asset_id,
            )
        except Exception as exc:
            code = getattr(exc, "code", "BRAND_LAYER_NOT_IN_LOCKED_CONTEXT")
            raise AssemblyPlannerError(code, str(exc)) from exc

    def _blocked_receipt(self, scene_spec: SceneSpec, actor_id: UUID, reason: str, command_id: UUID | None) -> AssemblyPlanReceipt:
        session = self._session(scene_spec)
        return self.repository.put_receipt(
            new_assembly_plan_receipt(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                actor_id=actor_id,
                complete_editing_session_id=scene_spec.complete_editing_session_id,
                scene_spec_id=scene_spec.scene_spec_id,
                brand_context_version_id=scene_spec.brand_context_version_id,
                brand_context_version_hash=scene_spec.brand_context_version_hash,
                decision_code="ASSEMBLY_PLAN_BLOCKED",
                evidence_refs=[reason],
                command_id=command_id,
            )
        )

    def _composition_plate(self, scene_spec_id: UUID):
        if self.composition_service is None:
            return None
        for job in self.composition_service.repository.composition_jobs.values():
            if job.scene_spec_id == scene_spec_id:
                return next((plate for plate in self.composition_service.repository.plates.values() if plate.composition_job_id == job.composition_job_id), None)
        return None

    def _scene_spec(self, scene_spec_id: UUID) -> SceneSpec:
        scene_spec = self.scene_spec_compiler.repository.scene_specs.get(scene_spec_id)
        if scene_spec is None:
            raise AssemblyPlannerError("SCENE_SPEC_REQUIRED", "SceneSpec is required for assembly planning.")
        return scene_spec

    def _session(self, scene_spec: SceneSpec):
        if self.scene_spec_compiler.editing_session_service is None:
            raise AssemblyPlannerError("EDITING_SESSION_SERVICE_REQUIRED", "Editing Session service is required.")
        return self.scene_spec_compiler.editing_session_service.repository.sessions[scene_spec.complete_editing_session_id]

    @staticmethod
    def _canvas(aspect_ratio: str) -> tuple[int, int]:
        return {
            "9:16": (1080, 1920),
            "4:5": (1080, 1350),
            "1:1": (1080, 1080),
            "16:9": (1920, 1080),
        }.get(aspect_ratio, (1080, 1920))


@dataclass
class AssemblyCommandHandler:
    command_type: str
    service: AssemblyPlanner
    aggregate_type: str = "assembly_plan"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type in {
            "CompileLayerManifestCommand",
            "CompileAnimationPlanCommand",
            "CompileEditDecisionListCommand",
            "CompileCaptionManifestCommand",
            "CompileAudioMixManifestCommand",
        }:
            plan = self.service.compile_assembly_plan(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                caption_cues=payload.get("caption_cues"),
                audio_components=payload.get("audio_components"),
                command_id=envelope.command_id,
            )
            return plan.model_dump(mode="json")
        if self.command_type == "ValidateAssemblyPlanCommand":
            return self.service.validate_assembly_plan(UUID(payload["assembly_plan_id"])).model_dump(mode="json")
        if self.command_type == "BlockRenderWithoutAssemblyPlanCommand":
            return self.service.block_render_without_assembly_plan(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise AssemblyPlannerError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("assembly_plan_id") or payload.get("scene_spec_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_assembly_command_handlers(bus: CommandBus, service: AssemblyPlanner) -> None:
    for command_type in [
        "CompileLayerManifestCommand",
        "CompileAnimationPlanCommand",
        "CompileEditDecisionListCommand",
        "CompileCaptionManifestCommand",
        "CompileAudioMixManifestCommand",
        "ValidateAssemblyPlanCommand",
        "BlockRenderWithoutAssemblyPlanCommand",
    ]:
        bus.register_handler(AssemblyCommandHandler(command_type=command_type, service=service))
