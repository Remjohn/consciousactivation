from __future__ import annotations

import json

from ccp_studio.contracts.template_preview_atlas import (
    FrameProfile,
    TemplateApprovalReceipt,
    TemplateApprovalStatus,
    TemplateAtlas,
    TemplateFormat,
    TemplatePreviewRequest,
    TemplateSamplePayload,
    TemplateSlot,
    TemplateSlotMap,
    TemplateSlotRole,
    TemplateVersion,
    stable_hash,
)
from ccp_studio.repositories.template_preview_atlas import InMemoryTemplatePreviewAtlasRepository
from ccp_studio.services.template_preview_service import TemplatePreviewService


class TemplateAtlasService:
    def __init__(
        self,
        repository: InMemoryTemplatePreviewAtlasRepository | None = None,
        preview_service: TemplatePreviewService | None = None,
    ):
        self.repository = repository or InMemoryTemplatePreviewAtlasRepository()
        self.preview_service = preview_service or TemplatePreviewService()

    def create_atlas(self, atlas_name: str = "CCP Template Atlas V1") -> TemplateAtlas:
        atlas = TemplateAtlas(atlas_name=atlas_name)
        self.repository.upsert("atlases", atlas.template_atlas_id, atlas)
        return atlas

    def default_supervisual_slot_map(self, template_id: str = "supervisual_memory_object_hero") -> TemplateSlotMap:
        return TemplateSlotMap(
            template_id=template_id,
            template_format=TemplateFormat.SUPERVISUAL,
            frame_profile=FrameProfile.ONE_ONE_SOFT_ROUNDED,
            slots=[
                TemplateSlot(slot_key="source_truth", role=TemplateSlotRole.SOURCE_TRUTH, label="Source Truth"),
                TemplateSlot(slot_key="hero_object", role=TemplateSlotRole.HERO_OBJECT, label="Hero Object"),
                TemplateSlot(slot_key="power_phrase", role=TemplateSlotRole.POWER_PHRASE, label="Power Phrase"),
                TemplateSlot(slot_key="brand_mark", role=TemplateSlotRole.BRAND_MARK, label="Brand Mark"),
                TemplateSlot(slot_key="negative_space", role=TemplateSlotRole.NEGATIVE_SPACE, label="Negative Space"),
            ],
        )

    def default_carousel_slot_map(self, template_id: str = "carousel_relief_peak_sequence") -> TemplateSlotMap:
        return TemplateSlotMap(
            template_id=template_id,
            template_format=TemplateFormat.CAROUSEL,
            frame_profile=FrameProfile.FOUR_FIVE_CAROUSEL,
            slots=[
                TemplateSlot(slot_key="carousel_thesis", role=TemplateSlotRole.CAROUSEL_THESIS, label="Carousel Thesis"),
                TemplateSlot(slot_key="closure_contract", role=TemplateSlotRole.CLOSURE_CONTRACT, label="Closure Contract"),
                TemplateSlot(slot_key="slides", role=TemplateSlotRole.SLIDE_SEQUENCE, label="Slide Sequence"),
            ],
        )

    def default_format02_slot_map(self, template_id: str = "format02_avatar_object_scene") -> TemplateSlotMap:
        return TemplateSlotMap(
            template_id=template_id,
            template_format=TemplateFormat.FORMAT02_SCENE,
            frame_profile=FrameProfile.NINE_SIXTEEN_PAPERCUT,
            slots=[
                TemplateSlot(slot_key="concept_statement", role=TemplateSlotRole.CONCEPT_STATEMENT, label="Concept"),
                TemplateSlot(slot_key="headline_text", role=TemplateSlotRole.HEADLINE_TEXT, label="Headline"),
                TemplateSlot(slot_key="avatar_action", role=TemplateSlotRole.AVATAR_ACTION, label="Avatar Action"),
                TemplateSlot(slot_key="hero_object", role=TemplateSlotRole.HERO_OBJECT, label="Hero Object"),
                TemplateSlot(slot_key="audience_proxy", role=TemplateSlotRole.AUDIENCE_PROXY, label="Audience Proxy"),
                TemplateSlot(slot_key="sfl_function", role=TemplateSlotRole.SFL_FUNCTION, label="SFL Function"),
            ],
        )

    def compile_preview_from_payload(
        self,
        *,
        slot_map: TemplateSlotMap,
        payload: TemplateSamplePayload,
    ):
        request = TemplatePreviewRequest(
            template_id=slot_map.template_id,
            template_format=slot_map.template_format,
            slot_map=slot_map,
            sample_payload=payload,
        )
        result = self.preview_service.compile_preview(request)
        self.repository.upsert("slot_maps", slot_map.template_slot_map_id, slot_map)
        self.repository.upsert("sample_payloads", payload.template_sample_payload_id, payload)
        self.repository.upsert("preview_results", result.template_preview_result_id, result)
        return result

    def version_template(self, *, slot_map: TemplateSlotMap, preview_result_id: str | None = None, version: int = 1) -> TemplateVersion:
        slot_dump = []
        for slot in slot_map.slots:
            slot_dump.append(slot.model_dump() if hasattr(slot, "model_dump") else slot.dict())
        source = json.dumps(
            {
                "template_id": slot_map.template_id,
                "template_format": slot_map.template_format.value,
                "frame_profile": slot_map.frame_profile.value,
                "slots": slot_dump,
            },
            sort_keys=True,
        )
        template_version = TemplateVersion(
            template_id=slot_map.template_id,
            version=version,
            template_format=slot_map.template_format,
            slot_map=slot_map,
            template_hash=stable_hash(source),
            preview_result_id=preview_result_id,
        )
        self.repository.upsert("template_versions", template_version.template_version_id, template_version)
        return template_version

    def approve_template(self, *, template_id: str, template_version_id: str, approved_by: str, notes: str | None = None) -> TemplateApprovalReceipt:
        receipt = TemplateApprovalReceipt(
            template_id=template_id,
            template_version_id=template_version_id,
            approval_status=TemplateApprovalStatus.APPROVED,
            approved_by=approved_by,
            notes=notes,
        )
        self.repository.upsert("approval_receipts", receipt.template_approval_receipt_id, receipt)
        return receipt

    def add_to_atlas(self, atlas: TemplateAtlas, version: TemplateVersion, preview, approval: TemplateApprovalReceipt | None = None) -> TemplateAtlas:
        atlas.template_versions.append(version)
        atlas.preview_results.append(preview)
        if approval:
            atlas.approval_receipts.append(approval)
        self.repository.upsert("atlases", atlas.template_atlas_id, atlas)
        return atlas
