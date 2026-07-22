from __future__ import annotations

from ccp_studio.contracts.format_intelligence import (
    FormatId,
    FormatIntelligenceContext,
    GenericExtractionPacketRef,
)
from ccp_studio.contracts.narrative_format_bridge import (
    BridgeStatus,
    FormatProgramCompileReceipt,
    NarrativePacketBridgeRef,
    NarrativePacketKind,
    NarrativeToFormatBridgeReceipt,
    NarrativeToFormatBridgeRequest,
)
from ccp_studio.contracts.narrative_story_doctor import (
    CarouselExtractionPacket,
    Format01StoryExtractionPacket,
    Format02ExplainerExtractionPacket,
    Format03ReactionExtractionPacket,
    Format04ConsciousReactionExtractionPacket,
    MemeVisualExtractionPacket,
    PollVisualExtractionPacket,
    ReactionSeedPacket,
    SuperVisualExtractionPacket,
)
from ccp_studio.services.format_intelligence_service import FormatIntelligenceService


class NarrativeToFormatBridgeService:
    def __init__(self, format_service: FormatIntelligenceService | None = None):
        self.format_service = format_service or FormatIntelligenceService()

    def make_context(self, request: NarrativeToFormatBridgeRequest) -> FormatIntelligenceContext:
        return self.format_service.hydrate_context(
            brand_id=request.brand_id,
            brand_context_version_id=request.brand_context_version_id,
            source_extraction_run_id=request.source_extraction_run_id,
            archetype_program_id=request.archetype_program_id,
            primitive_coalition_candidate_id=request.primitive_coalition_candidate_id,
            delivery_recipe_program_id=request.delivery_recipe_program_id,
            target_formats=[ref.target_format for ref in request.packet_refs],
        )

    def to_generic_extraction_packet_ref(self, ref: NarrativePacketBridgeRef) -> GenericExtractionPacketRef:
        return GenericExtractionPacketRef(
            extraction_packet_id=ref.packet_id,
            target_format=ref.target_format,
            sub_format_hint=ref.sub_format_hint,
            source_span_refs=ref.source_span_refs,
            payload=ref.extraction_payload,
        )

    def ref_from_supervisual(self, packet: SuperVisualExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.SUPERVISUAL,
            packet_id=packet.supervisual_extraction_packet_id,
            target_format=FormatId.SUPERVISUAL,
            source_span_refs=packet.source_span_refs,
            sub_format_hint="memory_object_supervisual",
            extraction_payload={
                "single_source_truth": packet.single_source_truth,
                "visual_hook": packet.visual_hook_candidate,
                "edge_product": packet.edge_product,
                "proof_object": packet.proof_object_candidate,
                "memory_object": packet.memory_object_candidate,
                "style_route_hint": packet.style_route_hint,
            },
        )

    def ref_from_carousel(self, packet: CarouselExtractionPacket) -> NarrativePacketBridgeRef:
        sequence_steps = [
            {
                "role": slide.role,
                "viewer_state": packet.viewer_state_sequence[min(slide.slide_index - 1, len(packet.viewer_state_sequence) - 1)].value if packet.viewer_state_sequence else "unknown",
                "source_ref": slide.source_ref,
            }
            for slide in packet.slides
        ]
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.CAROUSEL,
            packet_id=packet.carousel_extraction_packet_id,
            target_format=FormatId.CAROUSEL,
            source_span_refs=packet.source_span_refs,
            sub_format_hint="relief_peak_carousel",
            extraction_payload={
                "carousel_thesis": packet.carousel_thesis,
                "viewer_state_sequence": [state.value for state in packet.viewer_state_sequence],
                "closure_contract": packet.closure_contract,
                "sequence_steps": sequence_steps,
                "visual_system_seed": packet.visual_system_seed,
            },
        )

    def ref_from_format01(self, packet: Format01StoryExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.FORMAT01,
            packet_id=packet.format01_packet_id,
            target_format=FormatId.FORMAT_01_CINEMATIC_STORY,
            source_span_refs=packet.aroll_story_spine.source_span_refs,
            sub_format_hint=packet.sub_format,
            extraction_payload={
                "a_roll_story_spine": packet.aroll_story_spine.aroll_story_spine_id,
                "emotional_change_map": packet.emotional_change_map.emotional_change_map_id,
                "cut_question_chain": [cut.cut_question_contract_id for cut in packet.cut_question_chain],
                "broll_foreshadowing_pairs": [pair.broll_foreshadowing_pair_id for pair in packet.broll_foreshadowing_pairs],
                "sonic_story_arc_seed": packet.sonic_story_arc_seed.sonic_story_arc_seed_id,
                "memory_object": packet.memory_object_candidates[0] if packet.memory_object_candidates else None,
            },
        )

    def ref_from_format02(self, packet: Format02ExplainerExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.FORMAT02,
            packet_id=packet.format02_packet_id,
            target_format=FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER,
            source_span_refs=packet.source_span_refs,
            sub_format_hint=packet.sub_format,
            extraction_payload={
                "teachable_mechanism": packet.teachable_mechanism,
                "concept_nodes": packet.concept_nodes,
                "diagram_sequence": "|".join(packet.diagram_sequence),
                "avatar_performance_requirements": packet.avatar_performance_requirements,
            },
        )

    def ref_from_format03(self, packet: Format03ReactionExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.FORMAT03,
            packet_id=packet.format03_packet_id,
            target_format=FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS,
            source_span_refs=packet.source_span_refs,
            sub_format_hint=packet.sub_format,
            extraction_payload={
                "proof_or_quote_surface": packet.proof_or_quote_surface,
                "coach_reaction_angle": packet.coach_reaction_angle,
                "rough_notation_targets": packet.rough_notation_targets,
                "reaction_question": packet.reaction_question,
            },
        )

    def ref_from_format04(self, packet: Format04ConsciousReactionExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.FORMAT04,
            packet_id=packet.format04_packet_id,
            target_format=FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING,
            source_span_refs=packet.source_span_refs,
            sub_format_hint=packet.sub_format,
            extraction_payload={
                "debate_tension": packet.debate_tension,
                "reaction_ui_surface": packet.reaction_ui_surface,
                "score_state_seed": packet.score_state_seed,
                "meme_mechanism": packet.meme_mechanism,
            },
        )

    def ref_from_meme(self, packet: MemeVisualExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.MEME,
            packet_id=packet.meme_visual_packet_id,
            target_format=FormatId.MEME_VISUAL,
            source_span_refs=packet.source_span_refs,
            sub_format_hint=packet.sub_format,
            extraction_payload={
                "source_truth": packet.source_truth,
                "compressed_paradox": packet.compressed_paradox,
                "meme_mechanism": packet.meme_mechanism,
                "risk": packet.risk,
            },
        )

    def ref_from_poll(self, packet: PollVisualExtractionPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.POLL,
            packet_id=packet.poll_visual_packet_id,
            target_format=FormatId.POLL_VISUAL,
            source_span_refs=packet.source_span_refs,
            sub_format_hint=packet.sub_format,
            extraction_payload={
                "question": packet.question,
                "options": packet.options,
                "poll_options": packet.options,
                "discussion_value": packet.discussion_value,
            },
        )

    def ref_from_reaction_seed(self, packet: ReactionSeedPacket) -> NarrativePacketBridgeRef:
        return NarrativePacketBridgeRef(
            packet_kind=NarrativePacketKind.REACTION_SEED,
            packet_id=packet.reaction_seed_id,
            target_format=FormatId.REACTION_SEED,
            source_span_refs=packet.source_span_refs,
            sub_format_hint="validation_reaction_seed",
            extraction_payload={
                "source_quote": packet.source_quote,
                "reaction_question": packet.reaction_question,
                "compatible_reaction_formats": packet.compatible_reaction_formats,
            },
        )

    def compile_one(self, context: FormatIntelligenceContext, ref: NarrativePacketBridgeRef):
        generic = self.to_generic_extraction_packet_ref(ref)
        program = self.format_service.compile_format_program(context, generic)
        verdict = self.format_service.authorize_format_program(program)
        adapter = None
        status = BridgeStatus.AUTHORIZED if verdict.authorized else BridgeStatus.COMPILED
        if verdict.authorized:
            adapter = self.format_service.compile_engine_adapter_payload(program)
            status = BridgeStatus.ADAPTED
        receipt = FormatProgramCompileReceipt(
            packet_id=ref.packet_id,
            target_format=ref.target_format,
            generic_extraction_packet_id=generic.extraction_packet_id,
            format_program_id=program.format_intelligence_program_id,
            commander_verdict_id=verdict.commander_verdict_id,
            engine_adapter_payload_id=adapter.engine_adapter_payload_id if adapter else None,
            status=status,
        )
        return program, verdict, adapter, receipt

    def compile_batch(self, request: NarrativeToFormatBridgeRequest) -> NarrativeToFormatBridgeReceipt:
        context = self.make_context(request)
        receipts = []
        adapters = []
        blockers = []
        for ref in request.packet_refs:
            try:
                _, verdict, adapter, receipt = self.compile_one(context, ref)
                receipts.append(receipt)
                if adapter:
                    adapters.append(adapter)
                if verdict.blockers:
                    blockers.extend(verdict.blockers)
            except Exception as exc:
                blockers.append(f"{ref.packet_id}: {exc}")
        status = BridgeStatus.FAILED if blockers else BridgeStatus.ADAPTED
        return NarrativeToFormatBridgeReceipt(
            request_id=request.narrative_to_format_bridge_request_id,
            compile_receipts=receipts,
            engine_adapter_payloads=adapters,
            status=status,
            blockers=blockers,
        )
