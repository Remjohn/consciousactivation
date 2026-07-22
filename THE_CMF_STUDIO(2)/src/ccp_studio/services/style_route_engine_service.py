from __future__ import annotations

from ccp_studio.contracts.style_route_runtime import (
    AssetReference,
    CACProductionSpec,
    CompositionRole,
    GMGExpertSelection,
    GMGProductionSpec,
    GMGVerbatimNounMap,
    PaperCutArtifactSpec,
    PaperCutEditorialSpec,
    PassStatus,
    ProviderCapability,
    ProviderJobBlueprint,
    RequestingComponent,
    RouteProductionSpec,
    SourceGroundingMode,
    SourceReference,
    StyleRouteDecision,
    StyleRouteDecisionRequest,
    StyleRouteEvaluationReceipt,
    StyleRouteFamily,
    StyleRouteId,
    StyleRoutePreconditionReport,
    StyleRouteRepairInstruction,
    StyleRouteSourcePacket,
    StyleRouteUsageReceipt,
    TargetOutputType,
)
from ccp_studio.repositories.style_route_engine import InMemoryStyleRouteEngineRepository


GMG_ROUTES = {
    StyleRouteId.GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT,
    StyleRouteId.GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST,
    StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR,
    StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT,
    StyleRouteId.GMG_EXPERT_05_EDITORIAL_SCRIBE,
    StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER,
}


class StyleRouteEngineService:
    """Style Route / CAC / GMG / Paper-Cut V1 service.

    Compiles route decisions and provider blueprints. Never executes providers.
    """

    def __init__(self, repository: InMemoryStyleRouteEngineRepository | None = None):
        self.repository = repository or InMemoryStyleRouteEngineRepository()

    def create_decision_request(self, **kwargs) -> StyleRouteDecisionRequest:
        request = StyleRouteDecisionRequest(**kwargs)
        return self.repository.upsert_request(request)

    def validate_route_preconditions(self, request: StyleRouteDecisionRequest, route_id: StyleRouteId) -> StyleRoutePreconditionReport:
        required = ["brand_context_version_id", "frame_profile", "composition_role", "source_grounding_mode"]
        present = [key for key in required if getattr(request, key, None)]
        missing: list[str] = []
        violations: list[str] = []

        if route_id in request.forbidden_routes:
            violations.append("route_forbidden_by_request")
        if request.frame_profile.startswith("16:9") and request.target_output_type != TargetOutputType.SOURCE_REFERENCE:
            violations.append("16_9_is_source_only_for_short_form_route")

        if route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA:
            required += ["real_life_source_reference", "environment_logic"]
            if request.source_grounding_mode not in {SourceGroundingMode.DIRECT_REAL_REFERENCE, SourceGroundingMode.COMPOSITE_REAL_REFERENCES}:
                violations.append("cac_requires_direct_or_composite_real_reference")
            if not self._has_real_life_source(request):
                missing.append("real_life_source_reference")
        elif route_id == StyleRouteId.PAPER_CUT_ARTIFACT:
            required.append("source_object_reference")
            if not (request.source_references or request.asset_candidate_refs):
                missing.append("source_object_reference")
            if request.source_grounding_mode == SourceGroundingMode.STYLE_REFERENCE_ONLY:
                violations.append("paper_cut_artifact_cannot_use_style_reference_only")
        elif route_id == StyleRouteId.DOCUMENTARY_PROOF:
            required.append("proof_or_document_source")
            if not self._has_document_or_proof_source(request):
                missing.append("proof_or_document_source")
        elif route_id == StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR:
            required.append("photo_cutout_object")
            if not self._has_asset_role(request, "photo_cutout"):
                missing.append("photo_cutout_object")
        elif route_id == StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT:
            required.append("document_evidence_archive_input")
            if not self._has_document_or_proof_source(request):
                missing.append("document_evidence_archive_input")
        elif route_id == StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER:
            if request.source_grounding_mode not in {SourceGroundingMode.SOURCE_LANGUAGE_REFERENCE, SourceGroundingMode.ABSTRACT_SYMBOLIC_EXCEPTION}:
                violations.append("gmg_expert_06_requires_source_language_or_abstract_symbolic_mode")

        report = StyleRoutePreconditionReport(
            request_id=request.style_route_decision_request_id,
            route_id=route_id,
            required_inputs=sorted(set(required)),
            present_inputs=sorted(set(present)),
            missing_inputs=sorted(set(missing)),
            violations=violations,
            source_grounding_valid=not any("source" in v for v in violations),
            provider_ready=not missing and not violations,
            pass_status=PassStatus.FAIL if missing or violations else PassStatus.PASS,
        )
        return self.repository.upsert_precondition_report(report)

    def select_style_route(self, request: StyleRouteDecisionRequest) -> StyleRouteDecision:
        selected = request.operator_route_hint or self._default_route_for_request(request)
        report = self.validate_route_preconditions(request, selected)
        decision = StyleRouteDecision(
            request_id=request.style_route_decision_request_id,
            selected_route_id=selected,
            route_family=self._route_family(selected),
            confidence=0.85 if report.pass_status == PassStatus.PASS else 0.45,
            decision_rationale=f"Selected {selected.value} from request context and route preconditions.",
            source_grounding_mode=request.source_grounding_mode,
            required_inputs=report.required_inputs,
            missing_inputs=report.missing_inputs,
            compatible_provider_capabilities=self._provider_capabilities_for_route(selected),
            frame_profile_compatibility="16:9" not in request.frame_profile or request.target_output_type == TargetOutputType.SOURCE_REFERENCE,
            composition_role_compatibility=True,
            precondition_report_id=report.style_route_precondition_report_id,
            provider_ready=report.provider_ready,
            blocked_routes=request.forbidden_routes,
        )
        return self.repository.upsert_decision(decision)

    def compile_source_packet(self, request: StyleRouteDecisionRequest, *, visual_nouns: list[str] | None = None) -> StyleRouteSourcePacket:
        packet = StyleRouteSourcePacket(
            request_id=request.style_route_decision_request_id,
            source_grounding_mode=request.source_grounding_mode,
            source_references=request.source_references,
            visual_nouns=visual_nouns or [],
            asset_refs=request.asset_candidate_refs,
            is_source_grounded=bool(request.source_references or request.asset_candidate_refs),
        )
        return self.repository.upsert_source_packet(packet)

    def extract_gmg_verbatim_nouns(self, *, source_terms: list[str], requested_nouns: list[str], approved_asset_nouns: list[str] | None = None) -> GMGVerbatimNounMap:
        source_set = {term.lower() for term in source_terms + (approved_asset_nouns or [])}
        approved = [noun for noun in requested_nouns if noun.lower() in source_set]
        rejected = [noun for noun in requested_nouns if noun.lower() not in source_set]
        noun_map = GMGVerbatimNounMap(source_terms=source_terms, approved_nouns=approved, rejected_nouns=rejected, approved_asset_nouns=approved_asset_nouns or [])
        return self.repository.upsert_noun_map(noun_map)

    def compile_cac_production_spec(self, source_packet: StyleRouteSourcePacket, **overrides) -> CACProductionSpec:
        spec = CACProductionSpec(
            source_packet_id=source_packet.style_route_source_packet_id,
            source_grounding_mode=source_packet.source_grounding_mode,
            real_reference_refs=[r.source_reference_id for r in source_packet.source_references] or [a.asset_ref_id for a in source_packet.asset_refs],
            mundane_anchor=overrides.get("mundane_anchor", "source-backed mundane object"),
            contact_point=overrides.get("contact_point", "human contact with object or environment"),
            composition_logic=overrides.get("composition_logic", "human-scale editorial realism"),
            atmosphere=overrides.get("atmosphere", "quiet documentary atmosphere"),
            imperfection_cues=overrides.get("imperfection_cues", ["minor clutter", "non-perfect surface", "natural asymmetry"]),
            lens_language=overrides.get("lens_language", "natural lens, motivated depth"),
            camera_distance=overrides.get("camera_distance", "close observational distance"),
            lighting_motivation=overrides.get("lighting_motivation", "motivated real-world light"),
            human_scale_space=overrides.get("human_scale_space", "human-scale room or work surface"),
            forbidden_cliches=["generic cinematic gloss", "luxury stock aesthetic", "abstract symbolic scene"],
            provider_constraints=["real-life source reference required", "motivated light required"],
            eval_targets=["realism", "source_fidelity", "human_scale_recognition", "motivated_light", "imperfection"],
        )
        return self.repository.upsert_cac_spec(spec)

    def route_gmg_expert(self, *, source_terms: list[str], intent: str) -> GMGExpertSelection:
        haystack = " ".join(source_terms + [intent]).lower()
        if any(t in haystack for t in ["system", "network", "flow", "signal", "process", "mechanism"]):
            selected = StyleRouteId.GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT
        elif any(t in haystack for t in ["hero", "pressure", "force", "avatar", "protagonist"]):
            selected = StyleRouteId.GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST
        elif any(t in haystack for t in ["emotion", "awkward", "humor", "cutout", "stick"]):
            selected = StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR
        elif any(t in haystack for t in ["document", "receipt", "archive", "record", "letter", "evidence"]):
            selected = StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT
        elif any(t in haystack for t in ["metric", "framework", "label", "infographic", "teaching"]):
            selected = StyleRouteId.GMG_EXPERT_05_EDITORIAL_SCRIBE
        else:
            selected = StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER
        return self.repository.upsert_gmg_selection(GMGExpertSelection(selected_expert_route_id=selected, rationale=f"Routed from intent: {intent}", confidence=0.82))

    def compile_gmg_production_spec(self, *, route_id: StyleRouteId, source_packet: StyleRouteSourcePacket, noun_map: GMGVerbatimNounMap, frame_profile: str, composition_role: CompositionRole, prompt_contract: str, has_photo_cutout_object: bool = False, has_document_archive_input: bool = False) -> GMGProductionSpec:
        expert_number = int(route_id.value.split("_")[2])
        spec = GMGProductionSpec(
            route_id=route_id,
            expert_number=expert_number,
            source_packet_id=source_packet.style_route_source_packet_id,
            verbatim_noun_map_id=noun_map.gmg_verbatim_noun_map_id,
            primary_visual_nouns=noun_map.approved_nouns,
            motion_language=self._motion_language_for_gmg(route_id),
            prompt_contract=prompt_contract,
            frame_profile=frame_profile,
            composition_role=composition_role,
            expert_input_requirements=self._gmg_requirements(route_id),
            has_photo_cutout_object=has_photo_cutout_object,
            has_document_archive_input=has_document_archive_input,
            forbidden_patterns=self._forbidden_patterns_for_route(route_id),
        )
        return self.repository.upsert_gmg_spec(spec)

    def compile_paper_cut_artifact_spec(self, *, source_object_refs: list[str], composition_role: CompositionRole = CompositionRole.PAPER_CUT_OBJECT, semantic_role: str = "source-grounded artifact") -> PaperCutArtifactSpec:
        spec = PaperCutArtifactSpec(
            source_object_refs=source_object_refs,
            cutout_requirements=["clean mask", "visible paper edge", "object silhouette preserved"],
            mask_requirements=["foreground object mask"],
            layer_depth=3,
            paper_edge_treatment="slightly torn white paper edge",
            shadow_treatment="hard tabletop shadow with tactile separation",
            attachment_treatment="small tape or paperclip only when semantically useful",
            semantic_role=semantic_role,
            composition_role=composition_role,
        )
        return self.repository.upsert_paper_artifact_spec(spec)

    def compile_paper_cut_editorial_spec(self, *, frame_profile: str, visual_hierarchy: list[str], layer_system: list[str], object_anchors: list[str] | None = None) -> PaperCutEditorialSpec:
        spec = PaperCutEditorialSpec(
            visual_hierarchy=visual_hierarchy,
            paper_surface="editorial paper surface with tactile grain",
            layer_system=layer_system,
            object_anchors=object_anchors or [],
            type_label_treatment="readable editorial label treatment",
            mobile_readability_notes="text and object scale must remain readable on mobile",
            frame_profile=frame_profile,
        )
        return self.repository.upsert_paper_editorial_spec(spec)

    def compile_route_production_spec(self, *, decision: StyleRouteDecision, request: StyleRouteDecisionRequest, source_packet: StyleRouteSourcePacket, route_specific_spec_type: str, route_specific_spec_id: str, forbidden_patterns: list[str] | None = None, expected_output_type: TargetOutputType | None = None) -> RouteProductionSpec:
        spec = RouteProductionSpec(
            style_route_decision_id=decision.style_route_decision_id,
            route_id=decision.selected_route_id,
            brand_id=request.brand_id,
            brand_context_version_id=request.brand_context_version_id,
            visual_preproduction_packet_id=request.visual_preproduction_packet_id,
            visual_beat_plan_id=request.visual_beat_plan_id,
            frame_profile=request.frame_profile,
            composition_role=request.composition_role,
            source_packet_id=source_packet.style_route_source_packet_id,
            route_specific_spec_type=route_specific_spec_type,
            route_specific_spec_id=route_specific_spec_id,
            forbidden_patterns=forbidden_patterns or self._forbidden_patterns_for_route(decision.selected_route_id),
            provider_constraints=["provider job must preserve primary style route purity"],
            expected_output_type=expected_output_type or request.target_output_type,
            eval_targets=self._eval_targets_for_route(decision.selected_route_id),
        )
        return self.repository.upsert_route_spec(spec)

    def compile_provider_job_blueprint(self, *, route_spec: RouteProductionSpec, source_references: list[str] | None = None, input_asset_refs: list[str] | None = None, reference_asset_refs: list[str] | None = None, prompt_contract: str | None = None) -> ProviderJobBlueprint:
        blueprint = ProviderJobBlueprint(
            route_production_spec_id=route_spec.route_production_spec_id,
            primary_style_route_id=route_spec.route_id,
            recommended_provider_capability=self._provider_capabilities_for_route(route_spec.route_id)[0],
            input_asset_refs=input_asset_refs or [],
            reference_asset_refs=reference_asset_refs or [],
            source_references=source_references or [],
            frame_profile=route_spec.frame_profile,
            composition_role=route_spec.composition_role,
            prompt_contract=prompt_contract or f"Compile provider instruction for {route_spec.route_id.value}.",
            negative_prompt_contract=", ".join(route_spec.forbidden_patterns),
            output_requirements=["source_reference", "style_route", "frame_profile", "composition_role"],
            idempotency_key_seed=f"{route_spec.route_production_spec_id}:{route_spec.route_id.value}",
            required_receipts=["ProviderJobReceipt", "StyleRouteUsageReceipt"],
            blocked_until=[],
            execution_state="blueprint_only",
        )
        return self.repository.upsert_provider_blueprint(blueprint)

    def evaluate_route_output(self, *, route_id: StyleRouteId, route_production_spec_id: str | None = None, forbidden_patterns_detected: list[str] | None = None, source_grounding_score: float = 0.8) -> StyleRouteEvaluationReceipt:
        patterns = forbidden_patterns_detected or []
        receipt = StyleRouteEvaluationReceipt(
            route_id=route_id,
            route_production_spec_id=route_production_spec_id,
            source_grounding_score=source_grounding_score,
            forbidden_patterns_detected=patterns,
            pass_status=PassStatus.FAIL if patterns or source_grounding_score < 0.5 else PassStatus.PASS,
            rationale="Deterministic V1 style route evaluation.",
        )
        return self.repository.upsert_evaluation(receipt)

    def compile_repair_instruction(self, *, route_id: StyleRouteId, target_ref: str, issue: str, repair_action: str, requires_new_asset_reference: bool = False) -> StyleRouteRepairInstruction:
        return self.repository.upsert_repair_instruction(StyleRouteRepairInstruction(route_id=route_id, target_ref=target_ref, issue=issue, repair_action=repair_action, requires_new_asset_reference=requires_new_asset_reference))

    def record_route_usage(self, *, route_id: StyleRouteId, brand_id: str, brand_context_version_id: str, requesting_component: RequestingComponent, route_production_spec_id: str | None = None, provider_job_blueprint_id: str | None = None, output_ref: str | None = None, frame_profile: str | None = None, composition_role: CompositionRole | None = None) -> StyleRouteUsageReceipt:
        receipt = StyleRouteUsageReceipt(route_id=route_id, brand_id=brand_id, brand_context_version_id=brand_context_version_id, requesting_component=requesting_component, route_production_spec_id=route_production_spec_id, provider_job_blueprint_id=provider_job_blueprint_id, output_ref=output_ref, frame_profile=frame_profile, composition_role=composition_role)
        return self.repository.upsert_usage(receipt)

    def explain_route_decision(self, decision: StyleRouteDecision) -> str:
        return f"{decision.selected_route_id.value} selected with confidence {decision.confidence:.2f}. Provider ready: {decision.provider_ready}. Missing inputs: {decision.missing_inputs or 'none'}."

    def _default_route_for_request(self, request: StyleRouteDecisionRequest) -> StyleRouteId:
        if request.composition_role in {CompositionRole.PROOF_OBJECT, CompositionRole.PAPER_CUT_OBJECT} and (request.source_references or request.asset_candidate_refs):
            return StyleRouteId.PAPER_CUT_ARTIFACT
        if request.source_grounding_mode in {SourceGroundingMode.DIRECT_REAL_REFERENCE, SourceGroundingMode.COMPOSITE_REAL_REFERENCES}:
            return StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA
        if request.source_grounding_mode == SourceGroundingMode.ABSTRACT_SYMBOLIC_EXCEPTION:
            return StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER
        return StyleRouteId.DETERMINISTIC_SKIA_CARD

    def _route_family(self, route_id: StyleRouteId) -> StyleRouteFamily:
        if route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA:
            return StyleRouteFamily.REAL_CINEMATIC
        if route_id in GMG_ROUTES:
            return StyleRouteFamily.GMG
        if route_id in {StyleRouteId.PAPER_CUT_EDITORIAL, StyleRouteId.PAPER_CUT_ARTIFACT}:
            return StyleRouteFamily.PAPER_CUT
        if route_id == StyleRouteId.DETERMINISTIC_SKIA_CARD:
            return StyleRouteFamily.DETERMINISTIC
        return StyleRouteFamily.EVIDENCE_INTERFACE_AVATAR

    def _provider_capabilities_for_route(self, route_id: StyleRouteId) -> list[ProviderCapability]:
        if route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA:
            return [ProviderCapability.IDEOGRAM_4, ProviderCapability.GPT_IMAGE, ProviderCapability.FAKE_PROVIDER]
        if route_id in GMG_ROUTES:
            return [ProviderCapability.MOTION_CANVAS, ProviderCapability.REMOTION, ProviderCapability.SKIA, ProviderCapability.FAKE_PROVIDER]
        if route_id in {StyleRouteId.PAPER_CUT_ARTIFACT, StyleRouteId.PAPER_CUT_EDITORIAL}:
            return [ProviderCapability.QWEN_IMAGE_LAYERED, ProviderCapability.SAM3, ProviderCapability.SKIA, ProviderCapability.FAKE_PROVIDER]
        if route_id == StyleRouteId.DETERMINISTIC_SKIA_CARD:
            return [ProviderCapability.SKIA, ProviderCapability.FAKE_PROVIDER]
        return [ProviderCapability.GPT_IMAGE, ProviderCapability.SKIA, ProviderCapability.FAKE_PROVIDER]

    def _has_real_life_source(self, request: StyleRouteDecisionRequest) -> bool:
        return any(ref.is_real_life_reference for ref in request.source_references) or bool(request.asset_candidate_refs)

    def _has_document_or_proof_source(self, request: StyleRouteDecisionRequest) -> bool:
        source_text = " ".join([ref.source_kind + " " + (ref.description or "") for ref in request.source_references]).lower()
        role_text = " ".join([ref.asset_role or "" for ref in request.asset_candidate_refs]).lower()
        return any(term in source_text + " " + role_text for term in ["document", "receipt", "archive", "record", "letter", "evidence", "proof"])

    def _has_asset_role(self, request: StyleRouteDecisionRequest, role_fragment: str) -> bool:
        return any(role_fragment in (asset.asset_role or "").lower() for asset in request.asset_candidate_refs)

    def _gmg_requirements(self, route_id: StyleRouteId) -> list[str]:
        if route_id == StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR:
            return ["stick_figure", "photo_cutout_object", "direct_interaction_rule"]
        if route_id == StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT:
            return ["document_evidence_archive_input", "single_artifact_or_document_system"]
        if route_id == StyleRouteId.GMG_EXPERT_05_EDITORIAL_SCRIBE:
            return ["metric_or_framework", "label_hierarchy", "two_color_plus_paper"]
        if route_id == StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER:
            return ["source_language_concept", "visual_equation", "pure_geometry"]
        return ["source_nouns", "expert_specific_visual_logic"]

    def _motion_language_for_gmg(self, route_id: StyleRouteId) -> str:
        return {
            StyleRouteId.GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT: "nodes, vectors, signal flow, schematic motion",
            StyleRouteId.GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST: "single protagonist pressure, noir force, kinetic impact",
            StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR: "stick figure plus photo cutout direct interaction",
            StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT: "paper artifacts, archival motion, stop-motion texture boil",
            StyleRouteId.GMG_EXPERT_05_EDITORIAL_SCRIBE: "sketch to fill to label, editorial infographic motion",
            StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER: "pure geometry, white lines, visual equation",
        }.get(route_id, "expert-specific motion language")

    def _forbidden_patterns_for_route(self, route_id: StyleRouteId) -> list[str]:
        if route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA:
            return ["generic cinematic gloss", "luxury stock aesthetic", "abstract symbolic scene"]
        if route_id == StyleRouteId.GMG_EXPERT_05_EDITORIAL_SCRIBE:
            return ["3d", "glass", "neon"]
        if route_id == StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER:
            return ["gold", "photo object", "paper texture", "generic tech ui"]
        if route_id == StyleRouteId.PAPER_CUT_ARTIFACT:
            return ["fake proof object", "decorative paper texture"]
        return ["route averaging", "generic visual mush"]

    def _eval_targets_for_route(self, route_id: StyleRouteId) -> list[str]:
        if route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA:
            return ["realism", "source_fidelity", "human_scale_truth", "motivated_light", "anti_stock_feel"]
        if route_id in GMG_ROUTES:
            return ["expert_purity", "source_noun_fidelity", "logic_clarity", "forbidden_symbol_absence"]
        if route_id in {StyleRouteId.PAPER_CUT_ARTIFACT, StyleRouteId.PAPER_CUT_EDITORIAL}:
            return ["artifact_truth", "tactile_depth", "paper_materiality", "edge_quality", "mobile_readability"]
        return ["route_fit", "brand_fit", "composition_role_fit"]
