import pytest

from ccp_studio.contracts.format_intelligence import FormatId, EngineTarget, GenericExtractionPacketRef
from ccp_studio.services.format_intelligence_service import FormatIntelligenceService
from ccp_studio.services.supervisual_format_program_adapter_service import (
    CarouselFormatProgramAdapterService,
    SuperVisualFormatProgramAdapterService,
)


def _service_and_context():
    service = FormatIntelligenceService()
    ctx = service.hydrate_context(brand_id="brand_1", brand_context_version_id="bcv_1")
    return service, ctx


def test_supervisual_adapter_consumes_authorized_supervisual_format_program():
    service, ctx = _service_and_context()
    packet = GenericExtractionPacketRef(
        extraction_packet_id="sv_packet_1",
        target_format=FormatId.SUPERVISUAL,
        source_span_refs=["span_1"],
        payload={
            "single_source_truth": "truth",
            "visual_hook": "hook",
            "edge_product": "edge",
        },
    )
    program = service.compile_format_program(ctx, packet)
    service.authorize_format_program(program)
    adapter_input, receipt = SuperVisualFormatProgramAdapterService().adapt(program)
    assert adapter_input.brand_context_version_id == "bcv_1"
    assert adapter_input.source_span_refs == ["span_1"]
    assert adapter_input.engine_target == EngineTarget.SUPERVISUAL_ENGINE
    assert receipt.pass_status == "pass"


def test_supervisual_adapter_rejects_unauthorized_program():
    service, ctx = _service_and_context()
    packet = GenericExtractionPacketRef(
        extraction_packet_id="sv_packet_1",
        target_format=FormatId.SUPERVISUAL,
        source_span_refs=["span_1"],
        payload={
            "single_source_truth": "truth",
            "visual_hook": "hook",
            "edge_product": "edge",
        },
    )
    program = service.compile_format_program(ctx, packet)
    with pytest.raises(Exception):
        SuperVisualFormatProgramAdapterService().adapt(program)


def test_carousel_adapter_consumes_authorized_carousel_format_program():
    service, ctx = _service_and_context()
    packet = GenericExtractionPacketRef(
        extraction_packet_id="carousel_packet_1",
        target_format=FormatId.CAROUSEL,
        source_span_refs=["span_1"],
        payload={
            "carousel_thesis": "thesis",
            "viewer_state_sequence": ["entry", "payoff"],
            "closure_contract": "closure",
            "sequence_steps": [
                {"role": "cover", "viewer_state": "entry", "source_ref": "span_1"},
                {"role": "payoff", "viewer_state": "payoff", "source_ref": "span_1"},
            ],
        },
    )
    program = service.compile_format_program(ctx, packet)
    service.authorize_format_program(program)
    adapter_input, receipt = CarouselFormatProgramAdapterService().adapt(program)
    assert adapter_input.brand_context_version_id == "bcv_1"
    assert adapter_input.engine_target == EngineTarget.CAROUSEL_ENGINE
    assert adapter_input.sequence_steps[0]["step_index"] == 1
    assert adapter_input.closure_contract_ref == "closure"


def test_carousel_adapter_rejects_unauthorized_program():
    service, ctx = _service_and_context()
    packet = GenericExtractionPacketRef(
        extraction_packet_id="carousel_packet_1",
        target_format=FormatId.CAROUSEL,
        source_span_refs=["span_1"],
        payload={
            "carousel_thesis": "thesis",
            "viewer_state_sequence": ["entry"],
            "closure_contract": "closure",
            "sequence_steps": [{"role": "cover", "viewer_state": "entry"}],
        },
    )
    program = service.compile_format_program(ctx, packet)
    with pytest.raises(Exception):
        CarouselFormatProgramAdapterService().adapt(program)
