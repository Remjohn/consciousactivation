from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import (
    LockedCompositionElements,
    ProviderCompositionPlateContract,
    ProviderEditBoundary,
    ProviderName,
    ProviderRole,
)


class ProviderCompositionPlateService:
    def compile_ideogram_plate_contract(
        self,
        *,
        composition_scene_program_id: str,
        locked_elements: LockedCompositionElements,
        placeholder_object_slots: list[str] | None = None,
    ) -> ProviderCompositionPlateContract:
        boundary = ProviderEditBoundary(
            provider_name=ProviderName.IDEOGRAM,
            provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR,
            allowed_edits=["generate_layout_plate", "rough_typography_preview", "placeholder_object_slots"],
            forbidden_edits=["rewrite_text", "change_layout", "invent_claims", "add_extra_objects"],
        )
        return ProviderCompositionPlateContract(
            composition_scene_program_id=composition_scene_program_id,
            locked_elements=locked_elements,
            edit_boundary=boundary,
            placeholder_object_slots=placeholder_object_slots or [],
        )
