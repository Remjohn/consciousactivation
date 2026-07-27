from __future__ import annotations

from datetime import datetime, timezone

from ccp_studio.contracts.visual_preproduction import (
    AssetRequirement,
    AuthorizationStatus,
    CameraMoralStance,
    ConstraintGateCReport,
    ConstraintViolation,
    FamiliarityElementId,
    KineticVerb,
    LightingPreset,
    PRIMALAnalysis,
    PacketStatus,
    PassStatus,
    PreproductionDepth,
    REQUIRED_FAMILIARITY_ELEMENTS,
    ShotType,
    SourceAuthorityLevel,
    SourceRef,
    StoryboardCommanderVerdict,
    StoryboardIngredientSet,
    TargetComponent,
    TCode,
    VAEDecoderReport,
    VCode,
    VisualAnalystReport,
    VisualBeatPlan,
    VisualFamiliarityElementAssessment,
    VisualPreproductionPacket,
    VisualPreproductionRequest,
    VisualSchema,
)
from ccp_studio.repositories.visual_preproduction import InMemoryVisualPreproductionRepository


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class VisualPreproductionService:
    """Canonical Visual Preproduction V1 service.

    V1 is deterministic and in-memory-testable. DSPy programs can be added
    behind these methods without changing downstream contracts.
    """

    def __init__(self, repository: InMemoryVisualPreproductionRepository | None = None):
        self.repository = repository or InMemoryVisualPreproductionRepository()

    def create_request(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        target_component: TargetComponent,
        preproduction_depth: PreproductionDepth,
        source_context_refs: list[SourceRef] | None = None,
        primitive_coalition_contract_id: str | None = None,
        strategy_brief_ref: str | None = None,
        brand_avatar_ref: str | None = None,
        operator_notes: str | None = None,
    ) -> VisualPreproductionRequest:
        request = VisualPreproductionRequest(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            target_component=target_component,
            preproduction_depth=preproduction_depth,
            source_context_refs=source_context_refs or [],
            primitive_coalition_contract_id=primitive_coalition_contract_id,
            strategy_brief_ref=strategy_brief_ref,
            brand_avatar_ref=brand_avatar_ref,
            operator_notes=operator_notes,
        )
        return self.repository.upsert_request(request)

    def compile_visual_schema(
        self,
        request: VisualPreproductionRequest,
        *,
        environment_logic: str,
        source_authority_map: dict[str, SourceAuthorityLevel] | None = None,
        human_context: str | None = None,
        object_logic: str | None = None,
        lighting_context: str | None = None,
        color_context: str | None = None,
        visual_tropes_to_use: list[str] | None = None,
        visual_tropes_to_avoid: list[str] | None = None,
    ) -> VisualSchema:
        elements = self._default_familiarity_elements()
        schema = VisualSchema(
            brand_id=request.brand_id,
            brand_context_version_id=request.brand_context_version_id,
            source_context_refs=request.source_context_refs,
            primitive_coalition_contract_id=request.primitive_coalition_contract_id,
            strategy_brief_ref=request.strategy_brief_ref,
            brand_avatar_ref=request.brand_avatar_ref,
            target_component=request.target_component,
            preproduction_depth=request.preproduction_depth,
            visual_familiarity_elements=elements,
            environment_logic=environment_logic,
            human_context=human_context,
            object_logic=object_logic,
            lighting_context=lighting_context,
            color_context=color_context,
            visual_tropes_to_use=visual_tropes_to_use or [],
            visual_tropes_to_avoid=visual_tropes_to_avoid or ["generic skyline", "abstract glowing network", "faceless confident founder"],
            source_authority_map=source_authority_map or {"environment_logic": SourceAuthorityLevel.RESEARCH_SUPPORTED},
            negative_space_risks=[],
            style_route_constraints=[],
            asset_intelligence_requirements=[],
        )
        return self.repository.upsert_visual_schema(schema)

    def map_source_evidence(
        self,
        schema: VisualSchema,
        *,
        claim_to_authority: dict[str, SourceAuthorityLevel],
    ) -> VisualSchema:
        schema.source_authority_map.update(claim_to_authority)
        return self.repository.upsert_visual_schema(schema)

    def score_familiarity_elements(
        self,
        schema: VisualSchema,
        *,
        default_score: float = 0.75,
    ) -> VisualSchema:
        updated = []
        for item in schema.visual_familiarity_elements:
            updated.append(
                VisualFamiliarityElementAssessment(
                    element_id=item.element_id,
                    finding=item.finding,
                    source_evidence_refs=item.source_evidence_refs,
                    score=item.score if item.score is not None else default_score,
                    not_applicable=item.not_applicable,
                    not_applicable_reason=item.not_applicable_reason,
                )
            )
        schema.visual_familiarity_elements = updated
        return self.repository.upsert_visual_schema(schema)

    def map_subjective_distortions(
        self,
        schema: VisualSchema,
        *,
        distortions: list[str],
    ) -> VisualSchema:
        schema.subjective_distortions = distortions
        return self.repository.upsert_visual_schema(schema)

    def compile_storyboard_ingredients(
        self,
        schema: VisualSchema,
        *,
        required_visual_ingredients: list[str] | None = None,
        character_anchor: str | None = None,
        environment_anchor: str | None = None,
        proof_objects: list[str] | None = None,
        micro_semiotic_anchors: list[str] | None = None,
        style_references: list[str] | None = None,
    ) -> StoryboardIngredientSet:
        asset_requirements = [
            AssetRequirement(
                ingredient_kind="proof_object",
                semantic_need="source-grounded proof or familiar real-life object",
                required=True,
                required_asset_roles=["proof_object"],
                source_authority_required=SourceAuthorityLevel.RESEARCH_SUPPORTED,
            )
        ]
        ingredients = StoryboardIngredientSet(
            visual_schema_id=schema.visual_schema_id,
            brand_id=schema.brand_id,
            brand_context_version_id=schema.brand_context_version_id,
            target_component=schema.target_component,
            required_visual_ingredients=required_visual_ingredients or ["proof_object", "environment_anchor"],
            character_anchor=character_anchor,
            environment_anchor=environment_anchor or schema.environment_logic,
            proof_objects=proof_objects or [],
            micro_semiotic_anchors=micro_semiotic_anchors or [],
            style_references=style_references or [],
            lighting_requirements=[schema.lighting_context] if schema.lighting_context else [],
            shot_requirements=[ShotType.INSERT, ShotType.STATIC_PROOF_CARD],
            motion_requirements=[KineticVerb.REVEAL],
            source_authority_requirements={"environment_anchor": SourceAuthorityLevel.RESEARCH_SUPPORTED},
            asset_requirements=asset_requirements,
        )
        return self.repository.upsert_ingredient_set(ingredients)

    def emit_asset_requirements(self, ingredients: StoryboardIngredientSet) -> list[AssetRequirement]:
        return ingredients.asset_requirements

    def compile_beat_visual_plan(
        self,
        schema: VisualSchema,
        *,
        source_beat_ref: str | None = None,
        beat_index: int = 0,
        beat_role: str = "single_visual",
        viewer_state_target: str | None = None,
        visual_question: str | None = None,
        visual_payoff: str | None = None,
        shot_type: ShotType = ShotType.STATIC_PROOF_CARD,
        t_code: TCode = TCode.T_SOURCE_PROOF,
        v_code: VCode = VCode.V_OBJECT_ANCHOR,
        kinetic_verb: KineticVerb = KineticVerb.REVEAL,
        camera_moral_stance: CameraMoralStance = CameraMoralStance.WITNESS,
        environment_directive: str | None = None,
        lighting_preset: LightingPreset = LightingPreset.PAPER_TABLETOP,
        forbidden_visuals: list[str] | None = None,
    ) -> VisualBeatPlan:
        plan = VisualBeatPlan(
            visual_schema_id=schema.visual_schema_id,
            source_beat_ref=source_beat_ref,
            beat_index=beat_index,
            beat_role=beat_role,
            viewer_state_target=viewer_state_target,
            primitive_obligation=schema.primitive_coalition_contract_id,
            visual_question=visual_question,
            visual_payoff=visual_payoff,
            shot_type=shot_type,
            t_code=t_code,
            v_code=v_code,
            kinetic_verb=kinetic_verb,
            camera_moral_stance=camera_moral_stance,
            environment_directive=environment_directive or schema.environment_logic,
            lighting_preset=lighting_preset,
            forbidden_visuals=forbidden_visuals or schema.visual_tropes_to_avoid,
        )
        return self.repository.upsert_beat_plan(plan)

    def run_primal_analysis(
        self,
        beat_plan: VisualBeatPlan,
        *,
        feeling: str,
        body_truth: str,
        environment: str | None = None,
        timestamp_or_temporal_context: str = "source-derived moment",
        uniqueness: str = "specific source-backed visual detail",
        source_evidence_refs: list[str] | None = None,
    ) -> PRIMALAnalysis:
        primal = PRIMALAnalysis(
            visual_beat_plan_id=beat_plan.visual_beat_plan_id,
            feeling=feeling,
            body_truth=body_truth,
            environment=environment or beat_plan.environment_directive,
            timestamp_or_temporal_context=timestamp_or_temporal_context,
            uniqueness=uniqueness,
            source_evidence_refs=source_evidence_refs or [],
            pass_status=PassStatus.PASS,
        )
        return self.repository.upsert_primal(primal)

    def run_vae_decoder(
        self,
        beat_plan: VisualBeatPlan,
        *,
        semantic_check: str = "Visual directive is semantically legible.",
        shadow_filter: str = "No unintended shadow meaning detected.",
        anti_cliche_gate: str = "No generic startup cliché.",
        generic_visual_risks: list[str] | None = None,
        recommended_repairs: list[str] | None = None,
    ) -> VAEDecoderReport:
        risks = generic_visual_risks or []
        status = PassStatus.FAIL if risks else PassStatus.PASS
        vae = VAEDecoderReport(
            visual_beat_plan_id=beat_plan.visual_beat_plan_id,
            semantic_check=semantic_check,
            shadow_filter=shadow_filter,
            anti_cliche_gate=anti_cliche_gate,
            generic_visual_risks=risks,
            recommended_repairs=recommended_repairs or [],
            pass_status=status,
        )
        return self.repository.upsert_vae(vae)

    def run_constraint_gate_c(
        self,
        *,
        target_ref: str,
        character_anchor_present: bool = True,
        source_authority_pass: bool = True,
        lighting_cliche_pass: bool = True,
        asset_coverage_pass: bool = True,
    ) -> ConstraintGateCReport:
        checks = {
            "character_anchor_vs_beat_action": character_anchor_present,
            "source_authority_for_environment": source_authority_pass,
            "lighting_x_anti_cliche": lighting_cliche_pass,
            "asset_requirement_coverage": asset_coverage_pass,
        }
        violations = []
        for check_id, passed in checks.items():
            if not passed:
                violations.append(
                    ConstraintViolation(
                        check_id=check_id,
                        severity="blocking",
                        message=f"Constraint Gate C failed: {check_id}",
                        repair_action=f"Repair {check_id} before packet freeze.",
                    )
                )
        report = ConstraintGateCReport(
            target_ref=target_ref,
            checks=checks,
            violations=violations,
            repair_actions=[v.repair_action for v in violations if v.repair_action],
            pass_status=PassStatus.FAIL if violations else PassStatus.PASS,
        )
        return self.repository.upsert_gate_c(report)

    def validate_with_visual_analyst(
        self,
        *,
        target_component: TargetComponent,
        beat_plans: list[VisualBeatPlan],
        packet_id: str | None = None,
    ) -> VisualAnalystReport:
        failed = []
        passed = []
        for plan in beat_plans:
            if not plan.t_code:
                failed.append("missing_t_code")
            else:
                passed.append("t_code_present")
            if not plan.v_code:
                failed.append("missing_v_code")
            else:
                passed.append("v_code_present")
            if not plan.kinetic_verb:
                failed.append("missing_kinetic_verb")
            else:
                passed.append("kinetic_verb_present")
            if not plan.environment_directive:
                failed.append("missing_environment_directive")
            else:
                passed.append("environment_directive_present")

        report = VisualAnalystReport(
            visual_preproduction_packet_id=packet_id,
            target_component=target_component,
            checked_directives=[p.visual_beat_plan_id for p in beat_plans],
            passed_checks=passed,
            failed_checks=failed,
            repair_required=bool(failed),
            pass_status=PassStatus.FAIL if failed else PassStatus.PASS,
            analyst_notes="Deterministic V1 visual analyst checks completed.",
        )
        return self.repository.upsert_analyst_report(report)

    def authorize_with_storyboard_commander(
        self,
        *,
        packet_id: str | None = None,
        batch_ref: str | None = None,
        visual_anchor_present: bool = True,
        camera_moral_stance_present: bool = True,
        montage_logic_present: bool = True,
    ) -> StoryboardCommanderVerdict:
        repairs = []
        if not visual_anchor_present:
            repairs.append("Add visual anchor block.")
        if not camera_moral_stance_present:
            repairs.append("Define camera moral stance.")
        if not montage_logic_present:
            repairs.append("Define montage logic.")

        status = AuthorizationStatus.AUTHORIZED if not repairs else AuthorizationStatus.REPAIR_REQUIRED
        verdict = StoryboardCommanderVerdict(
            visual_preproduction_packet_id=packet_id,
            batch_ref=batch_ref,
            visual_anchor_block_status="passed" if visual_anchor_present else "failed",
            camera_moral_stance_status="passed" if camera_moral_stance_present else "failed",
            montage_logic_status="passed" if montage_logic_present else "failed",
            authorization_status=status,
            required_repairs=repairs,
            approved_for_downstream=status == AuthorizationStatus.AUTHORIZED,
        )
        return self.repository.upsert_commander_verdict(verdict)

    def create_packet(
        self,
        *,
        request: VisualPreproductionRequest,
        schema: VisualSchema,
        ingredients: StoryboardIngredientSet | None = None,
        beat_plans: list[VisualBeatPlan] | None = None,
        primal_reports: list[PRIMALAnalysis] | None = None,
        vae_reports: list[VAEDecoderReport] | None = None,
        gate_c_report: ConstraintGateCReport | None = None,
        analyst_report: VisualAnalystReport | None = None,
        commander_verdict: StoryboardCommanderVerdict | None = None,
    ) -> VisualPreproductionPacket:
        packet = VisualPreproductionPacket(
            brand_id=request.brand_id,
            brand_context_version_id=request.brand_context_version_id,
            target_component=request.target_component,
            preproduction_depth=request.preproduction_depth,
            source_context_refs=request.source_context_refs,
            primitive_coalition_contract_id=request.primitive_coalition_contract_id,
            visual_schema_id=schema.visual_schema_id,
            storyboard_ingredient_set_id=ingredients.storyboard_ingredient_set_id if ingredients else None,
            visual_beat_plan_ids=[p.visual_beat_plan_id for p in beat_plans or []],
            primal_analysis_ids=[p.primal_analysis_id for p in primal_reports or []],
            vae_report_ids=[p.vae_decoder_report_id for p in vae_reports or []],
            constraint_gate_c_report_id=gate_c_report.constraint_gate_c_report_id if gate_c_report else None,
            visual_analyst_report_id=analyst_report.visual_analyst_report_id if analyst_report else None,
            storyboard_commander_verdict_id=commander_verdict.storyboard_commander_verdict_id if commander_verdict else None,
            asset_requirement_refs=[req.asset_requirement_id for req in ingredients.asset_requirements] if ingredients else [],
            style_route_constraints=schema.style_route_constraints,
            packet_status=PacketStatus.VALIDATED if analyst_report and analyst_report.pass_status == PassStatus.PASS else PacketStatus.DRAFT,
        )
        return self.repository.upsert_packet(packet)

    def freeze_packet(
        self,
        packet: VisualPreproductionPacket,
        *,
        gate_c_report: ConstraintGateCReport | None = None,
        analyst_report: VisualAnalystReport | None = None,
        commander_verdict: StoryboardCommanderVerdict | None = None,
    ) -> VisualPreproductionPacket:
        if gate_c_report and gate_c_report.blocking_violations:
            raise ValueError("Cannot freeze packet with blocking Constraint Gate C violations.")
        if analyst_report and analyst_report.pass_status == PassStatus.FAIL:
            raise ValueError("Cannot freeze packet with failed Visual Analyst Report.")
        if packet.preproduction_depth == PreproductionDepth.FULL_BATCH:
            if not commander_verdict or not commander_verdict.approved_for_downstream:
                raise ValueError("Full-batch packet freeze requires approved Storyboard Commander verdict.")

        packet.constraint_gate_c_report_id = gate_c_report.constraint_gate_c_report_id if gate_c_report else packet.constraint_gate_c_report_id
        packet.visual_analyst_report_id = analyst_report.visual_analyst_report_id if analyst_report else packet.visual_analyst_report_id
        packet.storyboard_commander_verdict_id = commander_verdict.storyboard_commander_verdict_id if commander_verdict else packet.storyboard_commander_verdict_id
        packet.packet_status = PacketStatus.FROZEN
        packet.frozen_at = _now_iso()
        if "style_route.select" not in packet.approved_downstream_actions:
            packet.approved_downstream_actions.append("style_route.select")
        if "asset_intelligence.retrieve" not in packet.approved_downstream_actions:
            packet.approved_downstream_actions.append("asset_intelligence.retrieve")
        return self.repository.upsert_packet(packet)

    def apply_revision(self, packet: VisualPreproductionPacket, *, repair_note: str) -> VisualPreproductionPacket:
        packet.packet_status = PacketStatus.REPAIR_REQUIRED
        packet.provider_preconditions.append(f"revision_required:{repair_note}")
        return self.repository.upsert_packet(packet)

    def _default_familiarity_elements(self) -> list[VisualFamiliarityElementAssessment]:
        findings = {
            FamiliarityElementId.UNIVERSAL_EXPERIENCES: "Ground the image in a familiar human experience.",
            FamiliarityElementId.RECOGNIZABLE_EMOTIONS: "Emotion must be legible without explanation.",
            FamiliarityElementId.FAMILIAR_BODY_TYPES: "Use recognizable body/gesture language when people are present.",
            FamiliarityElementId.DECISIVE_MOMENTS: "Choose a moment with before/after implication.",
            FamiliarityElementId.CONTEXTUAL_CLUES: "Include concrete clues that locate the visual world.",
            FamiliarityElementId.HUMAN_SCALE_SPACES: "Keep space human-scale unless style route requires abstraction.",
            FamiliarityElementId.LIMINAL_SPACES: "Use thresholds, tables, hallways, screens, or transitional spaces when relevant.",
            FamiliarityElementId.CULTURAL_SYMBOLS: "Use culturally legible symbols only when source-grounded.",
            FamiliarityElementId.ARCHETYPAL_COMPOSITIONS: "Choose a composition archetype the viewer can parse quickly.",
            FamiliarityElementId.NATURAL_FRAMING: "Use natural framing or card framing to guide attention.",
            FamiliarityElementId.FOCAL_POINT_RULE: "One dominant focal point must be clear.",
            FamiliarityElementId.LIGHTING_CONTEXTS: "Lighting must imply a believable real-world context.",
            FamiliarityElementId.COLOR_PALETTE: "Palette should align with brand context and style route.",
            FamiliarityElementId.NOSTALGIC_AESTHETIC: "Nostalgia may be used only when source/brand supports it.",
            FamiliarityElementId.LIGHT_QUALITY: "Light quality should be specific, not generic cinematic gloss.",
            FamiliarityElementId.VISUAL_TROPES_USE_AVOID: "Use source-backed tropes and block generic clichés.",
        }
        return [
            VisualFamiliarityElementAssessment(
                element_id=element,
                finding=finding,
                source_evidence_refs=[],
                score=0.75,
            )
            for element, finding in findings.items()
        ]
