import pytest

from ccp_studio.contracts.narrative_story_doctor import (
    ArollStorySpine,
    AssetPackageCandidateSet,
    BrollForeshadowingPair,
    CoverageStatus,
    ExtractionMode,
    ExtractionTarget,
    Format02ExplainerExtractionPacket,
    Format03ReactionExtractionPacket,
    Format04ConsciousReactionExtractionPacket,
    IngredientType,
    LayerAwareExtractionContext,
    MemeVisualExtractionPacket,
    PollVisualExtractionPacket,
    QuestionProductionContract,
    ReactionSeedPacket,
    SourceFidelityReceipt,
    PassStatus,
)
from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


TRANSCRIPT = (
    "At the time, I thought being constantly available made me reliable. "
    "The week I burned out, my calendar was proof that I had confused capacity with worth. "
    "I didn't burn out because I was weak. "
    "I burned out because I built a life with no recovery margins."
)


def _brief():
    return {
        "interview_brief_id": "brief_1",
        "interview_objective": "capture transformation story ingredients",
        "target_archetypes": ["Transformation Story", "Witness Story", "Relief Peak"],
        "target_primitives": ["recognition", "integrity", "relief"],
        "target_expression_states": ["quiet_confession"],
        "target_content_formats": ["format_01_cinematic_story", "carousel_sequence", "supervisual_single_image"],
        "questions": [
            {
                "question_id": "q_017",
                "question_text": "What did that season cost you privately?",
                "target_archetypes": ["Transformation Story"],
                "target_expression_state": "quiet_confession",
                "first_line_anchor": "At the time, I thought...",
                "depth_anchor": "What did that belief cost you in a visible way?",
                "expected_ingredients": ["before_after_change", "emotional_pause", "memory_object", "source_quote"],
                "target_asset_routes": ["format_01_cinematic_story", "carousel_sequence", "supervisual_single_image"],
                "evaluation_logic": {"must_generate_source_material": True, "must_produce_strong_landing": True},
            }
        ],
    }


def _compiled():
    service = NarrativeStoryDoctorService()
    context = service.hydrate_context(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        extraction_mode=ExtractionMode.INTERVIEW_BRIEF_BOUND,
        interview_brief_id="brief_1",
    )
    binding = service.bind_interview_brief(context, _brief())
    graph = service.compile_expected_ingredient_graph(binding)
    source = service.normalize_source(
        transcript_text=TRANSCRIPT,
        mode=ExtractionMode.INTERVIEW_BRIEF_BOUND,
        source_id="interview_1",
        speaker="guest",
        question_id="q_017",
    )
    beat_map = service.compile_transcript_beat_map(source)
    expressions = service.extract_expression_moments(beat_map)
    clusters = service.compile_clusters(beat_map, source)
    cluster = clusters[0]
    meaning, experience, edge = service.compile_meaning_candidates(cluster)
    return service, context, binding, graph, source, beat_map, expressions, cluster, meaning, experience, edge


def test_story_doctor_run_requires_brand_context_version():
    with pytest.raises(Exception):
        LayerAwareExtractionContext(brand_id="brand_1", brand_context_version_id="")


def test_interview_brief_compiles_question_contracts():
    service = NarrativeStoryDoctorService()
    context = service.hydrate_context(brand_id="brand_1", brand_context_version_id="bcv_1")
    binding = service.bind_interview_brief(context, _brief())
    assert binding.question_contracts[0].target_expression_state == "quiet_confession"
    assert IngredientType.MEMORY_OBJECT in binding.question_contracts[0].expected_ingredients


def test_question_contract_defines_archetype_expression_anchors_routes_eval():
    contract = QuestionProductionContract(
        question_id="q1",
        question_text="What changed?",
        target_archetypes=["Transformation Story"],
        target_expression_state="quiet_confession",
        first_line_anchor="At the time...",
        depth_anchor="What did it cost?",
        expected_ingredients=[IngredientType.BEFORE_AFTER_CHANGE],
        target_asset_routes=[ExtractionTarget.FORMAT_01_CINEMATIC_STORY],
        evaluation_logic={"must_produce_strong_landing": True},
    )
    assert contract.first_line_anchor
    assert contract.depth_anchor
    assert contract.target_asset_routes[0] == ExtractionTarget.FORMAT_01_CINEMATIC_STORY


def test_expected_ingredient_graph_compiles_from_brief():
    service, context, binding, graph, *_ = _compiled()
    assert len(graph.nodes) == 4
    assert any(node.ingredient_type == IngredientType.MEMORY_OBJECT for node in graph.nodes)


def test_brief_biases_extraction_without_inventing_evidence():
    service, context, binding, graph, source, beat_map, expressions, cluster, meaning, experience, edge = _compiled()
    contract = binding.question_contracts[0]
    actual = [IngredientType.BEFORE_AFTER_CHANGE, IngredientType.EMOTIONAL_PAUSE, IngredientType.SOURCE_QUOTE]
    diff = service.compare_expected_actual(contract, actual)
    assert IngredientType.MEMORY_OBJECT in diff.misses
    assert IngredientType.MEMORY_OBJECT not in diff.hits


def test_raw_transcript_mode_marks_lower_confidence():
    service = NarrativeStoryDoctorService()
    source = service.normalize_source(transcript_text=TRANSCRIPT, mode=ExtractionMode.RAW_TRANSCRIPT)
    assert source.timing_confidence == "low"


def test_complete_expression_session_generates_multiple_editing_session_requests():
    service, _, _, _, _, _, _, cluster, _, _, _ = _compiled()
    reqs = service.compile_complete_editing_session_requests("xes_1", cluster)
    assert reqs[0].source_expression_session_id == "xes_1"
    assert reqs[0].source_span_refs


def test_cluster_compiler_preserves_verbatim_spans():
    service, _, _, _, source, beat_map, _, cluster, *_ = _compiled()
    assert cluster.source_span_ids == [source.spans[0].span_id]
    assert "recovery margins" in cluster.verbatim_anchor


def test_archetype_fit_matrix_scores_transformation_story_for_before_after_change():
    service, *_, cluster, meaning, experience, edge = _compiled()
    matrix = service.score_archetype_fit(cluster)
    names = {score.archetype for score in matrix.scores}
    assert "Transformation Story" in names
    assert "Relief Peak" in names


def test_primitive_coalition_compiler_emits_misuse_risk():
    service, *_, cluster, meaning, experience, edge = _compiled()
    primitive = service.compile_primitive_candidates(cluster, edge)
    coalition = service.compile_primitive_coalition(primitive)
    assert coalition.governing_primitives
    assert "self_care_cliche" in coalition.misuse_risks


def test_format01_packet_requires_story_change_and_aroll_spine():
    service, _, _, _, _, beat_map, _, cluster, _, _, edge = _compiled()
    packet = service.compile_format01_packet(cluster, beat_map, edge)
    assert packet.aroll_story_spine.spine_lines
    assert packet.cut_question_chain
    assert packet.emotional_change_map.truthful_payoff


def test_format02_packet_requires_teachable_mechanism():
    with pytest.raises(Exception):
        Format02ExplainerExtractionPacket(
            sub_format="bad",
            teachable_mechanism="",
            source_span_refs=["span_1"],
            concept_nodes=["a"],
            diagram_sequence=["b"],
        )


def test_format03_packet_requires_proof_object_or_quote_surface():
    with pytest.raises(Exception):
        Format03ReactionExtractionPacket(
            sub_format="bad",
            proof_or_quote_surface="",
            source_span_refs=["span_1"],
            coach_reaction_angle="angle",
        )


def test_format04_packet_requires_debate_or_ranking_tension():
    with pytest.raises(Exception):
        Format04ConsciousReactionExtractionPacket(
            sub_format="bad",
            debate_tension="",
            source_span_refs=["span_1"],
            reaction_ui_surface="this_vs_that",
        )


def test_supervisual_packet_extracts_single_source_truth():
    service, *_, cluster, meaning, experience, edge = _compiled()
    packet = service.compile_supervisual_packet(cluster, edge)
    assert packet.single_source_truth
    assert packet.source_span_refs
    assert packet.visual_hook_candidate


def test_carousel_packet_extracts_claim_sequence_and_closure_contract():
    service, *_, cluster, meaning, experience, edge = _compiled()
    packet = service.compile_carousel_packet(cluster, edge)
    assert packet.carousel_thesis
    assert packet.closure_contract
    assert packet.slides[0].slide_index == 1


def test_meme_packet_requires_micro_contradiction_or_humor_mechanism():
    with pytest.raises(Exception):
        MemeVisualExtractionPacket(
            sub_format="micro",
            source_truth="truth",
            compressed_paradox="paradox",
            meme_mechanism="",
            source_span_refs=["span_1"],
        )


def test_poll_packet_requires_meaningful_tension_options():
    with pytest.raises(Exception):
        PollVisualExtractionPacket(
            sub_format="poll",
            question="Choose",
            options=["only one"],
            source_span_refs=["span_1"],
        )


def test_reaction_seed_is_stored_even_if_not_produced():
    packet = ReactionSeedPacket(
        source_quote="quote",
        source_span_refs=["span_1"],
        reaction_question="React?",
        compatible_reaction_formats=["Validation Reaction"],
    )
    assert packet.status == "stored_for_future_use"


def test_question_coverage_receipt_records_hits_misses_unexpected_wins():
    service, context, binding, graph, source, beat_map, expressions, cluster, *_ = _compiled()
    contract = binding.question_contracts[0]
    actual = [
        IngredientType.BEFORE_AFTER_CHANGE,
        IngredientType.EMOTIONAL_PAUSE,
        IngredientType.SOURCE_QUOTE,
        IngredientType.POWER_PHRASE,
    ]
    diff = service.compare_expected_actual(contract, actual)
    receipt = service.compile_question_coverage(contract, diff, [source.spans[0].span_id])
    assert receipt.coverage_status == CoverageStatus.PARTIAL_HIT
    assert IngredientType.MEMORY_OBJECT in receipt.expected_ingredients_missing
    assert IngredientType.POWER_PHRASE in receipt.unexpected_high_value_ingredients


def test_followup_question_targets_missing_ingredient():
    service = NarrativeStoryDoctorService()
    gap = service.compile_gap_report([IngredientType.MEMORY_OBJECT], [])
    followups = service.compile_followup_questions(gap, "Witness Story")
    assert "physical object" in followups.questions[0].question_text


def test_extraction_commander_rejects_paraphrased_source_quote():
    service, _, _, _, source, *_ = _compiled()
    receipt = service.evaluate_source_fidelity(source.spans, generated_claims=["This exact invented claim is not in transcript"])
    assert receipt.pass_status == PassStatus.FAIL
    verdict = service.authorize_extraction(receipt)
    assert not verdict.authorized
    assert "source_fidelity_failed" in verdict.blockers


def test_asset_package_candidate_set_contains_4_videos_2_carousels_2_memes_2_polls_reaction_seeds():
    service = NarrativeStoryDoctorService()
    package = service.compile_asset_package_candidate_set(
        video_packet_ids=["v1", "v2", "v3", "v4"],
        carousel_packet_ids=["c1", "c2"],
        supervisual_packet_ids=["s1"],
        meme_visual_packet_ids=["m1", "m2"],
        poll_visual_packet_ids=["p1", "p2"],
        reaction_seed_ids=["r1", "r2"],
        source_expression_session_id="xes_1",
        enforce_counts=True,
    )
    assert len(package.video_packet_ids) == 4
    assert len(package.carousel_packet_ids) == 2
    assert len(package.meme_visual_packet_ids) == 2
    assert len(package.poll_visual_packet_ids) == 2
    assert len(package.reaction_seed_ids) == 2
