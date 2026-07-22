import pytest

from ccp_studio.contracts.format_intelligence import (
    EngineAdapterPayload,
    EngineTarget,
    FormatCommanderVerdict,
    FormatId,
    FormatIngredientType,
    FormatIntelligenceContext,
    FormatMemeticCuePolicy,
    FormatStyleRoutePolicy,
    FrameProfile,
    GenericExtractionPacketRef,
    PassStatus,
    PollVisualFormatProgram,
    StyleRoute,
)
from ccp_studio.services.format_intelligence_service import FormatIntelligenceService


def packet(target, payload=None, sub_format=None):
    return GenericExtractionPacketRef(
        extraction_packet_id=f"packet_{target.value}",
        target_format=target,
        sub_format_hint=sub_format,
        source_span_refs=["span_1"],
        payload=payload or {},
    )


def context():
    service = FormatIntelligenceService()
    return service.hydrate_context(brand_id="brand_1", brand_context_version_id="bcv_1")


def test_context_requires_brand_context_version():
    with pytest.raises(Exception):
        FormatIntelligenceContext(brand_id="brand_1", brand_context_version_id="")


def test_generic_extraction_packet_requires_source_refs():
    with pytest.raises(Exception):
        GenericExtractionPacketRef(extraction_packet_id="p1", target_format=FormatId.SUPERVISUAL, source_span_refs=[], payload={})


def test_format01_rejects_missing_aroll_story_spine():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.FORMAT_01_CINEMATIC_STORY, payload={
            "emotional_change_map": "change_1",
            "cut_question_chain": ["cut_1"],
            "sonic_story_arc_seed": "sound_1",
        }))


def test_format01_compiles_with_aroll_story_spine_and_cut_question_chain():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.FORMAT_01_CINEMATIC_STORY, payload={
        "a_roll_story_spine": "spine_1",
        "emotional_change_map": "change_1",
        "cut_question_chain": ["cut_1"],
        "sonic_story_arc_seed": "sound_1",
        "broll_foreshadowing_pairs": ["broll_pair_1"],
        "memory_object": "planner",
    }))
    assert program.format_id == FormatId.FORMAT_01_CINEMATIC_STORY
    assert program.broll_policy.forbid_filler
    assert program.sound_doctrine.memetic_policy.per_seconds == 30


def test_format02_rejects_missing_mechanism():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER, payload={
            "concept_nodes": ["a"],
            "diagram_sequence": "diagram_1",
        }))


def test_format02_compiles_avatar_paper_cut_policy():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER, payload={
        "teachable_mechanism": "mechanism_1",
        "concept_nodes": ["capacity", "recovery_margin"],
        "diagram_sequence": "diagram_1",
        "avatar_performance_requirements": ["point", "pause"],
    }))
    assert program.avatar_performance_policy.avatar_required
    assert StyleRoute.AVATAR_PERFORMANCE_LAYER in program.style_route_policy.primary_routes


def test_format03_rejects_missing_proof_surface():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS, payload={
            "coach_reaction_angle": "recognition",
        }))


def test_format03_compiles_reaction_surface_policy():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS, payload={
        "proof_or_quote_surface": "quote surface",
        "coach_reaction_angle": "quiet recognition",
        "rough_notation_targets": ["phrase_1"],
    }))
    assert program.reaction_surface_policy.reaction_surface_required
    assert program.proof_policy.proof_surface_required


def test_format04_rejects_missing_debate_tension():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING, payload={
            "reaction_ui_surface": "this_vs_that",
        }))


def test_format04_memetic_cue_policy_is_10_seconds():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING, payload={
        "debate_tension": "weakness vs bad system design",
        "reaction_ui_surface": "this_vs_that",
        "score_state_seed": "myth_break",
        "meme_mechanism": "micro_contradiction",
    }))
    assert program.sound_doctrine.memetic_policy.per_seconds == 10
    assert StyleRoute.UI_REACTION_SURFACE in program.style_route_policy.primary_routes


def test_memetic_policy_rejects_too_fast_format01_cues():
    with pytest.raises(Exception):
        FormatMemeticCuePolicy(format_id=FormatId.FORMAT_01_CINEMATIC_STORY, max_cues=1, per_seconds=10)


def test_supervisual_requires_single_source_truth():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.SUPERVISUAL, payload={
            "visual_hook": "hook",
            "edge_product": "edge",
        }))


def test_supervisual_compiles_single_source_truth():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.SUPERVISUAL, payload={
        "single_source_truth": "I built a life with no recovery margins.",
        "visual_hook": "A calendar so full it becomes evidence.",
        "edge_product": "Capacity without recovery is extraction.",
    }))
    assert program.single_source_truth_ref
    assert program.render_requirement.engine_target == EngineTarget.SUPERVISUAL_ENGINE


def test_carousel_requires_closure_contract():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.CAROUSEL, payload={
            "carousel_thesis": "Thesis",
            "viewer_state_sequence": ["entry"],
            "sequence_steps": [{"role": "cover", "viewer_state": "entry"}],
        }))


def test_carousel_compiles_sequence_grammar():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.CAROUSEL, payload={
        "carousel_thesis": "Burnout is not always weakness.",
        "viewer_state_sequence": ["entry", "payoff"],
        "closure_contract": "Source-faithful reframe",
        "sequence_steps": [
            {"role": "cover", "viewer_state": "perceptual_entry", "source_ref": "span_1"},
            {"role": "payoff", "viewer_state": "truthful_payoff", "source_ref": "span_1"},
        ],
    }))
    assert len(program.sequence_steps) == 2
    assert program.closure_contract_ref


def test_meme_requires_meme_mechanism():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.MEME_VISUAL, payload={
            "source_truth": "truth",
            "compressed_paradox": "paradox",
        }))


def test_poll_requires_two_options():
    service = FormatIntelligenceService()
    ctx = context()
    with pytest.raises(Exception):
        service.compile_format_program(ctx, packet(FormatId.POLL_VISUAL, payload={
            "question": "Question?",
            "options": ["one"],
        }))


def test_style_route_policy_rejects_forbidden_routes():
    policy = FormatStyleRoutePolicy(
        format_id=FormatId.FORMAT_01_CINEMATIC_STORY,
        primary_routes=[StyleRoute.CAC],
        forbidden_routes=[StyleRoute.UI_REACTION_SURFACE],
    )
    with pytest.raises(Exception):
        policy.validate_selected_routes([StyleRoute.CAC, StyleRoute.UI_REACTION_SURFACE])


def test_commander_blocks_missing_required_ingredients():
    service = FormatIntelligenceService()
    ctx = context()
    packet_ref = packet(FormatId.SUPERVISUAL, payload={
        "single_source_truth": "truth",
        "visual_hook": "hook",
        # edge_product missing
    })
    with pytest.raises(Exception):
        # Specialized SuperVisual program blocks first, so test checklist directly.
        service.compile_format_program(ctx, packet_ref)


def test_authorized_program_compiles_engine_adapter_payload():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.SUPERVISUAL, payload={
        "single_source_truth": "truth",
        "visual_hook": "hook",
        "edge_product": "edge",
    }))
    verdict = service.authorize_format_program(program)
    assert verdict.authorized
    payload = service.compile_engine_adapter_payload(program)
    assert payload.engine_target == EngineTarget.SUPERVISUAL_ENGINE
    assert payload.source_span_refs == ["span_1"]


def test_engine_adapter_payload_requires_authorized_program():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.SUPERVISUAL, payload={
        "single_source_truth": "truth",
        "visual_hook": "hook",
        "edge_product": "edge",
    }))
    with pytest.raises(Exception):
        service.compile_engine_adapter_payload(program)


def test_render_requirement_rejects_provider_calls_during_final_render():
    from ccp_studio.contracts.format_intelligence import FormatRenderRequirement
    with pytest.raises(Exception):
        FormatRenderRequirement(
            format_id=FormatId.SUPERVISUAL,
            frame_profile=FrameProfile.ONE_ONE_SOFT_ROUNDED,
            engine_target=EngineTarget.SUPERVISUAL_ENGINE,
            provider_calls_allowed_during_final_render=True,
        )


def test_reaction_seed_program_can_store_only():
    service = FormatIntelligenceService()
    ctx = context()
    program = service.compile_format_program(ctx, packet(FormatId.REACTION_SEED, payload={
        "source_quote": "quote",
        "reaction_question": "React?",
        "compatible_reaction_formats": ["Validation Reaction"],
    }))
    assert program.store_only
    verdict = service.authorize_format_program(program)
    assert verdict.authorized


def test_all_major_formats_compile_and_authorize():
    service = FormatIntelligenceService()
    ctx = context()
    packets = [
        packet(FormatId.FORMAT_01_CINEMATIC_STORY, {
            "a_roll_story_spine": "spine", "emotional_change_map": "change", "cut_question_chain": ["cut"], "sonic_story_arc_seed": "sound"
        }),
        packet(FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER, {
            "teachable_mechanism": "mechanism", "concept_nodes": ["a"], "diagram_sequence": "diagram"
        }),
        packet(FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS, {
            "proof_or_quote_surface": "proof", "coach_reaction_angle": "angle"
        }),
        packet(FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING, {
            "debate_tension": "tension", "reaction_ui_surface": "ui"
        }),
    ]
    for pkt in packets:
        program = service.compile_format_program(ctx, pkt)
        verdict = service.authorize_format_program(program)
        assert verdict.authorized
        adapter = service.compile_engine_adapter_payload(program)
        assert adapter.engine_target == EngineTarget.VIDEO_EDITING_ENGINE
