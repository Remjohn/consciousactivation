"""Provider request lineage adapter for TS-CMF-022."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.brand_context_gate import ProviderBrandContextReceipt
from ccp_studio.services.brand_context_gate_service import BrandContextGateService


@dataclass
class ProviderRequestBuilder:
    gate_service: BrandContextGateService

    def bind_brand_context_receipt(self, *, provider_job_id: UUID, scene_spec_id: UUID) -> ProviderBrandContextReceipt:
        return self.gate_service.build_provider_context_receipt(
            provider_job_id=provider_job_id,
            scene_spec_id=scene_spec_id,
        )
