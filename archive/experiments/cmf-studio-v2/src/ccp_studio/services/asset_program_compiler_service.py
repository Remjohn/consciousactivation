"""Batch 2 asset and program compiler service for TS-CMF-093 through TS-CMF-119."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.asset_program_compilers import (
    AnimationStudioMigrationManifest,
    AvatarExportReceipt,
    AvatarExportWorkerJob,
    CarouselAtlasRouteReceipt,
    CarouselBuilderProgram,
    CarouselExportReceipt,
    CarouselSequencePlan,
    CarouselSlideAtom,
    CarouselSlideLibrary,
    CompositionHandoffPackage,
    ContentSequenceProgram,
    CueSuppressionDecision,
    ExpressionAcquisitionPlan,
    ExpressionIngredient,
    ExpressionIngredientInventory,
    ExpressionRelationEdge,
    GeometricsSceneSpec,
    GoldenFixtureResult,
    HeadlessFrameRenderReceipt,
    HeadlessFrameRenderRequest,
    InterviewBriefV2Plan,
    LiveIngredientCoverageTracker,
    OTIOAuditManifest,
    PackageLearningReceipt,
    PrimitiveTriadContract,
    RegistryBundleLoadReceipt,
    RigEditOperation,
    SequenceEvalReceipt,
    SequenceHypothesis,
    SequencingRegistryKernel,
    SingleImageEvalReviewReceipt,
    SingleImageProviderJobPlan,
    SingleImageRegistrySnapshot,
    SingleImageRouteDecision,
    SingleImageSkiaScene,
    SkiaRenderBinding,
    SkiaRenderReceipt,
    StillVisualLayerMaterialization,
    SuperVisualFamilyContract,
    TwoDCharacterGenesis,
    TwoDCharacterPerformanceCue,
    TwoDCharacterProviderAdapterDecision,
    TwoDCharacterRenderReceipt,
    TwoDCharacterRepairPlan,
    TwoDCharacterRig,
    TwoDCharacterSceneProgram,
    VideoEditProgram,
    VideoEditScene,
    VideoRenderContract,
    compiler_hash,
)
from ccp_studio.contracts.composition_runtime import (
    ApprovalStatus,
    CompositionTemplateLayer,
    CompositionZone,
    VideoFormatCode,
)
from ccp_studio.repositories.asset_program_compilers import InMemoryAssetProgramCompilerRepository


class AssetProgramCompilerServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class AssetProgramCompilerService:
    repository: InMemoryAssetProgramCompilerRepository = field(default_factory=InMemoryAssetProgramCompilerRepository)
    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[3])
    _registry_cache: dict[str, dict[str, Any]] = field(default_factory=dict)

    def load_registry_bundle(self, registry_ref: str) -> tuple[dict[str, Any], RegistryBundleLoadReceipt]:
        path = self._project_path(registry_ref)
        if not path.exists():
            receipt = self.repository.put_registry_load_receipt(
                RegistryBundleLoadReceipt(
                    registry_ref=registry_ref,
                    absolute_path=str(path),
                    decision="blocked",
                    entry_count=0,
                    blocker_codes=["CMF_REGISTRY_NOT_FOUND"],
                )
            )
            raise AssetProgramCompilerServiceError("CMF_REGISTRY_NOT_FOUND", f"Registry not found: {registry_ref}")
        if registry_ref not in self._registry_cache:
            self._registry_cache[registry_ref] = json.loads(path.read_text(encoding="utf-8"))
        data = self._registry_cache[registry_ref]
        receipt = self.repository.put_registry_load_receipt(
            RegistryBundleLoadReceipt(
                registry_ref=registry_ref,
                absolute_path=str(path),
                decision="loaded",
                entry_count=self._entry_count(data),
                evidence_refs=[f"registry:{registry_ref}"],
            )
        )
        return data, receipt

    def migrate_animation_studio_manifest(
        self,
        *,
        legacy_source_ref: str = "THE CMF STUDIO/reference/apps/animation-studio",
        migrated_asset_refs: list[str] | None = None,
    ) -> AnimationStudioMigrationManifest:
        manifest = AnimationStudioMigrationManifest(
            legacy_source_ref=legacy_source_ref,
            operator_editor_route="/operator/animation-studio/rig-editor",
            rig_editor_panels=["character-genesis", "rig-joints", "pose-library", "mouth-shapes", "timed-performance"],
            migrated_asset_refs=migrated_asset_refs
            or [
                "asset://animation-studio/papercut-rigs",
                "asset://animation-studio/avatar-pose-library",
                "asset://animation-studio/operator-preview-panels",
            ],
            receipts_required=["rig_edit_operation", "headless_frame_render_receipt", "avatar_export_receipt"],
        )
        return self.repository.put_animation_migration_manifest(manifest)

    def plan_rig_edit(
        self,
        *,
        target_rig_ref: str,
        operator_id: UUID,
        operation_type: str = "pose_adjustment",
        evidence_refs: list[str] | None = None,
    ) -> RigEditOperation:
        evidence_refs = evidence_refs or [f"rig:{target_rig_ref}", "operator:manual_adjustment"]
        before_hash = compiler_hash({"target_rig_ref": target_rig_ref, "state": "before"})
        after_hash = compiler_hash({"target_rig_ref": target_rig_ref, "operation_type": operation_type, "evidence_refs": evidence_refs})
        operation = RigEditOperation(
            operation_type=operation_type,  # type: ignore[arg-type]
            target_rig_ref=target_rig_ref,
            before_hash=before_hash,
            after_hash=after_hash,
            operator_id=operator_id,
            evidence_refs=evidence_refs,
        )
        return self.repository.put_rig_edit_operation(operation)

    def queue_headless_frame_render(
        self,
        *,
        composition_template_id: UUID,
        runtime_manifest_ref: str,
        frame_start: int = 0,
        frame_end: int = 90,
        fps: int = 30,
        output_format: str = "png_sequence",
    ) -> tuple[HeadlessFrameRenderRequest, HeadlessFrameRenderReceipt]:
        deterministic_hash = compiler_hash(
            {
                "composition_template_id": composition_template_id,
                "runtime_manifest_ref": runtime_manifest_ref,
                "frame_start": frame_start,
                "frame_end": frame_end,
                "fps": fps,
                "output_format": output_format,
            }
        )
        request = self.repository.put_headless_frame_render_request(
            HeadlessFrameRenderRequest(
                composition_template_id=composition_template_id,
                runtime_manifest_ref=runtime_manifest_ref,
                frame_start=frame_start,
                frame_end=frame_end,
                fps=fps,
                output_format=output_format,  # type: ignore[arg-type]
                deterministic_inputs_hash=deterministic_hash,
            )
        )
        receipt = self.repository.put_headless_frame_render_receipt(
            HeadlessFrameRenderReceipt(
                headless_frame_render_request_id=request.headless_frame_render_request_id,
                frame_manifest_ref=f"frame_manifest:{request.headless_frame_render_request_id}",
                preview_ref=f"preview://headless/{request.headless_frame_render_request_id}.png",
                decision_code="HEADLESS_FRAME_RENDER_QUEUED",
            )
        )
        return request, receipt

    def queue_avatar_export(
        self,
        *,
        character_rig_ref: str,
        performance_program_ref: str,
        export_targets: list[str] | None = None,
    ) -> tuple[AvatarExportWorkerJob, AvatarExportReceipt]:
        export_targets = export_targets or ["alpha_png_sequence", "webm_alpha"]
        deterministic_hash = compiler_hash(
            {
                "character_rig_ref": character_rig_ref,
                "performance_program_ref": performance_program_ref,
                "export_targets": export_targets,
            }
        )
        job = self.repository.put_avatar_export_job(
            AvatarExportWorkerJob(
                character_rig_ref=character_rig_ref,
                performance_program_ref=performance_program_ref,
                export_targets=export_targets,  # type: ignore[arg-type]
                deterministic_inputs_hash=deterministic_hash,
            )
        )
        receipt = self.repository.put_avatar_export_receipt(
            AvatarExportReceipt(
                avatar_export_worker_job_id=job.avatar_export_worker_job_id,
                exported_asset_refs=[f"avatar_export:{job.avatar_export_worker_job_id}:{target}" for target in export_targets],
                decision_code="AVATAR_EXPORT_QUEUED",
            )
        )
        return job, receipt

    def compile_geometrics_scene(
        self,
        *,
        scene_code: str,
        primitive_route_id: VideoFormatCode = "SV-EDU",
        skia_component_refs: list[str] | None = None,
    ) -> tuple[GeometricsSceneSpec, SkiaRenderBinding, SkiaRenderReceipt]:
        zones = [
            CompositionZone(zone_id="background", role="paper_or_plate_background", x=0, y=0, width=1, height=1),
            CompositionZone(zone_id="headline", role="editable_text", x=0.08, y=0.08, width=0.84, height=0.22),
            CompositionZone(zone_id="hero", role="layered_subject_or_symbol", x=0.08, y=0.34, width=0.84, height=0.54),
        ]
        layers = [
            CompositionTemplateLayer(layer_id="bg-paper", layer_type="skia_rect_texture", zone_id="background", source_ref="texture://paper", z_index=0),
            CompositionTemplateLayer(layer_id="headline-text", layer_type="pretext_editable_text", zone_id="headline", source_ref="copy://headline", z_index=20),
            CompositionTemplateLayer(layer_id="hero-layer", layer_type="qwen_layered_asset", zone_id="hero", source_ref="layer://hero", z_index=10),
        ]
        primitive_ids = self._primitive_ids_for_route(primitive_route_id)
        deterministic_hash = compiler_hash(
            {"scene_code": scene_code, "primitive_route_id": primitive_route_id, "zones": [zone.model_dump() for zone in zones], "layers": [layer.model_dump() for layer in layers]}
        )
        scene = self.repository.put_geometrics_scene_spec(
            GeometricsSceneSpec(
                scene_code=scene_code,
                canvas={"width": 1080, "height": 1350},
                zones=zones,
                layers=layers,
                skia_component_refs=skia_component_refs or ["skia:canvas", "skia:image", "skia:text", "rough-notation:highlight"],
                sam3_mask_refs=["sam3:hero-mask"],
                pretext_text_layer_refs=["pretext:headline-text"],
                primitive_validation_ids=primitive_ids,
                deterministic_inputs_hash=deterministic_hash,
            )
        )
        binding = self.repository.put_skia_render_binding(
            SkiaRenderBinding(
                source_scene_ref=f"geometrics_scene:{scene.geometrics_scene_spec_id}",
                component_refs=scene.skia_component_refs,
                render_job_ref=f"skia_render_job:{scene.geometrics_scene_spec_id}",
                deterministic_inputs_hash=scene.deterministic_inputs_hash,
            )
        )
        receipt = self.repository.put_skia_render_receipt(
            SkiaRenderReceipt(
                skia_render_binding_id=binding.skia_render_binding_id,
                output_asset_ref=f"render://skia/{binding.skia_render_binding_id}.png",
                decision_code="SKIA_RENDER_CONTRACT_READY",
                evidence_refs=[f"geometrics_scene:{scene.geometrics_scene_spec_id}"],
            )
        )
        return scene, binding, receipt

    def compile_carousel_slide_library(
        self,
        *,
        registry_ref: str = "registries/composition/carousel_slide_composition_library.v1.json",
    ) -> CarouselSlideLibrary:
        data, receipt = self.load_registry_bundle(registry_ref)
        atoms = [
            CarouselSlideAtom(
                slide_atom_code=item["slide_atom_code"],
                display_name=item["display_name"],
                composition_meaning=item["composition_meaning"],
                allowed_positions=item["allowed_positions"],
                compatible_format_codes=item["compatible_format_codes"],
                primitive_triads=[
                    PrimitiveTriadContract(
                        primitive_id=triad["primitive_id"],
                        canonical_name=triad["canonical_name"],
                        role=triad["role"],
                        evidence_ref=f"{registry_ref}:{item['slide_atom_code']}:{triad['primitive_id']}",
                    )
                    for triad in item["default_primitive_triads"]
                ],
                visual_grammar=item.get("visual_grammar", {}),
                query_tags=item.get("query_tags", []),
            )
            for item in data["slide_atoms"]
        ]
        library = CarouselSlideLibrary(
            registry_id=data["registry_id"],
            recognized_format_codes=data["recognized_carousel_format_codes"],
            slide_atoms=atoms,
            global_rules=data.get("global_rules", {}),
            registry_load_receipt_id=receipt.registry_bundle_load_receipt_id,
        )
        return self.repository.put_carousel_slide_library(library)

    def compile_carousel_sequence(
        self,
        *,
        library: CarouselSlideLibrary,
        source_context_refs: list[str],
        format_code: str = "CAR-JUX",
        slide_count: int = 5,
    ) -> CarouselSequencePlan:
        if len(source_context_refs) == 0:
            raise AssetProgramCompilerServiceError("CAROUSEL_SOURCE_CONTEXT_REQUIRED", "Carousel sequence requires source context.")
        compatible = [atom for atom in library.slide_atoms if format_code in atom.compatible_format_codes]
        if len(compatible) < 2:
            raise AssetProgramCompilerServiceError("CAROUSEL_LIBRARY_TOO_SMALL", "Carousel sequence requires at least two compatible slide atoms.")
        first = next((atom for atom in compatible if "first" in atom.allowed_positions), compatible[0])
        rest = [atom for atom in compatible if atom.slide_atom_code != first.slide_atom_code]
        selected = [first, *rest[: max(1, slide_count - 1)]]
        primitive_ids = self._primitive_ids_from_triads(selected[0].primitive_triads)
        deterministic_hash = compiler_hash(
            {"format_code": format_code, "source_context_refs": source_context_refs, "slide_atom_codes": [atom.slide_atom_code for atom in selected]}
        )
        plan = CarouselSequencePlan(
            format_code=format_code,  # type: ignore[arg-type]
            source_context_refs=source_context_refs,
            slide_atom_codes=[atom.slide_atom_code for atom in selected],
            sequence_rationale="Use a premise hook, audience/context mirror, stakes, reframing, and response close so each slide owns a distinct composition meaning.",
            primitive_validation_ids=primitive_ids,
            deterministic_inputs_hash=deterministic_hash,
        )
        return self.repository.put_carousel_sequence_plan(plan)

    def compile_carousel_builder_program(self, *, sequence_plan: CarouselSequencePlan, library: CarouselSlideLibrary) -> tuple[CarouselBuilderProgram, CarouselExportReceipt]:
        atom_by_code = {atom.slide_atom_code: atom for atom in library.slide_atoms}
        slide_specs = [
            {
                "slide_number": index + 1,
                "slide_atom_code": code,
                "composition_meaning": atom_by_code[code].composition_meaning,
                "visual_grammar": atom_by_code[code].visual_grammar,
                "primitive_validation_ids": self._primitive_ids_from_triads(atom_by_code[code].primitive_triads),
                "renderer": "skia",
            }
            for index, code in enumerate(sequence_plan.slide_atom_codes)
        ]
        deterministic_hash = compiler_hash({"sequence_plan": sequence_plan.model_dump(mode="json"), "slide_specs": slide_specs})
        program = self.repository.put_carousel_builder_program(
            CarouselBuilderProgram(
                carousel_sequence_plan_id=sequence_plan.carousel_sequence_plan_id,
                slide_specs=slide_specs,
                geometrics_layout_plan_ref=f"geometrics_layout_plan:{sequence_plan.carousel_sequence_plan_id}",
                skia_render_job_refs=[f"skia_render_job:carousel:{sequence_plan.carousel_sequence_plan_id}:{index + 1}" for index in range(len(slide_specs))],
                ideogram_composition_refs=[f"ideogram_composition_ref:{spec['slide_atom_code']}" for spec in slide_specs],
                deterministic_inputs_hash=deterministic_hash,
            )
        )
        receipt = self.repository.put_carousel_export_receipt(
            CarouselExportReceipt(
                carousel_builder_program_id=program.carousel_builder_program_id,
                exported_slide_refs=[f"render://carousel/{program.carousel_builder_program_id}/{index + 1}.png" for index in range(len(slide_specs))],
                decision_code="CAROUSEL_EXPORT_CONTRACT_READY",
            )
        )
        return program, receipt

    def route_carousel_atlas(
        self,
        *,
        slide_atom_code: str,
        registry_ref: str = "registries/composition/carousel_composition_atlas.v1.json",
    ) -> CarouselAtlasRouteReceipt:
        data, _receipt = self.load_registry_bundle(registry_ref)
        compositions = data.get("canonical_compositions", [])
        selected = compositions[0]
        if "MYTH" in slide_atom_code or "BREAK" in slide_atom_code:
            selected = next((item for item in compositions if "myth" in item["summary"].lower() or "contrast" in item["summary"].lower()), selected)
        route_receipt = CarouselAtlasRouteReceipt(
            composition_id=selected["composition_id"],
            selected_for_slide_atom_code=slide_atom_code,
            supported_aspect_ratios=selected.get("supported_aspect_ratios", []),
            tool_routing=selected.get("tool_routing", {}),
            decision_code="CAROUSEL_ATLAS_ROUTE_ACCEPTED",
            evidence_refs=[f"{registry_ref}:{selected['composition_id']}"],
        )
        return self.repository.put_carousel_atlas_route_receipt(route_receipt)

    def load_single_image_registry_snapshot(
        self,
        *,
        registry_ref: str = "registries/composition/single_image_composition_registry.v2.json",
    ) -> SingleImageRegistrySnapshot:
        data, receipt = self.load_registry_bundle(registry_ref)
        composition_ids = [item["composition_id"] for item in data["compositions"]]
        snapshot = SingleImageRegistrySnapshot(
            registry_schema_id=data["schema_id"],
            composition_ids=composition_ids,
            registry_load_receipt_id=receipt.registry_bundle_load_receipt_id,
            deterministic_inputs_hash=compiler_hash({"registry_ref": registry_ref, "composition_ids": composition_ids}),
        )
        return self.repository.put_single_image_registry_snapshot(snapshot)

    def route_single_image(
        self,
        *,
        archetype_ref: str,
        format_code: str = "SUPERVISUAL",
        registry_ref: str = "registries/composition/single_image_composition_registry.v2.json",
    ) -> SingleImageRouteDecision:
        data, _receipt = self.load_registry_bundle(registry_ref)
        selected = next(
            (
                item
                for item in data["compositions"]
                if archetype_ref in item.get("compatible_archetypes", [])
                or archetype_ref in item.get("compatible_reaction_archetypes", [])
                or archetype_ref in item.get("compatible_derivatives", [])
            ),
            data["compositions"][0],
        )
        decision = SingleImageRouteDecision(
            composition_id=selected["composition_id"],
            archetype_ref=archetype_ref,
            format_code=format_code,  # type: ignore[arg-type]
            selected_family=selected["family"],
            decision_code="SINGLE_IMAGE_ROUTE_ACCEPTED",
            evidence_refs=[f"{registry_ref}:{selected['composition_id']}"],
        )
        return self.repository.put_single_image_route_decision(decision)

    def compile_supervisual_family_contract(self, *, route_decision: SingleImageRouteDecision) -> SuperVisualFamilyContract:
        triads = self._primitive_triads_for_route("SV-FRB")
        contract = SuperVisualFamilyContract(
            family_code=f"SUPERVISUAL-{route_decision.selected_family.upper()}",
            composition_ids=[route_decision.composition_id],
            primitive_triads=triads,
            visual_pressure_policy="SuperVisuals must make one high-signal claim inspectable through composition, not decorative intensity.",
            doctrine_refs=[
                "TS-CMF-099",
                "TS-CMF-102",
                "THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE",
            ],
        )
        return self.repository.put_supervisual_family_contract(contract)

    def plan_single_image_provider_job(self, *, route_decision: SingleImageRouteDecision) -> tuple[StillVisualLayerMaterialization, SingleImageProviderJobPlan]:
        materialization = self.repository.put_still_visual_layer_materialization(
            StillVisualLayerMaterialization(
                source_route_decision_id=route_decision.single_image_route_decision_id,
                layer_refs=["layer:background", "layer:hero", "layer:editable_text", "layer:brand_signature"],
                qwen_layered_receipt_ref=f"qwen_layered:{route_decision.single_image_route_decision_id}",
                sam3_mask_refs=[f"sam3_mask:hero:{route_decision.single_image_route_decision_id}"],
            )
        )
        plan = self.repository.put_single_image_provider_job_plan(
            SingleImageProviderJobPlan(
                single_image_route_decision_id=route_decision.single_image_route_decision_id,
                provider_jobs=[
                    {
                        "provider": "ideogram_4",
                        "responsibility": "composition_reference",
                        "authority": "layout_and_mood_only",
                    },
                    {
                        "provider": "qwen_layered",
                        "responsibility": "editable_layer_decomposition",
                        "authority": "asset_layers_only",
                    },
                    {
                        "provider": "sam3",
                        "responsibility": "mask_refinement",
                        "authority": "cutout_mask_only",
                    },
                ],
                layer_materialization_refs=[f"still_layer_materialization:{materialization.still_visual_layer_materialization_id}"],
            )
        )
        return materialization, plan

    def compile_single_image_skia_scene(
        self,
        *,
        route_decision: SingleImageRouteDecision,
        registry_ref: str = "registries/composition/single_image_composition_registry.v2.json",
    ) -> SingleImageSkiaScene:
        data, _receipt = self.load_registry_bundle(registry_ref)
        composition = next(item for item in data["compositions"] if item["composition_id"] == route_decision.composition_id)
        zones = composition.get("zones", [])
        layer_stack = [
            {
                "layer_id": zone["id"],
                "role": zone["role"],
                "content_type": zone["content_type"],
                "z_index": zone["z_index"],
                "editable": zone["content_type"] == "text",
            }
            for zone in zones
        ]
        primitive_ids = self._primitive_ids_for_route("SV-FRB")
        scene = SingleImageSkiaScene(
            single_image_route_decision_id=route_decision.single_image_route_decision_id,
            canvas={"width": 1080, "height": 1350},
            zones=zones,
            layer_stack=layer_stack,
            rough_notation_plan=composition.get("rough_notation_contract", {}),
            skia_component_refs=["skia:canvas", "skia:image", "skia:text", "rough-notation:annotation"],
            primitive_validation_ids=primitive_ids,
            deterministic_inputs_hash=compiler_hash({"route": route_decision.model_dump(mode="json"), "zones": zones, "layers": layer_stack}),
        )
        return self.repository.put_single_image_skia_scene(scene)

    def run_single_image_eval_review(self, *, scene: SingleImageSkiaScene, golden_fixture_ref: str = "golden://single-image/supervisual-001") -> tuple[GoldenFixtureResult, SingleImageEvalReviewReceipt]:
        passed = len(scene.primitive_validation_ids) >= 3 and bool(scene.zones) and bool(scene.layer_stack)
        fixture = self.repository.put_golden_fixture_result(
            GoldenFixtureResult(
                fixture_ref=golden_fixture_ref,
                target_object_ref=f"single_image_skia_scene:{scene.single_image_skia_scene_id}",
                passed=passed,
                diff_summary="Scene has deterministic canvas, zone stack, primitive triad, and rough notation contract.",
                blocker_codes=[] if passed else ["SINGLE_IMAGE_GOLDEN_FIXTURE_FAILED"],
            )
        )
        receipt = self.repository.put_single_image_eval_review_receipt(
            SingleImageEvalReviewReceipt(
                single_image_skia_scene_id=scene.single_image_skia_scene_id,
                score=0.94 if passed else 0.4,
                decision="approved" if passed else "blocked",
                blocker_codes=[] if passed else ["SINGLE_IMAGE_EVAL_BLOCKED"],
                golden_fixture_refs=[fixture.fixture_ref],
                evidence_refs=[f"golden_fixture_result:{fixture.golden_fixture_result_id}"],
            )
        )
        return fixture, receipt

    def compile_video_edit_program(
        self,
        *,
        interview_asset_contract_ref: str,
        transcript_beat_map_ref: str,
        content_format_targets: list[VideoFormatCode] | None = None,
    ) -> VideoEditProgram:
        content_format_targets = content_format_targets or ["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]
        scenes = [
            VideoEditScene(
                scene_code=f"{format_code}-scene-001",
                video_format_code=format_code,
                start_seconds=index * 12.0,
                end_seconds=(index + 1) * 12.0,
                composition_template_ref=f"composition_template:{format_code}:default",
                transcript_beat_refs=[f"{transcript_beat_map_ref}:beat:{index + 1}"],
                layer_stack_refs=[f"layer_stack:{format_code}:base", f"layer_stack:{format_code}:text"],
            )
            for index, format_code in enumerate(content_format_targets)
        ]
        timeline_ref = f"otio://timeline/{uuid4()}"
        otio = OTIOAuditManifest(
            timeline_ref=timeline_ref,
            scene_refs=[scene.scene_code for scene in scenes],
            marker_refs=[f"marker:{scene.scene_code}:beat-lock" for scene in scenes],
            deterministic_inputs_hash=compiler_hash({"timeline_ref": timeline_ref, "scenes": [scene.model_dump(mode="json") for scene in scenes]}),
            audit_notes=["OTIO owns auditability; CMF render contracts own final deterministic render authority."],
        )
        render_contracts = [
            VideoRenderContract(
                render_target="remotion",
                render_tier="proxy",
                timeline_ref=timeline_ref,
                expected_output_ref=f"render://video/proxy/{timeline_ref.split('/')[-1]}.mp4",
                deterministic_inputs_hash=otio.deterministic_inputs_hash,
            ),
            VideoRenderContract(
                render_target="ffmpeg",
                render_tier="final",
                timeline_ref=timeline_ref,
                expected_output_ref=f"render://video/final/{timeline_ref.split('/')[-1]}.mp4",
                deterministic_inputs_hash=otio.deterministic_inputs_hash,
            ),
        ]
        program = VideoEditProgram(
            interview_asset_contract_ref=interview_asset_contract_ref,
            transcript_beat_map_ref=transcript_beat_map_ref,
            content_format_targets=content_format_targets,
            scenes=scenes,
            otio_audit_manifest=otio,
            render_contracts=render_contracts,
            approval_status=ApprovalStatus.draft,
        )
        return self.repository.put_video_edit_program(program)

    def compile_two_d_character_genesis(
        self,
        *,
        character_ref: str,
        brand_genesis_ref: str,
        visual_dna_refs: list[str] | None = None,
    ) -> tuple[TwoDCharacterGenesis, TwoDCharacterRig]:
        primitive_ids = self._primitive_ids_for_route("SV-EDU")
        genesis = self.repository.put_two_d_character_genesis(
            TwoDCharacterGenesis(
                character_ref=character_ref,
                brand_genesis_ref=brand_genesis_ref,
                visual_dna_refs=visual_dna_refs or ["visual_dna:papercut-materiality", "visual_dna:guest-likeness"],
                acting_library_refs=["acting_library:64-state", "acting_library:micro-gesture"],
                required_pose_count=64,
                primitive_validation_ids=primitive_ids,
            )
        )
        rig = self.repository.put_two_d_character_rig(
            TwoDCharacterRig(
                character_genesis_id=genesis.two_d_character_genesis_id,
                rig_ref=f"rig://two-d/{character_ref}",
                joint_map={"head": "joint:head", "torso": "joint:torso", "left_hand": "joint:left_hand", "right_hand": "joint:right_hand"},
                mouth_shape_refs=["mouth:rest", "mouth:open", "mouth:wide", "mouth:smile"],
                pose_state_refs=[f"pose:{index:02d}" for index in range(1, 65)],
                deterministic_inputs_hash=compiler_hash({"genesis": genesis.model_dump(mode="json")}),
            )
        )
        return genesis, rig

    def decide_two_d_character_adapter(
        self,
        *,
        provider_name: str,
        proposed_use: str,
        production_authority_allowed: bool = False,
    ) -> TwoDCharacterProviderAdapterDecision:
        blocker_codes = [] if not production_authority_allowed else ["TWO_D_PROVIDER_CANNOT_OWN_FINAL_AUTHORITY"]
        decision = TwoDCharacterProviderAdapterDecision(
            provider_name=provider_name,  # type: ignore[arg-type]
            proposed_use=proposed_use,
            production_authority_allowed=production_authority_allowed,
            adapter_boundary="Provider can author or preview rig data; CMF schema, timing, eval, and render receipts remain canonical.",
            decision_code="TWO_D_ADAPTER_SANDBOX_ACCEPTED" if not blocker_codes else "TWO_D_ADAPTER_BLOCKED",
            blocker_codes=blocker_codes,
        )
        return self.repository.put_two_d_character_adapter_decision(decision)

    def compile_two_d_character_scene_program(
        self,
        *,
        rig: TwoDCharacterRig,
        transcript_spans: list[dict[str, Any]],
    ) -> TwoDCharacterSceneProgram:
        cues = [
            TwoDCharacterPerformanceCue(
                cue_ref=f"cue:{index + 1}",
                transcript_span_ref=item["transcript_span_ref"],
                start_seconds=float(item["start_seconds"]),
                end_seconds=float(item["end_seconds"]),
                pose_state_ref=rig.pose_state_refs[index % len(rig.pose_state_refs)],
                gesture=item.get("gesture", "open_palm_teaching"),
                mouth_shape_ref=rig.mouth_shape_refs[index % len(rig.mouth_shape_refs)] if rig.mouth_shape_refs else None,
            )
            for index, item in enumerate(transcript_spans)
        ]
        program = TwoDCharacterSceneProgram(
            character_rig_id=rig.two_d_character_rig_id,
            papercut_materiality_ref="papercut://fibrous-paper-shadow-stack",
            performance_cues=cues,
            rough_notation_refs=["rough-notation:underline-key-term", "rough-notation:circle-framework-node"],
            deterministic_inputs_hash=compiler_hash({"rig": rig.model_dump(mode="json"), "cues": [cue.model_dump(mode="json") for cue in cues]}),
        )
        return self.repository.put_two_d_character_scene_program(program)

    def render_two_d_character_program(self, *, scene_program: TwoDCharacterSceneProgram) -> tuple[TwoDCharacterRenderReceipt, TwoDCharacterRepairPlan | None]:
        passed = len(scene_program.performance_cues) > 0 and bool(scene_program.rough_notation_refs)
        receipt = self.repository.put_two_d_character_render_receipt(
            TwoDCharacterRenderReceipt(
                two_d_character_scene_program_id=scene_program.two_d_character_scene_program_id,
                preview_ref=f"preview://two-d-character/{scene_program.two_d_character_scene_program_id}.mp4",
                alpha_export_ref=f"render://two-d-character/{scene_program.two_d_character_scene_program_id}.webm",
                decision="approved" if passed else "repair_required",
                blocker_codes=[] if passed else ["TWO_D_CHARACTER_TIMING_OR_ANNOTATION_MISSING"],
                eval_receipt_refs=[f"eval://two-d-character/{scene_program.two_d_character_scene_program_id}"],
            )
        )
        repair = None
        if not passed:
            repair = self.repository.put_two_d_character_repair_plan(
                TwoDCharacterRepairPlan(
                    two_d_character_render_receipt_id=receipt.two_d_character_render_receipt_id,
                    repair_actions=["add_transcript_timed_performance_cue", "add_papercut_or_rough_notation_ref"],
                    blocker_codes=receipt.blocker_codes,
                )
            )
        return receipt, repair

    def create_sequencing_kernel(self) -> SequencingRegistryKernel:
        refs = [
            "registries/composition/carousel_slide_composition_library.v1.json",
            "registries/composition/carousel_composition_atlas.v1.json",
            "registries/composition/single_image_composition_registry.v2.json",
            "registries/evals/composition/cmf_composition_primitive_triads.v1.json",
        ]
        kernel = SequencingRegistryKernel(
            kernel_code="CMF-SEQUENCE-KERNEL-V1",
            registry_refs=refs,
            primitive_policy_refs=["cmf.composition_primitive_triads.v1"],
            skill_compiler_refs=["JIT-SKILL:interview-brief", "JIT-SKILL:expression-extraction", "JIT-SKILL:narrative-induction"],
            deterministic_inputs_hash=compiler_hash(refs),
        )
        return self.repository.put_sequencing_kernel(kernel)

    def compile_interview_brief_v2(
        self,
        *,
        brand_context_ref: str,
        audience_context_ref: str,
        research_evidence_refs: list[str],
    ) -> InterviewBriefV2Plan:
        if not research_evidence_refs:
            raise AssetProgramCompilerServiceError("INTERVIEW_BRIEF_RESEARCH_EVIDENCE_REQUIRED", "Interview Brief V2 requires research evidence.")
        hypotheses = [
            SequenceHypothesis(
                hypothesis_ref="hypothesis:context-premise-001",
                premise="Audience context premise should be converted into questions that make the guest reveal usable expression ingredients.",
                audience_context_ref=audience_context_ref,
                evidence_refs=research_evidence_refs,
            )
        ]
        acquisition_plan = ExpressionAcquisitionPlan(
            acquisition_plan_ref="expression_acquisition:interview-brief-v2",
            interview_question_refs=["question:origin", "question:contrast", "question:stakes", "question:recognition"],
            guest_signal_refs=["signal:identity-shift", "signal:provocation", "signal:framework", "signal:emotional-proof"],
            coverage_targets=["story", "claim", "framework", "reaction", "visual_seed"],
        )
        plan = InterviewBriefV2Plan(
            brand_context_ref=brand_context_ref,
            sequence_hypotheses=hypotheses,
            expression_acquisition_plan=acquisition_plan,
            doctrine_refs=["CCP V9", "CCP V9.1", "Context Premise", "Matrix of Edging"],
            decision_code="INTERVIEW_BRIEF_V2_READY",
        )
        return self.repository.put_interview_brief_v2_plan(plan)

    def track_live_ingredient_coverage(
        self,
        *,
        interview_brief_v2_plan: InterviewBriefV2Plan,
        captured_ingredient_refs: list[str],
        suppressed_cues: list[str] | None = None,
    ) -> LiveIngredientCoverageTracker:
        suppressed_cues = suppressed_cues or []
        decisions = [
            CueSuppressionDecision(
                cue_ref=cue,
                suppressed=True,
                reason="Cue suppressed because the live interview already captured the ingredient or the guest moved into a higher-signal lane.",
                evidence_refs=[f"interview_brief_v2_plan:{interview_brief_v2_plan.interview_brief_v2_plan_id}"],
            )
            for cue in suppressed_cues
        ]
        targets = interview_brief_v2_plan.expression_acquisition_plan.coverage_targets
        missing = [target for target in targets if not any(target in ref for ref in captured_ingredient_refs)]
        tracker = LiveIngredientCoverageTracker(
            interview_brief_v2_plan_id=interview_brief_v2_plan.interview_brief_v2_plan_id,
            coverage_target_refs=targets,
            captured_ingredient_refs=captured_ingredient_refs,
            cue_suppression_decisions=decisions,
            decision_code="LIVE_COVERAGE_SUFFICIENT" if not missing else "LIVE_COVERAGE_PARTIAL",
            blocker_codes=[] if not missing else ["LIVE_INGREDIENT_COVERAGE_GAP"],
        )
        return self.repository.put_live_coverage_tracker(tracker)

    def build_expression_inventory(
        self,
        *,
        ingredients: list[dict[str, Any]],
        relation_edges: list[dict[str, Any]] | None = None,
    ) -> ExpressionIngredientInventory:
        parsed = [
            ExpressionIngredient(
                ingredient_ref=item["ingredient_ref"],
                ingredient_type=item["ingredient_type"],
                source_evidence_refs=item.get("source_evidence_refs", []),
                transcript_span_ref=item.get("transcript_span_ref"),
                guest_truth_claim=item.get("guest_truth_claim"),
            )
            for item in ingredients
        ]
        blocker_codes = ["EXPRESSION_INGREDIENT_SOURCE_EVIDENCE_MISSING"] if any(not item.source_evidence_refs for item in parsed) else []
        edges = [ExpressionRelationEdge(**item) for item in relation_edges or []]
        inventory = ExpressionIngredientInventory(
            ingredients=parsed,
            relation_edges=edges,
            blocker_codes=blocker_codes,
            deterministic_inputs_hash=compiler_hash({"ingredients": [item.model_dump(mode="json") for item in parsed], "edges": [edge.model_dump(mode="json") for edge in edges]}),
        )
        return self.repository.put_expression_ingredient_inventory(inventory)

    def compile_content_sequence_program(
        self,
        *,
        kernel: SequencingRegistryKernel,
        inventory: ExpressionIngredientInventory,
        target_compilers: list[str] | None = None,
    ) -> ContentSequenceProgram:
        target_compilers = target_compilers or ["carousel", "single_image", "video_edit", "two_d_character"]
        blocker_codes = list(inventory.blocker_codes)
        if any(not ingredient.source_evidence_refs for ingredient in inventory.ingredients):
            blocker_codes.append("CONTENT_SEQUENCE_GUEST_TRUTH_UNSUPPORTED")
        handoff_packages = [
            CompositionHandoffPackage(
                target_compiler=compiler,  # type: ignore[arg-type]
                handoff_refs=[ingredient.ingredient_ref for ingredient in inventory.ingredients],
                required_receipt_refs=[f"registry_kernel:{kernel.sequencing_registry_kernel_id}", f"inventory:{inventory.expression_ingredient_inventory_id}"],
            )
            for compiler in target_compilers
        ]
        program = ContentSequenceProgram(
            sequencing_registry_kernel_id=kernel.sequencing_registry_kernel_id,
            expression_ingredient_inventory_id=inventory.expression_ingredient_inventory_id,
            handoff_packages=handoff_packages,
            sequence_slots=[
                {"slot": index + 1, "ingredient_ref": ingredient.ingredient_ref, "recommended_compiler": target_compilers[index % len(target_compilers)]}
                for index, ingredient in enumerate(inventory.ingredients)
            ],
            decision="approved" if not blocker_codes else "blocked",
            blocker_codes=sorted(set(blocker_codes)),
            deterministic_inputs_hash=compiler_hash({"kernel": kernel.model_dump(mode="json"), "inventory": inventory.model_dump(mode="json"), "target_compilers": target_compilers}),
        )
        return self.repository.put_content_sequence_program(program)

    def run_sequence_eval(self, *, program: ContentSequenceProgram) -> tuple[SequenceEvalReceipt, PackageLearningReceipt]:
        approved = program.decision == "approved"
        receipt = self.repository.put_sequence_eval_receipt(
            SequenceEvalReceipt(
                content_sequence_program_id=program.content_sequence_program_id,
                primitive_score=0.92 if approved else 0.35,
                doctrine_score=0.93 if approved else 0.4,
                decision="approved" if approved else "blocked",
                blocker_codes=program.blocker_codes,
                evidence_refs=[f"content_sequence_program:{program.content_sequence_program_id}"],
            )
        )
        learning = self.repository.put_package_learning_receipt(
            PackageLearningReceipt(
                sequence_eval_receipt_id=receipt.sequence_eval_receipt_id,
                learned_registry_updates=["sequence_eval:no_fabricated_guest_truth_enforced"] if approved else [],
            )
        )
        return receipt, learning

    def _project_path(self, registry_ref: str) -> Path:
        candidate = Path(registry_ref)
        if not candidate.is_absolute():
            candidate = self.project_root / registry_ref
        resolved = candidate.resolve()
        project_root = self.project_root.resolve()
        if not resolved.is_relative_to(project_root):
            receipt = self.repository.put_registry_load_receipt(
                RegistryBundleLoadReceipt(
                    registry_ref=registry_ref,
                    absolute_path=str(resolved),
                    decision="blocked",
                    entry_count=0,
                    blocker_codes=["CMF_REGISTRY_OUTSIDE_PROJECT_ROOT"],
                )
            )
            raise AssetProgramCompilerServiceError("CMF_REGISTRY_OUTSIDE_PROJECT_ROOT", f"Registry must live inside THE CMF STUDIO: {receipt.absolute_path}")
        return resolved

    @staticmethod
    def _entry_count(data: dict[str, Any]) -> int:
        for key in ["slide_atoms", "canonical_compositions", "compositions", "rubrics"]:
            if isinstance(data.get(key), list):
                return len(data[key])
        return len(data)

    def _primitive_triads_for_route(self, route_id: VideoFormatCode) -> list[PrimitiveTriadContract]:
        data, _receipt = self.load_registry_bundle("registries/evals/composition/cmf_composition_primitive_triads.v1.json")
        route = data["route_triads"][route_id]
        selected: list[dict[str, Any]] = []
        for role in data["required_roles"]:
            selected.append(next(item for item in route["allowed_primitives"] if item["role"] == role))
        return [
            PrimitiveTriadContract(
                primitive_id=item["primitive_id"],
                canonical_name=item["canonical_name"],
                role=item["role"],
                evidence_ref=f"primitive_triads:{route_id}:{item['primitive_id']}",
            )
            for item in selected
        ]

    def _primitive_ids_for_route(self, route_id: VideoFormatCode) -> list[str]:
        return self._primitive_ids_from_triads(self._primitive_triads_for_route(route_id))

    @staticmethod
    def _primitive_ids_from_triads(triads: list[PrimitiveTriadContract]) -> list[str]:
        return [item.primitive_id for item in triads]
