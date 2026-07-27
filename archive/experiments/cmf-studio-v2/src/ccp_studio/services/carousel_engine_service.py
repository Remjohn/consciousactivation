from __future__ import annotations
from ccp_studio.contracts.carousel_engine import *
from ccp_studio.repositories.carousel_engine import InMemoryCarouselEngineRepository
from ccp_studio.services.carousel_eval_service import CarouselEvalService
from ccp_studio.services.carousel_render_service import CarouselRenderService

class CarouselEngineService:
    def __init__(self, repository=None, render_service=None, eval_service=None):
        self.repository = repository or InMemoryCarouselEngineRepository()
        self.render_service = render_service or CarouselRenderService()
        self.eval_service = eval_service or CarouselEvalService()

    def _save(self, store, obj, attr):
        return self.repository.upsert(store, getattr(obj, attr), obj)

    def create_project(self, *, brand_id, brand_context_version_id, source_context_refs, primitive_coalition_contract_id=None):
        p = CarouselProject(brand_id=brand_id, brand_context_version_id=brand_context_version_id, source_context_refs=source_context_refs, primitive_coalition_contract_id=primitive_coalition_contract_id, status=CarouselProjectStatus.ACTIVE)
        return self._save("projects", p, "carousel_project_id")

    def create_variant(self, *, project: CarouselProject, frame_profile="4:5_CAROUSEL_SLIDE"):
        v = CarouselVariant(carousel_project_id=project.carousel_project_id, brand_id=project.brand_id, brand_context_version_id=project.brand_context_version_id, frame_profile=frame_profile)
        project.variant_ids.append(v.carousel_variant_id)
        self._save("projects", project, "carousel_project_id")
        return self._save("variants", v, "carousel_variant_id")

    def create_variant_from_format_adapter_input(self, adapter_input):
        from ccp_studio.services.carousel_format_draft_wiring_service import CarouselFormatDraftWiringService

        return CarouselFormatDraftWiringService().create_variant_from_format_adapter_input(adapter_input)

    def compile_source_packet(self, project: CarouselProject, claim_texts=None):
        claim_texts = claim_texts or ["Source-backed insight", "Proof comes from workflow", "The sequence makes it saveable"]
        claims = [CarouselSourceClaim(claim_text=t, source_refs=[SourceRef(source_kind="source_context", source_id=project.source_context_refs[0], quote=t)]) for t in claim_texts]
        packet = CarouselSourcePacket(brand_id=project.brand_id, brand_context_version_id=project.brand_context_version_id, source_context_refs=project.source_context_refs, candidate_claims=claims, proof_points=["workflow proof"], examples=["operator cockpit"], frameworks=["context → sequence → proof"])
        return self._save("source_packets", packet, "carousel_source_packet_id")

    def compile_sequence_strategy(self, *, source_packet: CarouselSourcePacket, slide_count_range=(5,7), primitive_coalition_contract_id=None, complexity="standard", preproduction_depth="standard"):
        s = CarouselSequenceStrategy(
            brand_id=source_packet.brand_id, brand_context_version_id=source_packet.brand_context_version_id,
            source_packet_id=source_packet.carousel_source_packet_id, primitive_coalition_contract_id=primitive_coalition_contract_id,
            carousel_objective="Turn source truth into a saveable multi-slide argument.",
            audience_state_before="curious but unconvinced", audience_state_after="clear and ready to save",
            viewer_state_sequence=[ViewerState.PERCEPTUAL_ENTRY, ViewerState.RELEVANT_OPEN_QUESTION, ViewerState.ACTIVE_PREDICTION, ViewerState.TRUTHFUL_PAYOFF, ViewerState.EXPECTED_FUTURE_VALUE],
            narrative_arc="hook → problem → reframe → proof → mechanism → save",
            slide_count_range=slide_count_range, claim_policy="source-backed", visual_rhythm_policy="alternating dense/spacious", saveability_strategy="save card", cta_strategy="soft CTA", complexity=complexity, preproduction_depth=preproduction_depth)
        return self._save("sequence_strategies", s, "sequence_strategy_id")

    def plan_viewer_state_sequence(self, strategy, slide_count):
        states = list(strategy.viewer_state_sequence)
        seq = CarouselViewerStateSequence(sequence_strategy_id=strategy.sequence_strategy_id, states=states, slide_state_map={i: states[min(i-1, len(states)-1)] for i in range(1, slide_count+1)})
        return self._save("viewer_sequences", seq, "viewer_state_sequence_id")

    def route_slide_count(self, strategy, preferred_count=None):
        mn, mx = strategy.slide_count_range
        count = preferred_count or min(max(mn, 6), mx)
        d = CarouselSlideCountDecision(sequence_strategy_id=strategy.sequence_strategy_id, slide_count=count, rationale="V1 deterministic route")
        return self._save("slide_count_decisions", d, "slide_count_decision_id")

    def compile_slide_role_plan(self, strategy, count_decision):
        base = [SlideRole.COVER_HOOK, SlideRole.CONTEXT_SETUP, SlideRole.PROBLEM_FRAME, SlideRole.REFRAME_SLIDE, SlideRole.PROOF_SLIDE, SlideRole.MECHANISM_SLIDE, SlideRole.SAVE_CARD, SlideRole.CTA_SLIDE][:count_decision.slide_count]
        roles = [CarouselSlideRoleSpec(slide_index=i, slide_role=r, viewer_state_target=strategy.viewer_state_sequence[min(i-1, len(strategy.viewer_state_sequence)-1)], source_claim_requirement="source-backed", visual_function=f"{r.value} visual", copy_function=f"{r.value} copy", asset_requirement="proof_object" if r == SlideRole.PROOF_SLIDE else None) for i, r in enumerate(base, start=1)]
        plan = CarouselSlideRolePlan(sequence_strategy_id=strategy.sequence_strategy_id, slide_roles=roles)
        return self._save("slide_role_plans", plan, "slide_role_plan_id")

    def validate_narrative_arc(self, role_plan):
        blockers = []
        role_values = [role.slide_role for role in role_plan.slide_roles]
        if SlideRole.COVER_HOOK not in role_values:
            blockers.append("missing_cover_hook")
        if not any(role in role_values for role in {SlideRole.PROOF_SLIDE, SlideRole.MECHANISM_SLIDE, SlideRole.FRAMEWORK_SLIDE}):
            blockers.append("missing_source_payoff")
        report = CarouselNarrativeArcReport(
            slide_role_plan_id=role_plan.slide_role_plan_id,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )
        return self._save("sequence_audits", report, "narrative_arc_report_id")

    def compile_claim_map(self, source_packet, role_plan):
        entries = []
        for role in role_plan.slide_roles:
            if role.slide_role in {SlideRole.COVER_HOOK, SlideRole.CTA_SLIDE}: continue
            claim = source_packet.candidate_claims[min(len(entries), len(source_packet.candidate_claims)-1)]
            entries.append(CarouselClaimMapEntry(slide_index=role.slide_index, claim=claim.claim_text, source_ref_ids=[r.source_ref_id for r in claim.source_refs], supporting_quote=claim.source_refs[0].quote))
        cm = CarouselClaimMap(source_packet_id=source_packet.carousel_source_packet_id, entries=entries)
        return self._save("claim_maps", cm, "claim_map_id")

    def compile_copy_system(self, *, brand_id, brand_context_version_id, frame_profile):
        cs = CarouselCopySystem(brand_id=brand_id, brand_context_version_id=brand_context_version_id, frame_profile=frame_profile)
        return self._save("copy_systems", cs, "copy_system_id")

    def compile_slide_briefs(self, role_plan, claim_map):
        claims = {e.slide_index: e for e in claim_map.entries}
        out = []
        for role in role_plan.slide_roles:
            claim = claims.get(role.slide_index)
            b = CarouselSlideBrief(slide_index=role.slide_index, slide_role=role.slide_role, headline_intent=f"{role.slide_role.value} headline", source_claim_refs=[claim.claim] if claim else [], non_claim_function=claim is None, visual_directive=role.visual_function, asset_needs=[role.asset_requirement] if role.asset_requirement else [])
            self._save("slide_briefs", b, "slide_brief_id")
            out.append(b)
        return out

    def compile_slide_copy(self, brief, copy_system):
        packet = CarouselSlideCopyPacket(slide_index=brief.slide_index, headline=brief.headline_intent[:copy_system.headline_char_budget], support_line="Source-backed support." if brief.source_claim_refs else "Non-claim transition.")
        return self._save("slide_copy_packets", packet, "slide_copy_packet_id")

    def compile_asset_requirement_plan(self, variant, briefs):
        reqs = [CarouselAssetRequirement(slide_index=b.slide_index, role=n, semantic_need=f"{n} for slide {b.slide_index}") for b in briefs for n in b.asset_needs] or [CarouselAssetRequirement(role="sequence_motif", semantic_need="shared visual motif")]
        plan = CarouselAssetRequirementPlan(carousel_variant_id=variant.carousel_variant_id, requirements=reqs)
        return self._save("asset_requirement_plans", plan, "asset_requirement_plan_id")

    def plan_asset_allocation(self, variant, requirement_plan):
        bindings = [CarouselAssetCandidateBinding(slide_index=req.slide_index or 1, asset_id=f"asset_{req.role}_{req.slide_index or 'sequence'}", rights_status="provenance_ready") for req in requirement_plan.requirements]
        plan = CarouselAssetAllocationPlan(carousel_variant_id=variant.carousel_variant_id, bindings=bindings)
        return self._save("asset_allocation_plans", plan, "asset_allocation_plan_id")

    def lock_visual_system(self, variant):
        system = CarouselVisualSystem(carousel_variant_id=variant.carousel_variant_id, motif_system="source-backed proof motif", background_system="editorial card background", type_scale="mobile-readable", color_policy="brand-safe contrast", slide_numbering_policy="subtle", spacing_rhythm="dense/spacious alternating", cross_slide_continuity="shared motif and type")
        variant.status = CarouselVariantStatus.VISUAL_SYSTEM_LOCKED
        self._save("variants", variant, "carousel_variant_id")
        return self._save("visual_systems", system, "visual_system_id")

    def compile_style_route_policy(self, variant, slide_count):
        assignments = [CarouselStyleRouteAssignment(slide_index=i, primary_style_route="PAPER_CUT_EDITORIAL" if i != slide_count else "DETERMINISTIC_SKIA_CARD", allowed_route_family="paper_cut") for i in range(1, slide_count+1)]
        policy = CarouselStyleRoutePolicy(carousel_variant_id=variant.carousel_variant_id, assignments=assignments)
        return self._save("style_route_policies", policy, "style_route_policy_id")

    def generate_slide_composition_hypotheses(self, visual_system, briefs):
        if not visual_system.locked: raise ValueError("No slide composition before visual system lock")
        out = []
        for b in briefs:
            h = CarouselSlideCompositionHypothesis(slide_index=b.slide_index, attention_path="headline → visual → support", copy_placement="top-left", asset_placement="center", negative_space="30%")
            self._save("composition_hypotheses", h, "composition_hypothesis_id")
            out.append(h)
        return out

    def lock_slide_compositions(self, hypotheses):
        out = []
        for h in hypotheses:
            d = CarouselSlideCompositionDecision(slide_index=h.slide_index, selected_hypothesis_id=h.composition_hypothesis_id)
            self._save("composition_decisions", d, "composition_decision_id")
            out.append(d)
        return out

    def audit_sequence_composition(self, variant, decisions, hypotheses):
        blockers = []
        decision_indexes = [decision.slide_index for decision in decisions]
        if decision_indexes != list(range(1, len(decision_indexes) + 1)):
            blockers.append("composition_indexes_not_continuous")
        if any(h.mobile_readability_risk for h in hypotheses):
            blockers.append("mobile_readability_risk")
        audit = CarouselSequenceCompositionAudit(
            carousel_variant_id=variant.carousel_variant_id,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )
        return self._save("sequence_audits", audit, "sequence_composition_audit_id")

    def compile_slide_layer_plans(self, decisions, copy_packets):
        copy_by_slide = {p.slide_index: p for p in copy_packets}
        plans = []
        for d in decisions:
            layers = [
                CarouselLayerSpec(slide_index=d.slide_index, layer_role="background", asset_sha256=f"bg_hash_{d.slide_index}"),
                CarouselLayerSpec(slide_index=d.slide_index, layer_role="headline", text_ref=getattr(copy_by_slide.get(d.slide_index), "slide_copy_packet_id", None)),
                CarouselLayerSpec(slide_index=d.slide_index, layer_role="proof_object", materialization_mode=MatMode.PROVIDER_MATERIALIZED, asset_id=f"asset_slide_{d.slide_index}", asset_sha256=f"hash_slide_{d.slide_index}"),
            ]
            plan = CarouselSlideLayerPlan(slide_index=d.slide_index, composition_decision_id=d.composition_decision_id, layers=layers)
            self._save("layer_plans", plan, "slide_layer_plan_id")
            plans.append(plan)
        return plans

    def compile_provider_blueprints(self, *, layer_plans, decisions, frame_profile, style_route_policy=None):
        if not decisions: raise ValueError("No provider blueprint before composition lock")
        locked = {d.slide_index: d for d in decisions if d.locked}
        route_by_slide = {a.slide_index: a.primary_style_route for a in (style_route_policy.assignments if style_route_policy else [])}
        out = []
        for plan in layer_plans:
            if plan.slide_index not in locked: raise ValueError("Provider blueprints require locked compositions")
            for layer in plan.layers:
                if layer.materialization_mode == MatMode.PROVIDER_MATERIALIZED:
                    b = CarouselProviderJobBlueprint(slide_index=plan.slide_index, source_refs=[layer.asset_id], primary_style_route=route_by_slide.get(plan.slide_index, "PAPER_CUT_EDITORIAL"), frame_profile=frame_profile, composition_role=layer.layer_role, composition_decision_id=locked[plan.slide_index].composition_decision_id, prompt_contract=f"Materialize {layer.layer_role}")
                    self._save("provider_blueprints", b, "provider_job_blueprint_id")
                    out.append(b)
        return out

    def compile_render_batch_contract(self, variant, layer_plans):
        hashes = [l.asset_sha256 for p in layer_plans for l in p.layers if l.asset_sha256]
        c = CarouselRenderBatchContract(carousel_variant_id=variant.carousel_variant_id, frame_profile=variant.frame_profile, slide_count=len(layer_plans), slide_layer_plan_ids=[p.slide_layer_plan_id for p in layer_plans], required_asset_hashes=hashes, font_refs=["brand_font"])
        variant.slide_count = len(layer_plans); variant.render_batch_contract_id = c.render_batch_contract_id; variant.status = CarouselVariantStatus.RENDER_READY
        self._save("variants", variant, "carousel_variant_id")
        return self._save("render_contracts", c, "render_batch_contract_id")

    def render_batch(self, contract):
        receipts, preview = self.render_service.render_batch(contract)
        for r in receipts: self._save("render_receipts", r, "slide_render_receipt_id")
        return receipts, preview

    def run_eval(self, variant, **kwargs):
        r = self.eval_service.run_sequence_eval(carousel_variant_id=variant.carousel_variant_id, **kwargs)
        variant.evaluation_receipt_id = r.sequence_evaluation_receipt_id
        variant.status = CarouselVariantStatus.EVALUATED if r.pass_status == PassStatus.PASS else CarouselVariantStatus.REVISION_REQUIRED
        self._save("variants", variant, "carousel_variant_id")
        return self._save("eval_receipts", r, "sequence_evaluation_receipt_id")

    def apply_revision(self, variant, feedback: str):
        lower = feedback.lower(); cmds = []
        if "unsupported claim" in lower or "remove claim" in lower: cmds.append(CarouselRevisionCommand(command_type=RevisionCommandType.REMOVE_UNSUPPORTED_CLAIM))
        if "negative space" in lower: cmds.append(CarouselRevisionCommand(command_type=RevisionCommandType.INCREASE_NEGATIVE_SPACE))
        if "split" in lower: cmds.append(CarouselRevisionCommand(command_type=RevisionCommandType.SPLIT_DENSE_SLIDE))
        if "editorial" in lower: cmds.append(CarouselRevisionCommand(command_type=RevisionCommandType.MAKE_MORE_EDITORIAL))
        if not cmds: cmds.append(CarouselRevisionCommand(command_type=RevisionCommandType.CHANGE_SLIDE_HEADLINE, payload={"feedback": feedback}))
        rec = CarouselRevisionReceipt(carousel_variant_id=variant.carousel_variant_id, commands=cmds)
        return self._save("revision_receipts", rec, "carousel_revision_receipt_id")

    def compare_variants(self, baseline_variant, candidate_variant, baseline_eval=None, candidate_eval=None):
        source_delta = 0.0
        cohesion_delta = 0.0
        readability_delta = 0.0
        style_delta = 0.0
        if baseline_eval and candidate_eval:
            source_delta = candidate_eval.source_fidelity - baseline_eval.source_fidelity
            cohesion_delta = candidate_eval.sequence_cohesion - baseline_eval.sequence_cohesion
            readability_delta = candidate_eval.mobile_readability - baseline_eval.mobile_readability
            style_delta = candidate_eval.style_route_purity - baseline_eval.style_route_purity
        preferred = candidate_variant.carousel_variant_id if (source_delta + cohesion_delta + readability_delta + style_delta) >= 0 else baseline_variant.carousel_variant_id
        report = CarouselVariantComparisonReport(
            baseline_variant_id=baseline_variant.carousel_variant_id,
            candidate_variant_id=candidate_variant.carousel_variant_id,
            preferred_variant_id=preferred,
            source_fidelity_delta=source_delta,
            sequence_cohesion_delta=cohesion_delta,
            mobile_readability_delta=readability_delta,
            style_route_purity_delta=style_delta,
        )
        return self._save("variant_comparison_reports", report, "carousel_variant_comparison_report_id")

    def compile_export_pack(self, variant, render_receipts, approval_status="approved"):
        pack = CarouselExportPack(carousel_variant_id=variant.carousel_variant_id, approval_status=approval_status, slide_image_uris=[r.output_uri for r in render_receipts], alt_text=[f"Carousel slide {r.slide_index}" for r in render_receipts], posting_order=[r.slide_index for r in render_receipts], caption_seed="Source-backed caption seed")
        variant.export_pack_id = pack.carousel_export_pack_id; variant.status = CarouselVariantStatus.EXPORTED
        self._save("variants", variant, "carousel_variant_id")
        return self._save("export_packs", pack, "carousel_export_pack_id")

    def prepare_approval(self, variant, export_pack):
        if not variant.evaluation_receipt_id: raise ValueError("Carousel approval requires evaluation receipt")
        packet = CarouselApprovalPacket(carousel_variant_id=variant.carousel_variant_id, evaluation_receipt_id=variant.evaluation_receipt_id, export_pack_id=export_pack.carousel_export_pack_id, summary="Ready for review")
        return self._save("approval_packets", packet, "carousel_approval_packet_id")
