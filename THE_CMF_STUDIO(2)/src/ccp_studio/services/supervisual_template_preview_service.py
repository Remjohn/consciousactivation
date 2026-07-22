from __future__ import annotations

from ccp_studio.contracts.template_preview_atlas import (
    SuperVisualTemplatePreview,
    TemplateFormat,
    TemplatePreviewRequest,
    svg_to_data_uri,
)


class SuperVisualTemplatePreviewService:
    def compile_preview(self, request: TemplatePreviewRequest) -> SuperVisualTemplatePreview:
        values = request.sample_payload.values
        svg = self._svg(values)
        return SuperVisualTemplatePreview(
            template_id=request.template_id,
            template_format=TemplateFormat.SUPERVISUAL,
            frame_profile=request.slot_map.frame_profile,
            slot_labels={slot.slot_key: slot.label for slot in request.slot_map.slots},
            sample_values=values,
            preview_svg=svg,
            thumbnail_uri=svg_to_data_uri(svg),
            single_source_truth=str(values["source_truth"]),
            hero_object_label=str(values["hero_object"]),
            power_phrase=str(values["power_phrase"]),
        )

    def _svg(self, values: dict) -> str:
        source = str(values.get("source_truth", "Source truth"))
        hero = str(values.get("hero_object", "Hero object"))
        phrase = str(values.get("power_phrase", "Power phrase"))
        brand = str(values.get("brand_mark", "CCP"))
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900">
  <rect width="900" height="900" rx="60" fill="#f4ead7"/>
  <rect x="80" y="80" width="740" height="740" rx="44" fill="#fff8e8" stroke="#2f2b24" stroke-width="4"/>
  <rect x="130" y="150" width="330" height="330" rx="36" fill="#d7e8c7" stroke="#2f2b24" stroke-width="3"/>
  <text x="295" y="320" text-anchor="middle" font-size="32" font-family="Arial">{hero}</text>
  <text x="500" y="200" font-size="42" font-family="Arial" font-weight="700">{phrase}</text>
  <text x="500" y="280" font-size="24" font-family="Arial">{source[:52]}</text>
  <circle cx="740" cy="740" r="46" fill="#2f2b24"/>
  <text x="740" y="752" text-anchor="middle" font-size="28" fill="#fff8e8" font-family="Arial">{brand}</text>
</svg>"""
