"""Creative library workflow adapter for TS-CMF-020."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.rig_manifest import RigManifest, RigPreviewTest, RigLayer
from ccp_studio.services.creative_library_service import CreativeLibraryService


@dataclass
class CreativeLibraryWorkflow:
    service: CreativeLibraryService

    def create_rig_manifest(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        acting_library_version_id: UUID,
        layers: list[RigLayer],
        mouth_shape_refs: list[str],
        eye_brow_variant_refs: list[str],
        gesture_variant_refs: list[str],
        body_layer_refs: list[str],
        preview_tests: list[RigPreviewTest],
    ) -> RigManifest:
        return self.service.create_rig_manifest(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            acting_library_version_id=acting_library_version_id,
            layers=layers,
            mouth_shape_refs=mouth_shape_refs,
            eye_brow_variant_refs=eye_brow_variant_refs,
            gesture_variant_refs=gesture_variant_refs,
            body_layer_refs=body_layer_refs,
            preview_tests=preview_tests,
        )
