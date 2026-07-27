from __future__ import annotations

from ccp_studio.contracts.template_preview_atlas import (
    CarouselSlidePreview,
    CarouselTemplatePreview,
    TemplateFormat,
    TemplatePreviewRequest,
    svg_to_data_uri,
)


class CarouselTemplatePreviewService:
    def compile_preview(self, request: TemplatePreviewRequest) -> CarouselTemplatePreview:
        values = request.sample_payload.values
        slides = [CarouselSlidePreview(**slide) for slide in values["slides"]]
        svg = self._svg(values, slides)
        return CarouselTemplatePreview(
            template_id=request.template_id,
            template_format=TemplateFormat.CAROUSEL,
            frame_profile=request.slot_map.frame_profile,
            slot_labels={slot.slot_key: slot.label for slot in request.slot_map.slots},
            sample_values=values,
            preview_svg=svg,
            thumbnail_uri=svg_to_data_uri(svg),
            carousel_thesis=str(values["carousel_thesis"]),
            closure_contract=str(values["closure_contract"]),
            slides=slides,
        )

    def _svg(self, values: dict, slides: list[CarouselSlidePreview]) -> str:
        cards = []
        x = 50
        for slide in slides:
            cards.append(f"""<rect x="{x}" y="160" width="250" height="420" rx="28" fill="#fff8e8" stroke="#2f2b24" stroke-width="3"/>
  <text x="{x+24}" y="215" font-size="24" font-family="Arial" font-weight="700">{slide.slide_index}. {slide.role}</text>
  <text x="{x+24}" y="285" font-size="26" font-family="Arial">{slide.headline[:22]}</text>""")
            x += 280
        thesis = str(values.get("carousel_thesis", "Carousel thesis"))
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720">
  <rect width="960" height="720" fill="#efe4d0"/>
  <text x="50" y="90" font-size="42" font-family="Arial" font-weight="700">{thesis[:48]}</text>
  {''.join(cards)}
</svg>"""
