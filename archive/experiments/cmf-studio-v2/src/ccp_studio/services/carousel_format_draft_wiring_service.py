from __future__ import annotations

from ccp_studio.contracts.format_engine_draft_wiring import (
    CarouselDraftVariantState,
    FormatEngineDraftWiringReceipt,
)
from ccp_studio.contracts.format_intelligence import EngineTarget, PassStatus
from ccp_studio.contracts.supervisual_carousel_format_adapters import CarouselEngineFormatAdapterInput


class CarouselFormatDraftWiringService:
    def create_variant_from_format_adapter_input(
        self,
        adapter_input: CarouselEngineFormatAdapterInput,
    ) -> tuple[CarouselDraftVariantState, FormatEngineDraftWiringReceipt]:
        draft = CarouselDraftVariantState(
            brand_id=adapter_input.brand_id,
            brand_context_version_id=adapter_input.brand_context_version_id,
            format_program_id=adapter_input.format_program_id,
            source_extraction_packet_id=adapter_input.source_extraction_packet_id,
            source_span_refs=adapter_input.source_span_refs,
            carousel_thesis_ref=adapter_input.carousel_thesis_ref,
            sequence_steps=adapter_input.sequence_steps,
            closure_contract_ref=adapter_input.closure_contract_ref,
            composition_grammar=adapter_input.composition_grammar,
            layer_stack=adapter_input.layer_stack,
            style_routes_allowed=adapter_input.style_routes_allowed,
            style_routes_forbidden=adapter_input.style_routes_forbidden,
            frame_profile=adapter_input.frame_profile,
            eval_gates=adapter_input.eval_gates,
            render_requirement=adapter_input.render_requirement,
            slide_count_hint=len(adapter_input.sequence_steps),
            engine_target=EngineTarget.CAROUSEL_ENGINE,
        )
        receipt = FormatEngineDraftWiringReceipt(
            adapter_input_id=adapter_input.carousel_engine_format_adapter_input_id,
            draft_state_id=draft.carousel_draft_variant_state_id,
            engine_target=EngineTarget.CAROUSEL_ENGINE,
            pass_status=PassStatus.PASS,
        )
        return draft, receipt

    # Alias for naming symmetry.
    def create_draft_variant_from_format_adapter_input(
        self,
        adapter_input: CarouselEngineFormatAdapterInput,
    ) -> tuple[CarouselDraftVariantState, FormatEngineDraftWiringReceipt]:
        return self.create_variant_from_format_adapter_input(adapter_input)
