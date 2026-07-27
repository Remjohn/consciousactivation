from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import (
    LockedCompositionElements,
    ProviderEditBoundary,
    ProviderName,
    ProviderRole,
    RealLifeCutoutPlacementPlan,
    ReferenceEditContract,
)


class ReferenceEditContractService:
    def compile_flux_reference_edit_contract(
        self,
        *,
        composition_plate_ref: str,
        reference_inputs: list[RealLifeCutoutPlacementPlan],
        locked_elements: LockedCompositionElements,
    ) -> ReferenceEditContract:
        boundary = ProviderEditBoundary(
            provider_name=ProviderName.FLUX,
            provider_role=ProviderRole.REFERENCE_BASED_OBJECT_EDITOR,
            allowed_edits=["replace_placeholder_object", "paperize_reference", "add_contact_shadow", "harmonize_lighting"],
            forbidden_edits=["rewrite_text", "move_avatar", "change_layout", "invent_claims", "add_extra_objects"],
        )
        return ReferenceEditContract(
            composition_plate_ref=composition_plate_ref,
            reference_inputs=reference_inputs,
            locked_elements=locked_elements,
            edit_boundary=boundary,
        )
