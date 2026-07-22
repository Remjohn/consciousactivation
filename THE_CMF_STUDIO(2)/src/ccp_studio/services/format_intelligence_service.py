from __future__ import annotations

from ccp_studio.contracts.format_intelligence import (
    CarouselFormatProgram,
    CarouselSequenceStep,
    EngineAdapterPayload,
    EngineTarget,
    Format01CinematicStoryProgram,
    Format02AvatarPaperCutExplainerProgram,
    Format03LivingCommentaryReactionProgram,
    Format04ConsciousReactionEditingProgram,
    FormatActivationDecision,
    FormatAntiSlopRule,
    FormatBrollPolicy,
    FormatCommanderVerdict,
    FormatCompositionGrammar,
    FormatEvalGateSet,
    FormatFirstFramePolicy,
    FormatId,
    FormatIngredientCheck,
    FormatIngredientChecklist,
    FormatIngredientRequirement,
    FormatIngredientType,
    FormatIntelligenceContext,
    FormatLayerRequirement,
    FormatLayerStackSpec,
    FormatMemeticCuePolicy,
    FormatMemoryObjectPolicy,
    FormatMotionDoctrine,
    FormatProofPolicy,
    FormatReactionSurfacePolicy,
    FormatRenderRequirement,
    FormatRepairCommand,
    FormatSoundDoctrine,
    FormatStyleRoutePolicy,
    FormatSubFormatRoute,
    FormatSubtitlePolicy,
    FormatAvatarPerformancePolicy,
    FrameProfile,
    GenericExtractionPacketRef,
    IngredientStatus,
    MemeVisualFormatProgram,
    PassStatus,
    PollVisualFormatProgram,
    ReactionSeedFormatProgram,
    StyleRoute,
    SuperVisualFormatProgram,
)
from ccp_studio.repositories.format_intelligence import InMemoryFormatIntelligenceRepository


class FormatIntelligenceService:
    def __init__(self, repository: InMemoryFormatIntelligenceRepository | None = None):
        self.repository = repository or InMemoryFormatIntelligenceRepository()

    def hydrate_context(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        source_extraction_run_id: str | None = None,
        archetype_program_id: str | None = None,
        primitive_coalition_candidate_id: str | None = None,
        delivery_recipe_program_id: str | None = None,
        target_formats: list[FormatId] | None = None,
    ) -> FormatIntelligenceContext:
        context = FormatIntelligenceContext(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            source_extraction_run_id=source_extraction_run_id,
            archetype_program_id=archetype_program_id,
            primitive_coalition_candidate_id=primitive_coalition_candidate_id,
            delivery_recipe_program_id=delivery_recipe_program_id,
            target_formats=target_formats or [],
        )
        return self.repository.upsert("contexts", context.format_intelligence_context_id, context)

    def register_extraction_packet(self, packet: GenericExtractionPacketRef) -> GenericExtractionPacketRef:
        return self.repository.upsert("extraction_packets", packet.extraction_packet_id, packet)

    def route_format(self, packet: GenericExtractionPacketRef) -> FormatActivationDecision:
        reason = f"Packet target {packet.target_format.value} selected by Narrative Story Doctor."
        decision = FormatActivationDecision(
            format_id=packet.target_format,
            activated=True,
            activation_reason=reason,
            evidence=packet.source_span_refs,
            confidence=0.82,
        )
        return self.repository.upsert("activation_decisions", decision.format_activation_decision_id, decision)

    def route_sub_format(self, packet: GenericExtractionPacketRef) -> FormatSubFormatRoute:
        sub_format = packet.sub_format_hint or self._default_sub_format(packet)
        route = FormatSubFormatRoute(
            format_id=packet.target_format,
            sub_format_id=sub_format,
            rationale=f"Sub-format {sub_format} selected from extraction packet fields.",
            confidence=0.78,
        )
        return self.repository.upsert("sub_format_routes", route.format_sub_format_route_id, route)

    def compile_ingredient_requirements(self, format_id: FormatId) -> list[FormatIngredientRequirement]:
        required = {
            FormatId.FORMAT_01_CINEMATIC_STORY: [
                FormatIngredientType.AROLL_STORY_SPINE,
                FormatIngredientType.EMOTIONAL_CHANGE_MAP,
                FormatIngredientType.CUT_QUESTION_CHAIN,
                FormatIngredientType.SONIC_STORY_ARC_SEED,
            ],
            FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER: [
                FormatIngredientType.TEACHABLE_MECHANISM,
                FormatIngredientType.CONCEPT_NODES,
                FormatIngredientType.DIAGRAM_SEQUENCE,
            ],
            FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS: [
                FormatIngredientType.PROOF_OR_QUOTE_SURFACE,
                FormatIngredientType.COACH_REACTION_ANGLE,
            ],
            FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING: [
                FormatIngredientType.DEBATE_TENSION,
                FormatIngredientType.REACTION_UI_SURFACE,
            ],
            FormatId.SUPERVISUAL: [
                FormatIngredientType.SINGLE_SOURCE_TRUTH,
                FormatIngredientType.VISUAL_HOOK,
                FormatIngredientType.EDGE_PRODUCT,
            ],
            FormatId.CAROUSEL: [
                FormatIngredientType.CAROUSEL_THESIS,
                FormatIngredientType.VIEWER_STATE_SEQUENCE,
                FormatIngredientType.CLOSURE_CONTRACT,
            ],
            FormatId.MEME_VISUAL: [
                FormatIngredientType.MEME_MECHANISM,
            ],
            FormatId.POLL_VISUAL: [
                FormatIngredientType.POLL_OPTIONS,
            ],
            FormatId.REACTION_SEED: [
                FormatIngredientType.REACTION_QUESTION,
            ],
        }[format_id]
        return [FormatIngredientRequirement(ingredient_type=item, reason=f"{format_id.value} requires {item.value}") for item in required]

    def compile_ingredient_checklist(self, packet: GenericExtractionPacketRef, requirements: list[FormatIngredientRequirement]) -> FormatIngredientChecklist:
        checks: list[FormatIngredientCheck] = []
        for req in requirements:
            value = packet.payload.get(req.ingredient_type.value)
            if value:
                status = IngredientStatus.PRESENT
                evidence = str(value)
                missing = None
            else:
                status = IngredientStatus.MISSING if req.required else IngredientStatus.PARTIAL
                evidence = None
                missing = f"missing {req.ingredient_type.value}"
            checks.append(FormatIngredientCheck(
                ingredient_type=req.ingredient_type,
                status=status,
                evidence=evidence,
                missing_reason=missing,
            ))
        return FormatIngredientChecklist(format_id=packet.target_format, checks=checks)

    def compile_composition_grammar(self, format_id: FormatId, sub_format_id: str) -> FormatCompositionGrammar:
        rules_by_format = {
            FormatId.FORMAT_01_CINEMATIC_STORY: ["A-roll is the story spine", "B-roll must foreshadow or contrast", "sparse power phrases", "negative space protects emotion"],
            FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER: ["one concept equals one motion", "avatar gesture must match concept", "diagram reveals sequentially"],
            FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS: ["upper canvas proof surface", "lower canvas coach reaction", "annotation synchronized to speech"],
            FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING: ["reaction UI surface carries debate state", "score changes follow argument shift", "no zoom spam"],
            FormatId.SUPERVISUAL: ["one source truth", "one visual hero", "intentional negative space"],
            FormatId.CAROUSEL: ["slide roles are sequential", "source claims remain traceable", "closure contract required"],
            FormatId.MEME_VISUAL: ["joke preserves source truth", "risk boundary explicit"],
            FormatId.POLL_VISUAL: ["options represent real tension", "no false binary"],
            FormatId.REACTION_SEED: ["store source quote and reaction question"],
        }
        return FormatCompositionGrammar(
            format_id=format_id,
            sub_format_id=sub_format_id,
            grammar_name=f"{sub_format_id}_grammar",
            rules=rules_by_format[format_id],
            attention_path=self._attention_path(format_id),
            text_policy=self._text_policy(format_id),
        )

    def compile_layer_stack(self, format_id: FormatId) -> FormatLayerStackSpec:
        layer_roles = {
            FormatId.FORMAT_01_CINEMATIC_STORY: ["background_climate", "a_roll_closeup", "memory_or_proof_object", "subtitle_or_power_phrase"],
            FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER: ["paper_background", "avatar_performance_layer", "diagram_layer", "annotation_layer", "caption_layer"],
            FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS: ["background", "proof_surface_upper", "coach_cutout_lower", "rough_notation", "caption_layer"],
            FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING: ["reaction_ui_surface", "coach_cutout", "score_state", "meme_anchor", "caption_layer"],
            FormatId.SUPERVISUAL: ["background", "hero_visual", "text_overlay", "brand_mark"],
            FormatId.CAROUSEL: ["background", "slide_surface", "headline", "proof_object", "slide_number"],
            FormatId.MEME_VISUAL: ["background", "meme_object", "caption", "risk_boundary"],
            FormatId.POLL_VISUAL: ["background", "question", "options", "brand_mark"],
            FormatId.REACTION_SEED: ["metadata_only"],
        }[format_id]
        layers = [
            FormatLayerRequirement(layer_role=role, z_index=index, description=f"{role} layer")
            for index, role in enumerate(layer_roles, start=1)
        ]
        return FormatLayerStackSpec(format_id=format_id, layers=layers, min_layers=1)

    def compile_motion_doctrine(self, format_id: FormatId) -> FormatMotionDoctrine:
        if format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            allowed = ["snap_zoom", "score_tick", "fast_reveal", "punch_in"]
            banned = ["unmotivated_zoom_spam", "meme_overload"]
            max_events = 8
        elif format_id == FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            allowed = ["paper_slide", "draw_on", "label_pop", "gesture_point", "diagram_trace"]
            banned = ["decorative_avatar_motion", "overloaded_diagram_motion"]
            max_events = 8
        else:
            allowed = ["slow_push_in", "drift", "subtle_parallax", "hand_drawn_reveal"]
            banned = ["hyperactive_pop_in", "zoom_spam", "kinetic_text_overload"]
            max_events = 4
        return FormatMotionDoctrine(format_id=format_id, allowed_motion=allowed, banned_motion=banned, max_motion_events_per_15s=max_events)

    def compile_sound_doctrine(self, format_id: FormatId) -> FormatSoundDoctrine:
        if format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            policy = FormatMemeticCuePolicy(format_id=format_id, max_cues=1, per_seconds=10)
            profile = "high_intensity_voice_led"
            cues = ["snap", "score_tick", "reveal_hit"]
        elif format_id == FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            policy = FormatMemeticCuePolicy(format_id=format_id, max_cues=1, per_seconds=30)
            profile = "clean_voice_chalk_paper"
            cues = ["chalk_scratch", "paper_slide"]
        else:
            policy = FormatMemeticCuePolicy(format_id=format_id, max_cues=1, per_seconds=30)
            profile = "voice_first_room_tone"
            cues = ["room_tone", "paper_rustle"]
        return FormatSoundDoctrine(format_id=format_id, sonic_profile=profile, allowed_cues=cues, memetic_policy=policy)

    def compile_style_route_policy(self, format_id: FormatId) -> FormatStyleRoutePolicy:
        if format_id == FormatId.FORMAT_01_CINEMATIC_STORY:
            return FormatStyleRoutePolicy(
                format_id=format_id,
                primary_routes=[StyleRoute.CAC, StyleRoute.DOCUMENTARY_PROOF],
                secondary_routes=[StyleRoute.PAPER_CUT_ARTIFACT],
                forbidden_routes=[StyleRoute.UI_REACTION_SURFACE, StyleRoute.AVATAR_PERFORMANCE_LAYER],
            )
        if format_id == FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            return FormatStyleRoutePolicy(
                format_id=format_id,
                primary_routes=[StyleRoute.PAPER_CUT_EDITORIAL, StyleRoute.AVATAR_PERFORMANCE_LAYER],
                secondary_routes=[StyleRoute.GMG_EXPERT_05, StyleRoute.GMG_EXPERT_06, StyleRoute.MOTION_CANVAS, StyleRoute.MANIM, StyleRoute.ROUGH_NOTATION],
                forbidden_routes=[],
            )
        if format_id == FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS:
            return FormatStyleRoutePolicy(
                format_id=format_id,
                primary_routes=[StyleRoute.DOCUMENTARY_PROOF, StyleRoute.ROUGH_NOTATION],
                secondary_routes=[StyleRoute.UI_REACTION_SURFACE, StyleRoute.CAC],
                forbidden_routes=[StyleRoute.AVATAR_PERFORMANCE_LAYER],
            )
        if format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            return FormatStyleRoutePolicy(
                format_id=format_id,
                primary_routes=[StyleRoute.UI_REACTION_SURFACE],
                secondary_routes=[StyleRoute.DOCUMENTARY_PROOF, StyleRoute.ROUGH_NOTATION, StyleRoute.GMG_EXPERT_06],
                forbidden_routes=[StyleRoute.PAPER_CUT_ARTIFACT],
            )
        if format_id == FormatId.SUPERVISUAL:
            return FormatStyleRoutePolicy(format_id=format_id, primary_routes=[StyleRoute.CAC], secondary_routes=[StyleRoute.DOCUMENTARY_PROOF, StyleRoute.PAPER_CUT_ARTIFACT])
        if format_id == FormatId.CAROUSEL:
            return FormatStyleRoutePolicy(format_id=format_id, primary_routes=[StyleRoute.PAPER_CUT_EDITORIAL], secondary_routes=[StyleRoute.CAC, StyleRoute.DOCUMENTARY_PROOF, StyleRoute.GMG_EXPERT_05])
        return FormatStyleRoutePolicy(format_id=format_id, primary_routes=[StyleRoute.UI_REACTION_SURFACE], secondary_routes=[StyleRoute.CAC])

    def compile_eval_gate_set(self, format_id: FormatId) -> FormatEvalGateSet:
        rules = [
            FormatAntiSlopRule(code="source_fidelity", description="Output must preserve source meaning."),
            FormatAntiSlopRule(code="no_generic_render", description="Reject generic output that ignores format grammar."),
        ]
        if format_id == FormatId.FORMAT_01_CINEMATIC_STORY:
            rules.append(FormatAntiSlopRule(code="no_broll_filler", description="B-roll must foreshadow, contrast, or clarify."))
        if format_id == FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS:
            rules.append(FormatAntiSlopRule(code="proof_surface_required", description="Upper proof or quote surface is required."))
        if format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            rules.append(FormatAntiSlopRule(code="no_zoom_spam", description="Fast motion must follow argument shift."))
        gates = ["source_fidelity_eval", "composition_eval", "format_grammar_eval", "anti_slop_gate"]
        return FormatEvalGateSet(format_id=format_id, gates=gates, anti_slop_rules=rules)

    def compile_render_requirement(self, format_id: FormatId) -> FormatRenderRequirement:
        target_map = {
            FormatId.SUPERVISUAL: (FrameProfile.ONE_ONE_SOFT_ROUNDED, EngineTarget.SUPERVISUAL_ENGINE),
            FormatId.CAROUSEL: (FrameProfile.FOUR_FIVE_CAROUSEL, EngineTarget.CAROUSEL_ENGINE),
            FormatId.MEME_VISUAL: (FrameProfile.ONE_ONE_PROOF_CARD, EngineTarget.MEME_VISUAL_ENGINE),
            FormatId.POLL_VISUAL: (FrameProfile.ONE_ONE_PROOF_CARD, EngineTarget.POLL_VISUAL_ENGINE),
            FormatId.REACTION_SEED: (FrameProfile.ONE_ONE_PROOF_CARD, EngineTarget.REACTION_ENGINE),
            FormatId.FORMAT_01_CINEMATIC_STORY: (FrameProfile.NINE_SIXTEEN_VERTICAL, EngineTarget.VIDEO_EDITING_ENGINE),
            FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER: (FrameProfile.NINE_SIXTEEN_PAPERCUT, EngineTarget.VIDEO_EDITING_ENGINE),
            FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS: (FrameProfile.NINE_SIXTEEN_SPLIT_REACTION, EngineTarget.VIDEO_EDITING_ENGINE),
            FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING: (FrameProfile.NINE_SIXTEEN_CONSCIOUS_REACTION, EngineTarget.VIDEO_EDITING_ENGINE),
        }
        frame, engine = target_map[format_id]
        return FormatRenderRequirement(format_id=format_id, frame_profile=frame, engine_target=engine, output_requirements=["hash_assets", "deterministic_timing"])

    def compile_base_program_parts(self, context: FormatIntelligenceContext, packet: GenericExtractionPacketRef, sub_route: FormatSubFormatRoute):
        requirements = self.compile_ingredient_requirements(packet.target_format)
        checklist = self.compile_ingredient_checklist(packet, requirements)
        return {
            "brand_id": context.brand_id,
            "brand_context_version_id": context.brand_context_version_id,
            "source_extraction_packet_id": packet.extraction_packet_id,
            "source_span_refs": packet.source_span_refs,
            "archetype_program_id": context.archetype_program_id,
            "primitive_coalition_candidate_id": context.primitive_coalition_candidate_id,
            "delivery_recipe_program_id": context.delivery_recipe_program_id,
            "format_id": packet.target_format,
            "sub_format_id": sub_route.sub_format_id,
            "activation_reason": f"Compiled from extraction packet {packet.extraction_packet_id}",
            "ingredient_checklist": checklist,
            "composition_grammar": self.compile_composition_grammar(packet.target_format, sub_route.sub_format_id),
            "layer_stack_spec": self.compile_layer_stack(packet.target_format),
            "motion_doctrine": self.compile_motion_doctrine(packet.target_format),
            "sound_doctrine": self.compile_sound_doctrine(packet.target_format),
            "style_route_policy": self.compile_style_route_policy(packet.target_format),
            "first_frame_policy": FormatFirstFramePolicy(format_id=packet.target_format),
            "subtitle_policy": FormatSubtitlePolicy(format_id=packet.target_format),
            "eval_gate_set": self.compile_eval_gate_set(packet.target_format),
            "render_requirement": self.compile_render_requirement(packet.target_format),
        }

    def compile_format_program(self, context: FormatIntelligenceContext, packet: GenericExtractionPacketRef):
        self.register_extraction_packet(packet)
        sub_route = self.route_sub_format(packet)
        parts = self.compile_base_program_parts(context, packet, sub_route)
        payload = packet.payload

        if packet.target_format == FormatId.FORMAT_01_CINEMATIC_STORY:
            program = Format01CinematicStoryProgram(
                **parts,
                broll_policy=FormatBrollPolicy(required=True, broll_function="foreshadowing_and_contrast"),
                proof_policy=FormatProofPolicy(proof_required=bool(payload.get("proof_object")), proof_surface_required=False),
                memory_object_policy=FormatMemoryObjectPolicy(memory_object_required=bool(payload.get("memory_object"))),
                aroll_story_spine_ref=str(payload.get("a_roll_story_spine", "")),
                emotional_change_map_ref=str(payload.get("emotional_change_map", "")),
                cut_question_chain_refs=list(payload.get("cut_question_chain", [])),
                broll_foreshadowing_pair_refs=list(payload.get("broll_foreshadowing_pairs", [])),
                sonic_story_arc_seed_ref=str(payload.get("sonic_story_arc_seed", "")),
            )
        elif packet.target_format == FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            program = Format02AvatarPaperCutExplainerProgram(
                **parts,
                avatar_performance_policy=FormatAvatarPerformancePolicy(avatar_required=True, allowed_clip_types=["point", "pause", "open_hand_reframe"]),
                teachable_mechanism_ref=str(payload.get("teachable_mechanism", "")),
                concept_node_refs=list(payload.get("concept_nodes", [])),
                diagram_sequence_ref=str(payload.get("diagram_sequence", "")),
                avatar_clip_requirements=list(payload.get("avatar_performance_requirements", [])),
            )
        elif packet.target_format == FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS:
            program = Format03LivingCommentaryReactionProgram(
                **parts,
                proof_policy=FormatProofPolicy(proof_required=True, proof_surface_required=True),
                reaction_surface_policy=FormatReactionSurfacePolicy(reaction_surface_required=True, upper_surface_role="proof_or_quote_surface", lower_surface_role="coach_reaction_surface"),
                proof_or_quote_surface_ref=str(payload.get("proof_or_quote_surface", "")),
                coach_reaction_angle_ref=str(payload.get("coach_reaction_angle", "")),
                rough_notation_target_refs=list(payload.get("rough_notation_targets", [])),
            )
        elif packet.target_format == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            program = Format04ConsciousReactionEditingProgram(
                **parts,
                reaction_surface_policy=FormatReactionSurfacePolicy(reaction_surface_required=True, upper_surface_role="reaction_ui_surface", lower_surface_role="coach_reaction"),
                debate_tension_ref=str(payload.get("debate_tension", "")),
                reaction_ui_surface_ref=str(payload.get("reaction_ui_surface", "")),
                score_state_seed_ref=str(payload.get("score_state_seed", "")),
                meme_mechanism_ref=str(payload.get("meme_mechanism", "")),
            )
        elif packet.target_format == FormatId.SUPERVISUAL:
            program = SuperVisualFormatProgram(
                **parts,
                single_source_truth_ref=str(payload.get("single_source_truth", "")),
                visual_hook_ref=str(payload.get("visual_hook", "")),
                edge_product_ref=str(payload.get("edge_product", "")),
            )
        elif packet.target_format == FormatId.CAROUSEL:
            steps = [
                CarouselSequenceStep(step_index=i + 1, role=item.get("role", f"slide_{i+1}"), viewer_state=item.get("viewer_state", "unknown"), source_ref=item.get("source_ref"))
                for i, item in enumerate(payload.get("sequence_steps", []))
            ]
            program = CarouselFormatProgram(
                **parts,
                carousel_thesis_ref=str(payload.get("carousel_thesis", "")),
                sequence_steps=steps,
                closure_contract_ref=str(payload.get("closure_contract", "")),
            )
        elif packet.target_format == FormatId.MEME_VISUAL:
            program = MemeVisualFormatProgram(
                **parts,
                source_truth_ref=str(payload.get("source_truth", "")),
                compressed_paradox_ref=str(payload.get("compressed_paradox", "")),
                meme_mechanism_ref=str(payload.get("meme_mechanism", "")),
                risk_boundary=str(payload.get("risk", "")),
            )
        elif packet.target_format == FormatId.POLL_VISUAL:
            program = PollVisualFormatProgram(
                **parts,
                poll_question_ref=str(payload.get("question", "")),
                option_refs=list(payload.get("options", [])),
                discussion_value=str(payload.get("discussion_value", "medium")),
            )
        elif packet.target_format == FormatId.REACTION_SEED:
            program = ReactionSeedFormatProgram(
                **parts,
                source_quote_ref=str(payload.get("source_quote", "")),
                reaction_question_ref=str(payload.get("reaction_question", "")),
                compatible_reaction_formats=list(payload.get("compatible_reaction_formats", [])),
            )
        else:
            raise ValueError(f"Unsupported format {packet.target_format}")

        return self.repository.upsert("programs", program.format_intelligence_program_id, program)

    def authorize_format_program(self, program) -> FormatCommanderVerdict:
        blockers = []
        repair_commands = []
        if program.ingredient_checklist.missing_required:
            blockers.append("missing_required_ingredients")
            for missing in program.ingredient_checklist.missing_required:
                repair_commands.append(FormatRepairCommand(command_type="supply_missing_ingredient", reason=missing.missing_reason or missing.ingredient_type.value))
        if program.format_id == FormatId.FORMAT_01_CINEMATIC_STORY and program.broll_policy and program.broll_policy.forbid_filler is False:
            blockers.append("format01_broll_filler_risk")
        verdict = FormatCommanderVerdict(
            authorized=not blockers,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
            repair_commands=repair_commands,
        )
        program.commander_verdict = verdict
        program.status = "authorized" if verdict.authorized else "blocked"
        self.repository.upsert("programs", program.format_intelligence_program_id, program)
        return self.repository.upsert("verdicts", verdict.commander_verdict_id, verdict)

    def compile_engine_adapter_payload(self, program) -> EngineAdapterPayload:
        if not program.commander_verdict or not program.commander_verdict.authorized:
            raise ValueError("Engine adapter payload requires authorized format program")
        payload = {
            "format_id": program.format_id.value,
            "sub_format_id": program.sub_format_id,
            "composition_grammar": program.composition_grammar.model_dump(),
            "layer_stack": program.layer_stack_spec.model_dump(),
            "style_route_policy": program.style_route_policy.model_dump(),
            "eval_gates": program.eval_gate_set.model_dump(),
            "render_requirement": program.render_requirement.model_dump(),
        }
        adapter = EngineAdapterPayload(
            format_program_id=program.format_intelligence_program_id,
            engine_target=program.render_requirement.engine_target,
            payload_kind=f"{program.format_id.value}_engine_payload",
            source_span_refs=program.source_span_refs,
            payload=payload,
            commander_verdict_id=program.commander_verdict.commander_verdict_id,
        )
        return self.repository.upsert("adapter_payloads", adapter.engine_adapter_payload_id, adapter)

    # Internal helpers
    def _default_sub_format(self, packet: GenericExtractionPacketRef) -> str:
        defaults = {
            FormatId.FORMAT_01_CINEMATIC_STORY: "relief_peak_story",
            FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER: "scene_to_principle_explainer",
            FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS: "quote_commentary_reaction",
            FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING: "myth_debunk_reaction",
            FormatId.SUPERVISUAL: "memory_object_supervisual",
            FormatId.CAROUSEL: "relief_peak_carousel",
            FormatId.MEME_VISUAL: "micro_contradiction",
            FormatId.POLL_VISUAL: "tension_poll",
            FormatId.REACTION_SEED: "validation_reaction_seed",
        }
        return defaults[packet.target_format]

    def _attention_path(self, format_id: FormatId) -> list[str]:
        if format_id == FormatId.FORMAT_01_CINEMATIC_STORY:
            return ["face", "pause", "memory_object", "power_phrase", "face_return"]
        if format_id == FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS:
            return ["proof_surface", "coach_reaction", "annotation", "caption"]
        if format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            return ["reaction_ui", "score_state", "coach_reaction", "meme_anchor"]
        return ["headline", "hero_visual", "supporting_detail"]

    def _text_policy(self, format_id: FormatId) -> str:
        if format_id == FormatId.FORMAT_01_CINEMATIC_STORY:
            return "power_phrase_sparse"
        if format_id == FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            return "concept_label_sequence"
        if format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            return "high_readability_ui_labels"
        return "source_faithful"
