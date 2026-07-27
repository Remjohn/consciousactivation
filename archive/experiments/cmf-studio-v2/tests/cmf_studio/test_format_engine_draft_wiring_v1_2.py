import pytest

from ccp_studio.contracts.format_engine_draft_wiring import CarouselDraftVariantState, SuperVisualDraftState
from ccp_studio.contracts.format_intelligence import EngineTarget, FormatId, GenericExtractionPacketRef
from ccp_studio.services.carousel_format_draft_wiring_service import CarouselFormatDraftWiringService
from ccp_studio.services.carousel_engine_service import CarouselEngineService
from ccp_studio.services.format_engine_draft_wiring_service import FormatEngineDraftWiringService
from ccp_studio.services.format_intelligence_service import FormatIntelligenceService
from ccp_studio.services.supervisual_format_draft_wiring_service import SuperVisualFormatDraftWiringService
from ccp_studio.services.supervisual_format_program_adapter_service import (
    CarouselFormatProgramAdapterService,
    SuperVisualFormatProgramAdapterService,
)


def _format_service_and_context():
    service = FormatIntelligenceService()
    ctx = service.hydrate_context(brand_id="brand_1", brand_context_version_id="bcv_1")
    return service, ctx


def _supervisual_adapter_input():
    service, ctx = _format_service_and_context()
    packet = GenericExtractionPacketRef(
        extraction_packet_id="sv_packet_1",
        target_format=FormatId.SUPERVISUAL,
        source_span_refs=["span_1"],
        payload={
            "single_source_truth": "I built a life with no recovery margins.",
            "visual_hook": "A planner so full it becomes evidence.",
            "edge_product": "Capacity without recovery is extraction.",
        },
    )
    program = service.compile_format_program(ctx, packet)
    service.authorize_format_program(program)
    adapter_input, _ = SuperVisualFormatProgramAdapterService().adapt(program)
    return adapter_input


def _carousel_adapter_input():
    service, ctx = _format_service_and_context()
    packet = GenericExtractionPacketRef(
        extraction_packet_id="carousel_packet_1",
        target_format=FormatId.CAROUSEL,
        source_span_refs=["span_1"],
        payload={
            "carousel_thesis": "Burnout is not always weakness.",
            "viewer_state_sequence": ["entry", "payoff"],
            "closure_contract": "Source-faithful reframe.",
            "sequence_steps": [
                {"role": "cover", "viewer_state": "entry", "source_ref": "span_1"},
                {"role": "payoff", "viewer_state": "payoff", "source_ref": "span_1"},
            ],
        },
    )
    program = service.compile_format_program(ctx, packet)
    service.authorize_format_program(program)
    adapter_input, _ = CarouselFormatProgramAdapterService().adapt(program)
    return adapter_input


def test_supervisual_adapter_input_builds_supervisual_draft_state():
    adapter_input = _supervisual_adapter_input()
    draft, receipt = SuperVisualFormatDraftWiringService().build_from_format_adapter_input(adapter_input)
    assert isinstance(draft, SuperVisualDraftState)
    assert draft.brand_context_version_id == "bcv_1"
    assert draft.source_span_refs == ["span_1"]
    assert draft.engine_target == EngineTarget.SUPERVISUAL_ENGINE
    assert not draft.provider_calls_executed
    assert not draft.render_executed
    assert receipt.pass_status == "pass"


def test_carousel_adapter_input_creates_carousel_draft_variant_state():
    adapter_input = _carousel_adapter_input()
    draft, receipt = CarouselFormatDraftWiringService().create_variant_from_format_adapter_input(adapter_input)
    assert isinstance(draft, CarouselDraftVariantState)
    assert draft.brand_context_version_id == "bcv_1"
    assert draft.source_span_refs == ["span_1"]
    assert draft.engine_target == EngineTarget.CAROUSEL_ENGINE
    assert draft.slide_count_hint == 2
    assert not draft.provider_calls_executed
    assert not draft.render_executed
    assert receipt.pass_status == "pass"


def test_generic_draft_wiring_service_routes_supervisual_and_carousel_inputs():
    sv_input = _supervisual_adapter_input()
    carousel_input = _carousel_adapter_input()
    result = FormatEngineDraftWiringService().create_batch([sv_input, carousel_input])
    assert result.pass_status == "pass"
    assert len(result.supervisual_drafts) == 1
    assert len(result.carousel_drafts) == 1
    assert len(result.receipts) == 2


def test_draft_wiring_rejects_missing_source_refs_for_supervisual_state():
    adapter_input = _supervisual_adapter_input()
    data = adapter_input.model_dump() if hasattr(adapter_input, "model_dump") else adapter_input.dict()
    data["source_span_refs"] = []
    with pytest.raises(Exception):
        SuperVisualDraftState(**data)


def test_draft_wiring_rejects_non_continuous_carousel_steps():
    adapter_input = _carousel_adapter_input()
    data = adapter_input.model_dump() if hasattr(adapter_input, "model_dump") else adapter_input.dict()
    data["sequence_steps"] = [
        {"step_index": 1, "role": "cover", "viewer_state": "entry"},
        {"step_index": 3, "role": "payoff", "viewer_state": "payoff"},
    ]
    with pytest.raises(Exception):
        CarouselDraftVariantState(
            brand_id=data["brand_id"],
            brand_context_version_id=data["brand_context_version_id"],
            format_program_id=data["format_program_id"],
            source_extraction_packet_id=data["source_extraction_packet_id"],
            source_span_refs=data["source_span_refs"],
            carousel_thesis_ref=data["carousel_thesis_ref"],
            sequence_steps=data["sequence_steps"],
            closure_contract_ref=data["closure_contract_ref"],
            composition_grammar=data["composition_grammar"],
            layer_stack=data["layer_stack"],
            style_routes_allowed=data["style_routes_allowed"],
            style_routes_forbidden=data["style_routes_forbidden"],
            frame_profile=data["frame_profile"],
            eval_gates=data["eval_gates"],
            render_requirement=data["render_requirement"],
            slide_count_hint=2,
        )


def test_carousel_engine_service_create_variant_from_format_adapter_input():
    adapter_input = _carousel_adapter_input()
    draft, receipt = CarouselEngineService().create_variant_from_format_adapter_input(adapter_input)
    assert isinstance(draft, CarouselDraftVariantState)
    assert draft.brand_context_version_id == "bcv_1"
    assert draft.source_span_refs == ["span_1"]
    assert not draft.provider_calls_executed
    assert not draft.render_executed
    assert receipt.pass_status == "pass"
