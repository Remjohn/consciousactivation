from __future__ import annotations

from ccp_studio.contracts.provider_adapters import (
    ProviderAssetInput,
    ProviderCapabilityId,
    ProviderExecutionRequest,
    ProviderId,
    ProviderJobReceipt,
    ProviderOutputRequirement,
    ProviderPromptContract,
)
from ccp_studio.services.provider_orchestration_service import ProviderOrchestrationService


class SuperVisualProviderMaterializationService:
    """SuperVisual-specific wrapper around provider orchestration.

    SuperVisualBuilderService should call this service, not provider adapters directly.
    """

    def __init__(self, provider_orchestration_service: ProviderOrchestrationService | None = None):
        self.provider_orchestration_service = provider_orchestration_service or ProviderOrchestrationService()

    def materialize_from_blueprint(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        provider_id: ProviderId,
        provider_capability_id: ProviderCapabilityId,
        provider_job_blueprint_id: str,
        route_production_spec_id: str,
        primary_style_route_id: str,
        source_references: list[str],
        frame_profile: str,
        composition_role: str,
        prompt: str,
        negative_prompt: str | None,
        input_assets: list[ProviderAssetInput] | None = None,
        reference_assets: list[ProviderAssetInput] | None = None,
        output_requirements: list[ProviderOutputRequirement] | None = None,
        idempotency_key: str | None = None,
        operator_approval_ref: str | None = None,
        trusted_auto_approval_policy_id: str | None = None,
        allow_fake_without_approval: bool = False,
    ) -> ProviderJobReceipt:
        prompt_contract = ProviderPromptContract(
            primary_prompt=prompt,
            negative_prompt=negative_prompt,
            route_id=primary_style_route_id,
            frame_profile=frame_profile,
            composition_role=composition_role,
            source_reference_ids=source_references,
        )
        request = ProviderExecutionRequest(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            provider_id=provider_id,
            provider_capability_id=provider_capability_id,
            provider_job_blueprint_id=provider_job_blueprint_id,
            route_production_spec_id=route_production_spec_id,
            primary_style_route_id=primary_style_route_id,
            source_references=source_references,
            input_assets=input_assets or [],
            reference_assets=reference_assets or [],
            frame_profile=frame_profile,
            composition_role=composition_role,
            prompt_contract=prompt_contract,
            output_requirements=output_requirements or [ProviderOutputRequirement()],
            idempotency_key=idempotency_key or f"{provider_job_blueprint_id}:{primary_style_route_id}",
            operator_approval_ref=operator_approval_ref,
            trusted_auto_approval_policy_id=trusted_auto_approval_policy_id,
            allow_fake_without_approval=allow_fake_without_approval,
        )
        return self.provider_orchestration_service.run(request)
