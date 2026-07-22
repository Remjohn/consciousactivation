from __future__ import annotations

from ccp_studio.contracts.format_engine_draft_wiring import FormatEngineDraftWiringBatchResult
from ccp_studio.contracts.format_intelligence import EngineTarget, PassStatus
from ccp_studio.contracts.supervisual_carousel_format_adapters import (
    CarouselEngineFormatAdapterInput,
    SuperVisualBuilderFormatAdapterInput,
)
from ccp_studio.services.carousel_format_draft_wiring_service import CarouselFormatDraftWiringService
from ccp_studio.services.supervisual_format_draft_wiring_service import SuperVisualFormatDraftWiringService


class FormatEngineDraftWiringService:
    def __init__(
        self,
        supervisual_service: SuperVisualFormatDraftWiringService | None = None,
        carousel_service: CarouselFormatDraftWiringService | None = None,
    ):
        self.supervisual_service = supervisual_service or SuperVisualFormatDraftWiringService()
        self.carousel_service = carousel_service or CarouselFormatDraftWiringService()

    def create_draft_from_adapter_input(self, adapter_input):
        if isinstance(adapter_input, SuperVisualBuilderFormatAdapterInput):
            return self.supervisual_service.build_from_format_adapter_input(adapter_input)
        if isinstance(adapter_input, CarouselEngineFormatAdapterInput):
            return self.carousel_service.create_variant_from_format_adapter_input(adapter_input)
        raise TypeError(f"Unsupported adapter input type: {type(adapter_input)!r}")

    def create_batch(self, adapter_inputs: list) -> FormatEngineDraftWiringBatchResult:
        supervisual_drafts = []
        carousel_drafts = []
        receipts = []
        blockers = []
        for adapter_input in adapter_inputs:
            try:
                draft, receipt = self.create_draft_from_adapter_input(adapter_input)
                receipts.append(receipt)
                if receipt.engine_target == EngineTarget.SUPERVISUAL_ENGINE:
                    supervisual_drafts.append(draft)
                elif receipt.engine_target == EngineTarget.CAROUSEL_ENGINE:
                    carousel_drafts.append(draft)
            except Exception as exc:
                blockers.append(str(exc))
        return FormatEngineDraftWiringBatchResult(
            supervisual_drafts=supervisual_drafts,
            carousel_drafts=carousel_drafts,
            receipts=receipts,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )
