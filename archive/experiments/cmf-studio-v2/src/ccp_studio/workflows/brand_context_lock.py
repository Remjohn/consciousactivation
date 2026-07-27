"""Brand Context lock workflow adapter for TS-CMF-021."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.brand_context import BrandContextAssetBundle, BrandContextVersion
from ccp_studio.services.brand_context_service import BrandContextService


@dataclass
class BrandContextLockWorkflow:
    service: BrandContextService

    def create_and_lock(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        asset_bundle: BrandContextAssetBundle,
        actor_id: UUID,
    ) -> BrandContextVersion:
        draft = self.service.create_draft(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            asset_bundle=asset_bundle,
            created_by_actor_id=actor_id,
        )
        return self.service.lock_version(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_context_version_id=draft.brand_context_version_id,
            approved_by_actor_id=actor_id,
        )
