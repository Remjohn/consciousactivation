from ccp_studio.contracts.narrative_format_bridge import NarrativeToFormatBridgeRequest
from ccp_studio.contracts.narrative_story_doctor import (
    ArollStorySpine,
    BrollForeshadowingPair,
    CarouselExtractionPacket,
    CarouselSlideSeed,
    CutQuestionContract,
    EmotionalChangeMap,
    Format01StoryExtractionPacket,
    Format02ExplainerExtractionPacket,
    Format03ReactionExtractionPacket,
    Format04ConsciousReactionExtractionPacket,
    MemeVisualExtractionPacket,
    PollVisualExtractionPacket,
    PowerPhrasePlan,
    ReactionSeedPacket,
    RhythmPriorityMap,
    SonicStoryArcSeed,
    SuperVisualExtractionPacket,
    ViewerStateFunction,
)
from ccp_studio.contracts.format_intelligence import EngineTarget, FormatId
from ccp_studio.services.narrative_to_format_bridge_service import NarrativeToFormatBridgeService


def test_format01_packet_maps_and_compiles_to_format01_program():
    bridge = NarrativeToFormatBridgeService()
    spine = ArollStorySpine(source_span_refs=["span_1"], spine_lines=["I built a life with no recovery margins."])
    packet = Format01StoryExtractionPacket(
        sub_format="relief_peak_story",
        aroll_story_spine=spine,
        emotional_change_map=EmotionalChangeMap(before_state="old", truthful_payoff="truth", after_state="new"),
        cut_question_chain=[CutQuestionContract(cut_index=1, raises="where", answers="truth", feeling="recognition", tempo="slow", source_span_refs=["span_1"])],
        broll_foreshadowing_pairs=[BrollForeshadowingPair(before_visual="clean planner", after_visual="marked planner", change_function="pressure revealed")],
        rhythm_priority_map=RhythmPriorityMap(priorities_by_scene={"truth": "emotion"}),
        power_phrase_plan=PowerPhrasePlan(phrases=["No recovery margins."]),
        sonic_story_arc_seed=SonicStoryArcSeed(),
        memory_object_candidates=["planner"],
    )
    ref = bridge.ref_from_format01(packet)
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[ref])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"
    assert receipt.engine_adapter_payloads[0].engine_target == EngineTarget.VIDEO_EDITING_ENGINE


def test_format02_packet_maps_to_avatar_papercut_program():
    bridge = NarrativeToFormatBridgeService()
    packet = Format02ExplainerExtractionPacket(
        sub_format="scene_to_principle",
        teachable_mechanism="capacity needs recovery margin",
        source_span_refs=["span_1"],
        concept_nodes=["capacity", "recovery"],
        diagram_sequence=["fill", "collapse", "reframe"],
        avatar_performance_requirements=["point"],
    )
    ref = bridge.ref_from_format02(packet)
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[ref])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"


def test_format03_packet_maps_to_living_commentary_program():
    bridge = NarrativeToFormatBridgeService()
    packet = Format03ReactionExtractionPacket(
        sub_format="quote_commentary_reaction",
        proof_or_quote_surface="I built a life with no recovery margins.",
        source_span_refs=["span_1"],
        coach_reaction_angle="recognition",
        rough_notation_targets=["no recovery margins"],
    )
    ref = bridge.ref_from_format03(packet)
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[ref])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"


def test_format04_packet_maps_to_conscious_reaction_program():
    bridge = NarrativeToFormatBridgeService()
    packet = Format04ConsciousReactionExtractionPacket(
        sub_format="myth_debunk_reaction",
        debate_tension="weakness vs system design",
        source_span_refs=["span_1"],
        reaction_ui_surface="this_vs_that",
        score_state_seed="myth_break",
        meme_mechanism="micro_contradiction",
    )
    ref = bridge.ref_from_format04(packet)
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[ref])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"


def test_supervisual_packet_maps_to_supervisual_format_program():
    bridge = NarrativeToFormatBridgeService()
    packet = SuperVisualExtractionPacket(
        single_source_truth="I built a life with no recovery margins.",
        visual_hook_candidate="A planner so full it becomes evidence.",
        edge_product="Capacity without recovery is extraction.",
        source_span_refs=["span_1"],
        memory_object_candidate="planner",
    )
    ref = bridge.ref_from_supervisual(packet)
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[ref])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"
    assert receipt.engine_adapter_payloads[0].engine_target == EngineTarget.SUPERVISUAL_ENGINE


def test_carousel_packet_maps_to_carousel_format_program():
    bridge = NarrativeToFormatBridgeService()
    packet = CarouselExtractionPacket(
        carousel_thesis="Burnout is not always weakness.",
        source_span_refs=["span_1"],
        viewer_state_sequence=[ViewerStateFunction.PERCEPTUAL_ENTRY, ViewerStateFunction.TRUTHFUL_PAYOFF],
        slides=[
            CarouselSlideSeed(slide_index=1, role="cover", slide_copy="What if burnout was not weakness?", source_ref="span_1"),
            CarouselSlideSeed(slide_index=2, role="payoff", slide_copy="No recovery margins.", source_ref="span_1"),
        ],
        open_loop="What if?",
        closure_contract="Source-faithful reframe.",
    )
    ref = bridge.ref_from_carousel(packet)
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[ref])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"
    assert receipt.engine_adapter_payloads[0].engine_target == EngineTarget.CAROUSEL_ENGINE


def test_meme_poll_reaction_seed_packets_map():
    bridge = NarrativeToFormatBridgeService()
    meme = bridge.ref_from_meme(MemeVisualExtractionPacket(
        sub_format="micro_contradiction",
        source_truth="calendar says reliable",
        compressed_paradox="nervous system says hostage",
        meme_mechanism="micro_contradiction",
        source_span_refs=["span_1"],
    ))
    poll = bridge.ref_from_poll(PollVisualExtractionPacket(
        sub_format="tension_poll",
        question="Is burnout weakness or no margin?",
        options=["Weakness", "No margin"],
        source_span_refs=["span_1"],
    ))
    reaction = bridge.ref_from_reaction_seed(ReactionSeedPacket(
        source_quote="No recovery margins.",
        source_span_refs=["span_1"],
        reaction_question="React?",
        compatible_reaction_formats=["Validation Reaction"],
    ))
    request = NarrativeToFormatBridgeRequest(brand_id="brand_1", brand_context_version_id="bcv_1", packet_refs=[meme, poll, reaction])
    receipt = bridge.compile_batch(request)
    assert receipt.status == "adapted"
    assert len(receipt.engine_adapter_payloads) == 3


def test_bridge_fails_without_source_refs():
    bridge = NarrativeToFormatBridgeService()
    try:
        SuperVisualExtractionPacket(
            single_source_truth="truth",
            visual_hook_candidate="hook",
            edge_product="edge",
            source_span_refs=[],
        )
    except Exception as exc:
        assert "source_span_refs" in str(exc)
