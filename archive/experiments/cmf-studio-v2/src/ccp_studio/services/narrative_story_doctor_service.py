from __future__ import annotations

import re
from collections import Counter

from ccp_studio.contracts.narrative_story_doctor import (
    ArollStorySpine,
    ArchetypeFitMatrix,
    ArchetypeFitScore,
    ArchetypeMeaningProgram,
    AssetPackageCandidateSet,
    BrollForeshadowingPair,
    BriefAlignmentReport,
    CarouselExtractionPacket,
    CarouselSlideSeed,
    ClusterMeaningGraph,
    CompleteEditingSessionRequestCandidate,
    CutQuestionContract,
    DeliveryRecipeProgram,
    EdgeCandidate,
    EmotionalChangeMap,
    EvidenceStatus,
    ExpectedActualIngredientDiff,
    ExpectedIngredientEdge,
    ExpectedIngredientGraph,
    ExpectedIngredientNode,
    ExperiencePlaneCandidate,
    ExpressionIngredientInventory,
    ExpressionMomentCandidate,
    ExpressionMomentType,
    ExtractionCommanderVerdict,
    ExtractionGapReport,
    ExtractionMode,
    ExtractionQualityReceipt,
    ExtractionSourcePacket,
    ExtractionTarget,
    FollowUpQuestion,
    FollowUpQuestionSet,
    Format01StoryExtractionPacket,
    Format02ExplainerExtractionPacket,
    Format03ReactionExtractionPacket,
    Format04ConsciousReactionExtractionPacket,
    FormatFitMatrix,
    FormatFitScore,
    IngredientType,
    InterviewBriefBinding,
    InterviewerLearningReceipt,
    LayerAwareExtractionContext,
    MeaningPlaneCandidate,
    MemeVisualExtractionPacket,
    NarrativeCluster,
    NarrativeStoryDoctorRun,
    PassStatus,
    PollVisualExtractionPacket,
    PowerPhrasePlan,
    PrimitiveCandidateSet,
    PrimitiveCoalitionCandidate,
    QuestionCoverageReceipt,
    QuestionProductionContract,
    ReactionSeedPacket,
    RhythmPriorityMap,
    SonicStoryArcSeed,
    SourceFidelityReceipt,
    SourceReference,
    SuperVisualExtractionPacket,
    TranscriptBeat,
    TranscriptBeatMap,
    VerbatimSpan,
    VideoExtractionPacket,
    ViewerStateFunction,
    CoverageStatus,
)
from ccp_studio.repositories.narrative_story_doctor import InMemoryNarrativeStoryDoctorRepository


class NarrativeStoryDoctorService:
    def __init__(self, repository: InMemoryNarrativeStoryDoctorRepository | None = None):
        self.repository = repository or InMemoryNarrativeStoryDoctorRepository()

    def hydrate_context(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        extraction_mode: ExtractionMode = ExtractionMode.RAW_TRANSCRIPT,
        interview_brief_id: str | None = None,
        complete_expression_session_id: str | None = None,
        target_formats: list[ExtractionTarget] | None = None,
    ) -> LayerAwareExtractionContext:
        context = LayerAwareExtractionContext(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            extraction_mode=extraction_mode,
            interview_brief_id=interview_brief_id,
            complete_expression_session_id=complete_expression_session_id,
            target_formats=target_formats or [],
            doctrine_refs=[
                "interview_first",
                "expression_first",
                "primitive_first",
                "source_fidelity",
                "composition_before_editing",
            ],
        )
        return self.repository.upsert("contexts", context.context_id, context)

    def compile_question_contracts(self, brief: dict) -> list[QuestionProductionContract]:
        contracts: list[QuestionProductionContract] = []
        for index, item in enumerate(brief.get("questions", []), start=1):
            expected = [
                IngredientType(value)
                for value in item.get("expected_ingredients", ["source_quote"])
            ]
            routes = [
                ExtractionTarget(value)
                for value in item.get("target_asset_routes", [])
            ]
            contract = QuestionProductionContract(
                question_id=item.get("question_id", f"q_{index:03d}"),
                question_text=item["question_text"],
                target_archetypes=item.get("target_archetypes", ["Witness Story"]),
                target_expression_state=item.get("target_expression_state", "truthful_reflection"),
                first_line_anchor=item.get("first_line_anchor"),
                depth_anchor=item.get("depth_anchor"),
                expected_primitives=item.get("expected_primitives", []),
                expected_ingredients=expected,
                target_asset_routes=routes,
                asset_routes=item.get("asset_routes", []),
                evaluation_logic=item.get("evaluation_logic", {"must_generate_source_material": True}),
            )
            contracts.append(contract)
        return contracts

    def bind_interview_brief(self, context: LayerAwareExtractionContext, brief: dict) -> InterviewBriefBinding:
        question_contracts = self.compile_question_contracts(brief)
        binding = InterviewBriefBinding(
            interview_brief_id=brief["interview_brief_id"],
            brand_id=context.brand_id,
            brand_context_version_id=context.brand_context_version_id,
            interview_objective=brief.get("interview_objective", "extract production ingredients"),
            target_archetypes=brief.get("target_archetypes", ["Witness Story"]),
            target_primitives=brief.get("target_primitives", []),
            target_expression_states=brief.get("target_expression_states", []),
            target_output_families=brief.get("target_output_families", []),
            target_content_formats=[ExtractionTarget(v) for v in brief.get("target_content_formats", [])],
            question_contracts=question_contracts,
            bias_strength=brief.get("bias_strength", 0.65),
        )
        return self.repository.upsert("brief_bindings", binding.interview_brief_binding_id, binding)

    def compile_expected_ingredient_graph(self, binding: InterviewBriefBinding) -> ExpectedIngredientGraph:
        nodes: list[ExpectedIngredientNode] = []
        edges: list[ExpectedIngredientEdge] = []
        last_node_id: str | None = None
        for contract in binding.question_contracts:
            for ingredient in contract.expected_ingredients:
                node = ExpectedIngredientNode(
                    question_id=contract.question_id,
                    ingredient_type=ingredient,
                    target_archetype=contract.target_archetypes[0],
                    target_format=contract.target_asset_routes[0] if contract.target_asset_routes else None,
                )
                nodes.append(node)
                if last_node_id:
                    edges.append(ExpectedIngredientEdge(from_node_id=last_node_id, to_node_id=node.node_id, relation="same_question_path"))
                last_node_id = node.node_id
        graph = ExpectedIngredientGraph(
            interview_brief_id=binding.interview_brief_id,
            brand_context_version_id=binding.brand_context_version_id,
            nodes=nodes,
            edges=edges,
        )
        binding.expected_ingredient_graph_id = graph.expected_ingredient_graph_id
        self.repository.upsert("brief_bindings", binding.interview_brief_binding_id, binding)
        return self.repository.upsert("expected_graphs", graph.expected_ingredient_graph_id, graph)

    def normalize_source(
        self,
        *,
        transcript_text: str,
        mode: ExtractionMode = ExtractionMode.RAW_TRANSCRIPT,
        source_id: str = "transcript_001",
        speaker: str = "speaker",
        question_id: str | None = None,
    ) -> ExtractionSourcePacket:
        source_ref = SourceReference(source_kind="transcript", source_id=source_id, start_ms=0, end_ms=max(1000, len(transcript_text) * 40))
        span = VerbatimSpan(
            text=transcript_text.strip(),
            speaker=speaker,
            source_ref_id=source_ref.source_ref_id,
            question_id=question_id,
            start_ms=0,
            end_ms=source_ref.end_ms,
        )
        packet = ExtractionSourcePacket(
            mode=mode,
            transcript_text=transcript_text,
            source_references=[source_ref],
            spans=[span],
            timing_confidence="low" if mode == ExtractionMode.RAW_TRANSCRIPT else "high",
        )
        return self.repository.upsert("source_packets", packet.extraction_source_packet_id, packet)

    def compile_transcript_beat_map(self, packet: ExtractionSourcePacket) -> TranscriptBeatMap:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\\s+", packet.transcript_text.strip()) if s.strip()]
        if not sentences:
            sentences = [packet.transcript_text.strip()]
        beats: list[TranscriptBeat] = []
        cursor = 0
        source_ref_id = packet.source_references[0].source_ref_id
        span_id = packet.spans[0].span_id if packet.spans else None
        for idx, sentence in enumerate(sentences, start=1):
            duration = max(1200, len(sentence) * 45)
            semantic = self._semantic_function(sentence)
            emotional = self._emotional_function(sentence)
            beat = TranscriptBeat(
                speaker=packet.spans[0].speaker if packet.spans else "speaker",
                start_ms=cursor,
                end_ms=cursor + duration,
                verbatim_text=sentence,
                source_ref_id=source_ref_id,
                source_span_ids=[span_id] if span_id else [],
                semantic_function=semantic,
                emotional_function=emotional,
                viewer_state_function=self._viewer_state_for_index(idx),
                expression_signal=self._expression_signal(sentence),
                visual_signal=self._visual_signal(sentence),
                asset_signal=self._asset_signal(sentence),
            )
            beats.append(beat)
            cursor += duration
        beat_map = TranscriptBeatMap(extraction_source_packet_id=packet.extraction_source_packet_id, beats=beats)
        return self.repository.upsert("beat_maps", beat_map.transcript_beat_map_id, beat_map)

    def extract_expression_moments(self, beat_map: TranscriptBeatMap) -> ExpressionIngredientInventory:
        moments: list[ExpressionMomentCandidate] = []
        for beat in beat_map.beats:
            lower = beat.verbatim_text.lower()
            if any(token in lower for token in ["i didn't", "i did not", "i thought", "i realized", "i burned out"]):
                moments.append(ExpressionMomentCandidate(
                    expression_type=ExpressionMomentType.PAUSE,
                    description="truthful reflection / likely pause candidate",
                    beat_id=beat.beat_id,
                    timestamp_ms=beat.start_ms,
                    confidence=0.74,
                ))
            if any(token in lower for token in ["calendar", "planner", "page", "object"]):
                moments.append(ExpressionMomentCandidate(
                    expression_type=ExpressionMomentType.OBJECT_TOUCH,
                    description="object signal / memory object candidate",
                    beat_id=beat.beat_id,
                    timestamp_ms=beat.start_ms,
                    confidence=0.70,
                ))
        if not moments:
            first = beat_map.beats[0]
            moments.append(ExpressionMomentCandidate(
                expression_type=ExpressionMomentType.EMPHASIS,
                description="default emphasis candidate",
                beat_id=first.beat_id,
                timestamp_ms=first.start_ms,
                confidence=0.4,
            ))
        inventory = ExpressionIngredientInventory(expression_moments=moments)
        return self.repository.upsert("expression_inventories", inventory.expression_inventory_id, inventory)

    def compile_clusters(self, beat_map: TranscriptBeatMap, packet: ExtractionSourcePacket) -> list[NarrativeCluster]:
        anchor_beat = self._select_anchor_beat(beat_map)
        text = anchor_beat.verbatim_text
        lower = packet.transcript_text.lower()
        object_signals = [word for word in ["calendar", "planner", "desk", "hotel", "letter", "photo"] if word in lower]
        expression_signals = [sig for sig in ["pause", "exhale", "downward gaze", "confession"] if sig in lower or "i didn't" in lower]
        targets = self._target_candidates(lower)
        cluster = NarrativeCluster(
            source_span_ids=[packet.spans[0].span_id] if packet.spans else [],
            beat_ids=[beat.beat_id for beat in beat_map.beats],
            verbatim_anchor=text,
            emotional_movement=self._emotional_movement(lower),
            object_signals=object_signals,
            expression_signals=expression_signals,
            visual_signals=object_signals + ["human_scale_space"] if object_signals else ["human_expression"],
            possible_output_targets=targets,
        )
        self.repository.upsert("clusters", cluster.cluster_id, cluster)
        return [cluster]

    def compile_cluster_meaning_graph(self, clusters: list[NarrativeCluster]) -> ClusterMeaningGraph:
        graph = ClusterMeaningGraph(
            clusters=clusters,
            edges=[{"from": clusters[0].cluster_id, "to": clusters[0].cluster_id, "relation": "self_contained_truth"}] if clusters else [],
        )
        return self.repository.upsert("cluster_graphs", graph.cluster_meaning_graph_id, graph)

    def compile_meaning_candidates(self, cluster: NarrativeCluster) -> tuple[MeaningPlaneCandidate, ExperiencePlaneCandidate, EdgeCandidate]:
        lower = cluster.verbatim_anchor.lower()
        if "recovery margins" in lower or "calendar" in lower:
            meaning = "capacity as worth"
            experience = "quiet recognition and relief"
            edge = "capacity without recovery is extraction"
            risks = ["self_care_cliche", "productivity_moralizing"]
        else:
            meaning = "source truth requiring structure"
            experience = "recognition"
            edge = cluster.verbatim_anchor[:120]
            risks = ["generic_summary"]
        meaning_candidate = MeaningPlaneCandidate(cluster_id=cluster.cluster_id, meaning_family="recognition", statement=meaning)
        experience_candidate = ExperiencePlaneCandidate(cluster_id=cluster.cluster_id, experience_family="relief", felt_state=experience)
        edge_candidate = EdgeCandidate(cluster_id=cluster.cluster_id, edge_product=edge, misuse_risks=risks)
        return meaning_candidate, experience_candidate, edge_candidate

    def score_archetype_fit(self, cluster: NarrativeCluster) -> ArchetypeFitMatrix:
        text = (cluster.verbatim_anchor + " " + cluster.emotional_movement).lower()
        scores = []
        if any(token in text for token in ["i thought", "i didn't", "burned out", "recovery", "changed"]):
            scores.extend([
                ArchetypeFitScore(archetype="Relief Peak", score=0.88, rationale="truthful reframe and relief turn", source_span_ids=cluster.source_span_ids),
                ArchetypeFitScore(archetype="Transformation Story", score=0.82, rationale="before/after identity change signal", source_span_ids=cluster.source_span_ids),
                ArchetypeFitScore(archetype="Witness Story", score=0.76, rationale="source confession and human identification", source_span_ids=cluster.source_span_ids),
            ])
        else:
            scores.extend([
                ArchetypeFitScore(archetype="Core Educator", score=0.61, rationale="general explanatory potential", source_span_ids=cluster.source_span_ids),
                ArchetypeFitScore(archetype="Quote Commentary", score=0.55, rationale="compact quote potential", source_span_ids=cluster.source_span_ids),
            ])
        matrix = ArchetypeFitMatrix(cluster_id=cluster.cluster_id, scores=scores)
        return self.repository.upsert("archetype_matrices", matrix.archetype_fit_matrix_id, matrix)

    def compile_archetype_program(self, matrix: ArchetypeFitMatrix) -> ArchetypeMeaningProgram:
        best = max(matrix.scores, key=lambda score: score.score)
        modules = self._modules_for_archetype(best.archetype)
        program = ArchetypeMeaningProgram(
            primary_archetype=best.archetype,
            secondary_archetypes=[score.archetype for score in matrix.scores if score.archetype != best.archetype],
            required_modules=modules,
            source_evidence_span_ids=best.source_span_ids,
            format_affinity={
                ExtractionTarget.FORMAT_01_CINEMATIC_STORY.value: 0.9 if "Story" in best.archetype or "Relief" in best.archetype else 0.4,
                ExtractionTarget.CAROUSEL_SEQUENCE.value: 0.78,
                ExtractionTarget.SUPERVISUAL_SINGLE_IMAGE.value: 0.74,
            },
            risk_flags=[],
        )
        return self.repository.upsert("archetype_programs", program.archetype_program_id, program)

    def compile_primitive_candidates(self, cluster: NarrativeCluster, edge: EdgeCandidate | None = None) -> PrimitiveCandidateSet:
        edge_text = edge.edge_product if edge else cluster.verbatim_anchor
        primitive = PrimitiveCandidateSet(
            cluster_id=cluster.cluster_id,
            meaning_plane_family="recognition",
            experience_plane_family="relief",
            primitive_family="integrity",
            primitive_binding_candidate="recognition through embodied reframe",
            coalition_signature_candidate=f"source_quote + expression + {','.join(cluster.object_signals) or 'human_truth'}",
            edge_product_candidate=edge_text,
            misuse_risk_candidates=edge.misuse_risks if edge else ["generic_summary"],
        )
        return self.repository.upsert("primitive_sets", primitive.primitive_candidate_set_id, primitive)

    def compile_primitive_coalition(self, primitive_set: PrimitiveCandidateSet) -> PrimitiveCoalitionCandidate:
        coalition = PrimitiveCoalitionCandidate(
            primitive_candidate_set_id=primitive_set.primitive_candidate_set_id,
            coalition_signature=primitive_set.coalition_signature_candidate,
            governing_primitives=[primitive_set.primitive_family, primitive_set.meaning_plane_family, primitive_set.experience_plane_family],
            misuse_risks=primitive_set.misuse_risk_candidates,
        )
        return coalition

    def compile_delivery_recipe(self, archetype_program: ArchetypeMeaningProgram) -> DeliveryRecipeProgram:
        archetype = archetype_program.primary_archetype.lower()
        if "relief" in archetype or "witness" in archetype:
            seq = ["identification", "story", "permission_to_be_seen", "hope"]
            temp = "gentle_permission"
            motion = "slow_drift"
        elif "myth" in archetype:
            seq = ["named_false_belief", "persistence_reason", "coach_proof", "reframe"]
            temp = "sharp_contrast"
            motion = "faster_reveal"
        else:
            seq = ["context", "mechanism", "proof", "close"]
            temp = "quiet_confidence"
            motion = "controlled"
        recipe = DeliveryRecipeProgram(
            archetype_program_id=archetype_program.archetype_program_id,
            module_sequence=seq,
            emotional_temperature=temp,
            motion_intensity_hint=motion,
            sound_doctrine_hint="voice_first",
        )
        return self.repository.upsert("delivery_recipes", recipe.delivery_recipe_program_id, recipe)

    def score_format_fit(self, cluster: NarrativeCluster) -> FormatFitMatrix:
        lower = cluster.verbatim_anchor.lower() + " " + " ".join(cluster.object_signals)
        scores = []
        scores.append(FormatFitScore(
            target=ExtractionTarget.FORMAT_01_CINEMATIC_STORY,
            score=0.9 if any(t in lower for t in ["burn", "calendar", "planner", "recovery", "i thought"]) else 0.45,
            rationale="story change and memory/object signal",
        ))
        scores.append(FormatFitScore(target=ExtractionTarget.SUPERVISUAL_SINGLE_IMAGE, score=0.78, rationale="single visual truth potential"))
        scores.append(FormatFitScore(target=ExtractionTarget.CAROUSEL_SEQUENCE, score=0.80, rationale="clear thesis and sequence potential"))
        scores.append(FormatFitScore(
            target=ExtractionTarget.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER,
            score=0.62 if any(t in lower for t in ["because", "system", "structure", "framework"]) else 0.35,
            rationale="teachable mechanism potential",
        ))
        scores.append(FormatFitScore(
            target=ExtractionTarget.FORMAT_03_LIVING_COMMENTARY_REACTIONS,
            score=0.70 if any(t in lower for t in ["proof", "quote", "calendar", "screenshot"]) else 0.42,
            rationale="proof/quote commentary potential",
        ))
        scores.append(FormatFitScore(
            target=ExtractionTarget.FORMAT_04_CONSCIOUS_REACTIONS_EDITING,
            score=0.58 if any(t in lower for t in ["weak", "myth", "versus", "vs", "wrong"]) else 0.18,
            rationale="debate tension potential",
        ))
        matrix = FormatFitMatrix(cluster_id=cluster.cluster_id, scores=scores)
        return self.repository.upsert("format_matrices", matrix.format_fit_matrix_id, matrix)

    def compare_expected_actual(
        self,
        contract: QuestionProductionContract,
        actual_ingredients: list[IngredientType],
        route_change: str | None = None,
    ) -> ExpectedActualIngredientDiff:
        expected = contract.expected_ingredients
        hits = [ingredient for ingredient in expected if ingredient in actual_ingredients]
        misses = [ingredient for ingredient in expected if ingredient not in actual_ingredients]
        unexpected = [ingredient for ingredient in actual_ingredients if ingredient not in expected]
        return ExpectedActualIngredientDiff(
            question_id=contract.question_id,
            expected_ingredients=expected,
            actual_ingredients=actual_ingredients,
            hits=hits,
            misses=misses,
            unexpected_wins=unexpected,
            route_change=route_change,
        )

    def compile_question_coverage(
        self,
        contract: QuestionProductionContract,
        diff: ExpectedActualIngredientDiff,
        answer_span_refs: list[str],
    ) -> QuestionCoverageReceipt:
        status = CoverageStatus.STRONG_HIT if len(diff.misses) == 0 else CoverageStatus.PARTIAL_HIT if diff.hits else CoverageStatus.MISS
        followup = None
        if diff.misses:
            followup = self._followup_for_missing(diff.misses[0])
        receipt = QuestionCoverageReceipt(
            question_id=contract.question_id,
            coverage_status=status,
            answer_span_refs=answer_span_refs,
            expected_ingredients_hit=diff.hits,
            expected_ingredients_missing=diff.misses,
            unexpected_high_value_ingredients=diff.unexpected_wins,
            best_output_routes=contract.target_asset_routes,
            follow_up_needed=bool(diff.misses),
            follow_up_question=followup,
        )
        return self.repository.upsert("receipts", receipt.question_coverage_receipt_id, receipt)

    def compile_supervisual_packet(self, cluster: NarrativeCluster, edge: EdgeCandidate) -> SuperVisualExtractionPacket:
        packet = SuperVisualExtractionPacket(
            single_source_truth=cluster.verbatim_anchor,
            visual_hook_candidate=self._visual_hook(cluster),
            edge_product=edge.edge_product,
            source_span_refs=cluster.source_span_ids,
            proof_object_candidate=cluster.object_signals[0] if cluster.object_signals else None,
            memory_object_candidate=cluster.object_signals[0] if cluster.object_signals else None,
            micro_semiotic_anchor_candidate="paper mark" if any(o in ["calendar", "planner"] for o in cluster.object_signals) else None,
            visual_spr_candidate=f"visualize: {edge.edge_product}",
            style_route_hint="CAC + Documentary Proof" if cluster.object_signals else "CAC",
            text_overlay_candidate=self._power_phrase(cluster.verbatim_anchor),
        )
        return self.repository.upsert("packets", packet.supervisual_extraction_packet_id, packet)

    def compile_carousel_packet(self, cluster: NarrativeCluster, edge: EdgeCandidate) -> CarouselExtractionPacket:
        source = cluster.source_span_ids
        slides = [
            CarouselSlideSeed(slide_index=1, role="cover_hook", slide_copy="What if this was not weakness?", source_ref=source[0] if source else None),
            CarouselSlideSeed(slide_index=2, role="old_belief", slide_copy="I thought being constantly available made me reliable.", source_ref=source[0] if source else None),
            CarouselSlideSeed(slide_index=3, role="proof_object", slide_copy="My calendar was proof.", source_ref=source[0] if source else None),
            CarouselSlideSeed(slide_index=4, role="truthful_payoff", slide_copy=cluster.verbatim_anchor[:80], source_ref=source[0] if source else None),
            CarouselSlideSeed(slide_index=5, role="save_card", slide_copy=edge.edge_product[:80], source_ref=source[0] if source else None),
        ]
        packet = CarouselExtractionPacket(
            carousel_thesis=edge.edge_product,
            source_span_refs=source,
            viewer_state_sequence=[
                ViewerStateFunction.PERCEPTUAL_ENTRY,
                ViewerStateFunction.RELEVANT_OPEN_QUESTION,
                ViewerStateFunction.ACTIVE_PREDICTION,
                ViewerStateFunction.TRUTHFUL_PAYOFF,
                ViewerStateFunction.HUMAN_AFFINITY,
                ViewerStateFunction.EXPECTED_FUTURE_VALUE,
            ],
            slides=slides,
            open_loop="What if the problem is not weakness?",
            closure_contract="The viewer receives a source-faithful reframe.",
            visual_system_seed="soft editorial proof-object sequence",
            asset_requirement_seed=cluster.object_signals,
        )
        return self.repository.upsert("packets", packet.carousel_extraction_packet_id, packet)

    def compile_video_packet(self, beat_map: TranscriptBeatMap, inventory: ExpressionIngredientInventory) -> VideoExtractionPacket:
        beat_refs = [beat.beat_id for beat in beat_map.beats]
        packet = VideoExtractionPacket(
            selected_beat_refs=beat_refs,
            aroll_spine_candidates=[beat.verbatim_text for beat in beat_map.beats[:4]],
            expression_moment_refs=[moment.expression_moment_id for moment in inventory.expression_moments],
            scene_candidate_map={beat.beat_id: beat.semantic_function for beat in beat_map.beats},
            broll_requirements=[beat.asset_signal for beat in beat_map.beats if beat.asset_signal],
            sonic_story_requirements=["voice_first", "pause_preservation"],
            subtitle_power_phrases=[self._power_phrase(beat.verbatim_text) for beat in beat_map.beats[:3]],
            timeline_duration_hint_seconds=60,
        )
        return self.repository.upsert("packets", packet.video_extraction_packet_id, packet)

    def compile_format01_packet(self, cluster: NarrativeCluster, beat_map: TranscriptBeatMap, edge: EdgeCandidate) -> Format01StoryExtractionPacket:
        spine_lines = [beat.verbatim_text for beat in beat_map.beats[:4]]
        spine = ArollStorySpine(source_span_refs=cluster.source_span_ids, spine_lines=spine_lines)
        change = EmotionalChangeMap(
            before_state="availability as worth",
            pressure_state="calendar as proof",
            truthful_payoff=cluster.verbatim_anchor,
            after_state=edge.edge_product,
        )
        cuts = [
            CutQuestionContract(
                cut_index=1,
                raises="Where is this going?",
                answers="Toward a truthful reframe.",
                feeling="quiet pressure",
                tempo="slow",
                source_span_refs=cluster.source_span_ids,
            ),
            CutQuestionContract(
                cut_index=2,
                raises="How should I feel?",
                answers="Recognition and relief.",
                feeling="quiet recognition",
                tempo="hold the pause",
                source_span_refs=cluster.source_span_ids,
            ),
        ]
        broll = []
        if cluster.object_signals:
            broll.append(BrollForeshadowingPair(
                before_visual=f"clean {cluster.object_signals[0]}",
                after_visual=f"overmarked {cluster.object_signals[0]}",
                change_function="what looked reliable became extraction",
                source_signal=cluster.object_signals[0],
            ))
        packet = Format01StoryExtractionPacket(
            sub_format="relief_peak_story",
            aroll_story_spine=spine,
            emotional_change_map=change,
            cut_question_chain=cuts,
            broll_foreshadowing_pairs=broll,
            rhythm_priority_map=RhythmPriorityMap(priorities_by_scene={"confession": "emotion", "object_insert": "story", "pressure": "rhythm"}),
            power_phrase_plan=PowerPhrasePlan(phrases=[self._power_phrase(cluster.verbatim_anchor), edge.edge_product]),
            sonic_story_arc_seed=SonicStoryArcSeed(room_tone="warm_room", sound_cues=["paper_cue"] if cluster.object_signals else []),
            memory_object_candidates=cluster.object_signals,
        )
        return self.repository.upsert("packets", packet.format01_packet_id, packet)

    def compile_format02_packet(self, cluster: NarrativeCluster) -> Format02ExplainerExtractionPacket:
        mechanism = "Capacity requires recovery margin to remain sustainable"
        packet = Format02ExplainerExtractionPacket(
            sub_format="scene_to_principle",
            teachable_mechanism=mechanism,
            source_span_refs=cluster.source_span_ids,
            concept_nodes=["availability", "capacity", "recovery_margin", "burnout"],
            diagram_sequence=["calendar fills", "margin disappears", "system collapses", "reframe appears"],
            avatar_performance_requirements=["point_to_calendar", "open_hand_on_reframe"],
        )
        return self.repository.upsert("packets", packet.format02_packet_id, packet)

    def compile_format03_packet(self, cluster: NarrativeCluster) -> Format03ReactionExtractionPacket:
        surface = cluster.verbatim_anchor
        packet = Format03ReactionExtractionPacket(
            sub_format="quote_commentary_reaction",
            proof_or_quote_surface=surface,
            source_span_refs=cluster.source_span_ids,
            coach_reaction_angle="quiet recognition and interpretation",
            rough_notation_targets=["no recovery margins"] if "recovery" in surface.lower() else [],
            reaction_question="Is this weakness, or a system with no recovery margin?",
        )
        return self.repository.upsert("packets", packet.format03_packet_id, packet)

    def compile_format04_packet(self, cluster: NarrativeCluster) -> Format04ConsciousReactionExtractionPacket:
        packet = Format04ConsciousReactionExtractionPacket(
            sub_format="myth_debunk_reaction",
            debate_tension="Burnout as weakness vs burnout as no recovery margin",
            source_span_refs=cluster.source_span_ids,
            reaction_ui_surface="this_vs_that_panel",
            score_state_seed="myth_break",
            meme_mechanism="micro_contradiction",
        )
        return self.repository.upsert("packets", packet.format04_packet_id, packet)

    def compile_meme_packet(self, cluster: NarrativeCluster) -> MemeVisualExtractionPacket:
        packet = MemeVisualExtractionPacket(
            sub_format="micro_contradiction",
            source_truth=cluster.verbatim_anchor,
            compressed_paradox="When your calendar says reliable but your nervous system says hostage",
            meme_mechanism="micro_contradiction",
            source_span_refs=cluster.source_span_ids,
            risk="avoid mocking burnout",
        )
        return self.repository.upsert("packets", packet.meme_visual_packet_id, packet)

    def compile_poll_packet(self, cluster: NarrativeCluster) -> PollVisualExtractionPacket:
        packet = PollVisualExtractionPacket(
            sub_format="tension_poll",
            question="Is burnout weakness, over-responsibility, or a life without recovery margins?",
            options=["Weakness", "Over-responsibility", "No recovery margins", "All of them"],
            source_span_refs=cluster.source_span_ids,
            discussion_value="high",
        )
        return self.repository.upsert("packets", packet.poll_visual_packet_id, packet)

    def compile_reaction_seed(self, cluster: NarrativeCluster, inventory: ExpressionIngredientInventory) -> ReactionSeedPacket:
        moment_id = inventory.expression_moments[0].expression_moment_id if inventory.expression_moments else None
        packet = ReactionSeedPacket(
            source_expression_moment_id=moment_id,
            source_quote=cluster.verbatim_anchor,
            source_span_refs=cluster.source_span_ids,
            reaction_question="Is this weakness, or bad system design?",
            compatible_reaction_formats=["Validation Reaction", "Vote Then React", "Debate with Jury Mode"],
        )
        return self.repository.upsert("packets", packet.reaction_seed_id, packet)

    def compile_complete_editing_session_requests(
        self,
        source_expression_session_id: str,
        cluster: NarrativeCluster,
    ) -> list[CompleteEditingSessionRequestCandidate]:
        request = CompleteEditingSessionRequestCandidate(
            source_expression_session_id=source_expression_session_id,
            asset_type="format_01_video",
            archetype="Relief Peak",
            derivative="cinematic_story_commentary",
            cmf_route="CAC_CINEMATIC_STORY",
            source_span_refs=cluster.source_span_ids,
            evaluation_requirements=["presence_weighted_eval", "source_fidelity"],
        )
        return [request]

    def compile_asset_package_candidate_set(
        self,
        *,
        video_packet_ids: list[str],
        carousel_packet_ids: list[str],
        supervisual_packet_ids: list[str],
        meme_visual_packet_ids: list[str],
        poll_visual_packet_ids: list[str],
        reaction_seed_ids: list[str],
        source_expression_session_id: str | None = None,
        enforce_counts: bool = False,
    ) -> AssetPackageCandidateSet:
        return AssetPackageCandidateSet(
            source_expression_session_id=source_expression_session_id,
            video_packet_ids=video_packet_ids,
            carousel_packet_ids=carousel_packet_ids,
            supervisual_packet_ids=supervisual_packet_ids,
            meme_visual_packet_ids=meme_visual_packet_ids,
            poll_visual_packet_ids=poll_visual_packet_ids,
            reaction_seed_ids=reaction_seed_ids,
            enforce_guest_asset_pack_counts=enforce_counts,
        )

    def compile_gap_report(self, expected: list[IngredientType], actual: list[IngredientType]) -> ExtractionGapReport:
        missing = [ingredient for ingredient in expected if ingredient not in actual]
        severity = "high" if len(missing) >= 3 else "medium" if missing else "low"
        return ExtractionGapReport(missing_ingredients=missing, severity=severity)

    def compile_followup_questions(self, gap_report: ExtractionGapReport, target_archetype: str | None = None) -> FollowUpQuestionSet:
        questions = [
            FollowUpQuestion(
                question_text=self._followup_for_missing(ingredient),
                missing_ingredient=ingredient,
                target_archetype=target_archetype,
                reason=f"Needed to complete {ingredient.value}",
            )
            for ingredient in gap_report.missing_ingredients
        ]
        return FollowUpQuestionSet(questions=questions)

    def evaluate_source_fidelity(self, spans: list[VerbatimSpan], generated_claims: list[str] | None = None) -> SourceFidelityReceipt:
        generated_claims = generated_claims or []
        transcript = " ".join(span.text for span in spans).lower()
        invented = [claim for claim in generated_claims if claim.lower() not in transcript]
        receipt = SourceFidelityReceipt(
            pass_status=PassStatus.FAIL if invented else PassStatus.PASS,
            invented_claims=invented,
            checked_span_ids=[span.span_id for span in spans],
        )
        return self.repository.upsert("receipts", receipt.source_fidelity_receipt_id, receipt)

    def authorize_extraction(self, source_fidelity: SourceFidelityReceipt, gap_report: ExtractionGapReport | None = None) -> ExtractionCommanderVerdict:
        blockers = []
        if source_fidelity.pass_status == PassStatus.FAIL:
            blockers.append("source_fidelity_failed")
        if gap_report and gap_report.severity == "high":
            blockers.append("high_severity_extraction_gaps")
        verdict = ExtractionCommanderVerdict(
            authorized=not blockers,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
            recommendations=["collect follow-up question answers"] if blockers else ["ready for downstream engine packet use"],
        )
        return self.repository.upsert("receipts", verdict.extraction_commander_verdict_id, verdict)

    def compile_interviewer_learning_receipt(
        self,
        coverage_receipts: list[QuestionCoverageReceipt],
    ) -> InterviewerLearningReceipt:
        missed = []
        successes = []
        followups = []
        for receipt in coverage_receipts:
            if receipt.expected_ingredients_missing:
                missed.extend([ingredient.value for ingredient in receipt.expected_ingredients_missing])
            if receipt.expected_ingredients_hit:
                successes.extend([ingredient.value for ingredient in receipt.expected_ingredients_hit])
            if receipt.follow_up_question:
                followups.append(receipt.follow_up_question)
        return InterviewerLearningReceipt(
            missed_depth_paths=sorted(set(missed)),
            successful_activation_patterns=sorted(set(successes)),
            recommended_followup_questions=followups,
        )

    # -----------------------------------------------------------------
    # Internal heuristics
    # -----------------------------------------------------------------
    def _semantic_function(self, text: str) -> str:
        lower = text.lower()
        if "?" in text:
            return "open_question"
        if any(t in lower for t in ["because", "realized", "truth", "didn't", "did not"]):
            return "truthful_payoff"
        if any(t in lower for t in ["thought", "used to", "at the time"]):
            return "old_belief"
        if any(t in lower for t in ["calendar", "planner", "proof"]):
            return "proof_object"
        return "source_statement"

    def _emotional_function(self, text: str) -> str:
        lower = text.lower()
        if any(t in lower for t in ["burn", "weak", "cost", "private"]):
            return "vulnerability"
        if any(t in lower for t in ["recovery", "relief", "hope"]):
            return "relief"
        return "recognition"

    def _viewer_state_for_index(self, index: int) -> ViewerStateFunction:
        sequence = [
            ViewerStateFunction.PERCEPTUAL_ENTRY,
            ViewerStateFunction.RELEVANT_OPEN_QUESTION,
            ViewerStateFunction.ACTIVE_PREDICTION,
            ViewerStateFunction.TRUTHFUL_PAYOFF,
            ViewerStateFunction.HUMAN_AFFINITY,
            ViewerStateFunction.EXPECTED_FUTURE_VALUE,
        ]
        return sequence[min(index - 1, len(sequence) - 1)]

    def _expression_signal(self, text: str) -> str | None:
        lower = text.lower()
        if any(t in lower for t in ["i didn't", "i did not", "i thought", "i burned"]):
            return "quiet_confession"
        if "?" in lower:
            return "curiosity"
        return None

    def _visual_signal(self, text: str) -> str | None:
        lower = text.lower()
        for token in ["calendar", "planner", "desk", "paper", "hotel"]:
            if token in lower:
                return token
        return None

    def _asset_signal(self, text: str) -> str | None:
        sig = self._visual_signal(text)
        return f"{sig}_asset" if sig else None

    def _select_anchor_beat(self, beat_map: TranscriptBeatMap) -> TranscriptBeat:
        priority = sorted(
            beat_map.beats,
            key=lambda beat: (
                1 if any(t in beat.verbatim_text.lower() for t in ["recovery", "burn", "truth", "weak", "calendar", "proof"]) else 0,
                len(beat.verbatim_text),
            ),
            reverse=True,
        )
        return priority[0]

    def _emotional_movement(self, lower: str) -> str:
        if "burn" in lower and "recovery" in lower:
            return "shame_to_structural_clarity"
        if "thought" in lower:
            return "old_belief_to_reframe"
        return "recognition_to_clarity"

    def _target_candidates(self, lower: str) -> list[ExtractionTarget]:
        targets = [ExtractionTarget.SUPERVISUAL_SINGLE_IMAGE, ExtractionTarget.CAROUSEL_SEQUENCE, ExtractionTarget.VIDEO_SCENE]
        if any(t in lower for t in ["burn", "calendar", "planner", "recovery", "i thought"]):
            targets.insert(0, ExtractionTarget.FORMAT_01_CINEMATIC_STORY)
        if any(t in lower for t in ["because", "system", "structure", "framework"]):
            targets.append(ExtractionTarget.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER)
        if any(t in lower for t in ["proof", "quote", "calendar"]):
            targets.append(ExtractionTarget.FORMAT_03_LIVING_COMMENTARY_REACTIONS)
        if any(t in lower for t in ["weak", "myth", "wrong"]):
            targets.append(ExtractionTarget.FORMAT_04_CONSCIOUS_REACTIONS_EDITING)
        targets.extend([ExtractionTarget.MEME_VISUAL, ExtractionTarget.POLL_VISUAL, ExtractionTarget.REACTION_SEED])
        return list(dict.fromkeys(targets))

    def _modules_for_archetype(self, archetype: str) -> list[str]:
        lower = archetype.lower()
        if "relief" in lower or "witness" in lower or "transformation" in lower:
            return ["identification", "story", "permission_to_be_seen", "hope"]
        if "myth" in lower:
            return ["named_false_belief", "persistence_reason", "coach_proof", "reframe"]
        return ["context", "mechanism", "proof", "close"]

    def _visual_hook(self, cluster: NarrativeCluster) -> str:
        if cluster.object_signals:
            return f"A {cluster.object_signals[0]} so specific it becomes evidence."
        return f"One source truth: {cluster.verbatim_anchor[:80]}"

    def _power_phrase(self, text: str) -> str:
        lower = text.lower()
        if "recovery margins" in lower:
            return "No recovery margins."
        if "weak" in lower:
            return "It was not weakness."
        return text[:64].rstrip(".") + "."

    def _followup_for_missing(self, ingredient: IngredientType) -> str:
        if ingredient == IngredientType.MEMORY_OBJECT:
            return "Was there a physical object from that season that still carries the feeling?"
        if ingredient == IngredientType.PROOF_OBJECT:
            return "What visible proof would show this was happening?"
        if ingredient == IngredientType.BEFORE_AFTER_CHANGE:
            return "What changed before and after that moment?"
        if ingredient == IngredientType.EMOTIONAL_PAUSE:
            return "Where did your body feel the truth before you had words for it?"
        return f"What specific detail would help us capture {ingredient.value}?"
