"""Brand Genesis workflow adapter for TS-CMF-018."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.brand_genesis import BrandGenesisWorkflowRun
from ccp_studio.services.brand_genesis_service import BrandGenesisService


@dataclass
class BrandGenesisWorkflow:
    service: BrandGenesisService

    def start(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        actor_id: UUID,
    ) -> BrandGenesisWorkflowRun:
        return self.service.start_workflow(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            actor_id=actor_id,
        )
