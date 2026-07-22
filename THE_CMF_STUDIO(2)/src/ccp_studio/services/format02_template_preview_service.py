from __future__ import annotations

from ccp_studio.contracts.template_preview_atlas import (
    Format02SceneTemplatePreview,
    TemplateFormat,
    TemplatePreviewRequest,
    svg_to_data_uri,
)


class Format02TemplatePreviewService:
    def compile_preview(self, request: TemplatePreviewRequest) -> Format02SceneTemplatePreview:
        values = request.sample_payload.values
        svg = self._svg(values)
        return Format02SceneTemplatePreview(
            template_id=request.template_id,
            template_format=TemplateFormat.FORMAT02_SCENE,
            frame_profile=request.slot_map.frame_profile,
            slot_labels={slot.slot_key: slot.label for slot in request.slot_map.slots},
            sample_values=values,
            preview_svg=svg,
            thumbnail_uri=svg_to_data_uri(svg),
            concept_statement=str(values["concept_statement"]),
            headline_text=str(values["headline_text"]),
            avatar_action=str(values["avatar_action"]),
            hero_object=str(values["hero_object"]),
            audience_proxy=str(values["audience_proxy"]),
            sfl_function=str(values["sfl_function"]),
        )

    def _svg(self, values: dict) -> str:
        headline = str(values.get("headline_text", "Headline"))
        avatar_action = str(values.get("avatar_action", "avatar action"))
        hero = str(values.get("hero_object", "real cutout"))
        proxy = str(values.get("audience_proxy", "proxy"))
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <rect width="1080" height="1920" fill="#f4ead7"/>
  <rect x="90" y="120" width="900" height="220" rx="44" fill="#fff8e8" stroke="#2f2b24" stroke-width="4"/>
  <text x="540" y="255" text-anchor="middle" font-size="58" font-family="Arial" font-weight="700">{headline}</text>
  <rect x="105" y="540" width="430" height="430" rx="40" fill="#d7e8c7" stroke="#2f2b24" stroke-width="4"/>
  <text x="320" y="765" text-anchor="middle" font-size="40" font-family="Arial">{hero}</text>
  <circle cx="780" cy="780" r="170" fill="#f1c8b6" stroke="#2f2b24" stroke-width="4"/>
  <text x="780" y="780" text-anchor="middle" font-size="34" font-family="Arial">Avatar</text>
  <text x="780" y="835" text-anchor="middle" font-size="26" font-family="Arial">{avatar_action}</text>
  <rect x="120" y="1220" width="260" height="160" rx="26" fill="#2f2b24"/>
  <text x="250" y="1310" text-anchor="middle" fill="#fff8e8" font-size="30" font-family="Arial">{proxy}</text>
  <rect x="680" y="1260" width="270" height="120" rx="30" fill="#fff8e8" stroke="#2f2b24" stroke-width="3"/>
  <text x="815" y="1332" text-anchor="middle" font-size="28" font-family="Arial">negative space</text>
</svg>"""
