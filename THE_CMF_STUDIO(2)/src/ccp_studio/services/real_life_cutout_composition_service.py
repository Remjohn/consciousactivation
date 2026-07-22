from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import CompositionRole, RealLifeCutoutPlacementPlan


class RealLifeCutoutCompositionService:
    def compile_cutout_plan(
        self,
        *,
        asset_id: str,
        source_ref: str,
        role: CompositionRole,
        placement: str,
    ) -> RealLifeCutoutPlacementPlan:
        return RealLifeCutoutPlacementPlan(
            asset_id=asset_id,
            source_ref=source_ref,
            role=role,
            placement=placement,
        )
