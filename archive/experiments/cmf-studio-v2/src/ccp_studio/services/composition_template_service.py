from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import (
    CompositionRole,
    CompositionTemplate,
    FrameFormatProfile,
    SceneTemplate,
)


class CompositionTemplateService:
    def get_format02_template(self, template_name: str = "format02_avatar_object_card") -> CompositionTemplate:
        return CompositionTemplate(
            template_name=template_name,
            format_id="format_02_avatar_papercut_explainer",
            frame_profile=FrameFormatProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER,
            required_roles=[
                CompositionRole.TEXT_ANCHOR,
                CompositionRole.AVATAR,
                CompositionRole.HERO_OBJECT,
            ],
            minimum_negative_space_ratio=0.30,
        )

    def get_format02_scene_template(self, scene_role: str) -> SceneTemplate:
        return SceneTemplate(
            scene_role=scene_role,
            template_name=f"{scene_role}_template",
            allowed_composition_templates=["format02_avatar_object_card"],
            default_attention_path=["headline", "hero_object", "avatar", "audience_proxy"],
        )
