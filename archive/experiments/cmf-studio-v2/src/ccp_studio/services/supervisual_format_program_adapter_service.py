from __future__ import annotations

from ccp_studio.contracts.format_intelligence import (
    CarouselFormatProgram,
    EngineTarget,
    FormatId,
    PassStatus,
    SuperVisualFormatProgram,
)
from ccp_studio.contracts.supervisual_carousel_format_adapters import (
    CarouselEngineFormatAdapterInput,
    FormatAdapterReceipt,
    SuperVisualBuilderFormatAdapterInput,
)


def _dump_model(model):
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


class SuperVisualFormatProgramAdapterService:
    def adapt(self, program: SuperVisualFormatProgram) -> tuple[SuperVisualBuilderFormatAdapterInput, FormatAdapterReceipt]:
        self._assert_authorized(program)
        if program.format_id != FormatId.SUPERVISUAL:
            raise ValueError("SuperVisual adapter requires SuperVisualFormatProgram")
        style_policy = program.style_route_policy
        render_req = program.render_requirement
        adapter_input = SuperVisualBuilderFormatAdapterInput(
            brand_id=program.brand_id,
            brand_context_version_id=program.brand_context_version_id,
            format_program_id=program.format_intelligence_program_id,
            source_extraction_packet_id=program.source_extraction_packet_id,
            source_span_refs=program.source_span_refs,
            single_source_truth_ref=program.single_source_truth_ref,
            visual_hook_ref=program.visual_hook_ref,
            edge_product_ref=program.edge_product_ref,
            composition_grammar=_dump_model(program.composition_grammar),
            layer_stack=_dump_model(program.layer_stack_spec),
            style_routes_allowed=[route.value for route in style_policy.primary_routes + style_policy.secondary_routes],
            style_routes_forbidden=[route.value for route in style_policy.forbidden_routes],
            negative_space_policy=program.composition_grammar.negative_space_policy,
            frame_profile=render_req.frame_profile.value,
            eval_gates=program.eval_gate_set.gates,
            render_requirement=_dump_model(render_req),
            commander_verdict_id=program.commander_verdict.commander_verdict_id,
        )
        receipt = FormatAdapterReceipt(
            format_program_id=program.format_intelligence_program_id,
            adapter_input_id=adapter_input.supervisual_builder_format_adapter_input_id,
            engine_target=EngineTarget.SUPERVISUAL_ENGINE,
            pass_status=PassStatus.PASS,
        )
        return adapter_input, receipt

    def _assert_authorized(self, program):
        if not program.commander_verdict or not program.commander_verdict.authorized:
            raise ValueError("Format program must be authorized before adapter consumption")


class CarouselFormatProgramAdapterService:
    def adapt(self, program: CarouselFormatProgram) -> tuple[CarouselEngineFormatAdapterInput, FormatAdapterReceipt]:
        self._assert_authorized(program)
        if program.format_id != FormatId.CAROUSEL:
            raise ValueError("Carousel adapter requires CarouselFormatProgram")
        style_policy = program.style_route_policy
        render_req = program.render_requirement
        adapter_input = CarouselEngineFormatAdapterInput(
            brand_id=program.brand_id,
            brand_context_version_id=program.brand_context_version_id,
            format_program_id=program.format_intelligence_program_id,
            source_extraction_packet_id=program.source_extraction_packet_id,
            source_span_refs=program.source_span_refs,
            carousel_thesis_ref=program.carousel_thesis_ref,
            sequence_steps=[_dump_model(step) for step in program.sequence_steps],
            closure_contract_ref=program.closure_contract_ref,
            composition_grammar=_dump_model(program.composition_grammar),
            layer_stack=_dump_model(program.layer_stack_spec),
            style_routes_allowed=[route.value for route in style_policy.primary_routes + style_policy.secondary_routes],
            style_routes_forbidden=[route.value for route in style_policy.forbidden_routes],
            frame_profile=render_req.frame_profile.value,
            eval_gates=program.eval_gate_set.gates,
            render_requirement=_dump_model(render_req),
            commander_verdict_id=program.commander_verdict.commander_verdict_id,
        )
        receipt = FormatAdapterReceipt(
            format_program_id=program.format_intelligence_program_id,
            adapter_input_id=adapter_input.carousel_engine_format_adapter_input_id,
            engine_target=EngineTarget.CAROUSEL_ENGINE,
            pass_status=PassStatus.PASS,
        )
        return adapter_input, receipt

    def _assert_authorized(self, program):
        if not program.commander_verdict or not program.commander_verdict.authorized:
            raise ValueError("Format program must be authorized before adapter consumption")
