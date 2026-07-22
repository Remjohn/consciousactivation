"""Complete Editing Session workflow adapter for TS-CMF-036."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.brand_context_gate import BrandContextGateResult
from ccp_studio.contracts.complete_editing_session import CompleteEditingSession
from ccp_studio.contracts.composition import CompositionPlate
from ccp_studio.contracts.scene_spec import SceneSpec
from ccp_studio.contracts.brand_context_gate import SelectedBrandAssetRef
from ccp_studio.services.complete_editing_session_service import CompleteEditingSessionService


@dataclass
class CompleteEditingSessionWorkflow:
    service: Any
    scene_spec_compiler: Any | None = None
    composition_service: Any | None = None
    scene_intelligence_service: Any | None = None

    def validate_brand_context(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID | None,
    ) -> BrandContextGateResult:
        return self.service.validate_production_context(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
        )

    def stage9_create_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        source_expression_moment_id: UUID,
        asset_route_receipt_id: UUID,
        brand_context_version_id: UUID,
        actor_id: UUID,
        asset_package_item_id: UUID | None = None,
    ) -> CompleteEditingSession:
        service: CompleteEditingSessionService = self.service
        session = service.create_session(
            organization_id=organization_id,
            brand_id=brand_id,
            source_expression_moment_id=source_expression_moment_id,
            asset_route_receipt_id=asset_route_receipt_id,
            asset_package_item_id=asset_package_item_id,
            brand_context_version_id=brand_context_version_id,
            actor_id=actor_id,
        )
        service.start_workflow(
            complete_editing_session_id=session.complete_editing_session_id,
            actor_id=actor_id,
        )
        return session

    def stage9_compile_scene_spec(
        self,
        *,
        complete_editing_session_id: UUID,
        actor_id: UUID,
        selected_asset_refs: list[SelectedBrandAssetRef],
        platform_variants: list[dict[str, Any]],
        revision_policy: dict[str, Any],
        **kwargs: Any,
    ) -> SceneSpec:
        if self.scene_spec_compiler is None:
            raise RuntimeError("SceneSpec compiler must be configured for Stage 9 compilation.")
        return self.scene_spec_compiler.compile_scene_spec(
            complete_editing_session_id=complete_editing_session_id,
            actor_id=actor_id,
            selected_asset_refs=selected_asset_refs,
            platform_variants=platform_variants,
            revision_policy=revision_policy,
            **kwargs,
        )

    def stage10_composition_control(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
    ) -> CompositionPlate:
        if self.composition_service is None:
            raise RuntimeError("Composition service must be configured for Stage 10 composition control.")
        job = self.composition_service.compile_composition_job(scene_spec_id=scene_spec_id, actor_id=actor_id)
        return self.composition_service.submit_ideogram_composition_job(
            composition_job_id=job.composition_job_id,
            actor_id=actor_id,
        )

    def stage9_10_scene_intelligence(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
    ):
        if self.scene_intelligence_service is None:
            raise RuntimeError("Scene intelligence service must be configured for Stage 9/10 orchestration.")
        return self.scene_intelligence_service.run_scene_intelligence(
            scene_spec_id=scene_spec_id,
            actor_id=actor_id,
        )
