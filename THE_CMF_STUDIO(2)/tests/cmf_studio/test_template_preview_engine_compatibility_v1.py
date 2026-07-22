from ccp_studio.contracts.carousel_engine import CarouselPreviewPack
from ccp_studio.contracts.supervisual_runtime import SuperVisualSnapshot, SuperVisualVariantStatus
from ccp_studio.contracts.template_preview_atlas import TemplateFormat, TemplateSamplePayload
from ccp_studio.services.template_atlas_service import TemplateAtlasService


def test_supervisual_template_preview_can_be_referenced_by_runtime_snapshot_payload():
    atlas = TemplateAtlasService()
    slot_map = atlas.default_supervisual_slot_map()
    preview = atlas.compile_preview_from_payload(
        slot_map=slot_map,
        payload=TemplateSamplePayload(
            template_format=TemplateFormat.SUPERVISUAL,
            values={
                "source_truth": "A single source truth anchors the design.",
                "hero_object": "paperized notebook",
                "power_phrase": "One truth.",
                "brand_mark": "CCP",
                "negative_space": "left_margin",
            },
        ),
    )

    snapshot = SuperVisualSnapshot(
        supervisual_project_id="sv_project_1",
        supervisual_variant_id="sv_variant_1",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        status=SuperVisualVariantStatus.DRAFT,
        step="template_preview_selected",
        preview_ref=preview.thumbnail_uri,
        display_payload={
            "template_preview_result_id": preview.template_preview_result_id,
            "template_id": preview.template_id,
            "source_mode": "template_preview_atlas",
        },
    )

    assert snapshot.preview_ref == preview.thumbnail_uri
    assert snapshot.display_payload["template_preview_result_id"] == preview.template_preview_result_id


def test_carousel_template_preview_indexes_match_preview_pack_sequence_assumption():
    atlas = TemplateAtlasService()
    slot_map = atlas.default_carousel_slot_map()
    preview = atlas.compile_preview_from_payload(
        slot_map=slot_map,
        payload=TemplateSamplePayload(
            template_format=TemplateFormat.CAROUSEL,
            values={
                "carousel_thesis": "A sourced carousel needs a closure contract.",
                "closure_contract": "Close with a source-faithful reframe.",
                "slides": [
                    {"slide_index": 1, "role": "cover_hook", "headline": "Start with the myth."},
                    {"slide_index": 2, "role": "proof_slide", "headline": "Show the source."},
                    {"slide_index": 3, "role": "save_card", "headline": "Keep the reframe."},
                ],
            },
        ),
    )
    pack = CarouselPreviewPack(
        carousel_variant_id="carousel_variant_1",
        slide_receipt_ids=[f"template_preview_slide_{slide.slide_index}" for slide in preview.slides],
    )

    assert [slide.slide_index for slide in preview.slides] == [1, 2, 3]
    assert pack.slide_receipt_ids == [
        "template_preview_slide_1",
        "template_preview_slide_2",
        "template_preview_slide_3",
    ]

