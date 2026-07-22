import pytest

from ccp_studio.contracts.template_preview_atlas import (
    FrameProfile,
    TemplateApprovalReceipt,
    TemplateApprovalStatus,
    TemplateFormat,
    TemplatePreviewRequest,
    TemplatePreviewResult,
    TemplateSamplePayload,
    TemplateSlot,
    TemplateSlotMap,
    TemplateSlotRole,
    TemplateVersion,
    svg_to_data_uri,
)
from ccp_studio.services.template_atlas_service import TemplateAtlasService
from ccp_studio.services.template_preview_service import TemplatePreviewService


def _supervisual_payload():
    return TemplateSamplePayload(
        template_format=TemplateFormat.SUPERVISUAL,
        values={
            "source_truth": "I built a life with no recovery margins.",
            "hero_object": "paperized planner cutout",
            "power_phrase": "No recovery margins.",
            "brand_mark": "CCP",
            "negative_space": "lower_third",
        },
    )


def _carousel_payload():
    return TemplateSamplePayload(
        template_format=TemplateFormat.CAROUSEL,
        values={
            "carousel_thesis": "Burnout is not always weakness.",
            "closure_contract": "Source-faithful reframe.",
            "slides": [
                {"slide_index": 1, "role": "cover", "headline": "What if it wasn't weakness?"},
                {"slide_index": 2, "role": "proof", "headline": "No recovery margins."},
                {"slide_index": 3, "role": "save_card", "headline": "Support before collapse."},
            ],
        },
    )


def _format02_payload():
    return TemplateSamplePayload(
        template_format=TemplateFormat.FORMAT02_SCENE,
        values={
            "concept_statement": "Natural does not always mean safe.",
            "headline_text": "Natural ≠ always safe?",
            "avatar_action": "raise_finger",
            "hero_object": "real tea cup cutout",
            "audience_proxy": "confused_seeker",
            "sfl_function": "relevant_open_question",
        },
    )


def test_slot_map_requires_slots():
    with pytest.raises(Exception):
        TemplateSlotMap(
            template_id="template_1",
            template_format=TemplateFormat.SUPERVISUAL,
            frame_profile=FrameProfile.ONE_ONE_SOFT_ROUNDED,
            slots=[],
        )


def test_slot_map_rejects_duplicate_slot_keys():
    slot1 = TemplateSlot(slot_key="source_truth", role=TemplateSlotRole.SOURCE_TRUTH, label="Source Truth")
    slot2 = TemplateSlot(slot_key="source_truth", role=TemplateSlotRole.SOURCE_TRUTH, label="Source Truth Duplicate")
    with pytest.raises(Exception):
        TemplateSlotMap(
            template_id="template_1",
            template_format=TemplateFormat.SUPERVISUAL,
            frame_profile=FrameProfile.ONE_ONE_SOFT_ROUNDED,
            slots=[slot1, slot2],
        )


def test_sample_payload_must_satisfy_required_slots():
    service = TemplateAtlasService()
    slot_map = service.default_supervisual_slot_map()
    payload = TemplateSamplePayload(template_format=TemplateFormat.SUPERVISUAL, values={"source_truth": "truth"})
    with pytest.raises(Exception):
        payload.assert_satisfies(slot_map)


def test_preview_request_blocks_provider_and_renderer_calls():
    service = TemplateAtlasService()
    slot_map = service.default_supervisual_slot_map()
    with pytest.raises(Exception):
        TemplatePreviewRequest(
            template_id=slot_map.template_id,
            template_format=TemplateFormat.SUPERVISUAL,
            slot_map=slot_map,
            sample_payload=_supervisual_payload(),
            provider_calls_allowed=True,
        )
    with pytest.raises(Exception):
        TemplatePreviewRequest(
            template_id=slot_map.template_id,
            template_format=TemplateFormat.SUPERVISUAL,
            slot_map=slot_map,
            sample_payload=_supervisual_payload(),
            renderer_calls_allowed=True,
        )


def test_supervisual_preview_compiles_svg_and_thumbnail():
    service = TemplateAtlasService()
    slot_map = service.default_supervisual_slot_map()
    preview = service.compile_preview_from_payload(slot_map=slot_map, payload=_supervisual_payload())
    assert preview.template_format == TemplateFormat.SUPERVISUAL
    assert preview.preview_svg.startswith("<svg")
    assert preview.thumbnail_uri.startswith("data:image/svg+xml;base64,")
    assert preview.single_source_truth


def test_carousel_preview_compiles_continuous_slides():
    service = TemplateAtlasService()
    slot_map = service.default_carousel_slot_map()
    preview = service.compile_preview_from_payload(slot_map=slot_map, payload=_carousel_payload())
    assert preview.template_format == TemplateFormat.CAROUSEL
    assert [slide.slide_index for slide in preview.slides] == [1, 2, 3]
    assert preview.preview_svg.startswith("<svg")


def test_carousel_preview_rejects_non_continuous_slide_indexes():
    service = TemplateAtlasService()
    slot_map = service.default_carousel_slot_map()
    payload = TemplateSamplePayload(
        template_format=TemplateFormat.CAROUSEL,
        values={
            "carousel_thesis": "Thesis",
            "closure_contract": "Close",
            "slides": [
                {"slide_index": 1, "role": "cover", "headline": "Cover"},
                {"slide_index": 3, "role": "payoff", "headline": "Payoff"},
            ],
        },
    )
    with pytest.raises(Exception):
        service.compile_preview_from_payload(slot_map=slot_map, payload=payload)


def test_format02_preview_compiles_avatar_object_proxy_slots():
    service = TemplateAtlasService()
    slot_map = service.default_format02_slot_map()
    preview = service.compile_preview_from_payload(slot_map=slot_map, payload=_format02_payload())
    assert preview.template_format == TemplateFormat.FORMAT02_SCENE
    assert preview.avatar_action == "raise_finger"
    assert preview.audience_proxy == "confused_seeker"
    assert preview.sfl_function == "relevant_open_question"
    assert preview.preview_svg.startswith("<svg")


def test_format02_preview_rejects_too_many_visible_words():
    service = TemplateAtlasService()
    slot_map = service.default_format02_slot_map()
    payload = TemplateSamplePayload(
        template_format=TemplateFormat.FORMAT02_SCENE,
        values={
            "concept_statement": "Overloaded",
            "headline_text": "This headline has far too many visible words for the format two preview budget limit",
            "avatar_action": "point",
            "hero_object": "object",
            "audience_proxy": "confused_seeker",
            "sfl_function": "open_question",
        },
    )
    with pytest.raises(Exception):
        service.compile_preview_from_payload(slot_map=slot_map, payload=payload)


def test_generic_preview_service_routes_to_format02():
    atlas = TemplateAtlasService()
    slot_map = atlas.default_format02_slot_map()
    request = TemplatePreviewRequest(
        template_id=slot_map.template_id,
        template_format=TemplateFormat.FORMAT02_SCENE,
        slot_map=slot_map,
        sample_payload=_format02_payload(),
    )
    preview = TemplatePreviewService().compile_preview(request)
    assert preview.template_format == TemplateFormat.FORMAT02_SCENE


def test_template_version_requires_hash():
    service = TemplateAtlasService()
    slot_map = service.default_supervisual_slot_map()
    with pytest.raises(Exception):
        TemplateVersion(
            template_id=slot_map.template_id,
            version=1,
            template_format=TemplateFormat.SUPERVISUAL,
            slot_map=slot_map,
            template_hash="",
        )


def test_template_version_matches_slot_map_format():
    service = TemplateAtlasService()
    slot_map = service.default_supervisual_slot_map()
    with pytest.raises(Exception):
        TemplateVersion(
            template_id=slot_map.template_id,
            version=1,
            template_format=TemplateFormat.CAROUSEL,
            slot_map=slot_map,
            template_hash="hash",
        )


def test_template_approval_cannot_pass_with_blockers():
    with pytest.raises(Exception):
        TemplateApprovalReceipt(
            template_id="template_1",
            template_version_id="version_1",
            approval_status=TemplateApprovalStatus.APPROVED,
            approved_by="operator",
            blockers=["missing preview"],
        )


def test_template_approval_requires_approved_by_when_approved():
    with pytest.raises(Exception):
        TemplateApprovalReceipt(
            template_id="template_1",
            template_version_id="version_1",
            approval_status=TemplateApprovalStatus.APPROVED,
        )


def test_atlas_registers_preview_version_and_approval():
    service = TemplateAtlasService()
    atlas = service.create_atlas()
    slot_map = service.default_supervisual_slot_map()
    preview = service.compile_preview_from_payload(slot_map=slot_map, payload=_supervisual_payload())
    version = service.version_template(slot_map=slot_map, preview_result_id=preview.template_preview_result_id)
    approval = service.approve_template(template_id=slot_map.template_id, template_version_id=version.template_version_id, approved_by="operator")
    atlas = service.add_to_atlas(atlas, version, preview, approval)
    assert len(atlas.template_versions) == 1
    assert len(atlas.preview_results) == 1
    assert len(atlas.approval_receipts) == 1


def test_template_result_rejects_non_svg_preview():
    with pytest.raises(Exception):
        TemplatePreviewResult(
            template_id="template_1",
            template_format=TemplateFormat.SUPERVISUAL,
            frame_profile=FrameProfile.ONE_ONE_SOFT_ROUNDED,
            slot_labels={},
            sample_values={},
            preview_svg="not svg",
            thumbnail_uri="data:image/svg+xml;base64,abc",
        )


def test_template_result_rejects_provider_execution_flag():
    svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    with pytest.raises(Exception):
        TemplatePreviewResult(
            template_id="template_1",
            template_format=TemplateFormat.SUPERVISUAL,
            frame_profile=FrameProfile.ONE_ONE_SOFT_ROUNDED,
            slot_labels={},
            sample_values={},
            preview_svg=svg,
            thumbnail_uri=svg_to_data_uri(svg),
            provider_calls_executed=True,
        )


def test_default_slot_maps_have_expected_frame_profiles():
    service = TemplateAtlasService()
    assert service.default_supervisual_slot_map().frame_profile == FrameProfile.ONE_ONE_SOFT_ROUNDED
    assert service.default_carousel_slot_map().frame_profile == FrameProfile.FOUR_FIVE_CAROUSEL
    assert service.default_format02_slot_map().frame_profile == FrameProfile.NINE_SIXTEEN_PAPERCUT
