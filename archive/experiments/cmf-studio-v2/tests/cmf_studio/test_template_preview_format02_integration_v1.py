import pytest

from ccp_studio.contracts.format02_composition_intelligence import Format02SceneRole
from ccp_studio.contracts.template_preview_atlas import TemplateFormat, TemplateSamplePayload
from ccp_studio.services.format02_composition_service import Format02CompositionService
from ccp_studio.services.template_atlas_service import TemplateAtlasService


def _format02_payload(headline_text="Natural does not always mean safe."):
    return TemplateSamplePayload(
        template_format=TemplateFormat.FORMAT02_SCENE,
        values={
            "concept_statement": "Natural products still need dosage context.",
            "headline_text": headline_text,
            "avatar_action": "raise_finger",
            "hero_object": "tea cup cutout",
            "audience_proxy": "confused_seeker",
            "sfl_function": "relevant_open_question",
        },
    )


def test_format02_template_preview_preserves_scene_slots_for_composition():
    atlas = TemplateAtlasService()
    slot_map = atlas.default_format02_slot_map()
    preview = atlas.compile_preview_from_payload(slot_map=slot_map, payload=_format02_payload())

    scene = Format02CompositionService().compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="scene_1",
        scene_role=Format02SceneRole.TRUTH_DEFINE,
        concept_statement=preview.concept_statement,
        headline_text=preview.headline_text,
        avatar_action_ref=preview.avatar_action,
        hero_object_asset_id="asset_tea_cup",
        hero_object_source_ref="source_ref_tea_cup",
        audience_proxy_sfl_function=preview.sfl_function,
    )

    assert preview.avatar_action == "raise_finger"
    assert preview.hero_object == "tea cup cutout"
    assert preview.audience_proxy == "confused_seeker"
    assert preview.sfl_function == "relevant_open_question"
    assert scene.concept_unit.concept_statement == preview.concept_statement
    assert scene.composition_scene_program.text_placement_plan.max_visible_words == 14


def test_format02_template_preview_enforces_visible_word_budget_before_composition():
    atlas = TemplateAtlasService()
    slot_map = atlas.default_format02_slot_map()
    with pytest.raises(Exception):
        atlas.compile_preview_from_payload(
            slot_map=slot_map,
            payload=_format02_payload(
                "This headline contains too many visible words for a format two template preview budget today"
            ),
        )
