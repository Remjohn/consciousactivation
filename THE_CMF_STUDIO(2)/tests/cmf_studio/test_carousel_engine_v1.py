import pytest
from ccp_studio.contracts.carousel_engine import *
from ccp_studio.services.carousel_engine_service import CarouselEngineService

def test_carousel_project_requires_brand_context_version():
    with pytest.raises(Exception):
        CarouselProject(brand_id="b", brand_context_version_id="", source_context_refs=["s"])

def test_carousel_source_packet_claims_require_source_refs():
    with pytest.raises(Exception):
        CarouselSourceClaim(claim_text="unsupported", claim_type=ClaimType.FACTUAL)

def test_sequence_strategy_requires_audience_state_transition():
    with pytest.raises(Exception):
        CarouselSequenceStrategy(brand_id="b", brand_context_version_id="v", source_packet_id="s", carousel_objective="teach", audience_state_before="", audience_state_after="clear", viewer_state_sequence=[ViewerState.PERCEPTUAL_ENTRY], narrative_arc="arc", slide_count_range=(5,7), claim_policy="source", visual_rhythm_policy="alt", saveability_strategy="save", cta_strategy="soft")

def test_slide_count_range_rejects_empty_or_excessive_count():
    with pytest.raises(Exception):
        CarouselSlideCountDecision(sequence_strategy_id="s", slide_count=0, rationale="bad")
    with pytest.raises(Exception):
        CarouselSlideCountDecision(sequence_strategy_id="s", slide_count=13, rationale="bad")

def test_slide_role_plan_has_continuous_slide_indexes():
    with pytest.raises(Exception):
        CarouselSlideRolePlan(sequence_strategy_id="s", slide_roles=[
            CarouselSlideRoleSpec(slide_index=1, slide_role=SlideRole.COVER_HOOK, viewer_state_target=ViewerState.PERCEPTUAL_ENTRY, visual_function="v", copy_function="c"),
            CarouselSlideRoleSpec(slide_index=3, slide_role=SlideRole.PROOF_SLIDE, viewer_state_target=ViewerState.TRUTHFUL_PAYOFF, visual_function="v", copy_function="c"),
        ])

def test_each_slide_has_unique_role_or_declared_repeat_reason():
    with pytest.raises(Exception):
        CarouselSlideRolePlan(sequence_strategy_id="s", slide_roles=[
            CarouselSlideRoleSpec(slide_index=1, slide_role=SlideRole.PROOF_SLIDE, viewer_state_target=ViewerState.TRUTHFUL_PAYOFF, visual_function="v", copy_function="c"),
            CarouselSlideRoleSpec(slide_index=2, slide_role=SlideRole.PROOF_SLIDE, viewer_state_target=ViewerState.TRUTHFUL_PAYOFF, visual_function="v", copy_function="c"),
        ])

def test_claim_map_blocks_unsupported_factual_claim():
    with pytest.raises(Exception):
        CarouselClaimMapEntry(slide_index=1, claim="unsupported", claim_type=ClaimType.FACTUAL)

def test_copy_packet_obeys_frame_profile_text_budget():
    with pytest.raises(Exception):
        CarouselSlideCopyPacket(slide_index=1, headline="x"*80, headline_char_budget=20)

def test_visual_preproduction_full_batch_required_for_complex_carousel():
    with pytest.raises(Exception):
        CarouselSequenceStrategy(brand_id="b", brand_context_version_id="v", source_packet_id="s", carousel_objective="teach", audience_state_before="before", audience_state_after="after", viewer_state_sequence=[ViewerState.PERCEPTUAL_ENTRY], narrative_arc="arc", slide_count_range=(5,7), claim_policy="source", visual_rhythm_policy="alt", saveability_strategy="save", cta_strategy="soft", complexity="complex", preproduction_depth="standard")

def test_asset_allocation_excludes_blocked_assets():
    with pytest.raises(Exception):
        CarouselAssetAllocationPlan(carousel_variant_id="v", bindings=[CarouselAssetCandidateBinding(slide_index=1, asset_id="a", blocked=True)])

def test_visual_system_locks_before_slide_composition():
    service = CarouselEngineService()
    p = service.create_project(brand_id="b", brand_context_version_id="v", source_context_refs=["s"])
    v = service.create_variant(project=p)
    sys = service.lock_visual_system(v)
    sys.locked = False
    with pytest.raises(Exception):
        service.generate_slide_composition_hypotheses(sys, [])

def test_style_route_policy_rejects_route_averaging():
    with pytest.raises(Exception):
        CarouselStyleRoutePolicy(carousel_variant_id="v", assignments=[CarouselStyleRouteAssignment(slide_index=1, primary_style_route="CAC+GMG")])

def test_slide_composition_lock_required_before_provider_blueprints():
    service = CarouselEngineService()
    with pytest.raises(Exception):
        service.compile_provider_blueprints(layer_plans=[], decisions=[], frame_profile="4:5_CAROUSEL_SLIDE")

def test_provider_blueprints_have_source_refs_style_route_frame_profile_composition_role():
    service = CarouselEngineService()
    decision = CarouselSlideCompositionDecision(slide_index=1, selected_hypothesis_id="h")
    layer = CarouselLayerSpec(slide_index=1, layer_role="proof_object", materialization_mode=MatMode.PROVIDER_MATERIALIZED, asset_id="asset_1", asset_sha256="hash_1")
    plan = CarouselSlideLayerPlan(slide_index=1, composition_decision_id=decision.composition_decision_id, layers=[layer])
    b = service.compile_provider_blueprints(layer_plans=[plan], decisions=[decision], frame_profile="4:5_CAROUSEL_SLIDE")[0]
    assert b.source_refs and b.primary_style_route and b.frame_profile and b.composition_role

def test_narrative_arc_validation_requires_hook_and_payoff():
    service = CarouselEngineService()
    role_plan = CarouselSlideRolePlan(sequence_strategy_id="s", slide_roles=[
        CarouselSlideRoleSpec(slide_index=1, slide_role=SlideRole.CONTEXT_SETUP, viewer_state_target=ViewerState.PERCEPTUAL_ENTRY, visual_function="v", copy_function="c"),
        CarouselSlideRoleSpec(slide_index=2, slide_role=SlideRole.SAVE_CARD, viewer_state_target=ViewerState.EXPECTED_FUTURE_VALUE, visual_function="v", copy_function="c"),
    ])
    report = service.validate_narrative_arc(role_plan)
    assert report.pass_status == PassStatus.FAIL
    assert "missing_cover_hook" in report.blockers
    assert "missing_source_payoff" in report.blockers

def test_sequence_composition_audit_blocks_mobile_readability_risk():
    service = CarouselEngineService()
    p = service.create_project(brand_id="b", brand_context_version_id="v", source_context_refs=["s"])
    v = service.create_variant(project=p)
    hypothesis = CarouselSlideCompositionHypothesis(
        slide_index=1,
        attention_path="headline to proof",
        copy_placement="top",
        asset_placement="center",
        negative_space="low",
        mobile_readability_risk=True,
    )
    decision = CarouselSlideCompositionDecision(slide_index=1, selected_hypothesis_id=hypothesis.composition_hypothesis_id)
    audit = service.audit_sequence_composition(v, [decision], [hypothesis])
    assert audit.pass_status == PassStatus.FAIL
    assert "mobile_readability_risk" in audit.blockers

def test_render_batch_contract_requires_asset_hashes():
    with pytest.raises(Exception):
        CarouselRenderBatchContract(carousel_variant_id="v", frame_profile="4:5_CAROUSEL_SLIDE", slide_count=1, slide_layer_plan_ids=["lp"], required_asset_hashes=[])

def test_16_9_rejected_as_carousel_delivery():
    with pytest.raises(Exception):
        CarouselVariant(carousel_project_id="p", brand_id="b", brand_context_version_id="v", frame_profile="16:9_SOURCE_INTERVIEW")

def test_sequence_eval_blocks_unsupported_claim_and_mobile_readability():
    r = CarouselSequenceEvaluationReceipt(carousel_variant_id="v", claim_support=.2, mobile_readability=.2)
    assert r.pass_status == PassStatus.FAIL
    assert "unsupported_claim" in r.blockers
    assert "mobile_readability_failure" in r.blockers

def test_revision_feedback_compiles_to_typed_commands():
    service = CarouselEngineService()
    p = service.create_project(brand_id="b", brand_context_version_id="v", source_context_refs=["s"])
    v = service.create_variant(project=p)
    rec = service.apply_revision(v, "increase negative space and remove unsupported claim")
    types = {cmd.command_type for cmd in rec.commands}
    assert RevisionCommandType.INCREASE_NEGATIVE_SPACE in types
    assert RevisionCommandType.REMOVE_UNSUPPORTED_CLAIM in types

def test_variant_comparison_report_prefers_candidate_on_non_negative_delta():
    service = CarouselEngineService()
    p = service.create_project(brand_id="b", brand_context_version_id="v", source_context_refs=["s"])
    baseline = service.create_variant(project=p)
    candidate = service.create_variant(project=p)
    baseline_eval = CarouselSequenceEvaluationReceipt(carousel_variant_id=baseline.carousel_variant_id, sequence_cohesion=.7)
    candidate_eval = CarouselSequenceEvaluationReceipt(carousel_variant_id=candidate.carousel_variant_id, sequence_cohesion=.8)
    report = service.compare_variants(baseline, candidate, baseline_eval=baseline_eval, candidate_eval=candidate_eval)
    assert report.preferred_variant_id == candidate.carousel_variant_id
    assert report.sequence_cohesion_delta > 0

def test_export_pack_requires_approved_variant():
    with pytest.raises(Exception):
        CarouselExportPack(carousel_variant_id="v", approval_status="draft", slide_image_uris=["1.png"], alt_text=["1"], posting_order=[1])

def test_fake_end_to_end_carousel_build_path():
    service = CarouselEngineService()
    p = service.create_project(brand_id="b", brand_context_version_id="v", source_context_refs=["s"])
    v = service.create_variant(project=p)
    source = service.compile_source_packet(p)
    strategy = service.compile_sequence_strategy(source_packet=source)
    count = service.route_slide_count(strategy)
    roles = service.compile_slide_role_plan(strategy, count)
    claims = service.compile_claim_map(source, roles)
    copy_system = service.compile_copy_system(brand_id=p.brand_id, brand_context_version_id=p.brand_context_version_id, frame_profile=v.frame_profile)
    briefs = service.compile_slide_briefs(roles, claims)
    copies = [service.compile_slide_copy(b, copy_system) for b in briefs]
    reqs = service.compile_asset_requirement_plan(v, briefs)
    service.plan_asset_allocation(v, reqs)
    visual = service.lock_visual_system(v)
    hypos = service.generate_slide_composition_hypotheses(visual, briefs)
    decisions = service.lock_slide_compositions(hypos)
    layers = service.compile_slide_layer_plans(decisions, copies)
    contract = service.compile_render_batch_contract(v, layers)
    receipts, preview = service.render_batch(contract)
    evalr = service.run_eval(v)
    export = service.compile_export_pack(v, receipts, approval_status="approved")
    approval = service.prepare_approval(v, export)
    assert len(receipts) == count.slide_count
    assert preview.slide_receipt_ids
    assert evalr.pass_status == PassStatus.PASS
    assert approval.approval_ready
