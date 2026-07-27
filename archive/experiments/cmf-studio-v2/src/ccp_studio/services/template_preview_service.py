from __future__ import annotations

from ccp_studio.contracts.template_preview_atlas import TemplateFormat, TemplatePreviewRequest
from ccp_studio.services.carousel_template_preview_service import CarouselTemplatePreviewService
from ccp_studio.services.format02_template_preview_service import Format02TemplatePreviewService
from ccp_studio.services.supervisual_template_preview_service import SuperVisualTemplatePreviewService


class TemplatePreviewService:
    def __init__(
        self,
        supervisual_service: SuperVisualTemplatePreviewService | None = None,
        carousel_service: CarouselTemplatePreviewService | None = None,
        format02_service: Format02TemplatePreviewService | None = None,
    ):
        self.supervisual = supervisual_service or SuperVisualTemplatePreviewService()
        self.carousel = carousel_service or CarouselTemplatePreviewService()
        self.format02 = format02_service or Format02TemplatePreviewService()

    def compile_preview(self, request: TemplatePreviewRequest):
        if request.template_format == TemplateFormat.SUPERVISUAL:
            return self.supervisual.compile_preview(request)
        if request.template_format == TemplateFormat.CAROUSEL:
            return self.carousel.compile_preview(request)
        if request.template_format == TemplateFormat.FORMAT02_SCENE:
            return self.format02.compile_preview(request)
        raise ValueError(f"Unsupported template format: {request.template_format}")
