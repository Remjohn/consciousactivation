"""Review lineage view adapter for TS-CMF-022."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.brand_context_gate import BrandContextLineageView
from ccp_studio.services.brand_context_gate_service import BrandContextGateService


@dataclass
class ReviewLineageService:
    gate_service: BrandContextGateService

    def view_brand_context_lineage(
        self,
        *,
        downstream_object_id: UUID,
        downstream_object_type: str,
        scene_spec_id: UUID,
    ) -> BrandContextLineageView:
        return self.gate_service.generate_lineage_view(
            downstream_object_id=downstream_object_id,
            downstream_object_type=downstream_object_type,
            scene_spec_id=scene_spec_id,
        )
