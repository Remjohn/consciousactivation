"""Acting library workflow adapter for TS-CMF-019."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.acting_library import ActingLibraryVersion
from ccp_studio.services.acting_library_service import ActingLibraryService


@dataclass
class ActingLibraryWorkflow:
    service: ActingLibraryService

    def generate_grid(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        source_artifact_ids: list[UUID],
        provider_name: str,
    ) -> ActingLibraryVersion:
        return self.service.generate_reference_grid(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            source_artifact_ids=source_artifact_ids,
            provider_name=provider_name,
        )
