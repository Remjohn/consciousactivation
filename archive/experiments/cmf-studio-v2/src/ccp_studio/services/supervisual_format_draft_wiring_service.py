from __future__ import annotations

from ccp_studio.contracts.format_engine_draft_wiring import (
    FormatEngineDraftWiringReceipt,
    SuperVisualDraftState,
)
from ccp_studio.contracts.format_intelligence import EngineTarget, PassStatus
from ccp_studio.contracts.supervisual_carousel_format_adapters import SuperVisualBuilderFormatAdapterInput


class SuperVisualFormatDraftWiringService:
    def build_from_format_adapter_input(
        self,
        adapter_input: SuperVisualBuilderFormatAdapterInput,
    ) -> tuple[SuperVisualDraftState, FormatEngineDraftWiringReceipt]:
        draft = SuperVisualDraftState(
            brand_id=adapter_input.brand_id,
            brand_context_version_id=adapter_input.brand_context_version_id,
            format_program_id=adapter_input.format_program_id,
            source_extraction_packet_id=adapter_input.source_extraction_packet_id,
            source_span_refs=adapter_input.source_span_refs,
            single_source_truth_ref=adapter_input.single_source_truth_ref,
            visual_hook_ref=adapter_input.visual_hook_ref,
            edge_product_ref=adapter_input.edge_product_ref,
            composition_grammar=adapter_input.composition_grammar,
            layer_stack=adapter_input.layer_stack,
            style_routes_allowed=adapter_input.style_routes_allowed,
            style_routes_forbidden=adapter_input.style_routes_forbidden,
            negative_space_policy=adapter_input.negative_space_policy,
            frame_profile=adapter_input.frame_profile,
            eval_gates=adapter_input.eval_gates,
            render_requirement=adapter_input.render_requirement,
            engine_target=EngineTarget.SUPERVISUAL_ENGINE,
        )
        receipt = FormatEngineDraftWiringReceipt(
            adapter_input_id=adapter_input.supervisual_builder_format_adapter_input_id,
            draft_state_id=draft.supervisual_draft_state_id,
            engine_target=EngineTarget.SUPERVISUAL_ENGINE,
            pass_status=PassStatus.PASS,
        )
        return draft, receipt

    # Alias for older naming preference.
    def build_draft_from_format_adapter_input(
        self,
        adapter_input: SuperVisualBuilderFormatAdapterInput,
    ) -> tuple[SuperVisualDraftState, FormatEngineDraftWiringReceipt]:
        return self.build_from_format_adapter_input(adapter_input)
