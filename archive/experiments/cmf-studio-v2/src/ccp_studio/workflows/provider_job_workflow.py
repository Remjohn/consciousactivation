"""Provider job workflow for TS-CMF-042, TS-CMF-044, TS-CMF-045, and TS-CMF-048."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.comfy_gpu_worker import GpuWorkerJob
from ccp_studio.contracts.generative_adapters import GenerativeProviderOutput
from ccp_studio.contracts.provider_jobs import ProviderReceipt
from ccp_studio.contracts.provider_recovery import RecoveryActionType, RecoveryReceipt
from ccp_studio.contracts.visual_research import AssetResearchReceipt
from ccp_studio.services.comfy_gpu_worker_service import ComfyGpuWorkerService
from ccp_studio.services.generative_provider_service import GenerativeProviderService
from ccp_studio.services.provider_operations_service import ProviderOperationsService
from ccp_studio.services.provider_recovery_service import ProviderRecoveryService
from ccp_studio.services.visual_research_service import VisualResearchService


@dataclass
class ProviderJobWorkflow:
    service: ProviderOperationsService
    generative_provider_service: GenerativeProviderService | None = None
    comfy_gpu_worker_service: ComfyGpuWorkerService | None = None
    recovery_service: ProviderRecoveryService | None = None
    visual_research_service: VisualResearchService | None = None

    def stage11_provider_execution(
        self,
        *,
        provider_capability_id: str,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        input_artifact_hashes: list[str],
        input_types: list[str],
        idempotency_key: str,
        complete_editing_session_id: UUID | None = None,
        scene_spec_id: UUID | None = None,
        prompt_hash: str | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> ProviderReceipt:
        return self.service.execute_provider_job(
            provider_capability_id=provider_capability_id,
            organization_id=organization_id,
            brand_id=brand_id,
            requested_by_actor_id=actor_id,
            complete_editing_session_id=complete_editing_session_id,
            scene_spec_id=scene_spec_id,
            input_artifact_hashes=input_artifact_hashes,
            input_types=input_types,
            prompt_hash=prompt_hash,
            parameters=parameters,
            idempotency_key=idempotency_key,
        )

    def stage11_generative_provider_adapter(
        self,
        *,
        provider_capability_id: str,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        purpose: str,
        input_artifact_hashes: list[str],
        input_types: list[str],
        parameters: dict[str, Any],
        idempotency_key: str,
        prompt_hash: str | None = None,
        consent_record_version_ids: list[UUID] | None = None,
        requires_consent_compatibility: bool = False,
        evaluation_target_id: UUID | None = None,
    ) -> GenerativeProviderOutput:
        if self.generative_provider_service is None:
            raise RuntimeError("GenerativeProviderService is required for generative provider adapters.")
        return self.generative_provider_service.submit_generative_provider_job(
            provider_capability_id=provider_capability_id,
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            purpose=purpose,
            input_artifact_hashes=input_artifact_hashes,
            input_types=input_types,
            prompt_hash=prompt_hash,
            parameters=parameters,
            consent_record_version_ids=consent_record_version_ids,
            requires_consent_compatibility=requires_consent_compatibility,
            evaluation_target_id=evaluation_target_id,
            idempotency_key=idempotency_key,
        )

    def stage11_comfy_gpu_worker(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        workflow_asset_id: UUID,
        workflow_hash: str,
        input_artifact_hashes: list[str],
        typed_parameters: dict[str, Any],
        cloud_provider: str,
        gpu_tier: str,
        docker_image_digest: str,
        expected_output_count: int,
    ) -> GpuWorkerJob:
        if self.comfy_gpu_worker_service is None:
            raise RuntimeError("ComfyGpuWorkerService is required for ComfyUI GPU workers.")
        return self.comfy_gpu_worker_service.queue_comfy_gpu_worker_job(
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            workflow_asset_id=workflow_asset_id,
            workflow_hash=workflow_hash,
            input_artifact_hashes=input_artifact_hashes,
            typed_parameters=typed_parameters,
            cloud_provider=cloud_provider,
            gpu_tier=gpu_tier,
            docker_image_digest=docker_image_digest,
            expected_output_count=expected_output_count,
        )

    def stage11_12_recovery(
        self,
        *,
        provider_job_id: UUID,
        action_type: RecoveryActionType | str,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        requeued_work_ids: list[str] | None = None,
        missing_work_ids: list[str] | None = None,
        allow_duplicate_cost: bool = False,
        side_effects: list[str] | None = None,
    ) -> RecoveryReceipt:
        if self.recovery_service is None:
            raise RuntimeError("ProviderRecoveryService is required for provider recovery.")
        return self.recovery_service.stage11_12_recovery(
            provider_job_id=provider_job_id,
            action_type=action_type,
            actor_id=actor_id,
            idempotency_key=idempotency_key,
            reason=reason,
            requeued_work_ids=requeued_work_ids,
            missing_work_ids=missing_work_ids,
            allow_duplicate_cost=allow_duplicate_cost,
            side_effects=side_effects,
        )

    def stage11_asset_research(
        self,
        *,
        visual_research_query_id: UUID,
        candidates: list[dict[str, Any]],
        actor_id: UUID,
        downstream_render_route: str,
    ) -> AssetResearchReceipt:
        if self.visual_research_service is None:
            raise RuntimeError("VisualResearchService is required for asset research.")
        return self.visual_research_service.run_asset_research(
            visual_research_query_id=visual_research_query_id,
            candidates=candidates,
            actor_id=actor_id,
            downstream_render_route=downstream_render_route,
        )
