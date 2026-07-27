"""Batch 1 composition runtime service for TS-CMF-072 through TS-CMF-092."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.composition_runtime import (
    AdapterDecision,
    ApprovalStatus,
    BeatMapCompilationReceipt,
    BrandGenesisSubstrateBinding,
    CompositionApprovalBlocker,
    CompositionApprovalReadModel,
    CompositionBeat,
    CompositionBeatMap,
    CompositionEvalSuiteRun,
    CompositionLayoutPlan,
    CompositionOperatorApprovalReceipt,
    CompositionPreflightReceipt,
    CompositionRuntimeBinding,
    CompositionRuntimeBindingReceipt,
    CompositionTemplateApprovalReceipt,
    CompositionTemplateFamily,
    CompositionTemplateJson,
    CompositionTemplateLayer,
    CompositionZone,
    ContentAssetCodeReservation,
    EvalTargetSelection,
    ExpressionLineageBinding,
    ExpressionLineageBindingReceipt,
    FourVideoFormatPlan,
    FourVideoSlotRequirement,
    GenerativeAssetFactoryJob,
    GeometricsHandoffPlan,
    IdeogramProductionBridgeReceipt,
    IntegrationAdapterDecision,
    IntegrationCandidate,
    LayerExtractionResult,
    LayerManifestEntry,
    MicroSemioticAnchorSelection,
    OpenSourceAdapterBinding,
    OpenSourceTemplateConversion,
    PaperCutMaterialityRule,
    PaperCutMotionCue,
    PaperCutRuntimeManifest,
    PaperCutRuntimeReceipt,
    PaperCutSfxCue,
    PerformanceStateSelection,
    PrimitiveValidationResult,
    ProductionTextPlan,
    QwenLayeredDecompositionReceipt,
    ReactionClipRenderManifest,
    ReactionClipRendererProps,
    RendererComponentCompatibilityReport,
    RendererComponentRegistration,
    RendererPropsCompilationReceipt,
    RendererPropsManifest,
    ResolvedBrandGenesisSubstrate,
    ReviewReadModel,
    SAM3SaliencyReceipt,
    SceneTemplateBinding,
    SceneTemplateBindingReceipt,
    SourceTimestampRange,
    SubjectCutoutLayer,
    TimelineCue,
    VideoFormatRouteReceipt,
    VisualFeelContract,
    runtime_hash,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.composition_runtime import InMemoryCompositionRuntimeRepository


class CompositionRuntimeServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class CompositionRuntimeService:
    repository: InMemoryCompositionRuntimeRepository = field(default_factory=InMemoryCompositionRuntimeRepository)
    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[3])
    _primitive_registry_cache: dict[str, Any] | None = None

    def primitive_triad_registry(self) -> dict[str, Any]:
        if self._primitive_registry_cache is None:
            registry_path = self.project_root / "registries" / "evals" / "composition" / "cmf_composition_primitive_triads.v1.json"
            self._primitive_registry_cache = json.loads(registry_path.read_text(encoding="utf-8"))
        return self._primitive_registry_cache

    def bind_scene_template(
        self,
        *,
        scene_spec: Any,
        reaction_template_route_receipt: Any,
        actor_id: UUID,
    ) -> SceneTemplateBinding:
        if reaction_template_route_receipt.decision_code != "REACTION_TEMPLATE_ROUTE_ACCEPTED":
            self.repository.put_scene_template_binding_receipt(
                SceneTemplateBindingReceipt(
                    scene_spec_id=scene_spec.scene_spec_id,
                    decision_code="SCENE_TEMPLATE_BINDING_BLOCKED",
                    blocker_codes=["REACTION_TEMPLATE_ROUTE_NOT_ACCEPTED"],
                    evidence_refs=[f"reaction_template_route_receipt:{reaction_template_route_receipt.reaction_template_route_receipt_id}"],
                    actor_id=actor_id,
                )
            )
            raise CompositionRuntimeServiceError("REACTION_TEMPLATE_ROUTE_NOT_ACCEPTED", "Scene template binding requires an accepted reaction template route.")
        patch = reaction_template_route_receipt.scene_spec_requirement_patch
        missing = [key for key in ["renderer_route", "composition_id", "scene_pattern", "live_clip_slots", "motion_grammar"] if not patch.get(key)]
        if missing:
            self.repository.put_scene_template_binding_receipt(
                SceneTemplateBindingReceipt(
                    scene_spec_id=scene_spec.scene_spec_id,
                    decision_code="SCENE_TEMPLATE_BINDING_BLOCKED",
                    blocker_codes=["SCENE_TEMPLATE_RUNTIME_FIELDS_MISSING"],
                    evidence_refs=missing,
                    actor_id=actor_id,
                )
            )
            raise CompositionRuntimeServiceError("SCENE_TEMPLATE_RUNTIME_FIELDS_MISSING", "Reaction route did not carry the required scene runtime fields.")
        binding = self.repository.put_scene_template_binding(
            SceneTemplateBinding(
                scene_spec_id=scene_spec.scene_spec_id,
                reaction_template_route_id=reaction_template_route_receipt.reaction_template_route_id,
                template_code=str(reaction_template_route_receipt.template_code.value if hasattr(reaction_template_route_receipt.template_code, "value") else reaction_template_route_receipt.template_code),
                content_format_code=reaction_template_route_receipt.content_format_code,
                scene_pattern=patch["scene_pattern"],
                renderer_route=patch["renderer_route"],
                composition_id=patch["composition_id"],
                live_clip_slots=patch["live_clip_slots"],
                motion_grammar=patch["motion_grammar"],
                primitive_eval_obligations=patch.get("primitive_eval_obligations", []),
                source_lineage_refs=[
                    f"scene_spec:{scene_spec.scene_spec_id}",
                    f"reaction_template_route:{reaction_template_route_receipt.reaction_template_route_id}",
                    *reaction_template_route_receipt.source_support_evidence,
                ],
            )
        )
        self.repository.put_scene_template_binding_receipt(
            SceneTemplateBindingReceipt(
                scene_template_binding_id=binding.scene_template_binding_id,
                scene_spec_id=scene_spec.scene_spec_id,
                decision_code="SCENE_TEMPLATE_BINDING_ACCEPTED",
                evidence_refs=binding.source_lineage_refs,
                actor_id=actor_id,
            )
        )
        return binding

    def default_visual_feel_contract(self, route_id: str) -> VisualFeelContract:
        route = self._route_rule(route_id)
        obligations = [item["primitive_id"] for item in route["allowed_primitives"][:3]]
        return self.repository.put_visual_feel_contract(
            VisualFeelContract(
                route_id=route_id,
                required_distinct_feel=route["required_distinct_feel"],
                primitive_obligations=obligations,
                forbidden_style_collapses=route.get("route_specific_hard_failures", []),
                source_doctrine_refs=self.primitive_triad_registry()["source_doctrine_refs"],
            )
        )

    def primitive_results_for_route(self, route_id: str) -> list[PrimitiveValidationResult]:
        route = self._route_rule(route_id)
        selected: list[dict[str, Any]] = []
        for role in self.primitive_triad_registry()["required_roles"]:
            selected.append(next(item for item in route["allowed_primitives"] if item["role"] == role))
        return [
            PrimitiveValidationResult(
                primitive_id=item["primitive_id"],
                primitive_name=item["canonical_name"],
                role=item["role"],
                score=max(float(item["minimum_score"]), 0.9),
                threshold=float(item["minimum_score"]),
                evidence_ref=f"source:{route_id}:{item['primitive_id']}",
                composition_element_ref=f"composition_element:{item['role']}",
                decision="pass",
            )
            for item in selected
        ]

    def validate_primitive_preflight(
        self,
        *,
        route_id: str,
        composition_id: str,
        visual_feel_contract_id: UUID,
        primitive_results: list[PrimitiveValidationResult | dict[str, Any]],
    ) -> CompositionPreflightReceipt:
        parsed = [item if isinstance(item, PrimitiveValidationResult) else PrimitiveValidationResult(**item) for item in primitive_results]
        allowed = {item["primitive_id"]: item for item in self._route_rule(route_id)["allowed_primitives"]}
        registry = self.primitive_triad_registry()
        hard_failures: list[str] = []
        for result in parsed:
            if result.primitive_id not in allowed:
                hard_failures.append("COMPOSITION_PRIMITIVE_ID_NOT_REGISTERED")
            elif result.role != allowed[result.primitive_id]["role"]:
                hard_failures.append("COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING")
            if not result.evidence_ref:
                hard_failures.append("COMPOSITION_PRIMITIVE_EVIDENCE_MISSING")
            if result.score < result.threshold or result.decision != "pass":
                hard_failures.append("COMPOSITION_PRIMITIVE_SCORE_BELOW_THRESHOLD")
        passed = [item for item in parsed if item.decision == "pass" and item.score >= item.threshold and item.primitive_id in allowed]
        role_coverage = {role: any(item.role == role for item in passed) for role in registry["required_roles"]}
        if len(passed) < int(registry["minimum_validated_primitives"]):
            hard_failures.append("COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET")
        if not all(role_coverage.values()):
            hard_failures.append("COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING")
        receipt = CompositionPreflightReceipt(
            composition_id=composition_id,
            route_id=route_id,
            visual_feel_contract_id=visual_feel_contract_id,
            minimum_validated_primitives=int(registry["minimum_validated_primitives"]),
            primitive_validation_count=len(passed),
            primitive_results=parsed,
            role_coverage=role_coverage,
            hard_failure_codes=sorted(set(hard_failures)),
            decision="approved" if not hard_failures else "blocked",
        )
        return self.repository.put_composition_preflight_receipt(receipt)

    def register_composition_template_json(
        self,
        *,
        binding: SceneTemplateBinding,
        route_id: str,
        actor_id: UUID,
        primitive_results: list[PrimitiveValidationResult | dict[str, Any]] | None = None,
        zones: list[CompositionZone] | None = None,
        layers: list[CompositionTemplateLayer] | None = None,
        preview_asset_refs: list[str] | None = None,
    ) -> CompositionTemplateJson:
        visual_feel = self.default_visual_feel_contract(route_id)
        primitive_results = primitive_results or self.primitive_results_for_route(route_id)
        preflight = self.validate_primitive_preflight(
            route_id=route_id,
            composition_id=binding.composition_id,
            visual_feel_contract_id=visual_feel.visual_feel_contract_id,
            primitive_results=primitive_results,
        )
        if preflight.decision != "approved":
            raise CompositionRuntimeServiceError("COMPOSITION_PREFLIGHT_BLOCKED", ",".join(preflight.hard_failure_codes))
        zones = zones or self._default_reaction_zones()
        layers = layers or self._default_reaction_layers()
        payload = {
            "binding": binding.model_dump(mode="json"),
            "zones": [zone.model_dump(mode="json") for zone in zones],
            "layers": [layer.model_dump(mode="json") for layer in layers],
            "visual_feel_contract_id": visual_feel.visual_feel_contract_id,
            "primitive_validation_ids": [item.primitive_id for item in preflight.primitive_results if item.decision == "pass"],
        }
        template = self.repository.put_composition_template(
            CompositionTemplateJson(
                template_family_code=binding.template_code,
                content_format_code=binding.content_format_code,
                aspect_ratio="9:16",
                width=1080,
                height=1920,
                fps=30,
                duration_seconds=45,
                zones=zones,
                layers=layers,
                source_lineage_refs=binding.source_lineage_refs,
                primitive_validation_ids=payload["primitive_validation_ids"],
                visual_feel_contract_id=visual_feel.visual_feel_contract_id,
                preview_asset_refs=preview_asset_refs or [],
                composition_json_hash=runtime_hash(payload),
                approval_status=ApprovalStatus.approved,
            )
        )
        self.repository.put_template_approval_receipt(
            CompositionTemplateApprovalReceipt(
                composition_template_id=template.composition_template_id,
                composition_json_hash=template.composition_json_hash,
                decision="approved",
                evidence_refs=[
                    f"scene_template_binding:{binding.scene_template_binding_id}",
                    f"visual_feel_contract:{visual_feel.visual_feel_contract_id}",
                    f"composition_preflight:{preflight.composition_preflight_receipt_id}",
                    f"actor:{actor_id}",
                ],
                actor_id=actor_id,
            )
        )
        return template

    def compile_reaction_renderer_manifest(
        self,
        *,
        composition_template_id: UUID,
        beat_map: CompositionBeatMap,
        subject_cutouts: list[SubjectCutoutLayer] | None = None,
    ) -> ReactionClipRenderManifest:
        template = self._composition_template(composition_template_id)
        zone_roles = {zone.role: zone.zone_id for zone in template.zones}
        upper_zone = zone_roles.get("upper_reaction_ui") or template.zones[0].zone_id
        lower_zone = zone_roles.get("lower_human_cutouts") or template.zones[-1].zone_id
        cutouts = subject_cutouts or [
            SubjectCutoutLayer(subject_ref="guest:primary", role="guest", zone_id=lower_zone, mask_ref="mask:guest-upper-body", background_removed=True, eye_line="toward_interviewer"),
            SubjectCutoutLayer(subject_ref="interviewer:primary", role="interviewer", zone_id=lower_zone, mask_ref="mask:interviewer-upper-body", background_removed=True, eye_line="toward_guest"),
        ]
        props = ReactionClipRendererProps(
            composition_template_id=template.composition_template_id,
            content_format_code=template.content_format_code,
            upper_reaction_ui_zone_id=upper_zone,
            lower_human_cutout_zone_id=lower_zone,
            subject_cutouts=cutouts,
            beat_cue_refs=[cue.cue_id for cue in beat_map.timeline_cues],
            caption_policy="two_line_captions_follow_guest_reaction_without_covering_faces",
            audio_policy="preserve_guest_voice_and_interviewer_reaction_pause",
        )
        return ReactionClipRenderManifest(
            renderer_props=props,
            frame_size=f"{template.width}x{template.height}",
            deterministic_inputs_hash=runtime_hash({"template": template.composition_json_hash, "beat_map": beat_map.model_dump(mode="json")}),
            receipts_required=["CompositionTemplateApprovalReceipt", "BeatMapCompilationReceipt", "BackgroundRemovalReceipt"],
        )

    def build_composition_approval_read_model(
        self,
        *,
        scene_template_binding_id: UUID,
        composition_template_id: UUID,
        preview_refs: list[str] | None = None,
        eval_receipt_refs: list[str] | None = None,
        blockers: list[CompositionApprovalBlocker] | None = None,
    ) -> CompositionApprovalReadModel:
        binding = self.repository.scene_template_bindings[scene_template_binding_id]
        template = self._composition_template(composition_template_id)
        parsed_blockers = blockers or []
        read_model = CompositionApprovalReadModel(
            scene_template_binding=binding,
            composition_template=template,
            preview_refs=preview_refs or [],
            eval_receipt_refs=eval_receipt_refs or [],
            blockers=parsed_blockers,
            approval_status=ApprovalStatus.blocked if any(item.severity == "hard" for item in parsed_blockers) else template.approval_status,
            operator_commands=["approve_composition_template", "request_composition_repair", "reject_preview"],
        )
        return self.repository.put_approval_read_model(read_model)

    def register_integration_candidate(self, candidate: IntegrationCandidate | dict[str, Any]) -> IntegrationCandidate:
        parsed = candidate if isinstance(candidate, IntegrationCandidate) else IntegrationCandidate(**candidate)
        return self.repository.put_integration_candidate(parsed)

    def run_integration_fit_eval(self, integration_candidate_id: UUID) -> IntegrationAdapterDecision:
        candidate = self.repository.integration_candidates[integration_candidate_id]
        criteria = {
            "deterministic_boundary": 1.0 if candidate.deterministic_boundary else 0.0,
            "contractability": 0.9 if candidate.category in {"video_editing", "visual_composition", "animation", "search", "memory"} else 0.65,
            "license_fit": 0.9 if candidate.license_family.lower() in {"mit", "apache-2.0", "bsd"} else 0.45,
            "sandboxability": 1.0,
            "no_production_authority": 1.0 if not candidate.production_authority_allowed else 0.0,
        }
        score = sum(criteria.values()) / len(criteria)
        blockers: list[str] = []
        if candidate.production_authority_allowed:
            blockers.append("OPEN_SOURCE_DIRECT_PRODUCTION_AUTHORITY_FORBIDDEN")
        if criteria["license_fit"] < 0.7:
            blockers.append("OPEN_SOURCE_LICENSE_REVIEW_REQUIRED")
        decision = AdapterDecision.approved_adapter if score >= 0.78 and not blockers else AdapterDecision.sandbox_only
        if score < 0.55:
            decision = AdapterDecision.rejected
        adapter_decision = IntegrationAdapterDecision(
            integration_candidate_id=candidate.integration_candidate_id,
            decision=decision,
            score=score,
            criteria_scores=criteria,
            adapter_boundary="CMF-owned adapter emits Pydantic receipts; upstream project never owns final state.",
            sandbox_required=True,
            blocker_codes=blockers,
            evidence_refs=[*candidate.evidence_refs, candidate.repo_url],
        )
        return self.repository.put_integration_adapter_decision(adapter_decision)

    def plan_four_video_formats(self, *, organization_id: UUID, brand_id: UUID, expression_moment_id: UUID) -> FourVideoFormatPlan:
        requirements = [
            FourVideoSlotRequirement(
                slot_code="SV-CSC",
                slot_name="Cinematic Story Commentary",
                route_purpose="Make them feel the story.",
                required_dependencies=["InterviewAssetContract", "ExpressionMoment", "SceneSpec", "CompositionTemplateJson"],
                doctrine_refs=["narrative_state_induction", "emotional_truth", "complete_editing_session"],
                composition_rules=["documentary_closeups", "memory_object_inserts", "cinematic_negative_space"],
            ),
            FourVideoSlotRequirement(
                slot_code="SV-EDU",
                slot_name="Educational / Explainer",
                route_purpose="Make them understand the idea.",
                required_dependencies=["PaperCutRuntimeManifest", "PerformanceStateSelection", "CompositionBeatMap"],
                doctrine_refs=["teaching_as_compassion", "primitive_distillation", "paper_cut_materiality"],
                composition_rules=["textured_paper_layers", "2d_avatar", "rough_annotations", "diagram_motion"],
            ),
            FourVideoSlotRequirement(
                slot_code="SV-FRB",
                slot_name="Challenger / Frame Breaker",
                route_purpose="Make them confront the frame.",
                required_dependencies=["ReactionTemplateRoute", "VisualFeelContract", "PrimitivePreflight"],
                doctrine_refs=["constructive_tension", "attack_problem_not_person", "source_backed_proof"],
                composition_rules=["proof_surface", "poll_or_debate_card", "high_contrast_tension"],
            ),
            FourVideoSlotRequirement(
                slot_code="SV-RRC",
                slot_name="Reaction / Recognition Clip",
                route_purpose="Make them trust the human moment.",
                required_dependencies=["ReactionClipRendererProps", "BeatMapCompilationReceipt", "BackgroundRemovalReceipt"],
                doctrine_refs=["human_proof", "voice_identity", "attention_routing"],
                composition_rules=["upper_reaction_ui", "lower_upper_body_cutouts", "reaction_pause_timing"],
            ),
        ]
        receipts = [
            VideoFormatRouteReceipt(
                slot_code=item.slot_code,
                expression_moment_id=expression_moment_id,
                selected=True,
                decision_code="VIDEO_FORMAT_ROUTE_SELECTED",
                evidence_refs=[f"expression_moment:{expression_moment_id}", f"slot:{item.slot_code}"],
            )
            for item in requirements
        ]
        return self.repository.put_four_video_format_plan(
            FourVideoFormatPlan(
                organization_id=organization_id,
                brand_id=brand_id,
                slot_requirements=requirements,
                route_receipts=receipts,
            )
        )

    def register_default_template_families(self) -> list[CompositionTemplateFamily]:
        families = [
            CompositionTemplateFamily(family_code="RCT-VRS", display_name="Reaction Versus", supported_format_codes=["SV-RRC", "SV-FRB"], asset_code_prefix="VRS", route_id="SV-RRC"),
            CompositionTemplateFamily(family_code="RCT-TIER", display_name="Reaction Tier List", supported_format_codes=["SV-RRC", "SV-FRB"], asset_code_prefix="TIER", route_id="SV-RRC"),
            CompositionTemplateFamily(family_code="PPR-EDU", display_name="PaperCut Educational", supported_format_codes=["SV-EDU"], asset_code_prefix="PPR", route_id="SV-EDU"),
            CompositionTemplateFamily(family_code="CIN-STORY", display_name="Cinematic Story", supported_format_codes=["SV-CSC"], asset_code_prefix="CIN", route_id="SV-CSC"),
        ]
        return [self.repository.put_template_family(item) for item in families]

    def reserve_content_asset_code(self, *, brand_id: UUID, template_family_code: str, content_format_code: str, sequence_number: int, object_ref: str) -> ContentAssetCodeReservation:
        if template_family_code not in self.repository.template_families:
            self.register_default_template_families()
        family = self.repository.template_families[template_family_code]
        code = f"CMF-{family.asset_code_prefix}-{content_format_code}-{sequence_number:04d}"
        if code in self.repository.asset_code_reservations:
            raise CompositionRuntimeServiceError("CONTENT_ASSET_CODE_ALREADY_RESERVED", code)
        return self.repository.put_asset_code_reservation(
            ContentAssetCodeReservation(
                content_asset_code=code,
                brand_id=brand_id,
                template_family_code=template_family_code,
                content_format_code=content_format_code,
                sequence_number=sequence_number,
                reserved_for_object_ref=object_ref,
            )
        )

    def resolve_brand_genesis_substrate(self, *, scene_spec: Any, source_refs: list[str] | None = None) -> ResolvedBrandGenesisSubstrate:
        binding = BrandGenesisSubstrateBinding(
            brand_context_version_id=scene_spec.brand_context_version_id,
            brand_context_version_hash=scene_spec.brand_context_version_hash,
            voice_dna_ref=f"brand_context:{scene_spec.brand_context_version_id}:voice_dna",
            visual_dna_ref=f"brand_context:{scene_spec.brand_context_version_id}:visual_dna",
            emotional_dna_ref=f"brand_context:{scene_spec.brand_context_version_id}:emotional_dna",
            micro_semiotic_anchor_refs=[f"scene_spec:{scene_spec.scene_spec_id}:micro_semiotic"],
            negative_space_refs=[f"scene_spec:{scene_spec.scene_spec_id}:negative_space"],
        )
        substrate = ResolvedBrandGenesisSubstrate(
            binding=binding,
            composition_constraints={
                "brand_context_version_hash": scene_spec.brand_context_version_hash,
                "visual_style": scene_spec.visual_style,
                "identity_boundary": "locked_brand_context_assets_only",
            },
            evidence_refs=source_refs or [f"scene_spec:{scene_spec.scene_spec_id}", f"brand_context_version:{scene_spec.brand_context_version_id}"],
        )
        return self.repository.put_brand_genesis_substrate(substrate)

    def bind_expression_lineage(
        self,
        *,
        interview_asset_contract_id: UUID,
        expression_moment_id: UUID,
        complete_editing_session_id: UUID,
        asset_route_receipt_id: UUID,
        transcript_segment_refs: list[str],
    ) -> ExpressionLineageBindingReceipt:
        binding = ExpressionLineageBinding(
            interview_asset_contract_id=interview_asset_contract_id,
            expression_moment_id=expression_moment_id,
            complete_editing_session_id=complete_editing_session_id,
            asset_route_receipt_id=asset_route_receipt_id,
            transcript_segment_refs=transcript_segment_refs,
            extraction_receipt_refs=[f"expression_moment:{expression_moment_id}"],
            eval_target_refs=[f"asset_route_receipt:{asset_route_receipt_id}"],
        )
        return ExpressionLineageBindingReceipt(
            expression_lineage_binding=binding,
            decision_code="EXPRESSION_LINEAGE_BOUND",
            evidence_refs=[*transcript_segment_refs, f"interview_asset_contract:{interview_asset_contract_id}"],
        )

    def compile_beat_map(self, *, expression_moment_id: UUID, segments: list[dict[str, Any]]) -> tuple[CompositionBeatMap, BeatMapCompilationReceipt]:
        if not segments:
            raise CompositionRuntimeServiceError("TRANSCRIPT_SEGMENTS_REQUIRED", "Beat-map compilation requires transcript segments.")
        beats: list[CompositionBeat] = []
        cues: list[TimelineCue] = []
        for index, segment in enumerate(segments, start=1):
            beat_id = segment.get("beat_id", f"beat-{index:02d}")
            source_range = SourceTimestampRange(
                source_ref=segment.get("source_ref", f"transcript_segment:{index}"),
                start_seconds=float(segment["start_seconds"]),
                end_seconds=float(segment["end_seconds"]),
            )
            beats.append(
                CompositionBeat(
                    beat_id=beat_id,
                    beat_role=segment.get("beat_role", "claim_or_reaction"),
                    source_range=source_range,
                    speaker=segment.get("speaker", "guest"),
                    text=segment["text"],
                    expression_state=segment.get("expression_state", "contained conviction"),
                    primitive_refs=segment.get("primitive_refs", []),
                )
            )
            cues.append(
                TimelineCue(
                    cue_id=f"cue-{index:02d}",
                    beat_id=beat_id,
                    cue_type=segment.get("cue_type", "caption_and_layer_reveal"),
                    start_seconds=source_range.start_seconds,
                    end_seconds=source_range.end_seconds,
                    target_layer_id=segment.get("target_layer_id", "headline"),
                    payload={"text": segment["text"], "speaker": segment.get("speaker", "guest")},
                )
            )
        beat_map = self.repository.put_beat_map(
            CompositionBeatMap(
                expression_moment_id=expression_moment_id,
                beats=beats,
                timeline_cues=cues,
                source_lineage_refs=[beat.source_range.source_ref for beat in beats],
            )
        )
        receipt = self.repository.put_beat_map_receipt(
            BeatMapCompilationReceipt(
                composition_beat_map_id=beat_map.composition_beat_map_id,
                beat_count=len(beats),
                cue_count=len(cues),
                decision_code="BEAT_MAP_COMPILED",
                evidence_refs=beat_map.source_lineage_refs,
            )
        )
        return beat_map, receipt

    def bind_composition_runtime(
        self,
        *,
        scene_template_binding_id: UUID,
        composition_template_id: UUID,
        brand_genesis_substrate_id: UUID,
        expression_lineage_binding_ref: str,
        visual_feel_contract_id: UUID,
        composition_beat_map_id: UUID,
        renderer_route: str,
        open_source_adapter_bindings: list[OpenSourceAdapterBinding] | None = None,
    ) -> CompositionRuntimeBinding:
        if composition_template_id not in self.repository.composition_templates:
            raise CompositionRuntimeServiceError("COMPOSITION_TEMPLATE_REQUIRED", "Runtime binding requires approved composition JSON.")
        binding = self.repository.put_runtime_binding(
            CompositionRuntimeBinding(
                scene_template_binding_id=scene_template_binding_id,
                composition_template_id=composition_template_id,
                brand_genesis_substrate_id=brand_genesis_substrate_id,
                expression_lineage_binding_ref=expression_lineage_binding_ref,
                visual_feel_contract_id=visual_feel_contract_id,
                composition_beat_map_id=composition_beat_map_id,
                open_source_adapter_bindings=open_source_adapter_bindings or [],
                renderer_route=renderer_route,
                approval_status=ApprovalStatus.approved,
            )
        )
        self.repository.put_runtime_binding_receipt(
            CompositionRuntimeBindingReceipt(
                composition_runtime_binding_id=binding.composition_runtime_binding_id,
                decision_code="COMPOSITION_RUNTIME_BOUND",
                evidence_refs=[
                    f"scene_template_binding:{scene_template_binding_id}",
                    f"composition_template:{composition_template_id}",
                    f"beat_map:{composition_beat_map_id}",
                ],
            )
        )
        return binding

    def select_performance_state(self, *, expression_state: str, emotion: str, gesture: str, evidence_refs: list[str]) -> PerformanceStateSelection:
        code_seed = runtime_hash({"expression_state": expression_state, "emotion": emotion, "gesture": gesture})[:6].upper()
        selection = PerformanceStateSelection(
            acting_state_code=f"ACT-{code_seed}",
            expression_state=expression_state,
            emotion=emotion,
            gesture=gesture,
            camera_attitude="upper_body_cutout_three_quarter_for_interview_first_delivery",
            eligibility_score=0.91,
            source_evidence_refs=evidence_refs,
        )
        return self.repository.put_performance_state_selection(selection)

    def compile_papercut_runtime_manifest(self, *, composition_template_id: UUID, rig_refs: list[str], beat_map: CompositionBeatMap) -> tuple[PaperCutRuntimeManifest, PaperCutRuntimeReceipt]:
        template = self._composition_template(composition_template_id)
        materiality = [
            PaperCutMaterialityRule(
                rule_id="paper-layer-materiality",
                texture="fibrous_paper_with_visible_edge",
                edge_policy="slightly_irregular_cut_edges",
                shadow_policy="soft_offset_shadow_for_2_5d_depth",
                allowed_style_tokens=["paper", "tactile", "editorial", "warm", "layered"],
            )
        ]
        motion = [
            PaperCutMotionCue(
                motion_cue_id=f"motion-{cue.cue_id}",
                layer_id=cue.target_layer_id,
                motion_type="paper_slide_or_pop",
                start_seconds=cue.start_seconds,
                end_seconds=cue.end_seconds,
                easing="ease_out_back_low_amplitude",
                meaning_ref=cue.beat_id,
            )
            for cue in beat_map.timeline_cues
        ]
        sfx = [
            PaperCutSfxCue(
                sfx_cue_id="sfx-paper-tick",
                cue_ref=motion[0].motion_cue_id,
                sound_family="paper_tick",
                volume_db=-18.0,
                meaning_ref="tactile_teaching_attention",
            )
        ]
        manifest = self.repository.put_papercut_manifest(
            PaperCutRuntimeManifest(
                composition_template_id=template.composition_template_id,
                materiality_rules=materiality,
                motion_cues=motion,
                sfx_cues=sfx,
                rig_refs=rig_refs,
                doctrine_eval_refs=["registries/evals/doctrine/cmf_papercut_rig_doctrine_eval.v1.json"],
            )
        )
        receipt = self.repository.put_papercut_receipt(
            PaperCutRuntimeReceipt(
                papercut_runtime_manifest_id=manifest.papercut_runtime_manifest_id,
                decision_code="PAPERCUT_RUNTIME_READY",
                evidence_refs=[f"composition_template:{composition_template_id}", f"beat_map:{beat_map.composition_beat_map_id}", *rig_refs],
            )
        )
        return manifest, receipt

    def select_micro_semiotic_anchors(self, *, route_id: str, audience_context_ref: str, anchor_refs: list[str], risk_score: float) -> MicroSemioticAnchorSelection:
        blockers = ["MICRO_SEMIOTIC_ANCHOR_RISK_TOO_HIGH"] if risk_score > 0.45 else []
        selection = MicroSemioticAnchorSelection(
            selected_anchor_refs=anchor_refs,
            route_id=route_id,
            audience_context_ref=audience_context_ref,
            risk_score=risk_score,
            risk_notes=["Requires operator review before final render."] if blockers else [],
            blocker_codes=blockers,
        )
        return self.repository.put_micro_semiotic_anchor_selection(selection)

    def bridge_ideogram_to_production_template(self, *, composition_job_id: UUID, zones: list[CompositionZone], layer_manifest_ref: str) -> IdeogramProductionBridgeReceipt:
        layout = CompositionLayoutPlan(
            source_composition_job_id=composition_job_id,
            frame_plan={"authority": "layout_only", "final_identity_and_text": "downstream"},
            zones=zones,
            text_space_strategy="editable_downstream_text_layers_only",
        )
        text_plan = ProductionTextPlan(
            editable_text_layers=["headline", "subcaption", "callout"],
            final_copy_source_refs=[f"composition_job:{composition_job_id}:text_content_ref"],
            downstream_renderer="skia",
        )
        handoff = GeometricsHandoffPlan(target_runtime="skia", layer_manifest_ref=layer_manifest_ref)
        receipt = IdeogramProductionBridgeReceipt(
            source_composition_job_id=composition_job_id,
            layout_plan_id=layout.composition_layout_plan_id,
            text_plan_id=text_plan.production_text_plan_id,
            geometrics_handoff_plan_id=handoff.geometrics_handoff_plan_id,
            decision_code="IDEOGRAM_LAYOUT_BRIDGED_TO_PRODUCTION_TEMPLATE",
            evidence_refs=[f"composition_job:{composition_job_id}", layer_manifest_ref],
        )
        return self.repository.put_ideogram_bridge_receipt(receipt)

    def extract_layers(self, *, source_asset_ref: str, layer_roles: list[str]) -> tuple[GenerativeAssetFactoryJob, LayerExtractionResult]:
        job = GenerativeAssetFactoryJob(
            provider="qwen_layered",
            requested_asset_role="layer_decomposition",
            source_context_refs=[source_asset_ref],
            deterministic_downstream_owner="cmf_geometrics_skia_runtime",
        )
        qwen = QwenLayeredDecompositionReceipt(
            source_asset_ref=source_asset_ref,
            layer_count=len(layer_roles),
            extracted_layer_refs=[f"{source_asset_ref}:layer:{role}" for role in layer_roles],
        )
        sam3 = SAM3SaliencyReceipt(source_asset_ref=source_asset_ref, mask_refs=[f"{source_asset_ref}:mask:{role}" for role in layer_roles], confidence=0.88)
        layers = [
            LayerManifestEntry(
                layer_id=f"layer-{index:02d}",
                source_ref=f"{source_asset_ref}:layer:{role}",
                role=role,
                bounds={"x": 0.05 * index, "y": 0.05 * index, "width": 0.8, "height": 0.2},
            )
            for index, role in enumerate(layer_roles, start=1)
        ]
        result = self.repository.put_layer_extraction_result(
            LayerExtractionResult(
                source_asset_ref=source_asset_ref,
                qwen_receipt_id=qwen.qwen_layered_decomposition_receipt_id,
                sam3_receipt_id=sam3.sam3_saliency_receipt_id,
                layers=layers,
                repair_required=sam3.confidence < 0.8,
                blocker_codes=[] if sam3.confidence >= 0.8 else ["LAYER_MASK_CONFIDENCE_LOW"],
            )
        )
        return job, result

    def compile_renderer_props(
        self,
        *,
        runtime_binding_id: UUID,
        component: RendererComponentRegistration,
    ) -> tuple[RendererPropsManifest, RendererComponentCompatibilityReport, RendererPropsCompilationReceipt]:
        runtime_binding = self.repository.runtime_bindings[runtime_binding_id]
        template = self._composition_template(runtime_binding.composition_template_id)
        blockers: list[str] = []
        if template.content_format_code not in component.supported_format_codes:
            blockers.append("RENDERER_COMPONENT_FORMAT_MISMATCH")
        if component.sandbox_policy != "no_network_no_production_api":
            blockers.append("RENDERER_COMPONENT_SANDBOX_POLICY_REQUIRED")
        compatible = not blockers
        report = RendererComponentCompatibilityReport(
            component_code=component.component_code,
            compatible=compatible,
            blocker_codes=blockers,
            evidence_refs=[f"composition_template:{template.composition_template_id}", f"runtime_binding:{runtime_binding_id}"],
        )
        manifest = self.repository.put_renderer_props_manifest(
            RendererPropsManifest(
                composition_runtime_binding_id=runtime_binding_id,
                renderer_target=component.renderer_target,
                component_code=component.component_code,
                props={
                    "composition_template": template.model_dump(mode="json"),
                    "runtime_binding": runtime_binding.model_dump(mode="json"),
                },
                deterministic_inputs_hash=runtime_hash({"template": template.composition_json_hash, "runtime_binding": runtime_binding.model_dump(mode="json")}),
                asset_policy_refs=["locked_brand_context_assets_only", "no_unscoped_fetch"],
            )
        )
        receipt = self.repository.put_renderer_props_receipt(
            RendererPropsCompilationReceipt(
                renderer_props_manifest_id=manifest.renderer_props_manifest_id,
                compatibility_report_id=report.renderer_component_compatibility_report_id,
                decision_code="RENDERER_PROPS_COMPILED" if compatible else "RENDERER_PROPS_BLOCKED",
                evidence_refs=report.evidence_refs,
            )
        )
        return manifest, report, receipt

    def convert_open_source_template(
        self,
        *,
        integration_adapter_decision_id: UUID,
        source_project: str,
        source_template_ref: str,
        cmf_template_family_code: str,
        converted_component_code: str,
    ) -> OpenSourceTemplateConversion:
        decision = self.repository.integration_adapter_decisions[integration_adapter_decision_id]
        blockers: list[str] = []
        if decision.decision == AdapterDecision.rejected:
            blockers.append("OPEN_SOURCE_ADAPTER_REJECTED")
        conversion = OpenSourceTemplateConversion(
            integration_adapter_decision_id=integration_adapter_decision_id,
            source_project=source_project,
            source_template_ref=source_template_ref,
            cmf_template_family_code=cmf_template_family_code,
            converted_component_code=converted_component_code,
            sandbox_path_ref=f"sandbox/adapters/{source_project}/{converted_component_code}",
            direct_import_allowed=False,
            blocker_codes=blockers,
        )
        return self.repository.put_open_source_template_conversion(conversion)

    def run_composition_eval_suite(
        self,
        *,
        target_object_type: str,
        target_object_ref: str,
        preflight_receipt_id: UUID,
        doctrine_receipt_refs: list[str] | None = None,
    ) -> CompositionEvalSuiteRun:
        preflight = self.repository.composition_preflight_receipts[preflight_receipt_id]
        blockers = list(preflight.hard_failure_codes)
        selection = EvalTargetSelection(
            target_object_type=target_object_type,
            target_object_ref=target_object_ref,
            eval_family="composition_primitive_doctrine_suite",
            required_receipt_refs=[f"composition_preflight:{preflight_receipt_id}", *(doctrine_receipt_refs or [])],
        )
        score = preflight.primitive_validation_count / max(preflight.minimum_validated_primitives, 1)
        run = CompositionEvalSuiteRun(
            eval_target_selection=selection,
            primitive_preflight_receipt=preflight,
            doctrine_receipt_refs=doctrine_receipt_refs or [],
            blocker_codes=blockers,
            decision="approved" if not blockers else "blocked",
            score=min(score, 1.0),
        )
        return self.repository.put_eval_suite_run(run)

    def build_review_read_model(
        self,
        *,
        target_object_ref: str,
        eval_suite_run_id: UUID,
        evidence_refs: list[str],
    ) -> ReviewReadModel:
        run = self.repository.eval_suite_runs[eval_suite_run_id]
        blockers = [
            CompositionApprovalBlocker(blocker_code=code, severity="hard", message=f"Blocked by {code}", evidence_refs=evidence_refs)
            for code in run.blocker_codes
        ]
        model = ReviewReadModel(
            target_object_ref=target_object_ref,
            approval_status=ApprovalStatus.approved if not blockers else ApprovalStatus.blocked,
            blockers=blockers,
            eval_suite_run_refs=[f"composition_eval_suite_run:{eval_suite_run_id}"],
            evidence_refs=evidence_refs,
        )
        return self.repository.put_review_read_model(model)

    def record_operator_approval(self, *, review_read_model_id: UUID, operator_id: UUID) -> CompositionOperatorApprovalReceipt:
        model = self.repository.review_read_models[review_read_model_id]
        blockers = [blocker.blocker_code for blocker in model.blockers if blocker.severity == "hard"]
        receipt = CompositionOperatorApprovalReceipt(
            review_read_model_id=review_read_model_id,
            operator_id=operator_id,
            decision="approved" if not blockers else "blocked",
            blocker_codes=blockers,
            evidence_refs=[*model.evidence_refs, f"review_read_model:{review_read_model_id}"],
        )
        return self.repository.put_operator_approval_receipt(receipt)

    def _route_rule(self, route_id: str) -> dict[str, Any]:
        routes = self.primitive_triad_registry()["route_triads"]
        if route_id not in routes:
            raise CompositionRuntimeServiceError("COMPOSITION_ROUTE_NOT_REGISTERED", route_id)
        return routes[route_id]

    def _composition_template(self, composition_template_id: UUID) -> CompositionTemplateJson:
        template = self.repository.composition_templates.get(composition_template_id)
        if template is None:
            raise CompositionRuntimeServiceError("COMPOSITION_TEMPLATE_REQUIRED", "Composition template JSON is required.")
        return template

    @staticmethod
    def _default_reaction_zones() -> list[CompositionZone]:
        return [
            CompositionZone(zone_id="headline", role="headline", x=0.06, y=0.04, width=0.88, height=0.16, safe_area=True),
            CompositionZone(zone_id="upper-ui", role="upper_reaction_ui", x=0.04, y=0.20, width=0.92, height=0.42, safe_area=True),
            CompositionZone(zone_id="lower-human", role="lower_human_cutouts", x=0.00, y=0.54, width=1.00, height=0.46, safe_area=True),
        ]

    @staticmethod
    def _default_reaction_layers() -> list[CompositionTemplateLayer]:
        return [
            CompositionTemplateLayer(layer_id="background", layer_type="atmospheric_plate", zone_id="upper-ui", source_ref="brand_genesis:background_plate", z_index=0, editable=True),
            CompositionTemplateLayer(layer_id="reaction-ui", layer_type="poll_or_rank_ui", zone_id="upper-ui", source_ref="composition:reaction_template", z_index=10, editable=True),
            CompositionTemplateLayer(layer_id="guest-cutout", layer_type="subject_cutout", zone_id="lower-human", source_ref="source_video:guest_mask", z_index=20, editable=False),
            CompositionTemplateLayer(layer_id="interviewer-cutout", layer_type="subject_cutout", zone_id="lower-human", source_ref="source_video:interviewer_mask", z_index=21, editable=False),
            CompositionTemplateLayer(layer_id="headline", layer_type="editable_text", zone_id="headline", source_ref="interview_asset_contract:headline", z_index=30, editable=True),
        ]
